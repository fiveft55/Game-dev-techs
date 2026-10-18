# Spatial hashing

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Find nearby objects by grouping their positions into imaginary square boxes.

1. Choose the size of each imaginary box.
2. Work out which box contains the search position.
3. Find objects in that box or any of its eight neighboring boxes.
4. These are possible neighbors, not guaranteed touching objects. Check exact distance afterward.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

Bucket point entities into uniform cells for broad-phase neighbor queries. This returns candidates; exact distances and shape collisions require a narrow-phase check.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
