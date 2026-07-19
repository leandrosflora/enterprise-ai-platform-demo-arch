# AI Risk Framework

## Objetivo

Classificar riscos de IA, definir controles proporcionais e estabelecer evidências verificáveis para publicação e operação.

## Categorias

| Categoria | Exemplos |
|---|---|
| Segurança | Prompt injection, tool abuse, exfiltração, excessive agency. |
| Privacidade e compliance | LGPD, retenção, consentimento, transferência internacional. |
| Operacional | Indisponibilidade, falhas de integração, degradação de modelo. |
| Modelo | Hallucination, bias, toxicidade, regressão e baixa explicabilidade. |
| Financeiro | Consumo inesperado, ausência de quotas e chargeback. |
| Reputacional | Respostas inadequadas e decisões opacas. |

## Classificação

| Nível | Critério |
|---|---|
| LOW | Uso interno, sem dados sensíveis, sem ação transacional. |
| MEDIUM | Dados internos/confidenciais, RAG ou apoio à decisão humana. |
| HIGH | Dados pessoais/sensíveis, ferramenta de escrita ou impacto operacional relevante. |
| CRITICAL | Decisão automatizada regulada, impacto material em cliente, financeiro ou legal. |

## Matriz de riscos e controles

| Risco | Severidade padrão | Controles obrigatórios | Evidências |
|---|---:|---|---|
| Direct/indirect prompt injection | HIGH | segmentação de instruções, content scanning, tool allowlist, adversarial evaluation | testes de ataque e logs de bloqueio |
| Data leakage | CRITICAL | classificação, masking, tenant isolation, DLP, output filtering | teste de isolamento e relatório de classificação |
| Tool abuse | HIGH | escopos mínimos, policy enforcement, idempotência, aprovação humana | contrato aprovado, matriz de autorização, eventos |
| Excessive agency | HIGH | limites de autonomia, transaction boundary, human-in-the-loop | cenários de bloqueio e rollback |
| Hallucination | MEDIUM | RAG, citações, groundedness, fallback | dataset e relatório de avaliação |
| Poisoned knowledge | HIGH | proveniência, quarantine, aprovação de fonte, reindexação controlada | checksum, lineage e teste de conteúdo malicioso |
| Memory poisoning | HIGH | origem dos fatos, TTL, confirmação, isolamento por usuário | testes de contaminação cruzada |
| Bias | HIGH | revisão de dataset, fairness quando aplicável, revisão humana | critérios e relatório |
| Uso de dado sem base legal | CRITICAL | finalidade, minimização, retenção e aprovação LGPD | DPIA/LIA quando aplicável |
| Provider outage | MEDIUM | timeout, circuit breaker, bulkhead, fallback | teste de resiliência e runbook |
| Custo inesperado | MEDIUM | quotas, budgets, rate limits, alertas e bloqueio | dashboard e teste de limite |
| Falta de rastreabilidade | HIGH | trace context, audit trail, retenção e policy version | trace e evento de auditoria |
| Regressão de qualidade | MEDIUM | baseline, regression dataset e gate de deploy | relatório comparativo |
| Acesso indevido a KB | HIGH | ACL por documento/chunk, ABAC e filtros server-side | teste de acesso negado |

## Controles por nível

| Controle | LOW | MEDIUM | HIGH | CRITICAL |
|---|---:|---:|---:|---:|
| Owner definido | Obrigatório | Obrigatório | Obrigatório | Obrigatório |
| Avaliação automática | Obrigatório | Obrigatório | Obrigatório | Obrigatório |
| Revisão AI Architect | Opcional | Obrigatório | Obrigatório | Obrigatório |
| Revisão Security | Conforme escopo | Conforme escopo | Obrigatório | Obrigatório |
| Revisão LGPD | Conforme dados | Conforme dados | Obrigatório | Obrigatório |
| Jurídico/Regulatório | Não | Conforme escopo | Conforme escopo | Obrigatório |
| Auditoria | Básica | Completa | Completa | Completa + retenção estendida |
| Human-in-the-loop | Não | Conforme ação | Obrigatório para escrita crítica | Obrigatório |
| Rollback | Recomendado | Recomendado | Obrigatório | Obrigatório |
| FinOps budget | Recomendado | Obrigatório | Obrigatório | Obrigatório + bloqueio |

## Evidências mínimas

- Agent Card versionado;
- risk assessment com justificativa;
- evaluation report reproduzível;
- security review e threat model do caso de uso;
- LGPD review quando houver dado pessoal;
- matriz de autorização;
- traces, dashboards e alertas;
- budget e quotas;
- plano de rollback;
- runbook operacional.

## Gates de publicação

| Gate | Condição |
|---|---|
| G1 — Design | domínio, contratos, dados, dependências e owner definidos |
| G2 — Security/LGPD | classificação, autorização e threat model aprovados |
| G3 — Evaluation | thresholds do caso de uso atingidos |
| G4 — Observability | telemetria e alertas validados |
| G5 — FinOps | budget, quota e atribuição configurados |
| G6 — Operational readiness | runbook, capacidade, backup e rollback testados |
| G7 — Go-live | segregação de função e aprovação final registradas |

## Thresholds de qualidade

Thresholds são definidos por caso de uso e dataset. Valores iniciais:

| Métrica | LOW | MEDIUM | HIGH | CRITICAL |
|---|---:|---:|---:|---:|
| Groundedness mínimo para RAG | 0,80 | 0,85 | 0,90 | 0,95 |
| Relevance mínimo | 0,75 | 0,80 | 0,85 | 0,90 |
| Hallucination risk máximo | 0,15 | 0,10 | 0,05 | 0,03 |
| Toxicity máximo | 0,05 | 0,03 | 0,02 | 0,01 |

Latência não é threshold de risco. Ela segue a classe de workload definida nos requisitos não funcionais.

## Policy as code

Controles bloqueantes devem ser automatizados sempre que possível:

- agente sem owner ou risco não pode ser submetido;
- ferramenta não aprovada não pode ser vinculada;
- agente HIGH/CRITICAL sem dataset aprovado não pode ser publicado;
- budget ausente bloqueia MEDIUM ou superior;
- mesma identidade não pode submeter e aprovar;
- versão publicada é imutável;
- política inexistente resulta em `deny by default`.
