# Testing, Linting, And Verification

Use this reference for tests, CI, linting, static analysis, and quality gates.

## Local Validation

Prefer narrow commands first, then broaden:

```text
cargo fmt --check
cargo clippy --workspace --all-targets
cargo test --workspace
cargo test -p <package> <test-name>
cargo doc --workspace --no-deps
cargo deny check
cargo audit
```

Adapt to existing repo scripts when present.

## Static Verification

- Use rustfmt for formatting.
- Use Clippy for correctness, maintainability, and idiom lints.
- Use compiler lints for unsafe operations, unused lifetimes, redundant imports, missing debug implementations, and similar issues when the project enables them.
- Use `#[expect(...)]` for intentional lint overrides when supported, with a short reason.
- Prefer targeted lint opt-outs over broad crate-level suppression.

## Tests

- Cover observable behavior rather than implementation details.
- Use unit tests for local invariants and pure logic.
- Use integration tests for public crate behavior and cross-module workflows.
- Use property tests for parsers, serializers, state machines, and invariants with large input spaces.
- Use benchmarks for hot paths before and after performance changes.
- Make filesystem, network, clock, process, and environment interactions mockable.

## CI Expectations

- CI should run formatting, linting, tests, and relevant feature combinations.
- Security-sensitive crates should run dependency auditing when the project supports it.
- Unsafe-heavy crates should consider Miri in CI or targeted pre-merge checks.
- Feature-heavy crates should consider `cargo hack check --workspace --feature-powerset` for important feature combinations.
- Dependency cleanup may use `cargo +nightly udeps --workspace --all-targets` when the project supports it.
