# Foundation Models Integration

## Objetivo

Padronizar o consumo de modelos fundacionais por agentes e serviços da plataforma.

## Provedores Suportados

- Amazon Bedrock
- Azure OpenAI
- OpenAI
- Anthropic
- Google Gemini

## Padrões de Integração

- Model Adapter no Agent Runtime
- Abstração por provider e model id
- Fallback entre modelos compatíveis
- Controle de tokens
- Timeout e retry controlado

## Critérios de Seleção

| Critério | Descrição |
|---|---|
| Qualidade | Aderência ao caso de uso |
| Latência | Tempo de resposta esperado |
| Custo | Custo por input/output tokens |
| Compliance | Requisitos regulatórios e de dados |
| Capacidade | Context window, tool calling e multimodalidade |

## Requisitos

- Registro de uso por agente
- Observabilidade por chamada de modelo
- Mascaramento de dados sensíveis quando aplicável
- Política de retenção de prompts e respostas
