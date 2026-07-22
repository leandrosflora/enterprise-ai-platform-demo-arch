# Crosswalk de Governança, Risco e Compliance

## Objetivo

Transformar referências normativas e de mercado em uma matriz operacional de controles, evidências, owners e gates da Enterprise AI Platform.

Este crosswalk é uma ferramenta de rastreabilidade. Ele **não substitui interpretação jurídica, auditoria de certificação, análise regulatória ou avaliação específica do contexto da organização**.

## Como usar

1. selecione os controles aplicáveis ao caso de uso e ao nível de risco;
2. associe cada controle a um owner e a uma evidência verificável;
3. automatize o enforcement quando a condição for objetiva;
4. registre exceções, risco residual, prazo e controle compensatório;
5. revise o mapeamento quando legislação, norma, arquitetura ou finalidade mudar.

## Referências cobertas

| Referência | Papel no crosswalk |
|---|---|
| NIST AI RMF | funções Govern, Map, Measure e Manage para estruturar o ciclo de risco |
| ISO/IEC 42001 | sistema de gestão, responsabilidades, objetivos, controles e melhoria contínua |
| ISO/IEC 27001 | segurança da informação, gestão de acesso, fornecedores, incidentes e continuidade |
| EU AI Act | classificação por risco e obrigações proporcionais quando aplicável |
| LGPD | finalidade, necessidade, transparência, segurança, responsabilização e direitos do titular |
| OWASP para aplicações com LLM | ameaças e testes técnicos de aplicações com modelos generativos |

## Matriz de rastreabilidade

| ID | Controle da plataforma | NIST AI RMF | ISO/IEC 42001 | EU AI Act | LGPD | Evidência mínima | Owner primário | Gate | Enforcement |
|---|---|---|---|---|---|---|---|---|---|
| CTRL-001 | finalidade, sponsor e owner definidos | Govern / Map | contexto, liderança e accountability | finalidade e papel dos atores | finalidade e responsabilização | Outcome Card, Agent Card, owner registrado | Business Owner | Intake | automático |
| CTRL-002 | classificação de risco e impacto | Map / Govern | avaliação de riscos de IA | classificação e obrigações proporcionais | relatório de impacto quando aplicável | risk assessment versionado | AI Architect / Risk | Risk | híbrido |
| CTRL-003 | inventário e catálogo de ativos de IA | Govern | inventário, documentação e controle operacional | registro e documentação aplicável | registro das operações e accountability | AI Catalog com versões e owners | Platform Team | Intake / Release | automático |
| CTRL-004 | classificação, finalidade e lineage dos dados | Map / Manage | governança de dados para IA | data governance e qualidade | finalidade, necessidade e qualidade | data contract, lineage, classificação e retenção | Data Owner | Design | híbrido |
| CTRL-005 | versionamento imutável de modelo, prompt, dataset, policy e tool | Govern / Measure | controle de mudanças e informação documentada | documentação técnica e rastreabilidade | responsabilização e segurança | hashes, manifests e release bundle | Platform Team | Build / Release | automático |
| CTRL-006 | allowlist de modelos, fontes, regiões e tools | Govern / Manage | controles operacionais e fornecedores | requisitos proporcionais ao risco | segurança e transferência internacional | policy versionada e decisão de autorização | Security / Platform | Design / Runtime | automático |
| CTRL-007 | threat model e testes negativos | Map / Measure | gestão de riscos e controles | robustez, segurança e cibersegurança | segurança e prevenção | threat model, red-team e resultados de ataque | Security | Assurance | híbrido |
| CTRL-008 | avaliação de qualidade, segurança e regressão | Measure | monitoramento, medição e avaliação | precisão, robustez e qualidade conforme aplicação | qualidade e não discriminação quando aplicável | dataset, baseline, thresholds e evaluation report | Model Risk / Evaluation | Evaluation | automático + humano |
| CTRL-009 | human-in-the-loop e limites de autonomia | Govern / Manage | papéis, competência e controle operacional | supervisão humana quando aplicável | revisão de decisões automatizadas | matriz de autonomia, aprovadores e logs | Business Owner / Risk | Design / Runtime | híbrido |
| CTRL-010 | autorização por identidade, tenant, recurso e finalidade | Govern / Manage | controles de acesso e operação | controle e rastreabilidade | segurança, necessidade e acesso | matriz de autorização e testes de acesso negado | Security | Assurance / Runtime | automático |
| CTRL-011 | proveniência, citações e transparência da resposta | Map / Measure | comunicação e informação documentada | transparência e informação ao usuário quando aplicável | transparência e qualidade | citações, checksum, source version e policy decision | Product / Data Owner | Evaluation / Runtime | automático |
| CTRL-012 | logging, tracing e audit trail correlacionado | Measure / Manage | monitoramento, auditoria interna e registros | logging e documentação conforme risco | responsabilização e segurança | traces, eventos, retenção e acesso auditado | SRE / Security | Observability | automático |
| CTRL-013 | monitoramento contínuo e detecção de drift | Measure / Manage | monitoramento, análise e melhoria | pós-mercado quando aplicável | qualidade, segurança e atualização | dashboards, drift report e gatilhos de revisão | Model Risk / Operations | Operate | automático + humano |
| CTRL-014 | gestão de incidentes, suspensão e rollback | Manage | não conformidade, ação corretiva e continuidade | incidentes e ações corretivas quando aplicável | incidente de segurança e mitigação | incidente, decisão, rollback e postmortem | Operations / Security | Operate | híbrido |
| CTRL-015 | budgets, quotas e unit economics | Govern / Manage | objetivos, recursos e controle operacional | proporcionalidade e sustentabilidade operacional | necessidade e minimização indireta de processamento | budget, quota, custo por tarefa e bloqueios | FinOps / Product | FinOps | automático |
| CTRL-016 | gestão de fornecedores e modelos externos | Govern / Map / Manage | controle de fornecedores e serviços externos | obrigações entre provider e deployer | operadores, transferência e segurança | due diligence, contrato, região e exit plan | Procurement / Legal / Security | Design | humano + policy |
| CTRL-017 | reavaliação após mudança material | Manage | gestão de mudanças e melhoria contínua | nova avaliação quando houver mudança relevante | nova finalidade ou alteração relevante | change record e novo evidence bundle | AI Architect / Risk | Change | automático + humano |
| CTRL-018 | retenção, exclusão e retirada verificável | Manage | lifecycle, controle de informação e melhoria | retirada e documentação quando aplicável | retenção, eliminação e direitos do titular | retirement record, revogação e prova de exclusão | Data Owner / Operations | Retire | híbrido |

