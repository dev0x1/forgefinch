---
name: api-contracts
description: Use for OpenAPI artifacts, contract-root tooling, generated TypeScript SDKs, Rust contract DTOs, Rust public API SDKs, and release checks in the in-tree API contract boundary.
---

# api-contracts

## Purpose

Maintain the in-tree public API contract and SDK distribution
boundary without moving backend product behavior into it.

## Use This Skill When

- Updating OpenAPI source or the bundled contract artifact.
- Regenerating or changing the TypeScript SDK.
- Updating Rust DTOs or the Rust public API SDK.
- Changing contract-root tooling, checks, docs, or release workflow.
- Coordinating a platform public API behavior change with contract and SDK
  artifacts in the same repo.

## Workflow

1. Read `AGENTS.md`, `docs/architecture/api-contract-repo.md`, and the active
   workpackage record under `docs/workpackages/` when present.
2. Confirm the change belongs in the contract/SDK distribution boundary. If it
   changes backend route behavior, policy, persistence, audit, evidence, or
   projections, coordinate the owning platform slice rather than implementing
   that behavior here.
3. Use repository-defined variables such as `CONTRACT_ROOT` and
   `OPENAPI_BUNDLE` rather than hardcoded ad hoc paths.
4. For OpenAPI changes, also use `$openapi-authoring`.
5. For SDK generation or SDK runtime changes, also use
   `$sdk-generation`.
6. For release or downstream consumer handoff changes, also
   use `$api-contract-release`.
7. Classify each query as an authenticated-user resource, product resource,
   bounded resource summary, collection, search/directory, or
   consuming-client composition. Keep consuming-client composition out of the
   public API contract.
8. For every query contract, record its intended caller, exact authorization
   metadata, field provenance, freshness/snapshot posture, pagination, and
   explicit capability/version discovery behavior.
9. Confirm that one collection semantic has one canonical path, operation ID,
   and DTO family. A separate search or directory must declare meaningfully
   different behavior rather than aliasing the collection.
10. Use the repository's resource-action operation-ID convention, for example
    `get_workspace_overview` or `list_workspace_workstreams`; do not encode the
    path version as `get_v1_*` or mix naming conventions across equivalent
    resources.
11. Confirm each OpenAPI operation is reachable through the constructed
    production router. Do not accept a handler symbol, catalog row, or generated
    method as runtime implementation evidence.
12. For OpenAPI changes, run `just api-contract-check`.
13. For TypeScript SDK changes, run `just sdk-ts-generate` and
   `just sdk-ts-check`.
14. For Rust SDK changes, run `just sdk-rust-check`.
15. For docs/process changes, run `just lint-docs` and
   `just contract-workpackages-check`.

## Guardrails

- Do not implement backend route handlers, domain behavior, persistence,
  policy decisions, audit storage, evidence storage, or projections here.
- Do not let generated SDK code hide OpenAPI or backend contract drift.
- Do not add unpinned Node, Cargo, or CI dependencies.
- Keep generated TypeScript files committed with the OpenAPI artifact they
  were generated from.
- Keep repository-defined contract-root and OpenAPI-bundle variables as
  repository-local build/dev variables; they are not runtime product config.
- Do not name shared routes, operation IDs, DTOs, or contract groups after
  Electron desktop app, desktop, web, mobile, CLI, or another consuming client.
- Do not put composer, navigation, panel, widget, feed, or other UI layout
  state in a generic product-resource DTO. Keep client composition client-owned
  and expose bounded resource summaries or separately pageable collections.
- Do not make a general authenticated-user context depend on an administrative
  collection or capability. Contract metadata and role tests must prove the
  context is usable by every intended signed-in role.
- Do not use 404 as feature/version discovery. Preserve concealed-resource 404
  semantics and advertise supported contract versions and effective
  capabilities explicitly.
- Do not describe a projection field as authoritative unless its owning
  implementation persists it, computes it from named authoritative inputs, or
  exposes it as explicitly optional/unavailable.
- Do not permit duplicate collection contracts with different operation IDs or
  DTOs unless a separately named search/directory semantic is documented and
  tested.
- Do not mix semantic resource-action operation IDs with path/version-derived
  names for equivalent public operations.
- Do not treat OpenAPI/generated-client presence as runtime route closure;
  executable router reachability is required.
- Do not add environment-only DTO fields, operations, examples, or relaxed
  authorization. Optional integration packs use the same public contract as
  the core backend.

## Done Means

- Contract artifacts, generated SDK files, docs, and tests agree.
- Public query contracts are client-neutral, authorization-correct, canonical,
  explicit about availability and freshness, and reachable in the production
  router.
- The relevant `just` checks pass or are recorded as skipped with a concrete
  reason.
- Backend behavior changes are coordinated in the owning platform workpackage,
  not silently absorbed in SDK code.
