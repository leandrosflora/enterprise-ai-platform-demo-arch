# Runbook — Troubleshooting de Invocação de Agente

## Entrada mínima

Colete sem expor dados sensíveis:

- horário UTC;
- `correlationId`;
- agente e versão;
- tenant;
- classe de workload;
- status HTTP ou `executionStatus`;
- policy ID/version quando houver bloqueio.

## Sequência de diagnóstico

1. localizar o trace pelo `correlationId`;
2. verificar autenticação e autorização no Gateway;
3. confirmar versão `PUBLISHED` no cache do Runtime;
4. revisar decisão do Policy Decision Point;
5. identificar primeiro span com erro ou latência anormal;
6. verificar backlog e DLQ;
7. confirmar budget e quota;
8. aplicar fallback ou bloquear componente afetado.

## Árvore rápida

| Sintoma | Verificação | Ação inicial |
|---|---|---|
| `401` | token, issuer, audience e clock skew | corrigir identidade |
| `403` | escopo, tenant e policy decision | revisar autorização, não liberar bypass |
| `404` | visibilidade do recurso e versão publicada | validar catálogo e tenant |
| `409` | idempotência ou estado | consultar operação original |
| `422` | policy violation e evidência faltante | corrigir configuração |
| `429` | quota, rate limit ou budget | reduzir consumo ou aprovar novo limite |
| `BLOCKED` | policy/guardrail | confirmar bloqueio esperado |
| `PARTIAL` | dependência degradada | informar limitação e acionar fallback |
| timeout | span mais lento e deadline | isolar provedor/tool e usar assíncrono |

## Contenção

- desabilitar versão ou tool específica, não a plataforma inteira;
- forçar fallback somente para modelos e regiões aprovados;
- preservar `deny by default`;
- pausar ações transacionais se auditoria estiver indisponível;
- comunicar impacto, escopo e workaround.

## Encerramento

- causa identificada;
- métricas normalizadas;
- mensagens na DLQ tratadas;
- smoke test concluído;
- timeline e evidências anexadas;
- ação preventiva registrada.
