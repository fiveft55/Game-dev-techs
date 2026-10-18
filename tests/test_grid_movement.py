"""Behavioral checks for a real persistent tile controller, including time boundaries."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('grid_movement', ROOT / 'mechanics/grid-movement/python/example.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class GridMovementTests(unittest.TestCase):
    def test_four_directions_move_exactly_one_tile(self):
        for direction, expected in [('up',(1,0)), ('right',(2,1)), ('down',(1,2)), ('left',(0,1))]:
            with self.subTest(direction=direction):
                player = m.GridMover([[0]*3 for _ in range(3)], start=(1,1), step_seconds=0)
                result = player.update(0, direction)
                self.assertEqual(player.tile, expected)
                self.assertEqual(player.target, expected)
                self.assertEqual(player.position, expected)
                self.assertFalse(player.moving)
                self.assertEqual((result['started'], result['arrived'], result['blocked']), (1,1,False))

    def test_walls_and_all_map_edges_block_without_moving(self):
        for direction in ('up','right','down','left'):
            player = m.GridMover([[0]], step_seconds=0)
            self.assertTrue(player.update(0,direction)['blocked'])
            self.assertEqual(player.tile,(0,0))
        player = m.GridMover([[0,1],[0,0]], step_seconds=0)
        self.assertTrue(player.update(0,'right')['blocked'])
        self.assertEqual(player.tile,(0,0))
        self.assertFalse(player.update(0,'down')['blocked'])
        self.assertEqual(player.tile,(0,1))

    def test_smooth_half_step_and_exact_landing_after_release(self):
        player = m.GridMover([[0,0,0]], step_seconds=.2)
        result = player.update(.1,'right')
        self.assertEqual(player.tile,(0,0))
        self.assertEqual(player.target,(1,0))
        self.assertEqual(player.position,(.5,0))
        self.assertTrue(player.moving)
        self.assertEqual((result['started'],result['arrived']), (1,0))
        result = player.update(.1,None)
        self.assertEqual(player.position,(1,0))
        self.assertEqual(player.tile,(1,0))
        self.assertFalse(player.moving)
        self.assertEqual(result['arrived'],1)
        self.assertEqual(player.update(.8,None)['started'],0)
        self.assertEqual(player.tile,(1,0))

    def test_buffered_turn_waits_for_arrival(self):
        player = m.GridMover([[0,0],[0,0]], step_seconds=.2, buffer_seconds=.15)
        player.update(.1,'right')
        result = player.update(.1,'down')
        self.assertEqual(player.tile,(1,0))
        self.assertEqual(player.target,(1,1))
        self.assertEqual(player.position,(1,0))
        self.assertEqual((result['started'],result['arrived']), (1,1))
        player.update(.2,None)
        self.assertEqual(player.tile,(1,1))
        self.assertFalse(player.moving)

    def test_latest_pending_turn_replaces_the_previous_one(self):
        player = m.GridMover([[0,0],[0,0]], step_seconds=.3, buffer_seconds=.2)
        player.update(.1,'right')
        player.update(.05,'down')
        player.update(.15,'left')
        self.assertEqual(player.tile,(1,0))
        self.assertEqual(player.target,(0,0))
        player.update(.3,None)
        self.assertEqual(player.tile,(0,0))

    def test_expired_buffer_is_not_executed_but_exact_deadline_is_valid(self):
        for buffer, expected in ((.05,(1,0)), (.1,(1,1))):
            with self.subTest(buffer=buffer):
                player = m.GridMover([[0,0],[0,0]], step_seconds=.2, buffer_seconds=buffer)
                player.update(.1,'right')
                player.update(.1,'down')
                self.assertEqual(player.target,expected)

    def test_releasing_preserves_a_live_turn_but_stops_repeating(self):
        player = m.GridMover([[0,0],[0,0],[0,0]], step_seconds=.2, buffer_seconds=.3)
        player.update(0,'right')
        player.update(.05,'down')
        player.update(.15,None)
        self.assertEqual(player.target,(1,1))
        player.update(.2,None)
        self.assertEqual(player.tile,(1,1))
        self.assertFalse(player.moving)
        player.update(.5,None)
        self.assertEqual(player.tile,(1,1))

    def test_hold_repeat_waits_for_delay_and_resets_on_release(self):
        player = m.GridMover([[0]*8], step_seconds=0, repeat_delay=.3, repeat_interval=.1)
        self.assertEqual(player.update(0,'right')['started'],1)
        self.assertEqual(player.update(.29,'right')['started'],0)
        self.assertEqual(player.update(.01,'right')['started'],1)
        self.assertEqual(player.tile,(2,0))
        self.assertEqual(player.update(.1,'right')['started'],1)
        player.update(0,None)
        self.assertEqual(player.update(0,'right')['started'],1)
        self.assertEqual(player.tile,(4,0))
        player.update(.29,'right')
        self.assertEqual(player.tile,(4,0))

    def test_blocked_request_is_consumed_and_held_key_retries_on_schedule(self):
        player = m.GridMover([[0,1]], step_seconds=0)
        self.assertTrue(player.update(0,'right')['blocked'])
        self.assertFalse(player.update(.2,'right')['blocked'])
        self.assertTrue(player.update(.1,'right')['blocked'])
        self.assertEqual(player.tile,(0,0))

    def test_large_update_matches_many_small_updates(self):
        for step, delay, interval in ((0,.3,.1),(.1,.3,.1),(.23,.17,.07)):
            with self.subTest(step=step):
                whole = m.GridMover([[0]*20], step_seconds=step, repeat_delay=delay, repeat_interval=interval)
                split = m.GridMover([[0]*20], step_seconds=step, repeat_delay=delay, repeat_interval=interval)
                result = whole.update(.8,'right')
                started = arrived = 0
                for _ in range(80):
                    part = split.update(.01,'right')
                    started += part['started']; arrived += part['arrived']
                self.assertEqual(whole.tile,split.tile)
                self.assertEqual(whole.target,split.target)
                for a,b in zip(whole.position,split.position): self.assertAlmostEqual(a,b,places=8)
                self.assertEqual((result['started'],result['arrived']),(started,arrived))

    def test_invalid_inputs_leave_the_controller_unchanged(self):
        player = m.GridMover([[0,0]])
        for dt,direction in ((-1,None),(2,None),(float('nan'),None),(True,None),(0,'diagonal'),(0,(1,1))):
            with self.subTest(dt=dt,direction=direction):
                old = list(player._state)
                with self.assertRaises(ValueError): player.update(dt,direction)
                self.assertEqual(player._state,old)
        for grid,start in (([],(0,0)), ([[0],[0,0]],(0,0)), ([[1]],(0,0)), ([[0]],(-1,0)), ([[2]],(0,0))):
            with self.assertRaises(ValueError): m.GridMover(grid,start=start)
        for kwargs in ({'repeat_interval':0}, {'repeat_delay':0}, {'step_seconds':-1}, {'buffer_seconds':-1}):
            with self.assertRaises(ValueError): m.GridMover([[0]],**kwargs)

    def test_input_map_is_copied(self):
        world = [[0,0]]
        player = m.GridMover(world, step_seconds=0)
        world[0][1] = 1
        self.assertFalse(player.update(0,'right')['blocked'])
        self.assertEqual(player.tile,(1,0))

    def test_explicit_numeric_state_continues_between_calls(self):
        grid = [0,0,0,0]
        config = [2,2,.2,.3,.1,.15]
        initial = [0,0,0,0,0,0,0,0,0]
        first = m._advance([*config,.1,2,*initial,*grid])
        second = m._advance([*config,.1,3,*first[:9],*grid])
        third = m._advance([*config,.2,0,*second[:9],*grid])
        self.assertEqual(third[:4],[1,1,1,1])
        self.assertEqual(third[9:11],[1,1])
        self.assertEqual(third[12],1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
