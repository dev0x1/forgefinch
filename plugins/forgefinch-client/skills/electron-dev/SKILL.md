---
name: electron-dev
description: "Use for Electron desktop development: main/preload/renderer architecture, BrowserWindow lifecycle, IPC validation, storage boundaries, navigation policy, CSP, permissions, React integration, multi-window state, and Playwright verification."
---

# Electron Dev

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

Use before adding or changing Electron main, preload, IPC, BrowserWindow, storage, app lifecycle, native OS integration, desktop renderer integration, electron-vite config, or Electron E2E behavior.

This skill combines Electron architecture and security guidance. The repository's
existing stack, package scripts, and source layout stay authoritative; do not
introduce release tooling, a different build system, an alternate IPC framework,
or auto-update behavior unless the task explicitly owns that change.

Use focused companion skills when the change needs them: `desktop-app-architecture` for product-level desktop behavior, `electron-security` for hardening review, `local-executor-runtime` for local executor work, `local-executor-rust` and `rust-crate-architecture` for Local Executor Rust code, `rust-contract-testing` for Local Executor HTTP/SSE contracts, `local-data-storage` for SQLite/settings persistence, and `privacy-secrets-permissions` for secrets, personal data, file permissions, clipboard, URLs, and diagnostics consent.

## Quick Reference

| Category | Prefer | Avoid |
|----------|--------|-------|
| Security | `contextBridge.exposeInMainWorld()` with narrow functions | `nodeIntegration: true` |
| IPC | `invoke`/`handle` for request-response | `send`/`on` for request-response |
| Preload | Typed function wrappers | Exposing raw `ipcRenderer` |
| Build tool | electron-vite | Webpack or Vite-only Electron wiring |
| Release tooling | Defer until release work starts | Adding packaging/signing config during app scaffolding work |
| State | Zustand in renderer, `electron-store` in main | Redux or renderer-owned durable settings |
| Testing | Playwright Electron E2E | Spectron |
| Updates | Defer auto-update implementation until release scope | Renderer-driven or ad hoc update checks |
| CSP | Restrictive self-only policy, session-level when app-wide | No CSP or broad wildcards |
| Error handling | Serializable result objects with stable error codes | Raw `Error` objects across IPC |
| Multi-window | Main process as shared state hub | Direct window-to-window synchronization |

## Architecture Thinking Process

Use this loop before changing main, preload, renderer, storage, or window architecture:

1. Define the product capability: core user flow, privileged resources, target platform assumptions, offline needs, and data sensitivity.
2. Place each capability by process boundary: renderer for browser-safe UI, preload for narrow bridge functions, shared for serializable contracts, and main for privileged desktop work.
3. Design security first: least privilege, defense in depth, explicit IPC, sender validation, and Zod validation before privileged work.
4. Choose window, persistence, and test strategy together so state ownership, close behavior, and verification are clear before implementation.

Before editing, be able to state: "this change needs these system resources, this process owns them, the renderer receives only this typed API, and these tests prove the boundary."

## Structure Purpose

The app is split by Electron process boundary and responsibility. Each folder exists to make privileged code easy to audit, renderer code browser-safe, and shared contracts explicit.

```text
src/
  main/
    index.ts
    window/
    ipc/
      channels.ts
      register.ts
      validation.ts
      handlers/
    storage/
    services/
  preload/
    index.ts
  shared/
    ipc/
    schemas/
    types/
  renderer/
    index.html
    src/
      app/
      components/
      domain/
      features/
      hooks/
      mocks/
      routes/
      stores/
      styles/
tests/
  e2e/
scripts/
<desktop-app-root>/native/local-executor/
```

## Process Ownership

- `<desktop-app-root>/src/main` owns privileged desktop behavior: app lifecycle, windows, menus, tray, native dialogs, filesystem, database, settings, shell, clipboard, notifications, OS integration, and IPC handlers.
- `<desktop-app-root>/src/main/window` owns `BrowserWindow` construction, window state, navigation policy, and window lifecycle concerns.
- `<desktop-app-root>/src/main/ipc` owns channel names, handler registration, sender validation, and main-process IPC handlers.
- `<desktop-app-root>/src/main/storage` owns durable local storage, repositories, migrations, and storage adapters.
- `<desktop-app-root>/src/main/services` owns desktop services that coordinate Electron or OS APIs without becoming renderer UI.
- `<desktop-app-root>/src/main/services` also owns local executor lifecycle and loopback HTTP/SSE
  clients when Local Executor work is selected; renderer code never talks to the
  local executor directly.
