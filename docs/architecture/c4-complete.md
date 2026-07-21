# Diagramas C4 e fluxos principais

Os diagramas usam Mermaid para permanecerem versionáveis e renderizáveis no MkDocs.

## Nível 1 — Contexto

```mermaid
flowchart LR
  User[Cliente / Colaborador] --> Channel[Canais digitais]
  Channel --> Platform[Enterprise AI Platform]
  Platform --> Corp[APIs e sistemas corporativos]
  Platform --> Models[Provedores de modelos]
  Platform --> Data[Fontes de conhecimento]
  Platform --> Human[Atendimento humano]
  Gov[Segurança, Risco, LGPD e Arquitetura] --> Platform
```

## Nível 2 — Containers

```mermaid
flowchart TB
  CH[Channel BFF] --> AG[Agent Gateway]
  AG --> AR[Agent Runtime]
  AR --> MG[Model Gateway]
  AR --> KS[Knowledge Service]
  AR --> MS[Memory Service]
  AR --> MCP[MCP Tool Services]
  AR --> EV[Evaluation Service]
  AR --> EB[Event Backbone]
  CP[Control Plane / AI Catalog] --> AG
  CP --> AR
  CP --> MG
  OT[OpenTelemetry Collector] --> OBS[Logs, Metrics e Traces]
  AG --> OT
  AR --> OT
  KS --> OT
  EV --> OT
```

## Nível 3 — Agent Runtime

```mermaid
flowchart LR
  API[Invocation API] --> LOAD[Agent Definition Loader]
  LOAD --> ORCH[Graph / Workflow Orchestrator]
  ORCH --> POLICY[Policy Hooks]
  ORCH --> PROMPT[Prompt Builder]
  ORCH --> MODEL[Model Client]
  ORCH --> TOOLS[Tool Executor]
  ORCH --> MEMORY[Memory Adapter]
  ORCH --> STATE[Checkpoint / State Store]
  ORCH --> TELEMETRY[Telemetry]
```

## Nível 3 — Knowledge Service

```mermaid
flowchart LR
  ING[Ingestion API] --> PARSE[Parser / OCR Adapter]
  PARSE --> CLASS[Classification and DLP]
  CLASS --> CHUNK[Chunking]
  CHUNK --> EMB[Embedding]
  EMB --> INDEX[Vector / Hybrid Index]
  RET[Retrieval API] --> ACL[Metadata and ACL Filter]
  ACL --> SEARCH[Hybrid Search]
  SEARCH --> RERANK[Reranking]
  RERANK --> CITE[Citation Builder]
```

## Nível 3 — Evaluation Service

```mermaid
flowchart LR
  DS[Evaluation Datasets] --> RUN[Evaluation Runner]
  REG[Agent / Prompt Registry] --> RUN
  RUN --> JUDGE[Rule, Model and Human Judges]
  JUDGE --> METRICS[Quality, Safety, Cost and Latency]
  METRICS --> GATE[Release Gate]
  METRICS --> DASH[Dashboards]
```

## Fluxo de publicação de agentes

```mermaid
sequenceDiagram
  participant Squad
  participant Catalog as AI Catalog
  participant CI as CI/CD
  participant Eval as Evaluation Service
  participant Gov as Governance Gate
  participant Runtime as Agent Runtime
  Squad->>Catalog: registra agente, versão, owner e risco
  Squad->>CI: envia configuração, prompts e testes
  CI->>Eval: executa avaliações offline e segurança
  Eval-->>CI: métricas, evidências e violações
  CI->>Gov: solicita aprovação quando aplicável
  Gov-->>CI: decisão e condições
  CI->>Runtime: publica versão imutável
  Runtime-->>Catalog: registra deployment e status
  Runtime->>Eval: envia telemetria para avaliação contínua
```

## Princípios

- definições de agentes são versionadas e imutáveis após publicação;
- promoção entre ambientes depende de evidências, não apenas de aprovação manual;
- rollback deve selecionar uma versão conhecida, sem editar produção;
- tracing conecta canal, agente, modelo, retrieval e ferramentas.