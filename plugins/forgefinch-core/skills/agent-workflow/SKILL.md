---
name: agent-workflow
description: Coordinate multi-step development, reviews, dependency changes, skill maintenance, and completion reporting in software repositories. Use with the applicable product plugin; do not use as a substitute for product architecture guidance.
---

# Development Workflow

Read the repository `AGENTS.md` first and select the smallest applicable set of
product skills. Repository instructions own architecture, tooling, security,
and completion commands; this skill owns the shared delivery sequence.

## Workflow

1. Inspect the current repository state, instructions, relevant implementation,
   and tests before changing files.
2. For broad work, create or select a schema-v4 workpackage and run definition
   before implementation. A small single-session change may keep an equivalent
   plan in the current task when repository rules allow it.
3. Implement one selected implementation slice at a time against its acceptance
   criteria and focused checks.
4. After all implementation slices are resolved, perform the independent,
   findings-first quality-review slice and run the profile's required quality
   command.
5. Perform final verification only after quality review is done. Prove the
   complete goal, constraints, integrations, and relevant regressions.
6. Report changed files, checks actually run, skipped or blocked checks with
   reasons, manual verification, and residual risk.

Use `$workpackage-planning`,
`$workpackage-definition`,
`$slice-execution`, `$workpackage-review`, and
`$verification` for their owning stages.

## Invariants

- Required checks are blocked rather than skipped when unavailable.
- Do not start quality review before implementation is resolved.
- Do not start final verification before quality review is resolved.
- A behavior defect uses `[defect-open]`, reopens the owning implementation
  slice, and resets review and verification to `todo` until re-reviewed and
  reverified.
- Do not claim a command passed unless it was executed and passed.
