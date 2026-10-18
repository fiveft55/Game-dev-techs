"""Representative mechanics composed without an engine or network dependency."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def mechanic(slug):
    spec = importlib.util.spec_from_file_location(slug, ROOT / 'mechanics' / slug / 'python/example.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CompositionTests(unittest.TestCase):
    def test_fog_respects_walls_and_keeps_exploration_history(self):
        sight = mechanic('line-of-sight')
        fog = mechanic('fog-of-war').Fog(4, 1)
        grid = [[0, 1, 0, 0]]
        fog.update([(0, 0)], 4, lambda a, b: sight.visible(grid, a, b))
        self.assertEqual(fog.visible, {(0, 0)})
        fog.update([(3, 0)], 4, lambda a, b: sight.visible(grid, a, b))
        self.assertEqual(fog.visible, {(2, 0), (3, 0)})
        self.assertEqual(fog.explored, {(0, 0), (2, 0), (3, 0)})

    def test_weapon_cooldown_sweep_and_damage(self):
        cooldown = mechanic('ability-cooldown').Cooldown(duration=.5)
        projectile = mechanic('projectile-sweep')
        stats = mechanic('rpg-progression')
        hp = 20
        for now in (0, .1, .5):
            if cooldown.use(now) and projectile.hit_fraction((0, 0), (10, 0), (5, -1, 1, 2)) is not None:
                hp -= stats.damage(8, 3)
        self.assertEqual(hp, 10)  # Only two of the three fire attempts can shoot.

    def test_crafting_roundtrips_through_a_versioned_save(self):
        import json
        crafting = mechanic('crafting-recipes')
        saves = mechanic('save-migration')
        old = saves.load_save('{"version":1,"gold":7}')
        crafted = crafting.craft(old['inventory'], {'gold': 3}, {'potion': 1}, 2)
        new = saves.load_save(json.dumps({'version': 2, 'inventory': crafted}))
        self.assertEqual(new['inventory'], {'gold': 1, 'potion': 2})
        self.assertEqual(old['inventory'], {'gold': 7})

    def test_authority_correction_replays_integer_inputs(self):
        rollback = mechanic('rollback-resimulation').Rollback
        predicted = rollback(0, lambda state, command: state + command)
        predicted.advance(2)
        predicted.advance(2)
        predicted.advance(-1)
        # The server corrects tick 1 from position 2 to 1; later inputs are retained.
        self.assertEqual(predicted.correct(1, 1), 2)
        authoritative = rollback(0, lambda state, command: state + command)
        for command in (1, 2, -1):
            authoritative.advance(command)
        self.assertEqual(predicted.current, authoritative.current)


if __name__ == '__main__':
    unittest.main(verbosity=2)
