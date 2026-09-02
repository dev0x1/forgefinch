# Performance And Async

Use this reference for hot paths, allocation behavior, throughput, async execution, and long-running tasks.

## Performance Workflow

1. Identify whether the crate or path is performance or cost relevant.
2. Measure before optimizing.
3. Add or update benchmarks for hot paths.
4. Profile CPU and allocations when possible.
5. Optimize the bottleneck, then re-measure.

## Common Allocation Risks

- Repeated string formatting in hot paths.
- Unnecessary `String`, `Vec`, or collection clones.
- Repeated hashing of the same keys.
- Growing buffers without capacity planning.
- Per-item allocations where batching or arenas would fit.

## Throughput

- Prefer batching when individual-item processing creates avoidable overhead.
- Partition work into chunks that preserve cache locality.
- Avoid hot spinning, contended locks, and excessive task switching.
- Prefer shared state only when sharing is cheaper than recomputation.

## Async Behavior

- Do not run long CPU-bound loops on async executors without yielding or offloading.
- Add yield points for long-running async work when no `.await` naturally occurs.
- Use blocking pools or dedicated threads for blocking CPU or filesystem work when appropriate.
- Prefer bounded channels when backpressure matters.

## Benchmarks

- Use project-standard benchmark tools first.
- Include benchmark inputs that resemble realistic dev workloads.
- Keep benchmark results connected to the reason for the optimization.
