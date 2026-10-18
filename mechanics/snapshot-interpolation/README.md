# Multiplayer snapshot interpolation

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Draw another player between two known positions so their movement looks less jumpy.

1. Read an older position and a newer position, each with a time.
2. Find where the drawing time sits between those times.
3. Move the same fraction of the way between the two positions.
4. If drawing time is outside the pair, use the nearest endpoint rather than guessing ahead.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

Render remote entities between two server snapshots with an intentional delay. This reduces jitter but adds latency. Clamp outside the interval; extrapolation is a separate policy. Authenticate and validate network messages before interpolation.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
