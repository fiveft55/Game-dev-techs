# Grid movement (tile-based)

This independent mechanic is stored in `mechanics/grid-movement/`. Its tile destinations, wall checks, buffered turns and repeat timers belong to this folder.

For continuous distances and analog or diagonal input, use the separate [free-movement mechanic](../player-movement/README.md). Each folder has its own code, input contract and tests.

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Move a character one square at a time, stopping at walls and waiting until each step is finished.

1. Read one direction: up, right, down, left, or no button.
2. Check the next square. Stay put if it is outside the map or contains a wall.
3. Either jump straight to that square or slide to it over the chosen step time.
4. Remember the newest direction briefly if it is pressed during a step. Try it after landing.
5. Holding a direction waits for a short delay, then requests more steps at regular times. Releasing stops those repeats.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

A persistent four-direction tile controller for RPG exploration, roguelikes, mazes and tactical prototypes. Python plus native Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are included.

## What you get

- Exactly one adjacent tile per movement request, with wall and boundary checks.
- Instant steps (`step_seconds=0`) or a smooth slide with an exact tile landing.
- One-slot, latest-direction input buffering while a step is in progress.
- An initial hold delay and timed key repeat, independent of update frequency.
- Persistent state between calls, plus named position/event results in Python.

## Python: small example

From the repository root:

```python
import importlib.util
spec = importlib.util.spec_from_file_location('grid_movement', 'mechanics/grid-movement/python/example.py')
grid_movement = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grid_movement)

world = [[0, 0, 1], [0, 0, 0]]  # 0 is floor; 1 is wall.
player = grid_movement.GridMover(world, start=(0, 0), step_seconds=0.2)
player.update(0.1, 'right')
print(player.position)  # (0.5, 0.0): halfway to the next tile.
player.update(0.1, None)
print(player.tile)      # (1, 0): landed exactly, not between tiles.
result = player.update(0, 'right')
print(result['blocked'])  # True: the next tile is a wall.
```

If a tile is 32 pixels wide, multiply drawing coordinates by 32; keep movement/collision coordinates in tiles.

Use `player.position` for drawing, `player.tile` for the last completed tile and `player.target` for the destination reserved by the current step. `player.moving` tells whether that step is unfinished. These are read-only properties; the controller owns movement state. The map is copied into an immutable layout at construction.

## Direction and timing rules

Coordinates count rightward for X and downward for Y. Only one direction is accepted per update. Your input adapter must choose a direction when multiple keys are held; diagonal movement is not performed.

The direction passed to `update(dt, direction)` applies at the **start** of that interval. A changed direction counts as a fresh press; the first step can start immediately, even with `dt=0`. Repeating starts after `repeat_delay`, then every `repeat_interval`. Release stops future repeats. A valid pending turn can still survive release until its buffer expires.

A turn never changes an in-flight destination. New presses/repeats replace the one pending direction, which is consumed once when the character is idle. Blocked requests are consumed too; a held key can retry later. With `buffer_seconds=0`, requests made during travel do not survive any positive travel time.

Arrival is processed before a simultaneous repeat; the newest repeat may replace a pending turn. A buffer is valid at its exact expiry deadline. Events at the end of an update are processed, so a step may start with zero progress at that boundary. The next update advances it. A tolerance of 1e-9 is used for timing/progress comparisons.

`dt` must be finite and between zero and one second per call. Split longer elapsed intervals explicitly; the controller does not silently drop elapsed time. Repeat delay and interval must each be at least 0.01 seconds. Smooth step duration is a positive finite number; zero selects instant movement.

## Native state: use it in a real loop

The [portable contract](PORTS.md) gives the full input layout. Start with state `[x,y,x,y,0,0,0,0,0]`. Each call returns nine new state values followed by visual coordinates and three event counts/flags. **Keep those first nine values and pass them into the next call.** This controller is an exception to the older batch-only examples: it persists via explicit caller-owned state.

State fields, in order:

| Field | Plain meaning |
|---|---|
| tile_x, tile_y | Last square fully reached |
| target_x, target_y | Square being walked toward, or the current square if idle |
| progress | Fraction of the current step completed, from zero to one |
| buffered_direction | Newest waiting request; zero means none |
| held_direction | Button currently held; zero means release |
| repeat_remaining | Seconds until the next held-key request |
| buffer_remaining | Seconds left before the waiting request expires |

The final outputs are `visual_x`, `visual_y`, `steps_started`, `tiles_arrived` and `blocked_flag`. A call may start/finish multiple steps when hold-repeat times fall within its interval. `blocked_flag` means at least one attempted step hit a wall or map edge during this call.

## JavaScript: keeping state between updates

```js
const movement = require('./mechanics/grid-movement/javascript/mechanic.js');
const tiles = [0, 0, 1, 0, 0, 0]; // A map three tiles wide and two high.
const config = [3, 2, 0.2, 0.3, 0.1, 0.15];
let state = [0, 0, 0, 0, 0, 0, 0, 0, 0];
function update(dt, direction) {
  const next = movement.compute([...config, dt, direction, ...state, ...tiles]);
  if (next.length !== 14) throw new Error('Invalid movement update');
  state = next.slice(0, 9); // Keep the memory for the next frame.
  return {x: next[9], y: next[10], blocked: next[13] === 1};
}
console.log(update(0.1, 2)); // right: {x: 0.5, y: 0, blocked: false}
console.log(update(0.1, 0)); // release: {x: 1, y: 0, blocked: false}
console.log(update(0, 2));   // right into wall: {x: 1, y: 0, blocked: true}
```

The path above assumes a caller at the repository root. The other native languages use the same numbers and state layout, with the calling conventions listed in [PORTS.md](PORTS.md).

## Tests

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -p test_grid_movement.py -v
python3 tools/test_ports.py --mechanic grid-movement --languages all
```

Tests cover all four directions, walls, boundaries, partial and exact landings, buffered turns/expiry/replacement, release, hold timing, long-vs-split updates, invalid input, and passing explicit state between native-compatible calls.

## Limits and provenance

This is a single-actor controller on a static rectangular map. No jumping, diagonal stepping, pushing boxes, slopes, path selection, dynamic obstacles, multi-actor reservations or network authority is included. Keep configuration/map stable during a step; resolve shared occupancy outside this module. The destination becomes logically occupied only according to the policy you choose in your game; this example exposes both source and target so you can implement reservations.

Original code under the root [MIT license](../../LICENSE); no third-party code or assets were copied. See [language conventions](../../docs/language-ports.md) and [source policy](../../docs/sources.md).

## Optimization reading

See [the relevant optimization chapter](../../docs/optimization/05-movement-ai.md) and [the current-code cost audit](../../docs/optimization/mechanics-audit.md). Suggested improvements are not automatically implemented or benchmarked here.
