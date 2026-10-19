# Grid pathfinding

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Find the shortest walking route through a small square-tile map.

1. Start on the player tile and put it in a waiting line.
2. Check nearby tiles: right, left, down, and up. Skip walls and already checked tiles.
3. Remember which tile led to each new tile.
4. When the target is found, follow those memories backward and reverse them to get the route.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

Breadth-first search finds a shortest path with equal-cost four-way movement. Return an empty list when unreachable. Weighted terrain requires Dijkstra or A*, not this algorithm.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.

## Optimization reading

See [the relevant optimization chapter](../../docs/optimization/05-movement-ai.md) and [the current-code cost audit](../../docs/optimization/mechanics-audit.md). Suggested improvements are not automatically implemented or benchmarked here.
