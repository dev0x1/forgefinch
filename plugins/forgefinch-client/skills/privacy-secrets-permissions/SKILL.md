---
name: privacy-secrets-permissions
description: "Use for safeStorage, token storage, secret handling, personal data classification, log redaction, file permissions, clipboard safety, external URL privacy, diagnostics consent, and permission boundaries."
---

# privacy-secrets-permissions

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

## Purpose

Protect user data by default. Secrets stay out of renderer, logs, support bundles, and repo files. File, clipboard, URL, diagnostics, and OS permission access require explicit boundaries.

## Use this skill when

- storing credentials, tokens, API keys, user identifiers, file paths, clipboard data, diagnostics, logs, URLs, or permission-protected OS data
- adding file access, external link opening, support export, settings sync, auth, or local secrets

## Non-negotiable rules

- Secrets are never stored in plaintext.
- Secrets are never logged, exported, or sent to renderer unless a narrow, documented product requirement requires it.
- Use Electron safeStorage or approved OS credential storage from main only.
- User files are accessed only after explicit user action or documented app-scoped permission.
- local executor tokens, grants, raw local paths, raw browser data, raw file
  contents, and tool payloads stay out of renderer state and logs.
- External URLs are allowlisted and opened from main only.
- Diagnostics export requires explicit user consent and redaction.
- Privacy-impacting changes include tests for redaction and permission denial.

## Required workflow

1. Classify the data: secret, personal data, file path, telemetry, diagnostic, or public data.
2. Choose the approved storage and access boundary.
3. Implement redaction before logging, export, upload, or renderer display.
4. Add tests for denied, invalid, and redacted cases.
5. Document user consent and residual privacy risk.

## Repo placement

- Secret storage, file permissions, clipboard access, shell/external URL opening, and diagnostics collection belong in `<desktop-app-root>/src/main/services` or `<desktop-app-root>/src/main/storage`.
- local executor auth tokens, local action grants, local file/browser/tool access, and
  Local Executor diagnostics are main/Local Executor concerns only; renderer receives
  redacted status and user-safe results.
- Renderer code receives only redacted, user-safe values through narrow preload APIs.
- Serializable privacy classifications and redaction result types can live in `<desktop-app-root>/src/shared`; Node/Electron-specific implementations stay in main.
- External URL policy must align with `electron-dev` and `electron-security`.
- Tests cover denied, invalid, redacted, and allowed cases.

## Patterns And Examples

- Secret storage: identify secret type/lifetime, encrypt through main-only `safeStorage` or approved credential storage, return capability status instead of raw secrets, and delete on sign-out/reset.
- safeStorage wrapper: check encryption availability before encrypting, handle corrupt data with typed errors, and do not expose `safeStorage` directly to IPC handlers.
- PII classification: mark fields as secret, personal, sensitive path, diagnostic, or public; limit retention; avoid collecting data that is not required.
- Redaction: redact by key and value pattern, handle nested arrays/objects, and run before logging, export, upload, or renderer display.
- File permissions: use native dialogs, validate path/extension/size/operation, avoid retaining broad directory access, and handle denied permission gracefully.
- local executor actions: require a platform-backed scoped grant, expire grants
  quickly, redact Local Executor events before persistence or renderer display, and
  reject missing, expired, malformed, or overbroad grants. Use `rust-contract-testing`
  when the redaction or safe error boundary crosses Local Executor HTTP/SSE.
- Clipboard: require user action for copy, never copy secrets automatically, and never log clipboard contents.
- External URLs: parse with `URL`, allowlist protocol/origin, strip tracking parameters only when product privacy rules require it, and reject file/javascript/data/custom protocols.
- Diagnostics consent: show exactly what diagnostics contain, require explicit confirmation, redact before writing, and let the user choose export location.

safeStorage result example:

```ts
export type SecretStorageError =
  | { readonly code: 'ENCRYPTION_UNAVAILABLE'; readonly message: string }
  | { readonly code: 'DECRYPTION_FAILED'; readonly message: string }
```

Redaction example:

```ts
const sensitiveKeyPattern = /(token|secret|password|cookie|authorization|email|path)/i

export function redact(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(redact)
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value).map(([key, nested]) => [
        key,
        sensitiveKeyPattern.test(key) ? '[REDACTED]' : redact(nested)
      ])
    )
  }
  return typeof value === 'string' && /Bearer\s+[A-Za-z0-9._-]+/.test(value) ? '[REDACTED]' : value
}
```

## Required checks

- `pnpm typecheck`
- `pnpm lint`
- `pnpm test`
- `pnpm security:electron`

## Completion report additions

Include the exact skill name `privacy-secrets-permissions`, changed files, commands run, tests added or changed, manual verification, and residual risk. Do not report a check as passed unless it actually ran and passed.
