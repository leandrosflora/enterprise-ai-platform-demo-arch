# 6. Decision Guides

## Como usar este capítulo

Os guias abaixo não substituem ADRs. Eles ajudam a identificar a opção inicial mais adequada e os fatores que precisam ser registrados na decisão final.

## 1. Agente ou workflow determinístico?

| Use agente quando | Use workflow quando |
|---|---|
| entrada e linguagem são variáveis | sequência e regras são conhecidas |
| seleção de ferramentas depende de contexto | passos precisam ser reproduzíveis |
| existe necessidade de interpretação | erro precisa ser praticamente nulo |
| caminhos não podem ser enumerados facilmente | auditoria exige transições explícitas |
| resultado pode ser avaliado por rubrica | resultado é validado por regra objetiva |

### Recomendação

Use o menor nível de autonomia que resolva o problema. Um agente pode interpretar a intenção e delegar a execução para um workflow determinístico.

### Sinais de alerta

- agente usado apenas para encadear APIs conhecidas;
- ausência de limite claro de autonomia;
- ferramenta transacional sem idempotência;
- decisão crítica baseada apenas em texto gerado.

## 2. RAG ou fine-tuning?

| Critério | RAG | Fine-tuning |
|---|---|---|
| conhecimento muda com frequência | forte | fraco |
| necessidade de citações | forte | fraco |
| controle por documento | forte | difícil |
| adaptação de estilo ou formato | moderado | forte |
| conhecimento muito especializado e estável | possível | forte em alguns casos |
| remoção imediata de informação | forte | difícil |
| custo de preparação | ingestão e retrieval | dataset e treinamento |

### Recomendação

Comece com RAG para conhecimento corporativo mutável. Use fine-tuning para comportamento, formato, classificação ou linguagem especializada quando houver dataset e ganho mensurável.

### Combinação

Um modelo ajustado pode continuar usando RAG. Fine-tuning não elimina a necessidade de autorização, citações e lifecycle do conhecimento.

## 3. Memória ou estado transacional?

| Memória de IA | Estado transacional |
|---|---|
| preferência, contexto ou resumo | saldo, status, contrato, pedido ou decisão oficial |
| pode expirar ou ser recalculada | exige consistência e sistema de registro |
| confiança e origem precisam ser registradas | regras de integridade são obrigatórias |
| pode ser probabilística | deve ser determinístico |

### Recomendação

Nunca use memória do agente como sistema de registro. O agente deve consultar o sistema autoritativo para fatos transacionais.

## 4. MCP ou API tradicional?

| MCP é útil quando | API direta é melhor quando |
|---|---|
| múltiplos agentes descobrem tools padronizadas | existe um único consumidor estável |
| descrição e schema precisam ser expostos ao runtime | integração possui contrato já consolidado |
| a plataforma controla catálogo e autorização | baixa latência e caminho mínimo são prioritários |
| tools precisam ser habilitadas por política | descoberta dinâmica não traz valor |

### Recomendação

Use MCP como camada de exposição governada para agentes, sem transformar o MCP Server em novo sistema de negócio. A lógica e as regras permanecem nos serviços responsáveis.

## 5. Single-agent ou multi-agent?

| Single-agent | Multi-agent |
|---|---|
| menor complexidade | especialização explícita |
| avaliação mais simples | domínios e tools muito distintos |
| menos hops e custo | separação de contexto necessária |
| tracing direto | colaboração traz ganho comprovado |

### Recomendação

Comece com um agente e tools bem definidas. Introduza múltiplos agentes apenas quando a decomposição melhorar qualidade, segurança ou ownership de forma mensurável.

### Custos ocultos de multi-agent

- mais tokens e latência;
- falhas de handoff;
- dificuldade de atribuir responsabilidade;
- avaliação combinatória;
- propagação excessiva de contexto;
- observabilidade mais complexa.

## 6. Síncrono ou assíncrono?

| Síncrono | Assíncrono |
|---|---|
| interação humana imediata | tarefas longas ou em lote |
| resposta dentro do SLO do canal | dependências com latência variável |
| efeito simples e controlado | múltiplas etapas e retries |
| cancelamento ligado à sessão | processamento independente da conexão |

### Recomendação

