# ADR-001 — MCP para tool calling governado

**Status:** Aceito

## Contexto

Agentes precisam descobrir e executar ferramentas corporativas com contratos, autorização, versionamento e auditoria consistentes. Integrações REST diretas continuam adequadas para APIs de domínio, mas não resolvem sozinhas descoberta de tools, schemas orientados a agentes e enforcement uniforme durante o tool calling.

Este ADR consolida a decisão original de usar MCP com a estratégia legada de catálogo e governança de MCP Servers.

## Decisão

Usar **MCP** na fronteira entre Agent Runtime e ferramentas governadas. APIs REST continuam sendo usadas como interfaces de domínio internas e externas. O MCP não substitui REST; ele adiciona uma camada orientada ao consumo por agentes.

A plataforma deve manter um **MCP Registry** para:

- catálogo e descoberta de servidores, tools e schemas;
- ownership, classificação de risco e versão;
- políticas de autorização e allowlist por agente;
- compatibilidade entre versões de contrato;
- estado operacional e critérios de retirada;
- rastreabilidade entre tool call, identidade, política e sistema de registro.

## Fronteiras obrigatórias

- o Agent Runtime não acessa diretamente credenciais de sistemas de domínio;
- o MCP Server valida identidade de workload, tenant, scopes e finalidade;
- comandos com efeito colateral exigem idempotência e trilha de auditoria;
- operações longas retornam `operationId` e continuam de forma assíncrona;
- schemas e versões efetivas são registrados em traces e eventos;
- falha de política resulta em deny by default;
- MCP Servers não concentram regras de negócio que pertencem aos serviços de domínio.

## Por que

- descoberta padronizada de ferramentas e schemas;
- separação entre raciocínio do agente e implementação do domínio;
- enforcement central de identidade, escopo, estágio da jornada e auditoria;
- menor acoplamento entre framework de agentes e serviços corporativos;
- reutilização governada de tools entre agentes e domínios.

## Alternativas

| Alternativa | Vantagem | Limitação |
|---|---|---|
| REST direto | simples e universal | exige adaptação específica em cada agente e dispersa governança |
| Eventos | desacoplamento e escala | inadequado para toda interação request/response |
| SDK proprietário | produtividade inicial | lock-in e governança fragmentada |
| Plugin por agente | liberdade local | baixa reutilização e auditoria inconsistente |

## Consequências

O Tool Service/MCP Server torna-se uma fronteira de segurança e deve possuir SLO, observabilidade, política de versão, rollback e processo de onboarding. A adoção de MCP adiciona uma camada operacional, mas evita que autorização, auditoria e contratos sejam reimplementados por cada agente.

## Evidências mínimas

- contrato MCP versionado;
- owner e classificação de risco da tool;
- matriz de autorização;
- testes de argumentos inválidos, acesso negado e idempotência;
- traces correlacionando agente, versão, tool, política e resultado;
- runbook, SLO e estratégia de retirada.

## Critérios de revisão

Revisar a decisão quando o protocolo deixar de atender requisitos de segurança, compatibilidade, latência ou interoperabilidade, ou quando outro padrão aberto oferecer governança equivalente com menor custo operacional.
