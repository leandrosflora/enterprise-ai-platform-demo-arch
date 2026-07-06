# Audit Service

## Visão Geral

O Audit Service mantém a trilha de auditoria imutável da plataforma: uso de agentes, execução de ferramentas e decisões de governança. Consome eventos de praticamente todos os demais serviços e os torna disponíveis para conformidade e investigação.

## Responsabilidades

- Consumir eventos de todos os domínios (agentes, conhecimento, memória, governança, avaliação)
- Persistir trilha de auditoria imutável e pesquisável
- Publicar evento de confirmação de auditoria
- Disponibilizar trilha para consulta por times de conformidade e segurança
- Encaminhar registros de auditoria para o Observability Stack

## Fora de Escopo

- Decisão de aprovação ou rejeição de agentes
- Cálculo de custo (papel da Billing Service)
- Execução ou avaliação de agentes

## Dependências

| Dependência | Uso |
|---|---|
| Kafka | Consome eventos de todos os domínios da plataforma |
| Observability Stack | Publica logs e trilhas de auditoria |

## Eventos Consumidos

- `agent.created`, `agent.updated`, `agent.published`, `agent.retired`
- `agent.invoked`, `tool.executed`
- `knowledge.ingested`, `embedding.generated`, `document.indexed`
- `memory.updated`
- `evaluation.started`, `evaluation.completed`
- `governance.approved`, `governance.rejected`

## Eventos Publicados

- `audit.created`

## Requisitos Não Funcionais

| Requisito | Diretriz |
|---|---|
| Imutabilidade | Registros de auditoria não podem ser alterados ou apagados |
| Retenção | 5 anos, conforme política regulatória (ver [docs/contracts/events.md](../contracts/events.md)) |
| Disponibilidade | Consumo de eventos não pode perder mensagens (DLQ por domínio) |
| Conformidade | Suporta investigação e relatórios para LGPD e auditorias regulatórias |
