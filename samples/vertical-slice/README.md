# Vertical Slice

Demo mínima da Enterprise AI Platform. Ela demonstra o fluxo arquitetural e controles de segurança; não é implementação de produção.

## Componentes

- FastAPI: Agent Registry, Governance, Runtime e Model Gateway simplificados;
- Secure RAG: quarentena, checksum, fonte aprovada, ACL, clearance e post-filter;
- Secure Memory: consentimento, TTL, origem, confiança, subject isolation e anti-poisoning;
- Redpanda: eventos Kafka;
- OpenTelemetry Collector + Jaeger: traces;
- Prometheus: métricas;
- Redpanda Console: inspeção dos tópicos.

## Executar

```bash
cd samples/vertical-slice
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
- quarentena de documento com indirect prompt injection;
- checksum, proveniência e fonte aprovada;
- ACL por papel, finalidade, tenant e clearance;
- conteúdo RAG delimitado como `<untrusted_document>`;
- memória de perfil com consentimento obrigatório;
- TTL por tipo de memória;
- bloqueio de `RESTRICTED` e `MODEL_INFERRED` persistente;
- detecção de memory poisoning;
- isolamento por sujeito em hash;
- exclusão auditável de memória;
- métricas de invocação, custo e negação de política;
- propagação de correlation ID.

## Headers simulados de segurança

| Header | Uso |
|---|---|
| `X-Demo-Scopes` | Escopos autorizados |
| `X-Demo-Tenant` | Tenant derivado da identidade na produção |
| `X-Demo-Actor` | Ator auditável |
| `X-Demo-Subject` | Sujeito proprietário da memória |
| `X-Demo-Roles` | Papéis usados na ACL de RAG |
| `X-Demo-Clearance` | Clearance de classificação |

## O que permanece fora da demo

- IdP real e validação JWT;
- persistência transacional;
- antivírus, DLP e policy engine externos reais;
- ACL sincronizada com diretório corporativo;
- foundation model real;
- alta disponibilidade, KMS e IRSA;
- avaliação automática completa;
- workflow produtivo de revogação de consentimento e exclusão em backups.
