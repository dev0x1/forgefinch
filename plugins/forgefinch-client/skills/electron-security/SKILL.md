---
name: electron-security
description: "Use for focused Electron security hardening and review: BrowserWindow webPreferences, preload APIs, IPC validation, sender checks, external URLs, navigation, CSP, storage boundaries, and dependency risk."
---

# Electron security

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

Use this skill before and after every change touching Electron main, preload, IPC, BrowserWindow, web contents, URLs, shell, storage, or dependencies. `electron-dev` remains the authoritative architecture skill; this skill is the focused security checklist.

## Non-negotiable BrowserWindow settings

```ts
webPreferences: {
  nodeIntegration: false,
  contextIsolation: true,
  sandbox: true,
  webSecurity: true,
  preload: preloadPath,
}
```

Do not override these values.

## Prohibited patterns

- `nodeIntegration: true`
- `contextIsolation: false`
- `sandbox: false`
- `webSecurity: false`
- `allowRunningInsecureContent: true`
- `enableRemoteModule: true`
- raw `ipcRenderer` exposure
- generic preload `send`, `invoke`, `on` wrappers
- renderer imports from `electron`
- renderer imports from Node built-ins
- renderer access to local executor loopback HTTP/SSE endpoints
- unvalidated `shell.openExternal`
- arbitrary navigation
- `<webview>`

## Required security checks

- Validate every IPC payload with Zod.
- Validate IPC sender origin.
- Deny all new windows unless an allowlist permits the URL.
- Deny navigation outside the app origin.
- Use a restrictive Content Security Policy.
- Keep secrets, tokens, and local paths out of renderer state.
- Keep Local Executor port, auth token, raw logs, raw local paths, and raw tool
  payloads out of renderer state.
- Bind Local Executor services to `127.0.0.1` only and require ephemeral auth on every
  request and stream.
- Run the repository's Electron security check before completion when one exists.

## Review checklist

- Review BrowserWindow construction in `<desktop-app-root>/src/main/window`.
- Review preload exposure in `<desktop-app-root>/src/preload/index.ts` and renderer types in `<desktop-app-root>/src/renderer/src/types`.
- Review IPC channels, validation, sender checks, and handlers under `<desktop-app-root>/src/main/ipc` and `<desktop-app-root>/src/shared`.
- Review external URL and navigation policy under `<desktop-app-root>/src/main/services` and `<desktop-app-root>/src/main/window`.
- Review renderer imports to ensure no Electron or Node modules enter `<desktop-app-root>/src/renderer`.
- Review dependency changes through `agent-workflow` before adding packages or native modules.
- Review Local Executor lifecycle, loopback binding, auth token handling, and renderer
  isolation with `local-executor-runtime` before adding local executor behavior.
- Review Local Executor HTTP/SSE DTOs, safe errors, and SSE event shape with
  `rust-contract-testing` when Electron parses or projects Local Executor data.

## Patterns And Examples

Secure BrowserWindow pattern:

```ts
const window = new BrowserWindow({
  show: false,
  webPreferences: {
    preload: preloadPath,
    nodeIntegration: false,
    contextIsolation: true,
    sandbox: true,
    webSecurity: true
  }
})

window.webContents.setWindowOpenHandler(() => ({ action: 'deny' }))
```

IPC handler pattern:

```ts
export function handleCapability(event: IpcMainInvokeEvent, input: unknown) {
  assertTrustedSender(event)
  const request = CapabilityRequestSchema.parse(input)
  return service.run(request)
}
```

External URL pattern:

```ts
const allowedOrigins = new Set(['https://docs.example.com'])
const url = new URL(input)
if (url.protocol !== 'https:' || !allowedOrigins.has(url.origin)) {
  return { ok: false, error: { code: 'URL_NOT_ALLOWED', message: 'That link cannot be opened.' } }
}
```

CSP baseline:

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none';" />
```

Preload pattern:

```ts
contextBridge.exposeInMainWorld('electronAPI', {
  openExternalUrl: (url: string) => ipcRenderer.invoke(IPC_CHANNELS.externalUrlOpen, { url })
})
```

## Done when

- Security validator passes.
- IPC has positive and negative tests.
- BrowserWindow settings remain secure.
- Renderer has no privileged imports.
- Renderer has no direct Local Executor local API access.
- Main/preload changes were verified by relaunching Electron.