## Mapeamento por função do NIST AI RMF

### Govern

Controles principais: CTRL-001, CTRL-002, CTRL-003, CTRL-005, CTRL-006, CTRL-009, CTRL-010, CTRL-015, CTRL-016.

Evidências esperadas:

- operating model e RACI;
- políticas aprovadas;
- catálogo de casos, agentes, modelos e tools;
- classificação de risco;
- registro de exceções e risco residual;
- indicadores de governança.

### Map

Controles principais: CTRL-001, CTRL-002, CTRL-004, CTRL-007, CTRL-011, CTRL-016.

Evidências esperadas:

- finalidade e contexto de uso;
- população e stakeholders impactados;
- fontes de dados e lineage;
- dependências e fornecedores;
- impactos esperados e cenários de uso indevido.

### Measure

Controles principais: CTRL-007, CTRL-008, CTRL-011, CTRL-012, CTRL-013.

Evidências esperadas:

- datasets e baselines;
- testes funcionais, adversariais e de segurança;
- métricas por dimensão;
- observabilidade e amostragem;
- análise de drift e regressão.

### Manage

Controles principais: CTRL-006, CTRL-009, CTRL-010, CTRL-013, CTRL-014, CTRL-015, CTRL-017, CTRL-018.

Evidências esperadas:

- decisões de aceite, mitigação ou bloqueio;
- limites de autonomia;
- rollout controlado;
- incident response e rollback;
- reavaliação e retirada.

## Aplicabilidade por nível de risco

| Controle | LOW | MEDIUM | HIGH | CRITICAL |
|---|---:|---:|---:|---:|
| Owner, finalidade e catálogo | obrigatório | obrigatório | obrigatório | obrigatório |
| Data lineage e classificação | conforme dados | obrigatório | obrigatório | obrigatório + revisão independente |
| Threat model | simplificado | obrigatório | detalhado | detalhado + revisão formal |
| Avaliação | amostra | dataset | dataset + baseline | baseline + revisão independente |
| Human oversight | opcional | por ação | obrigatório para ações críticas | obrigatório para ações permitidas |
| Logging e auditoria | básico | completo | completo | completo + retenção estendida |
| Monitoramento de drift | periódico | periódico | contínuo por métricas | contínuo + gatilhos bloqueantes |
| Rollback e suspensão | recomendado | obrigatório | obrigatório e testado | obrigatório, testado e independente |
| Reavaliação | anual | semestral | trimestral ou por evento | contínua ou por evento material |

## Evidence bundle de compliance

```text
outcome-card.yaml
agent-card.yaml
risk-assessment.yaml
data-contracts/
lineage.json
architecture/
adrs/
model-manifest.json
prompt-manifest.json
dataset-manifest.json
policy-bundle/
threat-model.md
security-tests.json
evaluation-report.json
human-oversight-plan.md
observability-evidence.json
supplier-assessment.md
approval-decision.json
release-manifest.json
runbook.md
retirement-record.json
```

Nem todos os artefatos precisam usar esses formatos, mas a informação deve ser identificável, versionada e rastreável.

## Exceções

Uma exceção deve registrar:

- controle não atendido;
- justificativa e impacto;
- risco residual;
- controle compensatório;
- owner e aprovador independente;
- prazo de expiração;
- condição de revogação;
- evidência e ticket rastreável.

Exceção sem prazo ou owner é inválida. Controles legais ou regulatórios não podem ser dispensados apenas por decisão técnica.

## Cadência de manutenção

Revisar o crosswalk:

- ao menos trimestralmente para referências e políticas internas;
- após mudança regulatória relevante;
- após incidente material;
- quando uma nova classe de agente, modelo ou autonomia for introduzida;
- quando auditoria identificar lacuna de evidência ou enforcement.
