# 7. Modelo de maturidade e roadmap de adoção

## Princípio

A maturidade de uma AI Platform não é definida pelo número de serviços implantados. Ela é demonstrada pela capacidade de entregar casos de uso com qualidade, controle, operação e custo previsíveis.

## Modelo de maturidade

### Nível 0 — Experimentos isolados

**Características**

- notebooks, scripts e SaaS sem padrão comum;
- credenciais e configurações locais;
- pouca rastreabilidade;
- avaliação manual;
- custos não atribuídos;
- conhecimento e prompts copiados entre projetos.

**Objetivo para avançar**

Identificar padrões repetidos, owners e riscos materiais.

### Nível 1 — Padrões mínimos

**Características**

- templates de projeto;
- identidade e secrets adequados;
- logging básico;
- inventário inicial de casos;
- provedores e modelos aprovados;
- checklist de publicação.

**Evidência de maturidade**

Primeiros casos de baixo risco chegam à produção sem controles ad hoc.

### Nível 2 — Golden path executável

**Características**

- Agent Registry e ciclo de vida;
- Model Gateway;
- contratos e eventos versionados;
- CI/CD com avaliações e policies;
- observabilidade ponta a ponta;
- runbooks e rollback;
- primeiro serviço de knowledge ou tools.

**Evidência de maturidade**

Squads conseguem publicar versões controladas sem depender de implementação manual do time central.

### Nível 3 — Governança baseada em risco

**Características**

- AI Catalog completo;
- risk tiers e gates proporcionais;
- RAG e memória com lifecycle;
- datasets e baselines versionados;
- approval evidence;
- revisão periódica;
- incident management especializado.

**Evidência de maturidade**

A organização demonstra por que uma versão foi publicada e consegue suspender ou retirar rapidamente.

### Nível 4 — Escala federada

**Características**

- múltiplas unidades e tenants;
- marketplace de capacidades;
- MCP e tools governadas;
- chargeback ou showback;
- capacity management;
- community of practice;
- platform product management maduro.

**Evidência de maturidade**

A adoção cresce sem crescimento proporcional de exceções, incidentes ou esforço central.

### Nível 5 — Otimização contínua

**Características**

- routing orientado por qualidade, custo e disponibilidade;
- avaliações online e shadow traffic;
- error budgets influenciam releases;
- otimização por outcome;
- automação de revisão e evidências;
- resiliência multi-região quando justificada.

**Evidência de maturidade**

Qualidade, risco, custo e velocidade são geridos como dimensões do mesmo produto plataforma.

## Matriz de maturidade

| Dimensão | N0 | N1 | N2 | N3 | N4 | N5 |
|---|---|---|---|---|---|---|
| Delivery | artesanal | templates | golden path | gates por risco | self-service federado | otimização contínua |
| Governança | inexistente | checklist | workflow | evidências e revisão | policies em escala | automação adaptativa |
| Segurança | projeto a projeto | baseline | enforcement comum | threat model e testes | isolamento endurecido | continuous assurance |
| Evaluation | manual | amostras | datasets | baselines e regressão | online + offline | otimização por outcome |
| Operação | best effort | logs | SLOs e runbooks | incidentes e reviews | capacity e DR | error-budget driven |
| FinOps | fatura agregada | tags | custo por agente | budgets e quotas | showback/chargeback | routing econômico |
| Organização | iniciativas | champions | platform team | modelo federado | CoE e comunidade | product portfolio otimizado |

## Roadmap de referência em 12 meses

O calendário deve ser adaptado ao contexto. A sequência abaixo prioriza aprendizado operacional antes da expansão.

### Trimestre 1 — Foundation e primeiro golden path

**Entregas**

- platform charter e owners;
- capability map e backlog;
- Agent Registry mínimo;
- Agent Gateway e Runtime;
- Model Gateway;
- identidade, policies e telemetria;
- CI/CD com contratos;
- primeiro caso interno de baixo ou médio risco.

