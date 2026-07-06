## 1. Fix stale reference

- [x] 1.1 In `docs/README.md`, update the "Próximos artefatos recomendados" entry from `adr/ADR-002-vector-database.md` to `adr/ADR-002-vector-database-selection.md`

## 2. Resolve architecture placeholder folders

- [x] 2.1 Write `docs/architecture/principles/principles.md` with the platform's architectural principles (derived from patterns already implied in `docs/contracts/data-stores.md` and domain NFR sections: per-service data ownership, no direct cross-service DB access, event-driven integration, security/governance by default, end-to-end observability, cost-awareness)
- [x] 2.2 Remove `docs/architecture/decisions/` (including `.gitkeep`) since `docs/adr/` is the single home for ADRs
- [x] 2.3 Update the `docs/README.md` structure overview so `architecture/` is described as holding diagrams and principles, and decisions are described as living in `docs/adr/`

## 3. Add missing service docs

- [x] 3.1 Write `docs/services/agent-gateway.md` following the existing service template (Visão Geral, Responsabilidades, Dependências, Eventos Publicados, Requisitos Não Funcionais), consistent with how `docs/domains/agent-platform.md` describes it
- [x] 3.2 Write `docs/services/evaluation-service.md`, consistent with its use as a dependency in `docs/services/agent-runtime.md` and `docs/services/governance-service.md`
- [x] 3.3 Write `docs/services/audit-service.md`, consistent with its use as a dependency in `docs/services/governance-service.md`
- [x] 3.4 Write `docs/services/billing-service.md`, consistent with `docs/contracts/data-stores.md` (owns the "Custos e chargeback" PostgreSQL store) and `docs/finops/token-costs.md`

## 4. Update documentation maps

- [x] 4.1 Update `README.md`'s "Serviços" section to list the four new service docs
- [x] 4.2 Update `docs/README.md`'s "Estrutura" and any service listing to reflect the new files and resolved architecture folders

## 5. Verify

- [x] 5.1 Re-check that every path referenced in `README.md` and `docs/README.md` resolves to an existing file
- [x] 5.2 Re-check that every service named in a `docs/domains/*.md` "Serviços Relacionados" section has a corresponding `docs/services/*.md` page
