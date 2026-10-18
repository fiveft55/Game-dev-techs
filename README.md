# Game development reference library

An evolving learning library for reusable game algorithms, game history, and development tools. Original examples are MIT licensed. This is a first edition, not an exhaustive archive of all games, languages, or engines.

- [Major genre families, 1980s–present](docs/genres.md)
- [Evolution of development technology](docs/technology-history.md)
- [Mechanics index](docs/mechanics-index.md) and [machine-readable catalog](catalog.json)
- [Multiplayer architecture and security](docs/multiplayer-security.md)
- [Sources and licensing](docs/sources.md)
- [Expansion roadmap](docs/roadmap.md)

## Start learning

Use Python 3.10+ and run `python3 tools/validate.py` from this directory. No pip install, credentials, database service, or game engine is required. Start with ASCII rendering, movement, fixed timesteps, collisions, and pathfinding; then study physics, procedural worlds, editor undo, and networking concepts.

Each mechanic has its own folder, explanation, limitations, and commented source. Implementations are deliberately small and engine-independent. Language availability is recorded explicitly; missing ports are not working implementations. The repository itself is the searchable knowledge base; `catalog.json` supports future tooling.

## Contributing and future sessions

Read [AGENTS.md](AGENTS.md). Keep mechanics separate. Cite authoritative references and record licensing before importing anything. Do not upload commercial game code, extracted assets, secrets, or proprietary SDKs. Private visibility is not a redistribution license.
