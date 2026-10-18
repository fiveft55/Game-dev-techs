# Weighted loot selection

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Choose an item from a weighted prize list.

1. Imagine each item owns a strip of numbered raffle tickets.
2. Bigger weights give an item more tickets.
3. Find which item owns the supplied ticket number.
4. Return that item. Another part of the game must choose a fair ticket; this code does not generate secure randomness.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

## Mechanic and algorithm

Choose an item proportionally to positive integer weights using a caller-supplied random generator. Supplying the generator explicitly makes run reproduction and testing possible without global RNG state.

## Read the implementation

[`python/example.py`](python/example.py) is an independent, standard-library-only Python 3.10+ module. Comments highlight decisions worth changing for your own game. There are no engine dependencies or runtime side effects on import.

## Working example and behavioral check

From the repository root:

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -p test_genre_mechanics.py -k loot_table -v
```

The corresponding `test_loot_table` in [the test suite](../../tests/test_genre_mechanics.py) demonstrates real calls, expected outputs, and boundary or rejection cases. For interactive use:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("mechanic", "mechanics/loot-table/python/example.py")
mechanic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mechanic)
# Use the public functions/classes shown in the behavioral test.
```

## Assumptions and limits

No pity timers, rarity tiers, duplicates policy, or adversarial fairness. Use a server-owned appropriate generator for multiplayer; seeded random.Random is not a security primitive.

Tune the rules for your game and extend the tests before integrating. Educational coverage is not a full genre implementation or a production-readiness guarantee. The original Python API is preserved. Eight additional native kernels are available; see the portable contract for their API and scope differences.

## Provenance

Original code written for this repository under the root [MIT license](../../LICENSE). No third-party source or assets were scraped or bundled. See [genre coverage](../../docs/genre-coverage.md) for reuse across genres and the [source policy](../../docs/sources.md) before importing additional code.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
