---
name: tenant-rls
description: Use for tenant-scoped tables, RLS, tenant context propagation, and isolation tests inside a workpackage or slice.
---

# tenant-rls

## Purpose

Support tenant-scoped tables, RLS, tenant context propagation, and isolation tests inside the active workpackage.

## Use This Skill When

- The current workpackage or slice touches tenant-scoped tables, RLS, tenant context propagation, and isolation tests.
- A local check, review, or design choice needs this specialty.

## Workflow

1. Read `AGENTS.md`, `docs/process/WORKPACKAGE_SYSTEM.md`, the active workpackage YAML file when present, and nearby code or docs.
2. Confirm which acceptance criteria and slice this work supports.
3. Inspect existing architecture, boundaries, contracts, tests, and local service config before changing files.
4. Implement or review only the behavior needed for the selected slice.
5. Run targeted local checks when practical and record command names, results, changed files, and open questions.

## Required Output

- Workpackage or slice summary.
- Affected files, crates, services, schemas, policies, prompts, or docs.
- Local checks run, skipped with reason, or still needed.
- Open questions and next slice needs.

## Guardrails

- Keep application semantics inside application-owned code and schemas.
- Keep external services behind ports, adapters, typed config, and local checks.
- Keep security, identity, data ownership, and audit boundaries explicit when they are relevant.
- Do not broaden the slice beyond the workpackage acceptance criteria.
- Do not add later-environment planning unless the user asks for it.

## Done Means

- The slice behavior is present or the review finding is explicit.
- Required local checks are named and results are recorded.
- Architecture docs are updated when architecture truth changes.
- The selected slice entry or current task can show what changed and what remains.
