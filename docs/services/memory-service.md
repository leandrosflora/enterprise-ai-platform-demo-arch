# Memory Service

## Visão Geral

O Memory Service persiste somente contexto necessário e autorizado. Ele não é um log de conversa e não aceita que o modelo transforme inferências em fatos permanentes.

Padrão obrigatório: [Segurança de RAG e Memória](../security/rag-memory-security.md).

## Responsabilidades

- manter memória de sessão, curto prazo, longo prazo e perfil;
- aplicar tenant e isolamento por sujeito;
- validar finalidade, consentimento, origem, confiança e classificação;
- impor TTL por tipo;
- detectar memory poisoning;
- versionar alterações;
- excluir ou anonimizar após expiração ou revogação;
- emitir eventos sem valores sensíveis.

## Tipos de Memória

| Tipo | Finalidade | TTL máximo | Consentimento |
|---|---|---:|---|
| `SESSION` | Contexto da conversa atual | 24 horas | Conforme dado |
| `SHORT_TERM` | Continuidade operacional | 7 dias | Conforme finalidade |
| `LONG_TERM` | Fatos reutilizados | 365 dias | Obrigatório |
| `PROFILE` | Preferências explícitas | 365 dias | Obrigatório |

## Modelo de Item

```json
{
  "key": "preferred-language",
  "value": "pt-BR",
  "classification": "INTERNAL",
  "source": "USER_CONFIRMED",
  "confidence": 1.0,
  "purpose": "personalize-support",
  "consentReference": "consent-001",
  "expiresAt": "2027-01-01T00:00:00Z"
}
```

O valor é criptografado em repouso e não aparece em logs ou eventos.

## Política de Escrita

A decisão padrão é negar. A escrita só ocorre quando:

- o tenant e sujeito vêm da identidade autenticada;
- a finalidade está permitida;
- o TTL respeita o tipo;
- a classificação pode ser persistida;
- a origem é compatível com o tipo;
- não há indicador de poisoning;
- existe consentimento para `LONG_TERM` e `PROFILE`.

### Origem e confiança

| Origem | Sessão | Curto prazo | Longo prazo / Perfil |
|---|---:|---:|---:|
| `USER_CONFIRMED` | Sim | Sim | Sim |
| `SYSTEM_VERIFIED` | Sim | Sim | Sim |
| `TOOL_OUTPUT` | Sim | Conforme política | Não sem verificação |
| `MODEL_INFERRED` | Sim | Não | Não |

`RESTRICTED` é não persistente por padrão.

## Proteção contra Memory Poisoning

O serviço rejeita:

- instruções apresentadas como fatos;
- tentativas de sobrescrever system/developer instructions;
- conteúdo pedindo execução de ferramenta;
- dados derivados exclusivamente do modelo para memória persistente;
- alteração de preferência sem confirmação;
- conflito com fato verificado sem reconciliação.

Indicadores geram `policy_denials_total{resource_type="memory"}` e evento de auditoria sem o valor rejeitado.

## Isolamento

A chave lógica é:

```text
tenantId + subjectHash + sessionId + memoryType
```

- `subjectHash` é derivado da identidade;
- chamadas não aceitam um sujeito arbitrário no payload;
- workloads técnicos usam workload identity com escopo mínimo;
- consultas administrativas são separadas e auditadas;
- caches preservam a mesma chave de isolamento.

## APIs

```http
GET    /v1/sessions/{sessionId}/memory
PATCH  /v1/sessions/{sessionId}/memory
DELETE /v1/sessions/{sessionId}/memory
```

### Escrita

```json
{
  "memoryType": "PROFILE",
  "purpose": "Personalize approved support",
  "ttlSeconds": 3600,
  "consentReference": "consent-001",
  "items": [
    {
      "key": "preferred-language",
      "value": "pt-BR",
      "classification": "INTERNAL",
      "source": "USER_CONFIRMED",
      "confidence": 1.0
    }
  ]
}
```

## Ciclo de Vida

1. validar política;
2. gravar versão imutável;
3. atualizar ponteiro da versão ativa;
4. registrar TTL;
5. emitir `memory.updated` sem conteúdo;
6. expirar automaticamente;
7. excluir ou anonimizar;
8. emitir `memory.deleted`.

Revogação de consentimento bloqueia leitura e escrita antes do processamento assíncrono de exclusão.

## Eventos

- `memory.updated`
- `memory.expired`
- `memory.deleted`
- `memory.consent_revoked`

Campos permitidos: sessão, sujeito em hash, tipo, quantidade, versão, expiração e presença de consentimento. Valores são proibidos.

## Armazenamento

MongoDB ou banco equivalente com:

- criptografia em repouso;
- TTL index;
- chave composta de tenant e sujeito;
- versionamento otimista;
- backup compatível com exclusão;
- trilha de descarte.

## Requisitos Não Funcionais

| Requisito | Diretriz |
|---|---|
| Segurança | Deny by default e anti-poisoning |
| Privacidade | Consentimento, minimização e descarte |
| Isolamento | Tenant + subject hash |
| Rastreabilidade | Origem, confiança, versão e finalidade |
| Disponibilidade | Degradação sem memória quando indisponível |
| Consistência | Controle de concorrência e reconciliação |