Use assíncrono para ingestão, avaliações extensas, geração em lote e workflows longos. Retorne `202 Accepted`, um identificador e um endpoint ou evento de status.

## 7. Modelo único ou Model Gateway?

| Integração direta | Model Gateway |
|---|---|
| experimento isolado | múltiplos produtos ou provedores |
| baixo risco e curta duração | políticas de região, custo e modelos aprovados |
| nenhuma necessidade de fallback | roteamento e observabilidade comuns |
| simplicidade local é mais importante | portabilidade e governança são necessárias |

### Recomendação

Uma plataforma corporativa deve convergir para Model Gateway, mas não precisa bloquear protótipos de curta duração. A transição deve ocorrer antes da produção ou do uso de dados relevantes.

## 8. Vector database dedicada ou banco existente?

| Banco existente com busca vetorial | Vector database dedicada |
|---|---|
| volume e throughput moderados | escala ou padrões de busca especializados |
| consistência com metadados é importante | indexação distribuída e baixa latência em grande escala |
| equipe já opera a tecnologia | recursos avançados justificam nova plataforma |
| menor complexidade operacional | isolamento e tuning independentes são necessários |

### Recomendação

Evite adicionar uma tecnologia apenas porque ela é popular. Faça benchmark com corpus, filtros, atualização, disponibilidade e custo reais.

Consulte [ADR-002](../adr/ADR-002-vector-database-selection.md).

## 9. Cachear ou não cachear?

Cache pode reduzir custo e latência, mas precisa incorporar:

- identidade ou grupo autorizado;
- tenant;
- versão do agente;
- versão das fontes;
- classificação;
- finalidade;
- modelo e configuração;
- prazo de validade.

Não reutilize uma resposta entre usuários quando a autorização ou o contexto puderem alterar o resultado.

## 10. Build ou buy?

| Pergunta | Favorece build | Favorece buy |
|---|---|---|
| capacidade diferencia o negócio? | sim | não |
| requisitos de integração são específicos? | sim | não |
| controle de dados é crítico? | sim | depende do fornecedor |
| time possui capacidade de operar? | sim | não |
| time-to-market é prioridade absoluta? | não | sim |
| commodity madura existe no mercado? | não | sim |
| lock-in é aceitável? | não | sim |

### Componentes frequentemente compráveis

- observabilidade gerenciada;
- model APIs;
- scanners e DLP;
- vector search gerenciada;
- gateways ou catálogos, quando atendem às políticas.

### Componentes frequentemente estratégicos

- operating model;
- contratos corporativos;
- políticas e risk gates;
- integração com identidade e sistemas internos;
- datasets e avaliações do domínio;
- experiência do desenvolvedor;
- telemetria e atribuição de custos.

## 11. Provedor único ou multi-provider?

Multi-provider deve resolver um requisito concreto:

- disponibilidade;
- residência de dados;
- capacidade específica;
- negociação de custo;
- redução de concentração;
- necessidade regulatória.

Não implemente portabilidade abstrata completa sem consumidores. Padronize contratos e telemetria, mas aceite diferenças de capacidade entre modelos.

## 12. Guardrail no prompt ou policy enforcement externo?

Prompts são úteis para orientar comportamento, mas não devem ser a única barreira para:

- autorização;
- acesso a dados;
- seleção de tools;
- limites financeiros;
- ações críticas;
- retenção e descarte;
- regiões e modelos permitidos.

Esses controles devem ser aplicados por componentes determinísticos antes ou depois da geração.

## 13. Human in the loop ou human on the loop?

- **Human in the loop:** a execução pausa e exige aprovação.
- **Human on the loop:** a execução ocorre, mas é supervisionada e pode ser interrompida.

Use HITL quando o efeito for irreversível, regulado, financeiro ou de alto impacto. Use supervisão quando o volume impedir aprovação individual e existirem limites, detecção e rollback adequados.

## Template de ADR

Para cada decisão relevante, registre:

```text
Title
Status
Context
Decision drivers
Options considered
Decision
Consequences
Security and privacy impact
Operational impact
Cost impact
Validation plan
Revisit triggers
```

## Próximo capítulo

O [modelo de maturidade e roadmap](07-adoption-roadmap.md) organiza essas escolhas em uma sequência de adoção sustentável.
