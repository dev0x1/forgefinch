---
name: tdd
description: Use for implementing behavior changes, bug fixes, business logic, IPC, storage, stateful UI, and validation through strict red-green-refactor TDD.
---

# TDD Workflow

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

Use for behavior changes, bug fixes, business logic, IPC, storage, parsing, validation, and stateful UI.

## Non-Negotiable Sequence

1. Write the failing test first.
2. Run the targeted test and confirm it fails for the expected reason.
3. Implement the smallest passing change.
4. Run the targeted test and confirm it passes.
5. Refactor while keeping tests green.
6. Run the relevant broader checks.

Do not write production implementation before the failing test.

## Red Phase

- Test one behavior.
- Test the public boundary.
- Assert the observable outcome.
- Capture the failure output in the task notes.

## Green Phase

- Make the smallest change.
- Do not add unrelated cleanup.
- Do not generalize before the second concrete case.
- Keep security checks intact.

## Refactor Phase

- Rename for clarity.
- Extract duplication after tests pass.
- Keep module boundaries intact.
- Run the same test after every meaningful refactor.

## Bug Fixes

1. Reproduce the bug in a failing test.
2. Confirm the test fails without modifying production code.
3. Fix the smallest production unit.
4. Confirm the test passes.
5. Add adjacent edge-case tests only when they protect the same bug class.

Completion note format:

```md
Red: `<command>` failed with `<expected failure summary>`
Green: `<command>` passed
```

## IPC TDD

Write tests in this order:

1. Invalid payload is rejected.
2. Untrusted sender is rejected.
3. Valid payload calls the service with parsed values.
4. Service failure maps to the documented safe error.

Only after those tests exist, implement the IPC handler.

Security rule: the untrusted sender test must fail before implementation and pass after implementation.

## Component TDD

Test from the user's perspective.

Order:

1. Test initial accessible rendering.
2. Test the primary user action.
3. Test invalid/error state.
4. Implement minimal UI.
5. Refactor component structure.

Do not test internal state variables.

## Storage TDD

Order:

1. Create a temp database or temp app-data directory.
2. Write a failing test for repository behavior.
3. Implement repository logic.
4. Add a migration test when schema changes.
5. Verify cleanup does not touch real user data.

Never run storage tests against the developer's real app data directory.

## Refactor Safely

Before refactor:

```bash
pnpm test -- --run <target-test-file>
```

During refactor:

- Keep behavior unchanged.
- Rename one concept at a time.
- Move files without changing logic.
- Run targeted tests after each meaningful move.

After refactor:

```bash
pnpm typecheck
pnpm test
```

Done when the failing test was observed before implementation, the target test passes after implementation, broader checks relevant to touched files were run, and final report includes the red and green commands.
