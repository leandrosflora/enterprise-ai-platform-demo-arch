# Architecture Decision Records

Os ADRs registram decisões estruturais da plataforma, seu contexto, alternativas, consequências, evidências e critérios de revisão. A pasta `docs/adrs/` é a única fonte canônica para decisões arquiteturais.

## Catálogo

| ADR | Decisão | Status |
|---|---|---|
| [ADR-001](001-mcp-vs-rest.md) | MCP para tool calling governado; REST para APIs de domínio | Aceito |
| [ADR-002](002-persistent-memory.md) | Memória persistente somente sob critérios explícitos | Aceito |
| [ADR-003](003-agent-gateway.md) | Agent Gateway como ponto de entrada e enforcement | Aceito |
| [ADR-004](004-agent-runtime-strategy.md) | Agent Runtime com núcleo estável e adaptadores | Aceito |
| [ADR-005](005-vector-search-strategy.md) | OpenSearch como referência inicial para busca vetorial e híbrida | Aceito |
| [ADR-006](006-observability-strategy.md) | OpenTelemetry como padrão de observabilidade | Aceito |
| [ADR-007](007-evaluation-strategy.md) | Avaliação híbrida, regressiva e contínua | Aceito |

## Status permitidos

| Status | Uso |
|---|---|
| Proposto | decisão em discussão, ainda não vinculante |
| Aceito | decisão vigente |
| Depreciado | ainda existente, mas não recomendada para novas implementações |
| Substituído | decisão histórica substituída por outro ADR identificado |
| Rejeitado | alternativa analisada e não adotada |

## Regras

- um número identifica uma única decisão;
- o número do arquivo deve coincidir com o título do ADR;
- decisões aceitas não são reescritas para ocultar mudanças materiais;
- mudanças de direção criam novo ADR e marcam o anterior como substituído;
- cada ADR deve registrar consequências, evidências e critérios de revisão;
- links internos devem apontar apenas para `docs/adrs/`.

## Migração do catálogo legado

| Decisão legada | Destino canônico |
|---|---|
| Estratégia de Agent Runtime | ADR-004 |
| Seleção de banco vetorial | ADR-005 |
| Estratégia de integração via MCP | conteúdo consolidado no ADR-001 |
| Estratégia de observabilidade | ADR-006 |
| Estratégia de avaliação de IA | ADR-007 |

A validação documental bloqueia pastas concorrentes, IDs duplicados, divergência entre nome e título e ADRs ausentes deste índice.
