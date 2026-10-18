# match-grid: portable language versions

## Plain-English explanation

Remove matching rows or columns of tiles, then let the remaining tiles fall down.

1. Find long enough runs of identical nonempty tiles.
2. Mark each matching tile once, even where a row and column cross.
3. Remove all marked tiles together.
4. Slide surviving tiles to the bottom of each column without changing their order.

[New to code? Start with the beginner guide.](../../docs/beginner-guide.md)

These are independent native educational kernels, not wrappers that call Python. They share one explicit numeric-array contract across eight languages. The existing Python module retains its original API; the portable API is a separate interface and may expose a smaller core operation as explained below.

## Contract

- Input: `[width,height,minimum_run,...tiles]`
- Output: `[matched_count,...collapsed_tiles]`

Tile -1 is empty. Detect horizontal/vertical matches, merge intersections, then apply column gravity. No random refill or cascade.

Supply finite, correctly shaped numeric data. Integer indices/counts/IDs must be exact and within the safe binary64 range. Do not pass raw network or unvalidated save data directly. Bounds checks are present, but these kernels do not implement a comprehensive schema validator. C vectors have a default capacity of 4096 values; exceeding it triggers an assertion rather than truncation. An entire C program must use the same `PORT_CAPACITY`. See [language conventions](../../docs/language-ports.md) for numeric, state, performance and API differences.

## Native source

| Language | File | Entry point |
|---|---|---|
| c | [mechanic.c](c/mechanic.c) | `game_match_grid_compute(input)` |
| csharp | [Mechanic.cs](csharp/Mechanic.cs) | `MechanicMatchGrid.Compute(data)` |
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
[3, 3, 3, 1, 2, 3, 1, 1, 1, 1, 2, 3]
```

Expected output:

```json
[5, -1, -1, -1, -1, 2, 3, -1, 2, 3]
```

All 2 hand-authored cases are in [the shared fixture data](../../tests/port-fixtures.json), keyed by `match-grid`. Each case is run against every native language by the test runner.

From the repository root:

```sh
python3 tools/test_ports.py --mechanic match-grid --languages all
python3 tools/test_ports.py --mechanic match-grid --languages javascript,c
```

The runner fails on a missing toolchain by default. `--allow-missing` explicitly records missing tools; it does not mark them passed. Generated build artifacts stay under `.build/`. See [toolchain setup](../../docs/toolchains.md).

## Editing and reuse

For your own project, copy the native source (and the C header) with the MIT license, adapt the input decoding into named engine types, then extend the behavioral tests for your rules. Batched event ports start a fresh session per call; they are not automatically persistent service objects. To update this repository consistently, edit [the specification](../../tools/ports/specs.py), run `python3 tools/ports/generate.py` and `python3 tools/ports/document.py`, then run the native checks. Generation is a maintenance aid; the generated files have no Python runtime dependency.

All algorithms and adapters are original code under the root [MIT license](../../LICENSE). No third-party game source or assets are bundled.
