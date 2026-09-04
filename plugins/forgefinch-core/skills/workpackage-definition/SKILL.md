---
name: workpackage-definition
description: Turn a planned workpackage into a development-ready package by reconciling architecture, contracts, security, slices, acceptance criteria, checks, and test strategy.
---

# Workpackage Definition

Definition happens after planning and before implementation.

1. Read the workpackage YAML/spec, repository instructions, relevant product
   skills, implementation, tests, and current contracts.
2. Reconcile the goal and scope with actual architecture and identify product
   boundaries, data/contracts, policy/security, failure modes, observability,
   and verification surfaces.
3. Assign every required behavior and decision to an implementation slice.
4. Refine slice order, acceptance criteria, focused checks, open questions, and
   non-goals. Do not hide a blocking decision in narrative notes. Place checks
   by tier, never by duration: implementation slices carry only static and
   unit checks, and every integration, live, and destructive check belongs to
   the final verification slice.
5. Confirm the mandatory penultimate quality-review slice uses the applicable
   project profile and the final verification slice covers the complete goal.
6. Run the repository workpackage validator.

Do not implement product behavior during definition. Mark the package blocked
when an unresolved decision prevents a safe first slice.
