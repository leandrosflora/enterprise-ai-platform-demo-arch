# ADR-005 — Estratégia de busca vetorial e híbrida

**Status:** Aceito

## Contexto

A plataforma precisa suportar busca semântica e híbrida para cenários de RAG corporativo, preservando filtros por metadados, isolamento por tenant, autorização por documento e operação em escala.

## Decisão

Adotar **OpenSearch como implementação inicial de referência** para busca vetorial e híbrida, acessado exclusivamente por meio do Knowledge Service.

A arquitetura deve manter uma abstração de índice e retrieval para permitir outros mecanismos quando requisitos de domínio, custo, escala ou residência de dados justificarem a troca.

## Requisitos obrigatórios

- busca vetorial, textual e híbrida;
- filtros server-side por tenant, classificação, ACL, finalidade e retenção;
- versionamento do modelo de embedding e do índice;
- aliases ou mecanismo equivalente para promoção e rollback;
- exclusão verificável por `documentId` e `tenantId`;
- telemetria de latência, recall, custo e resultados filtrados;
- reindexação idempotente e sem indisponibilidade evitável.

## Alternativas

| Alternativa | Vantagem | Limitação |
|---|---|---|
| OpenSearch | busca híbrida, filtros e maturidade operacional | exige tuning e pode ter custo relevante |
| pgvector | simplicidade e proximidade com dados relacionais | menor especialização para busca híbrida em grande escala |
| MongoDB Vector Search | integração com documentos e memória | acopla retrieval ao datastore operacional |
| Vector database especializado | recursos vetoriais avançados | dependência adicional, custo e governança própria |

## Consequências positivas

- reduz a quantidade inicial de componentes especializados;
- permite busca textual e vetorial no mesmo mecanismo;
- aproveita filtros, aliases e práticas operacionais maduras;
- mantém a decisão reversível por meio do Knowledge Service.

## Consequências negativas

- OpenSearch pode não ser a melhor opção para todos os workloads;
- tuning de índices, shards, refresh e embeddings exige capacidade especializada;
- abstração excessiva pode esconder recursos úteis do mecanismo;
- migração exige reindexação e validação de qualidade.

## Evidências mínimas

- benchmark com dataset representativo;
- métricas de recall, precision, MRR ou nDCG conforme o caso;
- teste de isolamento e acesso negado;
- plano de versionamento e rollback do índice;
- custo estimado e observado por volume;
- procedimento de exclusão e reindexação.

## Critérios de revisão

Revisar quando qualidade, escala, custo, requisitos de filtros ou residência de dados deixarem de ser atendidos, ou quando outro mecanismo demonstrar ganho mensurável sem reduzir governança e portabilidade.
