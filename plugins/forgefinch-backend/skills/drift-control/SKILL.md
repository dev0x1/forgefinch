---
name: drift-control
description: Use for alignment between service matrix, routing, runbooks, infra, and skills inside a workpackage or slice.
---

# drift-control

## Purpose

Support alignment between service matrix, routing, runbooks, infra, and skills inside the active workpackage.

## Use This Skill When

- The current workpackage or slice touches alignment between service matrix, routing, runbooks, infra, and skills.
- A local check, review, or design choice needs this specialty.

## Workflow

1. Read `AGENTS.md`, `docs/process/WORKPACKAGE_SYSTEM.md`, the active workpackage YAML file when present, and nearby code or docs.
2. Confirm which acceptance criteria and slice this work supports.
3. Inspect existing architecture, boundaries, contracts, tests, and local service config before changing files.
4. When a lightweight environment is in scope, compare its application binary,
   router, middleware, identity verification semantics, policy path, schema,
   migrations, seed command, repositories, query services, DTOs, and safe
   errors with the production-shaped local environment.
5. Keep a checked allowlist of differences limited to composition-root external
   adapters or protocol-compatible mock services, and run the same product
   conformance scenarios in both environments.
6. Implement or review only the behavior needed for the selected slice.
7. Run targeted local checks when practical and record command names, results, changed files, and open questions.

## Required Output

- Workpackage or slice summary.
- Affected files, crates, services, schemas, policies, prompts, or docs.
- Local checks run, skipped with reason, or still needed.
- Open questions and next slice needs.

## Guardrails

- Keep application semantics inside application-owned code and schemas.
- Keep external services behind ports, adapters, typed config, and local checks.
- Keep security, identity, data ownership, and audit boundaries explicit when they are relevant.
- Treat optional integration packs as extensions of one backend. Do not allow
  route, domain, query, projection, DTO, schema, seed, policy, identity, or
  safe-error forks.
- Do not allow environment-name or mock-mode branches, fixture personas,
  placeholder projections, or deterministic mock values in production product
  modules. Mock values enter through seeds, test fixtures, or external adapter
  protocols.
- Do not let an omitted capability fabricate successful product state; require
  the normal explicit unavailable posture.
- Do not broaden the slice beyond the workpackage acceptance criteria.
- Do not add later-environment planning unless the user asks for it.

## Done Means

- The slice behavior is present or the review finding is explicit.
- Required local checks are named and results are recorded.
- Architecture docs are updated when architecture truth changes.
- The selected slice entry or current task can show what changed and what remains.
