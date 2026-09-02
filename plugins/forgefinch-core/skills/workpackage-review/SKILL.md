---
name: workpackage-review
description: Review workpackage YAML/spec completeness, slice state, acceptance criteria, mandatory quality review, evidence, boundaries, and completion claims.
---

# Workpackage Review

Report findings first, ordered by severity and supported with file references.

Check that:

- The filename, workpackage ID, `spec_ref`, goal, scope, slice IDs, and
  acceptance IDs are consistent.
- The spec describes the same target and strategy without carrying execution
  status.
- Schema-v4 packages have implementation slices with checks, one penultimate
  quality-review slice with the project-profile command, and one final
  verification slice.
- Started closure slices satisfy their prerequisites.
- Done slices have resolved acceptance, required checks, optional checks,
  questions, and findings.
- Product architecture, security, privacy, accessibility, contract, and test
  boundaries are covered where applicable.
- No open `[defect-open]` marker is hidden by a completion claim.

Do not call a package complete when required evidence is missing or a product
boundary has not been proven.
