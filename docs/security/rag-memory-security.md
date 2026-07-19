# Segurança de RAG e Memória

## Objetivo

Definir os controles obrigatórios para ingestão, recuperação e uso de conhecimento, além da persistência de memória conversacional e de perfil. A fonte executável das regras é [`../../policies/rag-memory-security.yaml`](../../policies/rag-memory-security.yaml).

A decisão padrão é **deny by default**. Conteúdo recuperado é sempre tratado como dado não confiável, nunca como instrução.

## Princípios

1. **Autorização acompanha o dado.** ACL, tenant, classificação e finalidade são propagados do documento para cada chunk.
2. **Ingestão não implica publicação.** Todo documento entra em quarentena e só pode ser indexado após validações.
3. **Retrieval não vaza existência.** Resultados não autorizados são filtrados sem informar ao chamador que o documento existe.
4. **Memória não é log.** Somente fatos necessários, com finalidade, origem, confiança, TTL e consentimento quando aplicável.
5. **Modelo não cria verdade persistente.** Conteúdo inferido pelo modelo não pode virar memória de longo prazo ou perfil.
6. **Dados sensíveis não persistem por padrão.** Classificação `RESTRICTED` é bloqueada; exceções exigem política específica fora da baseline.

## Pipeline seguro de RAG

```text
Fonte
  ↓
Validação de tipo e tamanho
  ↓
Antivírus / detecção de payload
  ↓
Checksum e proveniência
  ↓
Classificação e ACL
  ↓
Detecção de indirect prompt injection
  ↓
Quarentena
  ↓ aprovação
Extração e chunking com ACL herdada
  ↓
Embedding e indexação
  ↓
Retrieval com tenant + ACL + clearance + finalidade
  ↓
Post-filter e sanitização
  ↓
Contexto delimitado como <untrusted_document>
```

### Metadados obrigatórios por documento e chunk

| Campo | Finalidade |
|---|---|
| `tenantId` | Impedir mistura entre organizações. |
| `documentId` e `chunkId` | Rastreabilidade e exclusão seletiva. |
| `classification` | Aplicar clearance e controles de observabilidade. |
| `allowedRoles` / `allowedSubjects` | Enforcement de ACL. |
| `allowedPurposes` | Evitar reutilização para finalidade incompatível. |
| `sourceSystem` e `sourceUri` | Proveniência. |
| `checksum` | Detectar alteração após aprovação. |
| `approvedSource` | Permitir apenas fontes registradas. |
| `retentionPolicy` e `expiresAt` | Expiração, exclusão e reindexação. |
| `securityScanVersion` | Reproduzir a decisão de quarentena. |

### Quarentena obrigatória

O documento permanece `QUARANTINED` quando ocorrer qualquer uma destas condições:

- fonte não aprovada;
- checksum divergente;
- tipo ou tamanho não permitido;
- assinatura de malware ou payload ativo;
- indicador de indirect prompt injection;
- ausência de classificação, ACL, finalidade ou política de retenção.

A liberação exige evidência de todos os controles e gera evento auditável. Reindexação deve invalidar chunks e embeddings anteriores.

### Retrieval

A consulta aplica os filtros antes e depois da busca vetorial:

1. derivar tenant, usuário, papéis e clearance da identidade autenticada;
2. restringir índices/aliases por tenant;
3. aplicar ACL e classificação no mecanismo de busca;
4. executar post-filter no Knowledge Service;
5. remover resultados não autorizados sem revelar contagem ou título ao chamador externo;
6. retornar `policyDecisionId`, checksum e proveniência para auditoria;
7. delimitar conteúdo recuperado como não confiável;
8. bloquear instruções encontradas em documentos antes da montagem do prompt.

A resposta do modelo só pode citar chunks que passaram pela mesma decisão de autorização usada no retrieval.

## Memória segura

### Tipos

| Tipo | Uso | TTL máximo | Consentimento | Fonte permitida |
|---|---|---:|---|---|
| `SESSION` | Contexto da conversa atual | 24 horas | Não, salvo dado pessoal específico | Usuário, sistema, ferramenta e inferência do modelo |
| `SHORT_TERM` | Continuidade operacional curta | 7 dias | Conforme finalidade | Usuário, sistema ou ferramenta verificada |
| `LONG_TERM` | Fato reutilizado entre sessões | 365 dias | Obrigatório | Usuário confirmado ou sistema verificado |
| `PROFILE` | Preferências explícitas | 365 dias | Obrigatório | Usuário confirmado ou sistema verificado |

### Campos obrigatórios por item

- chave e valor minimizados;
- classificação;
- finalidade;
- origem;
- confiança;
- sujeito proprietário em hash;
- tenant;
- data de criação e expiração;
- versão;
- referência de consentimento quando exigida.

### Proteção contra memory poisoning

Antes da escrita, o Memory Service:

- rejeita comandos e instruções disfarçados de fatos;
- bloqueia indicadores como “ignore instruções anteriores”, tentativa de revelar system prompt ou desativar política;
- impede persistência de conteúdo `MODEL_INFERRED` fora de `SESSION`;
- exige origem `USER_CONFIRMED` ou `SYSTEM_VERIFIED` para `LONG_TERM` e `PROFILE`;
- rejeita `RESTRICTED`;
- registra somente metadados seguros nos eventos, nunca o valor completo.

Atualizações conflitantes devem preservar histórico de versão e exigir reconciliação quando fontes confiáveis discordarem.

### Isolamento e descarte

A chave lógica mínima é:

```text
tenantId + subjectHash + sessionId + memoryType
```

Leitura e exclusão usam o sujeito derivado da identidade. Um usuário não escolhe livremente outro `subjectId`. Consentimento revogado bloqueia novas leituras e dispara exclusão ou anonimização conforme a política.

## Observabilidade segura

Registrar:

- decisão de autorização e motivo de bloqueio;
- status de quarentena;
- IDs de documento/chunk;
- checksum e versão do scanner;
- tipo de memória, quantidade de itens, TTL e presença de consentimento;
- exclusão e reindexação.

Não registrar:

- prompt completo;
- texto integral do documento;
- valor integral da memória;
- dado pessoal em claro;
- tokens ou segredos.

## Gates de publicação

| Gate | Evidência |
|---|---|
| Ingestão | Teste de quarentena para malware, checksum e prompt injection. |
| Retrieval | Teste de ACL por documento/chunk, tenant e clearance. |
| Prompt | Evidência de delimitador e tratamento do contexto como não confiável. |
| Memória | Testes de consentimento, TTL, origem e poisoning. |
| Privacidade | Exclusão por sujeito e política de retenção. |
| Auditoria | Eventos sem payload sensível e com `policyDecisionId`. |

## Implementação demonstrativa

A vertical slice implementa:

- endpoint de ingestão com checksum, fonte aprovada e quarentena;
- busca com tenant, papéis, clearance, finalidade e post-filter;
- conteúdo delimitado como `<untrusted_document>`;
- memória com consentimento, TTL, origem, confiança e isolamento por sujeito;
- bloqueio de `RESTRICTED`, `MODEL_INFERRED` persistente e indicadores de poisoning;
- testes automatizados que exercitam esses controles.

A demo usa armazenamento em memória e headers simulados. Em produção, identidade, DLP, antivírus, policy engine e persistência devem ser serviços reais.
