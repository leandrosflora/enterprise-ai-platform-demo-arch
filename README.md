# Enterprise AI Platform - Arquitetura de Referência

> Arquitetura de referência para uma Plataforma Corporativa de IA cobrindo Agentic AI, MCP, RAG, Memória, Governança, Avaliação, Observabilidade, Segurança e FinOps.

---

## Visão Geral

Este repositório demonstra como projetar, governar e operar uma Plataforma Corporativa de IA em escala empresarial.

Capacidades abordadas:

- Plataforma de Agentes
- Plataforma de Conhecimento
- Plataforma de Memória
- Plataforma MCP
- Plataforma de Governança
- Plataforma de Avaliação
- Plataforma de Observabilidade
- Plataforma de FinOps

---

# Mapa da Documentação

## Arquitetura

### Modelo C4

- docs/architecture/diagrams/c4-context.puml
- docs/architecture/diagrams/c4-container.puml
- docs/architecture/diagrams/c4-component-agent-runtime.puml
- docs/architecture/diagrams/c4-component-knowledge-service.puml
- docs/architecture/diagrams/c4-component-governance-service.puml
- docs/architecture/diagrams/c4-deployment.puml

### Diagramas de Sequência

- docs/architecture/diagrams/sequences/agent-invocation.puml
- docs/architecture/diagrams/sequences/rag-query.puml
- docs/architecture/diagrams/sequences/mcp-tool-execution.puml
- docs/architecture/diagrams/sequences/agent-publishing.puml

### Event Storming

- docs/architecture/diagrams/event-storming.md

---

## Domínios

- docs/domains/agent-platform.md
- docs/domains/knowledge-platform.md
- docs/domains/memory-platform.md
- docs/domains/mcp-platform.md
- docs/domains/governance-platform.md
- docs/domains/evaluation-platform.md
- docs/domains/observability-platform.md
- docs/domains/finops-platform.md

---

## Serviços

- docs/services/agent-runtime.md
- docs/services/agent-registry.md
- docs/services/knowledge-service.md
- docs/services/memory-service.md
- docs/services/mcp-registry.md
- docs/services/governance-service.md

---

## Contratos

- docs/contracts/apis.md
- docs/contracts/events.md
- docs/contracts/async-api.yaml
- docs/contracts/data-stores.md
- docs/contracts/mcp-contracts.md

---

## Governança

- docs/governance/approval-workflow.md
- docs/governance/ai-catalog.md
- docs/governance/ai-risk-framework.md
- docs/governance/model-lifecycle.md

---

## Segurança

- docs/security/authentication.md
- docs/security/authorization.md
- docs/security/lgpd.md

---

## Observabilidade

- docs/observability/tracing.md
- docs/observability/dashboards.md

---

## FinOps

- docs/finops/token-costs.md

---

## Integrações

- docs/integrations/foundation-models.md
- docs/integrations/identity-provider.md
- docs/integrations/corporate-systems.md
- docs/integrations/observability-stack.md
- docs/integrations/external-tools.md

---

## ADRs

- ADR-001 Estratégia de Agent Runtime
- ADR-002 Seleção de Banco Vetorial
- ADR-003 Estratégia MCP
- ADR-004 Estratégia de Observabilidade
- ADR-005 Framework de Avaliação

---

# Stack Tecnológico de Referência

## Plataforma

- AWS
- Kubernetes (EKS)
- Amazon MSK
- Amazon Bedrock
- OpenTelemetry

## Dados

- PostgreSQL
- MongoDB
- OpenSearch
- Redis

## Desenvolvimento

- .NET
- React
- Kafka
- MCP

---

# Roadmap de Implementação

## Fase 1

Fundação da Plataforma

## Fase 2

Plataforma de Conhecimento e RAG Corporativo

## Fase 3

MCP e Integrações Corporativas

## Fase 4

Governança e Avaliação

## Fase 5

Escala, Marketplace e FinOps

Detalhes completos:

- docs/roadmap/implementation-roadmap.md

---

# Público-Alvo

- Arquitetos Corporativos
- Arquitetos de Soluções
- Arquitetos de IA
- Engenheiros de Plataforma
- Líderes Técnicos
- Times de Governança
- Times de Segurança

---

# Licença

MIT