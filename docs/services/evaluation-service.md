# Evaluation Service

## Visão Geral

O Evaluation Service avalia a qualidade das respostas geradas por agentes: groundedness, relevância, alucinação, toxicidade e regressão de qualidade. É consultado pelo Agent Runtime a cada invocação e pela Governance Service durante a aprovação de agentes.

## Responsabilidades

- Avaliar groundedness e relevância das respostas
- Detectar alucinação e toxicidade
- Executar avaliações de regressão para novas versões de agentes
- Publicar resultado de avaliação para consumo por Governance e Audit
- Suportar avaliação síncrona (bloqueante, para aprovação) e assíncrona (pós-execução, para monitoramento contínuo)

## Fora de Escopo

- Execução do agente
- Decisão final de aprovação (cabe à Governance Service, que consome o resultado da avaliação)
- Cálculo de custo

## API Principal

```http
POST /evaluations
GET /evaluations/{id}
```

## Dependências

| Dependência | Uso |
|---|---|
| Agent Runtime | Origem das respostas avaliadas |
| Governance Service | Consome resultado para decisão de aprovação |
| Kafka | Publica e consome eventos de avaliação |

## Eventos Publicados

- `evaluation.started`
- `evaluation.completed`

## Requisitos Não Funcionais

| Requisito | Diretriz |
|---|---|
| Latência | Avaliação assíncrona não deve bloquear a resposta ao usuário |
| Consistência | Critérios de avaliação versionados e reprodutíveis |
| Auditoria | Todo resultado de avaliação é rastreável a uma invocação ou versão de agente |
| Escalabilidade | Suporta avaliação em lote para regressão |

## Decisões Relacionadas

- [ADR-007 — Avaliação híbrida e contínua de IA](../adrs/007-evaluation-strategy.md)
