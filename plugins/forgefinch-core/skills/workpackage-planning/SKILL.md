---
name: workpackage-planning
description: Plan durable schema-v4 workpackage YAML records and colocated specs with implementation, mandatory quality-review, and final verification slices. Retain historical schema-v2/v3 records without rewriting them.
---

# Workpackage Planning

Read the repository `AGENTS.md`, process documentation, nearby implementation,
tests, and the applicable command profile before planning.

## Workflow

1. Define a one-sentence goal in this form: `<objective end state>, verified by
   <evidence/checks/artifacts>, while preserving <constraints/boundaries>.`
2. Put compact execution state in YAML and feature/architecture context in a
   colocated `.spec.md` file.
3. Create one or more `implementation` slices, exactly one penultimate
   `quality_review` slice, and exactly one final `verification` slice.
4. Prefix slice IDs with the workpackage ID and acceptance IDs with the slice
   ID. Give every slice acceptance criteria, checks, questions, notes, and
   completion fields.
5. Give every implementation slice at least one executable check. Mark every
   check `required: true` or `required: false`.
6. Put the project's mandatory quality command in the review slice. Read
   [project profiles](references/project-profiles.md) for the supported
   project commands.
7. Make final verification prove the whole goal, constraints, integrated
   behavior, and affected regression layers.
8. Run the repository's workpackage validator.

The complete schema and state invariants are in
[schema v4](references/schema-v4.md). Reusable files live in `assets/`.

Historical schema-v2/v3 records remain valid and are not upgraded merely for
consistency. New durable records use schema v4.
