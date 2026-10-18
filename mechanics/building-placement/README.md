# Rotated grid footprint placement

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Place a building footprint on a tile map only if every required square is free.

1. Rotate the footprint by the requested number of quarter turns.
2. Move it to the chosen anchor tile.
3. Check that every square is inside the map and unoccupied.
4. If any square fails, place nothing. Otherwise mark all footprint squares occupied together.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

## Mechanic and algorithm

Rotate a nonempty tile footprint in quarter-turn increments about its anchor, translate it to a world-grid cell, and reject out-of-bounds or occupied placements. Return a new occupied set only when all cells are valid.

## Read the implementation

[`python/example.py`](python/example.py) is an independent, standard-library-only Python 3.10+ module. Comments highlight decisions worth changing for your own game. There are no engine dependencies or runtime side effects on import.

## Working example and behavioral check

From the repository root:

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -p test_genre_mechanics.py -k building_placement -v
```

The corresponding `test_building_placement` in [the test suite](../../tests/test_genre_mechanics.py) demonstrates real calls, expected outputs, and boundary or rejection cases. For interactive use:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("mechanic", "mechanics/building-placement/python/example.py")
mechanic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mechanic)
# Use the public functions/classes shown in the behavioral test.
```

## Assumptions and limits

2D grid footprints, no terrain slope, structural support, road connectivity, build cost, mesh preview, or concurrent multiplayer transaction. Positive rotation is counterclockwise in Y-up coordinates.

Tune the rules for your game and extend the tests before integrating. Educational coverage is not a full genre implementation or a production-readiness guarantee. The original Python API is preserved. Eight additional native kernels are available; see the portable contract for their API and scope differences.

## Provenance

Original code written for this repository under the root [MIT license](../../LICENSE). No third-party source or assets were scraped or bundled. See [genre coverage](../../docs/genre-coverage.md) for reuse across genres and the [source policy](../../docs/sources.md) before importing additional code.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
