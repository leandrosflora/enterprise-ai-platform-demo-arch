# 8. Checklists de produção

## Como usar

Os checklists são instrumentos de verificação, não substitutos para análise. Itens não aplicáveis devem ser marcados com justificativa. Itens obrigatórios não atendidos precisam de bloqueio ou exceção formal com owner e validade.

## 1. Business readiness

- [ ] problema e usuário estão definidos;
- [ ] outcome e métricas de sucesso foram acordados;
- [ ] existe owner de negócio;
- [ ] existe owner técnico;
- [ ] a alternativa sem IA foi considerada;
- [ ] impacto de respostas incorretas foi analisado;
- [ ] processo de feedback foi definido;
- [ ] estratégia de comunicação e adoção existe;
- [ ] critérios de encerramento ou desativação estão definidos.

## 2. Architecture readiness

- [ ] contexto e containers estão documentados;
- [ ] fronteiras entre control plane e data plane são explícitas;
- [ ] sistemas de registro permanecem autoritativos;
- [ ] contratos de API, eventos e tools estão versionados;
- [ ] decisão agent versus workflow está registrada;
- [ ] sincronismo e processamento assíncrono estão justificados;
- [ ] timeouts, retries e circuit breakers estão definidos;
- [ ] idempotência existe para efeitos colaterais;
- [ ] fallback e degradação controlada foram desenhados;
- [ ] ADRs cobrem decisões relevantes;
- [ ] dependências e failure modes foram identificados.

## 3. Identity and authorization

- [ ] usuários são autenticados por IdP aprovado;
- [ ] workloads usam identidade própria;
- [ ] tokens são validados por issuer, audience, validade e assinatura;
- [ ] scopes mínimos estão definidos;
- [ ] autorização é `deny by default`;
- [ ] tenant e subject não são escolhidos livremente pelo cliente;
- [ ] acesso a agentes, knowledge bases, memory e tools é independente;
- [ ] service-to-service utiliza mecanismo aprovado;
- [ ] elevação de privilégio foi testada;
- [ ] revogação de acesso foi exercitada.

## 4. Data, RAG and memory

- [ ] fontes possuem owner e classificação;
- [ ] finalidade de uso está registrada;
- [ ] pipeline de ingestão usa quarentena;
- [ ] checksum e proveniência são preservados;
- [ ] malware, conteúdo ativo e indirect prompt injection são tratados;
- [ ] ACL é aplicada por documento e chunk;
- [ ] filtros obrigatórios não dependem do texto da query;
- [ ] conteúdo recuperado é tratado como não confiável;
- [ ] citações apontam para fontes acessíveis ao usuário;
- [ ] expiração e exclusão removem conteúdo do retrieval;
- [ ] embeddings e chunking são versionados;
- [ ] tipos de memória são explícitos;
- [ ] TTL máximo é aplicado;
- [ ] consentimento existe quando exigido;
- [ ] memória não substitui sistema de registro;
- [ ] memory poisoning e acesso cross-subject foram testados.

Consulte [Segurança de RAG e memória](../security/rag-memory-security.md).

## 5. Model and prompt readiness

- [ ] modelo está no catálogo aprovado;
- [ ] região e processamento atendem às políticas;
- [ ] prompt principal está versionado;
- [ ] parâmetros possuem limites;
- [ ] input e output token limits estão definidos;
- [ ] custo máximo por execução é controlado;
- [ ] fallback de modelo foi testado quando aplicável;
- [ ] redaction e filtros estão configurados;
- [ ] mudança de modelo dispara reavaliação;
- [ ] dependência de capacidade proprietária foi registrada.

## 6. Tool and MCP readiness

- [ ] tool possui owner e versão;
- [ ] schema de entrada e saída é restritivo;
- [ ] scopes são mínimos;
- [ ] operações de leitura e escrita são distinguíveis;
- [ ] timeout e limites existem;
- [ ] idempotência foi validada;
- [ ] retries não duplicam efeitos;
- [ ] compensação ou rollback foi definido;
- [ ] HITL existe para ações críticas;
- [ ] argumentos são validados fora do modelo;
- [ ] tool pode ser bloqueada sem derrubar o runtime;
- [ ] auditoria registra operação sem expor segredos.

## 7. Security and privacy

- [ ] threat model está atualizado;
- [ ] classificação de risco foi confirmada;
- [ ] secrets não estão no código ou prompt;
- [ ] dados sensíveis são minimizados;
- [ ] logs e traces possuem redaction;
- [ ] retenção e descarte foram definidos;
- [ ] base legal ou justificativa de finalidade foi analisada;
- [ ] incidentes de vazamento possuem runbook;
- [ ] dependências e imagens foram verificadas;
- [ ] egress está controlado;
- [ ] criptografia em trânsito e repouso está aplicada;
- [ ] exceções possuem compensating controls e expiração.