- `<desktop-app-root>/src/preload` owns the typed `window.electronAPI` bridge and exposes narrow capability functions only.
- `<desktop-app-root>/src/shared` owns serializable request/response types, result types, stable error codes, and schemas safe for main, preload, renderer, and tests.
- `<desktop-app-root>/src/renderer` owns React UI, browser-safe state, routing, styles, and user interactions.
- `<desktop-app-root>/src/renderer/src/features` owns product feature screens, feature state, and feature-specific components.
- `<desktop-app-root>/src/renderer/src/components`, `hooks`, `stores`, `styles`, and `domain` own reusable browser-safe renderer code.
- `<desktop-app-root>/src/renderer/src/mocks` owns sample data for prototype UI, demos, and tests.
- `<desktop-app-root>/tests/e2e` owns Playwright Electron app flows.
- `<desktop-app-root>/native/local-executor/` owns local executor Rust code when a selected
  workpackage adds Local Executor implementation.

## Capability Placement Matrix

Use this matrix to keep architecture decisions consistent with the owning repository:

| Capability | Put it in | Guardrail |
|------------|-----------|-----------|
| UI rendering and browser-safe interactions | `<desktop-app-root>/src/renderer` | No Electron or Node imports. |
| Browser-safe async product data without secrets | Renderer hooks with TanStack Query | Keep dependencies browser-safe and schemas explicit. |
| backend API REST/SSE | TypeScript API adapters plus Electron main services when credentials or privileged config are needed | Use OpenAPI/SSE contracts; do not route backend API calls through the Local Executor, the API client, or the public CLI. |
| Filesystem, shell, native dialogs, clipboard, notifications, OS integration | `<desktop-app-root>/src/main/services` plus IPC handlers | Require user intent, sender validation, and Zod-validated input. |
| Local Executor execution | Rust code under `<desktop-app-root>/native/local-executor/` plus Electron main services | Bind to loopback only, require ephemeral auth, and keep platform/cloud canonical. |
| Local Executor readiness/progress UI | `<desktop-app-root>/src/main/services` -> `<desktop-app-root>/src/shared` -> preload -> renderer feature | Renderer receives only redacted derived state. |
| Privileged or secret-bearing network calls | `<desktop-app-root>/src/main/services` | Do not leak tokens, headers, local paths, or stack traces to renderer. |
| Preferences, small settings, and window state | `<desktop-app-root>/src/main/storage` or `<desktop-app-root>/src/main/window` | Use `electron-store` through allowlisted, validated accessors. |
| Queryable durable domain data | `<desktop-app-root>/src/main/storage` repositories | Use SQLite behind typed repository APIs and migrations. |
| Credentials, private keys, and sensitive crypto | Main process only after explicit design | Do not store credentials in plain files or add native credential dependencies without dependency review. |
| Serializable IPC contracts and schemas | `<desktop-app-root>/src/shared` | Keep shared code free of Electron, Node, React, and browser globals. |
| Shared multi-window state | Main process hub | Broadcast typed events through preload APIs that return cleanup functions. |

## Placement Checklist

Before adding or moving code, answer these questions:

1. Does this code need Electron, Node, filesystem, database, shell, clipboard, notification, or OS access? Put it in `<desktop-app-root>/src/main`.
2. Does this code implement local executor behavior? Put Rust code
   under `<desktop-app-root>/native/local-executor/` and Electron lifecycle/client code under
   `<desktop-app-root>/src/main/services`.
3. Does the renderer need a privileged capability? Add a narrow IPC route, expose one typed preload function, and validate input with Zod in the main process.
4. Is it a serializable request, response, schema, result, or shared type? Put it in `<desktop-app-root>/src/shared`.
5. Is it UI, browser-safe state, routing, or user interaction? Put it in `<desktop-app-root>/src/renderer`.
6. Is it reusable across renderer features? Put it in `<desktop-app-root>/src/renderer/src/components`, `hooks`, `stores`, `styles`, or `domain`.
7. Is it owned by one product screen or workflow? Put it under `<desktop-app-root>/src/renderer/src/features/<feature>`.
8. Is it one-time setup, package-copy material, generated starter material, or generated output? Keep it out of source after it has served its purpose.

## Boundary Rules

- Renderer code must not import `electron`, `fs`, `path`, `child_process`, `worker_threads`, `os`, `net`, or other Node-only modules.
- Renderer code must not connect to local executor loopback HTTP/SSE endpoints or
  receive the Local Executor port, auth token, raw logs, local paths, or tool payloads.
