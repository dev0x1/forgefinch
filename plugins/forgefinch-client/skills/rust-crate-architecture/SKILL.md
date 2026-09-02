---
name: rust-crate-architecture
description: Use for local executor Cargo workspace layout, crate boundaries, dependency direction, ports/adapters, and repo placement.
---

# Rust Crate Architecture

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

Use this skill when adding, moving, splitting, or reviewing Rust crates under
`<desktop-app-root>/native/local-executor/`.

## Workspace Shape

The desktop Rust workspace is intentionally small and follows a layered style:

```text
<desktop-app-root>/native/local-executor/
  Cargo.toml
  Cargo.lock
  rust-toolchain.toml
  apps/
    local-executor/
  crates/
    contracts/
      local-executor-contracts/
    domains/
      local-executor-runtime/
    interfaces/
      local-executor-api/
```

Allowed dependency direction:

```text
apps/local-executor -> crates/interfaces/local-executor-api
crates/interfaces/local-executor-api -> crates/domains/local-executor-runtime
crates/interfaces/local-executor-api -> crates/contracts/local-executor-contracts
crates/domains/local-executor-runtime -> crates/contracts/local-executor-contracts
crates/contracts/local-executor-contracts -> serde/time/error primitives only
```

Forbidden direction examples:

```text
crates/contracts/* -> crates/domains/*
crates/contracts/* -> crates/interfaces/*
crates/domains/* -> crates/interfaces/*
<desktop-app-root>/native/local-executor/* -> sibling backend repos
<desktop-app-root>/native/local-executor/* -> ../backend/*
<desktop-app-root>/src/renderer/* -> <desktop-app-root>/native/local-executor/*
```

## Crate Ownership

- `apps/local-executor`: CLI parsing, token-file config, startup,
  shutdown, listener binding, and top-level runtime glue.
- `crates/contracts/local-executor-contracts`: serializable DTOs, safe
  errors, event envelopes, examples, and compatibility tests for local HTTP/SSE
  contracts.
- `crates/domains/local-executor-runtime`: volatile action registry,
  cancellation state, grant validation, local action orchestration, and domain
  errors. It must not own HTTP routing, Electron lifecycle, durable product
  state, or platform/cloud truth.
- `crates/interfaces/local-executor-api`: axum routes, auth extraction,
  request/response mapping, SSE response wiring, timeout/trace middleware, and
  safe error mapping.
- `<desktop-app-root>/src/main/services`: Electron-side process lifecycle, loopback HTTP client,
  SSE client, auth token ownership, event reconciliation, and renderer-safe
  state.

## Ports And Adapters Rules

- Keep local resources behind narrow runtime traits before adding real browser,
  file, shell, indexing, or tool adapters.
- The domain/runtime crate may define traits for local capabilities; concrete
  OS/browser/tool implementations should live in focused runtime or adapter
  modules with tests and explicit grant checks.
- External systems are substrates, not canonical product state. Platform/cloud
  APIs own plans, runs, policy, approvals, audit, outputs, and durable state.
- Do not create crates just to satisfy a template. Add a crate only when it has
  a real boundary, test surface, and dependency reason.

## Placement Decision Table

| Change | Place |
| --- | --- |
| CLI flag, token-file config, startup line | `apps/local-executor` |
| Local HTTP/SSE DTO or safe error envelope | `crates/contracts/local-executor-contracts` |
| Action registry, grant validation, cancellation | `crates/domains/local-executor-runtime` |
| axum route, auth extractor, SSE response | `crates/interfaces/local-executor-api` |
| Electron process manager or local API client | `<desktop-app-root>/src/main/services` |
| Renderer-visible status/progress type | `<desktop-app-root>/src/shared` only if serializable and redacted |
| React display of progress/approval | `<desktop-app-root>/src/renderer` through preload/app adapters |

## Required Checks

Run when Rust layout, manifests, or dependencies change:

```bash
cargo fmt --all --manifest-path <desktop-app-root>/native/local-executor/Cargo.toml --check
cargo clippy --manifest-path <desktop-app-root>/native/local-executor/Cargo.toml --all-targets -- -D warnings
cargo test --manifest-path <desktop-app-root>/native/local-executor/Cargo.toml
```

Run `pnpm lint` after skill/doc changes and `pnpm workpackages:check` after
workpackage file changes.

## Done Means

- Dependency direction is preserved.
- New crates or modules have a clear owner and tests.
- Electron, renderer, platform, and Rust responsibilities remain separated.
