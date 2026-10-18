# Native language ports

All 51 mechanics now have original Python implementations plus eight independent native kernels: **Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go**. That is 408 native implementation files, with C headers alongside them. The earlier movement-only C++, PHP and standalone examples are retained.

Start at the [mechanics index](mechanics-index.md), choose a mechanic, and open its `PORTS.md`. That file lists the exact input/output layout and a worked fixture. The original Python API has not changed.

## What “port” means here

The eight new languages share a small explicit numeric-array API. Algorithms run natively; they do not spawn Python, call a remote service, or load a generic Python interpreter. Descriptive local variables decode the inputs before computing results. Numeric IDs replace string item/actor/node identifiers. Array-based inputs make identical fixtures and engine-independent examples possible; your application can wrap these in named structs, classes, or engine types.

These are **portable core kernels, not full API replicas of the Python modules**. Important differences are explicit:

- The grid-movement controller is persistent through explicit state: carry its first nine output values into the next call. It includes key-repeat and buffer timers. Python also provides a named `GridMover` object.
- Some Python classes are represented by batched events starting a fresh session per call. Do not assume history persists between calls; keep events/state in a wrapper or adapt the kernel into an engine object.
- The save kernel migrates a decoded minimal `(version, gold)` record. It does not implement the Python JSON parser or arbitrary inventory schema.
- Quest ports accumulate objectives and expose a final claim decision, not a persistent atomic reward service. Rhythm ports judge presses; the caller performs audio-clock expiry/miss handling.
- Fog ports compute radius visibility and explored masks; compose an occlusion mask separately instead of passing a Python callback.
- Scheduler ports order a batch, not an incremental heap service. Spatial-hash ports scan flat cell records for clarity rather than retaining a dictionary of buckets.
- Rollback ports demonstrate deterministic scalar movement, not arbitrary callback-based simulation or network rollback.
- Maze/deck ports use a reproducible integer LCG, so their seeded outputs match each other but not Python's `random.Random`. This PRNG is not cryptographically secure. Loot selection takes a caller-generated uniform ticket.
- Numeric values use binary64 across ports. Offline production therefore lacks Python Decimal's decimal arithmetic. Use a suitable fixed-point or server-ledger design when exact economy accounting matters.

All inputs must follow their contract: finite numbers, exact integer counts/indices/IDs, correctly shaped records, and bounded sizes. Validate external JSON/network input before calling these algorithms. Some semantic errors return `[-1]` or another documented sentinel; malformed record shapes can assert or throw. These are educational modules, not hostile-input parsers.

## Calling conventions

Use [free movement](../mechanics/player-movement/README.md), stored in `player-movement`, as a first example. The separate [grid controller](../mechanics/grid-movement/README.md) has its own tile-based input/state contract. Input `[0, 0, 1, 0, 4, 0.5]` means position `(0,0)`, input `(1,0)`, speed `4`, and timestep `0.5` seconds. Every new port returns `[2,0]`.

### JavaScript

```js
const movement = require('../mechanics/player-movement/javascript/mechanic.js');
console.log(movement.compute([0, 0, 1, 0, 4, 0.5]));
```

The relative path above assumes a caller file under `tools/`. `compute` can also be used in a browser script; CommonJS export is guarded.

### TypeScript

```ts
import {compute} from '../mechanics/player-movement/typescript/mechanic';
const position: number[] = compute([0, 0, 1, 0, 4, 0.5]);
```

Compile with TypeScript strict mode. The port has no Node-specific type dependencies.

### Lua

```lua
-- From the repository root:
local movement = dofile('mechanics/player-movement/lua/mechanic.lua')
local position = movement.compute({0, 0, 1, 0, 4, 0.5})
print(position[1], position[2]) -- Lua arrays are one-based at the public boundary.
```

The `port_get` helper adapts documented zero-based logical offsets to Lua tables.

### C#

```csharp
using System.Collections.Generic;
// Compile this together with player-movement/csharp/Mechanic.cs.
List<double> position = MechanicPlayerMovement.Compute(
    new List<double> {0, 0, 1, 0, 4, 0.5});
```

Each mechanic has a distinct public class, so multiple modules can be compiled together. These pure classes do not depend on Unity.

### GDScript (Godot 4)

```gdscript
const Movement = preload("res://mechanics/player-movement/gdscript/mechanic.gd")
# Inside a method:
# var position: Array = Movement.compute([0, 0, 1, 0, 4, 0.5])
```

Files extend `RefCounted` and expose a static method. They do not create nodes, scenes, rendering loops, or input actions.

### C (C11)

```c
#include "mechanics/player-movement/c/mechanic.h"
int main(void) {
    PortVector input = {.values={0,0,1,0,4,0.5}, .count=6};
    PortVector position = game_player_movement_compute(input);
    return position.count == 2 && position.values[0] == 2 ? 0 : 1;
}
```

From the repository root, compile your caller together with `mechanics/player-movement/c/mechanic.c`, add `-I.` and link `-lm`. Use each module's header and a separate translation unit; do not paste multiple `.c` files into one translation unit. Every exported algorithm name is unique, and the validation runner links all 51 together.

`PortVector` owns a fixed buffer, default 4096 doubles. Overflow or invalid indexing asserts. Do not disable assertions while relying on those checks. The same `PORT_CAPACITY` must be defined for every linked source and caller to preserve ABI compatibility. By-value buffers and linear scans prioritize transparent ownership over production performance.

### Rust (edition 2021)

```rust
#[path = "../mechanics/player-movement/rust/mechanic.rs"]
mod movement;
fn main() {
    let position = movement::compute(&[0.0,0.0,1.0,0.0,4.0,0.5]);
    assert_eq!(position, vec![2.0,0.0]);
}
```

The path above assumes a caller file under `tools/`. Input is borrowed; output is an owned `Vec<f64>`. Helpers stay inside the module. There are no external crates or unsafe blocks.

### Go (1.20+)

```go
package main
import movement "github.com/fiveft55/Game-dev-techs/mechanics/player-movement/go"
func main() {
    position := movement.Compute([]float64{0,0,1,0,4,0.5})
    if len(position) != 2 || position[0] != 2 { panic("movement failed") }
}
```

Each mechanic lives in a separate importable package. Run from this Go module or depend on the repository module in your own project. The ports use only the standard library.

## Validation and maintenance

```sh
python3 tools/test_ports.py --languages all
python3 tools/test_ports.py --mechanic grid-pathfinding --languages c,rust,go
python3 tools/ports/generate.py --check
python3 tools/ports/document.py --check
python3 tools/validate.py
python3 tools/build_indexes.py --check
```

Shared hand-authored fixtures are stored in [tests/port-fixtures.json](../tests/port-fixtures.json). Missing toolchains fail the native test command by default; optional `--allow-missing` records them as missing rather than passed. Python's suite checks the generator, fixtures and representative behavior against existing Python modules, but that does not replace compiling/running the native languages.

Edit [specs.py](../tools/ports/specs.py) to change shared behavior, then regenerate native source, contracts and indexes. Native files remain editable for use outside this repository. Avoid hand-editing one generated port here without updating the generator/specification, or regeneration will overwrite it.

See [validation evidence](validation.md) for actual executions and [toolchains](toolchains.md) for setup. These tests cover representative behavior, not every input, compiler/platform combination, concurrency scenario or engine integration.
