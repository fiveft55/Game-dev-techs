# Swept projectile versus rectangle

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Check whether a fast bullet passed through a box between two updates.

1. Draw the entire line from the bullet old position to its new position.
2. Find the part of that line that is inside the box left-to-right.
3. Find the part that is inside the box bottom-to-top.
4. If those parts overlap, return the first hit point as a fraction of the move. A fraction of 0.4 means 40 percent along.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

## Mechanic and algorithm

The slab intersection algorithm finds the first contact of a moving point with an axis-aligned rectangle over one update. The return value is a fraction of the segment, from zero to one; None means no collision. This avoids discrete point-sampling tunneling.

## Read the implementation

[`python/example.py`](python/example.py) is an independent, standard-library-only Python 3.10+ module. Comments highlight decisions worth changing for your own game. There are no engine dependencies or runtime side effects on import.

## Working example and behavioral check

From the repository root:

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -p test_genre_mechanics.py -k projectile_sweep -v
```

The corresponding `test_projectile_sweep` in [the test suite](../../tests/test_genre_mechanics.py) demonstrates real calls, expected outputs, and boundary or rejection cases. For interactive use:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("mechanic", "mechanics/projectile-sweep/python/example.py")
mechanic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mechanic)
# Use the public functions/classes shown in the behavioral test.
```

## Assumptions and limits

2D finite inputs, point projectile, stationary rectangle, no penetration or response. Inflate a rectangle for a box projectile; a circle needs appropriate rounded geometry.

Tune the rules for your game and extend the tests before integrating. Educational coverage is not a full genre implementation or a production-readiness guarantee. The original Python API is preserved. Eight additional native kernels are available; see the portable contract for their API and scope differences.

## Provenance

Original code written for this repository under the root [MIT license](../../LICENSE). No third-party source or assets were scraped or bundled. See [genre coverage](../../docs/genre-coverage.md) for reuse across genres and the [source policy](../../docs/sources.md) before importing additional code.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
