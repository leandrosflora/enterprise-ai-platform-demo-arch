# Tracing, Métricas e SLOs

## Padrão

- OpenTelemetry para traces, métricas e logs correlacionados.
- W3C `traceparent` propagado por HTTP e no envelope Kafka.
- `traceId`, `spanId`, `correlationId`, `causationId` e `tenant.id` nas fronteiras aplicáveis.
- Logs estruturados em JSON.
- Dados sensíveis são mascarados antes da exportação.

## Trace principal

```text
agent.invocation
  ├─ agent.gateway.authenticate
  ├─ agent.gateway.authorize
  ├─ agent.runtime.load_configuration
  ├─ policy.evaluate
  ├─ memory.retrieve
  ├─ knowledge.retrieve
  │   ├─ knowledge.authorize_documents
  │   ├─ knowledge.embedding.generate
  │   └─ knowledge.vector_search
  ├─ prompt.build
  ├─ model.gateway.authorize
  ├─ model.gateway.route
  ├─ model.provider.invoke
  ├─ model.gateway.guardrail
  ├─ tool.execute
  │   ├─ mcp.registry.discover
  │   ├─ policy.evaluate_tool
  │   └─ mcp.tool.invoke
  ├─ evaluation.submit
  ├─ event.publish
  └─ audit.record
```

## Spans obrigatórios

| Span | Componente | Atributos obrigatórios |
|---|---|---|
| `agent.invocation` | Gateway | `agent.id`, `agent.version`, `tenant.id`, `channel`, `workload.class`, `risk.classification` |
| `agent.gateway.authenticate` | Gateway | `auth.provider`, `auth.result` |
| `agent.gateway.authorize` | Gateway | `auth.scopes`, `policy.id`, `policy.version`, `policy.decision` |
| `agent.runtime.load_configuration` | Runtime | `agent.id`, `agent.version`, `registry.cache_hit` |
| `policy.evaluate` | PDP/PEP | `policy.id`, `policy.version`, `decision`, `reason` |
| `memory.retrieve` | Memory | `session.id.hash`, `memory.type`, `memory.items_count`, `data.classification` |
| `memory.write` | Memory | `session.id.hash`, `operation`, `ttl.seconds`, `data.classification` |
| `knowledge.retrieve` | Knowledge | `knowledge_base.id`, `retrieval.strategy`, `top_k` |
| `knowledge.authorize_documents` | Knowledge | `candidate.count`, `authorized.count`, `policy.version` |
| `knowledge.embedding.generate` | Knowledge | `model.id`, `input.tokens` |
| `knowledge.vector_search` | Knowledge | `vector.index`, `result.count`, `score.max` |
| `prompt.build` | Runtime | `prompt.template_id`, `context.sources_count`, `input.tokens.estimated` |
| `model.gateway.authorize` | Model Gateway | `model.capability`, `data.classification`, `policy.decision` |
| `model.gateway.route` | Model Gateway | `provider.selected`, `model.selected`, `region.selected`, `fallback.rank` |
| `model.provider.invoke` | Model Gateway | `model.provider`, `model.id`, `input.tokens`, `output.tokens`, `cost.usd` |
| `model.gateway.guardrail` | Model Gateway | `guardrail.id`, `guardrail.version`, `decision` |
| `tool.execute` | Runtime | `tool.name`, `tool.version`, `tool.status`, `tool.risk` |
| `mcp.tool.invoke` | MCP Server | `tool.name`, `idempotency.required`, `operation.id`, `status` |
| `evaluation.submit` | Evaluation | `evaluation.type`, `dataset.id`, `status` |
| `event.publish` | Event backbone | `messaging.destination`, `event.type`, `schema.version` |
| `audit.record` | Audit | `audit.event_type`, `retention.class`, `audit.status` |

## Atributos globais

| Atributo | Regra |
|---|---|
| `tenant.id` | Obrigatório, sem cardinalidade livre. |
| `business_unit` | Quando aplicável. |
| `agent.id` e `agent.version` | Obrigatórios em execução de agente. |
| `session.id.hash` | Hash, nunca sessão sensível em claro. |
| `user.id.hash` | Hash estável apenas quando necessário. |
| `data.classification` | `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`. |
| `risk.classification` | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`. |
| `workload.class` | Classe definida nos NFRs. |

## Métricas

| Métrica | Tipo | Dimensões permitidas |
|---|---|---|
| `agent_invocations_total` | Counter | agente, tenant, status |
| `agent_invocation_duration_seconds` | Histogram | agente, workload, status |
| `policy_decision_duration_seconds` | Histogram | policy, decisão |
| `policy_denials_total` | Counter | policy, recurso, motivo controlado |
| `model_invocations_total` | Counter | provedor, modelo, status |
| `model_tokens_total` | Counter | provedor, modelo, tipo |
| `model_cost_usd_total` | Counter | agente, unidade, provedor |
| `model_fallback_total` | Counter | provedor origem/destino |
| `tool_executions_total` | Counter | ferramenta, status, risco |
| `knowledge_retrieval_duration_seconds` | Histogram | base, estratégia |
| `knowledge_authorization_filtered_total` | Counter | base, classificação |
| `evaluation_score` | Gauge | agente, dataset, métrica |
| `dlq_events_total` | Counter | evento, consumidor |

Não usar IDs de usuário, sessão, documento ou correlation ID como labels de métricas.

## SLOs de referência

| Capacidade | SLI | SLO | Janela |
|---|---|---:|---|
| `INTERACTIVE_SIMPLE` | P95 end-to-end | <= 5 s | 30 dias |
| `INTERACTIVE_RAG` | P95 end-to-end | <= 8 s | 30 dias |
| `INTERACTIVE_TOOL` | P95 end-to-end | <= 15 s | 30 dias |
| Operação assíncrona | P95 de aceite | <= 2 s | 30 dias |
| Knowledge retrieval | P95 | <= 2 s | 30 dias |
| Policy decision | P95 | <= 100 ms | 30 dias |
| Agent Gateway | Disponibilidade | >= 99,95% | 30 dias |
| Agent Runtime | Disponibilidade | >= 99,9% | 30 dias |
| Event publishing | Sucesso | >= 99,9% | 30 dias |
| Audit recording crítico | Sucesso | >= 99,99% | 30 dias |

## Alertas

| Alerta | Condição | Severidade | Runbook |
|---|---|---|---|
| AgentErrorRateHigh | erro > 5% por 10 min | Alta | troubleshooting-agent-invocation |
| SloBurnRateFast | burn rate > 14,4x por 5 min | Crítica | troubleshooting-agent-invocation |
| ModelProviderLatencyHigh | P95 > limite por 15 min | Média | fallback de provedor |
| ToolExecutionFailures | falha > 3% por 10 min | Alta | desabilitar tool crítica |
| PolicyDenialsSpike | > 3x baseline | Média | revisar abuso/configuração |
| CostBudgetExceeded | budget >= 100% | Alta | bloquear/degradar agente |
| AuditRecordingFailure | qualquer falha por 5 min | Crítica | pausar ações críticas |
| DLQBacklogGrowing | backlog crescente por 15 min | Alta | reprocessamento controlado |

## Segurança de telemetria

- não registrar prompt completo com dados pessoais ou classificação `CONFIDENTIAL`/`RESTRICTED`;
- mascarar CPF, e-mail, telefone, tokens, secrets e identificadores financeiros;
- auditoria preserva evidência funcional, não payload sensível bruto;
- traces usam IDs técnicos ou hashes;
- acesso a traces sensíveis exige autorização e é auditado.
