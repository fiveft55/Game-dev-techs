# 1. Measure first

Imagine a restaurant where food is late because the oven is full. Buying a faster cash register will not fix dinner. A game has the same problem: improve the part that is actually making the player wait.

## Frame budget and responsiveness

A frame budget is the time available to prepare the next displayed picture. `budget_ms = 1000 / target_fps`:

| Target | Approximate budget |
|---|---|
| 30 FPS | 33.33 ms |
| 60 FPS | 16.67 ms |
| 120 FPS | 8.33 ms |

These are arithmetic targets, not guarantees. CPU and GPU work can overlap across frames; they are not always a simple sum. Synchronization, present queues and display refresh also affect when a picture appears. A GPU-bound game may gain nothing from a CPU-only optimization. A faster frame rate can still coexist with poor input latency if too much work is queued.

Record individual frame times. Report median, p95 and p99 frame time, worst observed frame, sample duration and sample count. A p99 is meaningful only with enough observations and a clearly defined sampling method. An average FPS can hide repeated long pauses. Separate loading/compilation warm-up from steady play, but also measure startup if startup is a product requirement.

## What to measure

| Symptom | Inspect first | Common mistaken conclusion |
|---|---|---|
| Spikes during enemy spawning | Allocations, resource creation, initialization and GC | “The movement equation is slow.” |
| Looking at one area tanks FPS | GPU capture, overdraw, draw submission, lights and effects | “More simulation threads will fix it.” |
| Many units choose paths at once | Path requests, expanded nodes, allocations and map changes | “Every unit needs its own thread.” |
| Online play feels delayed | Server tick time, RTT, jitter, loss, queues and interpolation delay | “Encrypting less will make this acceptable.” |
| Long session memory growth | Object ownership, retained references, caches and resource lifetimes | “GC will eventually fix it.” |

Use counters as well as time: entities updated, collision candidates, exact tests, path nodes expanded, allocations/bytes, draw calls, triangles, visible chunks, serialized bytes, retransmissions and database queue depth. Counters explain why timing changed.

## Profiling workflow

1. Make a representative replay or fixed input script. Include the problem area and worst plausible content density.
2. Build the configuration you intend to ship. Keep symbols or an appropriate development build for profiling.
3. Capture an end-to-end timeline. Identify CPU, GPU, I/O, allocation, synchronization or network limits.
4. Inspect the expensive region. **Inclusive time** includes called work; **exclusive time** excludes it. Avoid adding inclusive times together and counting the same work twice.
5. Change one hypothesis at a time. Rerun both correctness checks and measurements.
6. Save the baseline, candidate, device/build details, distributions and workload with the result.

Sampling profilers periodically inspect running stacks. Instrumentation records chosen events. Both have overhead; short functions and heavily instrumented runs can be misleading. A stopwatch around a function measures elapsed time including waits; CPU time answers a different question. GPU work is asynchronous, so CPU time around a draw submission does not measure the GPU's complete rendering time.

## Target-device discipline

Test mobile builds on actual devices and sustained workloads: thermal throttling and battery limits can change results after minutes. Record resolution, graphics settings, CPU/GPU, memory, OS/runtime/compiler, power mode and background activity. Browser, editor, exported game, debug and release results are distinct. Do not compare two languages by timing one optimized native build against another language's editor/debug run.

Read: [Godot optimization](research.md#r03), [Godot profiler](research.md#r07), [Unity Profiler](research.md#r15), [Unreal Insights](research.md#r17), [Tracy](research.md#r20). Next: [theory](02-theory.md).
