from fastapi.testclient import TestClient

from app.main import agents, app, event_publisher


ALL_SCOPES = "agent.read agent.write governance.submit governance.approve agent.publish agent.invoke audit.read"


def headers(actor: str = "developer") -> dict[str, str]:
    return {
        "X-Demo-Scopes": ALL_SCOPES,
        "X-Demo-Actor": actor,
        "X-Demo-Tenant": "enterprise",
        "Idempotency-Key": f"test-{actor}-0000000000000000",
    }


def setup_function() -> None:
    agents.clear()
    event_publisher.events.clear()


def test_end_to_end_agent_lifecycle() -> None:
    with TestClient(app) as client:
        created = client.post(
            "/v1/agents",
            headers=headers(),
            json={
                "agentId": "policy-assistant",
                "name": "Policy Assistant",
                "version": "1.0.0",
                "owner": "governance-team",
                "businessUnit": "corporate-governance",
                "instructions": "Answer only from approved policies.",
                "riskClassification": "MEDIUM",
                "modelPolicy": {"capability": "TEXT_GENERATION"},
                "allowedTools": ["policy-document-search:1.0.0"],
                "knowledgeBaseIds": ["corporate-policies-kb"],
            },
        )
        assert created.status_code == 201
        assert created.json()["status"] == "DRAFT"

        submitted = client.post(
            "/v1/agents/policy-assistant:submit",
            headers=headers("developer"),
            json={
                "agentVersion": "1.0.0",
                "riskClassification": "MEDIUM",
                "evidence": ["evaluation.json"],
            },
        )
        assert submitted.status_code == 202
        approval_id = submitted.json()["approvalId"]

        denied = client.post(
            "/v1/agents/policy-assistant:approve",
            headers=headers("developer"),
            json={"reason": "Same person must not approve."},
        )
        assert denied.status_code == 422

        approved = client.post(
            "/v1/agents/policy-assistant:approve",
            headers=headers("ai-architect"),
            json={"reason": "Architecture and evidence were reviewed."},
        )
        assert approved.status_code == 200
        assert approved.json()["decision"] == "APPROVED"

        published = client.post(
            "/v1/agents/policy-assistant:publish",
            headers=headers("release-pipeline"),
            json={"approvalId": approval_id},
        )
        assert published.status_code == 202
        assert published.json()["status"] == "PUBLISHED"

        invoked = client.post(
            "/v1/agents/policy-assistant:invoke",
            headers=headers("business-user"),
            json={
                "input": "Qual é a regra de retenção?",
                "channel": "test",
                "sessionId": "session-1",
            },
        )
        assert invoked.status_code == 200
        payload = invoked.json()
        assert payload["executionStatus"] == "SUCCESS"
        assert payload["citations"]
        assert payload["toolCalls"][0]["status"] == "SUCCESS"
        assert {event["eventType"] for event in event_publisher.events} >= {
            "agent.created",
            "governance.approved",
            "agent.published",
            "agent.invoked",
            "tool.executed",
            "model.invoked",
        }


def test_missing_scope_is_denied() -> None:
    with TestClient(app) as client:
        response = client.get("/v1/agents")
        assert response.status_code == 403
