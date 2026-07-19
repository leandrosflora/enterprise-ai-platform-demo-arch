# Runbook — Onboarding e Publicação de Agente

## Objetivo

Publicar uma versão de agente com contratos, risco, segurança, avaliação, observabilidade, budget e rollback validados.

## Pré-requisitos

- owner técnico e owner de negócio definidos;
- Agent Card versionado;
- dataset de avaliação aprovado;
- knowledge bases e tools já registradas;
- budget e centro de custo definidos;
- acesso `agent.write`, `governance.submit` e permissões de teste.

## Procedimento

### 1. Validar o Agent Card

Obrigatório:

- `agentId`, nome e versão SemVer;
- owner e unidade de negócio;
- objetivo, usuários e dados utilizados;
- risco inicial;
- model policy por capacidade, sem credencial de provedor;
- tools e knowledge bases permitidas;
- classe de workload e SLO;
- política de memória.

**Critério de saída:** schema válido e nenhum campo bloqueante ausente.

### 2. Registrar a versão em DRAFT

```bash
curl -sS -X POST http://localhost:8080/v1/agents \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: policy-assistant-1.0.0-create' \
  -d @agent-card.json
```

**Esperado:** HTTP `201`, status `DRAFT` e `ETag`.

### 3. Validar dependências

- todos os MCP contracts estão aprovados;
- KBs aplicam ACL por documento/chunk;
- modelos solicitados estão no Model Catalog;
- secrets e regiões estão aprovados;
- política `deny by default` foi exercitada.

### 4. Executar avaliações

Executar ao menos:

- regression;
- groundedness/retrieval quando houver RAG;
- safety/adversarial;
- latência da classe de workload;
- custo por cenário.

**Critério de saída:** relatório reproduzível e thresholds atingidos.

### 5. Validar observabilidade

Executar uma invocação em ambiente de teste e confirmar:

- trace completo;
- decisão de política e versão;
- tokens e custo;
- eventos `agent.invoked` e dependências;
- ausência de payload sensível em logs.

### 6. Submeter para governança

```bash
curl -sS -X POST http://localhost:8080/v1/agents/policy-assistant:submit \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: policy-assistant-1.0.0-submit' \
  -d '{
    "agentVersion":"1.0.0",
    "riskClassification":"MEDIUM",
    "evidence":["evaluation-report.json","authorization-matrix.md","rollback-plan.md"]
  }'
```

**Esperado:** HTTP `202`, decisão `PENDING`.

### 7. Aprovar com segregação de função

A identidade que submeteu não pode aprovar. O aprovador valida os gates G1–G7.

**Esperado:** decisão `APPROVED`, com `approvalId` e trilha de auditoria.

### 8. Publicar

```bash
curl -sS -X POST http://localhost:8080/v1/agents/policy-assistant:publish \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: policy-assistant-1.0.0-publish' \
  -d '{"approvalId":"apv-001","releaseNotes":"Primeira versão"}'
```

**Esperado:** HTTP `202`, status `PUBLISHED` e evento `agent.published`.

### 9. Smoke test

- invocação autorizada retorna `SUCCESS` ou `PARTIAL` esperado;
- invocação sem escopo retorna `403`;
- tool não permitida retorna `BLOCKED`;
- dashboard mostra latência, tokens e custo;
- alertas de teste chegam ao canal correto.

## Rollback

1. bloquear novas invocações da versão;
2. restaurar a versão publicada anterior;
3. invalidar cache de configuração e políticas;
4. desabilitar tools afetadas;
5. preservar eventos, traces e evidências;
6. abrir incidente e registrar causa.

## Erros comuns

| Sintoma | Causa provável | Ação |
|---|---|---|
| `409 Conflict` | versão ou idempotency key já utilizada | consultar estado antes de repetir |
| `422 Policy Violation` | evidência, budget ou dependência ausente | corrigir o gate indicado |
| agente aprovado não publica | approval ID não corresponde à versão | refazer a publicação com a decisão correta |
| `BLOCKED` na invocação | policy bundle ausente ou desatualizado | validar distribuição e versão da política |
