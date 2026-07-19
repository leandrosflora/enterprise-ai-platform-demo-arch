# Política de Segurança

## Reporte responsável

Não publique vulnerabilidades, secrets ou dados pessoais em issues públicas.

Use o recurso **Security Advisories** do GitHub no repositório para reportar vulnerabilidades de forma privada. Inclua:

- componente afetado;
- cenário de exploração;
- impacto;
- versão ou commit;
- evidência mínima reproduzível;
- mitigação sugerida, quando houver.

## Escopo

São relevantes, entre outros:

- bypass de autorização;
- cross-tenant access;
- prompt injection com acesso a dados ou tools;
- execução indevida de MCP tools;
- exposição de secrets;
- falhas de idempotência com efeito duplicado;
- vazamento por logs, traces, memória ou RAG;
- dependências ou imagens comprometidas.

## Dados de teste

Use apenas dados sintéticos. Não inclua tokens reais, CPF, dados financeiros, prompts corporativos ou documentos confidenciais.

## Controles de contribuição

A pipeline verifica contratos, documentação, diagramas e a vertical slice. Mudanças em segurança, governança, contratos ou workflows exigem revisão do owner do repositório.
