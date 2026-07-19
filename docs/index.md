# Enterprise AI Platform

Este site apresenta um **book executável** sobre estratégia, arquitetura, governança e operação de plataformas corporativas de IA.

Ele combina narrativa editorial, referências técnicas, contratos versionados, policies e uma vertical slice executável.

## Comece pelo seu objetivo

<div class="grid cards" markdown>

-   :material-briefcase-outline: **Visão executiva**

    ---

    Entenda quando uma plataforma é necessária, quais capacidades ela oferece e como organizar o investimento.

    [Começar pelo problema](book/01-why-ai-platform.md)

-   :material-sitemap-outline: **Arquitetura**

    ---

    Explore capability map, control plane, data plane, serviços, contratos e decisões.

    [Abrir o capability map](book/02-capability-map.md)

-   :material-account-group-outline: **Operating model**

    ---

    Defina papéis, RACI, fóruns, golden path e rotas proporcionais ao risco.

    [Ler o operating model](book/03-operating-model.md)

-   :material-source-branch: **Delivery e lifecycle**

    ---

    Estruture gates, evidências, avaliação, publicação, operação e retirada de agentes.

    [Abrir o lifecycle](book/04-agent-lifecycle.md)

-   :material-shield-check-outline: **Segurança e governança**

    ---

    Aplique autorização, threat modeling, segurança de RAG, memória, LGPD e AI Risk Framework.

    [Ver segurança de RAG e memória](security/rag-memory-security.md)

-   :material-flask-outline: **Caso prático**

    ---

    Acompanhe um agente documental com RAG do problem statement ao checklist de produção.

    [Abrir o estudo de caso](book/05-case-study-document-agent.md)

</div>

## Livro

1. [Por que uma AI Platform?](book/01-why-ai-platform.md)
2. [Capability Map](book/02-capability-map.md)
3. [Operating Model](book/03-operating-model.md)
4. [Ciclo de vida de agentes](book/04-agent-lifecycle.md)
5. [Estudo de caso: agente documental com RAG](book/05-case-study-document-agent.md)
6. [Decision Guides](book/06-decision-guides.md)
7. [Modelo de maturidade e roadmap](book/07-adoption-roadmap.md)
8. [Checklists de produção](book/08-production-checklists.md)
9. [Glossário](book/glossary.md)

## Arquitetura resumida

```mermaid
flowchart TB
    subgraph CP[Control Plane]
      AR[Agent Registry]
      GR[Governance]
      ER[Evaluation Registry]
      MR[MCP Registry]
      PR[Policy Administration]
    end

    subgraph DP[Data Plane]
      AG[Agent Gateway]
      RT[Agent Runtime]
      PE[Policy Enforcement]
      KS[Knowledge Service]
      MS[Memory Service]
      MG[Model Gateway]
      MCP[MCP Execution]
    end

    AG --> RT
    RT --> PE
    RT --> KS
    RT --> MS
    RT --> MG
    RT --> MCP
    CP --> DP
```

## Referências canônicas

| Assunto | Fonte |
|---|---|
| APIs HTTP | [OpenAPI](contracts/openapi.yaml) |
| Eventos | [AsyncAPI](contracts/async-api.yaml) |
| Segurança de RAG e memória | [Padrão](security/rag-memory-security.md) |
| Risco | [AI Risk Framework](governance/ai-risk-framework.md) |
| SLOs | [Requisitos não funcionais](architecture/non-functional-requirements.md) |
| Deployment | [C4 Deployment](architecture/diagrams/c4-deployment.puml) |
| Demo | [Vertical slice](https://github.com/leandrosflora/enterprise-ai-platform-demo-arch/tree/main/samples/vertical-slice) |

## PDF

O workflow **Book** gera um manuscrito Markdown consolidado, um PDF e previews renderizados. Os arquivos ficam disponíveis como artifact do GitHub Actions a cada execução do workflow.
