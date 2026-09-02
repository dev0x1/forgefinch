# Workpackage Schema v4

New durable records contain `schema_version`, `id`, `title`, `status`, `owner`,
optional `spec_ref`, `goal`, `scope`, and `slices`.

Each slice contains `id`, `kind`, `title`, `status`, `summary`, `ac`, `checks`,
`questions`, `notes`, and `completion`. Each check contains `cmd`, Boolean
`required`, `status`, and `notes`.

## Ordering

- One or more `implementation` slices.
- Exactly one penultimate `quality_review` slice.
- Exactly one final `verification` slice.
- Quality review may start only after all implementation slices resolve.
- Verification may start only after implementation and quality review resolve.

## Completion

- A done slice has done acceptance criteria, done required checks, optional
  checks either done or justifiably skipped, and no open question.
- A complete package has every slice done and no open defect marker.
- A required check is never skipped. If unavailable, mark it blocked.
- `[defect-open]` in slice notes or completion prevents closure, reopens the
  owning implementation slice, and resets review and verification.

Schema-v2 and schema-v3 records remain supported as historical formats.
