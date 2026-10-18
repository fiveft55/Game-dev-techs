# Buffered jump and coyote time

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Make jumping feel forgiving when the button press is slightly early or slightly late.

1. Remember the last time the character touched the ground.
2. Remember the last time the jump button was pressed.
3. Allow a jump if those memories are still recent enough.
4. Use up that jump so one press cannot keep creating jumps in mid-air. A new landing restores it.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

## Mechanic and algorithm

Use a monotonic simulation clock in seconds. A recent jump press can be consumed upon landing; a jump can also be triggered shortly after leaving an edge. Return a jump decision for a separate movement/physics controller.

## Read the implementation

[`python/example.py`](python/example.py) is an independent, standard-library-only Python 3.10+ module. Comments highlight decisions worth changing for your own game. There are no engine dependencies or runtime side effects on import.

## Working example and behavioral check

From the repository root:

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -p test_genre_mechanics.py -k jump_controller -v
```

The corresponding `test_jump_controller` in [the test suite](../../tests/test_genre_mechanics.py) demonstrates real calls, expected outputs, and boundary or rejection cases. For interactive use:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("mechanic", "mechanics/jump-controller/python/example.py")
mechanic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mechanic)
# Use the public functions/classes shown in the behavioral test.
```

## Assumptions and limits

No collision or vertical integration. The caller must report actual grounded state before a jump and make the character airborne after a successful jump. One jump per grounded episode.

Tune the rules for your game and extend the tests before integrating. Educational coverage is not a full genre implementation or a production-readiness guarantee. The original Python API is preserved. Eight additional native kernels are available; see the portable contract for their API and scope differences.

## Provenance

Original code written for this repository under the root [MIT license](../../LICENSE). No third-party source or assets were scraped or bundled. See [genre coverage](../../docs/genre-coverage.md) for reuse across genres and the [source policy](../../docs/sources.md) before importing additional code.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
