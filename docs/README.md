# Documentação

Esta pasta concentra a documentação arquitetural da Enterprise AI Platform.

## Estrutura

```text
architecture/          Diagramas, princípios e requisitos não funcionais
adr/                   Architecture Decision Records (única fonte de decisões arquiteturais)
domains/               Domínios funcionais da plataforma
services/              Documentação dos serviços da plataforma
integrations/          Integrações externas e corporativas
contracts/             Eventos, APIs (REST e async) e data stores
governance/            Governança de IA, riscos e ciclo de aprovação
observability/         Tracing, métricas, dashboards e alertas
security/              Autenticação, autorização, LGPD, segredos e threat model
finops/                Custos, chargeback, showback e token analytics
runbooks/              Guias operacionais
roadmap/               Evolução planejada da plataforma
examples/              Exemplos ponta a ponta de eventos, prompts, traces e avaliações
reference-architectures/  Blueprints de soluções de referência por caso de uso
```

## Princípios e Requisitos Não Funcionais

- [Princípios Arquiteturais](architecture/principles/principles.md)
- [Requisitos Não Funcionais](architecture/non-functional-requirements.md)

## Diagramas iniciais

- [C4 Context](architecture/diagrams/c4-context.puml)
- [C4 Container](architecture/diagrams/c4-container.puml)

## Serviços

- [Agent Gateway](services/agent-gateway.md)
- [Agent Runtime](services/agent-runtime.md)
- [Agent Registry](services/agent-registry.md)
- [Knowledge Service](services/knowledge-service.md)
- [Memory Service](services/memory-service.md)
- [MCP Registry](services/mcp-registry.md)
- [Governance Service](services/governance-service.md)
- [Evaluation Service](services/evaluation-service.md)
- [Audit Service](services/audit-service.md)
- [Billing Service](services/billing-service.md)

## Contratos Implementáveis

- [OpenAPI](contracts/openapi.yaml)
- [AsyncAPI](contracts/async-api.yaml)
- [MCP Contracts](contracts/mcp-contracts.md)

## Segurança e Governança

- [Autenticação](security/authentication.md)
- [Autorização](security/authorization.md)
- [Threat Model](security/threat-model.md)
- [LGPD](security/lgpd.md)
- [AI Risk Framework](governance/ai-risk-framework.md)

## Exemplos

- [End-to-End: Agent + RAG + MCP](examples/end-to-end-agent-rag-mcp.md)
- [Prompt](examples/prompt-example.md)
- [Tool Call](examples/tool-call-example.md)
- [Kafka Event](examples/kafka-event-example.md)
- [Trace](examples/trace-example.md)
- [Evaluation](examples/evaluation-example.md)

## Arquiteturas de Referência

- [Customer Service Agent](reference-architectures/customer-service-agent.md)
- [Internal Copilot](reference-architectures/internal-copilot.md)
- [Document Analysis Agent](reference-architectures/document-analysis-agent.md)
- [Backoffice Automation Agent](reference-architectures/backoffice-automation-agent.md)
- [Conversational Analytics](reference-architectures/conversational-analytics.md)
