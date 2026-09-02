---
name: api-contract-release
description: Use for release, downstream consumer handoff, and platform coordination for backend API contracts and SDKs.
---

# api-contract-release

## Purpose

Coordinate contract and SDK changes so downstream consumers, especially
desktop apps and external SDK users, can verify generated artifacts and consume
published package or crate outputs.

## Use This Skill When

- Preparing contract and SDK artifacts for consumer handoff.
- Updating release notes, runbooks, package metadata, or consumer handoff docs.
- Changing CI/check recipes that downstream repos rely on.
- Coordinating OpenAPI/SDK changes with a platform backend behavior change.

## Workflow

1. Read `AGENTS.md`, `docs/runbooks/api-contract-release.md`, and the active
   workpackage record under `docs/workpackages/` when present.
2. Run the smallest check set for the touched surface; run `just check` before
   declaring artifacts ready for consumer handoff.
3. Record the platform commit SHA or package version used for downstream
   consumers.
4. Keep platform coordination explicit: backend route behavior, the public CLI
   behavior, and live Playwright HTTP checks remain outside SDK code.
5. Do not ask consumers to use floating branches, unpinned package ranges, or
   uncommitted generated artifacts.

## Guardrails

- `CONTRACT_ROOT` variables are build/dev path conventions only, not runtime
  product configuration.
- Do not publish or document unsigned local dev tokens, local passwords, or
  placeholder provider keys as shared-environment guidance.
- Do not merge generated SDK changes without their OpenAPI source and bundle.

## Done Means

- The release candidate artifacts have passing checks or documented blockers.
- Downstream consumers can pin a package version or commit SHA and run their
  bridge checks.
- Handoff docs name which boundary owns each follow-up: contract artifacts and
  SDKs here, backend route behavior and live API verification in platform
  route/test crates.
