# 9. Language and engine tools

Choose a language for integration, readability, safety, portability and the team, then profile the real workload. The repository's shared numeric kernels demonstrate rules; they are not a language-speed ranking.

| Language/runtime | First things to inspect | Useful tools/readings | Common trap |
|---|---|---|---|
| Python | Hot loops, list/dict allocation, conversion and extension boundaries | [cProfile/profile](research.md#r23), standard `timeit`, memory/allocation tools | Timing startup or rewriting everything in C before finding the hot region. |
| C | Algorithm, layout, lifetime, bounds and allocation | Platform sampling profiler, [Tracy](research.md#r20), sanitizers for correctness, [low-level manuals](research.md#r34) | Removing safety checks or using undefined behavior to appear faster. |
| C++ | Same as C, plus object copies, containers, allocation and ownership | Compiler/platform profiler, Tracy, allocation tracing | Assuming templates, virtual dispatch or abstraction are always expensive without inspecting the hot path. |
| C# / .NET | Managed allocation, GC pauses, boxing, copies and engine interop | [dotnet-trace](research.md#r27), [Unity Profiler](research.md#r15), [Unity GC guidance](research.md#r16) | Measuring editor/debug performance as if it were the target release player. |
| Lua | Table creation, allocation, repeated work and engine-call frequency | [Lua manual](research.md#r26); engine profiler; [LuaJIT profiler](research.md#r28) only for LuaJIT | Applying LuaJIT assumptions to the Lua 5.4 runtime used by these tests. |
| GDScript / Godot | Scene/process overhead, allocations, rendering/physics and script time | [Godot profiler](research.md#r07), [CPU](research.md#r04), [GPU](research.md#r05) | Treating a script rewrite as a solution to a GPU bottleneck. |
| JavaScript | Main-thread work, allocation, engine calls and browser rendering | [Node profiling](research.md#r24), [Chrome Performance](research.md#r25) | Mixing Node kernel timings with browser frame/rendering claims. |
| TypeScript | The JavaScript produced after compilation and its runtime workload | The same JS/browser tools | Expecting type annotations to make runtime math automatically faster. |
| Rust | Release profile, allocations, clones, data access and synchronization | [Rust Performance Book](research.md#r21), platform sampling, Tracy integrations where suitable | Assuming ownership safety proves a zero-allocation or parallel-speedup claim. |
| Go | Allocation/escape behavior, GC, goroutine scheduling and contention | [Go diagnostics / pprof / trace](research.md#r22) | Creating a goroutine for every tiny operation. |
| PHP | Request lifetime, serialization, network/database work and repeated parsing | Runtime/hosting profiler and application tracing | Treating request-oriented execution as an already built authoritative real-time game loop. |

Godot profiler coverage can differ by script language. The inspected current documentation specifically directs C# profiling to external .NET tooling; verify the guidance for your installed engine version rather than assuming the script profiler measures every language.

## Build and measurement discipline

Record compiler/runtime/engine version and flags. Compare supported optimized builds. Keep a separate correctness pass with assertions and suitable sanitizers/checkers; instrumentation and checking overhead can distort timing. Do not remove checks merely to match a faster benchmark configuration without a validated safety design.

An optimized build can make variables harder to inspect in a debugger. Retain symbols where supported and use sampling/tracing tools appropriate to the build. A release-build label alone does not prove all assets, shaders or scripts use the expected shipping configuration.

## Interop and representation

Moving a small equation into native code can lose if every call converts arrays, copies buffers or crosses an expensive engine/FFI boundary. Batch enough useful work per crossing while keeping latency and ownership acceptable. Copying the whole map into a movement call can cost more than its directional arithmetic.

The common port interface uses binary64 numbers and numeric IDs to keep fixtures comparable. C uses a fixed-capacity vector; some native algorithms are simple scans or batch forms rather than the Python data structures. Read each mechanic's `PORTS.md` and the [language conventions](../language-ports.md). Do not claim the ports are feature-for-feature identical services or performance-equivalent implementations.

## Engines already do substantial work

Use an engine's physics broad phase, rendering culling, animation system or supported resource cache when appropriate. Reimplementing them in scripts can duplicate work and be slower. An educational standalone algorithm remains useful for understanding rules and testing ideas, but engine integration should respect existing lifecycle and thread boundaries.

For broader architecture reading, see [Game Engine Architecture](research.md#r30). Next: [benchmarking](10-benchmarking.md).
