---
name: testing
description: Use for selecting, writing, fixing, or reviewing tests for React components, Electron IPC, preload, main process, storage, and Playwright E2E flows.
---

# Testing Workflow

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

Use for all test work and for any implementation that requires verification.

## Tool Decisions

- Pure functions: Vitest.
- React components: Vitest + React Testing Library.
- server-rendered web app unit and component tests: colocated under `<web-app-root>/src`.
- User interactions: `@testing-library/user-event`.
- Main-process services: Vitest with mocks or temp directories.
- local executor services: Cargo tests under `<desktop-app-root>/native/local-executor/`.
- local executor HTTP/SSE contracts: `rust-contract-testing` plus
  Rust axum/tower tests and Electron main parser tests when consumed.
- IPC handlers: Vitest with mocked `IpcMainInvokeEvent` and sender validation.
- Preload bridge: Vitest tests for exposed API shape.
- Electron E2E: Playwright under `<desktop-app-root>/tests/e2e`.

## Test Naming

Use behavior names:

```text
it('returns matching recipes for a trimmed query')
it('rejects invalid IPC payloads')
it('shows validation errors before saving')
```

Do not use vague names like `works`, `renders`, or `handles click`.

## Coverage Expectations

- New business logic: success, empty input, invalid input, failure path.
- New IPC: success, validation failure, sender rejection, service failure.
- New component: default state, user interaction, error/loading states where applicable.
- Bug fix: regression test that fails before the fix.
- Business logic files: 90% line coverage.
- IPC handlers: 100% branch coverage for validation and sender checks.
- Critical storage repositories: success and failure path coverage.
- local executor API and grant handling: success, invalid payload,
  unauthenticated request, denied/expired grant, cancellation, safe failure, and
  event emission coverage.

Coverage is a guardrail, not a substitute for meaningful tests. Reject high coverage with weak assertions.

## Component Tests

Required imports:

```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
```

Pattern:

```tsx
it('saves after the user enters a valid title', async () => {
  const user = userEvent.setup()
  const onSave = vi.fn()

  render(<RecipeForm onSave={onSave} />)

  await user.type(screen.getByLabelText('Recipe title'), 'Dal')
  await user.click(screen.getByRole('button', { name: 'Save recipe' }))

  expect(onSave).toHaveBeenCalledWith({ title: 'Dal' })
})
```

Rules:

- Query by role, label, text, or display value.
- Avoid snapshots.
- Avoid implementation details.
- Avoid `fireEvent`.

## IPC Handler Tests

Test cases for every IPC handler:

1. Valid payload returns expected result.
2. Invalid payload is rejected.
3. Untrusted sender is rejected.
4. Service failure returns or throws the documented safe error.

Mock event:

```ts
const trustedEvent = {
  senderFrame: { url: 'app://renderer/index.html' }
} as unknown as IpcMainInvokeEvent
```

Rules:

- Do not instantiate a real BrowserWindow in unit tests.
- Mock repositories and services.
- Validate Zod errors explicitly.
- Test sender validation before privileged service calls.

## Main Service Tests

Use temp directories and dependency injection.

Rules:

- Services receive filesystem paths, stores, database handles, or adapters through constructor parameters.
- Tests create temp resources and clean them up.
- Tests do not read or write the developer's real app data directory.
- Tests verify errors without depending on stack traces.

## local executor Tests

Use Cargo tests for local executor behavior and Vitest for Electron main-process
Local Executor clients.

Rules:

- Test `GET /v1/health`, `POST /v1/local-actions`,
  `POST /v1/local-actions/{actionId}/cancel`, and `GET /v1/events` once those
  endpoints exist.
- Cover loopback-only binding, ephemeral auth, invalid payloads, expired grants,
  denied grants, cancellation, event stream lifecycle, and safe errors.
- Do not test Local Executor behavior by letting renderer code call local endpoints.
- Do not depend on real user files, browser profiles, OS keychains, or the
  developer's real app data directory.

Layer ownership:

- Rust contract tests cover DTO serde, safe error envelopes, event envelopes,
  grant validation, and route behavior.
- Vitest covers Electron process management, HTTP/SSE client parsing, safe
  projection to shared/preload types, and dependency-unavailable states.
- Playwright Electron covers app startup, readiness, visible progress,
  cancellation, crash isolation, and renderer isolation only when those flows
  are user-visible.

## Preload Bridge Tests

Test exposed API shape.

Rules:

- The preload API exposes named functions only.
- The preload API does not expose `ipcRenderer`.
- The preload API does not expose generic `send`, `invoke`, `on`, or `removeListener` methods.
- Every exposed function maps to one channel.

Minimum assertion list:

```ts
expect(Object.keys(api).sort()).toEqual(['recipesSearch', 'settingsGet', 'settingsSet'].sort())
expect(api).not.toHaveProperty('ipcRenderer')
expect(api).not.toHaveProperty('invoke')
expect(api).not.toHaveProperty('send')
```

## Electron E2E

Place tests in `<desktop-app-root>/tests/e2e/*.spec.ts`.

Pattern:

```ts
import { test, expect, _electron as electron } from '@playwright/test'

test('app launches and shows the main window', async () => {
  const app = await electron.launch({ args: ['.'] })
  const window = await app.firstWindow()

  await expect(window.getByRole('heading', { name: 'Recipes' })).toBeVisible()

  await app.close()
})
```

Rules:

- Test complete user flows.
- Relaunch Electron after main, preload, startup, storage, or IPC changes.
- Do not disable Electron security settings for tests.
- Use stable accessible selectors.

Done when targeted tests pass, the relevant full test command is run before completion, the test proves user-visible or security-relevant behavior, and no test relies on arbitrary timeouts.
