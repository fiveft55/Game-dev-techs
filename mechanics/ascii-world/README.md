# ASCII world rendering

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Draw a tiny world using keyboard characters instead of pictures.

1. Read the map one row at a time.
2. Turn a floor tile into a dot and a wall tile into a hash sign.
3. Put an at sign where the player stands.
4. Put a new line between rows. The native ports return character numbers: 46 is dot, 35 is hash, and 64 is at sign.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

Keep tile data separate from its visual representation. ASCII works in terminals and is useful for prototyping maps without art assets. This renderer intentionally does not handle terminal control sequences or Unicode display widths.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
