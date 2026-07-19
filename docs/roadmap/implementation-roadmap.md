# Implementation Roadmap

## Baseline entregue neste repositório

A referência já contém:

- Enterprise AI Platform Book com jornadas por perfil;
- capability map e fronteiras de responsabilidade;
- operating model, RACI, fóruns e golden path;
- ciclo de vida de agentes baseado em risco e evidências;
- estudo de caso ponta a ponta de agente documental com RAG;
- decision guides e checklists de produção;
- exportação automatizada do book para Markdown e PDF;
- contratos OpenAPI e AsyncAPI canônicos;
- policies e validações de contrato em CI;
- C4 de container e deployment com control plane/data plane;
- Model Gateway explícito;
- segurança executável de RAG e memória;
- runbooks operacionais;
- vertical slice executável com Docker Compose;
- documentação publicável via MkDocs e GitHub Pages.

A vertical slice é deliberadamente pequena. As fases abaixo descrevem a evolução de uma implementação real para produção.

## Fase 1 — Foundation

### Objetivo

Criar o data plane mínimo para execução controlada de agentes.

### Entregas

- Agent Gateway;
- Agent Runtime;
- Agent Registry;
- OIDC e workload identity;
- Policy Decision Point e Policy Enforcement Points;
- Model Gateway;
- baseline OpenTelemetry;
- backbone Kafka;
- CI/CD com contract tests.

### Critérios de sucesso

- primeiro agente publicado por pipeline;
- trace ponta a ponta;
- eventos canônicos publicados;
- autorização `deny by default` exercitada;
- rollback validado;
- SLO de `INTERACTIVE_SIMPLE` medido.

## Fase 2 — Knowledge e Memory

### Entregas

- Knowledge Service;
- pipeline de ingestão com quarantine;
- ACL por documento e chunk;
- embeddings versionados;
- busca híbrida;
- citações;
- Memory Service com TTL, consentimento e exclusão;
- avaliação separada de retrieval e geração.

### Critérios de sucesso

- acesso cross-tenant bloqueado em testes;
- documentos eliminados deixam de aparecer no retrieval;
- groundedness e retrieval metrics coletadas;
- memory poisoning coberto por testes.

## Fase 3 — MCP e ferramentas corporativas

### Entregas

- MCP Registry;
- onboarding automatizado;
- tool contracts versionados;
- idempotência e outbox para escrita;
- human approval para ações críticas;
- auditoria e métricas por tool.

### Critérios de sucesso

- descoberta limitada por agente e política;
- repetição não duplica efeitos;
- tools podem ser bloqueadas sem indisponibilizar o Runtime;
- rollback ou compensação testados.

## Fase 4 — Governance e Evaluation

### Entregas

- AI Catalog;
- workflow com segregação de funções;
- risk assessment automatizado;
- datasets e baselines;
- quality gates;
- evidências imutáveis;
- model lifecycle.

### Critérios de sucesso

- nenhuma versão HIGH/CRITICAL publicada sem evidências;
- mesma identidade não submete e aprova;
- regressões bloqueiam deploy;
- thresholds são rastreáveis ao dataset e versão.

## Fase 5 — Scale e FinOps

### Entregas

- multi-tenant isolation endurecido;
- autoscaling por concorrência e backlog;
- budgets, quotas e chargeback;
- marketplace interno;
- disaster recovery;
- dashboards executivos;
- operação multi-região quando justificada.

### Critérios de sucesso

- custos atribuídos por área, agente e modelo;
- noisy neighbor controlado;
- testes de capacidade a 2x do pico;
- RTO/RPO exercitados;
- error budgets usados nas decisões de release.

## Sequenciamento de referência

| Fase | Horizonte inicial | Resultado |
|---|---|---|
| 1 | 0–3 meses | agente interno controlado em produção |
| 2 | 3–6 meses | RAG e memória com autorização e descarte |
| 3 | 6–9 meses | tools corporativas governadas |
| 4 | 9–12 meses | publicação baseada em risco e evidências |
| 5 | 12+ meses | escala, marketplace e controle financeiro |

Para a perspectiva organizacional e de adoção, consulte [Modelo de maturidade e roadmap](../book/07-adoption-roadmap.md).
