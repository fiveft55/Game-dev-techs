# Level editor undo/redo

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Let a map editor undo and redo painting a tile.

1. Before painting, remember the old tile and the new tile.
2. Undo restores the old tile and moves backward in the edit history.
3. Redo puts the new tile back and moves forward.
4. Painting after undo throws away the abandoned future edits.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

Model an edit as a command that stores the previous tile. A new edit clears the redo branch. This minimal in-memory editor has no file import, asset pipeline, UI, or collaboration.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
