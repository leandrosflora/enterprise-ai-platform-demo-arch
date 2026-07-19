#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
OPENAPI_PATH = ROOT / "docs/contracts/openapi.yaml"
ASYNCAPI_PATH = ROOT / "docs/contracts/async-api.yaml"
EVENTS_PATH = ROOT / "docs/contracts/events.md"
RAG_MEMORY_POLICY_PATH = ROOT / "policies/rag-memory-security.yaml"
RAG_MEMORY_DOC_PATH = ROOT / "docs/security/rag-memory-security.md"

RISK_ENUM = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
EXECUTION_ENUM = ["SUCCESS", "FAILED", "BLOCKED", "PARTIAL"]
DATA_ENUM = ["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"]
ENVELOPE_FIELDS = {
    "eventId",
    "eventType",
    "schemaVersion",
    "occurredAt",
    "correlationId",
    "tenantId",
    "source",
    "dataClassification",
    "payload",
}
RAG_INGESTION_CONTROLS = {
    "malware_scan",
    "content_type_validation",
    "checksum_validation",
    "source_approval",
    "provenance_capture",
    "prompt_injection_scan",
    "quarantine",
}
RAG_RETRIEVAL_CONTROLS = {
    "tenant_filter",
    "document_acl",
    "chunk_acl",
    "classification_clearance",
    "purpose_binding",
    "post_filter",
    "provenance_return",
    "context_delimiters",
}
MEMORY_CONTROLS = {
    "consent",
    "purpose_binding",
    "ttl",
    "provenance",
    "trust_level",
    "poisoning_detection",
    "subject_isolation",
    "tenant_isolation",
    "deny_sensitive_by_default",
    "deletion",
}


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    if not isinstance(data, dict):
        raise AssertionError(f"{path} must contain an object")
    return data


