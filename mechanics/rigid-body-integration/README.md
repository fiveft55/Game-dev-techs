# Gravity and integration

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Update a moving point when a force-like acceleration, such as gravity, changes its speed.

1. Start with position and speed in each direction.
2. Acceleration changes speed during the time step.
3. Use the new speed to change position.
4. This moves a point; it does not stop that point from falling through floors.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

Semi-implicit Euler updates velocity before position. This is an educational point mass under constant acceleration; it has no contacts, constraints, angular inertia, or continuous collision detection.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
