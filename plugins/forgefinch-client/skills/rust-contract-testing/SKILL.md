---
name: rust-contract-testing
description: Use for local executor HTTP/SSE contracts, DTOs, safe errors, route tests, event compatibility, and client/parser coverage.
---

# Rust Contract Testing

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

Use this skill when a change touches Local Executor request/response DTOs,
safe errors, SSE event shapes, axum routes, auth behavior, or Electron
main-process parsing of Local Executor responses.

## Contract Ownership

The first Local Executor contract is loopback HTTP plus SSE:

- `GET /v1/health`
- `POST /v1/local-actions`
- `POST /v1/local-actions/{actionId}/cancel`
- `GET /v1/events`

Rust contract truth lives in
`<desktop-app-root>/native/local-executor/crates/contracts/local-executor-contracts`.
Route behavior lives in
`<desktop-app-root>/native/local-executor/crates/interfaces/local-executor-api`.
Electron client/parser behavior lives in `<desktop-app-root>/src/main/services`.

The renderer never consumes Local Executor HTTP/SSE contracts directly.

## Required Coverage By Change

| Change | Required coverage |
| --- | --- |
| DTO field or enum | serde round trip, unknown/invalid case if applicable, safe example |
| Safe error code | API mapping test, no secret/path/stack leakage assertion |
| Auth behavior | missing token, bad token, valid token route tests |
| Health endpoint | response shape and readiness/capability flags |
| Start action endpoint | valid `local.noop`, invalid payload, denied/expired grant |
| Cancel endpoint | idempotent cancel, unknown action, event emission |
| SSE event | event envelope shape, correlation ID, safe metadata |
| Electron client parser | success, safe error, malformed response, event parsing |

## Contract Rules

- Use stable, explicit DTOs. Avoid untyped `serde_json::Value` except for
  deliberately opaque sanitized action input fields.
- Include correlation IDs and local action IDs where needed for reconciliation.
- Keep platform/cloud run IDs, action references, and grants explicit, but do
  not make the Local Executor canonical for run state.
- Do not emit secrets, raw paths, cookies, authorization headers, process argv,
  environment variables, raw browser/file data, raw tool payloads, or stack
  traces in responses or events.
- Version or compatibility-impacting contract changes must update architecture
  docs, the active workpackage acceptance criteria, Rust route tests, and Electron parser tests
  in the same slice.

## Testing Layers

- Rust contract/unit tests prove DTOs, safe errors, grants, and event envelopes.
- Rust axum/tower tests prove local route behavior in-process.
- Vitest main-process tests prove Electron Local Executor client parsing,
  lifecycle state mapping, and renderer-safe projection.
- Playwright Electron tests prove startup/readiness/visible progress only when
  app startup or user-visible Local Executor flows change.

Do not use renderer code or Playwright page scripts to call Local Executor
loopback endpoints directly.

## Required Checks

Run when Rust contracts or route behavior change:

```bash
cargo fmt --all --manifest-path <desktop-app-root>/native/local-executor/Cargo.toml --check
cargo clippy --manifest-path <desktop-app-root>/native/local-executor/Cargo.toml --all-targets -- -D warnings
cargo test --manifest-path <desktop-app-root>/native/local-executor/Cargo.toml
```

Run `pnpm test` when Electron client/parser/preload/shared contract projection
changes. Run `pnpm security:electron` when preload, IPC,
navigation, CSP, or renderer isolation changes.

## Done Means

- Contract tests prove positive and negative behavior at the owning layer.
- Error and event assertions verify redaction and stable codes.
- Electron receives only parsed, renderer-safe state.
