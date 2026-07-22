# Knowledge Service

## Visão Geral

O Knowledge Service ingere, classifica, coloca em quarentena, indexa e recupera conhecimento corporativo para fluxos RAG. Segurança é aplicada por documento e por chunk; o serviço nunca confia no conteúdo recuperado como instrução.

Padrão obrigatório: [Segurança de RAG e Memória](../security/rag-memory-security.md).

## Responsabilidades

- validar tipo, tamanho, checksum e origem;
- executar antivírus e detecção de payload ativo;
- detectar indirect prompt injection;
- manter documentos em quarentena até aprovação;
- extrair texto e metadados;
- propagar tenant, classificação, ACL, finalidade e retenção para chunks;
- gerar embeddings e versionar o modelo utilizado;
- indexar conteúdo em aliases/índices isolados por tenant;
- aplicar autorização antes e depois da busca;
- retornar citações com proveniência e decisão de política;
- excluir, reindexar e invalidar embeddings antigos.

## Pipeline de Ingestão

```text
Source
  ↓
Content type / size validation
  ↓
Malware and active-content scan
  ↓
Checksum and provenance validation
  ↓
Classification, ACL, purpose and retention
  ↓
Indirect prompt injection scan
  ↓
QUARANTINED
  ↓ approval
Extraction
  ↓
Chunking with inherited security metadata
  ↓
Embedding
  ↓
Indexing
```

### Estados

| Estado | Significado |
|---|---|
| `QUEUED` | Solicitação aceita. |
| `QUARANTINED` | Aguardando aprovação ou bloqueada por controle. |
| `INGESTING` | Extração e chunking em andamento. |
| `INDEXED` | Disponível para retrieval autorizado. |
| `FAILED` | Falha técnica ou política não recuperável. |

Um documento `QUARANTINED` ou expirado nunca participa da busca.

## Contrato de segurança do documento

```yaml
documentId: policy-001
classification: INTERNAL
accessPolicy:
  allowedRoles: [employee]
  allowedSubjects: []
  deniedRoles: []
  allowedPurposes: [ASSISTANCE]
provenance:
  sourceSystem: policy-repository
  sourceUri: s3://policies/policy-001.pdf
  checksum: sha256:...
  approvedSource: true
retentionPolicy:
  retentionDays: 365
  deletionMode: DELETE
```

Todos os chunks herdam a política. Redução de classificação ou ampliação de ACL exige nova aprovação e reindexação.

## Retrieval seguro

```text
Authenticated identity
  ↓ tenant, roles, subject, clearance
Query
  ↓ tenant pre-filter
Vector / hybrid search with ACL
  ↓
Knowledge Service post-filter
  ↓
Prompt-injection sanitization
  ↓
<untrusted_document> context
```

### Regras

- tenant e sujeito são derivados da identidade, não do payload;
- ACL é aplicada no documento e no chunk;
- clearance deve ser igual ou superior à classificação;
- finalidade da consulta deve estar autorizada;
- resultados negados são removidos sem revelar sua existência;
- a citação retorna `policyDecisionId`, checksum e origem;
- somente chunks autorizados podem ser enviados ao modelo;
- conteúdo recuperado é delimitado e não altera system/developer instructions.

## APIs

```http
POST /v1/knowledge-bases/{knowledgeBaseId}/documents
POST /v1/knowledge-bases/{knowledgeBaseId}:search
```

## Eventos Publicados

- `knowledge.ingested`
- `knowledge.quarantined`
- `document.indexed`
- `document.deleted`
- `embedding.generated`

Eventos não carregam texto integral. Devem conter IDs, classificação, checksum, status e motivos de quarentena.

## Exclusão e Reindexação

A exclusão remove:

1. documento original;
2. chunks;
3. embeddings;
4. caches;
5. referências em datasets derivados quando aplicável.

Reindexação cria nova versão imutável e invalida a anterior. O índice precisa suportar remoção por `documentId` e `tenantId`.

## Dependências

| Dependência | Uso |
|---|---|
| Object Storage | Originais em quarentena e aprovados |
| Malware/DLP Scanner | Análise de conteúdo |
| Policy Decision Point | ACL, finalidade e classificação |
| OpenSearch | Busca vetorial e híbrida |
| PostgreSQL | Metadados, proveniência e retenção |
| Foundation Models | Embeddings aprovados |
| Kafka | Eventos auditáveis |

## Requisitos Não Funcionais

| Requisito | Diretriz |
|---|---|
| Segurança | Deny by default, ACL por chunk e quarantine-first |
| Privacidade | Minimização, retenção e exclusão verificável |
| Rastreabilidade | Origem, checksum, versão e decisão de política |
| Qualidade | Avaliar retrieval separadamente da geração |
| Resiliência | Reprocessamento idempotente e DLQ |
| Escalabilidade | Ingestão assíncrona separada de consulta |

## Decisões Relacionadas

- [ADR-005 — Estratégia de busca vetorial e híbrida](../adrs/005-vector-search-strategy.md)
- [ADR-007 — Avaliação híbrida e contínua de IA](../adrs/007-evaluation-strategy.md)
