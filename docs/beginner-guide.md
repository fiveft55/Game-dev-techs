# Start here: game code in plain English

A game is a pile of small rules repeated very quickly. You do not need to understand a whole engine to learn one rule. Each mechanic folder now starts with a plain-English explanation, and `PORTS.md` shows a real input and its expected answer.

## Read one small example

Imagine a person standing at position zero. They walk right at four steps per second. Half a second passes. They should move two steps right.

The movement kernel takes:

```text
[0, 0, 1, 0, 4, 0.5]
 |  |  |  |  |    |
 x  y  right up speed seconds
```

It returns `[2, 0]`: two steps to the right, no steps up. The numbers are in a fixed order, like labeled boxes on a form. `PORTS.md` is the label sheet for each mechanic. Do not guess the meaning of a number from its position in a different mechanic.

Try it from the repository root with Node.js:

```sh
node -e "const m=require('./mechanics/player-movement/javascript/mechanic.js'); console.log(m.compute([0,0,1,0,4,0.5]));"
```

Or run its existing checks in every installed language:

```sh
python3 tools/test_ports.py --mechanic player-movement --languages all
```

## Common words

| Word | Everyday meaning |
|---|---|
| Function | A little machine: give it inputs, let it do a job, collect its answer. |
| Input / argument | Information you give that machine. |
| Return / output | The answer the machine hands back. |
| Variable | A named box that stores one value. `speed` is a box holding how fast something moves. |
| Array / list / vector | Several values kept in order, like numbered boxes on a shelf. |
| Index | The position of a box on that shelf. Most examples count from zero; Lua tables count from one outside the helper adapter. |
| ID | A label, not an amount. Item 7 is not necessarily seven items. |
| State | What the game remembers right now: position, health, current turn, or open doors. |
| Event | Something happened: a button press, a hit, a collected item, or a vote. |
| Flag | A yes/no switch, usually zero or one. |
| Condition / `if` | Ask a question and do something only when the answer is yes. |
| Loop | Do a job repeatedly. A `while` loop keeps going while its condition is true. |
| Timestep / `dt` | How many seconds one update represents. |
| Coordinate | A position number. Two numbers describe left/right and up/down. |
| Velocity | Speed with a direction. |
| Acceleration | How quickly velocity changes. Gravity is one example. |
| Normalize | Shrink or stretch a direction arrow to length one without turning it. |
| Collision | Two things touch, or a moving thing hits something. |
| Interpolate | Pick a point partway between two known values. Halfway between 0 and 10 is 5. |
| Snapshot | A saved picture of game data at one moment, not necessarily an image. |
| Deterministic | The same starting information and same inputs give the same result. |
| Seed | The starting number for a repeatable pretend-random sequence. It is not a secret key. |
| Schema / contract | The rule sheet saying what information is allowed and what each piece means. |
| Assertion / test | A check that shouts or fails when reality does not match the expected rule. |
| Compile | Turn source text into a program a runtime or computer can execute. |
| Kernel (here) | The small central calculation, without a screen, sound, networking, or engine around it. |

## What the small helper functions do

Every native file explains its helpers above their definitions. `port_get` reads a box; `port_put` changes a box; `port_push` adds a box at the end; `port_length` counts boxes. These helpers are not hidden game engines. They mostly adapt small differences between languages and check list positions.

`minimum` picks the smaller number and `maximum` picks the larger one. `floor` rounds downward. `sqrt` helps find distance. `sin`, `cos` and `tan` help work with angles. An angle in radians is another way to measure a turn: a full turn is about 6.28318 radians.

Computer numbers can round decimal values slightly. That is why many tests compare with a tiny allowed difference instead of demanding exact decimal equality. Whole-number item IDs must stay within the documented range.

## A safe learning order

1. Read the mechanic's plain-English section before reading code.
2. Find its first input and expected answer in `PORTS.md`.
3. Read the named variables inside `compute` or `Compute` to see how the input is unpacked.
4. Follow one small example by hand, writing down changed values.
5. Run the check, change one rule in your own copy, and predict the new answer before running again.

Begin with movement, collision, score/lives, inventory and cooldowns. Then try pathfinding, procedural maps, editors and multiplayer data rules. The test runner compiles/runs examples; it does not draw a playable game. Putting several mechanics together with graphics, input and sound is a separate step.

A negative marker such as `[-1]` may mean an invalid request or a particular no-result case. Read that mechanic's contract: not every negative number is an error. The library does not silently keep game sessions alive between calls to its batched kernels.
