# Seeded deck shuffle, draw, and discard

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Shuffle a card pile, draw cards, and reuse discarded cards when the pile runs out.

1. Shuffle by swapping cards using a repeatable number generator.
2. Drawing removes the last card from the pile.
3. If the pile is empty, shuffle the discard pile into a new draw pile.
4. If both piles are empty, return the no-card marker. This predictable shuffle is not secure against cheaters.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

## Mechanic and algorithm

A deck owns separate draw and discard piles. When the draw pile empties, reshuffle discarded cards using a local seeded RNG. The same seed and action sequence reproduce a single-player run.

## Read the implementation

[`python/example.py`](python/example.py) is an independent, standard-library-only Python 3.10+ module. Comments highlight decisions worth changing for your own game. There are no engine dependencies or runtime side effects on import.

## Working example and behavioral check

From the repository root:

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -p test_genre_mechanics.py -k deck_draw -v
```

The corresponding `test_deck_draw` in [the test suite](../../tests/test_genre_mechanics.py) demonstrates real calls, expected outputs, and boundary or rejection cases. For interactive use:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("mechanic", "mechanics/deck-draw/python/example.py")
mechanic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mechanic)
# Use the public functions/classes shown in the behavioral test.
```

## Assumptions and limits

Predictable PRNG, deliberately unsuitable for adversarial hidden-card security or real-money play. An online server must own the deck and send each player only their authorized view.

Tune the rules for your game and extend the tests before integrating. Educational coverage is not a full genre implementation or a production-readiness guarantee. The original Python API is preserved. Eight additional native kernels are available; see the portable contract for their API and scope differences.

## Provenance

Original code written for this repository under the root [MIT license](../../LICENSE). No third-party source or assets were scraped or bundled. See [genre coverage](../../docs/genre-coverage.md) for reuse across genres and the [source policy](../../docs/sources.md) before importing additional code.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
