# ADR-002 — Memória persistente sob critérios explícitos

**Status:** Aceito

## Contexto

Memória melhora continuidade e personalização, mas aumenta risco de privacidade, retenção indevida, contaminação entre tenants e uso de fatos desatualizados.

## Decisão

Adotar três níveis:

1. **memória de turno:** contexto da requisição;
2. **memória de sessão:** TTL curto em Redis;
3. **memória persistente:** armazenamento durável somente com propósito, consentimento ou base legal, classificação, TTL e mecanismos de exclusão.

Memória persistente não é padrão. O agente deve funcionar sem ela quando possível.

## Critérios para persistir

- melhora mensurável da experiência ou eficiência;
- dado permitido pela política e LGPD;
- isolamento por tenant e identidade;
- proveniência, data de atualização e confiança registradas;
- expiração e direito de exclusão implementados.

## Consequências

A recuperação deve filtrar escopo, recência e finalidade. Conteúdo recuperado é dado não confiável e não deve sobrescrever políticas ou instruções de sistema.

## Evidência no case

O case conversacional separa sessão ativa em Redis e histórico/memória de longo prazo em MongoDB, permitindo políticas distintas de TTL, acesso e retenção.