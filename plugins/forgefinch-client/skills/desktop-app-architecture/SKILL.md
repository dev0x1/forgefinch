---
name: desktop-app-architecture
description: "Use for desktop product architecture: app lifecycle, windows, menus, tray, shortcuts, commands, deep links, file dialogs, file associations, preferences, and platform-specific behavior."
---

# desktop-app-architecture

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

## Purpose

Design the app like a real desktop product. Electron process boundaries remain strict, and every native capability is modeled as a typed command owned by the main process.

Use `electron-dev` with this skill for process-boundary, BrowserWindow, IPC, preload, and security details.

## Use this skill when

- adding or changing app startup, shutdown, single-instance behavior, windows, menus, tray, shortcuts, native dialogs, file flows, protocol handlers, or preferences
- deciding where a desktop feature belongs across main, preload, renderer, shared, domain, and storage layers
- adding platform-specific behavior for macOS, Windows, or Linux

## Non-negotiable rules

- Main process owns app lifecycle and every native OS capability.
- Main process owns local executor lifecycle and local API access when local
  executor work is selected.
- Renderer owns UI only. Renderer never imports Electron or Node modules.
- Preload exposes one narrow typed function per capability.
- Every user-visible desktop action is registered as a typed command.
- Every BrowserWindow has an explicit owner, route, preload, security options, lifecycle policy, and close/minimize policy.
- Every menu item, shortcut, tray item, and deep link maps to a command. Do not duplicate behavior across UI entry points.
- Every platform branch is explicit and tested or manually verified on the target platform.

## Required workflow

1. Write the desktop capability inventory: user action, local executor capability, process owner, command, IPC/local API contract, UI entry points, and tests.
2. Implement domain or service logic before connecting UI chrome.
3. Register command handlers in main and expose renderer-safe preload functions only when needed.
4. Add menu, tray, shortcut, or protocol entry points by dispatching commands, not duplicating logic.
5. Verify startup, focused-window, no-window, and shutdown behavior.

## Repo placement

- App lifecycle and native entry points belong in `<desktop-app-root>/src/main`.
- BrowserWindow ownership, window state, navigation policy, and close/minimize behavior belong in `<desktop-app-root>/src/main/window`.
- Menus, tray, shortcuts, dialogs, deep links, commands, and OS services belong in `<desktop-app-root>/src/main/services`.
- local executor lifecycle, loopback HTTP/SSE client behavior, and Local Executor event
  mapping belong in `<desktop-app-root>/src/main/services`; Rust executor code belongs in
  `<desktop-app-root>/native/local-executor/`.
- IPC contracts belong in `<desktop-app-root>/src/shared/ipc` and `<desktop-app-root>/src/shared/schemas`; handlers belong in `<desktop-app-root>/src/main/ipc/handlers`.
- Renderer entry points for desktop actions belong in `<desktop-app-root>/src/renderer/src/features` or `<desktop-app-root>/src/renderer/src/routes` and call narrow preload APIs.
- Electron E2E coverage belongs in `<desktop-app-root>/tests/e2e`.

## Patterns And Examples

- Boot sequence: acquire a single-instance lock before expensive initialization, initialize logging and storage before windows that need them, start or verify Local Executor readiness only from main when needed, register IPC before loading renderer routes, and deny navigation by default.
- Window lifecycle: create windows through `<desktop-app-root>/src/main/window`, track ownership, secure preferences, route, preload, close/minimize behavior, focus behavior, and cleanup on destroy.
- Commands: centralize desktop actions so menus, tray, shortcuts, IPC, deep links, and renderer UI dispatch the same behavior instead of duplicating logic.
- Native menus and tray: create them in main only, derive enabled state from app state, include standard Electron roles where appropriate, and dispatch typed commands for app-specific actions.
- Deep links and file flows: parse with standard APIs, allowlist shape and operation, queue until app readiness, and route valid payloads through commands/services after validation.
- Platform differences: keep `process.platform` checks in main-process helpers and note unsupported manual verification in the completion report.

Command example:

```ts
export type CommandId = 'app.openPreferences' | 'app.quit'

export type CommandDefinition = {
  readonly id: CommandId
  readonly label: string
  readonly accelerator?: string
  readonly canRun: () => boolean
  readonly run: () => Promise<void> | void
}
```

Window definition example:

```ts
const secureWebPreferences = {
  preload: preloadPath,
  nodeIntegration: false,
  contextIsolation: true,
  sandbox: true,
  webSecurity: true
} as const
```

## Required checks

- `pnpm typecheck`
- `pnpm lint`
- `pnpm test`
- `pnpm test:e2e`

## Completion report additions

Include the exact skill name `desktop-app-architecture`, changed files, commands run, tests added or changed, manual verification, and residual risk. Do not report a check as passed unless it actually ran and passed.
