# Runbook — Onboarding de MCP Server e Tool

## Objetivo

Registrar e liberar uma ferramenta MCP com contrato, autenticação, autorização, idempotência, auditoria e rollback definidos.

## Pré-requisitos

- owner técnico e de negócio;
- ambiente de teste;
- autenticação por workload identity;
- OpenAPI ou contrato do sistema de destino;
- classificação de dados;
- definição de leitura ou escrita;
- runbook do sistema corporativo.

## Procedimento

### 1. Classificar a tool

Documentar:

- finalidade;
- efeitos colaterais;
- sistemas e dados acessados;
- risco `LOW`, `MEDIUM`, `HIGH` ou `CRITICAL`;
- necessidade de human approval;
- timeout e limite de concorrência.

### 2. Definir o contrato

Obrigatório:

- nome e versão SemVer;
- JSON Schema de entrada e saída;
- campos obrigatórios e limites;
- códigos de erro estáveis;
- política de idempotência;
- escopos;
- exemplos válidos e inválidos.

### 3. Implementar controles

- validação server-side de todos os argumentos;
- allowlist de operações;
- autorização no sistema de destino, não apenas no Runtime;
- secret manager;
- timeout, circuit breaker e bulkhead;
- idempotency key para escrita;
- redaction de logs;
- operação reversível ou compensação quando possível.

### 4. Testar

Casos mínimos:

- entrada válida;
- campo ausente e formato inválido;
- identidade sem escopo;
- acesso cross-tenant;
- timeout do destino;
- repetição com mesma idempotency key;
- tentativa de prompt/tool injection;
- falha parcial;
- rollback ou compensação.

### 5. Registrar no MCP Registry

Registrar contrato, owner, risco, endpoint, identidade de workload, SLO e evidências.

**Critério de saída:** status `SUBMITTED`, nunca disponível para descoberta produtiva.

### 6. Aprovar

- Security valida autenticação, egress e secrets;
- LGPD valida finalidade e minimização quando aplicável;
- AI Architect valida escopo e uso por agentes;
- owner do sistema de destino valida capacidade e rollback.

### 7. Publicar e vincular

A publicação torna a versão descobrível apenas para agentes explicitamente autorizados. Não usar wildcard de tool em produção.

### 8. Smoke test

- descoberta autorizada funciona;
- descoberta não autorizada retorna vazio ou negação;
- execução gera `tool.executed`;
- trace contém tool, versão, status e operation ID;
- repetição idempotente não duplica efeito;
- métricas e alertas estão ativos.

## Rollback

1. retirar a versão da descoberta;
2. bloquear execução no policy enforcement;
3. manter a versão anterior quando segura;
4. compensar operações pendentes quando aplicável;
5. preservar auditoria;
6. notificar owners dos agentes consumidores.

## Critérios de rejeição imediata

- secret no contrato ou código;
- autorização apenas no prompt;
- escrita sem idempotência;
- ausência de timeout;
- schema aberto sem justificativa;
- tool genérica que permite executar comandos arbitrários;
- ausência de owner ou rollback.
