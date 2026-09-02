---
name: type-system-quality
description: "Use for strict TypeScript, typed ESLint, IPC contracts, Zod schema boundaries, unsafe cast removal, discriminated unions, branded IDs, and type-level quality gates."
---

# type-system-quality

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

## Purpose

Make TypeScript a correctness system, not documentation. All runtime boundaries use Zod. All compile-time contracts are explicit. Unsafe code is isolated, named, reviewed, and tested.

## Use this skill when

- editing `tsconfig`, `eslint.config`, shared types, schemas, IPC contracts, domain models, repositories, hooks, or API clients
- fixing type errors, removing `any`, replacing unsafe casts, or tightening null and optional handling
- adding result types, domain errors, branded IDs, discriminated unions, or validation schemas

## Non-negotiable rules

- `strict: true`, `noImplicitOverride`, `noUncheckedIndexedAccess`, `noFallthroughCasesInSwitch`, and `forceConsistentCasingInFileNames` are mandatory in repo TypeScript configs.
- Add stricter options such as `exactOptionalPropertyTypes`, `useUnknownInCatchVariables`, and `noPropertyAccessFromIndexSignature` only through a focused type-hardening change that updates code and tests.
- Use `unknown`, validation, and narrowing. Do not use `any`.
- Do not use `as` casts to silence errors. A cast requires a named boundary function and a test.
- Use Zod at runtime boundaries: IPC, forms, file import, config, persisted data, and external service responses.
- Shared types under `<desktop-app-root>/src/shared` must be serializable and must not import Electron, Node, React, or browser-only modules.
- Generated shared API contracts under the repository's API client package remain runtime-neutral and must not own app credentials or session state.
- Errors crossing boundaries use discriminated unions. Do not throw raw strings.

## Required workflow

1. Identify the boundary being typed: internal compile-time code, runtime input, persistence, IPC, or UI props.
2. Add or update the narrowest type and the matching Zod schema when data crosses a boundary.
3. Replace broad object types with exact named types, readonly arrays, branded IDs, and discriminated unions.
4. Run targeted typecheck and tests before refactoring call sites.
5. Remove obsolete casts and delete dead types after the compiler confirms usage.

## Repo placement

- Shared serializable types live in `<desktop-app-root>/src/shared/types`, IPC contracts in `<desktop-app-root>/src/shared/ipc`, and runtime schemas in `<desktop-app-root>/src/shared/schemas`.
- Renderer prop and hook types live beside their component, hook, route, or feature.
- Main-process service, storage, and IPC handler types stay under `<desktop-app-root>/src/main`.
- Preload API types exposed to renderer belong in `<desktop-app-root>/src/renderer/src/types`.
- Do not introduce cross-process imports to share a type; move only serializable contracts into `<desktop-app-root>/src/shared`.
- server-rendered web app types and runtime schemas live beside its feature or API boundary under `<web-app-root>/src`; do not import Electron desktop app process contracts.

## Patterns And Examples

- Strict config: preserve the repo's current strict baseline; add extra strictness flags only in a focused hardening change that updates code and tests.
- No `any`: classify each `any` as boundary, legacy gap, or impossible type; use `unknown` plus Zod at boundaries and named exact types elsewhere.
- Safe catches: keep catch variables `unknown`, narrow with `instanceof Error` or helpers, log internal detail through approved logging, and return user-safe messages.
- Typed IPC: define one literal channel, derive request/response types from Zod schemas with `z.infer`, parse `unknown` in main, return typed results, and expose one preload function.
- Zod schemas: write schemas before duplicated manual types, use `.strict()` for trust boundaries, normalize optional/nullable/defaulted fields, and export parse helpers when repeated.
- Discriminated errors: use literal `code` fields, user-safe messages, and exhaustive handling in services/UI.
- Branded IDs: validate ID shape in constructors/parsers and never cast arbitrary strings to IDs outside those functions.
- Typed ESLint: type-aware linting should reject explicit `any`, floating promises, unsafe member access/assignment, and unnecessary assertions when those rules are enabled.

Result example:

```ts
export type Ok<T> = { readonly ok: true; readonly value: T }
export type Err<E extends { readonly code: string }> = { readonly ok: false; readonly error: E }
export type Result<T, E extends { readonly code: string }> = Ok<T> | Err<E>
```

Branded ID example:

```ts
type Brand<TValue, TBrand extends string> = TValue & { readonly __brand: TBrand }

export type RunId = Brand<string, 'RunId'>

export function toRunId(value: string): RunId {
  if (!/^run_[a-zA-Z0-9_-]+$/.test(value)) throw new Error('Invalid RunId')
  return value as RunId
}
```

## Required checks

- `pnpm typecheck`
- `pnpm lint`
- `pnpm test`

## Completion report additions

Include the exact skill name `type-system-quality`, changed files, commands run, tests added or changed, manual verification, and residual risk. Do not report a check as passed unless it actually ran and passed.
