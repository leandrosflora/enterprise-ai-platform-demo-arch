# Glossário

## ABAC

Attribute-Based Access Control. Autorização baseada em atributos do usuário, workload, recurso, contexto, tenant, finalidade e classificação.

## Agent Gateway

Fronteira de entrada para invocações de agentes. Aplica autenticação, rate limit, roteamento, validação e propagação de contexto.

## Agent Registry

Catálogo técnico de agentes, versões, owners, status, risco, modelos, tools e bases de conhecimento permitidas.

## Agent Runtime

Ambiente responsável por executar o agente, montar contexto, aplicar políticas, chamar modelos, conhecimento, memória e ferramentas.

## AI Catalog

Inventário corporativo de casos de uso, agentes, modelos, riscos, owners, decisões e status de ciclo de vida.

## AI Platform

Conjunto de capacidades, padrões, serviços e processos que permite criar e operar soluções de IA com autonomia controlada.

## Baseline

Referência usada para comparar uma versão: versão anterior, processo humano, modelo mais simples ou threshold aprovado.

## Capability

Habilidade organizacional ou técnica que descreve o que a plataforma precisa conseguir fazer, sem depender de uma tecnologia específica.

## Chunk

Trecho derivado de um documento para indexação e retrieval. Deve preservar provenance, classificação e autorização.

## Control Plane

Plano responsável por cadastro, configuração, governança, policies, avaliação, catálogos e promoção de versões.

## Correlation ID

Identificador propagado entre componentes para correlacionar uma execução ponta a ponta.

## Data Plane

Plano que executa invocações, retrieval, memória, modelos, tools e telemetria em tempo de execução.

## Dataset de avaliação

Conjunto versionado de entradas, contexto, respostas esperadas, rubricas e cenários negativos usado para medir comportamento.

## Deny by default

Princípio em que o acesso é negado quando nenhuma regra explícita permite a operação.

## Embedding

Representação vetorial de conteúdo usada em similaridade e retrieval. Modelo e versão precisam ser identificáveis.

## Error budget

Tolerância de falha derivada do SLO, usada para equilibrar confiabilidade e velocidade de mudança.

## Evaluation

Medição sistemática de qualidade, retrieval, groundedness, segurança, tools, desempenho, confiabilidade e custo.

## Evidence bundle

Pacote reproduzível de artefatos que sustenta uma decisão de publicação.

## Fine-tuning

Ajuste de parâmetros de um modelo usando um dataset para alterar comportamento, formato ou capacidade específica.

## Foundation Model

Modelo de propósito geral treinado em grande escala e usado como base para aplicações e agentes.

## Golden path

Caminho suportado e automatizado para construir, avaliar, aprovar, publicar e operar uma solução.

## Groundedness

Grau em que uma resposta é sustentada pelas evidências disponibilizadas ao modelo.

## Guardrail

Controle que limita entrada, saída ou comportamento. Guardrails probabilísticos não substituem autorização determinística.

## HITL

Human in the loop. A execução pausa até uma decisão humana.

## Idempotência

Propriedade que permite repetir uma operação sem produzir efeitos adicionais indevidos.

## Indirect prompt injection

Instrução maliciosa ou conflitante inserida em conteúdo recuperado, páginas, documentos ou resultados de ferramentas.

## Knowledge Base

Coleção governada de documentos e chunks disponíveis para retrieval sob políticas específicas.

## Long-term Memory

Memória persistida além da sessão atual. Exige finalidade, origem, confiança, TTL e consentimento quando aplicável.

## MCP

Model Context Protocol. Protocolo para exposição e descoberta padronizada de ferramentas e recursos para modelos e agentes.

## Memory poisoning

Inserção de conteúdo incorreto, malicioso ou não autorizado na memória para influenciar execuções futuras.

## Model Gateway

Camada que abstrai provedores e aplica roteamento, políticas, observabilidade, limites, fallback e controle de custo.

## Model routing

Seleção de modelo com base em capacidade, qualidade, região, custo, latência e disponibilidade.

## Multi-agent

Arquitetura em que múltiplos agentes especializados colaboram ou delegam tarefas entre si.

## NFR

Non-Functional Requirement. Requisito de segurança, confiabilidade, desempenho, privacidade, custo, suporte ou operação.

## OIDC

OpenID Connect. Protocolo de identidade construído sobre OAuth 2.0.

## Policy Decision Point

Componente que avalia políticas e produz uma decisão de autorização ou controle.

## Policy Enforcement Point

Componente que intercepta uma operação e aplica a decisão de política.

## Prompt

Conjunto de instruções, mensagens e contexto fornecido ao modelo. Deve ser versionado quando afeta o comportamento do produto.

## Provenance

Informações sobre origem, versão, transformações e cadeia de processamento de um dado ou artefato.

## RAG

Retrieval-Augmented Generation. Padrão que recupera evidências externas e as fornece ao modelo durante a geração.

## RBAC

Role-Based Access Control. Autorização baseada em papéis.

## Reranking

Reordenação dos resultados de retrieval usando um modelo ou algoritmo adicional.

## Retrieval

Processo de localizar evidências relevantes e autorizadas para uma consulta.

## Risk tier

Classe de risco que determina controles, evidências, revisões e gates aplicáveis.

## Session Memory

Contexto efêmero limitado à sessão e ao sujeito autorizado.

## Shadow evaluation

Execução de uma nova versão ou modelo em paralelo, sem usar sua resposta para afetar o usuário, para comparação segura.

## SLO

Service Level Objective. Objetivo mensurável de disponibilidade, latência, sucesso ou outra característica operacional.

## System of record

Sistema autoritativo para dados e estados transacionais. Memória de agente não deve assumir esse papel.

## Tenant

Unidade lógica de isolamento, como empresa, área, cliente ou ambiente.

## Tool

Capacidade externa invocada pelo agente por contrato estruturado. Pode consultar dados ou produzir efeitos.

## Vertical slice

Implementação mínima ponta a ponta usada para demonstrar contratos, fluxos e controles da arquitetura.

## Workload class

Categoria operacional usada para definir SLOs e limites diferentes, como interação simples, RAG, tool call ou processamento assíncrono.
