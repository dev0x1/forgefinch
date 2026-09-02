---
name: routing-navigation
description: Use for React or Next.js routes, layouts, validated parameters, guards, error boundaries, deep links, and navigation tests.
---

# routing-navigation

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

## Purpose

Keep navigation type-safe, URL state validated, layouts explicit, and route
components thin. Preserve the router already selected by the repository.

## Use this skill when

- adding screens, route files, nested layouts, search params, route params, route loaders, guarded routes, error boundaries, or navigation tests
- moving state from components into URL/search params
- fixing routing bugs or deep-link renderer behavior

## Non-negotiable rules

- Do not introduce a second router without an explicit migration decision.
- Every route param and search param is typed and validated.
- Route components compose feature components; they do not contain business logic.
- Layouts own shell structure, navigation landmarks, and shared loading/error UI.
- Electron route loaders fetch through approved query or preload APIs.
  Server-rendered pages and layouts fetch through server-only adapters.
- Route errors are handled by route-level error boundaries.

## Required workflow

1. Define route purpose, URL shape, params, search params, and layout ownership.
2. Add or update route file with typed validation.
3. Move feature behavior into feature components and hooks.
4. Add navigation tests for the visible user flow.
5. Verify direct load, in-app navigation, back/forward, and invalid URL behavior.

## Repo placement

- Route definitions live in `<desktop-app-root>/src/renderer/src/routes`.
- Route components compose app shell and feature components; product behavior lives in `<desktop-app-root>/src/renderer/src/features/<feature>`.
- Next.js App Router routes live in the `app` tree while product behavior stays
  in feature modules.
- Shared route helpers can live in `<desktop-app-root>/src/renderer/src/hooks` or `<desktop-app-root>/src/renderer/src/domain` when browser-safe.
- Route params and search schemas that also cross IPC belong in `<desktop-app-root>/src/shared/schemas`; renderer-only schemas can stay with routes.
- Component tests live beside route/feature code; critical navigation flows belong in `<desktop-app-root>/tests/e2e`.
- server-rendered web app route tests live beside its route or feature code; do not place web tests in the Electron E2E suite.

## Patterns And Examples

- Route definition: add Electron desktop app routes to its TanStack tree and server-rendered web app routes
  to its App Router tree; define params/search validation before feature behavior.
- Search params: validate with Zod or framework helpers, set defaults explicitly,
  update through owning router APIs, and do not mirror validated search params
  into Zustand.
- Layouts: keep shell structure, landmarks, shared loading/error UI, and focus targets in layout/app composition rather than duplicating shell markup across pages.
- Data loading: use approved TanStack Query/preload-backed functions in Electron desktop app and
  server-only BFF adapters in server-rendered web app; do not call raw IPC, expose tokens,
  or duplicate query logic in route code.
- Error boundaries: map known route errors to user-safe copy, provide retry/navigation recovery, and keep stack traces or secrets out of UI.
- Guards: implement allowed/rejected navigation explicitly, preserve intended destinations only when product flow requires it, and avoid protected content flashing before guards resolve.
- Tests: start from a real route, interact like a user, assert visible heading/landmark/state, and cover direct load, invalid URL/search, and back/forward when relevant.

Manual route tree example:

```tsx
const exampleRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/example',
  validateSearch: z.object({ q: z.string().catch('') }),
  component: ExampleScreen
})

const routeTree = rootRoute.addChildren([exampleRoute])
```

## Required checks

- `pnpm typecheck`
- `pnpm lint`
- `pnpm test`
- `pnpm test:e2e`

## Completion report additions

Include the exact skill name `routing-navigation`, changed files, commands run, tests added or changed, manual verification, and residual risk. Do not report a check as passed unless it actually ran and passed.