- Shared code must not import Electron, Node runtime modules, React components, or browser globals.
- Preload code must not expose raw `ipcRenderer` or generic `send`, `invoke`, or `on` wrappers.
- Main-process IPC handlers must validate sender origin and payloads before privileged work.
- Feature UI should depend on typed renderer services or `window.electronAPI`, not on main-process modules.
- Keep tests near the behavior they protect: unit/component tests beside source files, Electron flows in `<desktop-app-root>/tests/e2e`.
- Keep mock/demo data separate from runtime services.
- Prefer explicit modules over clever cross-folder abstractions.
- Add shared contracts before wiring IPC.
- Put feature-specific code with the feature until reuse is real.

## Electron And Local Executor Workflow

Use this rule: backend API decides, the Local Executor executes, backend API records.

Use this flow for any desktop feature backed by the local executor:

```text
Renderer UI
  -> narrow preload API
  -> Electron main IPC handler/service
  -> Electron main Local Executor HTTP/SSE client
  -> local executor loopback API
  -> backend/cloud reconciliation for canonical run/audit truth
```

Never use:

```text
Renderer UI -> 127.0.0.1 Local Executor HTTP/SSE
Renderer UI -> Rust Local Executor -> backend API REST/SSE
```

What changes when:

| Need | Modify |
| --- | --- |
| Start/stop/supervise the Local Executor process | `<desktop-app-root>/src/main/services`, main-process tests, `<desktop-app-root>/tests/e2e` when startup behavior is visible |
| Change the local HTTP/SSE wire shape | Rust contracts/API tests and Electron main parser tests in the same slice |
| Add renderer status or progress | `<desktop-app-root>/src/shared` redacted types, preload API, renderer feature state/UI, component tests |
| Add a new local action | Rust runtime/contracts, Electron main action adapter, backend grant/reconciliation behavior, approval/progress UI |
| Add file/browser/tool access | grant validation, explicit user approval, redaction, privacy tests, security validator, and E2E when user-visible |

Do not add the Local Executor loopback origin to renderer CSP `connect-src`.
Electron main owns all Local Executor HTTP/SSE communication.

When adding a Local Executor preload surface, prefer a local-action namespace
such as `desktopApi.local` once the app graduates from `window.electronAPI`:

```ts
desktopApi.local.getCapabilities()
desktopApi.local.executeApprovedAction(actionRef)
desktopApi.local.cancelAction(localActionRef)
desktopApi.local.subscribeStatus()
```

Do not put canonical product operations in that namespace:

```ts
desktopApi.local.createRun()
desktopApi.local.approveRequest()
desktopApi.local.writeAuditEvent()
desktopApi.local.proxyApiRequest()
```

## Electron And backend API Workflow

Use this flow for live backend API data:

```text
Renderer UI
  -> typed renderer adapter / TanStack Query hook
  -> narrow preload API when credentials or privileged config are needed
  -> Electron main API service
  -> TypeScript OpenAPI/SSE client
  -> backend API REST/SSE
```

Rules:

- backend API integration is TypeScript/OpenAPI/SSE, not Rust Local Executor.
- Credential-bearing transport, backend URL config, token injection, and SSE
  lifecycle belong behind Electron main/preload.
- Renderer code does not import raw generated transport clients, raw API
  DTOs, or raw EventSource/fetch helpers into route components.
- the public CLI and Rust the API client may be references for public transport
  semantics, but they are not the desktop end-user API path.
- Browser-safe API reads may start in renderer adapters/hooks, but token,
  backend URL, privileged header, idempotency, or SSE lifecycle concerns must
  cross preload into Electron main before reaching the backend API.
- Missing backend operations become recorded backend API gaps or explicit
  fixture-only behavior, not desktop-owned backend truth.

## BrowserWindow And Navigation

Every `BrowserWindow` must keep these settings:

```ts
webPreferences: {
  preload: preloadPath,
  nodeIntegration: false,
  contextIsolation: true,
  sandbox: true,
  webSecurity: true
}
```

Hardening checklist:

- Deny new windows by default with `setWindowOpenHandler`.
- Deny navigation by default; allow only app-owned origins.
- Do not load `http://` content.
- Do not open DevTools automatically in production.
- Do not enable `enableRemoteModule`.
- Do not enable `allowRunningInsecureContent`, `experimentalFeatures`, `nodeIntegrationInWorker`, or `nodeIntegrationInSubFrames`.
- Keep `<webview>` disabled unless a future feature explicitly justifies and tests it.
- Prefer app-wide navigation and window policy helpers under `<desktop-app-root>/src/main/window`.

Window strategy checklist:

