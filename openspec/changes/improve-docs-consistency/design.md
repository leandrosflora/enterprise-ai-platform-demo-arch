## Context

`enterprise-ai-platform-demo-arch` is a documentation-only repository (no application code) that serves as a reference architecture. `README.md` and `docs/README.md` publish a "map" of the documentation: domains, services, contracts, governance, ADRs, etc. A review of the tree against that map found four categories of drift:

1. `docs/README.md`'s "Próximos artefatos recomendados" list still points at `adr/ADR-002-vector-database.md`; the file was created as `docs/adr/ADR-002-vector-database-selection.md`.
2. `docs/architecture/principles/` and `docs/architecture/decisions/` exist only as `.gitkeep` placeholders, even though `docs/README.md` describes `architecture/` as holding "diagramas, princípios e decisões arquiteturais".
3. `docs/adr/` already holds all five ADRs (numbered, dated decisions), which is the same content type `docs/architecture/decisions/` was scaffolded for — two homes for one concept.
4. `docs/domains/*.md` "Serviços Relacionados" sections cite `Agent Gateway`, `Evaluation Service`, `Audit Service`, and `Billing Service`, but `docs/services/` has no page for any of them (it has pages for `agent-runtime`, `agent-registry`, `knowledge-service`, `memory-service`, `mcp-registry`, `governance-service` only).

Existing docs (domain pages, `docs/services/governance-service.md`, `docs/contracts/data-stores.md`) already establish a consistent per-service template: Visão Geral, Responsabilidades, (Fora de Escopo), APIs/lifecycle, Dependências, Eventos Publicados, Requisitos Não Funcionais, Decisões Relacionadas. New docs should follow it rather than invent a new shape.

## Goals / Non-Goals

**Goals:**
- Every path and filename referenced from `README.md` / `docs/README.md` resolves to a real file.
- Every folder the docs map promises has real content, or is removed if it has no distinct purpose.
- Every service named as "related" from a domain page has a corresponding `docs/services/*.md` page, written to the same template already used by existing service docs.
- `docs/adr/` remains the single home for architecture decision records; `docs/architecture/` does not duplicate it.

**Non-Goals:**
- Rewriting existing docs' depth or style — the terse, table/bullet-driven format is intentional and consistent; this change does not expand unrelated pages.
- Introducing new domains, capabilities, or services beyond the four already implied by existing cross-references.
- Any change to application code, CI, or tooling — there is none in this repo.

## Decisions

- **Remove `docs/architecture/decisions/` rather than populate it.** It duplicates `docs/adr/`, which already holds numbered ADRs (ADR-001..005) and is the location every other doc links to (e.g. `docs/services/agent-runtime.md` → `../adr/ADR-001-...`). Keeping two folders for the same content invites the next contributor to file a new decision in the wrong place. `docs/README.md`'s structure blurb is reworded to say decisions live in `docs/adr/`.
  - *Alternative considered*: keep `architecture/decisions/` as a curated index/pointer into `docs/adr/`. Rejected — an index folder with no content beyond links duplicates what `README.md`'s ADR section already lists.
- **Populate `docs/architecture/principles/` with a single `principles.md`.** Content is derived from patterns already implied but never stated explicitly across the repo (per-service data ownership in `docs/contracts/data-stores.md`, authorization/observability/audit requirements repeated in every domain's NFR section, event-driven integration in `docs/contracts/events.md`). Stating them once in `architecture/principles/` gives domain/service authors a shared reference instead of restating the same NFRs independently in every file.
  - *Alternative considered*: leave the folder out of the map entirely (remove the promise instead of fulfilling it). Rejected — the principles are the one piece of architectural intent not documented anywhere yet, and the repo's audience (architects) is exactly who needs them written down.
- **Write the four missing service docs using the existing template** (Visão Geral, Responsabilidades, Fora de Escopo, Dependências, Eventos Publicados, Requisitos Não Funcionais, Decisões Relacionadas where applicable), sized similarly to current service docs (roughly 30-100 lines). Content is derived from what's already implied about each service elsewhere in the repo (e.g. `Billing Service` already appears in `docs/contracts/data-stores.md` as owning a PostgreSQL store for "Custos e chargeback"; `Evaluation Service` is already a dependency listed in `agent-runtime.md` and `governance-service.md`).
  - *Alternative considered*: only fix the broken reference and leave the missing service docs for a separate change. Rejected — the four gaps are the same class of problem (map promises something the tree doesn't deliver) and are small enough to fix together.
- **Update both `README.md` and `docs/README.md` maps** to list the four new service docs and to reflect the resolved architecture folders, so the maps stay authoritative after this change.

## Risks / Trade-offs

- [Writing `principles.md` content that isn't a plain rename/move risks introducing "new" architectural intent not agreed elsewhere] → Mitigation: every principle stated is one already implied by repeated patterns in existing NFR sections and contracts docs, not a novel decision; keep it short (5-8 principles, no new capability).
- [Removing `docs/architecture/decisions/` could look like discarding planned content] → Mitigation: `docs/adr/` already fully covers the same purpose with 5 populated ADRs; call this out explicitly in the commit/PR description.
- [New service docs could drift from the real (non-existent) implementation since there is no code to verify against] → Mitigation: keep them consistent with what other docs already assert about these services (dependencies, events, data stores) rather than inventing new behavior.

## Migration Plan

Documentation-only change, applied directly to `main` via normal file edits; no runtime migration, rollback is a plain revert.
