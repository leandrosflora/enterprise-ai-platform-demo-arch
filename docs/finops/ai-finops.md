# FinOps para IA

FinOps deve conectar consumo técnico, unidade de negócio, agente, sessão e resultado. Medir apenas a fatura do provedor não permite responsabilização nem otimização.

## Modelo de custos

### Custo por agente

```text
custo_agente = modelos + embeddings + retrieval + ferramentas + infraestrutura + observabilidade
```

Dimensões mínimas: `tenant_id`, `agent_id`, `agent_version`, `environment`, `model`, `provider`, `cost_center` e período.

### Custo por sessão

```text
custo_sessao = soma(tokens_entrada, tokens_saida, chamadas_modelo, retrievals, tools, retries e infraestrutura_alocada)
```

Relacionar custo com sucesso da jornada, contenção, conversão, tempo economizado ou satisfação.

## Budget enforcement

Aplicar limites em camadas:

- organização e centro de custo;
- produto ou domínio;
- agente e versão;
- tenant, usuário e sessão;
- requisição individual.

Ações progressivas: alertar, reduzir limite de tokens, trocar modelo, desabilitar ferramentas caras, migrar para assíncrono e bloquear com resposta controlada.

## Cache semântico

Usar quando perguntas semanticamente equivalentes gerarem respostas estáveis. A chave deve considerar tenant, agente, versão do prompt, modelo, políticas e versão do conhecimento. Não cachear respostas personalizadas, sensíveis ou dependentes de estado sem escopo adequado.

## Routing por modelo

O Model Gateway deve selecionar modelo por classificação de tarefa, risco, qualidade mínima, latência, disponibilidade e budget. Uma política comum:

1. modelo econômico para classificação e extração simples;
2. modelo intermediário para RAG e tool calling comum;
3. modelo avançado para casos complexos ou escalonados.

## Fallback entre modelos

Fallback deve preservar compatibilidade de tool calling, tamanho de contexto, política de dados e qualidade mínima. Registrar motivo, custo adicional e diferença de resultado. Não usar fallback para contornar restrições de segurança.

## Métricas recomendadas

| Métrica | Uso |
|---|---|
| custo por sessão concluída | eficiência de jornada |
| custo por resposta aceita | qualidade econômica |
| tokens por etapa | detecção de prompts inchados |
| taxa de cache | economia potencial |
| custo de retries/fallback | instabilidade e desperdício |
| custo por ferramenta | otimização de integrações |
| orçamento consumido/projetado | controle preventivo |

## Controles de implementação

Emitir eventos de uso padronizados, calcular preço por tabela versionada e reconciliar estimativas com a fatura real do provedor. Custos devem aparecer nos dashboards de produto, não apenas no painel de cloud.