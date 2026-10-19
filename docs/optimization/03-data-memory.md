# 3. Data, allocation and memory

A store worker finds things faster when related products are together and the shelves are labeled. Programs often benefit from the same organization.

## Lifetime before clever containers

Decide who owns each object and when it can be destroyed. Track peak and steady memory, temporary allocation rate and retained resources. A resource leak is not solved by a faster allocator. Garbage-collected programs can still retain unused objects through event handlers, caches and static references.

Prefer reusing a correctly sized temporary buffer in a measured hot path over constructing many short-lived lists. Do not share that buffer with a renderer, job or network send that still reads it. Ownership is part of correctness.

## Object pooling

A pool keeps a bounded collection of reusable objects, often projectiles or particles. Acquire an inactive slot, reset all state, use it, then release it.

Good candidates have frequent creation/destruction and meaningful allocation or engine-resource initialization costs. Pooling can reduce spikes; it can also retain too much memory, complicate lifetime, hide stale state and add bookkeeping. Modern allocators or collectors may already handle small objects well.

Specify exhaustion policy: reject a cosmetic effect, grow within a cap, or deliberately reserve gameplay-critical capacity. Never silently drop a damaging projectile because the cosmetic pool was full. Reset timers, owner/team IDs, subscriptions, physics state and visual state. Consider a generation counter on reused IDs so an old reference cannot accidentally refer to a new occupant. Read [Object Pool](research.md#r13).

## Array of structs and structure of arrays

An array of structs keeps each entity's fields together: `{x,y,vx,vy,health}` repeated. A structure of arrays keeps `x[]`, `y[]`, `vx[]`, `vy[]`, `health[]` separately.

Use the access pattern to choose. A loop updating only positions and velocities may avoid loading health with SoA. A routine needing all fields of one entity may prefer AoS. Synchronizing several arrays creates new failure modes; a component-based design is not automatically cache-friendly. Sorting or compacting entities can invalidate stored indices. Stable IDs and explicit indirection are sometimes worth their cost.

The native kernels here use numeric arrays for shared fixtures and simple interfaces, not because that layout has been benchmarked as best. JS arrays, Python lists, Lua tables, Go slices, Rust vectors and C buffers have different representations. Identical-looking source does not imply identical cache behavior.

## SIMD, numerical shortcuts and precision

SIMD performs the same kind of operation on several values together. Contiguous independent position/velocity data can suit vectorized loops; scattered accesses, branches and small batches can reduce the benefit. Auto-vectorization depends on compiler, target instructions, aliasing and build options. Inspect generated code and measure the complete loop rather than assuming an array is vectorized.

Changing precision, using a lookup table or enabling aggressive floating-point transformations can change results. Define permitted position/angle error, overflow behavior and deterministic-replay requirements first. A lookup table uses memory and interpolation work; it is not automatically faster than the platform math implementation. Do not enable unsafe arithmetic assumptions simply to make tests faster.

## Caches and bounded resources

For path results, key by start/goal, movement capabilities and relevant map version. For meshes, key by geometry/material inputs and revision. Invalidate or rebuild affected entries when inputs change. Limit total bytes and define eviction, not just maximum item count.

A cache should report hit rate, miss cost, maintenance time and memory. A high hit rate on a trivial computation may save nothing. A low hit rate on a huge mesh build might still be worthwhile. Avoid pointer/object identity as a content key when semantically identical inputs should share a result.

## Actual library costs to notice

- [Inventory](../../mechanics/inventory/README.md) copies the stack list rather than mutating the caller's list. That makes failure/ownership easy to reason about, but copying has a cost.
- [Rollback](../../mechanics/rollback-resimulation/README.md) deep-copies state. Larger state and longer history increase memory and replay work.
- [Grid movement](../../mechanics/grid-movement/README.md) performs event-driven stepping, but its Python wrapper packs the full map into a fresh input list every call. Persistent map references are a potential optimization for an engine adapter.
- C kernels return a fixed-capacity `PortVector` by value. This is a teaching interface, not a claim that copying a large buffer is optimal. See [language conventions](../language-ports.md) before changing ABI/capacity.

Optimize these only after measuring realistic sizes. Reserve/reuse, immutable sharing or a smaller typed interface can help; each changes ownership and must preserve tests. Next: [collision and physics](04-collision-physics.md).
