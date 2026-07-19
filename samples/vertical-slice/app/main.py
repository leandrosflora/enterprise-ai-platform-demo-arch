from __future__ import annotations

import json
import logging
import os
import time
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

try:
    from aiokafka import AIOKafkaProducer
except ImportError:  # pragma: no cover - permits contract tests without Kafka dependency
    AIOKafkaProducer = None  # type: ignore[assignment,misc]

try:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
except ImportError:  # pragma: no cover
    trace = None  # type: ignore[assignment]

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(message)s")
logger = logging.getLogger("enterprise-ai-platform-demo")

INVOCATIONS = Counter(
    "agent_invocations_total",
    "Agent invocations",
    ["agent_id", "status"],
)
INVOCATION_DURATION = Histogram(
    "agent_invocation_duration_seconds",
    "Agent invocation duration",
    ["agent_id", "workload_class"],
)
POLICY_DENIALS = Counter(
    "policy_denials_total",
    "Policy denials",
    ["resource_type", "reason"],
)
MODEL_COST = Counter(
    "model_cost_usd_total",
    "Estimated model cost",
    ["agent_id", "model_id"],
)


class ModelPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capability: str = "TEXT_GENERATION"
    preferredModels: list[str] = Field(default_factory=lambda: ["demo.deterministic-model"])
    maxInputTokens: int = Field(default=8000, ge=1)
    maxOutputTokens: int = Field(default=1200, ge=1)
    temperature: float = Field(default=0.2, ge=0, le=2)
    maxCostUsd: float = Field(default=0.05, ge=0)


class AgentCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agentId: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{2,63}$")
    name: str
    version: str
    owner: str
    businessUnit: str | None = None
    instructions: str = Field(min_length=1)
    riskClassification: str = Field(pattern=r"^(LOW|MEDIUM|HIGH|CRITICAL)$")
    modelPolicy: ModelPolicy
    allowedTools: list[str] = Field(default_factory=list)
    knowledgeBaseIds: list[str] = Field(default_factory=list)


class GovernanceSubmission(BaseModel):
    agentVersion: str
    riskClassification: str = Field(pattern=r"^(LOW|MEDIUM|HIGH|CRITICAL)$")
    evidence: list[str] = Field(min_length=1)
    notes: str | None = None


class GovernanceDecisionRequest(BaseModel):
    reason: str = Field(min_length=10)
    conditions: list[str] = Field(default_factory=list)


class PublishRequest(BaseModel):
    approvalId: str
    releaseNotes: str | None = None


class InvokeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    input: str = Field(min_length=1, max_length=50000)
    channel: str
    sessionId: str
    executionMode: str = Field(default="SYNC", pattern=r"^(SYNC|ASYNC)$")
    context: dict[str, Any] = Field(default_factory=dict)


@dataclass
class AgentRecord:
    spec: AgentCreateRequest
    status: str = "DRAFT"
    submitted_by: str | None = None
    approval_id: str | None = None
    decided_by: str | None = None
    created_at: str = ""
    updated_at: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            **self.spec.model_dump(),
            "status": self.status,
            "approvalId": self.approval_id,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }


class EventPublisher:
    def __init__(self) -> None:
        self._producer: Any = None
        self.events: list[dict[str, Any]] = []

    async def start(self) -> None:
        bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        if not bootstrap or AIOKafkaProducer is None:
            logger.info(json.dumps({"event": "kafka.disabled"}))
            return

        self._producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap,
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        )
        try:
            await self._producer.start()
            logger.info(json.dumps({"event": "kafka.connected", "bootstrap": bootstrap}))
        except Exception as exc:  # pragma: no cover - infrastructure dependent
            logger.warning(json.dumps({"event": "kafka.unavailable", "error": type(exc).__name__}))
            self._producer = None

    async def stop(self) -> None:
        if self._producer is not None:
            await self._producer.stop()

    async def publish(
        self,
        event_type: str,
        correlation_id: str,
        tenant_id: str,
        source: str,
        payload: dict[str, Any],
        data_classification: str = "INTERNAL",
        causation_id: str | None = None,
    ) -> dict[str, Any]:
        envelope = {
            "eventId": str(uuid.uuid4()),
            "eventType": event_type,
            "schemaVersion": "1.0.0",
            "occurredAt": datetime.now(UTC).isoformat(),
            "correlationId": correlation_id,
            "causationId": causation_id,
            "tenantId": tenant_id,
            "source": source,
            "dataClassification": data_classification,
            "payload": payload,
        }
        self.events.append(envelope)
        self.events[:] = self.events[-200:]

        if self._producer is not None:
            topic = f"{event_type}.v1"
            try:
                await self._producer.send_and_wait(topic, envelope, key=tenant_id.encode("utf-8"))
            except Exception as exc:  # pragma: no cover
                logger.warning(json.dumps({"event": "kafka.publish_failed", "type": event_type, "error": type(exc).__name__}))

        logger.info(json.dumps(envelope, ensure_ascii=False))
        return envelope


