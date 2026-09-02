# Core Rust Principles

Use this reference for general Rust implementation, refactoring, and review.

## Default Style

- Prefer idiomatic Rust APIs that look familiar to the ecosystem.
- Prefer strong types over primitive strings, integers, or booleans with hidden semantics.
- Prefer explicit ownership and borrowing over broad cloning.
- Prefer simple modules and functions over object-oriented manager/service/factory patterns.
- Prefer regular free functions when computation does not naturally belong to a receiver.
- Avoid vague type names such as `Manager`, `Service`, `Factory`, `Helper`, and `Util` unless the domain meaning is precise.
- Document magic values, defaults, timeouts, limits, retry behavior, and surprising side effects.

## API Shape

- Keep essential behavior discoverable as inherent methods.
- Implement traits to interoperate with the ecosystem, but do not hide core behavior behind traits.
- Use newtypes for values with units, validation, or business semantics.
- Use `Default`, `Debug`, `Clone`, `Copy`, `Eq`, `Hash`, `Ord`, and `Display` where they make the type easier and safer to use.
- Keep public types easy for humans and coding agents to understand through names, docs, examples, and compiler checks.

## Panics

- Panic for detected programming bugs and impossible internal states.
- Return errors for expected runtime failure.
- Do not use panics for normal control flow or recoverable user/input/system failures.

## Agent-Friendly Rust

- Make APIs testable without real network, filesystem, clock, or process side effects.
- Provide examples for public APIs and important internal extension points.
- Keep observable behavior covered by tests before broad refactors.
- Use compiler diagnostics as part of the workflow: make small changes, compile, adjust.
