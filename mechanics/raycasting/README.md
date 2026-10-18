# Grid ray traversal

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Send an invisible straight line through a tile map and report the first wall it hits.

1. Start the line at a position and choose its direction.
2. Calculate which tile edge the line will cross next.
3. Move into that next tile and check whether it is a wall.
4. Stop at a wall, the map edge, or the step limit. The returned time-like number tells how far along the line the hit occurred.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

Traverse grid cells along a ray with the digital differential analyzer. The direction need not be normalized: returned t is a ray parameter, not distance unless direction has unit length. Corner ties choose the Y axis first.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
