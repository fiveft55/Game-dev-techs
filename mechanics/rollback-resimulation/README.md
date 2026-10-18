# Deterministic rollback and resimulation

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Fix an old game state, then redo later moves so the present agrees with that correction.

1. Keep the state before and after each numbered update.
2. Replace the state at the corrected update with the trusted value.
3. Apply every later recorded input again.
4. Return the corrected history. Do not replay real-world side effects such as charging money.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

## Mechanic and algorithm

Keep a snapshot before each simulation tick and the inputs used for it. When an authoritative correction arrives, restore the old state and replay later inputs. This example uses integer movement so the tiny simulation is exactly deterministic.

## Read the implementation

[`python/example.py`](python/example.py) is an independent, standard-library-only Python 3.10+ module. Comments highlight decisions worth changing for your own game. There are no engine dependencies or runtime side effects on import.

## Working example and behavioral check

From the repository root:

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -p test_genre_mechanics.py -k rollback_resimulation -v
```

The corresponding `test_rollback_resimulation` in [the test suite](../../tests/test_genre_mechanics.py) demonstrates real calls, expected outputs, and boundary or rejection cases. For interactive use:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("mechanic", "mechanics/rollback-resimulation/python/example.py")
mechanic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mechanic)
# Use the public functions/classes shown in the behavioral test.
```

## Assumptions and limits

Unbounded educational history, one-dimensional state, no input prediction, transport, animation effects, or production snapshot compression. Real games need bounded history and deterministic rules across peers; do not replay external side effects such as payments.

Tune the rules for your game and extend the tests before integrating. Educational coverage is not a full genre implementation or a production-readiness guarantee. The original Python API is preserved. Eight additional native kernels are available; see the portable contract for their API and scope differences.

## Provenance

Original code written for this repository under the root [MIT license](../../LICENSE). No third-party source or assets were scraped or bundled. See [genre coverage](../../docs/genre-coverage.md) for reuse across genres and the [source policy](../../docs/sources.md) before importing additional code.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
