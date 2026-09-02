---
name: slice-execution
description: Implement or review one selected schema-v4 workpackage slice against its acceptance criteria, project boundaries, and focused checks.
---

# Slice Execution

1. Read the active YAML/spec, repository instructions, applicable product
   skills, and nearby source/tests.
2. Confirm the selected slice exists, is decision-ready, and has acceptance
   criteria and executable checks.
3. For `quality_review`, confirm all implementation slices are resolved. Review
   the complete delta independently with findings first, then run the required
   quality command.
4. For `verification`, confirm implementation and quality review are resolved
   before proving the complete goal.
5. Implement or review only the selected slice, run targeted checks, and record
   honest results and completion evidence in YAML.

If review or verification exposes a behavior defect, add `[defect-open]`,
reopen the owning implementation slice, and reset both closure slices to
`todo`. Do not put status evidence in the descriptive spec.
