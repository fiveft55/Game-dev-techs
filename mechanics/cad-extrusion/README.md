# CAD-style profile extrusion

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Give a flat outline height to make a simple solid-looking 3D shape.

1. Copy the outline at floor height and at the requested top height.
2. Cover the bottom and top with triangles.
3. Connect matching bottom and top edges with more triangles.
4. Return points and triangle point-numbers. The outline must be simple, convex, and listed counterclockwise.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

Extrude a convex counterclockwise 2D polygon into a triangle mesh. This demonstrates geometry generation, not a CAD kernel. Inputs must be a simple convex profile without duplicate vertices; robust polygon validation and boolean operations are out of scope.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
