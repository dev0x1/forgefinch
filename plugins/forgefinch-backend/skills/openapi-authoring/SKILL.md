---
name: openapi-authoring
description: Use for authoring the public OpenAPI source, bundle, operation metadata, safe errors, idempotency documentation, and contract drift checks in the in-tree API contract boundary.
---

# openapi-authoring

## Purpose

Maintain the canonical public OpenAPI contract without moving
backend route behavior or product semantics into this boundary.

## Use This Skill When

- Editing modular OpenAPI source under the repository-owned API contract package.
- Updating the bundled `api.v1.json` artifact.
- Adding or revising operation IDs, tags, request/response schemas, safe error
  envelopes, pagination, idempotency, security, or SSE documentation.
- Reviewing API contract drift between platform route behavior and in-tree
  contract artifacts.

## Workflow

1. Read `AGENTS.md`, `docs/architecture/api-contract-repo.md`, and the active
   workpackage record under `docs/workpackages/` when present.
2. Confirm the OpenAPI change is only contract/source-of-truth work. Backend
   route handlers, persistence, policy, audit, evidence, and projections remain
   in platform route and domain crates.
3. Use repository-defined variables such as `CONTRACT_ROOT` and
   `OPENAPI_BUNDLE` for paths in scripts, docs, and checks.
4. Keep operation IDs stable unless the platform route intentionally changes
   behavior and the coordinated workpackage names the compatibility impact.
5. Keep safe error, auth, tenant context, idempotency, pagination, and SSE
   metadata explicit enough for generated SDKs and Playwright response-schema
   validation.
6. Run `just api-contract-check` after OpenAPI edits.
7. If the change affects generated clients, run `just sdk-ts-generate`,
   `just sdk-ts-check`, and `just sdk-rust-check` as applicable.

## Guardrails

- Do not implement route handlers or domain behavior here.
- Do not treat generated SDK output as a source of truth over OpenAPI.
- Do not remove public operation metadata without coordinating platform route,
  SDK, CLI, and live HTTP verification.
- Do not add unpinned generators or schema tools.

## Done Means

- Modular OpenAPI source, bundled OpenAPI, Rust contract tests, and generated
  SDK inputs agree.
- The relevant `just` checks pass or are recorded as skipped with a concrete
  reason.
- Any backend behavior dependency is captured in the coordinated platform
  workpackage.
