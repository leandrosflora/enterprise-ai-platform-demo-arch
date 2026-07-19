# Threat Model - Enterprise AI Platform

## Objetivo

Identificar ameaças relevantes usando STRIDE e controles específicos para agentes, RAG, memória e ferramentas.

## Escopo

- AI Portal, Agent Gateway e Agent Runtime;
- Model Gateway e provedores;
- Knowledge Service, índices vetoriais e pipeline de ingestão;
- Memory Service;
- MCP Registry e MCP Servers;
- Governance, Evaluation e Audit Services.

## STRIDE

| Categoria | Ameaça | Exemplo | Mitigação |
|---|---|---|---|
| Spoofing | Identidade falsificada | Token reutilizado acessando agente ou memória | OIDC, validação JWT, workload identity, mTLS |
| Tampering | Alteração indevida | Documento ou evento alterado após aprovação | Checksum, assinatura, versão imutável, schema validation |
| Repudiation | Negação de ação | Usuário nega tool call ou escrita de memória | Audit trail, correlation ID, sujeito em hash, timestamp |
| Information Disclosure | Vazamento | Chunk ou memória de outro tenant | ACL por chunk, clearance, subject isolation, redaction |
| Denial of Service | Exaustão | Explosão de retrieval, embeddings ou tool calls | Rate limit, quotas, timeout, circuit breaker |
| Elevation of Privilege | Escalada | Agente acessa KB ou ferramenta não autorizada | Deny by default, PDP/PEP, scopes e allowlists |

## Ameaças Específicas de IA

| Ameaça | Cenário | Controles obrigatórios |
|---|---|---|
| Direct Prompt Injection | Usuário tenta substituir instruções | Separação de instruções, filtros, policy enforcement |
| Indirect Prompt Injection | Documento recuperado contém comandos ao modelo | Quarentena, scanner, delimitadores, sanitização e avaliação adversarial |
| Data Exfiltration | Resposta inclui dado não autorizado | Tenant filter, ACL por chunk, output filtering e DLP |
| Poisoned Knowledge | Fonte ou documento altera respostas | Fonte aprovada, checksum, proveniência, quarantine-first |
| ACL Bypass | Busca vetorial retorna chunk fora do escopo | Filtro no índice + post-filter no serviço + testes negativos |
| Metadata Poisoning | Atacante reduz classificação ou amplia ACL | Metadados assinados/versionados e aprovação para mudança |
| Memory Poisoning | Instrução ou fato falso vira memória persistente | Validação de origem, confiança, consentimento e indicadores |
| Cross-Subject Memory Access | Usuário lê perfil de outro | Subject hash derivado da identidade e chave composta |
| Consent/Retention Failure | Memória permanece após revogação | TTL index, bloqueio imediato, delete/anonymous workflow |
| Tool Misuse | Ferramenta recebe argumento indevido | JSON Schema, allowlist, idempotência e human approval |
| Hallucination | Resposta incorreta apresentada como fato | Citações, groundedness, confidence e fallback |
| Excessive Agency | Agente atua além do permitido | Limites de autonomia, risk tiering e human-in-the-loop |

## Fronteiras de Confiança

```text
Usuário → Gateway → Runtime
                    ├─ Model Gateway → Provider externo
                    ├─ Knowledge Service → documentos não confiáveis
                    ├─ Memory Service → contexto persistente
                    └─ MCP → sistemas com efeito colateral
```

Documentos, respostas de ferramentas, conteúdo do usuário e saídas do modelo são entradas não confiáveis. Somente políticas, identidades e configurações publicadas pelo control plane são tratadas como instruções confiáveis.

## Controles Obrigatórios

- identidade centralizada e escopos mínimos;
- tenant e sujeito derivados do token;
- quarentena antes de indexação;
- ACL por documento e chunk;
- proveniência e checksum;
- conteúdo RAG delimitado como não confiável;
- consentimento, finalidade, TTL e origem para memória;
- bloqueio de memória `RESTRICTED`;
- detecção de poisoning;
- auditoria sem payload sensível;
- avaliação adversarial contínua;
- exclusão e reindexação verificáveis.

Detalhamento: [Segurança de RAG e Memória](rag-memory-security.md).

## Testes de Segurança Mínimos

1. documento com prompt injection permanece em quarentena;
2. papel ou clearance insuficiente recebe zero resultados;
3. tenant diferente não obtém indicação da existência do documento;
4. chunk sem ACL compatível não chega ao prompt;
5. memória de perfil sem consentimento é negada;
6. `MODEL_INFERRED` não persiste em perfil ou longo prazo;
7. indicador de poisoning é rejeitado;
8. outro sujeito não lê nem exclui a memória;
9. revogação e TTL removem o dado;
10. eventos não contêm texto ou valor sensível.

## Riscos Residuais

| Risco | Tratamento |
|---|---|
| Indicador novo de prompt injection | Atualização de scanner e red-team contínuo |
| Falso negativo de classificação | DLP, revisão humana e minimização |
| Inconsistência entre índice e metadados | Reconciliation job e fail closed |
| Exclusão em backup | Política de retenção e crypto-shredding |
| Mudança de comportamento do modelo | Regression testing e versionamento |
