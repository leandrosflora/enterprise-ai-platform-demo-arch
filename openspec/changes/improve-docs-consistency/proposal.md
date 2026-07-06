## Why

This repository is a documentation-only architecture reference (no application code). A full review of `docs/` and the root `README.md` found concrete consistency gaps that undermine the reference's usefulness: a stale file reference, two placeholder folders promised by the docs map but never populated, and four services that are cited as "Serviços Relacionados" from domain docs but have no corresponding service page. Left alone, these gaps make the map misleading for the architects and platform engineers this repo targets.

## What Changes

- Fix the stale reference in `docs/README.md` "Próximos artefatos recomendados" list: it points to `adr/ADR-002-vector-database.md`, but the actual file is `docs/adr/ADR-002-vector-database-selection.md`.
- Populate `docs/architecture/principles/` (currently only `.gitkeep`) with the platform's architectural principles, since `docs/README.md` describes this folder as holding "princípios arquiteturais".
- Resolve `docs/architecture/decisions/` (currently only `.gitkeep`), which duplicates the purpose of `docs/adr/` where ADRs already live: either remove the empty, redundant folder or repurpose it with a clear, distinct role documented in `docs/README.md`.
- Add the four missing service docs referenced from `docs/domains/*.md` "Serviços Relacionados" sections but absent from `docs/services/`: `agent-gateway.md`, `evaluation-service.md`, `audit-service.md`, `billing-service.md`, following the structure of existing service docs (e.g. `docs/services/agent-runtime.md`).
- Update `README.md` and `docs/README.md` documentation maps to list the new service docs and the resolved architecture folders.

## Capabilities

### New Capabilities
- `docs-integrity`: Consistency rules for the architecture documentation set — every folder promised by the docs map has content, every cross-referenced artifact (ADRs, services) resolves to an actual file, and every service mentioned as "related" from a domain doc has its own service page.

### Modified Capabilities
(none — `openspec/specs/` has no existing specs; this is the first capability introduced)

## Impact

- Affected files: `README.md`, `docs/README.md`, `docs/architecture/principles/*`, `docs/architecture/decisions/*` (or its removal), `docs/services/agent-gateway.md`, `docs/services/evaluation-service.md`, `docs/services/audit-service.md`, `docs/services/billing-service.md`.
- No application code, APIs, or runtime systems are affected — this is a documentation-only change.
