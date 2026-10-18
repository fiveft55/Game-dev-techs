# Authoritative movement command validation

## Mechanic and algorithm

The server accepts normalized input directions and increasing integer sequence numbers, then advances position with a server-selected fixed timestep. Reject malformed, stale, infinite, and oversized input instead of accepting a client position or client elapsed time.

## Read the implementation

[`python/example.py`](python/example.py) is an independent, standard-library-only Python 3.10+ module. Comments highlight decisions worth changing for your own game. There are no engine dependencies or runtime side effects on import.

## Working example and behavioral check

From the repository root:

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -p test_genre_mechanics.py -k server_input_validation -v
```

The corresponding `test_server_input_validation` in [the test suite](../../tests/test_genre_mechanics.py) demonstrates real calls, expected outputs, and boundary or rejection cases. For interactive use:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("mechanic", "mechanics/server-input-validation/python/example.py")
mechanic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mechanic)
# Use the public functions/classes shown in the behavioral test.
```

## Assumptions and limits

No actual sockets, authentication, world collision, rate limiting, encryption, or persistence. Call once per server simulation tick; draining an arbitrary number of commands per tick would permit speed hacks.

Tune the rules for your game and extend the tests before integrating. Educational coverage is not a full genre implementation or a production-readiness guarantee. This entry currently has Python code; other language ports are not present.

## Provenance

Original code written for this repository under the root [MIT license](../../LICENSE). No third-party source or assets were scraped or bundled. See [genre coverage](../../docs/genre-coverage.md) for reuse across genres and the [source policy](../../docs/sources.md) before importing additional code.
