# Cargo Workspace And Crates

Use this reference for workspace layout, crates, features, modules, and dependency organization.

## Workspace Shape

- Prefer smaller crates when boundaries are stable, ownership differs, compile time benefits, or reuse is real.
- Avoid premature crate splitting when the boundary is still fluid.
- Keep crate names, package names, feature names, and module names concrete and domain-specific.
- Keep examples, benches, integration tests, and test utilities in conventional Cargo locations.

## Feature Design

- Cargo features should be additive.
- Avoid features that disable behavior or create incompatible combinations.
- Validate important feature combinations when the crate exposes optional integrations.
- Gate test-only utilities behind a clearly named feature such as `test-util` when they must be shared.

## Dependency Hygiene

- Avoid leaking external dependency types in public APIs unless that dependency is part of the product contract.
- Prefer wrapper or conversion types when a dependency should remain replaceable.
- Keep `-sys` crates thin and dependency-light.
- Keep optional dependencies behind features.

## Module Layout

- Keep `src/lib.rs` thin: crate docs, crate attributes, module declarations, and only deliberate prelude or curated re-exports when the task explicitly calls for them.
- Put implementation, invariants, helpers, and tests in focused modules rather than in the crate root.
- Put related invariants inside the same module when private fields or unsafe internals depend on them.
- Avoid glob re-exports in public APIs.
- Use explicit `pub use` exports for the curated surface.
- Use `#[doc(inline)]` for internal public re-exports that should appear as native API items.
