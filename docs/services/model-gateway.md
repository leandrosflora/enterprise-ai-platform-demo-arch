# Model Gateway

## Visão Geral

O Model Gateway centraliza o acesso a foundation models e impede que runtimes de agentes chamem provedores diretamente.

## Responsabilidades

- aplicar allowlist de provedores, modelos e regiões;
- rotear por capacidade, custo, latência, disponibilidade e classificação de dados;
- validar budgets, quotas e limites de tokens;
- executar redaction e guardrails de entrada e saída;
- padronizar timeout, retry, circuit breaker e fallback;
- registrar versão efetiva do modelo, tokens, custo e latência;
- bloquear modelos ou regiões não aprovados;
- suportar respostas síncronas e streaming.

## Fora de Escopo

- orquestração do agente;
- gestão do catálogo de agentes;
- avaliação de negócio da resposta;
- persistência de memória conversacional.

## API interna

```http
POST /internal/v1/model-invocations
Authorization: Bearer <workload-token>
X-Correlation-Id: <uuid>
Content-Type: application/json
```

```json
{
  "agentId": "policy-assistant",
  "agentVersion": "1.0.0",
  "riskClassification": "MEDIUM",
  "dataClassification": "INTERNAL",
  "requestedCapability": "TEXT_GENERATION",
  "stream": false,
  "messages": [
    {"role": "user", "content": "Resuma a política."}
  ],
  "constraints": {
    "maxInputTokens": 8000,
    "maxOutputTokens": 1200,
    "maxCostUsd": 0.05,
    "allowedRegions": ["us-east-1"]
  }
}
```

## Políticas de roteamento

Ordem padrão:

1. compatibilidade com classificação e residência de dados;
2. modelo aprovado para o agente;
3. disponibilidade do provedor;
4. qualidade mínima registrada;
5. budget restante;
6. menor custo dentro do SLO.

## Segurança

- autenticação por workload identity;
- autorização por agente, modelo e tenant;
- nenhum secret de provedor é exposto ao Runtime;
- prompts sensíveis não são armazenados por padrão;
- logs usam hashes e metadados, nunca secrets;
- saída passa por guardrails antes de retornar ao Runtime.

## Observabilidade

Spans obrigatórios:

- `model.gateway.authorize`
- `model.gateway.route`
- `model.gateway.redact`
- `model.provider.invoke`
- `model.gateway.guardrail`

Métricas mínimas:

- invocações por modelo e status;
- tokens de entrada e saída;
- custo por agente e unidade;
- latência por provedor;
- taxa de fallback;
- bloqueios de política;
- violações de budget.

## Eventos

- `model.invoked`
- `model.fallback.executed`
- `model.policy.blocked`
- `budget.threshold.reached`
