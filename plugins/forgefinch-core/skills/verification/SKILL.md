---
name: verification
description: Run and record focused or complete-goal verification for workpackage slices, including failures, blocked checks, skipped checks, changed files, and residual risk.
---

# Development Verification

Use the selected slice, acceptance criteria, workpackage spec, repository
commands, and applicable product skills to select evidence.

- Run focused checks for implementation slices.
- For quality review, report findings before summaries and run the required
  project-profile quality command.
- Start final verification only after implementation and quality review are
  done. Cover the complete goal, named constraints, integrations, negative
  paths, persistence/restart when relevant, and affected regressions.
- Record exact commands and results. Required unavailable checks are blocked;
  optional checks may be skipped only with a concrete reason.
- A behavior defect reopens implementation with `[defect-open]` and resets
  closure slices.

Do not substitute a broad end-to-end check for missing lower-layer evidence,
and never report an unexecuted check as passed.
