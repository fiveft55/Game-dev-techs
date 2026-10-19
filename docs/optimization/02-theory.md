# 2. Theory that helps you choose

Theory predicts where an approach might fail. Measurements tell you whether that prediction matters in your game.

## Complexity: how work grows

`n` means the number of things involved. Big-O describes a growth bound, not milliseconds and not a guarantee about small inputs.

| Growth | Everyday picture | Game example |
|---|---|---|
| O(1) | One fixed-size calculation | Move one point or compare two boxes. |
| O(log n) | Repeatedly narrow the search | Find an animation frame in sorted cumulative times. |
| O(n) | Visit each thing once | Update all active actors. |
| O(n log n) | Sort a collection efficiently | Sort an initial initiative list. |
| O(n²) | Compare every thing with every other thing | Naive pair collision candidates. |

There are `n(n-1)/2` unordered pairs: 1,000 actors imply 499,500 pairs. A spatial index can reduce candidate work for spread-out objects, but a crowd in one small cell can still approach quadratic work. Hash-table access is usually average/amortized constant time under suitable assumptions; it is not an unconditional worst-case promise.

Use the variables that match the problem. BFS takes O(V+E) time for visited vertices and edges. A grid of bounded-degree cells gives O(V) worst-case traversal, plus storage. A* can explore fewer cells with a useful heuristic, but heap overhead and a poor heuristic can erase gains. “A* is faster” is not a universal theorem.

## Amdahl's law: optimize a meaningful fraction

For a fixed workload, if fraction `p` can be sped up by factor `s`, the ideal total speedup is:

`1 / ((1-p) + p/s)`.

Illustration: improving 10% of a frame by 10× gives `1/(0.9+0.01) ≈ 1.10×` overall, before extra overhead. Perfectly eliminating that 10% still cannot exceed about 1.11×. This is why a heavily optimized tiny movement function may not improve a rendering-bound game.

Parallel work has coordination, scheduling and synchronization costs. Gustafson's scaled-workload view asks a different question: how much **larger** a workload can run in a similar time as resources grow? It does not guarantee lower latency for the original fixed game frame. Read [Amdahl](research.md#r01) and [Gustafson](research.md#r37).

## Locality and the Roofline idea

A CPU fetches memory in chunks called cache lines. Repeatedly walking compact data can reuse fetched bytes; chasing separate heap objects may wait for scattered memory. The exact result depends on hardware, representation and access patterns.

At a chosen memory level, Roofline relates useful operations per byte transferred to achievable performance. A simplified ceiling is `min(peak_compute, memory_bandwidth × operational_intensity)`. A loop waiting on memory may benefit more from moving fewer bytes than from using fewer arithmetic instructions. This model needs measured or defensible hardware/workload parameters; it is not a benchmark result by itself. See [Roofline](research.md#r02) and [Data Locality](research.md#r14).

## Amortization and spreading work

Growing a dynamic array occasionally costs a copy, yet appending can be cheap on average over many operations. Games must also care about the expensive individual append that lands in a visible frame. Reserving a sensible capacity can move that cost earlier, at the price of retained memory.

Spread independent expensive jobs across updates when the rules permit it: a faraway NPC may think less frequently than the local player's collision controller. This trades freshness for frame-time consistency. Define a maximum permitted delay; do not silently make important enemies stop reacting.

## Queues, throughput and latency

Throughput is how much work finishes per second. Latency is how long one item waits. Larger batches can improve throughput while making one input wait longer. Little's law, under appropriate stable average conditions, relates average items in a system to arrival rate times average time: `L = lambda × W`. It does not predict a worst-case frame or bound a burst. If producers indefinitely outpace consumers, adding a queue hides overload until memory or latency fails. Use backpressure and budgets. See [Little](research.md#r38).

## Reuse work instead of repeating it

Cache a path, visibility result or mesh only when you can identify when it becomes stale. Each cache needs a key, invalidation rule, size budget and ownership. If computing the key, checking validity and maintaining the cache costs more than recomputing, the cache is a loss.

Approximation is a separate design choice. LOD, quantized snapshots and lower-frequency AI can save work by accepting less detail or freshness. Specify an acceptable error and test the gameplay consequence. Read [algorithm foundations](research.md#r29); next: [data and memory](03-data-memory.md).
