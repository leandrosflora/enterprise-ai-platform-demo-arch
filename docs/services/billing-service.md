# Billing Service

## Visão Geral

O Billing Service é responsável pelo FinOps da plataforma: rastreamento de tokens, alocação de custo por agente/time/unidade de negócio e geração de chargeback/showback.

## Responsabilidades

- Consumir eventos de uso (invocação de agente, execução de ferramenta, geração de embedding)
- Calcular custo por modelo, agente, time e unidade de negócio
- Gerar relatórios de chargeback e showback
- Alertar sobre consumo acima de limites definidos

## Fora de Escopo

- Execução do agente ou da ferramenta
- Auditoria de conformidade (papel da Audit Service)
- Definição de limites de aprovação de risco (papel da Governance Service)

## Dependências

| Dependência | Uso |
|---|---|
| Kafka | Consome eventos de uso para cálculo de custo |
| PostgreSQL | Persiste custos e dados de chargeback |

## Eventos Consumidos

- `agent.invoked`
- `tool.executed`
- `embedding.generated`

## Requisitos Não Funcionais

| Requisito | Diretriz |
|---|---|
| Retenção | 24 meses para dados de uso e cobrança, base para chargeback/showback |
| Precisão | Custo calculado deve refletir consumo real de tokens e ferramentas por invocação |
| Escalabilidade | Processa alto volume de eventos de uso sem atraso relevante no fechamento de período |
| Auditoria | Cálculos de custo devem ser rastreáveis ao evento de origem |

## Decisões Relacionadas

- [docs/finops/token-costs.md](../finops/token-costs.md)
