from __future__ import annotations

import hashlib
import re
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any, Literal

from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response, status
from pydantic import BaseModel, ConfigDict, Field, model_validator

try:
    from .main import (
        POLICY_DENIALS,
        actor_id,
        event_publisher,
        require_idempotency,
        require_scope,
        tenant_id,
    )
except ImportError:  # Docker executes modules directly from /app
    from main import (  # type: ignore
        POLICY_DENIALS,
        actor_id,
        event_publisher,
        require_idempotency,
        require_scope,
        tenant_id,
    )

router = APIRouter()

Classification = Literal["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"]
MemoryType = Literal["SESSION", "SHORT_TERM", "LONG_TERM", "PROFILE"]
MemorySource = Literal["USER_CONFIRMED", "SYSTEM_VERIFIED", "TOOL_OUTPUT", "MODEL_INFERRED"]

CLASSIFICATION_RANK = {
    "PUBLIC": 0,
    "INTERNAL": 1,
    "CONFIDENTIAL": 2,
    "RESTRICTED": 3,
}
MEMORY_TTL_CAPS = {
    "SESSION": 86_400,
    "SHORT_TERM": 604_800,
    "LONG_TERM": 31_536_000,
    "PROFILE": 31_536_000,
}
PROMPT_INJECTION_PATTERNS = {
    "ignore_previous_instructions": re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.I),
    "reveal_system_prompt": re.compile(r"(reveal|show|print)\s+(the\s+)?system\s+prompt", re.I),
    "override_policy": re.compile(r"(override|bypass|disable)\s+(security|policy|guardrail)", re.I),
    "execute_hidden_tool": re.compile(r"(execute|call|invoke)\s+(a\s+)?hidden\s+tool", re.I),
    "developer_message_spoofing": re.compile(r"(developer|system)\s+message\s*:", re.I),
}
MALWARE_PATTERNS = {
    "eicar_test_signature": re.compile(r"EICAR-STANDARD-ANTIVIRUS-TEST-FILE", re.I),
    "script_payload": re.compile(r"<script\b", re.I),
}


class AccessPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    allowedRoles: list[str] = Field(default_factory=lambda: ["employee"])
    allowedSubjects: list[str] = Field(default_factory=list)
    deniedRoles: list[str] = Field(default_factory=list)
    allowedPurposes: list[str] = Field(default_factory=lambda: ["ASSISTANCE"])


class Provenance(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sourceSystem: str
    sourceUri: str
    checksum: str | None = None
    approvedSource: bool = False
    ingestedBy: str | None = None


class RetentionPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    retentionDays: int = Field(default=365, ge=1, le=3650)
    deletionMode: Literal["DELETE", "ANONYMIZE"] = "DELETE"


class SecureDocumentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    documentId: str
    title: str
    content: str = Field(min_length=1, max_length=200_000)
    classification: Classification
    accessPolicy: AccessPolicy
    provenance: Provenance
    retentionPolicy: RetentionPolicy = Field(default_factory=RetentionPolicy)


class KnowledgeSearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1, max_length=10_000)
    topK: int = Field(default=5, ge=1, le=50)
    purpose: str = "ASSISTANCE"


class MemoryItemInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str = Field(min_length=1, max_length=100)
    value: str = Field(min_length=1, max_length=10_000)
    classification: Classification = "INTERNAL"
    source: MemorySource
    confidence: float = Field(default=1.0, ge=0, le=1)


class MemoryWriteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    memoryType: MemoryType
    purpose: str = Field(min_length=3, max_length=200)
    ttlSeconds: int = Field(ge=60, le=31_536_000)
    consentReference: str | None = None
    items: list[MemoryItemInput] = Field(min_length=1, max_length=50)

    @model_validator(mode="after")
    def validate_consent_and_ttl(self) -> "MemoryWriteRequest":
        if self.memoryType in {"LONG_TERM", "PROFILE"} and not self.consentReference:
            raise ValueError("LONG_TERM and PROFILE memory require consentReference")
        if self.ttlSeconds > MEMORY_TTL_CAPS[self.memoryType]:
            raise ValueError(f"ttlSeconds exceeds the cap for {self.memoryType}")
        return self


@dataclass
class SecureDocument:
    tenant_id: str
    knowledge_base_id: str
    request: SecureDocumentRequest
    status: str
    quarantine_reasons: list[str]
    checksum: str
    expires_at: str