agents: dict[str, AgentRecord] = {}
event_publisher = EventPublisher()


def configure_tracing() -> None:
    if trace is None:
        return
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    provider = TracerProvider(resource=Resource.create({"service.name": "enterprise-ai-platform-demo"}))
    if endpoint:
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True)))
    trace.set_tracer_provider(provider)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await event_publisher.start()
    yield
    await event_publisher.stop()


configure_tracing()
app = FastAPI(
    title="Enterprise AI Platform Vertical Slice",
    version="1.1.0",
    lifespan=lifespan,
)
if trace is not None:
    FastAPIInstrumentor.instrument_app(app)


@app.middleware("http")
async def correlation_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-Id") or str(uuid.uuid4())
    request.state.correlation_id = correlation_id
    started = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Correlation-Id"] = correlation_id
    logger.info(
        json.dumps(
            {
                "event": "http.request.completed",
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "durationMs": round((time.perf_counter() - started) * 1000, 2),
                "correlationId": correlation_id,
            }
        )
    )
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    correlation_id = getattr(request.state, "correlation_id", str(uuid.uuid4()))
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": f"https://enterprise-ai-platform.example.com/problems/{exc.status_code}",
            "title": str(exc.detail),
            "status": exc.status_code,
            "correlationId": correlation_id,
        },
        media_type="application/problem+json",
    )


def require_scope(required: str):
    async def dependency(
        scopes_header: Annotated[str | None, Header(alias="X-Demo-Scopes")] = None,
    ) -> None:
        scopes = set((scopes_header or "").split())
        if required not in scopes:
            POLICY_DENIALS.labels("api", "missing_scope").inc()
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing scope: {required}")

    return dependency


def tenant_id(value: Annotated[str | None, Header(alias="X-Demo-Tenant")] = None) -> str:
    return value or "enterprise"


def actor_id(value: Annotated[str | None, Header(alias="X-Demo-Actor")] = None) -> str:
    return value or "demo-user"


def require_idempotency(value: Annotated[str | None, Header(alias="Idempotency-Key")] = None) -> str:
    if value is None or len(value) < 16:
        raise HTTPException(status_code=400, detail="Idempotency-Key with at least 16 characters is required")
    return value


