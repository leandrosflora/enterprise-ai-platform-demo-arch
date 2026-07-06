# Governance Service

## Visão Geral

O Governance Service centraliza o ciclo de aprovação, publicação, controle de risco e conformidade dos agentes e soluções de IA da plataforma.

## Responsabilidades

- Gerenciar fluxo de aprovação de agentes
- Aplicar políticas corporativas de IA
- Registrar avaliações de risco
- Controlar publicação, suspensão e aposentadoria de agentes
- Integrar resultados de AI Evaluation ao processo decisório
- Manter trilha auditável de decisões

## Ciclo de Vida do Agente

```text
Draft
  ↓
Submitted for Review
  ↓
Risk Assessment
  ↓
Technical Review
  ↓
Compliance Review
  ↓
Approved / Rejected
  ↓
Published
  ↓
Retired
```

## APIs

### Submeter Agente para Aprovação

```http
POST /governance/agents/{agentId}/submit
```

### Aprovar Versão

```http
POST /governance/agents/{agentId}/versions/{version}/approve
```

### Rejeitar Versão

```http
POST /governance/agents/{agentId}/versions/{version}/reject
```

## Critérios de Aprovação

| Critério | Descrição |
|---|---|
| Segurança | Autenticação, autorização, segredos e exposição de dados |
| LGPD | Tratamento de dados pessoais e dados sensíveis |
| Risco de IA | Alucinação, viés, explicabilidade e impacto operacional |
| Observabilidade | Logs, métricas, traces e auditoria |
| Custos | Modelo, volume esperado e limite de consumo |
| Qualidade | Resultado mínimo nas avaliações definidas |

## Dependências

| Dependência | Uso |
|---|---|
| Agent Registry | Consultar metadados e versões |
| Evaluation Service | Consultar resultados de avaliação |
| Audit Service | Registrar decisões |
| PostgreSQL | Persistir workflows e pareceres |
| Kafka | Publicar eventos de governança |

## Eventos Publicados

- `governance.approved`
- `governance.rejected`
- `agent.published`
- `agent.retired`

## Requisitos Não Funcionais

| Requisito | Diretriz |
|---|---|
| Auditoria | Todas as decisões devem ser rastreáveis |
| Segregação | Papéis distintos para criador, aprovador e operador |
| Conformidade | Guardar evidências de aprovação |
| Segurança | Aplicar RBAC por domínio, área e criticidade |
| Escalabilidade | Suportar múltiplas áreas e esteiras de aprovação |

## Decisões Relacionadas

- [ADR-005 Evaluation Framework](../adr/ADR-005-evaluation-framework.md)
