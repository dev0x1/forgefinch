---
name: acceptance-specification
description: Write or review testable acceptance criteria, negative cases, done conditions, and check mappings for a selected workpackage slice.
---

# Acceptance Specification

Use the active workpackage YAML, its spec, applicable product skills, and nearby
implementation and tests.

## Rules

- Prefix each criterion ID with its slice ID, such as `WP-0001-S1-AC1`.
- State observable behavior, evidence, and important negative cases rather than
  implementation activities.
- Keep criteria within the selected slice and connect them to executable checks.
- Cover relevant contracts, security, privacy, accessibility, persistence,
  failure behavior, and architecture boundaries identified by product guidance.
- Quality-review criteria prove a findings-first review occurred and every
  finding was either resolved or reopened in its implementation slice.
- Final-verification criteria close the complete workpackage goal, constraints,
  integration journeys, and affected regression layers.

Done means criteria are concrete, testable, correctly prefixed, slice-scoped,
and mapped to evidence that can establish the goal.
