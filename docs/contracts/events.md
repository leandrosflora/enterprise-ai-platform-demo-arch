# Contratos de Eventos

## Fonte canônica

O arquivo [`async-api.yaml`](async-api.yaml) é a fonte executável dos eventos. Este documento define as convenções normativas. Exemplos e implementações não podem criar envelopes ou enums alternativos.

## Transporte e versionamento

- Transporte de referência: Kafka.
- Serialização de referência: JSON UTF-8.
- Tópicos usam o formato `<evento>.v<major>`, por exemplo `agent.invoked.v1`.
- `schemaVersion` usa SemVer.
- Mudanças incompatíveis exigem novo major e novo tópico.
- Produtores não removem campos durante a vida de um major.
- Consumidores ignoram campos desconhecidos.

## Envelope obrigatório

```json
{
  "eventId": "8dcf94dc-0af0-4f99-95d9-e617424b2c4b",
  "eventType": "agent.invoked",
  "schemaVersion": "1.0.0",
  "occurredAt": "2026-07-19T12:00:00Z",
  "correlationId": "30b846cc-d3f5-4aaa-9b99-aaf519dca78e",
  "causationId": "msg-001",
  "tenantId": "enterprise",
  "source": "agent-runtime",
  "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
  "dataClassification": "INTERNAL",
  "payload": {}
}
```

Campos obrigatórios:

| Campo | Regra |
|---|---|
| `eventId` | UUID único usado para deduplicação. |
| `eventType` | Nome sem versão, igual ao domínio sem o sufixo do tópico. |
| `schemaVersion` | Versão SemVer do schema. Não usar `eventVersion`. |
| `occurredAt` | ISO 8601 UTC. |
| `correlationId` | Correlação funcional de toda a execução. |
| `tenantId` | Tenant derivado da identidade ou contexto confiável. |
| `source` | Serviço produtor. |
| `dataClassification` | `PUBLIC`, `INTERNAL`, `CONFIDENTIAL` ou `RESTRICTED`. |
| `payload` | Payload tipado pelo AsyncAPI. |

`causationId` e `traceparent` são obrigatórios quando existe uma causa ou contexto distribuído anterior.

## Enums compartilhados

### Risco

`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.

### Estado de execução

`SUCCESS`, `FAILED`, `BLOCKED`, `PARTIAL`.

### Classificação de dados

`PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`.

## Catálogo de tópicos

| Evento | Tópico | Produtor principal | Consumidores típicos |
|---|---|---|---|
| `agent.created` | `agent.created.v1` | Agent Registry | Governance, Audit |
| `agent.updated` | `agent.updated.v1` | Agent Registry | Governance, Audit |
| `agent.published` | `agent.published.v1` | Governance | Registry, Runtime, Audit |
| `agent.retired` | `agent.retired.v1` | Governance | Registry, Runtime, Audit |
| `agent.invoked` | `agent.invoked.v1` | Agent Runtime | Audit, Billing, Evaluation |
| `tool.executed` | `tool.executed.v1` | Agent Runtime | Audit, Billing |
| `model.invoked` | `model.invoked.v1` | Model Gateway | Billing, Observability |
| `knowledge.ingested` | `knowledge.ingested.v1` | Knowledge Service | Audit |
| `embedding.generated` | `embedding.generated.v1` | Knowledge Service | Billing, Audit |
| `document.indexed` | `document.indexed.v1` | Knowledge Service | Audit |
| `memory.updated` | `memory.updated.v1` | Memory Service | Audit |
| `evaluation.started` | `evaluation.started.v1` | Evaluation Service | Audit |
| `evaluation.completed` | `evaluation.completed.v1` | Evaluation Service | Governance, Audit |
| `governance.approved` | `governance.approved.v1` | Governance | Registry, Audit |
| `governance.rejected` | `governance.rejected.v1` | Governance | Registry, Audit |
| `audit.created` | `audit.created.v1` | Audit Service | Observability / Archive |

## Entrega, idempotência e ordenação

- Semântica padrão: **at-least-once**.
- Consumidores deduplicam por `eventId`.
- Chaves de partição:
  - agente: `tenantId + agentId`;
  - sessão: `tenantId + sessionId`;
  - documento: `tenantId + knowledgeBaseId + documentId`.
- Não existe garantia global de ordenação entre tópicos.
- Comandos críticos usam outbox transacional no produtor.
- Consumidores persistem offset somente após concluir o processamento idempotente.

## Erros e DLQ

- Retry com backoff apenas para falhas transitórias.
- Eventos inválidos não são repetidos indefinidamente.
- DLQ por domínio com payload original, erro sanitizado e metadados de tentativa.
- Reprocessamento exige autorização, auditoria e preservação do `eventId` original.

## Segurança

- Payloads não devem transportar prompts completos ou dados pessoais quando metadados bastarem.
- Campos sensíveis são mascarados antes da publicação.
- ACLs de tópicos seguem least privilege.
- Eventos `CONFIDENTIAL` e `RESTRICTED` usam criptografia e retenção compatíveis com a classificação.

## Retenção de referência

| Classe | Retenção inicial | Observação |
|---|---:|---|
| Operacional | 90 dias | Diagnóstico e replay limitado. |
| Billing | 24 meses | Showback e chargeback. |
| Auditoria | 5 anos | Ajustar à obrigação regulatória aplicável. |
| DLQ | 30 dias | Reprocessamento controlado. |

Prazos são referências e devem ser aprovados por Jurídico, Segurança e LGPD para cada organização.
