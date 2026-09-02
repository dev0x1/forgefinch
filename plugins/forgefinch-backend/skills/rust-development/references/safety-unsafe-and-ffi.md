# Safety, Unsafe, And FFI

Use this reference for unsafe Rust, soundness review, FFI, platform calls, raw pointers, and shared library boundaries.

## Unsafe Policy

- Avoid `unsafe` by default.
- Use `unsafe` only for FFI/platform calls, novel abstractions, or benchmark-proven performance needs.
- Never use `unsafe` to bypass lifetimes, `Send`/`Sync`, ownership, or type-system friction.
- Every unsafe block should have nearby safety reasoning.
- Unsafe abstractions should be minimal, testable, and reviewed carefully.

## Soundness

- Safe functions must not allow undefined behavior through any safe call pattern.
- If callers must uphold invariants to avoid undefined behavior, expose an `unsafe fn` and document the contract.
- Keep unsafe invariants within tight module boundaries.
- Do not hide unsoundness behind safe wrappers.

## Miri And Adversarial Tests

- Use Miri for unsafe abstractions when available.
- Include adversarial tests for panicking closures, unusual trait implementations, aliasing, and drop behavior where relevant.

## FFI

- Prefer established interop crates and generated bindings where practical.
- FFI boundary types must be representation-safe and ownership-clear.
- Document who allocates, who frees, threading expectations, callback lifetime, nullability, and error reporting.
- Avoid sharing non-portable Rust state across dynamic library boundaries.
- Treat `String`, `Vec`, `Box`, `Rc`, `Arc`, non-`repr(C)` structs, statics, thread locals, and `TypeId`-dependent data as unsafe to share across independent Rust DLLs unless there is a proven boundary contract.
