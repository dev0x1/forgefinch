# Application Runtime And Errors

Use this reference for Rust applications, binaries, runtime setup, app-level errors, and logging.

## Application Errors

- Applications may use `anyhow`, `eyre`, or a similar application-level error crate.
- Pick one application error type and use it consistently.
- Do not mix several top-level application error styles in the same app.
- Use library-specific structured errors for reusable library crates.

## Runtime Setup

- Use Rust `1.95` for this repository unless a project guide updates the target. Use nightly only when a feature explicitly requires it and the tradeoff is documented.
- Use the project or stack-specific skill for framework choices such as async runtime, HTTP server, database access, schema generation, caching, eventing, and policy evaluation.
- Keep runtime and allocator decisions close to application startup.
- Consider a high-performance global allocator only when it fits the deployment and project policy.
- Document runtime assumptions such as Tokio flavor, thread count, blocking behavior, shutdown, and signal handling.

## Logging And Telemetry

- Prefer structured logging over formatted strings.
- Give important events stable names.
- Include machine-filterable fields for request IDs, tenant IDs, operation names, entity IDs, and error kinds.
- Redact or omit sensitive data.
- Keep log messages useful without requiring local debugger context.

## Operational Behavior

- Define graceful shutdown paths for servers, workers, and background tasks.
- Surface startup configuration errors clearly.
- Avoid hidden global state that makes tests and multi-instance execution unreliable.