## 8. Evaluation readiness

- [ ] dataset representa casos reais e edge cases;
- [ ] dataset e versão estão identificados;
- [ ] baseline está definida;
- [ ] qualidade da tarefa é medida separadamente;
- [ ] retrieval e groundedness são avaliados separadamente;
- [ ] prompt injection e leakage fazem parte dos testes;
- [ ] tool selection e argumentos são avaliados;
- [ ] performance e custo possuem thresholds;
- [ ] regressões bloqueiam release conforme risco;
- [ ] resultados são reproduzíveis;
- [ ] amostras de produção alimentam revisão controlada;
- [ ] avaliação humana possui rubrica e critérios consistentes.

## 9. Observability and SRE

- [ ] correlation ID é propagado;
- [ ] agent, version, model, tenant e session são correlacionáveis;
- [ ] métricas de sucesso, latência, tokens e custo existem;
- [ ] policy denials são observáveis;
- [ ] retrieval, memory e tools possuem spans;
- [ ] logs não armazenam prompts completos por padrão;
- [ ] SLO está definido por workload;
- [ ] alertas possuem owner e ação esperada;
- [ ] dashboards foram revisados com a equipe de suporte;
- [ ] capacidade foi testada;
- [ ] dependências críticas possuem circuit breaker ou fallback;
- [ ] runbooks estão acessíveis;
- [ ] on-call e escalonamento estão definidos;
- [ ] rollback foi exercitado.

## 10. FinOps readiness

- [ ] custos possuem tags ou dimensões por agente e tenant;
- [ ] tokens e custo são medidos por modelo;
- [ ] budget mensal e diário estão definidos;
- [ ] quotas preventivas existem;
- [ ] alertas de anomalia estão configurados;
- [ ] custo por tarefa bem-sucedida é acompanhado;
- [ ] reindexação e embeddings entram no modelo de custo;
- [ ] observabilidade e infraestrutura compartilhada estão consideradas;
- [ ] showback ou chargeback foi definido quando necessário;
- [ ] estratégia para reduzir custo sem degradar qualidade foi analisada.

## 11. Governance and release

- [ ] versão submetida está congelada;
- [ ] evidências correspondem ao artefato publicado;
- [ ] decisores possuem autoridade e independência necessárias;
- [ ] condições de aprovação são verificáveis;
- [ ] aprovação possui validade;
- [ ] pipeline verifica decisão antes da publicação;
- [ ] canary ou rollout progressivo está definido;
- [ ] feature flags e kill switch existem quando aplicável;
- [ ] comunicação de release foi preparada;
- [ ] revisão pós-release está agendada;
- [ ] gatilhos de reavaliação estão definidos.

## 12. Retirement readiness

- [ ] consumidores e usuários foram identificados;
- [ ] plano de migração ou substituição existe;
- [ ] novas invocações podem ser bloqueadas;
- [ ] credenciais e scopes serão revogados;
- [ ] knowledge e memory terão destinação adequada;
- [ ] evidências de auditoria serão retidas conforme política;
- [ ] budgets, dashboards e alertas serão encerrados;
- [ ] documentação e catálogo serão atualizados;
- [ ] owner aprovou a retirada.

## Release decision record

A decisão final pode usar o seguinte resumo:

```yaml
agentId: policy-assistant
agentVersion: 1.2.0
riskClassification: MEDIUM
releaseDecision: APPROVED
approvedAt: 2026-07-19T18:00:00Z
validUntil: 2027-01-19T18:00:00Z
conditions:
  - internal-users-only
  - long-term-memory-disabled
  - daily-budget-usd-100
artifacts:
  evaluation: evaluation-report.json
  threatModel: threat-model.md
  runbook: runbook.md
rollback:
  method: feature-flag
  targetVersion: 1.1.0
owners:
  business: corporate-governance
  technical: ai-product-squad
```

## Definition of done para uma versão publicada

Uma versão está pronta quando:

- entrega valor mensurável;
- possui risco conhecido e controles aplicados;
- pode ser observada e suportada;
- tem custo controlado;
- pode ser revertida, suspensa e retirada;
- possui evidências que permitem explicar por que foi publicada.

## Próximos materiais

- [Glossário](glossary.md)
- [Runbooks](../runbooks/)
- [AI Risk Framework](../governance/ai-risk-framework.md)
- [Requisitos não funcionais](../architecture/non-functional-requirements.md)
