# Simulation clock

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Make the game take equal-sized time steps, even when the screen draws at different speeds.

1. Imagine a bucket collecting seconds as the game runs.
2. Take one scoop of time for each game update.
3. Keep the leftover time for the next update.
4. After a big pause, throw away excess time so the game does not spend forever catching up.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

Separate simulation steps from rendering. Carry fractional time forward; cap accumulated time to avoid a spiral of death. Dropping excess time deliberately slows simulation after stalls. Never use this clamp for an authoritative wall-clock timer.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.

## Optimization reading

See [the relevant optimization chapter](../../docs/optimization/04-collision-physics.md) and [the current-code cost audit](../../docs/optimization/mechanics-audit.md). Suggested improvements are not automatically implemented or benchmarked here.
