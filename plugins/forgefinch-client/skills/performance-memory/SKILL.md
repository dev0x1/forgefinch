---
name: performance-memory
description: "Use for Electron startup performance, renderer render performance, bundle size, dependency cost, IPC batching, large lists, profiling, memory leaks, and performance regression reports."
---

# performance-memory

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

## Purpose

Keep the desktop app responsive. Measure before optimizing, reduce startup work, avoid chatty IPC, and prove improvements with before/after data.

For React-specific performance rule details, use the upstream
`react-best-practices` skill as supplemental guidance when it is installed;
repository structure and Electron boundaries still come from this plugin.

## Use this skill when

- adding large dependencies, heavy startup work, background services, IPC-heavy features, large lists, dashboards, image processing, or expensive React views
- investigating slow startup, high memory, UI jank, slow queries, bundle growth, leaks, or frozen windows

## Non-negotiable rules

- Measure before optimizing and measure again after changes.
- Main-process startup must remain lean and deterministic.
- Do not add large production dependencies without a dependency cost review.
- Batch or coalesce chatty IPC.
- Virtualize large lists.
- Keep CPU-heavy work out of renderer event handlers.
- Performance changes require a regression report in the completion summary.

## Required workflow

1. Define the user-visible performance target and baseline measurement.
2. Identify whether the bottleneck is startup, renderer render, IPC, database, filesystem, network, or packaging.
3. Make one optimization at a time.
4. Run tests to protect behavior.
5. Record before/after measurements and residual risk.

## Repo placement

- Main startup, background services, IPC batching, and native work belong in `<desktop-app-root>/src/main`.
- Renderer render performance, large lists, and expensive views belong in `<desktop-app-root>/src/renderer/src/features` or reusable components.
- Shared performance-sensitive pure helpers can live in `<desktop-app-root>/src/shared` only when they are serializable and runtime-neutral.
- Dependency cost review follows `agent-workflow`; do not add production packages without reason, impact, and validation.
- Use `pnpm build` only for bundle/build-output review or Electron build config changes.

## Patterns And Examples

- Startup budget: list startup tasks, mark each blocking/deferred/lazy, move non-critical work after the first window is ready, and avoid synchronous filesystem/database work unless required.
- Renderer profiling: reproduce the slow interaction, profile render counts, reduce broad subscriptions, move expensive derived data out of render, and memoize only costly calculations.
- IPC batching: replace loops of IPC calls with a validated batch route, enforce batch size, and return per-item errors when partial failure is expected.
- Large lists: measure expected item count before adding virtualization, keep rows pure and small, avoid hidden expensive content, and preserve keyboard/screen-reader behavior.
- Memory leaks: list created resources, clean up listeners, intervals, subscriptions, windows, file handles, and caches on unmount/close/dispose.
- Bundle analysis: check output when build size matters, find large imports or accidental main/Node imports, prefer route-level lazy loading for heavy screens, and keep preload minimal.
- Dependency cost: state the exact problem, check stack overlap, assess renderer/native/security impact, prefer dev dependencies when possible, and record maintenance risk.

Performance report example:

```md
## Scenario
- User-visible flow:
- Environment:

## Baseline
- Measurement:
- Method:

## Change
- Files:
- Hypothesis:

## After
- Measurement:
- Result:

## Residual risk
-
```

## Required checks

- `pnpm typecheck`
- `pnpm lint`
- `pnpm test`

## Completion report additions

Include the exact skill name `performance-memory`, changed files, commands run, tests added or changed, manual verification, and residual risk. Do not report a check as passed unless it actually ran and passed.
