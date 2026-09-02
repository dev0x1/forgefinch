---
name: rust-development
description: Use for Rust code, Cargo layout, tests, APIs, async behavior, and idiomatic crate design inside a workpackage or slice.
---

# rust-development

## Purpose

Support Rust code, Cargo layout, tests, APIs, async behavior, and idiomatic crate design inside the active workpackage.

## Use This Skill When

- The current workpackage or slice touches Rust code, Cargo layout, tests, APIs, async behavior, and idiomatic crate design.
- A local check, review, or design choice needs this specialty.

## Workflow

1. Read `AGENTS.md`, `docs/process/WORKPACKAGE_SYSTEM.md`, the active workpackage YAML file when present, and nearby code or docs.
2. Confirm which acceptance criteria and slice this work supports.
3. Inspect existing architecture, boundaries, contracts, tests, and local service config before changing files.
4. For Rust changes that add or change public REST, SCIM, SSE-over-HTTP, or
   other HTTP API behavior, keep OpenAPI contracts in
   the repository-owned API contract package, the API client SDK methods, and the public CLI commands
   in the same coordinated workpackage.
5. For user-facing SSE behavior, include SDK stream helpers and
   `public CLI watch ...` commands in the same workpackage.
6. For REST API tests in Rust, prefer axum/tower-style router tests for
   in-process route behavior and the API client integration tests for public
   HTTP behavior against a running the backend server.
7. Implement or review only the behavior needed for the selected slice.
8. Run targeted local checks when practical and record command names, results, changed files, and open questions.

## Required Output

- Workpackage or slice summary.
- Affected files, crates, services, schemas, policies, prompts, or docs.
- Public API Rust coverage, when applicable: `api-contracts`, backend server
  route tests, the API client unit/request
  tests, and the public CLI tests.
- REST API Rust test layer chosen: in-process route test, SDK unit/request
  test, CLI test, or Testcontainers substrate test.
- Local checks run, skipped with reason, or still needed.
- Open questions and next slice needs.

## Guardrails

- Keep application semantics inside application-owned code and schemas.
- Keep external services behind ports, adapters, typed config, and local checks.
- Keep security, identity, data ownership, and audit boundaries explicit when they are relevant.
- Keep the API client as a public REST/SSE SDK boundary, not a domain or
  persistence owner.
- Keep the public CLI as a thin CLI over the API client; it must not call
  the backend server internals, domain crates, database crates, or adapter crates.
- Do not broaden the slice beyond the workpackage acceptance criteria.
- Do not add later-environment planning unless the user asks for it.

## Done Means

- The slice behavior is present or the review finding is explicit.
- Required local checks are named and results are recorded.
- Architecture docs are updated when architecture truth changes.
- The selected slice entry or current task can show what changed and what remains.
