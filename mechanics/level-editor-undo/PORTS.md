# level-editor-undo: portable language versions

## Plain-English explanation

Let a map editor undo and redo painting a tile.

1. Before painting, remember the old tile and the new tile.
2. Undo restores the old tile and moves backward in the edit history.
3. Redo puts the new tile back and moves forward.
4. Painting after undo throws away the abandoned future edits.

[New to code? Start with the beginner guide.](../../docs/beginner-guide.md)

These are independent native educational kernels, not wrappers that call Python. They share one explicit numeric-array contract across eight languages. The existing Python module retains its original API; the portable API is a separate interface and may expose a smaller core operation as explained below.

## Contract

- Input: `[width,height,...[operation,cell,value]]`
- Output: `[...final_grid]`

Operations: 0 paint, 1 undo, 2 redo. Cell ID is y*width+x. New paint discards the redo branch. Ignored unused cell/value fields must still be supplied.

Supply finite, correctly shaped numeric data. Integer indices/counts/IDs must be exact and within the safe binary64 range. Do not pass raw network or unvalidated save data directly. Bounds checks are present, but these kernels do not implement a comprehensive schema validator. C vectors have a default capacity of 4096 values; exceeding it triggers an assertion rather than truncation. An entire C program must use the same `PORT_CAPACITY`. See [language conventions](../../docs/language-ports.md) for numeric, state, performance and API differences.

## Native source

| Language | File | Entry point |
|---|---|---|
| c | [mechanic.c](c/mechanic.c) | `game_level_editor_undo_compute(input)` |
| csharp | [Mechanic.cs](csharp/Mechanic.cs) | `MechanicLevelEditorUndo.Compute(data)` |
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
[2, 1, 0, 0, 5, 1, 0, 0, 2, 0, 0]
```

Expected output:

```json
[5, 0]
```

All 3 hand-authored cases are in [the shared fixture data](../../tests/port-fixtures.json), keyed by `level-editor-undo`. Each case is run against every native language by the test runner.

From the repository root:

```sh
python3 tools/test_ports.py --mechanic level-editor-undo --languages all
python3 tools/test_ports.py --mechanic level-editor-undo --languages javascript,c
```

The runner fails on a missing toolchain by default. `--allow-missing` explicitly records missing tools; it does not mark them passed. Generated build artifacts stay under `.build/`. See [toolchain setup](../../docs/toolchains.md).

## Editing and reuse

For your own project, copy the native source (and the C header) with the MIT license, adapt the input decoding into named engine types, then extend the behavioral tests for your rules. Batched event ports start a fresh session per call; they are not automatically persistent service objects. To update this repository consistently, edit [the specification](../../tools/ports/specs.py), run `python3 tools/ports/generate.py` and `python3 tools/ports/document.py`, then run the native checks. Generation is a maintenance aid; the generated files have no Python runtime dependency.

All algorithms and adapters are original code under the root [MIT license](../../LICENSE). No third-party game source or assets are bundled.
