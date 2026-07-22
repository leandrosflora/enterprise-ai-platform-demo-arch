# Agent Gateway

## Visão Geral

O Agent Gateway é o ponto único de entrada para invocações de agentes. Autentica e autoriza a chamada, aplica rate limiting e roteia a invocação para o Agent Runtime.

## Responsabilidades

- Expor a API pública de invocação de agentes
- Autenticar requisições via Identity Provider (OIDC)
- Autorizar acesso por agente e escopo
- Aplicar rate limiting e cache de curta duração
- Rotear a invocação para o Agent Runtime

## Fora de Escopo

- Execução do agente e orquestração de prompts, ferramentas e memória
- Avaliação de qualidade da resposta
- Aprovação e ciclo de vida do agente

## API Principal

```http
POST /agents/{agentId}/invoke
GET /agents/{agentId}
Authorization: Bearer <token>
```

## Dependências

| Dependência | Uso |
|---|---|
| Identity Provider | Autenticação e autorização (OIDC) |
| Agent Runtime | Roteamento da invocação |
| Redis | Cache e rate limiting |

## Requisitos Não Funcionais

| Requisito | Diretriz |
|---|---|
| Latência | Overhead mínimo antes de rotear para o Agent Runtime |
| Segurança | Autenticação e autorização em toda requisição |
| Escalabilidade | Escala horizontal por volume de invocações |
| Resiliência | Rate limiting para proteger o Agent Runtime contra picos |

## Decisões Relacionadas

- [ADR-004 — Agent Runtime com núcleo estável e adaptadores](../adrs/004-agent-runtime-strategy.md)