def get_agent(agent_id: str) -> AgentRecord:
    record = agents.get(agent_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return record


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics", include_in_schema=False)
async def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/v1/events")
async def list_events(_: None = Depends(require_scope("audit.read"))) -> dict[str, Any]:
    return {"items": event_publisher.events}


@app.get("/v1/agents")
async def list_agents(_: None = Depends(require_scope("agent.read"))) -> dict[str, Any]:
    return {"items": [record.as_dict() for record in agents.values()]}


@app.post("/v1/agents", status_code=201)
async def create_agent(
    spec: AgentCreateRequest,
    request: Request,
    tenant: str = Depends(tenant_id),
    _: str = Depends(require_idempotency),
    __: None = Depends(require_scope("agent.write")),
) -> dict[str, Any]:
    if spec.agentId in agents:
        raise HTTPException(status_code=409, detail="Agent already exists")
    now = datetime.now(UTC).isoformat()
    record = AgentRecord(spec=spec, created_at=now, updated_at=now)
    agents[spec.agentId] = record
    await event_publisher.publish(
        "agent.created",
        request.state.correlation_id,
        tenant,
        "agent-registry",
        {
            "agentId": spec.agentId,
            "agentVersion": spec.version,
            "status": record.status,
            "owner": spec.owner,
            "businessUnit": spec.businessUnit,
            "riskClassification": spec.riskClassification,
        },
    )
    return record.as_dict()


@app.post("/v1/agents/{agent_id}:submit", status_code=202)
async def submit_agent(
    agent_id: str,
    body: GovernanceSubmission,
    request: Request,
    actor: str = Depends(actor_id),
    tenant: str = Depends(tenant_id),
    _: str = Depends(require_idempotency),
    __: None = Depends(require_scope("governance.submit")),
) -> dict[str, Any]:
    record = get_agent(agent_id)
    if record.status != "DRAFT" or body.agentVersion != record.spec.version:
        raise HTTPException(status_code=409, detail="Agent must be DRAFT and version must match")
    if record.spec.riskClassification in {"HIGH", "CRITICAL"} and len(body.evidence) < 3:
        raise HTTPException(status_code=422, detail="HIGH/CRITICAL agents require at least three evidence items")
    record.status = "SUBMITTED"
    record.submitted_by = actor
    record.updated_at = datetime.now(UTC).isoformat()
    approval_id = f"apv-{uuid.uuid4().hex[:10]}"
    record.approval_id = approval_id
    await event_publisher.publish(
        "evaluation.started",
        request.state.correlation_id,
        tenant,
        "evaluation-service",
        {"evaluationId": f"eval-{uuid.uuid4().hex[:8]}", "agentId": agent_id, "status": "QUEUED"},
    )
    return {
        "approvalId": approval_id,
        "agentId": agent_id,
        "decision": "PENDING",
        "riskClassification": record.spec.riskClassification,
    }


@app.post("/v1/agents/{agent_id}:approve")
async def approve_agent(
    agent_id: str,
    body: GovernanceDecisionRequest,
    request: Request,
    actor: str = Depends(actor_id),
    tenant: str = Depends(tenant_id),
    _: str = Depends(require_idempotency),
    __: None = Depends(require_scope("governance.approve")),
) -> dict[str, Any]:
    record = get_agent(agent_id)
    if record.status != "SUBMITTED":
        raise HTTPException(status_code=409, detail="Agent must be SUBMITTED")
    if actor == record.submitted_by:
        raise HTTPException(status_code=422, detail="Submitter cannot approve the same agent")
    record.status = "APPROVED"
    record.decided_by = actor
    record.updated_at = datetime.now(UTC).isoformat()
    await event_publisher.publish(
        "governance.approved",
        request.state.correlation_id,
        tenant,
        "governance-service",
        {
            "approvalId": record.approval_id,
            "agentId": agent_id,
            "agentVersion": record.spec.version,
            "decision": "APPROVED",
            "riskClassification": record.spec.riskClassification,
            "decidedBy": actor,
            "conditions": body.conditions,
        },
    )
    return {
        "approvalId": record.approval_id,
        "agentId": agent_id,
        "decision": "APPROVED",
        "riskClassification": record.spec.riskClassification,
        "decidedBy": actor,
        "decidedAt": record.updated_at,
    }


@app.post("/v1/agents/{agent_id}:publish", status_code=202)
async def publish_agent(
    agent_id: str,
    body: PublishRequest,
    request: Request,
    tenant: str = Depends(tenant_id),
    _: str = Depends(require_idempotency),
    __: None = Depends(require_scope("agent.publish")),
) -> dict[str, Any]:
    record = get_agent(agent_id)
    if record.status != "APPROVED" or body.approvalId != record.approval_id:
        raise HTTPException(status_code=422, detail="Agent requires matching APPROVED decision")
    record.status = "PUBLISHED"
    record.updated_at = datetime.now(UTC).isoformat()
    await event_publisher.publish(
        "agent.published",
        request.state.correlation_id,
        tenant,
        "governance-service",
        {
            "agentId": agent_id,
            "agentVersion": record.spec.version,
            "status": record.status,
            "owner": record.spec.owner,
            "riskClassification": record.spec.riskClassification,
        },
    )
    return record.as_dict()


async def invoke_model_gateway(agent_id: str, user_input: str) -> tuple[str, dict[str, Any]]:
    model_id = "demo.deterministic-model"
    answer = (
        "A política de retenção exige finalidade aprovada, prazo definido e descarte "
        "ou anonimização ao término do período aplicável."
    )
    input_tokens = max(1, len(user_input.split()) * 2)
    output_tokens = len(answer.split()) * 2
    cost = round((input_tokens + output_tokens) * 0.000002, 6)
    MODEL_COST.labels(agent_id, model_id).inc(cost)
    return answer, {
        "provider": "demo",
        "modelId": model_id,
        "inputTokens": input_tokens,
        "outputTokens": output_tokens,
        "costUsd": cost,
        "latencyMs": 5,
        "status": "SUCCESS",
    }


@app.post("/v1/agents/{agent_id}:invoke")
async def invoke_agent(
    agent_id: str,
    body: InvokeRequest,
    request: Request,
    tenant: str = Depends(tenant_id),
    _: None = Depends(require_scope("agent.invoke")),
) -> dict[str, Any]:
    record = get_agent(agent_id)
    if record.status != "PUBLISHED":
        POLICY_DENIALS.labels("agent", "not_published").inc()
        raise HTTPException(status_code=422, detail="Only PUBLISHED agents can be invoked")

    if body.executionMode == "ASYNC":
        return JSONResponse(
            status_code=202,
            content={
                "executionId": f"exec-{uuid.uuid4().hex[:12]}",
                "status": "QUEUED",
                "statusUri": f"/v1/executions/exec-{uuid.uuid4().hex[:12]}",
            },
        )

    started = time.perf_counter()
    workload_class = "INTERACTIVE_RAG"
    with INVOCATION_DURATION.labels(agent_id, workload_class).time():
        answer, model_usage = await invoke_model_gateway(agent_id, body.input)

    latency_ms = int((time.perf_counter() - started) * 1000)
    message_id = f"msg-{uuid.uuid4().hex[:12]}"
    conversation_id = f"conv-{uuid.uuid4().hex[:12]}"

    await event_publisher.publish(
        "tool.executed",
        request.state.correlation_id,
        tenant,
        "agent-runtime",
        {
            "agentId": agent_id,
            "agentVersion": record.spec.version,
            "toolName": "policy-document-search",
            "toolVersion": "1.0.0",
            "status": "SUCCESS",
            "latencyMs": 3,
            "operationId": f"op-{uuid.uuid4().hex[:8]}",
        },
        causation_id=message_id,
    )
    await event_publisher.publish(
        "model.invoked",
        request.state.correlation_id,
        tenant,
        "model-gateway",
        {"agentId": agent_id, **model_usage},
        causation_id=message_id,
    )
    await event_publisher.publish(
        "agent.invoked",
        request.state.correlation_id,
        tenant,
        "agent-runtime",
        {
            "agentId": agent_id,
            "agentVersion": record.spec.version,
            "channel": body.channel,
            "status": "SUCCESS",
            "latencyMs": latency_ms,
            "inputTokens": model_usage["inputTokens"],
            "outputTokens": model_usage["outputTokens"],
            "costUsd": model_usage["costUsd"],
            "evaluationStatus": "QUEUED",
        },
        causation_id=message_id,
    )
    INVOCATIONS.labels(agent_id, "SUCCESS").inc()

    return {
        "conversationId": conversation_id,
        "messageId": message_id,
        "answer": answer,
        "executionStatus": "SUCCESS",
        "citations": [
            {
                "sourceId": "policy-lgpd-001",
                "title": "Política Corporativa de Privacidade e Retenção",
                "uri": "s3://demo/policies/lgpd-retention.md",
                "chunkId": "chunk-014",
                "score": 0.93,
                "dataClassification": "INTERNAL",
            }
        ],
        "toolCalls": [
            {
                "toolName": "policy-document-search",
                "toolVersion": "1.0.0",
                "status": "SUCCESS",
                "latencyMs": 3,
            }
        ],
        "tokenUsage": {
            "inputTokens": model_usage["inputTokens"],
            "outputTokens": model_usage["outputTokens"],
            "totalCostUsd": model_usage["costUsd"],
            "currency": "USD",
        },
        "evaluationStatus": "QUEUED",
    }