def expect(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    openapi = load_yaml(OPENAPI_PATH)
    asyncapi = load_yaml(ASYNCAPI_PATH)
    rag_memory_policy = load_yaml(RAG_MEMORY_POLICY_PATH)
    events_text = EVENTS_PATH.read_text(encoding="utf-8")
    rag_memory_text = RAG_MEMORY_DOC_PATH.read_text(encoding="utf-8")

    expect(str(openapi.get("openapi", "")).startswith("3.1"), "OpenAPI must use 3.1.x", errors)
    schemes = openapi.get("components", {}).get("securitySchemes", {})
    oidc = schemes.get("oidc", {})
    expect(oidc.get("type") == "openIdConnect", "OpenAPI must model OIDC with openIdConnect", errors)

    parameters = openapi.get("components", {}).get("parameters", {})
    expect("IdempotencyKey" in parameters, "OpenAPI must define Idempotency-Key", errors)

    openapi_schemas = openapi.get("components", {}).get("schemas", {})
    expect(
        openapi_schemas.get("RiskClassification", {}).get("enum") == RISK_ENUM,
        "OpenAPI risk enum differs from canonical enum",
        errors,
    )
    expect(
        openapi_schemas.get("DataClassification", {}).get("enum") == DATA_ENUM,
        "OpenAPI data classification enum differs from canonical enum",
        errors,
    )
    tool_status = (
        openapi_schemas.get("ToolCall", {})
        .get("properties", {})
        .get("status", {})
        .get("enum")
    )
    expect(tool_status == EXECUTION_ENUM, "OpenAPI tool status differs from canonical enum", errors)

    ingestion_statuses = (
        openapi_schemas.get("IngestDocumentResponse", {})
        .get("properties", {})
        .get("status", {})
        .get("enum", [])
    )
    expect("QUARANTINED" in ingestion_statuses, "Document ingestion must model QUARANTINED", errors)
    memory_properties = openapi_schemas.get("UpdateMemoryRequest", {}).get("properties", {})
    expect("ttlSeconds" in memory_properties, "Memory contract must require TTL", errors)
    expect("consentReference" in memory_properties, "Memory contract must model consentReference", errors)
    openapi_paths = openapi.get("paths", {})
    memory_path = openapi_paths.get("/v1/sessions/{sessionId}/memory", {})
    expect("delete" in memory_path, "Memory contract must expose deletion", errors)
    search_path = openapi_paths.get("/v1/knowledge-bases/{knowledgeBaseId}:search", {})
    expect("post" in search_path, "Knowledge contract must expose secure retrieval", errors)

    async_schemas = asyncapi.get("components", {}).get("schemas", {})
    envelope = async_schemas.get("EventEnvelope", {})
    required = set(envelope.get("required", []))
    properties = set(envelope.get("properties", {}).keys())
    expect(ENVELOPE_FIELDS <= required, "AsyncAPI envelope is missing required canonical fields", errors)
    expect(ENVELOPE_FIELDS <= properties, "AsyncAPI envelope is missing canonical properties", errors)
    expect("eventVersion" not in properties, "Use schemaVersion; eventVersion is forbidden", errors)
    expect(
        async_schemas.get("RiskClassification", {}).get("enum") == RISK_ENUM,
        "AsyncAPI risk enum differs from canonical enum",
        errors,
    )
    expect(
        async_schemas.get("ExecutionStatus", {}).get("enum") == EXECUTION_ENUM,
        "AsyncAPI execution enum differs from canonical enum",
        errors,
    )
    expect(
        async_schemas.get("DataClassification", {}).get("enum") == DATA_ENUM,
        "AsyncAPI data classification enum differs from canonical enum",
        errors,
    )

    channels = asyncapi.get("components", {}).get("channels", {})
    for name, channel in channels.items():
        address = channel.get("address", "")
        expect(address.endswith(".v1"), f"Channel {name} must have a versioned .v1 address", errors)

    expect('"eventVersion"' not in events_text, "events.md must not use eventVersion in JSON examples", errors)
    for field in ENVELOPE_FIELDS:
        expect(f'"{field}"' in events_text or f"`{field}`" in events_text, f"events.md missing {field}", errors)
    for value in RISK_ENUM + EXECUTION_ENUM + DATA_ENUM:
        expect(value in events_text, f"events.md missing canonical enum value {value}", errors)

    expect(rag_memory_policy.get("default_decision") == "DENY", "RAG/memory policy must deny by default", errors)
    rag_policy = rag_memory_policy.get("rag", {})
    ingestion_controls = set(rag_policy.get("ingestion", {}).get("required_controls", []))
    retrieval_controls = set(rag_policy.get("retrieval", {}).get("required_controls", []))
    memory_policy = rag_memory_policy.get("memory", {})
    memory_controls = set(memory_policy.get("required_controls", []))
    expect(RAG_INGESTION_CONTROLS <= ingestion_controls, "RAG ingestion policy is missing controls", errors)
    expect(RAG_RETRIEVAL_CONTROLS <= retrieval_controls, "RAG retrieval policy is missing controls", errors)
    expect(MEMORY_CONTROLS <= memory_controls, "Memory policy is missing controls", errors)
    expect(
        "RESTRICTED" in memory_policy.get("blocked_classifications", []),
        "RESTRICTED memory must be blocked by default",
        errors,
    )
    for memory_type in ("SESSION", "SHORT_TERM", "LONG_TERM", "PROFILE"):
        expect(
            memory_type in memory_policy.get("types", {}),
            f"Memory policy missing type {memory_type}",
            errors,
        )
    expect(
        memory_policy.get("types", {}).get("PROFILE", {}).get("consent_required") is True,
        "PROFILE memory must require consent",
        errors,
    )
    expect(
        memory_policy.get("types", {}).get("LONG_TERM", {}).get("model_inferred_allowed") is False,
        "LONG_TERM memory must reject model-inferred facts",
        errors,
    )
    for required_term in (
        "indirect prompt injection",
        "ACL",
        "consentimento",
        "memory poisoning",
        "subjectHash",
        "untrusted_document",
    ):
        expect(required_term.lower() in rag_memory_text.lower(), f"RAG/memory security doc missing {required_term}", errors)

    if errors:
        print("Contract validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
