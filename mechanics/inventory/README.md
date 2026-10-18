# Inventory stacking

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Put items into piles without making any pile or backpack too full.

1. Fill existing piles of the same item first.
2. Put leftover items into new piles while free backpack slots remain.
3. Never put more than the pile limit into one pile.
4. Return the new piles and how many items could not fit. Item numbers are labels, not quantities.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

Merge stackable items to a per-stack cap and return overflow when capacity is exhausted. Item IDs must be stable data identifiers, not user-controlled filesystem paths.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
