# Game mechanics optimization handbook

**Make the game do less unnecessary work, then measure whether the player benefits.** That is the central idea. A clever-looking algorithm is not proof of a faster game.

This handbook covers CPU time, memory, physics, movement, AI, rendering, worlds, networking, persistence, concurrency and language/runtime choices. Explanations start in plain English and then introduce the theory. Examples refer to this repository's actual code. Techniques described here are recommendations unless the [mechanics audit](mechanics-audit.md) explicitly identifies an existing implementation.

This is a broad practical reference, not every optimization ever published. No game performance benchmark was run for this documentation update. Numerical examples are arithmetic illustrations, not measured speedups. Use the experiment recipe before making performance claims about your own game.

## Chapters

| Chapter | What you will learn |
|---|---|
| [1. Measure first](01-measurement.md) | Find the slow part, choose budgets, read frame times and compare builds fairly. |
| [2. Useful theory](02-theory.md) | Complexity, Amdahl's law, memory locality, Roofline, amortized work and queueing. |
| [3. Data and memory](03-data-memory.md) | Pools, allocation, layouts, caching, handles and lifetime. |
| [4. Collision and physics](04-collision-physics.md) | Broad phases, spatial partitions, swept tests, timesteps and solver budgets. |
| [5. Movement, AI and gameplay](05-movement-ai.md) | Free/grid movement, navigation, visibility, scheduling, animation and procedural work. |
| [6. Rendering and worlds](06-rendering-worlds.md) | CPU/GPU bottlenecks, culling, batching, LOD, chunks and streaming. |
| [7. Networking and persistence](07-networking-persistence.md) | Interest sets, snapshot budgets, compression, rollback, databases and save work. |
| [8. Concurrency](08-concurrency.md) | Jobs, dependencies, contention, determinism and background work. |
| [9. Language and engine tools](09-language-tools.md) | Practical advice for the languages in this library and their profilers. |
| [10. Benchmark recipe](10-benchmarking.md) | Reproducible experiments, correctness gates and a result template. |
| [11. Audit of all 51 mechanics](mechanics-audit.md) | What the current code really does, its costs and likely next improvements. |
| [Research and reading list](research.md) | 38 annotated primary/official references, books, papers and tutorials. |

## Choose a learning path

- **New to coding:** read chapters 1 and 3, then the free/grid movement section in chapter 5. Use the [beginner glossary](../beginner-guide.md).
- **A game stutters:** read chapters 1 and 10, then examine allocation/GC in chapter 3 and streaming in chapter 6.
- **Too many enemies or projectiles:** read chapters 4 and 5. Profile before introducing a pool or spatial index.
- **Large world or multiplayer:** read chapters 6–8. Track memory, bandwidth and queues as well as CPU time.
- **Studying the mathematics:** read chapter 2 and its original paper references; then test one prediction with chapter 10.

## Four questions before changing code

1. What is too slow or too large **on the target device**?
2. Which measured subsystem contributes most to that problem?
3. What exact change should reduce that cost, and what extra cost might it introduce?
4. How will you show the gameplay result is still correct?

Do not remove validation, network authentication, collision correctness or gameplay rules simply to make a timing number look better. A faster wrong result is a different program.

## How references were handled

Read [research.md](research.md) for access and review status. HTTP success means a link responded, not that its entire content was reviewed. Some sites were blocked by the workspace's proxy; those references remain clearly identified reading suggestions. Accessible official/author material was inspected in bounded excerpts. No third-party full text, book, paper, engine or asset was copied into this repository.
