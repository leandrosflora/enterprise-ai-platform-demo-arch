# Contribuindo

## Fluxo

1. abra uma issue descrevendo problema, impacto e proposta;
2. crie uma branch curta;
3. altere a fonte canônica, não apenas exemplos derivados;
4. execute as validações locais;
5. abra um PR com contexto, trade-offs e evidências.

## Validações

```bash
pip install pyyaml mkdocs-material
python scripts/validate_contracts.py
python scripts/validate_docs.py
mkdocs build --strict
bash scripts/render_diagrams.sh
```

Para a vertical slice:

```bash
pip install -r samples/vertical-slice/app/requirements.txt
PYTHONPATH=samples/vertical-slice pytest -q samples/vertical-slice/tests
docker compose -f samples/vertical-slice/docker-compose.yml config --quiet
```

## Regras arquiteturais

- AsyncAPI é a fonte canônica dos eventos.
- OpenAPI é a fonte canônica das APIs HTTP.
- Decisões relevantes exigem ADR.
- Versões publicadas e contratos major são imutáveis.
- Segurança, observabilidade e FinOps fazem parte do contrato.
- Exemplos devem validar contra os schemas correspondentes.

## Commits

Use mensagens objetivas, por exemplo:

- `docs: clarify policy enforcement`
- `feat: add model gateway contract`
- `ci: validate asyncapi schemas`

## Pull request

O PR deve informar:

- problema;
- decisão tomada;
- impacto em contratos e compatibilidade;
- riscos e controles;
- testes executados;
- necessidade de migração ou rollback.
