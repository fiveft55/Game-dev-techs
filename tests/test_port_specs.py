"""Audit generated code, documented contracts, and reference behavior.

Native execution is separately performed by tools/test_ports.py; these tests do
not substitute for compiling and running the eight target languages.
"""
from copy import deepcopy
import importlib.util
import json
import math
from pathlib import Path
import random
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/ports'))
from specs import SPECS
from generate import LANGUAGES, render, render_header
from document import render_contract, render_fixtures
from explanations import EXPLANATIONS


def reference(slug):
    spec=importlib.util.spec_from_file_location(slug,ROOT/'mechanics'/slug/'python/example.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def kernel(slug):
    def index(a,i):
        if i!=int(i) or not 0<=i<len(a): raise IndexError(i)
        return int(i)
    helpers=dict(
        get=lambda a,i:a[index(a,i)],
        put=lambda a,i,v:a.__setitem__(index(a,i),v),
        push=lambda a,v:a.append(v),pop_value=lambda a:a.pop(),length=len,
        minimum=min,maximum=max,floor_num=math.floor,sqrt_num=math.sqrt,
        abs_num=abs,exp_num=math.exp,sin_num=math.sin,cos_num=math.cos,
        tan_num=math.tan,mod_num=math.fmod,
        range=lambda *values:range(*(int(v) for v in values)))
    body='def compute(data):\n'+''.join('    '+line+'\n' for line in SPECS[slug]['body'].splitlines())
    exec(compile(body,f'<trusted port specification: {slug}>','exec'),helpers)
    return helpers['compute']


class PortSpecificationTests(unittest.TestCase):
    def assertVectorClose(self, actual, expected):
        self.assertEqual(len(actual),len(expected))
        for a,b in zip(actual,expected):
            self.assertTrue(math.isfinite(a))
            self.assertTrue(math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-9),(a,b))

    def test_every_mechanic_has_all_eight_ports_and_beginner_notes(self):
        catalog=json.loads((ROOT/'catalog.json').read_text())
        self.assertEqual(set(SPECS),{entry['id'] for entry in catalog})
        self.assertEqual(set(SPECS),set(EXPLANATIONS))
        for entry in catalog:
            slug=entry['id']
            self.assertIn('## Plain-English explanation',(ROOT/'mechanics'/slug/'README.md').read_text())
            for language,filename in LANGUAGES.items():
                with self.subTest(slug=slug,language=language):
                    path=f'mechanics/{slug}/{language}/{filename}'
                    self.assertEqual(entry['implementations'][language],path)
                    self.assertTrue((ROOT/path).is_file())
                    comment_text=' '.join(line.lstrip('/#- ') for line in (ROOT/path).read_text().splitlines())
                    self.assertIn(EXPLANATIONS[slug][0].split('.')[0],comment_text)

    def test_generated_native_files_and_headers_are_current(self):
        for slug,spec in SPECS.items():
            for language,filename in LANGUAGES.items():
                self.assertEqual((ROOT/'mechanics'/slug/language/filename).read_text(),render(slug,spec,language))
            self.assertEqual((ROOT/'mechanics'/slug/'c/mechanic.h').read_text(),render_header(slug))

    def test_shared_fixtures_and_contracts_are_current(self):
        self.assertEqual((ROOT/'tests/port-fixtures.json').read_text(),render_fixtures())
        for slug,spec in SPECS.items():
            self.assertEqual((ROOT/'mechanics'/slug/'PORTS.md').read_text(),render_contract(slug,spec))

    def test_all_hand_authored_fixtures_and_input_ownership(self):
        for slug,spec in SPECS.items():
            compute=kernel(slug)
            self.assertGreaterEqual(len(spec['cases']),2)
            for data,expected in spec['cases']:
                with self.subTest(slug=slug,input=data):
                    original=deepcopy(data)
                    self.assertVectorClose(compute(data),expected)
                    self.assertEqual(data,original)

    def test_math_kernels_against_existing_python_references(self):
        rng=random.Random(2026)
        move=reference('player-movement').move
        bounce=reference('ball-reflection').bounce
        sweep=reference('projectile-sweep').hit_fraction
        integrate=reference('rigid-body-integration').integrate
        move_port=kernel('player-movement'); bounce_port=kernel('ball-reflection')
        sweep_port=kernel('projectile-sweep'); integration_port=kernel('rigid-body-integration')
        for _ in range(80):
            x,y,ix,iy=[rng.uniform(-5,5) for _ in range(4)]
            speed,dt=rng.uniform(0,10),rng.uniform(0,.2)
            self.assertVectorClose(move_port([x,y,ix,iy,speed,dt]),move(x,y,ix,iy,speed,dt))
            normal=(rng.uniform(.1,1),rng.uniform(.1,1)); e=rng.random()
            self.assertVectorClose(bounce_port([ix,iy,*normal,e]),bounce((ix,iy),normal,e))
            rect=(x,y,abs(ix),abs(iy))
            end=(rng.uniform(-5,5),rng.uniform(-5,5))
            fraction=sweep((ix,iy),end,rect)
            self.assertVectorClose(sweep_port([ix,iy,*end,*rect]),[] if fraction is None else [fraction])
            position,velocity=integrate((x,y),(ix,iy),(0,-9.8),dt)
            self.assertVectorClose(integration_port([x,y,ix,iy,0,-9.8,dt]),[*position,*velocity])

    def test_grid_and_mesh_kernels_against_existing_python_references(self):
        rng=random.Random(17)
        path=reference('grid-pathfinding').path
        sight=reference('line-of-sight').visible
        path_port=kernel('grid-pathfinding'); sight_port=kernel('line-of-sight')
        for _ in range(30):
            grid=[[int(rng.random()<.25) for _ in range(5)] for _ in range(4)]
            grid[0][0]=grid[3][4]=0
            flat=[v for row in grid for v in row]
            expected=[y*5+x for x,y in path(grid,(0,0),(4,3))]
            self.assertEqual(path_port([5,4,0,19,*flat]),expected)
            self.assertEqual(sight_port([5,4,0,0,4,3,*flat]),[int(sight(grid,(0,0),(4,3)))])
        extrude=reference('cad-extrusion').extrude
        mesh_port=kernel('cad-extrusion')
        for profile in ([(0,0),(1,0),(0,1)],[(0,0),(2,0),(2,2),(0,2)]):
            vertices,faces=extrude(profile,3)
            expected=[len(vertices),len(faces),*[v for vertex in vertices for v in vertex],*[i for face in faces for i in face]]
            self.assertEqual(mesh_port([3,*[v for point in profile for v in point]]),expected)

    def test_seeded_mazes_have_connected_passages_and_closed_borders(self):
        maze=kernel('procedural-maze')
        for size in (5,7,9):
            for seed in (0,1,42):
                flat=maze([size,size,seed])
                self.assertEqual(flat,maze([size,size,seed]))
                self.assertEqual(len(flat),size*size)
                self.assertEqual(flat.count(0),2*((size-1)//2)**2-1)
                for cell,value in enumerate(flat):
                    if cell//size in (0,size-1) or cell%size in (0,size-1): self.assertEqual(value,1)
                seen={size+1}; waiting=[size+1]
                while waiting:
                    cell=waiting.pop()
                    for neighbor in (cell-1,cell+1,cell-size,cell+size):
                        if 0<=neighbor<len(flat) and flat[neighbor]==0 and neighbor not in seen:
                            seen.add(neighbor); waiting.append(neighbor)
                self.assertEqual(len(seen),flat.count(0))


if __name__=='__main__': unittest.main(verbosity=2)
