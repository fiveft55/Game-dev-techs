# Kinematic vehicle steering

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Move a simple car forward and bend its direction when the wheels steer.

1. Move the car along its current facing direction.
2. Use steering angle, speed, and axle spacing to decide how much it turns.
3. Update the facing direction for the next step.
4. This is a simple no-skidding model, not a realistic tire or suspension simulation.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

The bicycle model approximates front/rear axle geometry at low speeds with no tire slip. It is useful for prototypes, not a realistic tire, suspension, or crash simulator. Coordinates use radians and consistent world units.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
