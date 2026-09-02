# Library API Design

Use this reference for reusable crates, public APIs, library errors, builders, and interoperability.

The API checklist here is adapted from the official Rust API Guidelines checklist. When exact rule wording or examples matter, consult https://rust-lang.github.io/api-guidelines/checklist.html.

## Public API Principles

- Keep the public surface small, predictable, documented, and easy to test.
- Avoid exposing smart pointers such as `Arc`, `Rc`, `Box`, or `Pin` unless they are central to the API purpose.
- Prefer concrete types first, generics second, and `dyn Trait` only when generics create excessive nesting or the use case truly needs dynamic dispatch.
- Accept flexible inputs with `impl AsRef<Path>`, `impl AsRef<str>`, `impl Read`, `impl Write`, or `impl RangeBounds<T>` when this improves call-site ergonomics.
- Keep essential functionality as inherent methods; trait implementations should forward to those methods.

## Official API Checklist Lens

Use this lens when designing or reviewing public crate APIs:

- Naming: follow Rust casing, getter, iterator, conversion, feature, and word-order conventions.
- Interoperability: implement standard traits eagerly when meaningful, including common comparison, hashing, formatting, conversion, collection, serialization, and thread-safety traits.
- Macros: make macro input syntax match the generated output shape, support attributes and visibility where expected, and allow item macros wherever items are valid.
- Documentation: include crate docs, item examples, error/panic/safety notes,
  useful links, package metadata, change notes, and hide implementation noise
  from rustdoc.
- Predictability: put conversions on the most specific type, use methods when there is a natural receiver, avoid out-parameters, keep operator overloads unsurprising, and reserve `Deref` for smart-pointer-like types.
- Flexibility: expose intermediate results when avoiding duplicate work matters, let callers control allocation and copying, use generics to avoid needless assumptions, and keep traits object-safe when trait objects are a plausible use case.
- Type safety: use newtypes, custom argument types, `bitflags`, and builders to make invalid or ambiguous calls harder to express.
- Dependability: validate arguments, keep destructors infallible, and provide explicit alternatives for cleanup that may fail or block.
- Debuggability: implement useful, non-empty `Debug` for all public types.
- Future proofing: seal traits when downstream implementations would block evolution, keep struct fields private, hide newtype internals, and avoid unnecessary trait bounds on public data structures.
- Necessities: keep stable public dependencies stable and compatible with the crate's intended license posture.

## Builders And Initialization

- Use builders for complex construction with multiple optional values or validation.
- Prefer staged or cascaded builders only when construction order encodes real invariants.
- Keep simple constructors simple: use `new`, `default`, or direct struct literals where appropriate.

## Library Errors

- Reusable libraries should expose stable, situation-specific error structs.
- Capture useful context and support `std::error::Error`.
- Avoid exposing internal error enums that freeze implementation details.
- Prefer helper methods such as `is_timeout()` or `path()` over forcing callers to match every internal variant.
- Preserve source errors where useful.

## Interoperability

- Make important public types `Send` unless there is a clear reason not to.
- Make public types `Sync` when shared references can safely cross threads.
- Provide escape hatches to native handles or raw representations only when users genuinely need them.
- Avoid leaking third-party types in public APIs unless the third-party crate is part of the API contract.

## Naming And Conversions

- Use `as_` for cheap borrowed or view conversions.
- Use `to_` for conversions that allocate or copy from a borrowed value.
- Use `into_` for conversions that consume `self`.
- Implement `From`, `TryFrom`, `AsRef`, and `AsMut` where they make call sites simpler and semantics are unambiguous.
- Name iterators after their constructors: `iter` returns `Iter`, `iter_mut` returns `IterMut`, and `into_iter` returns `IntoIter`.
- Avoid feature names such as `default`, `full`, `misc`, or `extras`; name the capability or dependency instead.

## Predictable Function Design

- Prefer returning values over filling out-parameters.
- Use constructors as static inherent methods, usually `new`, `with_*`, or `from_*`.
- Keep conversion functions near the most specific involved type.
- Use receiver methods when the operation naturally acts on an instance.
- Use free functions when no receiver owns the concept.

## Future-Proofing

- Keep public struct fields private unless field-level construction is intentionally part of the stable API.
- Seal traits that should not be implemented outside the crate.
- Avoid unnecessary generic bounds on public structs; put bounds on impls and functions instead.
- Hide implementation details behind newtypes when representation may change.
