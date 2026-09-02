---
name: local-executor-runtime
description: "Use for local executor and local executor work in Electron applications: Local Executor architecture, Local Executor workspace placement, Electron main lifecycle ownership, loopback HTTP/SSE contracts, local action grants, renderer isolation, Local Executor diagnostics, crash isolation, and Rust verification."
---

# local executor Runtime

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

Use with `electron-dev`, `electron-security`, `privacy-secrets-permissions`,
`desktop-app-architecture`, `local-executor-rust`, `rust-crate-architecture`,
`rust-contract-testing`, and `testing` when local executor behavior
is planned, implemented, or reviewed.

## Non-Negotiable Rules

- The local executor is a local executor, not the canonical product backend.
- The governing rule is: backend API decides, the Local Executor executes,
  backend API records.
- Backend/cloud APIs own plans, runs, policy, approvals, audit, outputs, and
  durable product state.
- The Local Executor must not own or proxy backend API REST/SSE calls
  for plans, runs, approvals, audit logs, canonical outputs, workspace state,
  billing/usage, agent memory, team permissions, or other product truth.
- Electron main owns local executor startup, shutdown, restart policy, port discovery,
  ephemeral auth token handling, local HTTP client, and SSE client.
- Renderer code must never connect to Local Executor HTTP/SSE endpoints and must never
  receive the Local Executor port, auth token, raw logs, raw local paths, command
  lines, environment variables, secrets, or unredacted tool payloads.
- The local executor must bind to `127.0.0.1` only and reject unauthenticated access.
- local executor-backed actions require backend-backed scoped grants and visible user
  approval when policy requires approval.
- MVP Local Executor work must not add offline durable queues or local product state
  unless a later workpackage explicitly expands scope.

## Repo Placement

- local executor code belongs under `<desktop-app-root>/native/local-executor/`.
- Electron lifecycle and Local Executor client code belongs under `<desktop-app-root>/src/main/services`.
- Shared serializable contracts may live under `<desktop-app-root>/src/shared` only when safe for
  main, preload, renderer, and tests.
- Renderer features consume Local Executor-backed behavior only through typed app
  adapters or narrow preload APIs; do not import Local Executor clients into renderer.
- Prefer the preload namespace `desktopApi.local` once the app surface graduates
  from `window.electronAPI`. Keep it local-action-only; do not put backend API
  operations under this namespace.
- Rust tests live with Local Executor code. Electron E2E coverage lives in `<desktop-app-root>/tests/e2e`.

## Required Local API Shape

Use loopback HTTP plus SSE first:

- `GET /v1/health`
- `POST /v1/local-actions`
- `POST /v1/local-actions/{actionId}/cancel`
- `GET /v1/events`

Do not switch to WebSocket or gRPC without a workpackage decision covering
lifecycle, backpressure, cancellation, auth, packaging impact, and tests.

## Planning Checklist

Before implementation, define:

- Local Executor binary discovery and startup order
- loopback binding and port collision behavior
- ephemeral auth token generation, storage, and disposal
- health/readiness states
- local action request, response, cancellation, and SSE event schemas
- policy grant shape, expiration, and rejection cases
- whether renderer passes only an approved action reference or a sanitized
  action intent; do not expose raw grants, local paths, credentials, or policy
  internals to renderer state
- user approval requirements for each local action class
- event-to-platform reconciliation behavior
- diagnostics, redaction, support bundle, and crash isolation behavior
- Rust, TypeScript, security, and Electron E2E checks

## Modification Matrix

Use this matrix before editing to keep Rust, Electron, and platform-facing
contracts moving together:

| Change | Modify | Skills |
| --- | --- | --- |
| Rust crate/module layout | `<desktop-app-root>/native/local-executor/Cargo.toml`, `apps/**`, `crates/**` | `local-executor-rust`, `rust-crate-architecture` |
| Local HTTP/SSE DTO or safe error | `crates/contracts/local-executor-contracts`, route tests, Electron parser tests when consumed | `rust-contract-testing`, `local-executor-rust` |
| Local route behavior | `crates/interfaces/local-executor-api`, runtime tests, safe error mapping | `rust-contract-testing`, `local-executor-rust` |
| Runtime action/grant/cancel logic | `crates/domains/local-executor-runtime`, contract DTOs if shape changes | `local-executor-rust`, `rust-crate-architecture` |
| Electron startup/shutdown/supervision | `<desktop-app-root>/src/main/services`, main-process tests, Electron E2E if startup-visible | `electron-dev`, `electron-security`, `testing` |
| Electron Local Executor HTTP/SSE client | `<desktop-app-root>/src/main/services`, parser tests, redaction tests | `electron-dev`, `rust-contract-testing`, `privacy-secrets-permissions` |
| Renderer-visible status/progress | `<desktop-app-root>/src/shared`, preload, renderer feature code, component tests | `electron-dev`, `renderer-react`, `state-data-flow`, `testing` |
| New local action class | Rust runtime/contracts, Electron main adapter, platform grant/reconciliation docs, approval UI | `local-executor-runtime`, `local-executor-rust`, `rust-contract-testing`, `privacy-secrets-permissions` |
| Secrets, file/browser/tool payloads, diagnostics | Rust redaction, main-process redaction, support-bundle boundaries, denial tests | `privacy-secrets-permissions`, `electron-security`, `rust-contract-testing` |

## Implementation Workflow

1. Define or select the workpackage slice before adding Local Executor code.
2. Add Rust contracts and tests before wiring Electron main lifecycle code.
3. For contract changes, update Rust DTO/route coverage and Electron
   client/parser coverage in the same slice when Electron consumes the shape.
4. Keep Local Executor clients in main-process services; expose only renderer-safe
   derived state through existing Electron IPC/preload patterns when needed.
5. Keep platform-truth operations in TypeScript platform adapters/services, not
   in Rust Local Executor routes or preload local functions.
6. Validate every Local Executor request and event on both sides of the boundary.
7. Map Local Executor failures to stable user-safe error codes and log diagnostic
   detail only after redaction.
8. Reconcile action progress and results to platform-owned run/audit state.
9. Prove renderer isolation through tests or E2E checks.

Acceptable local preload shape:

```ts
desktopApi.local.getCapabilities()
desktopApi.local.executeApprovedAction(actionRef)
desktopApi.local.cancelAction(localActionRef)
desktopApi.local.subscribeStatus()
```

Do not add product-truth operations to the local namespace:

```ts
desktopApi.local.createRun()
desktopApi.local.approveRequest()
desktopApi.local.writeAuditEvent()
desktopApi.local.proxyPlatformRequest()
```

## Required Checks When local executor Code Changes

Run the checks that apply to touched files:

```bash
cargo fmt --all --manifest-path <desktop-app-root>/native/local-executor/Cargo.toml --check
cargo clippy --manifest-path <desktop-app-root>/native/local-executor/Cargo.toml --all-targets -- -D warnings
cargo test --manifest-path <desktop-app-root>/native/local-executor/Cargo.toml
pnpm typecheck
pnpm lint
pnpm test
pnpm test:e2e
pnpm security:electron
```

Do not report Cargo checks as passed unless the `<desktop-app-root>/native/local-executor/` workspace exists and
the command actually ran.
