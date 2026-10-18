# grid-movement: portable language versions

## Plain-English explanation

Move a character one square at a time, stopping at walls and waiting until each step is finished.

1. Read one direction: up, right, down, left, or no button.
2. Check the next square. Stay put if it is outside the map or contains a wall.
3. Either jump straight to that square or slide to it over the chosen step time.
4. Remember the newest direction briefly if it is pressed during a step. Try it after landing.
5. Holding a direction waits for a short delay, then requests more steps at regular times. Releasing stops those repeats.

[New to code? Start with the beginner guide.](../../docs/beginner-guide.md)

These are independent native educational kernels, not wrappers that call Python. They share one explicit numeric-array contract across eight languages. The existing Python module retains its original API; the portable API is a separate interface and may expose a smaller core operation as explained below.

## Contract

- Input: `[width,height,step_seconds,repeat_delay,repeat_interval,buffer_seconds,dt,direction,...9_state_values,...row_major_grid]`
- Output: `[...9_next_state_values,visual_x,visual_y,steps_started,tiles_arrived,blocked_flag]`

Persistent one-update controller. Directions 0=release,1=up,2=right,3=down,4=left (Y down). State: tile_x,tile_y,target_x,target_y,progress,buffered_direction,held_direction,repeat_remaining,buffer_remaining. Keep the first nine outputs for the next call. Zero tiles are walkable. dt is 0..1 seconds; repeat delay/interval >=0.01 seconds. See README for event ordering and static-map assumptions; [-1] means invalid configuration/state.

Supply finite, correctly shaped numeric data. Integer indices/counts/IDs must be exact and within the safe binary64 range. Do not pass raw network or unvalidated save data directly. Bounds checks are present, but these kernels do not implement a comprehensive schema validator. C vectors have a default capacity of 4096 values; exceeding it triggers an assertion rather than truncation. An entire C program must use the same `PORT_CAPACITY`. See [language conventions](../../docs/language-ports.md) for numeric, state, performance and API differences.

## Native source

| Language | File | Entry point |
|---|---|---|
| c | [mechanic.c](c/mechanic.c) | `game_grid_movement_compute(input)` |
| csharp | [Mechanic.cs](csharp/Mechanic.cs) | `MechanicGridMovement.Compute(data)` |
| lua | [mechanic.lua](lua/mechanic.lua) | `compute(data)` |
| gdscript | [mechanic.gd](gdscript/mechanic.gd) | `compute(data)` |
| typescript | [mechanic.ts](typescript/mechanic.ts) | `compute(data)` |
| javascript | [mechanic.js](javascript/mechanic.js) | `compute(data)` |
| rust | [mechanic.rs](rust/mechanic.rs) | `compute(data)` |
| go | [mechanic.go](go/mechanic.go) | `Compute(data)` |

C users include [mechanic.h](c/mechanic.h) and compile the matching `.c` as a separate translation unit. Namespaced entry points allow multiple mechanics to link together. Other languages isolate mechanics with modules/classes/packages.

## Working fixture

Input:

```json
[3, 1, 0, 0.3, 0.1, 0.15, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

Expected output:

```json
[1, 0, 1, 0, 0, 0, 2, 0.3, 0, 1, 0, 1, 1, 0]
```

All 15 hand-authored cases are in [the shared fixture data](../../tests/port-fixtures.json), keyed by `grid-movement`. Each case is run against every native language by the test runner.

From the repository root:

```sh
python3 tools/test_ports.py --mechanic grid-movement --languages all
python3 tools/test_ports.py --mechanic grid-movement --languages javascript,c
```

The runner fails on a missing toolchain by default. `--allow-missing` explicitly records missing tools; it does not mark them passed. Generated build artifacts stay under `.build/`. See [toolchain setup](../../docs/toolchains.md).

## Editing and reuse

For your own project, copy the native source (and the C header) with the MIT license, adapt the input decoding into named engine types, then extend the behavioral tests for your rules. Batched event ports start a fresh session per call; they are not automatically persistent service objects. To update this repository consistently, edit [the specification](../../tools/ports/specs.py), run `python3 tools/ports/generate.py` and `python3 tools/ports/document.py`, then run the native checks. Generation is a maintenance aid; the generated files have no Python runtime dependency.

All algorithms and adapters are original code under the root [MIT license](../../LICENSE). No third-party game source or assets are bundled.
