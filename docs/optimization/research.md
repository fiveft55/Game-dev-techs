# Research materials and further reading

Checked 19 October 2026 (Australia/Sydney). This is an annotated reading list for the handbook, not bundled third-party material. The record contains **38 references: 15 HTTP successes and 23 proxy-blocked requests**. Seven opening excerpts from official/author source files were inspected. An accessible page title alone is not a substantive content review.

Original papers/textbooks are included for theory; official documentation is preferred for APIs/tools; author tutorials explain implementation choices. Publisher pages may refer to paid books. No claim is made that every book/paper is freely accessible, that a blocked page was reviewed, or that every linked tool was installed/tested.

For a beginner, start with R03, R07, R10, R13 and R14. For theory, use R01, R02, R29, R37 and R38. For tools, choose your runtime/engine from chapter 9. Read source-code licenses before copying any external implementation.

“HTTP 200” reports the observed response, not verification of every technical claim, latest version, download or license. “Proxy blocked” records a workspace access limitation, not a judgment that the site is down. GitHub master branches and unversioned documentation can change; consult the release matching your project. [Machine-readable observations](research-links.json) retain individual outcomes and bounded review scopes.

<a id="r01"></a>
## R01 — Amdahl: Validity of the Single Processor Approach (1967)

- Link: [Amdahl: Validity of the Single Processor Approach (1967)](https://doi.org/10.1145/1465482.1465560)
- Type / level: research paper; advanced.
- Learn: Understand why speeding up one part cannot remove costs elsewhere.
- Apply carefully: A fixed-workload upper bound, not an observed speedup for this library.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r02"></a>
## R02 — Williams, Waterman and Patterson: Roofline (2009)

- Link: [Williams, Waterman and Patterson: Roofline (2009)](https://doi.org/10.1145/1498765.1498785)
- Type / level: research paper; advanced.
- Learn: Relate arithmetic work to memory traffic and bandwidth.
- Apply carefully: Hardware ceilings and operational intensity must be measured for the target machine.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r03"></a>
## R03 — Godot: General optimization

- Link: [Godot: General optimization](https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/performance/general_optimization.rst)
- Type / level: official engine documentation; beginner.
- Learn: Start with bottlenecks and an evidence-driven optimization process.
- Apply carefully: Master documentation can differ from your installed stable release.
- Access: HTTP 200; Opening excerpt inspected; not a full-source review.

<a id="r04"></a>
## R04 — Godot: CPU optimization

- Link: [Godot: CPU optimization](https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/performance/cpu_optimization.rst)
- Type / level: official engine documentation; intermediate.
- Learn: Learn CPU profiling and reducing expensive work.
- Apply carefully: Engine examples and APIs are version dependent.
- Access: HTTP 200; Opening excerpt inspected; not a full-source review.

<a id="r05"></a>
## R05 — Godot: GPU optimization

- Link: [Godot: GPU optimization](https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/performance/gpu_optimization.rst)
- Type / level: official engine documentation; intermediate.
- Learn: Learn geometry, shading and fill-rate bottlenecks.
- Apply carefully: A rendering technique useful on one GPU can hurt another.
- Access: HTTP 200; Opening excerpt inspected; not a full-source review.

<a id="r06"></a>
## R06 — Godot: Thread-safe APIs

- Link: [Godot: Thread-safe APIs](https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/performance/thread_safe_apis.rst)
- Type / level: official engine documentation; intermediate.
- Learn: Distinguish worker-safe data processing from engine operations with thread restrictions.
- Apply carefully: Consult the version-specific thread-safety guarantees before touching scenes or resources.
- Access: HTTP 200; Opening excerpt inspected; not a full-source review.

<a id="r07"></a>
## R07 — Godot: The profiler

- Link: [Godot: The profiler](https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/scripting/debug/the_profiler.rst)
- Type / level: official engine documentation; beginner.
- Learn: Read frame traces and inclusive/exclusive script costs.
- Apply carefully: Editor/debug measurements can differ from exported release builds.
- Access: HTTP 200; Opening excerpt inspected; not a full-source review.

<a id="r08"></a>
## R08 — Box2D documentation

- Link: [Box2D documentation](https://box2d.org/documentation/)
- Type / level: official library documentation; intermediate.
- Learn: Study timesteps, contacts, collision queries and real physics-engine constraints.
- Apply carefully: APIs differ substantially between Box2D versions; record the version.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r09"></a>
## R09 — Box2D source repository

- Link: [Box2D source repository](https://github.com/erincatto/box2d)
- Type / level: primary source code; advanced.
- Learn: Inspect a production-oriented 2D collision/physics implementation and its own tests.
- Apply carefully: Read current licensing and build instructions; source is not bundled here.
- Access: HTTP 200; not reviewed.

<a id="r10"></a>
## R10 — Red Blob Games: Introduction to A*

- Link: [Red Blob Games: Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- Type / level: author tutorial; beginner.
- Learn: Compare BFS, Dijkstra and A* using understandable examples.
- Apply carefully: Heuristics and movement costs must match your actual graph.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r11"></a>
## R11 — Gaffer on Games: Fix Your Timestep

- Link: [Gaffer on Games: Fix Your Timestep](https://gafferongames.com/post/fix_your_timestep/)
- Type / level: author technical article; intermediate.
- Learn: Understand fixed updates, interpolation and the spiral of death.
- Apply carefully: A fixed timestep is a stability/consistency technique, not automatically a speed improvement.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r12"></a>
## R12 — Gaffer on Games: State Synchronization

- Link: [Gaffer on Games: State Synchronization](https://gafferongames.com/post/state_synchronization/)
- Type / level: author technical article; intermediate.
- Learn: Study prioritization, state synchronization and network budgeting.
- Apply carefully: This is architecture guidance, not a secure networking implementation.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r13"></a>
## R13 — Game Programming Patterns: Object Pool

- Link: [Game Programming Patterns: Object Pool](https://raw.githubusercontent.com/munificent/game-programming-patterns/master/book/object-pool.markdown)
- Type / level: author book chapter; beginner.
- Learn: Understand reusing objects and bounding a pool.
- Apply carefully: Pools retain memory and require correct reset/ownership rules.
- Access: HTTP 200; Opening excerpt inspected; not a full-source review.

<a id="r14"></a>
## R14 — Game Programming Patterns: Data Locality

- Link: [Game Programming Patterns: Data Locality](https://raw.githubusercontent.com/munificent/game-programming-patterns/master/book/data-locality.markdown)
- Type / level: author book chapter; intermediate.
- Learn: Understand why nearby memory access can beat pointer chasing.
- Apply carefully: Benefits depend on access patterns and runtime object representation.
- Access: HTTP 200; Opening excerpt inspected; not a full-source review.

<a id="r15"></a>
## R15 — Unity: Profiler

- Link: [Unity: Profiler](https://docs.unity3d.com/Manual/Profiler.html)
- Type / level: official engine documentation; beginner.
- Learn: Find frame, CPU, GPU and memory information in Unity tooling.
- Apply carefully: Use documentation matching your Unity version and rendering pipeline.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r16"></a>
## R16 — Unity: Garbage collection best practices

- Link: [Unity: Garbage collection best practices](https://docs.unity3d.com/Manual/performance-garbage-collection-best-practices.html)
- Type / level: official engine documentation; intermediate.
- Learn: Spot allocations that can cause frame-time spikes.
- Apply carefully: Editor, Mono and IL2CPP behavior can differ; measure the target player.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r17"></a>
## R17 — Epic: Unreal Insights

- Link: [Epic: Unreal Insights](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-in-unreal-engine)
- Type / level: official engine documentation; intermediate.
- Learn: Use traces to reason about tasks, timings and resource usage.
- Apply carefully: Trace configuration and engine version affect available events.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r18"></a>
## R18 — NVIDIA: Nsight Graphics

- Link: [NVIDIA: Nsight Graphics](https://developer.nvidia.com/nsight-graphics)
- Type / level: official tool documentation; advanced.
- Learn: Inspect GPU captures and hardware performance bottlenecks.
- Apply carefully: Check supported GPUs/APIs; vendor-specific results do not generalize automatically.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r19"></a>
## R19 — RenderDoc

- Link: [RenderDoc](https://github.com/baldurk/renderdoc)
- Type / level: primary tool repository; intermediate.
- Learn: Capture a rendered frame and inspect draws, resources and state.
- Apply carefully: Frame capture is not a substitute for all timing measurements; platform/API support varies.
- Access: HTTP 200; not reviewed.

<a id="r20"></a>
## R20 — Tracy profiler

- Link: [Tracy profiler](https://github.com/wolfpld/tracy)
- Type / level: primary tool repository; advanced.
- Learn: Instrument CPU timelines, allocations and supported GPU workloads.
- Apply carefully: Instrumentation has overhead and requires correct build/runtime integration.
- Access: HTTP 200; not reviewed.

<a id="r21"></a>
## R21 — The Rust Performance Book

- Link: [The Rust Performance Book](https://github.com/nnethercote/perf-book)
- Type / level: author book repository; intermediate.
- Learn: Learn profiling, allocation and representation tradeoffs in Rust.
- Apply carefully: Inspect current chapters; release builds and representative workloads are essential.
- Access: HTTP 200; not reviewed.

<a id="r22"></a>
## R22 — Go: Diagnostics

- Link: [Go: Diagnostics](https://go.dev/doc/diagnostics)
- Type / level: official language documentation; intermediate.
- Learn: Choose Go profiling and tracing tools, including pprof.
- Apply carefully: Measure scheduling, allocation and GC as well as function time.
- Access: HTTP 200; not reviewed.

<a id="r23"></a>
## R23 — Python: The Python Profilers

- Link: [Python: The Python Profilers](https://docs.python.org/3/library/profile.html)
- Type / level: official language documentation; beginner.
- Learn: Use cProfile/profile and understand profiling overhead.
- Apply carefully: Function profiling and timing answer different questions.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r24"></a>
## R24 — Node.js: Profiling

- Link: [Node.js: Profiling](https://nodejs.org/en/learn/getting-started/profiling)
- Type / level: official runtime documentation; intermediate.
- Learn: Inspect CPU work in V8/Node applications.
- Apply carefully: Browser JavaScript needs browser tooling; Node results do not represent rendering performance.
- Access: HTTP 200; not reviewed.

<a id="r25"></a>
## R25 — Chrome DevTools: Performance

- Link: [Chrome DevTools: Performance](https://developer.chrome.com/docs/devtools/performance)
- Type / level: official tool documentation; beginner.
- Learn: Inspect browser main-thread work, rendering and long tasks.
- Apply carefully: CPU throttling is an approximation, not a replacement for testing actual devices.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r26"></a>
## R26 — Lua 5.4 Reference Manual: Garbage collection

- Link: [Lua 5.4 Reference Manual: Garbage collection](https://www.lua.org/manual/5.4/manual.html#2.5)
- Type / level: official language manual; intermediate.
- Learn: Understand Lua memory management and available collector behavior.
- Apply carefully: Lua 5.4 and LuaJIT are different runtimes; tuning is not interchangeable.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r27"></a>
## R27 — Microsoft: dotnet-trace

- Link: [Microsoft: dotnet-trace](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-trace)
- Type / level: official runtime documentation; intermediate.
- Learn: Collect runtime traces for allocation, GC and application activity.
- Apply carefully: Engine-embedded .NET runtimes may need engine-specific tools.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r28"></a>
## R28 — LuaJIT: Integrated profiler

- Link: [LuaJIT: Integrated profiler](https://luajit.org/ext_profiler.html)
- Type / level: official runtime documentation; intermediate.
- Learn: Profile code when your actual runtime is LuaJIT.
- Apply carefully: The repository Lua checks use Lua 5.4, not LuaJIT; no LuaJIT speed claim is made.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r29"></a>
## R29 — Introduction to Algorithms, fourth edition

- Link: [Introduction to Algorithms, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
- Type / level: textbook publisher page; advanced.
- Learn: Study complexity, graph algorithms, heaps, hashing and amortized analysis.
- Apply carefully: A publisher/book reference, not a claim of freely available full text.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r30"></a>
## R30 — Game Engine Architecture

- Link: [Game Engine Architecture](https://www.gameenginebook.com/)
- Type / level: author book site; advanced.
- Learn: Study engine subsystems, memory, scheduling and production architecture.
- Apply carefully: Check the edition; specific hardware/API details age.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r31"></a>
## R31 — GPU Gems 3, Chapter 32: Broad-Phase Collision Detection

- Link: [GPU Gems 3, Chapter 32: Broad-Phase Collision Detection](https://developer.nvidia.com/gpugems/gpugems3/part-v-physics-simulation/chapter-32-broad-phase-collision-detection)
- Type / level: vendor technical book chapter; advanced.
- Learn: Study spatial subdivision and broad-phase collision design.
- Apply carefully: A historical technical chapter; adapt architecture and GPU assumptions to current hardware.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r32"></a>
## R32 — Recast and Detour navigation

- Link: [Recast and Detour navigation](https://github.com/recastnavigation/recastnavigation)
- Type / level: primary source code; advanced.
- Learn: Inspect navigation-mesh generation, path queries and crowd-related components.
- Apply carefully: Integration, agent geometry and dynamic world behavior need separate validation.
- Access: HTTP 200; not reviewed.

<a id="r33"></a>
## R33 — RFC 9000: QUIC

- Link: [RFC 9000: QUIC](https://www.rfc-editor.org/rfc/rfc9000)
- Type / level: Internet standard; advanced.
- Learn: Understand transport flow/congestion control and stream behavior.
- Apply carefully: Choose a maintained implementation; a transport standard is not a game replication design.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r34"></a>
## R34 — Agner Fog: Software optimization resources

- Link: [Agner Fog: Software optimization resources](https://www.agner.org/optimize/)
- Type / level: author technical manuals; advanced.
- Learn: Study low-level CPU execution and instruction considerations.
- Apply carefully: Primarily x86-focused; not a universal model for ARM, mobile GPUs or managed runtimes.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r35"></a>
## R35 — LZ4 compression library

- Link: [LZ4 compression library](https://github.com/lz4/lz4)
- Type / level: primary source code; advanced.
- Learn: Evaluate compression/decompression tradeoffs for suitable data.
- Apply carefully: Measure payload size, CPU cost and latency together; compression is not encryption.
- Access: HTTP 200; not reviewed.

<a id="r36"></a>
## R36 — W3C WebGPU specification

- Link: [W3C WebGPU specification](https://www.w3.org/TR/webgpu/)
- Type / level: graphics standard; advanced.
- Learn: Understand the explicit browser GPU API model.
- Apply carefully: A specification, not a beginner optimization recipe or universal browser-support promise.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r37"></a>
## R37 — Gustafson: Reevaluating Amdahl's Law (1988)

- Link: [Gustafson: Reevaluating Amdahl's Law (1988)](https://doi.org/10.1145/42411.42415)
- Type / level: research paper; advanced.
- Learn: Understand why scaling workload size changes the parallel-speedup question.
- Apply carefully: Scaled-workload reasoning does not prove lower latency for a fixed frame workload.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

<a id="r38"></a>
## R38 — Little: A Proof for the Queuing Formula L = lambda W (1961)

- Link: [Little: A Proof for the Queuing Formula L = lambda W (1961)](https://doi.org/10.1287/opre.9.3.383)
- Type / level: research paper; advanced.
- Learn: Relate average arrivals, average queued work and average time in a stable system.
- Apply carefully: An average steady-state relation, not a bound on worst-case latency.
- Access: blocked by the workspace proxy (403); content not reviewed here. Curated reading suggestion, not a verified-content citation.

## Reusing outside material

Linking a paper, tutorial or repository does not relicense it under this project's MIT license. Preserve upstream terms and attribution when importing permitted code. Treat figures, text, art, fonts and game assets separately. Summaries in this handbook are original explanations; full source captures were kept outside the repository for inspection and were not bundled. See the [source policy](../sources.md).
