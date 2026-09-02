# Shared Forgefinch Development Workflow

Install `forgefinch-core` and the optional plugin appropriate for this
repository. Plugin installation does not merge this template into a project's
`AGENTS.md`; repository owners must adopt and tailor it explicitly.

For broad development work, use:

```text
Workpackage -> Definition -> Implementation Slices -> Code Quality Review -> Verification
```

- New durable workpackages use schema version 4.
- Historical schema-version-2 and schema-version-3 records remain valid.
- Every implementation slice has acceptance criteria and an executable check.
- Exactly one findings-first quality-review slice is penultimate.
- Exactly one complete-goal verification slice is last.
- Required checks are blocked, never skipped, when unavailable.
- A `[defect-open]` finding reopens the owning implementation slice and resets
  review and verification to `todo`.
- Use the repository's command profile; do not copy commands from another
  project.

Keep product architecture, security, testing, and completion-report rules in
the owning repository's `AGENTS.md`.
