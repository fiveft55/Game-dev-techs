# 4. Collision and physics

Before asking “do these two shapes touch?”, ask “which pairs are even worth checking?” That division is broad phase versus narrow phase.

## Broad phase: reduce possible pairs

| Structure | Useful situation | Costs and failure cases |
|---|---|---|
| Uniform grid / spatial hash | Similar-sized objects in a fairly even world | Cell-size tuning, moving-object updates and dense-cell worst cases. |
| Sweep and prune | Objects move coherently along a useful axis | Sorting/maintenance, bad distributions and teleportation. |
| Dynamic AABB tree | Varied sizes and many region/ray queries | Tree maintenance, traversal overhead and balancing policy. |
| Quadtree / octree | Hierarchical spatial subdivision | Objects crossing nodes, uneven density, update complexity. |

Do not adopt a hierarchy merely because its name sounds advanced. A small scene can be cheaper with a direct scan. Measure rebuild/update cost **plus all queries**, not just a query with a free prebuilt structure.

The Python [spatial hash](../../mechanics/spatial-hash/README.md) builds actual dictionary buckets. `nearby` checks nine cells. That is suitable only for the documented point-neighborhood contract: querying a larger radius needs more cells. For finite-size shapes, insert them into every overlapped cell or use another conservative scheme, then deduplicate candidate pairs. Choosing cells by object center alone can miss large-shape collisions.

The native spatial-hash kernels scan every point and filter cell coordinates. They illustrate candidate selection but do not retain an indexed hash table, so their per-query cost is still O(n). Do not cite them as an already optimized broad-phase implementation.

## Narrow phase and continuous movement

[AABB overlap](../../mechanics/aabb-collision/README.md) is a constant-size rectangle test. [Swept projectiles](../../mechanics/projectile-sweep/README.md) find whether a moving point crosses a stationary rectangle over a step, avoiding some tunneling that endpoint tests miss. A point sweep does not solve arbitrary rotating/accelerating body collisions. If a broad phase rejects the pair, the narrow phase never gets a chance: candidate generation must be conservative.

For repeated point-distance comparisons, squared distances can avoid square roots when you only need ordering or a radius test. Keep units consistent: compare squared distance against squared radius. Extremely large values can overflow or lose precision; this substitution is not automatically numerically safe for every input domain.

## Simulation budget and stability

[Fixed timesteps](../../mechanics/fixed-timestep/README.md) make update intervals predictable. They do not make an expensive solver cheap. More substeps or solver iterations can improve stability/contacts but cost more. Lowering them may change stacking, fast-body hits, constraints or game feel.

Keep physics state separate from render interpolation. Sleeping inactive bodies, sensible collision layers/masks and avoiding unnecessary contacts can reduce work without reducing every body's accuracy. Wake rules and interaction correctness need testing. Do not update authoritative physics at a distance-dependent rate without considering tunneling and fairness.

The point-mass [integrator](../../mechanics/rigid-body-integration/README.md) in this library has no contact solver, sleeping system or broad phase. Those are future engine integrations, not hidden capabilities of the example.

## What to verify

Record active bodies, candidate pairs, accepted contacts, solver time, substeps and worst-density scenes. Check negative coordinates, cell boundaries, large bodies, fast objects, teleportation, duplicate pair generation and objects moving between cells. Compare true contacts with a trusted brute-force oracle on small scenes before trusting performance results.

Read [Box2D docs](research.md#r08), [Box2D source](research.md#r09) and [GPU Gems broad phase](research.md#r31). Next: [movement and AI](05-movement-ai.md).
