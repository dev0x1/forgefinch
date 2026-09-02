---
name: state-data-flow
description: 'Use for Zustand stores, TanStack Query hooks, IPC-backed data fetching, cache invalidation, optimistic updates, async state, form state ownership, and duplicate-source-of-truth cleanup.'
---

# state-data-flow

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

## Purpose

Assign every piece of state to one owner. UI state, async resource state, form state, route state, persisted state, and main-process state must not duplicate each other.

## Use this skill when

- adding or modifying stores, hooks, query keys, cache invalidation, optimistic updates, background refresh, route search state, or IPC-backed data hooks
- fixing stale UI, duplicated state, loading/error confusion, or state sync bugs
- deciding whether data belongs in React state, Zustand, TanStack Query, React Hook Form, TanStack Router, SQLite, or electron-store

## Non-negotiable rules

- React local state owns ephemeral component-only UI state.
- Zustand owns shared client/UI state only. It does not own server, database, IPC, or persisted resource state.
- In Electron desktop app, TanStack Query owns asynchronous resource state, including IPC-backed data reads and mutations.
- React Hook Form owns in-progress form values and validation state.
- TanStack Router owns Electron desktop app navigation state; Next.js App Router owns Admin
  Center navigation state. Search params are validated in the owning boundary.
- Main-process repositories own persisted state.
- No duplicate source of truth. Derive, do not copy.

## Required workflow

1. Classify the state before coding: local UI, shared UI, async resource, form, route, or persisted.
2. Create query keys, store slices, or route search schemas before connecting components.
3. Write tests for loading, success, error, and invalidation behavior.
4. Keep hooks thin and components declarative.
5. Document invalidation and ownership in the changed files or completion report.

## Repo placement

- Feature hooks, query keys, mutations, and feature stores live under `<desktop-app-root>/src/renderer/src/features/<feature>`.
- server-rendered web app feature state and adapters live under its feature modules; App
  Router route state lives in the Next.js `app` tree when the repository has adopted that architecture.
- Reusable renderer hooks and stores live under `<desktop-app-root>/src/renderer/src/hooks` and `<desktop-app-root>/src/renderer/src/stores`.
- Route state belongs in `<desktop-app-root>/src/renderer/src/routes` through TanStack Router params/search validation.
- Persisted state belongs in `<desktop-app-root>/src/main/storage`; shared multi-window state is coordinated through main and typed preload events.
- IPC-backed reads and mutations use TanStack Query in renderer and validated handlers in main.
- server-rendered web app authenticated reads use Server Components/server-only adapters
  by default, and mutations use fixed Server Actions or route handlers.
  Client-side query state is limited to interactions that need it and never
  owns tokens, tenant authority, Electron IPC, or Local Executor access.

## Patterns And Examples

- State ownership matrix: classify every value as local UI, shared UI, async resource, form, route, persisted, or main-process shared state before coding.
- Zustand: use one small store per cohesive UI concern, store primitives/serializable UI state, expose actions, subscribe with selectors, and keep async resource fetching out.
- Query keys: use typed readonly tuple factories and include every variable that affects returned data; reuse keys for query, mutation invalidation, and prefetch.
- IPC-backed queries: expose narrow preload functions, wrap them in query functions, let TanStack Query own loading/error/retry/cache state, and map IPC result errors to UI-safe errors.
- Mutations and invalidation: identify affected keys, invalidate specific keys by default, update cache from returned data only when safe, and test stale-data scenarios.
- Optimistic updates: cancel affected queries, snapshot cache, apply minimal update, rollback exactly on error, and invalidate after settle.
- Background refresh: avoid polling by default, throttle or batch IPC refreshes, pause hidden-window work unless product requirements say otherwise, and surface sync status only when action is needed.
- Derived state: remove `useEffect` mirrors of props/query/route/form state; derive during render or memoize only expensive calculations.

Store example:

```ts
export const useSidebarStore = create<{
  readonly isOpen: boolean
  readonly toggle: () => void
}>((set) => ({
  isOpen: true,
  toggle: () => set((state) => ({ isOpen: !state.isOpen }))
}))
```

Query key example:

```ts
export const queryKeys = {
  runs: {
    all: ['runs'] as const,
    list: (filters: { readonly search: string }) => ['runs', 'list', filters] as const
  }
}
```

## Required checks

- `pnpm typecheck`
- `pnpm lint`
- `pnpm test`

## Completion report additions

Include the exact skill name `state-data-flow`, changed files, commands run, tests added or changed, manual verification, and residual risk. Do not report a check as passed unless it actually ran and passed.
