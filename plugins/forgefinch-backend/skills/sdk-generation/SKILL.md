---
name: sdk-generation
description: Use for generated TypeScript SDKs, Rust DTO/client SDKs, SDK tests, and SDK boundary guardrails in the in-tree API contract boundary.
---

# sdk-generation

## Purpose

Keep the TypeScript and Rust SDKs aligned with the canonical OpenAPI artifact
while preserving their boundary as public REST/SSE clients only.

## Use This Skill When

- Regenerating or reviewing `@project/API client`.
- Updating TypeScript SDK runtime helpers, generated operation metadata, or
  package scripts.
- Updating `api-contracts` DTOs or the API client request/response helpers.
- Changing SDK behavior for auth headers, tenant/correlation headers,
  idempotency keys, pagination, safe errors, or SSE reconnect helpers.

## Workflow

1. Read `AGENTS.md`, `docs/architecture/api-contract-repo.md`, and SDK docs
   under `docs/sdk/`.
2. Confirm SDK behavior follows the bundled OpenAPI artifact and does not hide
   contract/backend drift.
3. For TypeScript SDK generation, run `just sdk-ts-generate` and then
   `just sdk-ts-check`.
4. For Rust SDK or DTO changes, run `just sdk-rust-check`.
5. For full repo verification, run `just check`.
6. Keep generated TypeScript files committed with the OpenAPI artifact that
   produced them.

## Guardrails

- SDKs may prepare and execute public REST/SSE requests, parse safe errors,
  model pagination and idempotency, and expose raw/debug escape hatches.
- SDKs must not own product logic, authorization decisions, persistence,
  policy decisions, audit/evidence storage, or projections.
- the API client depends on `api-contracts` and public HTTP/SSE crates
  only; it must not depend on platform domain or adapter crates.
- Do not add unpinned npm or Cargo dependencies.

## Done Means

- SDK runtime, generated code, OpenAPI artifact, package metadata, and tests
  agree.
- `just sdk-ts-check` and/or `just sdk-rust-check` pass for touched SDKs.
- Any required platform route or CLI behavior is tracked in the owning
  workpackage.
