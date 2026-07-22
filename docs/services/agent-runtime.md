# Agent Runtime

## Visão Geral

O Agent Runtime é o coração da Enterprise AI Platform. Ele executa agentes, orquestra chamadas para modelos, consulta memória, recupera conhecimento, executa ferramentas via MCP e publica eventos operacionais.

## Responsabilidades

- Executar agentes publicados
- Orquestrar prompts, ferramentas, memória e RAG
- Invocar foundation models
- Aplicar políticas de timeout, retry e circuit breaker
- Publicar eventos de uso, auditoria e cobrança
- Acionar avaliação de qualidade da resposta

## Fora de Escopo

- Aprovação de agentes
- Gestão de catálogo
- Ingestão documental
- Gestão de usuários
- Cálculo financeiro consolidado

## Principais Componentes Internos

| Componente | Responsabilidade |
|---|---|
| Agent Executor | Controla o ciclo de execução do agente |
| Prompt Engine | Monta prompts, system instructions e contexto |
| Tool Executor | Executa ferramentas permitidas |
| MCP Client | Integra com MCP Registry e MCP Servers |
| Memory Adapter | Consulta e atualiza memória |
| Knowledge Adapter | Consulta Knowledge Service |
| Model Adapter | Abstrai provedores de LLM |
| Evaluation Adapter | Encaminha respostas para avaliação |
| Event Publisher | Publica eventos Kafka |

## API Principal

```http
POST /agents/{agentId}/invoke
Content-Type: application/json
Authorization: Bearer <token>
```

### Request

```json
{
  "input": "Quais contratos vencem este mês?",
  "channel": "ai-portal",
  "sessionId": "session-123",
  "context": {
    "businessUnit": "credit",
    "locale": "pt-BR"
  }
}
```

### Response

```json
{
  "conversationId": "conv-123",
  "messageId": "msg-456",
  "answer": "Foram encontrados 12 contratos com vencimento neste mês.",
  "citations": [],
  "toolCalls": [],
  "evaluationStatus": "queued"
}
```

## Dependências

| Dependência | Uso |
|---|---|
| Agent Registry | Carregar configuração do agente |
| MCP Registry | Descobrir ferramentas disponíveis |
| Knowledge Service | Recuperar conhecimento para RAG |
| Memory Service | Persistir contexto conversacional |
| Evaluation Service | Avaliar resposta |
| Foundation Models | Executar inferência |
| Kafka | Publicar eventos |
| Redis | Cache e rate limit |

## Eventos Publicados

- `agent.invoked`
- `tool.executed`
- `evaluation.started`

## Requisitos Não Funcionais

| Requisito | Diretriz |
|---|---|
| Latência | P95 menor que 5s para agentes simples |
| Resiliência | Retry controlado para chamadas transitórias |
| Segurança | Autorização por agente, ferramenta e escopo |
| Observabilidade | Trace por invocation, model call e tool call |
| Escalabilidade | Escala horizontal por volume de invocações |
| Auditoria | Registro completo de entrada, saída e decisões relevantes |

## Decisões Relacionadas

- [ADR-004 — Agent Runtime com núcleo estável e adaptadores](../adrs/004-agent-runtime-strategy.md)
- [ADR-001 — MCP para tool calling governado](../adrs/001-mcp-vs-rest.md)
- [ADR-006 — OpenTelemetry como padrão de observabilidade](../adrs/006-observability-strategy.md)
