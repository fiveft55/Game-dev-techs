# Axis-aligned rectangle collision

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Tell whether two upright rectangular boxes touch or overlap.

1. Look at the left and right edges of both boxes.
2. Look at the top and bottom edges too.
3. If there is a gap on either side-to-side or up-and-down check, they do not touch.
4. Return one for touching and zero for separate. Touching edges count.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

Use intervals on each axis. This version treats touching edges as contact. Rectangles are (x, y, width, height), with nonnegative dimensions. Fast bodies need swept tests or substeps to prevent tunneling.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
