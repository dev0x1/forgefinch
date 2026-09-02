# Documentation And Examples

Use this reference for Rustdoc, crate docs, module docs, public API docs, and examples.

## Public Docs

- Public crates should have crate-level documentation.
- Public modules should have `//!` module documentation when they are part of the API surface.
- Public items should start with a short summary sentence.
- Keep the first sentence compact and skimmable.

## Canonical Sections

Use these sections when applicable:

```text
Examples
Errors
Panics
Safety
Abort
```

Do not create parameter tables by default. Explain parameter meaning in prose when needed.

## Examples

- Provide examples that compile when possible.
- Prefer examples that show realistic use and error handling.
- Keep public API examples aligned with current crate features.
- Use doc tests when examples are part of the API contract.

## Safety Docs

- Every `unsafe fn`, unsafe trait, or safe abstraction around unsafe internals must document caller obligations or internal safety invariants.
- Safety docs should explain why the code is sound, not merely state that it is safe.

## Re-Exports

- Use explicit public re-exports.
- Use `#[doc(inline)]` for internal re-exports that should appear as native API items.
- Do not inline third-party re-exports.
