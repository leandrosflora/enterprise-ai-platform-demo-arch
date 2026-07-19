# Requisitos Não Funcionais

## Objetivo

Definir metas mensuráveis para design, testes, operação e governança da Enterprise AI Platform. Os SLOs são classificados por **tipo de workload**, não por nível de risco.

## Classes de workload

| Classe | Exemplo | Modo recomendado | SLO de latência P95 |
|---|---|---|---:|
| `INTERACTIVE_SIMPLE` | Chat sem RAG ou ferramenta | Síncrono | <= 5 s |
| `INTERACTIVE_RAG` | Retrieval + geração | Síncrono ou streaming | <= 8 s |
| `INTERACTIVE_TOOL` | Consulta a ferramenta sem efeito colateral | Síncrono | <= 15 s |
| `TRANSACTIONAL_AGENT` | Ferramenta de escrita ou aprovação humana | Assíncrono | Aceite <= 2 s; conclusão conforme processo |
| `BATCH_INGESTION` | Ingestão e indexação documental | Assíncrono | Definido por volume |
| `BATCH_EVALUATION` | Avaliação de datasets | Assíncrono | P95 <= 15 min para dataset padrão |

O risco define controles, aprovações e evidências. Ele não altera artificialmente a classe de latência.

## Disponibilidade e continuidade

| Capacidade | Meta de referência |
|---|---:|
| Agent Gateway | 99,95% mensal |
| Agent Runtime | 99,9% mensal |
| Policy Decision Point | 99,99% mensal |
| Control plane | 99,5% mensal |
| Publicação de eventos | 99,9% de sucesso |
| Registro de auditoria crítica | 99,99% de sucesso |
| RTO data plane | <= 2 h |
| RPO metadados transacionais | <= 15 min |

- serviços críticos são multi-AZ;
- o data plane usa a última política válida quando o control plane estiver indisponível;
- ausência de política aplicável resulta em `deny by default`;
- backups e restauração são testados pelo menos semestralmente.

## Performance

| Requisito | Meta |
|---|---:|
| Agent Gateway sem chamada externa | P95 <= 300 ms |
| Policy decision | P95 <= 100 ms |
| Knowledge retrieval | P95 <= 2 s |
| Model Gateway overhead | P95 <= 250 ms, excluindo o provedor |
| Tool execution de leitura | P95 <= 4 s, salvo contrato específico |
| Aceite de operação assíncrona | P95 <= 2 s |

Cada tool contract define seu próprio timeout. O padrão é 30 s e só pode ser ampliado com justificativa.

## Escalabilidade

- componentes stateless escalam horizontalmente;
- filas desacoplam ingestão, avaliação, auditoria e billing;
- chaves de partição preservam ordenação por agregado;
- autoscaling considera concorrência, latência, backlog e consumo de tokens;
- limites por tenant impedem noisy neighbor;
- testes de capacidade validam o dobro do pico previsto.

## Segurança

- OIDC/OAuth2 para identidades humanas e workload identity para serviços;
- RBAC combinado com políticas contextuais por tenant, recurso, dado e risco;
- mTLS ou mecanismo equivalente entre serviços críticos;
- secrets em secret manager, nunca em repositório ou variáveis de pipeline em claro;
- criptografia em trânsito e em repouso;
- egress allowlist para provedores externos;
- segregação entre control plane e data plane;
- SAST, dependency scanning, secret scanning e image scanning na pipeline.

## Dados e LGPD

- classificação obrigatória em documentos, memória, eventos e traces;
- minimização de dados por padrão;
- ACL por documento e chunk em retrieval;
- TTL explícito para memória;
- consulta, exclusão e anonimização suportadas;
- prompts e respostas sensíveis não são armazenados integralmente por padrão;
- linhagem e checksum para documentos ingeridos;
- quarantine e validação antes da indexação.

## Resiliência

| Mecanismo | Diretriz |
|---|---|
| Timeout | Menor que o deadline da chamada superior. |
| Retry | Apenas para erros transitórios e operações idempotentes. |
| Circuit breaker | Obrigatório para provedores e ferramentas externas. |
| Bulkhead | Isolamento por provedor, tenant e ferramenta crítica. |
| Fallback | Modelo, provedor ou fluxo alternativo aprovado. |
| Idempotência | Obrigatória para comandos e tool calls com efeito colateral. |
| Outbox | Obrigatória para eventos derivados de transações críticas. |
| Graceful degradation | Resposta parcial ou assíncrona quando seguro. |

## Observabilidade

- OpenTelemetry para traces, métricas e logs;
- W3C Trace Context em HTTP e eventos;
- `correlationId` para correlação funcional;
- métricas de latência, erro, tokens, custo, retrieval, qualidade e policy denials;
- alertas vinculados a runbooks;
- cardinalidade controlada; IDs de usuário não aparecem como labels de métricas.

## FinOps

- custo atribuído por tenant, unidade, agente, versão, modelo e ambiente;
- budget e quota por agente;
- alertas em 70%, 90% e 100%;
- bloqueio ou degradação controlada quando o limite for excedido;
- comparação de custo e qualidade antes de alterar o modelo padrão;
- custos de embeddings, armazenamento e ferramentas entram no custo total.

## Auditabilidade

- decisões de política registram policy ID e versão;
- alterações administrativas registram ator, antes/depois e justificativa;
- eventos críticos usam retenção aprovada;
- acesso aos próprios logs de auditoria também é auditado;
- evidências de governança são imutáveis após a publicação.
