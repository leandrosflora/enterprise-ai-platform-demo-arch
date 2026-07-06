# Tracing

## Objetivo

Garantir rastreabilidade ponta a ponta das execuções dos agentes, cobrindo invocação, memória, RAG, chamada de modelo, ferramentas MCP, avaliação, auditoria e FinOps.

## Padrão

- OpenTelemetry para traces, métricas e logs correlacionados.
- `traceId`, `spanId`, `correlationId` e `causationId` obrigatórios em toda fronteira síncrona e assíncrona.
- Propagação de contexto em HTTP headers e Kafka event envelope.
- Logs estruturados em JSON.

---

## Trace Principal: Agent Invocation

```text
agent.invocation
  ├─ agent.gateway.authenticate
  ├─ agent.gateway.authorize
  ├─ agent.runtime.load_configuration
  ├─ agent.runtime.policy_enforcement
  ├─ memory.retrieve
  ├─ knowledge.retrieve
  │   ├─ knowledge.embedding.generate
  │   └─ knowledge.vector_search
  ├─ prompt.build
  ├─ model.invoke
  ├─ tool.execute
  │   ├─ mcp.registry.discover
  │   └─ mcp.tool.invoke
  ├─ evaluation.submit
  ├─ event.publish
  └─ audit.record
```

---

## Spans Obrigatórios

| Span | Componente | Quando usar | Atributos obrigatórios |
|---|---|---|---|
| `agent.invocation` | Agent Gateway | Span raiz da invocação | `agent.id`, `agent.version`, `tenant.id`, `channel`, `user.id.hash`, `risk.classification` |
| `agent.gateway.authenticate` | Agent Gateway | Validação JWT/OIDC | `auth.provider`, `auth.result`, `tenant.id` |
| `agent.gateway.authorize` | Agent Gateway | Validação de escopos | `auth.scopes`, `auth.decision`, `policy.id` |
| `agent.runtime.load_configuration` | Agent Runtime | Carga de configuração do agente | `agent.id`, `agent.version`, `registry.cache_hit` |
| `agent.runtime.policy_enforcement` | Agent Runtime | Aplicação de política | `policy.id`, `policy.decision`, `blocked.reason` |
| `memory.retrieve` | Memory Service | Leitura de memória | `session.id`, `memory.type`, `memory.items_count` |
| `memory.write` | Memory Service | Atualização de memória | `session.id`, `memory.items_count`, `data.classification` |
| `knowledge.retrieve` | Knowledge Service | Busca RAG | `knowledge_base.id`, `retrieval.strategy`, `top_k` |
| `knowledge.embedding.generate` | Knowledge Service | Geração de embedding | `model.provider`, `model.id`, `input.tokens` |
| `knowledge.vector_search` | Knowledge Service | Busca vetorial/híbrida | `vector.index`, `result.count`, `score.max`, `latency.ms` |
| `prompt.build` | Agent Runtime | Montagem do prompt | `prompt.template_id`, `input.tokens.estimated`, `context.sources_count` |
| `model.invoke` | Agent Runtime | Chamada ao LLM | `model.provider`, `model.id`, `input.tokens`, `output.tokens`, `cost.usd`, `latency.ms` |
| `tool.execute` | Agent Runtime | Execução de ferramenta MCP | `tool.name`, `tool.version`, `tool.status`, `tool.risk`, `latency.ms` |
| `mcp.registry.discover` | MCP Registry | Descoberta de ferramenta | `tool.name`, `registry.cache_hit`, `policy.decision` |
| `mcp.tool.invoke` | MCP Server | Chamada à ferramenta | `tool.name`, `tool.version`, `idempotency.required`, `status` |
| `evaluation.submit` | Evaluation Service | Submissão para avaliação | `evaluation.type`, `evaluation.status`, `dataset.id` |
| `event.publish` | Platform Events | Publicação Kafka | `messaging.system`, `messaging.destination`, `event.type`, `schema.version` |
| `audit.record` | Audit Service | Registro auditável | `audit.event_type`, `retention.class`, `audit.status` |

---

## Atributos Globais Obrigatórios

| Atributo | Descrição |
|---|---|
| `trace.id` | Trace distribuído. |
| `correlation.id` | Correlação funcional entre requisições e eventos. |
| `causation.id` | Identificador da ação/evento causador. |
| `tenant.id` | Tenant/organização. |
| `business_unit` | Unidade de negócio quando aplicável. |
| `agent.id` | Identificador do agente. |
| `agent.version` | Versão do agente. |
| `session.id` | Sessão conversacional. |
| `user.id.hash` | Hash do usuário, nunca identificador sensível em claro. |
| `data.classification` | `PUBLIC`, `INTERNAL`, `CONFIDENTIAL` ou `RESTRICTED`. |
| `risk.classification` | `LOW`, `MEDIUM`, `HIGH` ou `CRITICAL`. |

