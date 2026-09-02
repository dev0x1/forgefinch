---
name: accessibility-keyboard-ux
description: "Use for keyboard-first desktop UX, focus management, dialogs, menus, shortcuts, ARIA, landmarks, screen-reader behavior, accessibility tests, and custom interactive controls."
---

# accessibility-keyboard-ux

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

## Purpose

Make the app usable without a mouse and understandable to assistive technologies. Desktop UI must be keyboard-first, focus-safe, and semantically correct.

## Use this skill when

- adding dialogs, menus, dropdowns, popovers, command palettes, shortcuts, forms, navigation, custom controls, empty states, or error states
- fixing focus loss, keyboard traps, inaccessible labels, screen-reader issues, or unclear shortcut behavior

## Non-negotiable rules

- Every interactive element is keyboard reachable.
- Focus is always visible.
- Dialogs trap focus and restore focus to the invoker on close.
- Custom controls must implement the expected keyboard model.
- Icon-only buttons require accessible names.
- Shortcut actions must also be available through visible UI.
- Do not replace semantic HTML with ARIA unless native elements cannot express the control.

## Required workflow

1. Identify the interaction pattern and native HTML element that matches it.
2. Implement semantic markup, accessible names, focus behavior, and keyboard behavior before visual polish.
3. Add tests using user-visible queries and keyboard interactions.
4. Verify tab order, Escape behavior, Enter/Space activation, and focus restoration.
5. Document any intentional accessibility exception as residual risk.

## Repo placement

- Renderer UI accessibility belongs in `<desktop-app-root>/src/renderer/src/components` or `<desktop-app-root>/src/renderer/src/features/<feature>`.
- Component tests live beside the component and use Testing Library role/name queries.
- App-flow keyboard coverage belongs in `<desktop-app-root>/tests/e2e`.
- Native menus, global shortcuts, and OS-level accessibility behavior also require `desktop-app-architecture` and `electron-dev`.
- Keep accessibility exceptions in the completion report; do not hide them in comments.

## Patterns And Examples

- Keyboard audit: verify the flow works with Tab, Shift+Tab, Enter, Space, expected Arrow keys, and Escape.
- Focus management: move focus to the page heading or main content after route changes when needed, store and restore focus for temporary surfaces, and never remove focus outlines globally.
- Dialogs: provide a visible title or accessible label, trap focus for modal dialogs, close with Escape, and restore focus to the invoker.
- Menus: use native Electron menus for app-level menus; use ARIA menu roles only for real menu widgets, not ordinary navigation lists.
- Shortcuts: expose the action through visible UI, respect editable text fields, and use app-level shortcuts through desktop command/menu patterns.
- Labels and announcements: prefer visible labels, use `aria-describedby` for help/errors, use `role="status"` for non-urgent updates, and use `role="alert"` for urgent failures.

Testing examples:

```ts
await user.tab()
await user.keyboard('{Escape}')
expect(screen.getByRole('dialog', { name: 'Preferences' })).toHaveFocus()
expect(screen.getByRole('alert')).toHaveTextContent('Title is required')
```

## Required checks

- `pnpm typecheck`
- `pnpm lint`
- `pnpm test`
- `pnpm test:e2e`

## Completion report additions

Include the exact skill name `accessibility-keyboard-ux`, changed files, commands run, tests added or changed, manual verification, and residual risk. Do not report a check as passed unless it actually ran and passed.
