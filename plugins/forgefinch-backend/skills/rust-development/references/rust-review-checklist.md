# Rust Review Checklist

Use this reference for Rust code reviews and risky implementation changes.

## Correctness

- Are ownership, borrowing, and lifetimes simpler than the alternatives?
- Are errors returned for expected failures and panics reserved for bugs?
- Are edge cases, empty inputs, invalid inputs, and boundary values covered?
- Are feature flags additive and tested where relevant?

## API Design

- Are public names precise and free of vague suffixes?
- Are public types documented, debuggable, and stable enough?
- Does the API expose dependency types or smart pointers unnecessarily?
- Are builders, generics, traits, and dynamic dispatch justified?

## Safety

- Is every unsafe block necessary?
- Is safety reasoning present and specific?
- Could safe callers trigger undefined behavior?
- Should Miri or additional adversarial tests be required?

## Performance

- Does the change add avoidable allocations, cloning, formatting, locking, or per-item overhead?
- Are optimizations benchmarked?
- Does async code block the executor or starve other tasks?

## Testing

- Are behavior changes covered by unit, integration, property, doc, or benchmark tests as appropriate?
- Are external effects mockable?
- Are examples and docs updated for public API changes?

## Tooling

- Were relevant `cargo fmt`, `cargo clippy`, `cargo test`, doc, feature, or Miri checks run?
- Are lint suppressions narrow and justified?
