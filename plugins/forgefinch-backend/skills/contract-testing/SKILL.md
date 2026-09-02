---
name: contract-testing
description: Use for contracts for APIs, events, policies, tools, connectors, model outputs, and adapters inside a workpackage or slice.
---

# contract-testing

## Purpose

Support contracts for APIs, events, policies, tools, connectors, model outputs, and adapters inside the active workpackage.

## Use This Skill When

- The current workpackage or slice touches contracts for APIs, events, policies, tools, connectors, model outputs, and adapters.
- A local check, review, or design choice needs this specialty.

## Workflow

1. Read `AGENTS.md`, `docs/process/WORKPACKAGE_SYSTEM.md`, the active workpackage YAML file when present, and nearby code or docs.
2. Confirm which acceptance criteria and slice this work supports.
3. Inspect existing architecture, boundaries, contracts, tests, and local service config before changing files.
4. For public REST, SCIM, SSE-over-HTTP, or other HTTP API behavior, confirm
   the same coordinated workpackage owns OpenAPI/route drift tests and DTO
   examples in the repository-owned API contract package, the API client SDK method coverage,
   and the public CLI command coverage.
5. For user-facing SSE behavior, confirm SDK SSE reconnect helper tests and
   `public CLI watch ...` command tests are part of the same workpackage.
6. Choose REST API test tools by layer: backend server route tests for internal
   route logic, the repository-owned API contract package for contract
   truth, the API client unit/request tests for SDK correctness, the public CLI tests
   for CLI correctness, and Playwright as the only live HTTP E2E/API scenario
   runner.
7. For query/read-model work, add tests for ordinary and privileged callers,
   cross-tenant denial, canonical collection uniqueness, field provenance,
   resource-scoped persistence queries, snapshot consistency, explicit
   capability/version discovery, and unknown-route versus concealed-resource
   behavior.
   When context embeds optional capabilities, inject a policy-evaluator outage
   and prove core identity/Workspace data remains successful while affected
   capabilities are explicitly unavailable; separately prove the entitlement
   endpoint still fails closed.
8. Prove runtime route reachability from the constructed production router;
   OpenAPI, generated SDK, catalog, or handler-symbol presence alone is not
   implementation evidence.
9. When optional integration availability is in scope, run the same public
   contract scenarios with the pack absent and present, verify only explicit
   capability differences, and scan production product modules for fixture
   branches or values.
10. Implement or review only the behavior needed for the selected slice.
11. Run targeted local checks when practical and record command names, results, changed files, and open questions.

## Required Output

- Workpackage or slice summary.
- Affected files, crates, services, schemas, policies, prompts, or docs.
- Public API contract coverage, when applicable: OpenAPI route drift and DTO
  examples in the repository-owned API contract package, SDK request
  building, auth/request context headers, idempotency, pagination, safe error
  parsing, SSE reconnect helpers, CLI `public CLI ... --output json` tests, and
  Playwright live HTTP scenarios.
- REST API test tool-layer choices and skipped layers with reasons.
- Local checks run, skipped with reason, or still needed.
- Open questions and next slice needs.

## Guardrails

- Keep application semantics inside application-owned code and schemas.
- Keep external services behind ports, adapters, typed config, and local checks.
- Keep security, identity, data ownership, and audit boundaries explicit when they are relevant.
- Do not add overlapping public API live HTTP tools; Playwright is the only
  live HTTP E2E/API scenario runner.
- Do not allow a general client-context test persona to hide a privileged
  dependency; include the least-privileged intended caller in the role matrix.
- Do not accept hard-coded, synthetic, or silently empty response fields as
  fixture convenience in production projections. Fixture values must enter
  through seeds, repositories, or external mock protocols.
- Do not use 404 probing as capability discovery or merge duplicate resource
  collection contracts.
- Do not name shared public API implementations for a consuming client.
- Do not accept a zero-drift ledger unless production-router reachability is
  part of the evidence.
- Do not broaden the slice beyond the workpackage acceptance criteria.
- Do not add later-environment planning unless the user asks for it.

## Done Means

- The slice behavior is present or the review finding is explicit.
- Required local checks are named and results are recorded.
- Architecture docs are updated when architecture truth changes.
- The selected slice entry or current task can show what changed and what remains.
