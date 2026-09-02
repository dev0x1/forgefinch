---
name: repo-scaffold
description: Use for workspace layout, Cargo members, repo directories, and modular-monolith structure inside a workpackage or slice.
---

# repo-scaffold

## Purpose

Support workspace layout, Cargo members, repo directories, and modular-monolith structure inside the active workpackage.

## Use This Skill When

- The current workpackage or slice touches workspace layout, Cargo members, repo directories, and modular-monolith structure.
- A local check, review, or design choice needs this specialty.

## Workflow

1. Read `AGENTS.md`, `docs/process/WORKPACKAGE_SYSTEM.md`, the active workpackage YAML file when present, and nearby code or docs.
2. Confirm which acceptance criteria and slice this work supports.
3. Inspect existing architecture, boundaries, contracts, tests, and local service config before changing files.
4. For public API workpackages, preserve the client-stack boundary:
   `apps/public CLI -> crates/interfaces/API client ->
   path/to/api-contracts`.
5. Runtime calls still go to the backend server public REST/SSE only.
6. Implement or review only the behavior needed for the selected slice.
7. Run targeted local checks when practical and record command names, results, changed files, and open questions.

## Required Output

- Workpackage or slice summary.
- Affected files, crates, services, schemas, policies, prompts, or docs.
- Repo layout and dependency-direction impact for `api-contracts`,
  the API client, TypeScript SDK, and the public CLI when the workpackage changes
  public API behavior.
- Local checks run, skipped with reason, or still needed.
- Open questions and next slice needs.

## Guardrails

- Keep application semantics inside application-owned code and schemas.
- Keep external services behind ports, adapters, typed config, and local checks.
- Keep security, identity, data ownership, and audit boundaries explicit when they are relevant.
- Do not let the public CLI depend on the backend server internals, domain crates,
  database crates, or adapter crates.
- Do not let the API client own domain behavior, persistence, policy
  decisions, audit storage, evidence storage, or projection state.
- Do not broaden the slice beyond the workpackage acceptance criteria.
- Do not add later-environment planning unless the user asks for it.

## Done Means

- The slice behavior is present or the review finding is explicit.
- Required local checks are named and results are recorded.
- Architecture docs are updated when architecture truth changes.
- The selected slice entry or current task can show what changed and what remains.
