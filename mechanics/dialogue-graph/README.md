# Conditional branching dialogue

<!-- BEGIN PLAIN ENGLISH -->
## Plain-English explanation

Choose which conversation options are allowed and where the conversation goes next.

1. Keep the current conversation node and simple yes-or-no story flags.
2. Look for the chosen event among options leaving that node.
3. Require the necessary flags before allowing the choice.
4. Grant new flags and move to the next node. Flag values 1, 2, and 4 are separate switches; adding them can store several switches together.

See [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. The [beginner guide](../../docs/beginner-guide.md) explains common coding words.
<!-- END PLAIN ENGLISH -->

## Mechanic and algorithm

Dialogue nodes contain text and choices. A choice has a label, destination, required flags, and flags granted on selection. Resolve choices against current flags so story conditions stay explicit.

## Read the implementation

[`python/example.py`](python/example.py) is an independent, standard-library-only Python 3.10+ module. Comments highlight decisions worth changing for your own game. There are no engine dependencies or runtime side effects on import.

## Working example and behavioral check

From the repository root:

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -p test_genre_mechanics.py -k dialogue_graph -v
```

The corresponding `test_dialogue_graph` in [the test suite](../../tests/test_genre_mechanics.py) demonstrates real calls, expected outputs, and boundary or rejection cases. For interactive use:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("mechanic", "mechanics/dialogue-graph/python/example.py")
mechanic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mechanic)
# Use the public functions/classes shown in the behavioral test.
```

## Assumptions and limits

No parser, localization, voice/audio, cinematic sequencing, or save integration. Flags use set membership; more expressive predicates need a constrained data schema, not eval.

Tune the rules for your game and extend the tests before integrating. Educational coverage is not a full genre implementation or a production-readiness guarantee. The original Python API is preserved. Eight additional native kernels are available; see the portable contract for their API and scope differences.

## Provenance

Original code written for this repository under the root [MIT license](../../LICENSE). No third-party source or assets were scraped or bundled. See [genre coverage](../../docs/genre-coverage.md) for reuse across genres and the [source policy](../../docs/sources.md) before importing additional code.

## Portable language versions

Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go implementations are documented in [PORTS.md](PORTS.md), including input/output layouts, code links, fixtures, and scope differences from this Python API.
