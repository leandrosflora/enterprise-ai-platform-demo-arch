# Documentação

Esta pasta contém a arquitetura de referência, contratos executáveis, controles de governança e guias operacionais da Enterprise AI Platform.

## Comece por aqui

1. [Visão geral](index.md)
2. [Princípios arquiteturais](architecture/principles/principles.md)
3. [Control plane e data plane](architecture/control-plane-data-plane.md)
4. [Requisitos não funcionais](architecture/non-functional-requirements.md)
5. [Contratos HTTP](contracts/openapi.yaml)
6. [Contratos de eventos](contracts/async-api.yaml)
7. [AI Risk Framework](governance/ai-risk-framework.md)
8. [Tracing e SLOs](observability/tracing.md)

## Estrutura

```text
architecture/             Princípios, NFRs, C4 e decisões de separação de planos
adr/                      Architecture Decision Records
contracts/                OpenAPI, AsyncAPI, MCP, eventos e data stores
domains/                  Domínios funcionais da plataforma
services/                 Responsabilidades e contratos por serviço
governance/               Workflow, risco, catálogo e ciclo de modelos
security/                 Autenticação, autorização, LGPD e threat model
observability/            Tracing, métricas, dashboards, alertas e SLOs
finops/                   Custos, budgets, chargeback e showback
runbooks/                 Procedimentos operacionais e troubleshooting
examples/                 Exemplos ponta a ponta
reference-architectures/  Blueprints por caso de uso
roadmap/                   Sequenciamento de implantação
```

## Fontes canônicas

| Assunto | Fonte |
|---|---|
| APIs HTTP | [`contracts/openapi.yaml`](contracts/openapi.yaml) |
| Eventos | [`contracts/async-api.yaml`](contracts/async-api.yaml) |
| Convenções de eventos | [`contracts/events.md`](contracts/events.md) |
| SLOs | [`architecture/non-functional-requirements.md`](architecture/non-functional-requirements.md) |
| Controles de risco | [`governance/ai-risk-framework.md`](governance/ai-risk-framework.md) |
| Autorização | [`security/authorization.md`](security/authorization.md) |

Exemplos e documentos derivados não podem redefinir enums, envelopes ou metas diferentes das fontes canônicas.

## Arquitetura

- [C4 Context](architecture/diagrams/c4-context.puml)
- [C4 Container](architecture/diagrams/c4-container.puml)
- [C4 Deployment](architecture/diagrams/c4-deployment.puml)
- [Control plane e data plane](architecture/control-plane-data-plane.md)
- [Event Storming](architecture/diagrams/event-storming.md)

## Serviços principais

- [Agent Gateway](services/agent-gateway.md)
- [Agent Runtime](services/agent-runtime.md)
- [Agent Registry](services/agent-registry.md)
- [Model Gateway](services/model-gateway.md)
- [Knowledge Service](services/knowledge-service.md)
- [Memory Service](services/memory-service.md)
- [MCP Registry](services/mcp-registry.md)
- [Governance Service](services/governance-service.md)
- [Evaluation Service](services/evaluation-service.md)
- [Audit Service](services/audit-service.md)
- [Billing Service](services/billing-service.md)

## Operação

- [Onboarding de agente](runbooks/onboarding-agent.md)
- [Onboarding MCP](runbooks/onboarding-mcp.md)
- [Troubleshooting de invocação](runbooks/troubleshooting-agent-invocation.md)

## Validação

Na raiz do repositório:

```bash
python scripts/validate_contracts.py
python scripts/validate_docs.py
./scripts/render_diagrams.sh
mkdocs build --strict
```
