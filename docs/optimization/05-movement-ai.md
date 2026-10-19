# 5. Movement, AI and gameplay work

An enemy does not need to ask every question every frame. It does need to answer important questions soon enough for the game rules.

## Free movement and grid movement stay separate

[Free movement](../../mechanics/player-movement/README.md) normalizes direction and integrates position. It is fixed-size math. Avoid optimizing this tiny function while ignoring thousands of path searches, render objects or map copies.

[Grid movement](../../mechanics/grid-movement/README.md) waits for tile arrivals, input-repeat times and buffered turns. Preserve its event ordering, exact landings and input semantics when changing performance. Its native state must be retained between calls. Packing an unchanged map each frame can dominate the small controller calculation; an engine wrapper can keep a map reference instead. That adapter is a suggestion, not an implemented change here.

## Navigation: choose the right question

The existing [BFS](../../mechanics/grid-pathfinding/README.md) is appropriate for equal-cost four-way grids. Dijkstra handles nonnegative variable edge costs. A* guides search with a heuristic; admissible/consistent heuristics and graph-search details determine optimality guarantees. Manhattan distance suits four-way unit-cost movement, not every diagonal, weighted, teleport or portal graph.

For many actors sharing a destination, a reverse distance/flow field may reuse work better than one search per actor. Hierarchical navigation can reduce large-world search, with refinement and boundary costs. Navmeshes change the graph representation, not the need to model agent size and movement rules.

Practical options:

1. Repath only when the goal or relevant world state changes enough.
2. Give requests priorities and a per-tick work budget.
3. Reuse storage for visited/predecessor data when ownership permits.
4. Cache validated routes with map/capability versions.
5. Spread nonurgent searches across ticks; define what an actor does while waiting.

Do not treat a time-sliced partial search as a completed path. Avoid starving low-priority actors indefinitely. Read [A*](research.md#r10) and [Recast/Detour](research.md#r32).

## Perception and thinking frequency

Use a cheap candidate/range filter before expensive [line-of-sight](../../mechanics/line-of-sight/README.md) checks. An object behind the camera can still affect gameplay; rendering visibility is not AI relevance. Caching visibility needs invalidation for observer/target movement, doors and changed obstacles.

Stagger faraway NPC decisions, but keep a maximum reaction delay. Important combat actors may need the authoritative tick rate. Measure perception queries, candidates, LOS traversals, path searches and decision latency. A “faster” AI that never notices the player is broken.

## Timers, waves and discrete events

Use the [wave spawner](../../mechanics/wave-spawner/README.md), [scheduler](../../mechanics/event-scheduler/README.md) or [cooldown](../../mechanics/ability-cooldown/README.md) patterns to avoid unnecessary polling where events are sparse. A heap helps incremental time ordering; a tiny list may be cheaper. The native scheduler uses insertion sorting for a batch and is not the same complexity as the Python heap service.

Hitch recovery can make many events due at once. Set a budget and an explicit backlog policy. Dropping cosmetic particles is different from dropping damage, crafting completion or authoritative actions.

## Animation, puzzles and generation

Sample sprite animation from an elapsed clock rather than repeatedly scanning every frame, where cumulative-duration lookup fits. Pooling visual effects may reduce allocation spikes, but measure retained memory. For match puzzles, tracking dirty rows/columns can avoid full-board scans; prove that intersections, cascades and gravity still produce the correct board.

Generate large mazes/meshes off the critical frame path or in bounded chunks. A seed makes a particular generator repeatable; changing algorithms, random sequences or task order can change the world. Preserve save/world-version compatibility deliberately. ## UI, input and audio

Update UI elements when their displayed values change rather than rebuilding every label/layout every simulation tick, if the engine supports that pattern. Account for localization, font/theme changes, resizing and accessibility settings when caching layout or text. Measure layout, text shaping, resource updates and draw work separately.

Keep input collection responsive and timestamps trustworthy. Reducing expensive AI frequency is different from ignoring local button transitions. In a rhythm game, preserve the audio-clock basis and calibration rather than judging notes from a convenient render-frame clock.

For audio, prioritize and bound voices/effects when product rules allow, and measure mixing, decode/streaming and resource changes. Avoid unnecessary creation of audio objects in hot paths. Respect the audio system's real-time/thread restrictions; a lock or blocking I/O on an audio callback can cause glitches. This library provides timing examples, not an audio engine.

Next: [rendering and worlds](06-rendering-worlds.md).
