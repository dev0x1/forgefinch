---
name: playwright-api-testing
description: Use for TypeScript Playwright APIRequest tests against a running HTTP API, especially OpenAPI-backed persistence, idempotency, tenant isolation, and safe error scenarios.
---

# playwright-api-testing

## Purpose

Write black-box HTTP API tests that call a running the backend server through
Playwright `APIRequestContext`, validate responses against the live OpenAPI
contract, and assert product behavior that only appears across real HTTP and
durable storage.

## Use This Skill When

- A slice needs live HTTP coverage beyond in-process Rust route tests.
- A public REST or SCIM scenario should prove persistence, idempotency,
  pagination, safe errors, or tenant isolation through the documented API.
- A local check, review, or design choice needs this specialty.

## Workflow

1. Read `AGENTS.md`, the active workpackage YAML file, the OpenAPI bundle from
   `OPENAPI_BUNDLE` or
   the repository-owned OpenAPI bundle, and the
   existing tests under `tests/http-api-playwright`.
2. Use `APIRequestContext`; do not add browser UI projects or browser
   downloads for API tests.
3. Gate live-server execution behind `BACKEND_HTTP_API_TESTS=1`; default
   runs may typecheck and list tests without requiring a running service.
4. Run `just test-http-api-playwright-check` when changing the Playwright
   package, helpers, tests, public API response schemas, or guidance that
   affects live HTTP API tests.
5. Run `just test-http-api-playwright` before completing a public API slice
   that changes behavior requiring a real HTTP boundary. The suite defaults to
   `the configured local backend URL`; set `BACKEND_API_BASE_URL=<url>` only when
   targeting a non-default API address.
6. Build requests from documented headers: authorization, tenant id, actor
   kind, actor id, correlation id, and idempotency key for commands.
7. Fetch the live OpenAPI document and validate successful JSON responses
   against the documented operation response schema before semantic assertions.
8. Keep scenarios stateful but isolated: generate unique ids/slugs, run workers
   serially when shared durable state is involved, and avoid assuming a clean
   database unless the check setup explicitly resets it.
9. Assert the application invariant directly: durable read-after-write,
   idempotent replay, cross-tenant denial or absence, pagination shape, safe
   error envelope, audit/evidence reference, or dependency-unavailable
   fail-closed behavior.
10. Do not run Playwright for changes limited to internal route logic,
   `api-contracts` contract truth, the API client request
   construction, the public CLI command formatting, or docs-only edits unless live
   HTTP product behavior changes too.
11. Record commands and required environment variables in the owning
   workpackage slice.

## Resource Operation Case Matrix

When covering a resource family, choose cases by operation shape and the
documented OpenAPI semantics. Keep endpoint-contract coverage in resource specs;
put cross-resource user journeys in scenario specs, which may belong to a
separate workpackage.

- `list`: valid default page, valid `page_limit`, invalid `page_limit`,
  invalid cursor, and tenant isolation for absent cross-tenant items.
- `get`: valid existing id, malformed id, unknown id, and cross-tenant access
  that denies or safely hides the resource without leaking details.
- `create`: valid minimal body, valid full body, missing required field,
  invalid enum or format, duplicate unique field, missing idempotency key for
  commands, same-key same-body replay, same-key different-body conflict, and
  forbidden actor.
- `patch` / `update`: valid mutable field change, immutable field rejection,
  invalid or empty patch, unknown id, idempotency replay/conflict for commands,
  and invalid state transitions such as archived or closed resources.
- `archive` / `delete` / action endpoints: valid state transition, repeated or
  already-transitioned state behavior, unknown id, idempotency replay/conflict
  for commands, and forbidden actor.
- SSE endpoints: valid connect, valid `Last-Event-ID`, unauthorized access,
  and tenant isolation for streamed events.

For broad OpenAPI coverage workpackages, keep a manifest that maps each
`operationId` to an owning resource spec and its covered case categories.
Live Playwright runs should fail for documented operations that are missing,
unimplemented, routed incorrectly, or returning bodies that do not match the
live OpenAPI response schema.

## Required Output

- Test file path and scenario purpose.
- OpenAPI operation ids covered.
- Required environment variables and service prerequisites.
- Local checks run or skipped with reasons.

## Guardrails

- Do not replace Rust route tests, `api-contracts`, the API client, or
  the public CLI coverage with Playwright.
- Do not mock the application's own public API in these tests.
- Do not store product truth or expected fixtures in process memory beyond
  per-test request-local values.
- Do not add unpinned npm dependencies or browser projects.
- Do not add another public API live HTTP scenario, smoke, or fuzzing runner;
  Playwright is the only live HTTP E2E/API scenario tool.

## Done Means

- The test calls a running service through public HTTP only.
- Successful JSON responses are checked against live OpenAPI schemas.
- Semantic assertions prove the user-visible invariant.
- The check is opt-in, documented, and reproducible from the package scripts
  or Justfile.
