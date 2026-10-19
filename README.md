# Game development reference library

An evolving learning library for reusable game algorithms, game history, and development tools. Original examples are MIT licensed. This library contains 51 original Python mechanics mapped to all 22 documented genre families, plus 408 native core-kernel implementations across eight additional languages. It is not an exhaustive archive of all games, languages, or engines.

- [Free movement: continuous positions and analog input](mechanics/player-movement/README.md)
- [Grid-based movement: instant steps, smooth slides and buffered turns](mechanics/grid-movement/README.md)
- [Beginner guide: code in plain English](docs/beginner-guide.md)
- [Game optimization handbook: theory, techniques and research](docs/optimization/README.md)
- [Eight-language ports and calling examples](docs/language-ports.md)
- [Toolchains and test commands](docs/toolchains.md)
- [Genre-to-mechanics coverage table](docs/genre-coverage.md) and [machine-readable mapping](genre-coverage.json)
- [Major genre families, 1980s–present](docs/genres.md)
- [Evolution of development technology](docs/technology-history.md)
- [Mechanics index](docs/mechanics-index.md) and [machine-readable catalog](catalog.json)
- [Multiplayer architecture and security](docs/multiplayer-security.md)
- [Sources and licensing](docs/sources.md)
- [Expansion roadmap](docs/roadmap.md)

## Choose a movement mechanic

These are separate implementations in separate folders, with independent input contracts and tests.

| Mechanic | Folder | Behavior |
|---|---|---|
| [Free movement](mechanics/player-movement/README.md) | `mechanics/player-movement/` | Move any distance using speed and elapsed time; supports analog and diagonal input. |
| [Grid movement](mechanics/grid-movement/README.md) | `mechanics/grid-movement/` | Step between adjacent tiles, check walls, and handle buffered turns and held-key repeat. |

## Start learning

Use Python 3.10+ and run `python3 tools/validate.py` from this directory. No pip install, credentials, database service, or game engine is required. Start with ASCII rendering, movement, fixed timesteps, collisions, and pathfinding; then study physics, procedural worlds, editor undo, and networking concepts.

Each mechanic has its own folder, explanation, limitations, and commented source. Implementations are deliberately small and engine-independent. Language availability is recorded explicitly; missing ports are not working implementations. The repository itself is the searchable knowledge base; `catalog.json` supports future tooling.

## Choose a genre

Open the coverage table, follow a mechanic's documentation or direct code link, and read its behavioral test for usage. Each genre row lists implemented algorithms separately from remaining integrations. All 51 mechanics have Python code plus native Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go kernels. These share a documented numeric-array contract, with explicit scope differences from Python APIs. Earlier movement-only C++/PHP examples remain available. Every mechanic now has a plain-English walkthrough and a worked input/output example.

Run all native fixtures with `python3 tools/test_ports.py --languages all`. To test one mechanic, add `--mechanic player-movement`. Missing compilers are reported as missing, not passed.

Regenerate the indexes with `python3 tools/build_indexes.py`; verify them with `python3 tools/build_indexes.py --check`.

## Contributing and future sessions

Read [AGENTS.md](AGENTS.md). Keep mechanics separate. Cite authoritative references and record licensing before importing anything. Do not upload commercial game code, extracted assets, secrets, or proprietary SDKs. Private visibility is not a redistribution license.
