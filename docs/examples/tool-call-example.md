# Exemplo - Tool Call MCP

## Objetivo

Exemplo de chamada de ferramenta exposta via MCP Server.

```json
{
  "correlationId": "corr-2026-001",
  "agentId": "internal-copilot",
  "toolName": "customer-search",
  "toolVersion": "1.0.0",
  "caller": {
    "userId": "user-123",
    "businessUnit": "Atendimento",
    "roles": ["BusinessUser"]
  },
  "arguments": {
    "document": "12345678900",
    "documentType": "CPF"
  }
}
```

## Resposta Esperada

```json
{
  "correlationId": "corr-2026-001",
  "status": "SUCCESS",
  "result": {
    "customerId": "cust-789",
    "status": "ACTIVE"
  }
}
```

## Controles

- Validação por JSON Schema
- Autorização por escopo
- Auditoria do tool call
- Mascaramento de dados sensíveis em logs
