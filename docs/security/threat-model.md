# Threat Model - Enterprise AI Platform

## Objetivo

Identificar ameaças relevantes para a Enterprise AI Platform usando STRIDE e definir controles mínimos para mitigação.

## Escopo

Componentes avaliados:

- AI Portal
- Agent Gateway
- Agent Runtime
- MCP Registry
- MCP Servers
- Knowledge Service
- Memory Service
- Evaluation Service
- Governance Service
- Audit Service
- Foundation Model Providers

---

## STRIDE

| Categoria | Ameaça | Exemplo | Mitigação |
|---|---|---|---|
| Spoofing | Falsificação de identidade | Token inválido ou reutilizado acessando agente | OIDC, validação de JWT, mTLS para serviço-serviço |
| Tampering | Alteração indevida | Manipulação de prompt, contrato MCP ou payload de evento | Assinatura de contratos, versionamento, validação de schema |
| Repudiation | Negação de ação | Usuário ou serviço nega execução de tool call | Audit trail imutável, correlationId, userId, timestamp |
| Information Disclosure | Vazamento de dados | Prompt ou resposta contendo dados sensíveis | Mascaramento, classificação, controle de acesso, DLP |
| Denial of Service | Indisponibilidade | Explosão de chamadas de modelo ou tool calls | Rate limiting, quotas, circuit breaker, timeout |
| Elevation of Privilege | Elevação de privilégio | Agente executa ferramenta fora do escopo autorizado | RBAC, ABAC, policy enforcement, escopos por tool |

---

## Ameaças Específicas de IA

| Ameaça | Descrição | Mitigação |
|---|---|---|
| Prompt Injection | Usuário tenta alterar instruções do agente | System prompts protegidos, filtros, validação de intenção |
| Data Exfiltration | Agente expõe dados de bases não autorizadas | Autorização por knowledge base, redaction, logging |
| Tool Misuse | Ferramenta é chamada com argumentos indevidos | JSON Schema, políticas, allowlist, revisão humana |
| Model Hallucination | Resposta incorreta apresentada como fato | RAG com citações, groundedness evaluation, disclaimers |
| Poisoned Knowledge | Base de conhecimento contém conteúdo malicioso | Curadoria, classificação, aprovação de fonte, reindexação controlada |
| Excessive Agency | Agente toma decisões além do permitido | Limites de autonomia, human-in-the-loop, risk tiering |

---

## Controles Obrigatórios

- Autenticação centralizada via Identity Provider
- Autorização por agente, ferramenta e base de conhecimento
- Auditoria de invocações, tool calls e decisões de governança
- CorrelationId obrigatório em todas as chamadas
- Mascaramento de dados sensíveis em logs e traces
- Avaliação contínua de segurança, qualidade e groundedness
- Retenção e descarte conforme LGPD

---

## Riscos Residuais

| Risco | Tratamento |
|---|---|
| Alucinação residual | Monitoramento, avaliação e revisão humana em casos críticos |
| Dependência de provedor externo | Estratégia multi-provider e fallback |
| Custo inesperado | Quotas, alertas e dashboards FinOps |
| Mudança de comportamento do modelo | Regression testing e versionamento de avaliações |
