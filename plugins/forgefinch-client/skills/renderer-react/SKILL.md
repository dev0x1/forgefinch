---
name: renderer-react
description: Use for React components in desktop application or server-rendered web app, including tests, accessibility, forms, styling, state boundaries, and runtime-safe imports.
---

# Renderer React Workflow

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

Use for new or changed React components in desktop, browser, or server-rendered
applications. Respect the owning runtime boundary and the repository's selected
router, state libraries, design system, and test stack.

## Component Structure

Reusable component:

```text
<desktop-app-root>/src/renderer/src/components/ComponentName/
  ComponentName.tsx
  ComponentName.test.tsx
  index.ts
```

Feature-specific component:

```text
<desktop-app-root>/src/renderer/src/features/<feature>/components/ComponentName/
  ComponentName.tsx
  ComponentName.test.tsx
  index.ts
```

server-rendered web app components follow the same colocated pattern under
`<web-app-root>/src/components` or
`<web-app-root>/src/features/<feature>/components`.

## Component Rules

- Use PascalCase component names.
- Use named exports only.
- Use `type ComponentNameProps = { ... }`.
- Do not use `React.FC`.
- Do not use default exports.
- Do not call IPC directly from presentational components.
- Client Components do not import Node or Electron modules. Server
  Components may import reviewed server-only BFF modules but never Electron,
  desktop IPC, or Local Executor code.
- Use the owning application's established design system and tokens. Do not
  introduce a second styling system without an explicit migration decision.
- Use semantic HTML before ARIA.
- Give every interactive element an accessible name.

## State Rules

- Local visual state stays inside the component.
- Shared renderer state uses Zustand.
- Electron desktop app server/async remote data uses the repository's selected
  query layer. A server-rendered web app uses
  Server Components/server-only adapters by default and client query state only
  for interactions that require it.
- In desktop application, native or persistent data access goes through `window.electronAPI` from a feature-level hook, not a presentational component.
- In server-rendered web app, authenticated remote data goes through server-only BFF
  adapters and reaches Client Components as validated view models. Never import
  desktop APIs or expose tokens through client data libraries.

## Accessibility

Required checks for every component:

- Buttons have accessible names.
- Inputs have labels.
- Dialogs have titles.
- Sections that need names use `aria-label` or visible headings.
- Loading states expose visible text.
- Error states expose visible text.
- Keyboard interaction works for custom controls.

Testing rule:

```ts
screen.getByRole('button', { name: 'Save recipe' })
screen.getByLabelText('Recipe title')
screen.getByRole('alert')
```

Use role/name queries first. Do not use `data-testid` unless no accessible query exists.

## Forms

Use React Hook Form + Zod.

Rules:

- Schema lives in `<desktop-app-root>/src/shared/schemas` when the payload crosses IPC.
- server-rendered web app request/response schemas live beside its feature or API boundary.
- Schema can live beside the component only when it is purely visual.
- Show validation errors with text connected to the input.
- Submit handlers call a feature hook, not raw IPC.

Required test cases:

1. Renders fields with accessible labels.
2. Blocks invalid submission.
3. Shows validation message.
4. Submits valid data once.

## New Component Generator

Use the reusable component generator when useful:

```bash
node <desktop-app-root>/scripts/create-component.mjs ComponentName
```

Then replace the starter implementation with the real component.

Manual component pattern:

```tsx
type ComponentNameProps = {
  title: string
}

export function ComponentName({ title }: ComponentNameProps): React.JSX.Element {
  return (
    <section aria-label={title} className="rounded-lg border p-4">
      <h2 className="text-lg font-semibold">{title}</h2>
    </section>
  )
}
```

Manual test pattern:

```tsx
import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { ComponentName } from './ComponentName'

describe('ComponentName', () => {
  it('renders an accessible section', () => {
    render(<ComponentName title="Example" />)
    expect(screen.getByRole('region', { name: 'Example' })).toBeInTheDocument()
  })
})
```

## Stateful Components

Rules:

1. Write a test for the user-visible state transition first.
2. Use `userEvent`, not `fireEvent`, for realistic interaction.
3. Keep state local unless another route or sibling feature needs it.
4. Move shared state to a feature store under the owning app's `src/features/<feature>/stores/`.
5. Keep persistent state out of client stores. Electron desktop app persists through main IPC; server-rendered web app persists through approved browser/API adapters.

Test pattern:

```tsx
const user = userEvent.setup()
render(<TogglePanel />)

await user.click(screen.getByRole('button', { name: 'Show details' }))
expect(screen.getByText('Details')).toBeInTheDocument()
```

## Component Review

Reject the change when any item is true:

- A Client Component imports `electron` or Node modules, or an server-rendered web app
  Server Component imports Electron, desktop IPC, or Local Executor code.
- server-rendered web app component imports desktop IPC, preload, or Local Executor code.
- Component calls `window.electronAPI` directly and is not a feature boundary hook/container.
- Component lacks tests.
- Test asserts class names instead of behavior.
- Interactive element lacks an accessible name.
- Props use `any`.
- Component uses default export.
- Component uses `React.FC`.

Done when the component has a test, the test uses user-visible behavior, the component exports through `index.ts`, accessibility names and roles are verified, and `pnpm test` or targeted Vitest command was run.
