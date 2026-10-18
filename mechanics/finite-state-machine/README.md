# Finite state machine

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Let a character switch between named situations, such as idle and jumping, using clear rules.

1. Keep one current state, represented here by a number.
2. Read the next event, such as a jump button press.
3. Find a rule matching the current state and that event.
4. Switch to the rule destination. If no rule matches, keep the old state.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

Represent legal transitions explicitly. Animation, enemy AI, and UI screens can share this pattern. Side effects and hierarchical states need additional design.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
