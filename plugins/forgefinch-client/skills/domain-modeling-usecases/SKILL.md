---
name: domain-modeling-usecases
description: "Use for domain entities, value objects, use cases, repositories, ports/adapters, business rules, workflows, domain errors, and logic that must run without React or Electron."
---

# domain-modeling-usecases

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

## Purpose

Keep business logic independent from UI, Electron, storage drivers, and transport details. Domain code must be fast, deterministic, and testable with Vitest only.

## Use this skill when

- adding recipes, users, projects, permissions, workflows, calculations, search rules, parsing rules, or business validations
- moving logic out of React components, IPC handlers, storage adapters, or route loaders
- creating repositories, services, ports, adapters, state machines, or domain fixtures

## Non-negotiable rules

- Domain code imports no React, Electron, Node filesystem APIs, BrowserWindow APIs, IPC APIs, or database drivers.
- Use cases depend on ports/interfaces, not concrete adapters.
- Validation happens at boundaries; invariants are enforced by constructors or factory functions.
- Expected failures return typed result objects. Do not throw for normal business outcomes.
- Every use case has unit tests for success, validation failure, and at least one domain failure.
- Adapters translate external concerns into domain types and domain errors.

## Required workflow

1. Name the business capability and define its inputs, outputs, invariants, and error codes.
2. Create or update domain entities/value objects first.
3. Implement the use case against repository/service ports in the owning process or shared module.
4. Add adapters in main, renderer, or storage layers only after domain tests pass.
5. Connect IPC or UI last and keep it thin.

## Repo placement

- Put serializable cross-process contracts, result types, schemas, and pure shared vocabulary in `<desktop-app-root>/src/shared`.
- Put renderer-only product vocabulary and browser-safe helpers in `<desktop-app-root>/src/renderer/src/domain` or the owning `<desktop-app-root>/src/renderer/src/features/<feature>`.
- Put privileged use cases that coordinate storage, filesystem, shell, or OS services in `<desktop-app-root>/src/main/services`.
- Put durable repository interfaces and adapters in `<desktop-app-root>/src/main/storage` when they touch SQLite or persisted data.
- Do not invent `<desktop-app-root>/src/main/domain`, `<desktop-app-root>/src/main/usecases`, or `<desktop-app-root>/src/shared/domain` unless a feature creates enough domain code to justify that folder and `electron-dev` placement rules still hold.

## Patterns And Examples

- Entity/value object: model stable business concepts with readonly properties, explicit factories, enforced invariants, and separate serialization helpers.
- Use case: define input, output, error union, and injected ports before wiring IPC or UI.
- Repository port: name methods by business intent; do not expose SQL, table names, driver types, or storage exceptions through domain APIs.
- Result errors: expected failures return `{ ok: false, error: { code, message } }`; unknown infrastructure failures are mapped at adapters.
- Workflow state: prefer explicit state/event unions or transition functions over loose boolean combinations.
- Fixtures: use named builders with valid defaults and override only fields relevant to the test.
- Adapters: keep Electron, filesystem, database, and external API adapters in main/storage layers and translate data into domain types.

Result example:

```ts
export type Result<T, E extends { readonly code: string }> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly error: E }
```

Use case shape:

```ts
export async function createThing(
  repository: ThingRepositoryPort,
  input: CreateThingInput
): Promise<Result<void, CreateThingError>> {
  if (input.title.trim().length === 0) {
    return { ok: false, error: { code: 'VALIDATION_FAILED', message: 'Title is required.' } }
  }
  if (await repository.existsByTitle(input.title)) {
    return { ok: false, error: { code: 'ALREADY_EXISTS', message: 'That title already exists.' } }
  }
  await repository.create(input)
  return { ok: true, value: undefined }
}
```

## Required checks

- `pnpm typecheck`
- `pnpm lint`
- `pnpm test`

## Completion report additions

Include the exact skill name `domain-modeling-usecases`, changed files, commands run, tests added or changed, manual verification, and residual risk. Do not report a check as passed unless it actually ran and passed.