@dataclass
class MemoryRecord:
    tenant_id: str
    session_id: str
    subject_hash: str
    memory_type: str
    purpose: str
    consent_reference: str | None
    items: list[dict[str, Any]]
    created_at: str
    updated_at: str
    expires_at: str
    version: int = 1

    def as_dict(self) -> dict[str, Any]:
        return {
            "sessionId": self.session_id,
            "subjectHash": self.subject_hash,
            "memoryType": self.memory_type,
            "purpose": self.purpose,
            "consentReference": self.consent_reference,
            "items": self.items,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "expiresAt": self.expires_at,
            "version": self.version,
        }


knowledge_documents: dict[tuple[str, str, str], SecureDocument] = {}
memory_records: dict[tuple[str, str, str], MemoryRecord] = {}


def subject_hash(subject: str) -> str:
    return hashlib.sha256(subject.encode("utf-8")).hexdigest()[:24]


def detect_patterns(text: str, patterns: dict[str, re.Pattern[str]]) -> list[str]:
    return [name for name, pattern in patterns.items() if pattern.search(text)]


def sanitize_untrusted_content(text: str) -> tuple[str, list[str]]:
    removed: list[str] = []
    safe_lines: list[str] = []
    for line in text.splitlines():
        matches = detect_patterns(line, PROMPT_INJECTION_PATTERNS)
        if matches:
            removed.extend(matches)
            continue
        safe_lines.append(line)
    sanitized = "\n".join(safe_lines).strip()
    return f"<untrusted_document>\n{sanitized}\n</untrusted_document>", sorted(set(removed))


def roles_header(value: Annotated[str | None, Header(alias="X-Demo-Roles")] = None) -> set[str]:
    return set((value or "employee").split())


def clearance_header(
    value: Annotated[str | None, Header(alias="X-Demo-Clearance")] = None,
) -> str:
    clearance = (value or "INTERNAL").upper()
    if clearance not in CLASSIFICATION_RANK:
        raise HTTPException(status_code=400, detail="Invalid X-Demo-Clearance")
    return clearance


def subject_header(
    value: Annotated[str | None, Header(alias="X-Demo-Subject")] = None,
) -> str:
    return value or "demo-subject"


def document_is_authorized(
    document: SecureDocument,
    roles: set[str],
    subject: str,
    clearance: str,
    purpose: str,
) -> bool:
    policy = document.request.accessPolicy
    if document.status != "INDEXED":
        return False
    if roles.intersection(policy.deniedRoles):
        return False
    subject_allowed = not policy.allowedSubjects or subject in policy.allowedSubjects
    role_allowed = not policy.allowedRoles or bool(roles.intersection(policy.allowedRoles))
    purpose_allowed = purpose in policy.allowedPurposes
    clearance_allowed = (
        CLASSIFICATION_RANK[clearance]
        >= CLASSIFICATION_RANK[document.request.classification]
    )
    return subject_allowed and role_allowed and purpose_allowed and clearance_allowed


def reset_security_state() -> None:
    knowledge_documents.clear()
    memory_records.clear()
    request = SecureDocumentRequest(
        documentId="policy-lgpd-001",
        title="Política Corporativa de Privacidade e Retenção",
        content=(
            "A retenção exige finalidade aprovada, prazo definido e descarte ou "
            "anonimização ao término do período aplicável."
        ),
        classification="INTERNAL",
        accessPolicy=AccessPolicy(
            allowedRoles=["employee", "governance"],
            allowedPurposes=["ASSISTANCE", "AUDIT"],
        ),
        provenance=Provenance(
            sourceSystem="policy-repository",
            sourceUri="s3://demo/policies/lgpd-retention.md",
            approvedSource=True,
            ingestedBy="bootstrap",
        ),
        retentionPolicy=RetentionPolicy(retentionDays=365),
    )
    checksum = hashlib.sha256(request.content.encode("utf-8")).hexdigest()
    knowledge_documents[("enterprise", "corporate-policies-kb", request.documentId)] = (
        SecureDocument(
            tenant_id="enterprise",
            knowledge_base_id="corporate-policies-kb",
            request=request,
            status="INDEXED",
            quarantine_reasons=[],
            checksum=checksum,
            expires_at=(datetime.now(UTC) + timedelta(days=365)).isoformat(),
        )
    )


reset_security_state()


