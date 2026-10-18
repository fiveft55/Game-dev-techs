# Learning review scheduling

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Choose when a learning question should be asked again.

1. Read the previous waiting period and whether the answer was correct.
2. A correct answer doubles the wait, starting at one day.
3. An incorrect answer resets the wait to one day.
4. Add that wait to the current time to get the next review time. This is a simple teaching example, not a proven learning model.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

## Mechanic and algorithm

A simple educational-game scheduler doubles a successful review interval, starting at one day, and resets it after a failed answer. Return interval and next due time in seconds.

## Read the implementation

[`python/example.py`](python/example.py) is an independent, standard-library-only Python 3.10+ module. Comments highlight decisions worth changing for your own game. There are no engine dependencies or runtime side effects on import.

## Working example and behavioral check

From the repository root:

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -p test_genre_mechanics.py -k spaced_repetition -v
```

The corresponding `test_spaced_repetition` in [the test suite](../../tests/test_genre_mechanics.py) demonstrates real calls, expected outputs, and boundary or rejection cases. For interactive use:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("mechanic", "mechanics/spaced-repetition/python/example.py")
mechanic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mechanic)
# Use the public functions/classes shown in the behavioral test.
```

## Assumptions and limits

This is a transparent toy scheduling policy, not SM-2, FSRS, a validated learning intervention, or a diagnostic/assessment model. Track a trusted review clock and protect learner data.

Tune the rules for your game and extend the tests before integrating. Educational coverage is not a full genre implementation or a production-readiness guarantee. The original Python API is preserved. Eight additional native kernels are available; see the portable contract for their API and scope differences.

## Provenance

Original code written for this repository under the root [MIT license](../../LICENSE). No third-party source or assets were scraped or bundled. See [genre coverage](../../docs/genre-coverage.md) for reuse across genres and the [source policy](../../docs/sources.md) before importing additional code.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
