#!/usr/bin/env bash
set -euo pipefail

API="${API:-http://localhost:8080}"
COMMON=(
  -H 'Content-Type: application/json'
  -H 'X-Demo-Tenant: enterprise'
  -H 'X-Correlation-Id: 7d8cf2aa-ef5f-4cc3-bafa-61ea26277511'
)

printf '\n1. Register agent\n'
curl -fsS -X POST "$API/v1/agents" \
  "${COMMON[@]}" \
  -H 'X-Demo-Actor: developer' \
  -H 'X-Demo-Scopes: agent.write' \
  -H 'Idempotency-Key: policy-assistant-1.0.0-create' \
  -d @agent-card.json | tee /tmp/agent-created.json

printf '\n\n2. Submit governance\n'
APPROVAL_ID=$(curl -fsS -X POST "$API/v1/agents/policy-assistant:submit" \
  "${COMMON[@]}" \
  -H 'X-Demo-Actor: developer' \
  -H 'X-Demo-Scopes: governance.submit' \
  -H 'Idempotency-Key: policy-assistant-1.0.0-submit' \
  -d '{"agentVersion":"1.0.0","riskClassification":"MEDIUM","evidence":["evaluation-report.json"]}' \
  | python -c 'import json,sys; print(json.load(sys.stdin)["approvalId"])')
echo "approvalId=$APPROVAL_ID"

printf '\n3. Approve\n'
curl -fsS -X POST "$API/v1/agents/policy-assistant:approve" \
  "${COMMON[@]}" \
  -H 'X-Demo-Actor: ai-architect' \
  -H 'X-Demo-Scopes: governance.approve' \
  -H 'Idempotency-Key: policy-assistant-1.0.0-approve' \
  -d '{"reason":"Architecture, security and evaluation evidence approved."}' | tee /tmp/agent-approved.json

printf '\n\n4. Publish\n'
curl -fsS -X POST "$API/v1/agents/policy-assistant:publish" \
  "${COMMON[@]}" \
  -H 'X-Demo-Actor: release-pipeline' \
  -H 'X-Demo-Scopes: agent.publish' \
  -H 'Idempotency-Key: policy-assistant-1.0.0-publish' \
  -d "{\"approvalId\":\"$APPROVAL_ID\",\"releaseNotes\":\"Demo release\"}" | tee /tmp/agent-published.json

printf '\n\n5. Invoke\n'
curl -fsS -X POST "$API/v1/agents/policy-assistant:invoke" \
  "${COMMON[@]}" \
  -H 'X-Demo-Actor: business-user' \
  -H 'X-Demo-Scopes: agent.invoke' \
  -d '{"input":"Qual é a regra de retenção de dados pessoais?","channel":"cli","sessionId":"session-demo"}' \
  | python -m json.tool

printf '\n6. Inspect events\n'
curl -fsS "$API/v1/events" -H 'X-Demo-Scopes: audit.read' | python -m json.tool
