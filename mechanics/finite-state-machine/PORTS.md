# finite-state-machine: portable language versions

## Plain-English explanation

Let a character switch between named situations, such as idle and jumping, using clear rules.

1. Keep one current state, represented here by a number.
2. Read the next event, such as a jump button press.
3. Find a rule matching the current state and that event.
4. Switch to the rule destination. If no rule matches, keep the old state.

[New to code? Start with the beginner guide.](../../docs/beginner-guide.md)

These are independent native educational kernels, not wrappers that call Python. They share one explicit numeric-array contract across eight languages. The existing Python module retains its original API; the portable API is a separate interface and may expose a smaller core operation as explained below.

## Contract

- Input: `[initial_state, transition_count, ...[from,event,to], ...events]`
- Output: `[final_state, accepted_count]`

Integer state/event IDs. First matching transition wins. Unknown events are ignored.

Supply finite, correctly shaped numeric data. Integer indices/counts/IDs must be exact and within the safe binary64 range. Do not pass raw network or unvalidated save data directly. Bounds checks are present, but these kernels do not implement a comprehensive schema validator. C vectors have a default capacity of 4096 values; exceeding it triggers an assertion rather than truncation. An entire C program must use the same `PORT_CAPACITY`. See [language conventions](../../docs/language-ports.md) for numeric, state, performance and API differences.

## Native source

| Language | File | Entry point |
|---|---|---|
| c | [mechanic.c](c/mechanic.c) | `game_finite_state_machine_compute(input)` |
| csharp | [Mechanic.cs](csharp/Mechanic.cs) | `MechanicFiniteStateMachine.Compute(data)` |
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
[0, 2, 0, 7, 1, 1, 8, 0, 99, 7, 8]
```

Expected output:

```json
[0, 2]
```

All 2 hand-authored cases are in [the shared fixture data](../../tests/port-fixtures.json), keyed by `finite-state-machine`. Each case is run against every native language by the test runner.

From the repository root:

```sh
python3 tools/test_ports.py --mechanic finite-state-machine --languages all
python3 tools/test_ports.py --mechanic finite-state-machine --languages javascript,c
```

The runner fails on a missing toolchain by default. `--allow-missing` explicitly records missing tools; it does not mark them passed. Generated build artifacts stay under `.build/`. See [toolchain setup](../../docs/toolchains.md).

## Editing and reuse

For your own project, copy the native source (and the C header) with the MIT license, adapt the input decoding into named engine types, then extend the behavioral tests for your rules. Batched event ports start a fresh session per call; they are not automatically persistent service objects. To update this repository consistently, edit [the specification](../../tools/ports/specs.py), run `python3 tools/ports/generate.py` and `python3 tools/ports/document.py`, then run the native checks. Generation is a maintenance aid; the generated files have no Python runtime dependency.

All algorithms and adapters are original code under the root [MIT license](../../LICENSE). No third-party game source or assets are bundled.
