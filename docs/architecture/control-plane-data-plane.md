# Control Plane e Data Plane

## Decisão

A plataforma separa **gestão e governança** de **execução online**.

- O **control plane** administra metadados, políticas, versões, aprovações e evidências.
- O **data plane** executa invocações, recuperação, memória, modelos e ferramentas sob políticas publicadas.

Essa separação reduz o blast radius, permite escalar cada plano de forma independente e impede que indisponibilidades administrativas interrompam workloads já publicados.

## Control plane

| Capacidade | Responsabilidade |
|---|---|
| Agent Registry | Metadados, versões imutáveis e estado do ciclo de vida. |
| Governance Service | Workflow, segregação de funções e evidências. |
| Evaluation Service | Datasets, baselines, thresholds e relatórios. |
| MCP Registry | Catálogo e versões aprovadas de ferramentas. |
| Policy Administration Point | Autoria, revisão e publicação de políticas. |
| Model Catalog | Allowlist de modelos, regiões, capacidades e restrições. |
| FinOps Administration | Budgets, quotas e regras de atribuição de custo. |

## Data plane

| Capacidade | Responsabilidade |
|---|---|
| Agent Gateway | Autenticação, autorização inicial, rate limit e roteamento. |
| Agent Runtime | Orquestração da execução do agente. |
| Policy Enforcement Points | Aplicação local de decisões em Gateway, Runtime, Knowledge e MCP. |
| Policy Decision Point | Decisão de política com baixa latência e cache controlado. |
| Knowledge Service | Retrieval com filtros de autorização por documento e chunk. |
| Memory Service | Memória de sessão e perfil com TTL, consentimento e descarte. |
| Model Gateway | Roteamento, guardrails, quotas, fallback e telemetria de modelos. |
| MCP Execution | Execução de ferramentas com allowlist, idempotência e auditoria. |

## Fluxo de publicação

1. O developer cria uma versão imutável do agente.
2. Contratos, datasets, budgets e políticas são validados.
3. Governance Service registra as decisões e evidências.
4. As políticas aprovadas são publicadas no Policy Decision Point.
5. Agent Registry muda a versão para `PUBLISHED`.
6. O data plane passa a aceitar invocações dessa versão.

## Fluxo de invocação

1. Agent Gateway valida identidade, tenant, escopo e limite de consumo.
2. Runtime carrega somente uma versão `PUBLISHED`.
3. Policy Decision Point avalia agente, usuário, ferramenta, dado e risco.
4. Knowledge, Memory, Model Gateway e MCP aplicam enforcement local.
5. Eventos e traces registram decisões, custo e resultado.

## Disponibilidade

O data plane não depende de chamadas síncronas ao control plane durante cada invocação. Configurações e políticas publicadas são distribuídas e armazenadas em cache com:

- versão e checksum;
- TTL explícito;
- invalidação por evento;
- fallback para a última política válida;
- comportamento `deny by default` quando não existe política aplicável.

## Isolamento

- namespaces e service accounts separados por plano;
- bancos de metadados não são acessados diretamente pelo data plane;
- políticas de rede restringem comunicação lateral;
- identidades de workload usam privilégio mínimo;
- operações administrativas exigem MFA e segregação de funções.
