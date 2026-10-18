"""Run real behavioral examples without third-party dependencies."""
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
def load(slug):
    spec=importlib.util.spec_from_file_location(slug,ROOT/'mechanics'/slug/'python'/'example.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class MechanicsTests(unittest.TestCase):
    def test_fixed_timestep(self):
        m = load('fixed-timestep')
        assert m.advance(0, .05, .02) == (2, .010000000000000002)

    def test_player_movement(self):
        m = load('player-movement')
        assert m.move(0, 0, 1, 0, 4, .5) == (2, 0)
        assert abs(sum(v*v for v in m.move(0,0,1,1,1,1))-1)<1e-9

    def test_aabb_collision(self):
        m = load('aabb-collision')
        assert m.overlaps((0,0,1,1),(1,0,1,1))
        assert not m.overlaps((0,0,1,1),(2,2,1,1))

    def test_grid_pathfinding(self):
        m = load('grid-pathfinding')
        assert m.path([[0,1,0],[0,0,0]],(0,0),(2,0)) == [(0,0),(0,1),(1,1),(2,1),(2,0)]
        assert m.path([[0,1,0]],(0,0),(2,0)) == []

    def test_raycasting(self):
        m = load('raycasting')
        assert m.cast([[0,0,1]],(.5,.5),(1,0)) == (2,0,1.5)

    def test_rigid_body_integration(self):
        m = load('rigid-body-integration')
        assert m.integrate((0,0),(0,0),(0,-10),.1) == ((0.0,-0.1),(0.0,-1.0))

    def test_steering_arrival(self):
        m = load('steering-arrival')
        assert m.desired_velocity((0,0),(1,0),10,5)==(2,0)
        assert m.desired_velocity((0,0),(0,0),10,5)==(0,0)

    def test_finite_state_machine(self):
        m = load('finite-state-machine')
        fsm=m.Machine("idle",{("idle","jump"):"air"})
        assert not fsm.send("land")
        assert fsm.send("jump") and fsm.state=="air"

    def test_inventory(self):
        m = load('inventory')
        assert m.add([("wood",60)],"wood",10,64,2)==([("wood",64),("wood",6)],0)
        assert m.add([],"wood",70,64,1)==([("wood",64)],6)

    def test_ascii_world(self):
        m = load('ascii-world')
        assert m.render([[1,1,1],[1,0,1]],(1,1))=="###\n#@#"

    def test_procedural_maze(self):
        m = load('procedural-maze')
        assert m.generate(9,9,42)==m.generate(9,9,42)
        assert sum(row.count(0) for row in m.generate(9,9))==31

    def test_camera_follow(self):
        m = load('camera-follow')
        assert abs(m.follow(m.follow(0,10,3,.1),10,3,.1)-m.follow(0,10,3,.2))<1e-12

    def test_spatial_hash(self):
        m = load('spatial-hash')
        b=m.build({"a":(-.1,0),"b":(10,10)},1)
        assert m.nearby(b,(0,0),1)==["a"]

    def test_racing_bicycle_model(self):
        m = load('racing-bicycle-model')
        assert m.drive(0,0,0,10,0,2,.1)==(1,0,0)

    def test_snapshot_interpolation(self):
        m = load('snapshot-interpolation')
        assert m.interpolate((0,(0,0)),(1,(10,20)),.5)==(5,10)
        assert m.interpolate((0,(0,)),(1,(10,)),2)==(10,)

    def test_replay_window(self):
        m = load('replay-window')
        w=m.ReplayWindow(4)
        assert w.accept(5) and w.accept(3)
        assert not w.accept(3) and not w.accept(1)
        assert w.accept(10**9)

    def test_level_editor_undo(self):
        m = load('level-editor-undo')
        e=m.Editor(2,2); e.paint(1,1,3)
        assert e.undo() and e.grid[1][1]==0
        assert e.redo() and e.grid[1][1]==3
        e.undo(); e.paint(0,0,2); assert not e.redo()

    def test_cad_extrusion(self):
        m = load('cad-extrusion')
        v,f=m.extrude([(0,0),(1,0),(1,1),(0,1)],2)
        assert len(v)==8 and len(f)==12
        assert all(0<=i<len(v) for triangle in f for i in triangle)

if __name__=='__main__':
    # Keep one entry point for both the original examples and the expanded library.
    import sys
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(MechanicsTests)
    suite.addTests(unittest.defaultTestLoader.discover(str(ROOT / 'tests')))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
