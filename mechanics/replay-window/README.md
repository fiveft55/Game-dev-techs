# Multiplayer replay protection

Status: implemented educational reference; Python 3 standard library.

Track a bounded window of authenticated sequence numbers to reject duplicates and stale packets while tolerating reordering. Sequence numbers must be nonnegative integers and must not wrap within a session. This is NOT encryption or authentication; update only after authenticating the packet.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.
