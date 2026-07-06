# APIs da Plataforma

## Agent Gateway

POST /agents/{agentId}/invoke
GET /agents/{agentId}

## Agent Registry

POST /agents
GET /agents
GET /agents/{agentId}
POST /agents/{agentId}/publish

## Knowledge Service

POST /knowledge-bases/{id}/documents
POST /knowledge-bases/{id}/search

## Memory Service

GET /sessions/{sessionId}/memory
POST /sessions/{sessionId}/memory

## Governance Service

POST /governance/agents/{id}/submit
POST /governance/agents/{id}/approve
POST /governance/agents/{id}/reject

## Evaluation Service

POST /evaluations
GET /evaluations/{id}
