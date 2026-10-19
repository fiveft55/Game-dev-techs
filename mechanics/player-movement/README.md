# Free movement (continuous)

This independent mechanic is stored in `mechanics/player-movement/`. It moves by continuous distances, supports analog input and normalized diagonal movement, and leaves collision handling to your game.

For one-tile steps with walls, buffered turns and key repeat, use the separate [grid-movement mechanic](../grid-movement/README.md). Each folder has its own code, input contract and tests.

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Move a player in the direction they press, without making diagonal movement faster.

1. Read where the player is and which direction they want to go.
2. If the direction arrow is too long, shrink it to length one.
3. Multiply that direction by speed and the time that passed.
4. Add the result to the old position.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

Status: implemented educational reference; Python 3 standard library.

Normalize diagonal input so diagonal travel is no faster than straight travel. Integrate velocity in units per second. Collision response and acceleration are separate mechanics.

## Read and run

Read [`python/example.py`](python/example.py). Inline comments explain consequential choices. Run all examples' behavioral checks from the repository root with `python3 tools/validate.py`. Import this module into a game loop or editor; it has no automatic runtime side effects.

## Adaptation checklist

Choose units and coordinate conventions. Validate external inputs at the application boundary. Add tests for your game's scale, determinism, error handling, and performance before shipping. This module is independent of other mechanics.

## Provenance

Original educational implementation for this repository, distributed under the root MIT license. General algorithms are explained in the [source registry](../../docs/sources.md); no third-party source code or assets are bundled.

## Additional language ports

These ports implement the same normalized movement equation for finite inputs and nonnegative speed/dt. The Python version rejects negative speed/dt; the small additional ports assume the caller validates those preconditions. They are not engine controllers.

From the repository root:

```sh
mkdir -p .build
cc -std=c11 -Wall -Wextra -Werror mechanics/player-movement/c/example.c -lm -o .build/move-c
.build/move-c
c++ -std=c++17 -Wall -Wextra -Werror mechanics/player-movement/cpp/example.cpp -o .build/move-cpp
.build/move-cpp
node mechanics/player-movement/javascript/example.js
lua mechanics/player-movement/lua/example.lua
php mechanics/player-movement/php/example.php
rustc mechanics/player-movement/rust/example.rs -o .build/move-rust
.build/move-rust
dotnet run --project mechanics/player-movement/csharp/Movement.csproj
```

See [validation evidence](../../docs/validation.md) for which toolchains actually ran.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.

## Run this mechanic independently

```sh
python3 tools/test_ports.py --mechanic player-movement --languages all
```

## Optimization reading

See [the relevant optimization chapter](../../docs/optimization/05-movement-ai.md) and [the current-code cost audit](../../docs/optimization/mechanics-audit.md). Suggested improvements are not automatically implemented or benchmarked here.