@router.post("/v1/knowledge-bases/{knowledge_base_id}/documents", status_code=202)
async def ingest_secure_document(
    knowledge_base_id: str,
    body: SecureDocumentRequest,
    request: Request,
    tenant: str = Depends(tenant_id),
    actor: str = Depends(actor_id),
    _: str = Depends(require_idempotency),
    __: None = Depends(require_scope("knowledge.write")),
) -> dict[str, Any]:
    checksum = hashlib.sha256(body.content.encode("utf-8")).hexdigest()
    quarantine_reasons: list[str] = []
    if not body.provenance.approvedSource:
        quarantine_reasons.append("source_not_approved")
    if body.provenance.checksum and body.provenance.checksum != checksum:
        quarantine_reasons.append("checksum_mismatch")
    quarantine_reasons.extend(detect_patterns(body.content, PROMPT_INJECTION_PATTERNS))
    quarantine_reasons.extend(detect_patterns(body.content, MALWARE_PATTERNS))
    quarantine_reasons = sorted(set(quarantine_reasons))
    document_status = "QUARANTINED" if quarantine_reasons else "INDEXED"
    body.provenance.ingestedBy = body.provenance.ingestedBy or actor
    record = SecureDocument(
        tenant_id=tenant,
        knowledge_base_id=knowledge_base_id,
        request=body,
        status=document_status,
        quarantine_reasons=quarantine_reasons,
        checksum=checksum,
        expires_at=(
            datetime.now(UTC) + timedelta(days=body.retentionPolicy.retentionDays)
        ).isoformat(),
    )
    knowledge_documents[(tenant, knowledge_base_id, body.documentId)] = record
    await event_publisher.publish(
        "knowledge.ingested",
        request.state.correlation_id,
        tenant,
        "knowledge-service",
        {
            "knowledgeBaseId": knowledge_base_id,
            "documentId": body.documentId,
            "status": document_status,
            "classification": body.classification,
            "quarantineReasons": quarantine_reasons,
            "checksum": checksum,
        },
        data_classification=body.classification,
    )
    return {
        "ingestionId": f"ing-{uuid.uuid4().hex[:12]}",
        "documentId": body.documentId,
        "status": document_status,
        "quarantineReasons": quarantine_reasons,
        "checksum": checksum,
    }


@router.post("/v1/knowledge-bases/{knowledge_base_id}:search")
async def secure_knowledge_search(
    knowledge_base_id: str,
    body: KnowledgeSearchRequest,
    tenant: str = Depends(tenant_id),
    roles: set[str] = Depends(roles_header),
    clearance: str = Depends(clearance_header),
    subject: str = Depends(subject_header),
    _: None = Depends(require_scope("knowledge.read")),
) -> dict[str, Any]:
    policy_decision_id = f"pd-{uuid.uuid4().hex[:12]}"
    query_terms = set(re.findall(r"\w+", body.query.lower()))
    authorized_results: list[dict[str, Any]] = []
    denied_count = 0

    for (document_tenant, kb_id, _), document in knowledge_documents.items():
        if document_tenant != tenant or kb_id != knowledge_base_id:
            continue
        if not document_is_authorized(document, roles, subject, clearance, body.purpose):
            denied_count += 1
            continue
        sanitized, removed = sanitize_untrusted_content(document.request.content)
        content_terms = set(re.findall(r"\w+", sanitized.lower()))
        overlap = len(query_terms.intersection(content_terms))
        score = min(0.99, 0.55 + overlap * 0.08)
        authorized_results.append(
            {
                "sourceId": document.request.documentId,
                "title": document.request.title,
                "uri": document.request.provenance.sourceUri,
                "chunkId": f"{document.request.documentId}-chunk-001",
                "score": round(score, 2),
                "dataClassification": document.request.classification,
                "text": sanitized,
                "provenance": {
                    "sourceSystem": document.request.provenance.sourceSystem,
                    "checksum": document.checksum,
                    "approvedSource": document.request.provenance.approvedSource,
                },
                "security": {
                    "policyDecisionId": policy_decision_id,
                    "authorizationApplied": True,
                    "promptInjectionIndicatorsRemoved": removed,
                    "contentTreatedAsUntrusted": True,
                },
            }
        )

    authorized_results.sort(key=lambda item: item["score"], reverse=True)
    if denied_count:
        POLICY_DENIALS.labels("knowledge", "acl_or_clearance").inc(denied_count)
    return {
        "policyDecisionId": policy_decision_id,
        "results": authorized_results[: body.topK],
        "filteredResultCount": denied_count,
    }


