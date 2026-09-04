# Workpackage Schema v5

Schema v5 keeps every schema-v4 field and adds a test-pyramid tier model to
checks. Each check declares `tier` (`static`, `unit`, `integration`, `live`,
or `destructive`) and `env` (`none`, `docker`, `dev-local`, `dev-local-full`,
or `disposable`), records `evidence` (`executed`, `skipped`, `seconds`, `run`)
once it has run, and may name another record in `blocked_by`.

## Placement

Placement follows the tier, never the duration. How long a check takes is not
a reason to move it.

- Implementation slices name only `static` and `unit` checks, and at least one
  of them runs with `env: none`. Implementation proves behavior through
  compilation, static checks, and unit tests.
- The quality-review slice runs the project's code-quality command and names
  only `static` and `unit` checks.
- Every `integration`, `live`, and `destructive` check belongs to the final
  verification slice, which names at least one `integration` and one `live`
  check and runs them once on the reviewed delta. No justification moves such
  a check into an earlier slice.
- A defect found by verification reopens the owning implementation slice and
  resets review and verification, exactly as in schema v4.

## Evidence

- A required `integration` or `live` check is `done` only with at least one
  executed test recorded in its evidence.
- A skipped optional check names the unavailable capability in its notes
  (`Unavailable capability: ...`).
- A required check blocked on a surface another record owns names that record
  in `blocked_by`; the slice and the package close once the named record is
  complete, and cycles are rejected.
- A check that has run names one catalogued command, never a chained command.

Schema-v2, v3, and v4 records remain valid historical formats and are never
rewritten only to add these fields.
