# Documentação

Esta pasta concentra a documentação arquitetural da Enterprise AI Platform.

## Estrutura

```text
architecture/     Diagramas e princípios arquiteturais
adr/              Architecture Decision Records (única fonte de decisões arquiteturais)
domains/          Domínios funcionais da plataforma
services/         Documentação dos serviços da plataforma
integrations/     Integrações externas e corporativas
contracts/        Eventos, APIs e data stores
governance/       Governança de IA, riscos e ciclo de aprovação
observability/    Tracing, métricas, dashboards e alertas
security/         Autenticação, autorização, LGPD e segredos
finops/           Custos, chargeback, showback e token analytics
runbooks/         Guias operacionais
roadmap/          Evolução planejada da plataforma
```

## Princípios

- [Princípios Arquiteturais](architecture/principles/principles.md)

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

## Próximos artefatos recomendados

1. `contracts/events.md`
2. `services/agent-runtime.md`
3. `services/knowledge-service.md`
4. `services/governance-service.md`
5. `adr/ADR-001-agent-runtime-strategy.md`
6. `adr/ADR-002-vector-database-selection.md`
