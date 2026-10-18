# deck-draw: portable language versions

## Plain-English explanation

Shuffle a card pile, draw cards, and reuse discarded cards when the pile runs out.

1. Shuffle by swapping cards using a repeatable number generator.
2. Drawing removes the last card from the pile.
3. If the pile is empty, shuffle the discard pile into a new draw pile.
4. If both piles are empty, return the no-card marker. This predictable shuffle is not secure against cheaters.

[New to code? Start with the beginner guide.](../../docs/beginner-guide.md)

These are independent native educational kernels, not wrappers that call Python. They share one explicit numeric-array contract across eight languages. The existing Python module retains its original API; the portable API is a separate interface and may expose a smaller core operation as explained below.

## Contract

- Input: `[uint32_seed,card_count,...card_ids,...operations]`
- Output: `[...drawn_card_ids_or_minus_one]`

Operation -1 draws; nonnegative operation discards that card. Portable LCG Fisher-Yates; only server-owned decks can protect hidden cards. Not cryptographic or gambling-ready.

Supply finite, correctly shaped numeric data. Integer indices/counts/IDs must be exact and within the safe binary64 range. Do not pass raw network or unvalidated save data directly. Bounds checks are present, but these kernels do not implement a comprehensive schema validator. C vectors have a default capacity of 4096 values; exceeding it triggers an assertion rather than truncation. An entire C program must use the same `PORT_CAPACITY`. See [language conventions](../../docs/language-ports.md) for numeric, state, performance and API differences.

## Native source

| Language | File | Entry point |
|---|---|---|
| c | [mechanic.c](c/mechanic.c) | `game_deck_draw_compute(input)` |
| csharp | [Mechanic.cs](csharp/Mechanic.cs) | `MechanicDeckDraw.Compute(data)` |
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
[0, 1, 7, -1, -1, 7, -1]
```

Expected output:

```json
[7, -1, 7]
```

All 5 hand-authored cases are in [the shared fixture data](../../tests/port-fixtures.json), keyed by `deck-draw`. Each case is run against every native language by the test runner.

From the repository root:

```sh
python3 tools/test_ports.py --mechanic deck-draw --languages all
python3 tools/test_ports.py --mechanic deck-draw --languages javascript,c
```

The runner fails on a missing toolchain by default. `--allow-missing` explicitly records missing tools; it does not mark them passed. Generated build artifacts stay under `.build/`. See [toolchain setup](../../docs/toolchains.md).

## Editing and reuse

For your own project, copy the native source (and the C header) with the MIT license, adapt the input decoding into named engine types, then extend the behavioral tests for your rules. Batched event ports start a fresh session per call; they are not automatically persistent service objects. To update this repository consistently, edit [the specification](../../tools/ports/specs.py), run `python3 tools/ports/generate.py` and `python3 tools/ports/document.py`, then run the native checks. Generation is a maintenance aid; the generated files have no Python runtime dependency.

All algorithms and adapters are original code under the root [MIT license](../../LICENSE). No third-party game source or assets are bundled.
