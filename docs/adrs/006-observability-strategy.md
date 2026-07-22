# ADR-006 — OpenTelemetry como padrão de observabilidade

**Status:** Aceito

## Contexto

Soluções com agentes e modelos generativos exigem rastreabilidade além de logs tradicionais. Uma execução pode atravessar gateway, runtime, políticas, memória, retrieval, modelos, ferramentas, avaliação e eventos, com impacto simultâneo em qualidade, segurança, custo e latência.

## Decisão

Adotar **OpenTelemetry** como padrão de traces, métricas e logs correlacionados. Cada invocação deve possuir trace ponta a ponta e spans específicos para decisões de política, retrieval, memória, model calls, tool calls, avaliação e auditoria.

Eventos assíncronos devem propagar contexto W3C e manter `correlationId` e `causationId` quando aplicável.

## Requisitos obrigatórios

- `agent.id`, `agent.version`, `tenant.id` e classificação de risco na execução;
- versão efetiva de modelo, prompt, policy, tool e knowledge snapshot;
- tokens, custo, latência, retries e fallback;
- decisão de autorização sem registrar secrets ou payload sensível bruto;
- mascaramento antes da exportação;
- controle de cardinalidade de métricas;
- retenção e acesso proporcionais à classificação do dado;
- correlação com eventos de auditoria e avaliação.

## Alternativas

| Alternativa | Vantagem | Limitação |
|---|---|---|
| Logs customizados por serviço | implementação local simples | correlação e semântica inconsistentes |
| Instrumentação proprietária única | integração rápida com um fornecedor | lock-in e portabilidade reduzida |
| Apenas eventos de auditoria | boa trilha de negócio | diagnóstico técnico e performance insuficientes |

## Consequências positivas

- correlação ponta a ponta entre capacidades;
- integração com stacks corporativas existentes;
- base comum para SRE, segurança, avaliação e FinOps;
- troca de backend sem alterar a instrumentação principal.

## Consequências negativas

- aumenta volume e custo de telemetria;
- exige governança de atributos e cardinalidade;
- instrumentação incorreta pode vazar dados ou gerar falsa confiança;
- sampling precisa preservar eventos críticos.

## Evidências mínimas

- trace de referência cobrindo uma invocação completa;
- catálogo de spans, atributos e métricas;
- teste de propagação HTTP e assíncrona;
- teste de redaction e ausência de secrets;
- dashboards, alertas e SLOs associados;
- política de retenção, sampling e acesso.

## Critérios de revisão

Revisar quando o padrão deixar de atender interoperabilidade, volume ou requisitos de segurança, ou quando a instrumentação causar custo operacional desproporcional ao diagnóstico e à governança obtidos.
