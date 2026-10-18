# Game development reference library

An evolving learning library for reusable game algorithms, game history, and development tools. Original examples are MIT licensed. This library currently contains 50 independent Python mechanics mapped to all 22 documented genre families. It is not an exhaustive archive of all games, languages, or engines.

- [Genre-to-mechanics coverage table](docs/genre-coverage.md) and [machine-readable mapping](genre-coverage.json)
- [Major genre families, 1980s–present](docs/genres.md)
- [Evolution of development technology](docs/technology-history.md)
- [Mechanics index](docs/mechanics-index.md) and [machine-readable catalog](catalog.json)
- [Multiplayer architecture and security](docs/multiplayer-security.md)
- [Sources and licensing](docs/sources.md)
- [Expansion roadmap](docs/roadmap.md)

## Start learning

Use Python 3.10+ and run `python3 tools/validate.py` from this directory. No pip install, credentials, database service, or game engine is required. Start with ASCII rendering, movement, fixed timesteps, collisions, and pathfinding; then study physics, procedural worlds, editor undo, and networking concepts.

Each mechanic has its own folder, explanation, limitations, and commented source. Implementations are deliberately small and engine-independent. Language availability is recorded explicitly; missing ports are not working implementations. The repository itself is the searchable knowledge base; `catalog.json` supports future tooling.

## Choose a genre

Open the coverage table, follow a mechanic's documentation or direct code link, and read its behavioral test for usage. Each genre row lists implemented algorithms separately from remaining integrations. All 50 mechanics have Python code; only movement currently has the seven additional language ports. C#, Lua, PHP, and Rust ports have not been executed in this workspace.

Regenerate the indexes with `python3 tools/build_indexes.py`; verify them with `python3 tools/build_indexes.py --check`.

## Contributing and future sessions

Read [AGENTS.md](AGENTS.md). Keep mechanics separate. Cite authoritative references and record licensing before importing anything. Do not upload commercial game code, extracted assets, secrets, or proprietary SDKs. Private visibility is not a redistribution license.
