# docs-integrity Specification

## Purpose
Keep the architecture documentation set internally consistent: every path the top-level maps (`README.md`, `docs/README.md`) reference must exist, every folder those maps promise must have content, and every service cited from a domain doc must have its own service page.

## Requirements

### Requirement: Documentation map references resolve to real files
Every file path named in `README.md` or `docs/README.md` SHALL correspond to an existing file in the repository.

#### Scenario: ADR reference in docs/README.md
- **WHEN** `docs/README.md` recommends an ADR artifact by filename
- **THEN** that filename SHALL match an existing file under `docs/adr/`

### Requirement: Architecture folders promised by the docs map contain content
Every subfolder of `docs/architecture/` described in `docs/README.md`'s structure overview SHALL contain at least one substantive file, or SHALL be removed from the repository and from the structure overview.

#### Scenario: Principles folder is populated
- **WHEN** `docs/README.md` describes `docs/architecture/` as containing "princípios arquiteturais"
- **THEN** `docs/architecture/principles/` SHALL contain a `principles.md` file documenting the platform's architectural principles

#### Scenario: No duplicate home for architecture decisions
- **WHEN** a reader looks for architecture decision records
- **THEN** they SHALL find them only under `docs/adr/`, and `docs/architecture/decisions/` SHALL NOT exist as an empty duplicate location

### Requirement: Every service cited from a domain doc has a service page
For each service name listed under a "Serviços Relacionados" section in any `docs/domains/*.md` file, a corresponding page SHALL exist at `docs/services/<service-slug>.md`, following the structure used by existing service docs (Visão Geral, Responsabilidades, Dependências, Eventos Publicados, Requisitos Não Funcionais).

#### Scenario: Agent Gateway is documented
- **WHEN** `docs/domains/agent-platform.md` lists "Agent Gateway" as a related service/capability
- **THEN** `docs/services/agent-gateway.md` SHALL exist and describe its responsibilities, dependencies, and NFRs

#### Scenario: Evaluation Service is documented
- **WHEN** `docs/domains/evaluation-platform.md` (or other domain docs) lists "Evaluation Service" as a related service
- **THEN** `docs/services/evaluation-service.md` SHALL exist and describe its responsibilities, dependencies, and NFRs

#### Scenario: Audit Service is documented
- **WHEN** a domain or service doc lists "Audit Service" as a dependency or related service
- **THEN** `docs/services/audit-service.md` SHALL exist and describe its responsibilities, dependencies, and NFRs

#### Scenario: Billing Service is documented
- **WHEN** `docs/contracts/data-stores.md` or a domain doc lists "Billing Service" as owning a data store or related service
- **THEN** `docs/services/billing-service.md` SHALL exist and describe its responsibilities, dependencies, and NFRs
