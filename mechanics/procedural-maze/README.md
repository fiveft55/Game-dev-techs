# Procedural maze generation

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Build a new maze by digging paths through a wall-filled map.

1. Fill the map with walls and open one starting square.
2. Pick a nearby unopened room using a repeatable number generator.
3. Break the wall between the old room and the new room.
4. When stuck, walk back through the remembered rooms until another path can be dug.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

Depth-first randomized carving creates a connected perfect maze on an odd-sized grid. A local seeded RNG makes results repeatable within the chosen implementation. Different language RNGs need not produce identical maps.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
