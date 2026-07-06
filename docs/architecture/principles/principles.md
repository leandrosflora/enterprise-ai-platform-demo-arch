# Princípios Arquiteturais

Estes princípios já estão implícitos nos contratos, domínios e serviços documentados neste repositório. Eles são explicitados aqui como referência única para quem propõe novos domínios, serviços ou integrações.

## 1. Ownership de dados por serviço

Cada serviço é dono do seu armazenamento; não há acesso direto a bancos de outros serviços. Integração entre serviços acontece por API síncrona ou evento assíncrono, nunca por acesso compartilhado a dados.

Ver: [docs/contracts/data-stores.md](../../contracts/data-stores.md).

## 2. Integração orientada a eventos

Mudanças de estado relevantes (criação, publicação, execução, aprovação) são publicadas como eventos versionados em Kafka, com envelope padrão (`eventId`, `correlationId`, `causationId`, `schemaVersion`). Consumidores reagem a eventos em vez de consultar o produtor de forma síncrona sempre que possível.

Ver: [docs/contracts/events.md](../../contracts/events.md).

## 3. Segurança e governança por padrão

Toda capacidade de agente, ferramenta ou dado é protegida por autenticação (OIDC/OAuth2), autorização por escopo, e passa pelo ciclo de aprovação da Governance Service antes de ir para produção. Não há capacidade "não governada" na plataforma.

Ver: [docs/governance/approval-workflow.md](../../governance/approval-workflow.md), [docs/security/authentication.md](../../security/authentication.md).

## 4. Auditoria e observabilidade ponta a ponta

Toda execução relevante (invocação de agente, chamada de ferramenta, decisão de governança) gera trilha auditável e é rastreável via trace distribuído. Auditoria e observabilidade não são adicionadas depois — fazem parte do contrato de eventos desde o início.

Ver: [docs/observability/tracing.md](../../observability/tracing.md), [docs/security/authorization.md](../../security/authorization.md).

## 5. Consciência de custo (FinOps) desde o design

Uso de modelos, ferramentas e armazenamento é medido e atribuído por agente, time ou unidade de negócio, permitindo chargeback/showback. Custos não são uma preocupação apenas operacional — são um requisito nas fases de design de domínios e serviços.

Ver: [docs/finops/token-costs.md](../../finops/token-costs.md).

## 6. Resiliência contra falhas de dependências externas

Chamadas a modelos, ferramentas MCP e serviços corporativos aplicam timeout, retry controlado e circuit breaker. Nenhum serviço assume disponibilidade total de suas dependências externas.

Ver: [docs/services/agent-runtime.md](../../services/agent-runtime.md).
