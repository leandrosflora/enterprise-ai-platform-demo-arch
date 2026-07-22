# ADR-004 — Agent Runtime com núcleo estável e adaptadores

**Status:** Aceito

## Contexto

A plataforma precisa executar agentes corporativos integrando modelos, memória, RAG, ferramentas, avaliação, políticas e observabilidade. O ecossistema de frameworks muda rapidamente; acoplar contratos corporativos a um framework específico aumenta lock-in e dificulta governança consistente.

## Decisão

Adotar um **Agent Runtime corporativo com núcleo estável e adaptadores** para frameworks e provedores de orquestração.

O núcleo deve controlar:

- identidade do agente e versão publicada;
- carregamento de configuração imutável;
- aplicação de políticas e limites de autonomia;
- execução de prompts, workflows e tools;
- integração com Model Gateway, Knowledge Service e Memory Service;
- checkpoint, timeout, retry e cancelamento;
- eventos, auditoria, avaliação e telemetria.

Adaptadores podem integrar LangGraph, Semantic Kernel, serviços gerenciados de agentes ou implementações customizadas, desde que preservem os contratos e controles do núcleo.

## Limites

- regras de negócio permanecem nos serviços de domínio;
- credenciais de provedores permanecem no Model Gateway;
- aprovação e catálogo permanecem no Control Plane;
- tools são acessadas por fronteiras governadas, preferencialmente MCP;
- o framework não define o formato canônico de auditoria, eventos ou políticas.

## Alternativas

| Alternativa | Vantagem | Limitação |
|---|---|---|
| Framework único | menor esforço inicial | lock-in e controles dependentes do framework |
| Runtime por squad | autonomia local | fragmentação de segurança, telemetria e custos |
| Serviço gerenciado único | operação simplificada | portabilidade e extensibilidade limitadas |

## Consequências positivas

- contratos corporativos permanecem estáveis durante trocas de framework;
- políticas, observabilidade e FinOps são uniformes;
- evolução tecnológica ocorre por adaptadores;
- agentes podem usar padrões distintos sem perder governança.

## Consequências negativas

- aumenta a complexidade inicial do runtime;
- exige testes de conformidade para adaptadores;
- recursos exclusivos de frameworks podem precisar de extensão controlada;
- o núcleo pode se tornar gargalo se acumular responsabilidades de domínio.

## Evidências mínimas

- contrato de invocação versionado;
- testes de conformidade do adaptador;
- traces de model call, retrieval, memória e tool call;
- teste de timeout, cancelamento, retry e rollback;
- policy decision registrada por execução;
- compatibilidade documentada entre versão do runtime e adaptadores.

## Critérios de revisão

Revisar quando um padrão aberto ou runtime gerenciado fornecer portabilidade, controles e observabilidade equivalentes, ou quando a camada de adaptação gerar mais custo e risco do que o lock-in que busca evitar.
