# World-to-chunk coordinates

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Find which big map piece owns a world tile, and where that tile sits inside the piece.

1. Divide the world coordinate by the piece size and round downward.
2. That gives the chunk, or big piece, number.
3. Subtract the chunk start to get the local tile number.
4. Rounding downward matters: world tile -1 is in chunk -1, at the last local tile.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

## Mechanic and algorithm

Split integer world coordinates into chunk coordinates and nonnegative local coordinates. Floor division is essential for negative positions: tile -1 belongs to chunk -1, local size-1.

## Read the implementation

[`python/example.py`](python/example.py) is an independent, standard-library-only Python 3.10+ module. Comments highlight decisions worth changing for your own game. There are no engine dependencies or runtime side effects on import.

## Working example and behavioral check

From the repository root:

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -p test_genre_mechanics.py -k chunk_coordinates -v
```

The corresponding `test_chunk_coordinates` in [the test suite](../../tests/test_genre_mechanics.py) demonstrates real calls, expected outputs, and boundary or rejection cases. For interactive use:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("mechanic", "mechanics/chunk-coordinates/python/example.py")
mechanic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mechanic)
# Use the public functions/classes shown in the behavioral test.
```

## Assumptions and limits

2D coordinate mapping only, no chunk streaming, mesh generation, file I/O, or floating-origin management.

Tune the rules for your game and extend the tests before integrating. Educational coverage is not a full genre implementation or a production-readiness guarantee. The original Python API is preserved. Eight additional native kernels are available; see the portable contract for their API and scope differences.

## Provenance

Original code written for this repository under the root [MIT license](../../LICENSE). No third-party source or assets were scraped or bundled. See [genre coverage](../../docs/genre-coverage.md) for reuse across genres and the [source policy](../../docs/sources.md) before importing additional code.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
