# ADR-007 — Avaliação híbrida e contínua de IA

**Status:** Aceito

## Contexto

Agentes corporativos precisam ser avaliados antes e depois da publicação para reduzir alucinação, baixa relevância, falhas de retrieval, uso incorreto de tools, respostas inseguras e regressões de qualidade. Avaliação apenas manual não escala; avaliação apenas em produção expõe usuários e processos a risco evitável.

## Decisão

Adotar um **Evaluation Service** com avaliação híbrida:

- automática para escala e regressão;
- baseada em regras para requisitos determinísticos;
- model-based quando houver critérios subjetivos controlados;
- humana para casos críticos, amostras e calibração;
- offline antes da promoção e online durante a operação.

Resultados devem ser versionados, reproduzíveis e rastreáveis a agente, prompt, modelo, dataset, policy, knowledge snapshot e código avaliados.

## Dimensões mínimas

- qualidade da tarefa;
- retrieval e groundedness;
- citation correctness;
- segurança, toxicidade e leakage;
- seleção e argumentos de tools;
- latência e confiabilidade;
- custo por invocação e tarefa concluída;
- regressão contra baseline e versão anterior.

## Alternativas

| Alternativa | Vantagem | Limitação |
|---|---|---|
| Avaliação apenas manual | julgamento contextual | baixa escala, custo e variabilidade |
| Avaliação apenas em produção | dados reais de uso | risco de publicar regressões não detectadas |
| Apenas LLM-as-judge | cobertura rápida | viés, instabilidade e dependência do judge |
| Nota agregada única | comunicação simples | esconde falhas críticas em dimensões específicas |

## Consequências positivas

- gates de publicação baseados em evidência;
- comparação reproduzível entre versões;
- detecção de degradação durante a operação;
- combinação de escala automática com julgamento humano proporcional ao risco.

## Consequências negativas

- aumenta custo de execução e manutenção de datasets;
- métricas e judges podem divergir da percepção do negócio;
- datasets desatualizados geram falsa confiança;
- cenários críticos continuam exigindo revisão independente.

## Evidências mínimas

- dataset versionado e aprovado;
- baseline e thresholds por dimensão;
- versão do evaluator e do judge;
- relatório de regressão;
- resultados de red-team e testes negativos;
- amostra de revisão humana e concordância quando aplicável;
- decisão de promoção, exceção ou bloqueio.

## Critérios de revisão

Revisar quando métricas deixarem de correlacionar com resultados reais, quando houver drift do dataset ou do domínio, quando custos de avaliação se tornarem desproporcionais ou quando novos métodos oferecerem maior validade e reprodutibilidade.
