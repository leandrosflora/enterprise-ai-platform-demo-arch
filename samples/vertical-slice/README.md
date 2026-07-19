# Vertical Slice

Demo mínima da Enterprise AI Platform. Ela demonstra o fluxo arquitetural; não é implementação de produção.

## Componentes

- FastAPI: Agent Registry, Governance, Runtime e Model Gateway simplificados;
- Redpanda: eventos Kafka;
- OpenTelemetry Collector + Jaeger: traces;
- Prometheus: métricas;
- Redpanda Console: inspeção dos tópicos.

## Executar

```bash
docker compose up --build
```

Após a API ficar saudável:

```bash
bash scripts/demo.sh
```

## Testes

Na raiz do repositório:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r samples/vertical-slice/app/requirements.txt
PYTHONPATH=samples/vertical-slice pytest -q samples/vertical-slice/tests
```

## Controles demonstrados

- escopos por operação;
- segregação entre submissão e aprovação;
- versão imutável durante o ciclo;
- idempotency key em comandos;
- agente precisa estar `PUBLISHED`;
- envelope canônico de eventos;
- RAG e tool call simulados;
- métricas de invocação e custo;
- propagação de correlation ID.

## O que permanece fora da demo

- IdP real e validação JWT;
- persistência transacional;
- ACL real por documento/chunk;
- policy engine externo;
- foundation model real;
- alta disponibilidade, KMS e IRSA;
- avaliação automática completa.
