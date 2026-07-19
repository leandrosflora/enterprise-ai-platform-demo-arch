# Documentação

Esta pasta contém o **Enterprise AI Platform Book**, a arquitetura de referência, contratos executáveis, policies, controles de governança e guias operacionais.

## Comece pelo book

1. [Entrada do livro](book/index.md)
2. [Por que uma AI Platform?](book/01-why-ai-platform.md)
3. [Capability Map](book/02-capability-map.md)
4. [Operating Model](book/03-operating-model.md)
5. [Ciclo de vida de agentes](book/04-agent-lifecycle.md)
6. [Estudo de caso de agente documental](book/05-case-study-document-agent.md)
7. [Decision Guides](book/06-decision-guides.md)
8. [Roadmap de adoção](book/07-adoption-roadmap.md)
9. [Checklists de produção](book/08-production-checklists.md)
10. [Glossário](book/glossary.md)

## Estrutura

```text
book/                     Narrativa, operating model, casos, decisões e checklists
architecture/             Princípios, NFRs, C4 e separação de planos
adr/                      Architecture Decision Records
contracts/                OpenAPI, AsyncAPI, MCP, eventos e data stores
domains/                  Domínios funcionais da plataforma
services/                 Responsabilidades e contratos por serviço
governance/               Workflow, risco, catálogo e ciclo de modelos
security/                 Autenticação, autorização, LGPD, RAG/memória e threat model
observability/            Tracing, métricas, dashboards, alertas e SLOs
finops/                   Custos, budgets, chargeback e showback
runbooks/                 Procedimentos operacionais e troubleshooting
examples/                 Exemplos ponta a ponta
reference-architectures/  Blueprints por caso de uso
roadmap/                  Sequenciamento técnico de implantação
```

## Relação entre book e referência

- O **book** explica problema, decisão, trade-offs, operating model e critérios de sucesso.
- A **referência técnica** define contratos, policies, componentes, eventos e procedimentos.
- A **vertical slice** demonstra partes dos controles de forma executável.

O conteúdo editorial não pode redefinir enums, envelopes, policies ou metas diferentes das fontes canônicas.

## Fontes canônicas

| Assunto | Fonte |
|---|---|
| APIs HTTP | [`contracts/openapi.yaml`](contracts/openapi.yaml) |
| Eventos | [`contracts/async-api.yaml`](contracts/async-api.yaml) |
| Convenções de eventos | [`contracts/events.md`](contracts/events.md) |
| SLOs | [`architecture/non-functional-requirements.md`](architecture/non-functional-requirements.md) |
| Controles de risco | [`governance/ai-risk-framework.md`](governance/ai-risk-framework.md) |
| Autorização | [`security/authorization.md`](security/authorization.md) |
| Segurança de RAG e memória | [`security/rag-memory-security.md`](security/rag-memory-security.md) + [`../policies/rag-memory-security.yaml`](../policies/rag-memory-security.yaml) |

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

## Gerar o book

Na raiz do repositório:

```bash
python scripts/build_book.py --check
python scripts/build_book.py
```

O PDF é gerado automaticamente pelo workflow `.github/workflows/book.yml` usando Pandoc e WeasyPrint.

## Validação

```bash
python scripts/validate_contracts.py
python scripts/validate_docs.py
python scripts/build_book.py --check
bash scripts/render_diagrams.sh
mkdocs build
```
