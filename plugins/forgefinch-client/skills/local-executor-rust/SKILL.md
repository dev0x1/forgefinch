---
name: local-executor-rust
description: Use for Rust code, Cargo layout, async behavior, typed errors, tests, and idiomatic implementation in an Electron application's embedded local executor.
---

# Rust Development

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

Use this skill for Rust changes in the desktop application repo. It is narrowed
to the desktop Local Executor workspace.

## Scope

- Rust code lives under `<desktop-app-root>/native/local-executor/`.
- The Local Executor is a local execution node, not the backend/cloud API.
- Do not add Rust elsewhere in the desktop repo without a workpackage decision.
- Do not add path dependencies to the sibling backend project repository.

Use with:

- `local-executor-runtime` for Local Executor behavior and Electron ownership.
- `rust-crate-architecture` for workspace, crate, and dependency boundaries.
- `rust-contract-testing` for HTTP/SSE DTOs, route behavior, and safe errors.
- `testing` and `verification` for checks and completion evidence.

## Required Workflow

1. Read `AGENTS.md`, `agent-workflow`, `local-executor-runtime`, the active
   workpackage YAML/spec when present, and nearby Rust code/tests.
2. Confirm the selected slice, acceptance criteria, and process boundary before
   editing.
3. Keep Rust 2024, the pinned Rust toolchain, tracked `Cargo.lock`, and
   `#![forbid(unsafe_code)]`.
4. Keep app roots thin: `main.rs` is startup glue and `lib.rs` is crate docs,
   attributes, modules, and curated re-exports.
5. Prefer typed domain/API errors over stringly errors. Use `thiserror` for
   reusable library/domain/API error enums when it improves clarity. Use
   `anyhow` only for binary startup glue, top-level command orchestration,
   tests, or one-way context where the error is not part of a stable API.
6. Return safe error envelopes across local HTTP/SSE boundaries. Never expose
   secrets, raw local paths, authorization headers, environment variables,
   command lines, raw tool payloads, or stack traces.
7. Add or update tests close to the Rust behavior before claiming the slice is
   complete.
8. Keep the selected slice narrow; do not add generic tool execution, durable
   queues, platform persistence, or packaging unless the workpackage owns it.

## Rust Implementation Rules

- Validate every local action request before touching local resources.
- Model cancellation, readiness, policy denial, and dependency-unavailable
  states explicitly.
- Use `Result<T, E>` with stable error types for library boundaries.
- Avoid panics for runtime/user/input errors.
- Avoid global mutable state unless it is an intentional runtime registry with
  tests for concurrency and cancellation behavior.
- Keep async tasks cancellable or bounded; document any task that intentionally
  outlives a request.
- Keep fixtures semantic and safe, such as `local.noop`; do not introduce real
  file, browser, shell, or OS automation without grant and approval coverage.
- Keep generated artifacts out of source and clean `target/` after verification
  when it is not needed.

## Dependency Rules

- Pin reviewed stable Cargo versions and commit `Cargo.lock`.
- Prefer platform-aligned crates already chosen for the workspace.
- Do not add Postgres, SQLx, Restate, OPA/OpenFGA, Vault, object storage,
  durable queue, browser automation, shell execution, or generic tool runner
  dependencies unless a later workpackage explicitly expands scope.
- Before adding a Rust dependency, record why it is needed, which crate imports
  it, runtime/security impact, and the checks that prove it.

## Required Checks

Run when Rust code or manifests change:

```bash
cargo fmt --all --manifest-path <desktop-app-root>/native/local-executor/Cargo.toml --check
cargo clippy --manifest-path <desktop-app-root>/native/local-executor/Cargo.toml --all-targets -- -D warnings
cargo test --manifest-path <desktop-app-root>/native/local-executor/Cargo.toml
```

Also run `pnpm workpackages:check` when workpackage files change and `pnpm
lint` when docs or skills change.

## Done Means

- The selected Rust behavior is implemented or the review finding is explicit.
- Tests cover success, validation failure, safe error, cancellation, and
  relevant event behavior.
- The final report names Cargo checks that actually ran, skipped checks with
  reasons, and any remaining Electron integration work.
