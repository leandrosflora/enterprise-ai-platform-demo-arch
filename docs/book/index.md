# Enterprise AI Platform Book

Este livro é uma **referência para orientar o desenho, a governança, a implementação e a operação de uma plataforma corporativa de IA**. Ele conecta estratégia, arquitetura, segurança, delivery e operação por meio de modelos, decisões, contratos e controles adaptáveis ao contexto de cada organização.

A proposta não é entregar uma plataforma pronta, uma distribuição de software ou uma implementação tecnológica obrigatória. O objetivo é fornecer um modelo mental, decisões explícitas, controles mínimos e caminhos de evolução que apoiem cada organização na construção da sua própria plataforma.

Os componentes e serviços descritos representam uma decomposição lógica de capacidades. Eles podem ser implementados com diferentes produtos, provedores, topologias e níveis de granularidade.

## O que você encontrará

- uma narrativa que começa pelo problema organizacional, antes da tecnologia;
- um capability map para delimitar o escopo da plataforma;
- um operating model com responsabilidades e fóruns de decisão;
- um ciclo de vida de agentes baseado em risco e evidências;
- um estudo de caso completo de agente documental com RAG;
- decision guides para escolhas arquiteturais recorrentes;
- um modelo de maturidade e roadmap de adoção;
- checklists de readiness para produção;
- contratos, diagramas, policies e amostras técnicas como material de referência.

## Caminhos de leitura

| Perfil | Caminho recomendado | Resultado esperado |
|---|---|---|
| Executivo ou sponsor | Capítulos 1, 2, 3 e 7 | entender valor, escopo, investimento, riscos e sequência de adoção |
| Arquiteto | Capítulos 1 a 7 | dominar capacidades, decisões, fronteiras e trade-offs |
| Engenharia de plataforma | Capítulos 2, 4, 5, 6 e 8 | transformar a referência em backlog implementável e operável |
| Segurança, Jurídico e LGPD | Capítulos 3, 4, 5 e 8 | identificar gates, evidências, classificação e responsabilidades |
| Product squad | Capítulos 1, 4, 5 e 8 | estruturar um caso de uso e publicá-lo pelo golden path |
| SRE e FinOps | Capítulos 2, 4, 7 e 8 | definir SLOs, capacidade, incidentes, budgets e accountability |

## Partes do livro

1. [Por que uma AI Platform?](01-why-ai-platform.md)
2. [Capability Map](02-capability-map.md)
3. [Operating Model](03-operating-model.md)
4. [Ciclo de vida de agentes](04-agent-lifecycle.md)
5. [Estudo de caso: agente documental com RAG](05-case-study-document-agent.md)
6. [Decision Guides](06-decision-guides.md)
7. [Modelo de maturidade e roadmap de adoção](07-adoption-roadmap.md)
8. [Checklists de produção](08-production-checklists.md)
9. [Glossário](glossary.md)

## Como usar os artefatos técnicos

Os capítulos explicam contexto, decisões e consequências. Os diretórios técnicos permanecem como fontes canônicas de referência:

| Assunto | Referência técnica |
|---|---|
| Princípios, C4 e NFRs | [`../architecture/`](../architecture/) |
| APIs, eventos e MCP | [`../contracts/`](../contracts/) |
| Capacidades e serviços lógicos | [`../services/`](../services/) |
| Governança e risco | [`../governance/`](../governance/) |
| Segurança | [`../security/`](../security/) |
| Observabilidade e SLOs | [`../observability/`](../observability/) |
| FinOps | [`../finops/`](../finops/) |
| Runbooks de referência | [`../runbooks/`](../runbooks/) |
| Amostra de validação | [`../../samples/vertical-slice/`](../../samples/vertical-slice/) |

A amostra técnica existe para verificar contratos e alguns controles documentados. Ela não representa uma arquitetura física recomendada nem uma implementação produtiva da plataforma.

## Convenção dos capítulos

Cada capítulo procura responder cinco perguntas:

1. Qual problema está sendo resolvido?
2. Qual decisão ou modelo é recomendado?
3. Quais trade-offs foram assumidos?
4. Como verificar que a decisão funciona?
5. Qual é o próximo artefato técnico a consultar?

## Escopo e limites

Este material é uma arquitetura de referência para implementação. Ele não substitui threat modeling específico, análise jurídica, sizing, homologação de fornecedores, testes de carga ou desenho detalhado de infraestrutura. As decisões devem ser reavaliadas quando o risco, o volume, a criticidade ou a regulamentação mudarem.