- Default to one main application window until a product flow proves another window type is needed.
- For multi-window features, keep shared state in main and give each window a typed role, lifecycle owner, and permission profile.
- Define close and quit behavior deliberately: destroy, hide, restore, or persist window state.
- Route deep links and protocol handling through main-process policy, never directly through renderer strings.
- Give each window type its own reviewed `webPreferences`, preload API surface, and navigation rules.

## IPC Workflow

One user capability equals one narrow preload function. One preload function maps to one IPC channel.

Before adding a channel, decide the initiator, direction, payload schema, result type, error codes, sender trust rule, and tests. Use `invoke`/`handle` for request-response. Add event subscriptions only when main needs to push state, and make every `on*` preload API return an unsubscribe function. Reserve bidirectional streams for explicit future designs with cancellation, backpressure, and lifecycle cleanup.

Add IPC files in this order:

```text
<desktop-app-root>/src/main/ipc/channels.ts
<desktop-app-root>/src/shared/ipc/<capability>.ts
<desktop-app-root>/src/shared/schemas/<capability>.schema.ts
<desktop-app-root>/src/main/ipc/handlers/<capability>.handler.ts
<desktop-app-root>/src/main/ipc/register.ts
<desktop-app-root>/src/preload/index.ts
<desktop-app-root>/src/renderer/src/types/electron-api.d.ts
```

Rules:

- Add a literal channel name in `<desktop-app-root>/src/main/ipc/channels.ts`.
- Add request and response types in `<desktop-app-root>/src/shared/ipc/`.
- Add a Zod request schema in `<desktop-app-root>/src/shared/schemas/`.
- Treat every renderer-provided payload as `unknown` until Zod validates it.
- Validate `event.senderFrame.url` or equivalent trusted origin before privileged work.
- Register the handler in `<desktop-app-root>/src/main/ipc/register.ts`.
- Expose one named preload function in `<desktop-app-root>/src/preload/index.ts`.
- Use `window.electronAPI.<capability>()` from renderer code.
- Add tests for success, validation failure, sender rejection, and handler failure.
- Return serializable results only; never return raw `Error` objects or stack traces to the renderer.
- Use stable error codes and user-safe messages for recoverable failures; log diagnostic detail in main only.
- Require confirmation, rate limiting, cancellation, or progress reporting when an IPC capability is expensive, destructive, long-running, or sensitive.

## Preload API

Use `contextBridge` with narrow functions:

```ts
const electronAPI = {
  getAppInfo: () => ipcRenderer.invoke(IPC_CHANNELS.appInfoGet),
  openExternalUrl: (url: string) => ipcRenderer.invoke(IPC_CHANNELS.externalUrlOpen, { url })
}

contextBridge.exposeInMainWorld('electronAPI', electronAPI)
```

Preload rules:

- Do not expose `ipcRenderer`.
- Do not expose generic `send`, `invoke`, `on`, `off`, or `removeListener` wrappers.
- Each function maps to a specific channel.
- Every `on*` subscription API must return an unsubscribe function.
- Keep preload free of filesystem, shell, database, and native OS behavior; route privileged work to main.

## URLs, CSP, And Permissions

- Open external URLs only through a main-process allowlist.
- Accept only `https:` external URLs unless a future feature explicitly justifies another protocol.
- Do not accept `javascript:`, `file:`, `data:`, `http:`, or custom protocols from renderer input.
- Do not concatenate URLs or pass renderer strings directly to `shell.openExternal`.
- Do not add Local Executor loopback origins to renderer `connect-src`; Electron main
  owns Local Executor HTTP/SSE communication.
- Keep renderer CSP restrictive: self-only scripts, no `unsafe-eval`, no objects, self base URI, and explicit `connect-src` origins only when a feature requires them.
- Prefer session-level CSP and permission handlers when implementing app-wide policy; meta CSP is acceptable for the current renderer shell until central policy is needed.
- Deny Chromium permission requests by default and allow only explicit origin-plus-permission pairs.

## Settings, Storage, And Multi-Window State

- Use `electron-store` from the main process only for settings, preferences, and small durable config.
- Use SQLite repositories under `<desktop-app-root>/src/main/storage` for queryable durable domain data.
- Validate setting keys against an allowlist and setting values with Zod.
- Do not expose store objects, database handles, file paths, SQL strings, or stack traces through preload.
- Treat the main process as the state hub for shared multi-window state.
- Do not sync windows directly with each other; mutate shared state through main, persist if needed, then broadcast typed events through preload APIs that return cleanup functions.
- Before adding persistence, decide what data persists, how sensitive it is, whether it needs migration, and whether users need backup, export, or deletion support.
- Keep sensitive data out of plain files. Add secure credential storage only through an explicit dependency review and main-process-only design.

