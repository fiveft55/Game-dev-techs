"""Generate navigable indexes from the catalog and genre mapping; --check detects drift."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render():
    catalog = json.loads((ROOT / 'catalog.json').read_text())
    coverage = json.loads((ROOT / 'genre-coverage.json').read_text())
    by_id = {entry['id']: entry for entry in catalog}
    if len(by_id) != len(catalog):
        raise ValueError('duplicate catalog IDs')
    for entry in catalog:
        for path in entry['implementations'].values():
            if not (ROOT / path).is_file():
                raise ValueError(f'missing code: {path}')

    def mechanic_link(slug):
        entry = by_id[slug]
        return f"[{entry['title']}](../mechanics/{slug}/README.md) ([Python](../{entry['implementations']['python']}), [8-language ports](../mechanics/{slug}/PORTS.md))"

    table = [
        '# Genre-to-mechanics coverage',
        '',
        'All 22 families in the genre history have a representative set of implemented core algorithms below. '
        'Every mechanic has links to its documentation, original Python source, and eight-language port contract. Each module has behavioral checks.',
        '',
        '**Coverage means reusable educational code exists, not that an entire genre, engine, or multiplayer game is complete.** '
        'The remaining column records concrete work outside this implementation set. '
        f'All {len(catalog)} entries additionally have native Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go kernels. '
        'Their numeric-array contracts and any scope differences from Python are documented per mechanic in PORTS.md and in [language conventions](language-ports.md).',
        '',
        'Run `python3 tools/validate.py` from the repository root. See [validation evidence](validation.md). '
        'All included code is original and MIT licensed; no third-party game source was scraped.',
        '',
        '| Genre family | Implemented mechanics — documentation and code | Remaining genre-specific systems |',
        '|---|---|---|',
    ]
    covered = set()
    for row in coverage['genres']:
        covered.update(row['implemented'])
        links = '; '.join(mechanic_link(slug) for slug in row['implemented'])
        table.append(f"| {row['genre']} | {links} | {row['remaining']} |")
    table += ['', '## Cross-cutting tools', '']
    for slug in coverage['cross_cutting']:
        covered.add(slug)
        table.append('- ' + mechanic_link(slug))
    if covered != set(by_id):
        raise ValueError(f'unmapped or unknown IDs: {covered ^ set(by_id)}')
    table += [
        '', '## Maintaining the mapping', '',
        'Edit [genre-coverage.json](../genre-coverage.json) and [catalog.json](../catalog.json), '
        'then run `python3 tools/build_indexes.py`. Run `python3 tools/build_indexes.py --check` to detect stale generated indexes. '
        'Do not add an implemented ID without real source and behavioral checks. Remaining systems are a backlog, not a list of completed implementations.',
    ]
    index = [
        '# Mechanics index', '',
        f'{len(catalog)} independent educational mechanics have original Python APIs and eight-language portable kernels with behavioral checks. '
        'See the [genre coverage table](genre-coverage.md) to choose a starting point by genre.', '',
        '| Mechanic | Available source code |', '|---|---|',
    ]
    for entry in catalog:
        links = ', '.join(f'[{language}](../{path})' for language, path in entry['implementations'].items())
        index.append(f"| [{entry['title']}](../mechanics/{entry['id']}/README.md) | {links} |")
    return {'docs/genre-coverage.md': '\n'.join(table)+'\n', 'docs/mechanics-index.md': '\n'.join(index)+'\n'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for path, content in render().items():
        target = ROOT / path
        if args.check:
            if not target.exists() or target.read_text() != content:
                stale.append(path)
        else:
            target.write_text(content)
    if stale:
        parser.exit(1, 'Stale indexes: '+', '.join(stale)+'\n')
    print('Indexes match source data' if args.check else 'Indexes generated')


if __name__ == '__main__':
    main()
