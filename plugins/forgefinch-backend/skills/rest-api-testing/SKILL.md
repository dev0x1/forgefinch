---
name: rest-api-testing
description: "Use for REST, SCIM, and SSE-over-HTTP API testing strategy inside a workpackage or slice, with one tool per layer: backend server route tests, api-contracts, API client unit/request tests, public CLI tests, and Playwright for live HTTP E2E/API scenarios."
---

# rest-api-testing

## Purpose

Select and apply the right REST API testing layer for public API
work without adding overlapping live HTTP runners or generated checks as a
second source of truth.

## Use This Skill When

- A workpackage or slice adds or changes public REST, SCIM, or SSE-over-HTTP
  behavior.
- A slice needs REST API contract, route, SDK, CLI, or live HTTP E2E/API test
  strategy.
- A local check, review, or design choice needs this specialty.

## Workflow

1. Read `AGENTS.md`, `docs/process/WORKPACKAGE_SYSTEM.md`,
   `docs/process/BOOKKEEPING.md`, the active workpackage YAML file, API
   architecture docs, and nearby route, contract, SDK, CLI, and test code.
2. Choose the smallest testing layer that proves the behavior:
   - In-process route tests: use Rust axum/tower-style router tests for route
     metadata, request context, idempotency, safe errors, and redaction.
   - Contract drift tests: use the repository-owned API contract package
     for OpenAPI parseability, route/operation drift, DTO examples, safe
     errors, and idempotency docs.
   - SDK correctness tests: use the API client unit/request tests for paths,
     auth/request-context headers, idempotency keys, pagination, safe error
     parsing, and SSE reconnect helpers.
   - CLI tests: use the public CLI tests for command mapping and output behavior.
   - Live HTTP E2E/API scenario tests: use Playwright `APIRequestContext` as
     the only live HTTP runner, with OpenAPI response-schema validation when
     the behavior needs durable storage, idempotency replay, pagination, safe
     error, or tenant-isolation assertions across multiple requests.
   - Container dependencies: use Testcontainers or Compose for real Postgres
     and substrate readiness when behavior depends on external services.
3. For user-facing SSE, include reconnect, `Last-Event-ID`, typed stream
   errors, redaction, and `public CLI watch ...` checks.
4. For public query collections and aggregates, add executable checks for
   canonical route uniqueness, production-router reachability, authorization
   metadata, least-privileged callers, cross-tenant isolation, explicit
   capability/version discovery, persisted or authoritatively computed fields,
   SQL resource scoping, and declared snapshot/freshness behavior.
   For authenticated context, exercise optional capability-evaluator failure
   and assert a successful core response with unavailable capability states;
   do not accept a 503 that makes a valid session look unauthenticated.
5. If a lightweight environment substitutes external dependencies, run the
   same Playwright API scenario against the production-shaped and lightweight
   compositions and compare results using only an explicit allowed-capability
   difference manifest.
6. Record the selected tool layer, why it applies, expected commands, skipped
   layers with reasons, and failure modes in the owning slice entry.
7. Pin any newly introduced CLI tool, Cargo crate, Docker image, or CI action
   before adding it to the repo or CI.

## Required Output

- Selected REST API testing layers and why they apply.
- Affected route, contract, SDK, CLI, Compose, or adapter files.
- Expected local checks and skipped test layers with reasons.
- Open questions and next slice needs.

## Guardrails

- Keep the repository-owned API contract package as the canonical
  OpenAPI/DTO contract owner.
- Keep the API client and the public CLI in the public API verification path for
  public behavior.
- Do not introduce a second live HTTP API scenario runner alongside
  Playwright.
- Do not use Playwright API tests to replace `api-contracts`,
  the API client, or the public CLI; use each layer for its assigned concern.
- Do not treat OpenAPI or generated SDK presence as proof that a production
  router exposes an operation.
- Do not let an administrative test persona stand in for the ordinary caller
  of a general context or overview route.
- Do not use 404 as a compatibility probe, accept duplicate collection
  semantics, or assert placeholder values as valid production projections.
- Do not create environment-specific expected product values; allowed
  core-versus-pack differences are external capability availability, not
  route, identity, policy, persistence, or DTO semantics.
- Do not add unpinned tools, images, actions, or dependencies.
- Do not broaden the slice beyond the workpackage acceptance criteria.

## Done Means

- Each public API slice has explicit route, contract, SDK, CLI, and Playwright
  live HTTP checks where applicable.
- Tool choices are recorded in the slice entry or current task.
- Required checks are named and results are recorded.
- The selected slice entry or current task can show what changed and what
  remains.