def validate_memory_item(item: MemoryItemInput, memory_type: str) -> None:
    indicators = detect_patterns(item.value, PROMPT_INJECTION_PATTERNS)
    if indicators:
        POLICY_DENIALS.labels("memory", "poisoning_detected").inc()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Memory poisoning indicators detected: {', '.join(indicators)}",
        )
    if item.classification == "RESTRICTED":
        POLICY_DENIALS.labels("memory", "restricted_persistence").inc()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="RESTRICTED data is non-persistent by default",
        )
    if memory_type in {"LONG_TERM", "PROFILE"} and item.source not in {
        "USER_CONFIRMED",
        "SYSTEM_VERIFIED",
    }:
        POLICY_DENIALS.labels("memory", "untrusted_source").inc()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Long-term memory requires USER_CONFIRMED or SYSTEM_VERIFIED source",
        )
    if item.source == "MODEL_INFERRED" and memory_type != "SESSION":
        POLICY_DENIALS.labels("memory", "model_inference_persistence").inc()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="MODEL_INFERRED items may only be stored in SESSION memory",
        )


@router.get("/v1/sessions/{session_id}/memory")
async def get_secure_memory(
    session_id: str,
    tenant: str = Depends(tenant_id),
    subject: str = Depends(subject_header),
    _: None = Depends(require_scope("memory.read")),
) -> dict[str, Any]:
    key = (tenant, session_id, subject_hash(subject))
    record = memory_records.get(key)
    if record is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    if datetime.fromisoformat(record.expires_at) <= datetime.now(UTC):
        memory_records.pop(key, None)
        raise HTTPException(status_code=404, detail="Memory not found")
    return record.as_dict()


@router.patch("/v1/sessions/{session_id}/memory")
async def update_secure_memory(
    session_id: str,
    body: MemoryWriteRequest,
    request: Request,
    tenant: str = Depends(tenant_id),
    subject: str = Depends(subject_header),
    actor: str = Depends(actor_id),
    _: str = Depends(require_idempotency),
    __: None = Depends(require_scope("memory.write")),
) -> dict[str, Any]:
    for item in body.items:
        validate_memory_item(item, body.memoryType)

    now = datetime.now(UTC)
    hashed_subject = subject_hash(subject)
    key = (tenant, session_id, hashed_subject)
    previous = memory_records.get(key)
    record = MemoryRecord(
        tenant_id=tenant,
        session_id=session_id,
        subject_hash=hashed_subject,
        memory_type=body.memoryType,
        purpose=body.purpose,
        consent_reference=body.consentReference,
        items=[
            {
                **item.model_dump(),
                "recordedBy": actor,
                "recordedAt": now.isoformat(),
            }
            for item in body.items
        ],
        created_at=previous.created_at if previous else now.isoformat(),
        updated_at=now.isoformat(),
        expires_at=(now + timedelta(seconds=body.ttlSeconds)).isoformat(),
        version=(previous.version + 1) if previous else 1,
    )
    memory_records[key] = record
    max_classification = max(
        (item.classification for item in body.items),
        key=lambda value: CLASSIFICATION_RANK[value],
    )
    await event_publisher.publish(
        "memory.updated",
        request.state.correlation_id,
        tenant,
        "memory-service",
        {
            "sessionId": session_id,
            "subjectHash": hashed_subject,
            "memoryType": body.memoryType,
            "itemCount": len(body.items),
            "version": record.version,
            "expiresAt": record.expires_at,
            "consentReferencePresent": bool(body.consentReference),
        },
        data_classification=max_classification,
    )
    return record.as_dict()


@router.delete("/v1/sessions/{session_id}/memory", status_code=204)
async def delete_secure_memory(
    session_id: str,
    request: Request,
    tenant: str = Depends(tenant_id),
    subject: str = Depends(subject_header),
    _: str = Depends(require_idempotency),
    __: None = Depends(require_scope("memory.delete")),
) -> Response:
    hashed_subject = subject_hash(subject)
    memory_records.pop((tenant, session_id, hashed_subject), None)
    await event_publisher.publish(
        "memory.deleted",
        request.state.correlation_id,
        tenant,
        "memory-service",
        {
            "sessionId": session_id,
            "subjectHash": hashed_subject,
            "deletionMode": "DELETE",
        },
    )
    return Response(status_code=204)