---

## Métricas Obrigatórias

| Métrica | Tipo | Dimensões | Objetivo |
|---|---|---|---|
| `agent_invocations_total` | Counter | `agent.id`, `tenant.id`, `status` | Volume e taxa de erro. |
| `agent_invocation_latency_ms` | Histogram | `agent.id`, `channel`, `risk.classification` | P50/P90/P95/P99 de resposta. |
| `model_invocations_total` | Counter | `model.provider`, `model.id`, `status` | Uso de modelos. |
| `model_tokens_total` | Counter | `model.provider`, `model.id`, `token.type` | Tokens de entrada/saída. |
| `model_cost_usd_total` | Counter | `agent.id`, `business_unit`, `model.provider` | Custo atribuído. |
| `tool_executions_total` | Counter | `tool.name`, `status`, `risk.classification` | Uso e falha de ferramentas. |
| `rag_retrieval_latency_ms` | Histogram | `knowledge_base.id`, `strategy` | Latência de recuperação. |
| `rag_groundedness_score` | Gauge | `agent.id`, `dataset.id` | Qualidade de resposta fundamentada. |
| `evaluation_failures_total` | Counter | `agent.id`, `evaluation.type` | Falhas de quality gates. |
| `policy_denials_total` | Counter | `policy.id`, `resource.type`, `reason` | Bloqueios de segurança/governança. |
| `dlq_events_total` | Counter | `event.type`, `consumer` | Falhas assíncronas. |

---

## SLOs de Referência

| Capacidade | SLI | SLO | Janela |
|---|---|---:|---|
| Agent Invocation simples | P95 latency | <= 5s | 30 dias |
| Agent Invocation com RAG | P95 latency | <= 8s | 30 dias |
| Tool execution | P95 latency | <= 4s | 30 dias |
| Knowledge retrieval | P95 latency | <= 2s | 30 dias |
| Agent availability | Success rate | >= 99.5% | 30 dias |
| Event publishing | Success rate | >= 99.9% | 30 dias |
| Evaluation processing | P95 completion | <= 2min | 30 dias |
| Audit recording | Success rate | >= 99.99% | 30 dias |
| Policy enforcement | Decision latency P95 | <= 100ms | 30 dias |

---

## Alertas

| Alerta | Condição | Severidade | Ação |
|---|---|---|---|
| AgentErrorRateHigh | Erro > 5% por 10 min | Alta | Acionar owner do agente. |
| ModelProviderLatencyHigh | P95 > 10s por 15 min | Média | Avaliar fallback/degradação. |
| ToolExecutionFailures | Falha > 3% por 10 min | Alta | Bloquear ferramenta crítica se necessário. |
| PolicyDenialsSpike | Aumento > 3x da baseline | Média | Investigar abuso ou configuração incorreta. |
| CostBudgetExceeded | Uso > 90% do budget mensal | Média | Notificar FinOps e owner. |
| AuditRecordingFailure | Qualquer falha por 5 min | Crítica | Pausar publicação de agentes críticos. |
| DLQBacklogGrowing | DLQ crescendo por 15 min | Alta | Acionar runbook de reprocessamento. |

---

## Logs Estruturados

Campos mínimos em logs de aplicação:

```json
{
  "timestamp": "2026-07-06T12:00:00Z",
  "level": "INFO",
  "service.name": "agent-runtime",
  "trace.id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span.id": "00f067aa0ba902b7",
  "correlation.id": "7d8cf2aa-ef5f-4cc3-bafa-61ea26277511",
  "tenant.id": "enterprise",
  "agent.id": "policy-assistant",
  "event.name": "model.invoke.completed",
  "model.provider": "bedrock",
  "model.id": "anthropic.claude-3-5-sonnet",
  "input.tokens": 1250,
  "output.tokens": 430,
  "latency.ms": 2850,
  "status": "SUCCESS"
}
```

## Regras de Segurança para Observabilidade

- Não registrar prompt completo quando contiver dados pessoais ou classificação `CONFIDENTIAL`/`RESTRICTED`.
- Mascarar CPF, e-mail, telefone, tokens, secrets e identificadores financeiros.
- Logs de auditoria devem preservar evidência funcional, não payload sensível bruto.
- Traces devem carregar hashes ou IDs técnicos, nunca segredo em claro.
