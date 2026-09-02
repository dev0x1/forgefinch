---
name: observability-diagnostics
description: "Use for structured logging, crash reporting, approved telemetry providers, main-process errors, renderer error boundaries, diagnostics export, support bundles, log redaction, and production troubleshooting."
---

# observability-diagnostics

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

## Purpose

Make production failures diagnosable without leaking secrets. Logs, crashes, errors, and support bundles must be structured, redacted, and user-consented where required.

## Use this skill when

- adding logging, crash reports, diagnostics export, support bundles, telemetry, renderer error boundaries, main-process error handling, or production troubleshooting tools
- fixing bugs that require reliable logs or crash context

## Non-negotiable rules

- Logs are structured and level-based.
- Logs never contain secrets, tokens, passwords, cookies, raw authorization headers, or unredacted personal data.
- Crash reporting initializes in main before risky startup work when an approved provider exists.
- Do not add Sentry, telemetry, or crash-reporting dependencies without following `agent-workflow` dependency policy.
- Renderer failures are caught by React error boundaries and reported through approved channels.
- Diagnostics export requires explicit user action and redaction.
- Support bundles include app version, platform, recent logs, safe config, and error summaries only.

## Required workflow

1. Define what operational question must be answered.
2. Add structured events at boundaries and failure points.
3. Redact before persistence, upload, export, or renderer display.
4. Add tests for redaction and error mapping.
5. Verify logs and diagnostics in development; verify release/runtime packaging only when release scope applies.

## Repo placement

- Main-process logging, crash handling, support bundle creation, and diagnostics export belong in `<desktop-app-root>/src/main/services`.
- Redaction helpers that are safe and serializable can live in `<desktop-app-root>/src/shared`; Node/Electron-backed redaction or file collection stays in `<desktop-app-root>/src/main`.
- Renderer error boundaries belong under `<desktop-app-root>/src/renderer/src/app`, `<desktop-app-root>/src/renderer/src/routes`, or the owning feature.
- Tests for redaction and error mapping live beside the module; app-level diagnostics export flows belong in `<desktop-app-root>/tests/e2e`.
- Use `pnpm build` only when Electron build config or release/runtime packaging behavior changes.

## Patterns And Examples

- Structured logging: log event names and structured fields, include app version and process name when useful, and redact before writing.
- Main errors: install top-level main-process handlers when adding observability infrastructure, map expected service errors to typed results, and show user-safe fatal startup errors.
- Renderer error boundaries: wrap the app shell, routes, or feature boundaries; show actionable fallback UI; report sanitized details; do not swallow failures silently.
- Crash reporting: initialize approved providers early in main, set release/environment/sample rates explicitly, gate uploads when consent or policy requires it, and never attach secrets.
- Diagnostics export: require explicit user action, show what will be exported, include only safe app/version/platform/settings/log/error summaries, and write through a native save flow.
- Support bundles: include a manifest, redacted logs, bounded size, and exclude database files unless the product explicitly requires them with consent.
- Redaction: apply key and value pattern redaction recursively before persistence, upload, renderer display, or export.

Logger example:

```ts
type LogLevel = 'debug' | 'info' | 'warn' | 'error'
type LogFields = Record<string, unknown>

export function log(level: LogLevel, event: string, fields: LogFields, redact: (value: LogFields) => LogFields) {
  const entry = { timestamp: new Date().toISOString(), level, event, ...redact(fields) }
  console[level === 'debug' ? 'debug' : level](JSON.stringify(entry))
}
```

Error boundary fallback example:

```tsx
function ErrorFallback({ onRetry }: { readonly onRetry: () => void }) {
  return (
    <section role="alert">
      <h1>Something went wrong</h1>
      <button type="button" onClick={onRetry}>Try again</button>
    </section>
  )
}
```

## Required checks

- `pnpm typecheck`
- `pnpm lint`
- `pnpm test`

## Completion report additions

Include the exact skill name `observability-diagnostics`, changed files, commands run, tests added or changed, manual verification, and residual risk. Do not report a check as passed unless it actually ran and passed.
