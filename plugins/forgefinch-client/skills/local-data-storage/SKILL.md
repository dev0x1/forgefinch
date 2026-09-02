---
name: local-data-storage
description: "Use for SQLite, better-sqlite3, migrations, repositories, transactions, backups, imports, exports, settings, native module rebuilds, and local persistence tests."
---

# local-data-storage

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

## Purpose

Persist domain data safely in the main process. `better-sqlite3` is the required domain persistence dependency. `electron-store` is limited to small settings and preferences. Do not introduce Drizzle or another ORM unless a dependency-change task explicitly approves it.

## Use this skill when

- adding database tables, migrations, repositories, transactions, backup/restore, import/export, settings persistence, or local data tests
- changing `better-sqlite3`, native module rebuilds, or app storage paths
- deciding whether data belongs in SQLite, electron-store, cache, route state, or renderer state

## Non-negotiable rules

- Database access happens in the main process only.
- Renderer never opens SQLite, never receives raw SQL, and never controls arbitrary query strings.
- Use named repository functions around `better-sqlite3`; keep raw SQL inside main-process storage modules with tests.
- Every schema change has a migration.
- Every repository has tests against an isolated test database.
- Every destructive operation has transaction safety and recovery behavior.
- Settings in electron-store must be schema-validated and small. Domain collections belong in SQLite.

## Required workflow

1. Classify the data: preference, domain record, cache, import/export payload, or temporary UI state.
2. Create or update schema and migration before repository behavior.
3. Write repository tests against a temporary database.
4. Expose data to renderer through typed use cases and IPC only.
5. Verify runtime migration and app data path behavior when storage config changes.

## Repo placement

- SQLite connections, migrations, repositories, transactions, import/export, backup/restore, and settings adapters live under `<desktop-app-root>/src/main/storage`.
- Storage orchestration that coordinates OS or app services can live under `<desktop-app-root>/src/main/services`.
- Serializable request/response types live in `<desktop-app-root>/src/shared/ipc`; runtime validation schemas live in `<desktop-app-root>/src/shared/schemas`.
- Renderer data access goes through TanStack Query hooks and narrow preload APIs; it never receives database handles, SQL strings, or arbitrary file paths.
- Use `pnpm build` only when native module handling, Electron build config, or storage path behavior changes.

## Patterns And Examples

- Main-only SQLite: open database handles in main, expose business operations through repositories/services, validate IPC before repository calls, and return serializable DTOs.
- Schema/migrations: keep schema SQL and migrations reviewed together; do not ship schema-only changes; never edit an applied production migration.
- Runtime migrations: run before UI routes need data, prevent concurrent migration, back up before destructive migrations, and fail with a user-safe error if migration cannot complete.
- Repository pattern: one repository per cohesive data area, business-named methods, prepared statements, DTO/domain mapping, and typed constraint errors.
- Transactions: wrap multi-write operations in `better-sqlite3` transactions, keep network/UI work outside transactions, and test rollback.
- Backup/restore: validate backups in a temporary database before replacing active data; never overwrite active data until validation passes.
- Import/export: use native dialogs from main, validate extension/size/schema, import in transactions, and redact secrets on export.
- Native modules: keep `better-sqlite3` out of renderer bundles and run `pnpm build` after Electron or native module changes.

Repository example:

```ts
import type Database from 'better-sqlite3'

type ThingRow = { readonly id: string; readonly title: string }

export class ThingRepository {
  private readonly findByIdStatement: Database.Statement<[string], ThingRow>

  constructor(db: Database.Database) {
    this.findByIdStatement = db.prepare('select id, title from things where id = ?')
  }

  findById(id: string): ThingRow | null {
    return this.findByIdStatement.get(id) ?? null
  }
}
```

## Required checks

- `pnpm typecheck`
- `pnpm lint`
- `pnpm test`

## Completion report additions

Include the exact skill name `local-data-storage`, changed files, commands run, tests added or changed, manual verification, and residual risk. Do not report a check as passed unless it actually ran and passed.
