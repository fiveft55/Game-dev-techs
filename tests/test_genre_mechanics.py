"""Behavioral checks for independent genre mechanics; no external packages."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load(slug):
    path = ROOT / 'mechanics' / slug / 'python' / 'example.py'
    spec = importlib.util.spec_from_file_location(slug, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class GenreMechanicsTests(unittest.TestCase):
    def test_score_lives(self):
        m = load('score-lives')
        s = m.Score(1, 100)
        s.award(250)
        self.assertEqual((s.points, s.lives), (250, 3))
        s.award(49)
        self.assertEqual(s.lives, 3)
        self.assertFalse(s.lose_life())
        self.assertFalse(s.lose_life())
        self.assertTrue(s.lose_life())
        with self.assertRaises(ValueError): s.award(-1)

    def test_jump_controller(self):
        m = load('jump-controller')
        j = m.Jump()
        self.assertFalse(j.update(0, True, False))
        self.assertTrue(j.update(.05, False, True))
        self.assertFalse(j.update(.06, False, True))
        k = m.Jump()
        self.assertFalse(k.update(0, False, True))
        self.assertTrue(k.update(.05, True, False))
        self.assertFalse(k.update(.06, True, True))
        with self.assertRaises(ValueError): k.update(.01, False, False)

    def test_projectile_sweep(self):
        m = load('projectile-sweep')
        self.assertAlmostEqual(m.hit_fraction((0,0),(10,0),(4,-1,2,2)), .4)
        self.assertIsNone(m.hit_fraction((0,3),(10,3),(4,-1,2,2)))
        self.assertEqual(m.hit_fraction((5,0),(5,0),(4,-1,2,2)), 0)
        self.assertAlmostEqual(m.hit_fraction((10,0),(0,0),(4,-1,2,2)), .4)
        with self.assertRaises(ValueError): m.hit_fraction((0,0),(1,1),(0,0,-1,2))

    def test_combat_frames(self):
        m = load('combat-frames')
        a = m.Attack(2, 2, 3)
        self.assertEqual([a.phase(i) for i in (0,2,4,7)], ['startup','active','recovery','finished'])
        self.assertFalse(a.try_hit(1,'enemy',True))
        self.assertTrue(a.try_hit(2,'enemy',True))
        self.assertFalse(a.try_hit(3,'enemy',True))
        self.assertTrue(a.try_hit(3,'other',True))
        with self.assertRaises(ValueError): m.Attack(0,0,1)

    def test_line_of_sight(self):
        m = load('line-of-sight')
        self.assertTrue(m.visible([[0,0,0]],(0,0),(2,0)))
        self.assertFalse(m.visible([[0,1,0]],(0,0),(2,0)))
        self.assertFalse(m.visible([[0,1],[1,0]],(0,0),(1,1)))
        self.assertTrue(m.visible([[0,0],[0,0]],(1,1),(0,0)))
        self.assertFalse(m.visible([[0]],(0,0),(1,0)))

    def test_rpg_progression(self):
        m = load('rpg-progression')
        self.assertEqual([m.level_for(x) for x in (0,99,100,10000)], [1,1,2,5])
        self.assertEqual(m.damage(10,12), 0)
        self.assertEqual(m.damage(10,2), 8)
        with self.assertRaises(ValueError): m.level_for(5,(0,100,50))

    def test_quest_objectives(self):
        m = load('quest-objectives')
        q=m.Quest({'gather':2,'talk':1})
        self.assertFalse(q.claim())
        q.record('gather',99); q.record('ignored'); q.record('talk')
        self.assertTrue(q.complete)
        self.assertTrue(q.claim())
        self.assertFalse(q.claim())
        self.assertEqual(q.progress['gather'],2)
        with self.assertRaises(ValueError): q.record('talk',-1)

    def test_dialogue_graph(self):
        m = load('dialogue-graph')
        d=m.Dialogue({'a':{'text':'Hi','choices':[
         {'label':'Key','next':'a','grants':['key']},
         {'label':'Enter','next':'b','requires':['key']}]},'b':{'text':'Inside'}},'a')
        self.assertEqual(len(d.choices()),1)
        d.choose(0)
        self.assertEqual(len(d.choices()),2)
        self.assertEqual(d.choose(1),'Inside')
        with self.assertRaises(ValueError): d.choose(0)

    def test_turn_order(self):
        m = load('turn-order')
        t=m.Turns({'b':10,'a':10,'c':1})
        self.assertEqual(t.current,'a')
        self.assertEqual(t.advance(),'b')
        t.remove('a'); self.assertEqual(t.current,'b')
        t.remove('b'); self.assertEqual(t.current,'c')
        t.remove('c'); self.assertIsNone(t.current)
        self.assertIsNone(t.advance())

    def test_resource_economy(self):
        m = load('resource-economy')
        b={'gold':5}
        self.assertIsNone(m.transact(b,{'gold':6}))
        self.assertEqual(b,{'gold':5})
        self.assertEqual(m.transact(b,{'gold':3},{'wood':2}),{'gold':2,'wood':2})
        with self.assertRaises(ValueError): m.transact(b,{'gold':-1})

    def test_fog_of_war(self):
        m = load('fog-of-war')
        f=m.Fog(5,1)
        f.update([(0,0)],1)
        self.assertEqual(f.visible,{(0,0),(1,0)})
        f.update([(4,0)],0)
        self.assertEqual(f.visible,{(4,0)})
        self.assertIn((0,0),f.explored)
        f.update([(2,0)],1,lambda a,b:b==(2,0))
        self.assertEqual(f.visible,{(2,0)})
        with self.assertRaises(ValueError): f.update([], -1)

    def test_wave_spawner(self):
        m = load('wave-spawner')
        w=m.Wave([(1,'a'),(1,'b'),(3,'boss')])
        self.assertEqual(w.update(0),[])
        self.assertEqual(w.update(2),['a','b'])
        self.assertEqual(w.update(2),[])
        self.assertEqual(w.update(4),['boss'])
        self.assertTrue(w.finished)
        with self.assertRaises(ValueError): w.update(1)

    def test_event_scheduler(self):
        m = load('event-scheduler')
        s=m.Scheduler(); s.schedule(2,{'job':'a'}); s.schedule(2,{'job':'b'}); s.schedule(1,'first')
        self.assertEqual(s.advance(1),[(1,'first')])
        self.assertEqual(s.advance(2),[(2,{'job':'a'}),(2,{'job':'b'})])
        self.assertEqual(s.advance(3),[])
        with self.assertRaises(ValueError): s.schedule(2,'late')

    def test_racing_checkpoints(self):
        m = load('racing-checkpoints')
        r=m.Race(2,2)
        self.assertFalse(r.enter(1)); r.exit(1)
        self.assertTrue(r.enter(0)); self.assertFalse(r.enter(0)); r.exit(0)
        self.assertTrue(r.enter(1)); r.exit(1)
        self.assertEqual(r.laps,1)
        r.enter(0); r.exit(0); r.enter(1)
        self.assertTrue(r.finished)
        with self.assertRaises(ValueError): r.enter(2)

    def test_ball_reflection(self):
        m = load('ball-reflection')
        self.assertEqual(m.bounce((2,-3),(0,2)),(2,3))
        self.assertEqual(m.bounce((2,-3),(0,1),.5),(2,1.5))
        self.assertEqual(m.bounce((2,3),(0,1)),(2,3))
        with self.assertRaises(ValueError): m.bounce((1,1),(0,0))

    def test_match_grid(self):
        m = load('match-grid')
        b=[[1,2,3],[1,1,1],[1,2,3]]
        found=m.matches(b)
        self.assertEqual(found,{(0,0),(0,1),(0,2),(1,1),(2,1)})
        self.assertEqual(m.clear_and_fall(b,found),[[None,None,None],[None,2,3],[None,2,3]])
        self.assertEqual(b[1],[1,1,1])
        self.assertEqual(m.matches([[None,None,None]]),set())
        with self.assertRaises(ValueError): m.matches([[1],[1,2]])

    def test_rhythm_judgement(self):
        m = load('rhythm-judgement')
        n=m.Note(1)
        self.assertIsNone(n.press(.5))
        self.assertEqual(n.press(1.1,.1),'perfect')
        self.assertIsNone(n.press(1))
        late=m.Note(1)
        self.assertEqual(late.expire(1.2),'miss')
        self.assertIsNone(late.press(1.2))
        with self.assertRaises(ValueError): m.Note(1,.1,.01)

    def test_crafting_recipes(self):
        m = load('crafting-recipes')
        bag={'wood':5}
        self.assertEqual(m.craft(bag,{'wood':2},{'plank':3},2),{'wood':1,'plank':6})
        self.assertIsNone(m.craft(bag,{'wood':2},{'plank':3},3))
        self.assertEqual(bag,{'wood':5})
        self.assertIsNone(m.craft({}, {'wood':1}, {'wood':2}))
        with self.assertRaises(ValueError): m.craft(bag,{'wood':2},{'plank':3},0)

    def test_chunk_coordinates(self):
        m = load('chunk-coordinates')
        self.assertEqual(m.split(-1,-17),((-1,-2),(15,15)))
        for x in range(-35,36):
         for y in (-17,0,16):
          chunk,local=m.split(x,y)
          self.assertEqual(m.join(chunk,local),(x,y))
        with self.assertRaises(ValueError): m.join((0,0),(16,0))

    def test_interest_management(self):
        m = load('interest-management')
        entities={'public':(1,0),'secret':(0,0),'far':(10,0)}
        self.assertEqual(m.relevant(entities,(0,0),2,lambda i:i!='secret'),['public'])
        self.assertEqual(m.relevant(entities,(0,0),0,lambda i:True),['secret'])
        with self.assertRaises(ValueError): m.relevant(entities,(0,0),-1,lambda i:True)

    def test_shrinking_zone(self):
        m = load('shrinking-zone')
        self.assertEqual(m.zone((0,0),(10,0),100,20,0,10,5),((5,0),60))
        self.assertEqual(m.zone((0,0),(10,0),100,20,0,10,20),((10,0),20))
        self.assertEqual(m.damage((5,0),(0,0),5,10,1),0)
        self.assertEqual(m.damage((6,0),(0,0),5,10,.5),5)
        with self.assertRaises(ValueError): m.zone((0,0),(0,0),10,20,0,10,1)

    def test_ballot_resolution(self):
        m = load('ballot-resolution')
        self.assertEqual(m.resolve(['a','b','c'],['a','b'],{'a':'b','b':'b','c':None}),'b')
        self.assertIsNone(m.resolve(['a','b'],['a','b'],{'a':'b','b':'a'}))
        self.assertIsNone(m.resolve(['a'],['a'],{'a':None}))
        with self.assertRaises(ValueError): m.resolve(['a'],['a'],{'intruder':'a'})

    def test_deck_draw(self):
        m = load('deck-draw')
        a=m.Deck(range(10),42); b=m.Deck(range(10),42)
        x=[a.draw() for _ in range(10)]
        self.assertEqual(x,[b.draw() for _ in range(10)])
        self.assertEqual(set(x),set(range(10)))
        self.assertIsNone(a.draw())
        a.discard('returned'); self.assertEqual(a.draw(),'returned')

    def test_spaced_repetition(self):
        m = load('spaced-repetition')
        self.assertEqual(m.review(0,True,100),(1,86500))
        self.assertEqual(m.review(4,True,0),(8,691200))
        self.assertEqual(m.review(8,False,0),(1,86400))
        with self.assertRaises(ValueError): m.review(-1,True,0)

    def test_offline_progress(self):
        m = load('offline-progress')
        from decimal import Decimal
        self.assertEqual(m.production('0.1',0,3),Decimal('0.3'))
        self.assertEqual(m.production(2,0,100,10),20)
        self.assertEqual(m.production(2,100,0),0)
        with self.assertRaises(ValueError): m.production(-1,0,1)

    def test_save_migration(self):
        m = load('save-migration')
        self.assertEqual(m.load_save('{"version":1,"gold":4}'),{'version':2,'inventory':{'gold':4}})
        self.assertEqual(m.load_save('{"version":2,"inventory":{}}'),{'version':2,'inventory':{}})
        for bad in ('[]','{"version":3}','{"version":2,"inventory":{"gold":-1}}','{"version":true}','not json'):
         with self.assertRaises(ValueError): m.load_save(bad)
        with self.assertRaises(ValueError): m.load_save(' '*65537)

    def test_ability_cooldown(self):
        m = load('ability-cooldown')
        c=m.Cooldown(2,3)
        self.assertTrue(c.use(0)); self.assertTrue(c.use(1)); self.assertFalse(c.use(2))
        self.assertEqual(c.available(3),1)
        self.assertEqual(c.available(4),2)
        with self.assertRaises(ValueError): c.available(2)

    def test_loot_table(self):
        m = load('loot-table')
        class Fixed:
         def __init__(self,n): self.n=n
         def randrange(self,total):
          self_total=total
          if not 0<=self.n<self_total: raise ValueError('invalid ticket')
          return self.n
        self.assertEqual(m.choose([('common',3),('rare',1)],Fixed(0)),'common')
        self.assertEqual(m.choose([('common',3),('rare',1)],Fixed(2)),'common')
        self.assertEqual(m.choose([('common',3),('rare',1)],Fixed(3)),'rare')
        with self.assertRaises(ValueError): m.choose([('bad',0)],Fixed(0))

    def test_rollback_resimulation(self):
        m = load('rollback-resimulation')
        r=m.Rollback({'x':0},lambda state,i:{'x':state['x']+i})
        r.advance(2); r.advance(3); r.advance(-1)
        self.assertEqual(r.current,{'x':4})
        self.assertEqual(r.correct(1,{'x':10}),{'x':12})
        view=r.current; view['x']=999
        self.assertEqual(r.current,{'x':12})
        self.assertEqual(r.correct(3,{'x':7}),{'x':7})
        with self.assertRaises(ValueError): r.correct(9,{'x':0})

    def test_server_input_validation(self):
        m = load('server-input-validation')
        p=m.Player(6,.5)
        self.assertTrue(p.apply({'sequence':0,'dx':1,'dy':0}))
        self.assertEqual((p.x,p.y),(3,0))
        self.assertFalse(p.apply({'sequence':0,'dx':1,'dy':0}))
        self.assertFalse(p.apply({'sequence':1,'dx':2,'dy':0}))
        self.assertFalse(p.apply({'sequence':1,'dx':float('nan'),'dy':0}))
        self.assertFalse(p.apply({'sequence':1,'dx':10**999,'dy':0}))
        self.assertFalse(p.apply({'sequence':1,'dx':0,'dy':0,'dt':100}))
        self.assertEqual(p.sequence,0)

    def test_animation_timeline(self):
        m = load('animation-timeline')
        a=m.Animation(['idle1','idle2'],[.25,.75])
        self.assertEqual(a.sample(0),'idle1')
        self.assertEqual(a.sample(.25),'idle2')
        self.assertEqual(a.sample(1),'idle1')
        self.assertEqual(a.sample(2,False),'idle2')
        with self.assertRaises(ValueError): a.sample(-1)

    def test_building_placement(self):
        m = load('building-placement')
        occupied={(0,0)}; shape={(0,0),(1,0)}
        self.assertEqual(m.place(occupied,shape,(2,1),4,4,1),{(0,0),(2,1),(2,2)})
        self.assertIsNone(m.place(occupied,shape,(0,0),4,4))
        self.assertIsNone(m.place(occupied,shape,(3,3),4,4))
        self.assertEqual(occupied,{(0,0)})
        with self.assertRaises(ValueError): m.place(occupied,[],(0,0),4,4)

    def test_grid_movement(self):
        m = load('grid-movement')
        player = m.GridMover([[0,0,1]], step_seconds=0)
        self.assertFalse(player.update(0,'right')['blocked'])
        self.assertEqual(player.tile,(1,0))
        player.update(0,None)
        self.assertTrue(player.update(0,'right')['blocked'])
        self.assertEqual(player.tile,(1,0))

if __name__ == "__main__":
    unittest.main(verbosity=2)