**Resultados**

- primeira versão publicada por pipeline;
- trace ponta a ponta;
- custo por invocação conhecido;
- rollback exercitado;
- feedback da primeira squad.

### Trimestre 2 — Knowledge, memória e evaluation

**Entregas**

- ingestão com quarentena;
- ACL por documento e chunk;
- citations e groundedness;
- memória com TTL e consentimento;
- datasets e baseline;
- risk workflow proporcional;
- dashboards de qualidade e custo.

**Resultados**

- agente documental operando com acesso controlado;
- regressões bloqueadas no pipeline;
- exclusão e expiração testadas;
- revisão de 30 ou 60 dias executada.

### Trimestre 3 — Tools e integração corporativa

**Entregas**

- MCP Registry;
- onboarding de tools;
- idempotência, outbox e compensação;
- HITL para ações críticas;
- tool metrics e audit;
- segundo e terceiro casos de uso.

**Resultados**

- ação corporativa governada;
- tools bloqueáveis por política;
- falhas e retries sem duplicar efeitos;
- reutilização comprovada entre squads.

### Trimestre 4 — Escala, FinOps e operating model

**Entregas**

- quotas e budgets por tenant e agente;
- showback;
- marketplace interno;
- maturity assessment;
- community of practice;
- capacity tests;
- DR e incident simulation;
- roadmap do próximo ano baseado em adoção.

**Resultados**

- custos atribuídos;
- lead time reduzido;
- operação com SLOs;
- crescimento sem aumento proporcional do time central.

## Backlog orientado a outcomes

Evite um backlog composto apenas por componentes. Estruture épicos como:

- reduzir o onboarding de uma squad de quatro semanas para cinco dias;
- garantir que nenhuma fonte não autorizada seja retornada;
- detectar regressão de groundedness antes do deploy;
- atribuir 95% dos custos a agentes e áreas;
- suspender uma versão em menos de cinco minutos;
- executar uma ação transacional sem duplicidade após retry.

Os componentes técnicos são entregas necessárias para atingir esses outcomes.

## KPIs da plataforma

### Adoção e experiência

- squads onboarded;
- agentes publicados e ativos;
- tempo para primeiro deploy;
- percentual no golden path;
- satisfação do desenvolvedor;
- taxa de reuso de capabilities.

### Qualidade e risco

- regressões bloqueadas;
- policy denials por categoria;
- incidentes de segurança ou privacidade;
- respostas grounded;
- taxa de fallback e abstention;
- exceções abertas e vencidas.

### Operação

- disponibilidade e p95 por workload;
- MTTR;
- saturação e backlog;
- taxa de sucesso de invocação;
- incidentes por agente e dependência;
- cumprimento de revisões periódicas.

### FinOps e valor

- custo por agente, área e modelo;
- custo por tarefa concluída;
- budget variance;
- economia de tempo ou redução de esforço;
- receita, conversão ou risco evitado quando aplicável;
- custo de plataforma por consumidor ativo.

## Guardrails de investimento

Antes de expandir uma capability, valide:

- ao menos dois consumidores ou um requisito corporativo forte;
- owner de produto e operação;
- SLO e custo esperados;
- contrato e estratégia de versionamento;
- plano de depreciação;
- métrica de sucesso;
- alternativa gerenciada ou comprável analisada.

## Antipadrões de roadmap

- implantar todos os componentes antes do primeiro caso real;
- medir progresso por quantidade de ferramentas;
- adotar multi-agent, memória longa e fine-tuning simultaneamente;
- construir marketplace sem consumidores;
- expandir para casos HIGH antes de operar um caso simples;
- ignorar suporte, incidentes e custos durante a POC;
- tratar governança como fase posterior.

## Próximo capítulo

Os [checklists de produção](08-production-checklists.md) convertem maturidade e lifecycle em verificações objetivas para cada release.
