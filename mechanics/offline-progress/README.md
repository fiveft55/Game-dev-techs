# Capped idle-game offline production

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Give an idle-game player resources for time spent away, up to a limit.

1. Subtract the last saved time from the current time.
2. If the clock moved backward, count zero time.
3. Limit the counted time so a very long absence does not give unlimited rewards.
4. Multiply counted seconds by production rate. Online games must use trusted time and prevent claiming twice.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

## Mechanic and algorithm

Compute constant-rate production from the elapsed interval between a saved timestamp and now. Clamp negative clock differences to zero and cap offline seconds to bound rewards.

## Read the implementation

[`python/example.py`](python/example.py) is an independent, standard-library-only Python 3.10+ module. Comments highlight decisions worth changing for your own game. There are no engine dependencies or runtime side effects on import.

## Working example and behavioral check

From the repository root:

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -p test_genre_mechanics.py -k offline_progress -v
```

The corresponding `test_offline_progress` in [the test suite](../../tests/test_genre_mechanics.py) demonstrates real calls, expected outputs, and boundary or rejection cases. For interactive use:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("mechanic", "mechanics/offline-progress/python/example.py")
mechanic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mechanic)
# Use the public functions/classes shown in the behavioral test.
```

## Assumptions and limits

Uses Decimal for stable decimal resource arithmetic, not a full large-number economy. Client timestamps are editable: online economies need server-owned time and transactional claims. This does not prevent repeated claims.

Tune the rules for your game and extend the tests before integrating. Educational coverage is not a full genre implementation or a production-readiness guarantee. The original Python API is preserved. Eight additional native kernels are available; see the portable contract for their API and scope differences.

## Provenance

Original code written for this repository under the root [MIT license](../../LICENSE). No third-party source or assets were scraped or bundled. See [genre coverage](../../docs/genre-coverage.md) for reuse across genres and the [source policy](../../docs/sources.md) before importing additional code.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
