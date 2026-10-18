"""Keep coverage claims aligned with the actual taxonomy, code, and tests."""
import ast
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(relative_path):
    spec = importlib.util.spec_from_file_location('checked_module', ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CoverageTests(unittest.TestCase):
    def test_every_documented_genre_is_mapped_once(self):
        # Read the actual taxonomy rather than comparing against a duplicated list.
        lines = (ROOT / 'docs/genres.md').read_text().splitlines()
        genres = [line.split('|')[1].strip() for line in lines
                  if line.startswith('| ') and not line.startswith('| Family |')]
        rows = json.loads((ROOT / 'genre-coverage.json').read_text())['genres']
        self.assertGreater(len(genres), 0)
        self.assertCountEqual([row['genre'] for row in rows], genres)
        for row in rows:
            self.assertTrue(row['implemented'], row['genre'])
            self.assertEqual(len(set(row['implemented'])), len(row['implemented']))
            self.assertTrue(row['remaining'], row['genre'])

    def test_every_catalog_entry_has_code_documentation_and_a_behavioral_test(self):
        catalog = json.loads((ROOT / 'catalog.json').read_text())
        methods = set()
        for path in (ROOT / 'tools/validate.py', ROOT / 'tests/test_genre_mechanics.py'):
            methods.update(node.name for node in ast.walk(ast.parse(path.read_text()))
                           if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'))
        self.assertEqual(len({entry['id'] for entry in catalog}), len(catalog))
        folders = {p.name for p in (ROOT / 'mechanics').iterdir() if p.is_dir()}
        self.assertEqual(folders, {entry['id'] for entry in catalog})
        for entry in catalog:
            with self.subTest(mechanic=entry['id']):
                self.assertIn('test_' + entry['id'].replace('-', '_'), methods)
                self.assertTrue((ROOT / 'mechanics' / entry['id'] / 'README.md').is_file())
                self.assertIn('python', entry['implementations'])
                for path in entry['implementations'].values():
                    resolved = (ROOT / path).resolve()
                    self.assertTrue(resolved.is_relative_to(ROOT))
                    self.assertTrue(resolved.is_file(), path)

    def test_generated_indexes_are_current_and_all_mechanics_are_mapped(self):
        builder = load('tools/build_indexes.py')
        for path, expected in builder.render().items():
            self.assertEqual((ROOT / path).read_text(), expected, path)

    def test_local_markdown_links_resolve(self):
        for path in ROOT.rglob('*.md'):
            if '.git' in path.parts:
                continue
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                self.assertTrue((path.parent / target.split('#')[0]).exists(), (path, target))


if __name__ == '__main__':
    unittest.main(verbosity=2)