## React Renderer Integration

- Keep React components browser-safe.
- Keep presentational components free of IPC and storage calls.
- Put privileged calls in feature boundary hooks or containers that call `window.electronAPI`.
- Use React StrictMode to catch effect cleanup bugs.
- Any component that subscribes to preload `on*` APIs must return the unsubscribe function from its effect cleanup.
- Use desktop shell and feature-level error boundaries when a renderer failure should not blank the whole app.
- Use TanStack Router, TanStack Query, Zustand, React Hook Form, Zod, Tailwind, and Lucide according to `agent-workflow`.

## electron-vite Review

- Keep electron-vite as the only Electron build tool.
- Main and preload builds must preserve Electron and Node process boundaries.
- Renderer aliases must point only to browser-safe renderer code or `<desktop-app-root>/src/shared`.
- Keep native modules and Node built-ins out of the renderer bundle.
- Do not add Webpack, Vite-only Electron wiring, alternate Electron build tools, packaging scripts, or starter generators.

## Playwright Electron Review

- Place Electron E2E tests under `<desktop-app-root>/tests/e2e`.
- Launch the app through Playwright's Electron support and close it in cleanup.
- Use accessible selectors for renderer assertions.
- Add E2E coverage when UI, main, preload, startup, routing, storage, or IPC behavior changes.
- When useful, evaluate BrowserWindow settings from the main process in E2E to verify `contextIsolation`, `sandbox`, and navigation assumptions.
- Do not weaken Electron security settings for tests.
- Cover main-process business logic with Vitest, IPC handlers with mocked sender frames, preload API shape with bridge tests, and critical desktop flows with Playwright.
- Add platform-specific tests only when behavior truly differs by OS.

## Common Anti-Patterns

| Anti-pattern | Problem | Repo rule |
|--------------|---------|-----------|
| `nodeIntegration: true` | XSS can escalate to privileged code execution. | Keep Node integration disabled. |
| Exposing `ipcRenderer` directly | Renderer gains broad IPC access. | Wrap each capability in `contextBridge` functions. |
| Missing `contextIsolation` | Renderer code can reach preload scope. | Keep context isolation enabled. |
| BrowserWindow without sandbox | Preload has broader Node access. | Keep sandbox enabled. |
| Unvalidated IPC arguments | Renderer input can become injection or confused-deputy risk. | Validate payloads with Zod in main. |
| Missing sender validation | Untrusted frames can invoke privileged handlers. | Validate sender origin before service calls. |
| Binding local services to `0.0.0.0` | Local development services become network-exposed. | Bind local-only services to `127.0.0.1` unless explicitly required. |
| Renderer connects to the local executor | Renderer can bypass main-process policy and leak local credentials or paths. | Route local executor access through Electron main services and typed renderer-safe APIs. |
| Unauthenticated Local Executor API | Other local processes can drive privileged actions. | Require an Electron-main-held ephemeral token on every Local Executor request and stream. |
| Missing CSP | Renderer script injection is easier. | Keep restrictive CSP and avoid `unsafe-eval`. |
| Raw errors across IPC | Error metadata is lost and stacks leak or mislead. | Return serializable result objects and stable error codes. |
| Direct window-to-window state sync | Multi-window state becomes race-prone and hard to audit. | Route shared state through main. |
| Deprecated Electron E2E tooling | Old tools lag modern Electron security/runtime behavior. | Use Playwright Electron. |
| Release work without a signing/update plan | Users can hit OS trust warnings or unsafe update paths later. | Keep release tooling out for now, then handle signing, distribution, and updates together in release scope. |

## Security Review

Run when Electron code changes:

```bash
pnpm security:electron
pnpm typecheck
pnpm test
```

Also run `pnpm test:e2e` when UI, main, preload, routing, app startup, IPC, or Local Executor lifecycle behavior changes. Reject changes with insecure BrowserWindow settings, missing sender validation, missing Zod validation, raw IPC exposure, renderer Electron imports, renderer local executor access, unauthenticated Local Executor requests, unallowlisted external URLs, unrestricted navigation, uncleaned IPC listeners, or new native dependencies without justification.

## Troubleshooting Checks

- `require is not defined`: expected in renderer. Keep Node integration disabled and expose only the needed capability through preload.
- `window.electronAPI` is missing: verify the preload path, `contextIsolation: true`, the `contextBridge.exposeInMainWorld` name, and `<desktop-app-root>/src/renderer/src/types/electron-api.d.ts`.
- IPC handler is not reached: verify channel constants match, handlers register before the window loads, sender validation is not rejecting the app origin, and async request-response flows use `invoke`/`handle`.
