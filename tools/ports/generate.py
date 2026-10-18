"""Generate independent native ports from a small, auditable imperative subset.

Run from any directory. The generated files contain real algorithms and helpers;
Python and this generator are not needed when using the ports in your game.
"""
import ast
import json
from pathlib import Path
import textwrap
from specs import SPECS
from explanations import EXPLANATIONS, HELPERS

ROOT = Path(__file__).resolve().parents[2]
LANGUAGES = {'c':'mechanic.c','csharp':'Mechanic.cs','lua':'mechanic.lua',
             'gdscript':'mechanic.gd','typescript':'mechanic.ts',
             'javascript':'mechanic.js','rust':'mechanic.rs','go':'mechanic.go'}
MATH = ['minimum','maximum','floor_num','sqrt_num','abs_num','exp_num','sin_num','cos_num','tan_num','mod_num']


class Compiler:
    def __init__(self, lang, spec):
        self.lang=lang
        self.source='def compute(data):\n'+textwrap.indent(spec['body'],'    ')
        self.tree=ast.parse(self.source).body[0]
        self.arrays={'data'}
        changed=True
        while changed:
            changed=False
            for node in ast.walk(self.tree):
                if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name):
                    value=node.value
                    array=isinstance(value,ast.List) or isinstance(value,ast.Name) and value.id in self.arrays
                    if array and node.targets[0].id not in self.arrays:
                        self.arrays.add(node.targets[0].id);changed=True
        self.locals=[]
        for node in ast.walk(self.tree):
            if isinstance(node,ast.Name) and isinstance(node.ctx,ast.Store) and node.id not in self.locals:
                self.locals.append(node.id)
        # Names are kept descriptive, while avoiding language keywords and builtins.
        self.names={name: {'out':'result','end':'end_index','event':'event_id','base':'base_index','loop':'looping'}.get(name,name) for name in self.locals+['data']}
        self.comment='--' if lang=='lua' else '#' if lang=='gdscript' else '//'

    def name(self,name): return self.names.get(name,name)

    def number(self,value):
        number=repr(float(value))
        if number.endswith('.0') and self.lang not in ('rust','csharp','go','gdscript','c'):
            return number[:-2]
        return number

    def expr(self,node):
        lang=self.lang
        if isinstance(node,ast.Name): return self.name(node.id)
        if isinstance(node,ast.Constant): return self.number(node.value)
        if isinstance(node,ast.List):
            values=', '.join(self.expr(x) for x in node.elts)
            if lang=='c': return '(PortVector){.values={'+(values or '0')+'}, .count='+str(len(node.elts))+'}'
            if lang=='csharp': return 'new List<double> {'+values+'}'
            if lang=='lua': return '{'+values+'}'
            if lang=='rust': return 'vec!['+values+']'
            if lang=='go': return '[]float64{'+values+'}'
            return '['+values+']'
        if isinstance(node,ast.BinOp):
            op={ast.Add:'+',ast.Sub:'-',ast.Mult:'*',ast.Div:'/',ast.Mod:'%'}[type(node.op)]
            return '('+self.expr(node.left)+' '+op+' '+self.expr(node.right)+')'
        if isinstance(node,ast.UnaryOp):
            return ('-' if isinstance(node.op,ast.USub) else '!')+'('+self.expr(node.operand)+')'
        if isinstance(node,ast.BoolOp):
            op=(' and ' if isinstance(node.op,ast.And) else ' or ') if lang in ('lua','gdscript') else (' && ' if isinstance(node.op,ast.And) else ' || ')
            return '('+op.join(self.expr(v) for v in node.values)+')'
        if isinstance(node,ast.Compare):
            operators={ast.Eq:'==',ast.NotEq:'~=' if lang=='lua' else '!=',ast.Lt:'<',ast.LtE:'<=',ast.Gt:'>',ast.GtE:'>='}
            parts=[]
            left=node.left
            for op,right in zip(node.ops,node.comparators):
                parts.append(self.expr(left)+' '+operators[type(op)]+' '+self.expr(right));left=right
            return '('+(' and ' if lang in ('lua','gdscript') else ' && ').join(parts)+')'
        if isinstance(node,ast.Call):
            function=node.func.id
            args=[self.expr(a) for a in node.args]
            if function in ('get','length','put','push','pop_value'):
                if lang in ('c','rust'): args[0]=('&mut ' if lang=='rust' and function in ('put','push','pop_value') else '&')+args[0]
                if lang=='go' and function in ('put','push','pop_value'): args[0]='&'+args[0]
            if lang=='rust' and function in ('put','push'):
                args=args[1:]+args[:1]
            return 'port_'+function+'('+', '.join(args)+')'
        raise ValueError(ast.dump(node))

    def statement(self,node,indent=1):
        lang=self.lang
        pad='    '*indent
        semicolon='' if lang in ('lua','gdscript','go') else ';'
        result=[]
        line=self.source.splitlines()[node.lineno-2].strip()
        if line.startswith('#'):
            result.append(pad+self.comment+' '+line[1:].strip())
        if isinstance(node,ast.Assign):
            target=node.targets[0].id
            value=self.expr(node.value)
            if isinstance(node.value,ast.Name) and node.value.id in self.arrays:
                if lang=='csharp': value='new List<double>('+value+')'
                if lang in ('javascript','typescript'): value=value+'.slice()'
                if lang=='lua': value='port_copy('+value+')'
                if lang=='gdscript': value=value+'.duplicate()'
                if lang=='rust': value=value+'.clone()'
                if lang=='go': value='append([]float64(nil), '+value+'...)'
            result.append(pad+self.name(target)+' = '+value+semicolon)
        elif isinstance(node,ast.AugAssign):
            op={ast.Add:'+',ast.Sub:'-',ast.Mult:'*',ast.Div:'/'}[type(node.op)]
            target=self.expr(node.target)
            if lang=='lua': result.append(pad+target+' = '+target+' '+op+' '+self.expr(node.value))
            else: result.append(pad+target+' '+op+'= '+self.expr(node.value)+semicolon)
        elif isinstance(node,ast.Expr): result.append(pad+self.expr(node.value)+semicolon)
        elif isinstance(node,ast.Return): result.append(pad+'return '+self.expr(node.value)+semicolon)
        elif isinstance(node,(ast.Break,ast.Continue)):
            if isinstance(node,ast.Continue): raise ValueError('continue is intentionally unsupported')
            result.append(pad+'break'+semicolon)
        elif isinstance(node,ast.If):
            cond=self.expr(node.test)
            start='if '+cond+' then' if lang=='lua' else 'if '+cond+':' if lang=='gdscript' else 'if '+cond+' {' if lang in ('rust','go') else 'if ('+cond+') {'
            result.append(pad+start)
            for child in node.body: result+=self.statement(child,indent+1)
            if node.orelse:
                result.append(pad+('else' if lang=='lua' else 'else:' if lang=='gdscript' else '} else {'))
                for child in node.orelse: result+=self.statement(child,indent+1)
            if lang!='gdscript': result.append(pad+('end' if lang=='lua' else '}'))
        elif isinstance(node,(ast.While,ast.For)):
            if isinstance(node,ast.For):
                values=node.iter.args
                start=self.expr(values[0]);stop=self.expr(values[1]);step=self.expr(values[2]) if len(values)>2 else self.number(1)
                counter=self.name(node.target.id)
                result.append(pad+counter+' = '+start+semicolon)
                condition='('+counter+' < '+stop+')'
            else: condition=self.expr(node.test)
            begin='while '+condition+' do' if lang=='lua' else 'while '+condition+':' if lang=='gdscript' else 'for '+condition+' {' if lang=='go' else 'while '+condition+' {' if lang=='rust' else 'while ('+condition+') {'
            result.append(pad+begin)
            for child in node.body: result+=self.statement(child,indent+1)
            if isinstance(node,ast.For):
                inc=counter+' = '+counter+' + '+step if lang=='lua' else counter+' += '+step+semicolon
                result.append(pad+'    '+inc)
            if lang!='gdscript': result.append(pad+('end' if lang=='lua' else '}'))
        else: raise ValueError(ast.dump(node))
        return result

    def function(self):
        lang=self.lang
        signature={'c':'PortVector compute(PortVector data) {','csharp':'public static List<double> Compute(List<double> data) {',
                   'javascript':'function compute(data) {','typescript':'export function compute(data: number[]): number[] {',
                   'lua':'local function compute(data)','gdscript':'static func compute(data: Array) -> Array:',
                   'rust':'pub fn compute(data: &[f64]) -> Vec<f64> {','go':'func Compute(data []float64) []float64 {'}[lang]
        out=[signature]
        for name in self.locals:
            array=name in self.arrays
            name=self.name(name)
            decl={'c':f'PortVector {name} = {{0}};' if array else f'double {name} = 0;',
                  'csharp':f'List<double> {name} = new List<double>();' if array else f'double {name} = 0;',
                  'javascript':f'let {name} = [];' if array else f'let {name} = 0;',
                  'typescript':f'let {name}: number[] = [];' if array else f'let {name}: number = 0;',
                  'lua':f'local {name} = {{}}' if array else f'local {name} = 0',
                  'gdscript':f'var {name}: Array = []' if array else f'var {name}: float = 0.0',
                  'rust':f'let mut {name}: Vec<f64> = Vec::new();' if array else f'let mut {name}: f64 = 0.0;',
                  'go':f'var {name} []float64' if array else f'var {name} float64'}[lang]
            out.append('    '+decl)
        for node in self.tree.body: out+=self.statement(node)
        if lang=='lua': out+=['end','return {compute=compute}']
        elif lang!='gdscript': out+=['}']
        if lang=='javascript': out+=['if (typeof module !== "undefined") module.exports = {compute};']
        return '\n'.join(out)


def helpers(lang):
    if lang=='c':
        return '''#include <assert.h>
#include <math.h>
#include <stddef.h>
// Fixed capacity keeps ownership simple. Assert on overflow; never truncate silently.
#ifndef PORT_CAPACITY
#define PORT_CAPACITY 4096
#endif
typedef struct { double values[PORT_CAPACITY]; size_t count; } PortVector;
static inline double port_length(const PortVector *a) { return (double)a->count; }
static inline size_t port_index(const PortVector *a, double i) { assert(isfinite(i) && i>=0 && i<(double)a->count && floor(i)==i); return (size_t)i; }
static inline double port_get(const PortVector *a, double i) { return a->values[port_index(a,i)]; }
static inline void port_put(PortVector *a, double i, double v) { a->values[port_index(a,i)] = v; }
static inline void port_push(PortVector *a, double v) { assert(a->count<PORT_CAPACITY); a->values[a->count++]=v; }
static inline double port_pop_value(PortVector *a) { assert(a->count>0); return a->values[--a->count]; }
static inline double port_minimum(double a,double b) { return fmin(a,b); }
static inline double port_maximum(double a,double b) { return fmax(a,b); }
static inline double port_floor_num(double a) { return floor(a); }
static inline double port_sqrt_num(double a) { return sqrt(a); }
static inline double port_abs_num(double a) { return fabs(a); }
static inline double port_exp_num(double a) { return exp(a); }
static inline double port_sin_num(double a) { return sin(a); }
static inline double port_cos_num(double a) { return cos(a); }
static inline double port_tan_num(double a) { return tan(a); }
static inline double port_mod_num(double a,double b) { return fmod(a,b); }'''
    if lang in ('javascript','typescript'):
        ts=lang=='typescript'
        result=[]
        def fn(name,args,body,result_type):
            params=', '.join(n+(': '+t if ts else '') for n,t in args)
            result.append('function port_'+name+'('+params+')'+(': '+result_type if ts else '')+' { '+body+' }')
        fn('length',[('a','number[]')],'return a.length;','number')
        fn('get',[('a','number[]'),('i','number')],'if (!Number.isInteger(i) || i < 0 || i >= a.length) throw new RangeError("index"); return a[i];','number')
        fn('put',[('a','number[]'),('i','number'),('v','number')],'port_get(a,i); a[i]=v;','void')
        fn('push',[('a','number[]'),('v','number')],'a.push(v);','void')
        fn('pop_value',[('a','number[]')],'if (a.length===0) throw new RangeError("empty"); return a.pop()'+('!' if ts else '')+';','number')
        for name,native in [('minimum','min'),('maximum','max'),('floor_num','floor'),('sqrt_num','sqrt'),('abs_num','abs'),('exp_num','exp'),('sin_num','sin'),('cos_num','cos'),('tan_num','tan'),('mod_num','')]:
            binary=name in ('minimum','maximum','mod_num')
            args=[('a','number')]+([('b','number')] if binary else [])
            fn(name,args,'return '+('a % b' if name=='mod_num' else 'Math.'+native+'(a'+(',b' if binary else '')+')')+';','number')
        return '\n'.join(result)
    if lang=='lua':
        return '''local function port_length(a) return #a end
local function port_get(a,i) assert(i>=0 and i==math.floor(i) and i<#a,"index"); return a[i+1] end
local function port_put(a,i,v) port_get(a,i); a[i+1]=v end
local function port_push(a,v) a[#a+1]=v end
local function port_pop_value(a) assert(#a>0,"empty"); return table.remove(a) end
local function port_copy(a) local b={} for i,v in ipairs(a) do b[i]=v end return b end
local function port_minimum(a,b) return math.min(a,b) end
local function port_maximum(a,b) return math.max(a,b) end
local function port_floor_num(a) return math.floor(a) end
local function port_sqrt_num(a) return math.sqrt(a) end
local function port_abs_num(a) return math.abs(a) end
local function port_exp_num(a) return math.exp(a) end
local function port_sin_num(a) return math.sin(a) end
local function port_cos_num(a) return math.cos(a) end
local function port_tan_num(a) return math.tan(a) end
local function port_mod_num(a,b) return math.fmod(a,b) end'''
    if lang=='csharp':
        return '''using System;
using System.Collections.Generic;
'''+'''private static double port_length(List<double> a) { return a.Count; }
private static double port_get(List<double> a,double i) { if(i<0 || i>=a.Count || Math.Floor(i)!=i) throw new ArgumentOutOfRangeException("i"); return a[(int)i]; }
private static void port_put(List<double> a,double i,double v) { port_get(a,i); a[(int)i]=v; }
private static void port_push(List<double> a,double v) { a.Add(v); }
private static double port_pop_value(List<double> a) { double v=a[a.Count-1]; a.RemoveAt(a.Count-1); return v; }
private static double port_minimum(double a,double b) { return Math.Min(a,b); }
private static double port_maximum(double a,double b) { return Math.Max(a,b); }
private static double port_floor_num(double a) { return Math.Floor(a); }
private static double port_sqrt_num(double a) { return Math.Sqrt(a); }
private static double port_abs_num(double a) { return Math.Abs(a); }
private static double port_exp_num(double a) { return Math.Exp(a); }
private static double port_sin_num(double a) { return Math.Sin(a); }
private static double port_cos_num(double a) { return Math.Cos(a); }
private static double port_tan_num(double a) { return Math.Tan(a); }
private static double port_mod_num(double a,double b) { return a % b; }'''
    if lang=='gdscript':
        return '''extends RefCounted

static func port_length(a: Array) -> float:
    return float(a.size())
static func port_get(a: Array, i: float) -> float:
    assert(i >= 0 and i < a.size() and floor(i) == i, "index")
    return float(a[int(i)])
static func port_put(a: Array, i: float, v: float) -> void:
    port_get(a, i)
    a[int(i)] = v
static func port_push(a: Array, v: float) -> void:
    a.append(v)
static func port_pop_value(a: Array) -> float:
    assert(not a.is_empty(), "empty")
    return float(a.pop_back())
static func port_minimum(a: float, b: float) -> float:
    return minf(a,b)
static func port_maximum(a: float, b: float) -> float:
    return maxf(a,b)
static func port_floor_num(a: float) -> float:
    return floor(a)
static func port_sqrt_num(a: float) -> float:
    return sqrt(a)
static func port_abs_num(a: float) -> float:
    return absf(a)
static func port_exp_num(a: float) -> float:
    return exp(a)
static func port_sin_num(a: float) -> float:
    return sin(a)
static func port_cos_num(a: float) -> float:
    return cos(a)
static func port_tan_num(a: float) -> float:
    return tan(a)
static func port_mod_num(a: float, b: float) -> float:
    return fmod(a,b)'''
    if lang=='rust':
        return '''#![allow(unused_assignments, unused_mut, dead_code, unused_parens)]
fn port_length(a: &[f64]) -> f64 { a.len() as f64 }
fn port_get(a: &[f64], i:f64) -> f64 { assert!(i.is_finite() && i>=0.0 && i.fract()==0.0 && i<(a.len() as f64)); a[i as usize] }
fn port_put(i:f64, v:f64, a: &mut Vec<f64>) { port_get(a,i); a[i as usize]=v; }
fn port_push(v:f64, a: &mut Vec<f64>) { a.push(v); }
fn port_pop_value(a: &mut Vec<f64>) -> f64 { a.pop().expect("empty") }
fn port_minimum(a:f64,b:f64)->f64 { a.min(b) }
fn port_maximum(a:f64,b:f64)->f64 { a.max(b) }
fn port_floor_num(a:f64)->f64 { a.floor() }
fn port_sqrt_num(a:f64)->f64 { a.sqrt() }
fn port_abs_num(a:f64)->f64 { a.abs() }
fn port_exp_num(a:f64)->f64 { a.exp() }
fn port_sin_num(a:f64)->f64 { a.sin() }
fn port_cos_num(a:f64)->f64 { a.cos() }
fn port_tan_num(a:f64)->f64 { a.tan() }
fn port_mod_num(a:f64,b:f64)->f64 { a % b }'''
    if lang=='go':
        return '''package mechanic

import "math"

func port_length(a []float64) float64 { return float64(len(a)) }
func port_get(a []float64, i float64) float64 { if math.IsNaN(i) || i<0 || math.Floor(i)!=i || i>=float64(len(a)) { panic("index") }; return a[int(i)] }
func port_put(a *[]float64, i float64, v float64) { port_get(*a,i); (*a)[int(i)]=v }
func port_push(a *[]float64,v float64) { *a=append(*a,v) }
func port_pop_value(a *[]float64) float64 { v:=(*a)[len(*a)-1]; *a=(*a)[:len(*a)-1]; return v }
func port_minimum(a,b float64) float64 { return math.Min(a,b) }
func port_maximum(a,b float64) float64 { return math.Max(a,b) }
func port_floor_num(a float64) float64 { return math.Floor(a) }
func port_sqrt_num(a float64) float64 { return math.Sqrt(a) }
func port_abs_num(a float64) float64 { return math.Abs(a) }
func port_exp_num(a float64) float64 { return math.Exp(a) }
func port_sin_num(a float64) float64 { return math.Sin(a) }
func port_cos_num(a float64) float64 { return math.Cos(a) }
func port_tan_num(a float64) float64 { return math.Tan(a) }
func port_mod_num(a,b float64) float64 { return math.Mod(a,b) }'''
    raise ValueError(lang)


def class_name(slug): return 'Mechanic'+''.join(part.title() for part in slug.split('-'))


def render(slug,spec,lang):
    c=Compiler(lang,spec)
    plain,steps=EXPLANATIONS[slug]
    header=[plain, f'{slug}: original MIT-licensed native educational port.',
            'Generated by tools/ports/generate.py; edit the specification to preserve parity.',
            'Input: '+spec['inputs'], 'Output: '+spec['outputs'],spec['notes'],
            'Precondition: finite, correctly shaped data; integer indices/counts/IDs.',
            'See ../PORTS.md for examples, limits, and the shared test fixtures.']
    comments='\n'.join(c.comment+' '+line for paragraph in header for line in textwrap.wrap(paragraph,96))
    support=helpers(lang)
    if lang=='c':
        support='#include \"mechanic.h\"\n#include <assert.h>\n#include <math.h>\n'+support[support.index('static inline double port_length'):]
    used={'port_'+node.func.id for node in ast.walk(c.tree)
          if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id!='range'}
    if 'port_put' in used: used.add('port_get')
    if 'port_get' in used and lang=='c': used.add('port_index')
    if any(isinstance(node,ast.Assign) and isinstance(node.value,ast.Name) and node.value.id in c.arrays
           for node in ast.walk(c.tree)):
        used.add('port_copy')
    if lang=='gdscript':
        sections=support.split('\nstatic func ')
        support=sections[0]+''.join('\nstatic func '+section for section in sections[1:]
                                  if 'port_'+section.split('port_',1)[1].split('(',1)[0] in used)
    else:
        import re
        support='\n'.join(line for line in support.splitlines()
                          if not re.search(r'\bport_\w+\(',line)
                          or re.search(r'\b(port_\w+)\(',line).group(1) in used)
    # Explain every helper before its definition, without changing its behavior.
    annotated=[]
    import re
    for line in support.splitlines():
        match=re.search(r'\bport_(\w+)\(',line)
        if match and match.group(1) in HELPERS:
            annotated.append(c.comment+' '+HELPERS[match.group(1)])
        annotated.append(line)
    support='\n'.join(annotated)
    simple='\n'.join(c.comment+' '+line for number,step in enumerate(steps,1)
                     for line in textwrap.wrap(str(number)+'. '+step,94))
    function=simple+'\n'+c.function()
    if lang=='c':
        function=function.replace('PortVector compute(', 'PortVector game_'+slug.replace('-','_')+'_compute(')
    if lang=='csharp':
        lines=support.splitlines()
        support='\n'.join(lines[:2])+'\npublic static class '+class_name(slug)+' {\n'+textwrap.indent('\n'.join(lines[2:]),'    ')
        function=textwrap.indent(function,'    ')+'\n}'
    return comments+'\n\n'+support+'\n\n'+function+'\n'


def render_header(slug):
    guard='GAME_'+slug.replace('-','_').upper()+'_H'
    return ('// Original MIT-licensed portable C interface; all linked units must use the same capacity.\n'
            '#ifndef '+guard+'\n#define '+guard+'\n#include <stddef.h>\n'
            '#ifndef PORT_CAPACITY\n#define PORT_CAPACITY 4096\n#endif\n'
            '#ifndef GAME_PORT_VECTOR_DEFINED\n#define GAME_PORT_VECTOR_DEFINED\n'
            'typedef struct { double values[PORT_CAPACITY]; size_t count; } PortVector;\n#endif\n'
            'PortVector game_'+slug.replace('-','_')+'_compute(PortVector input);\n#endif\n')


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    stale=[]
    for slug,spec in SPECS.items():
        for lang,filename in LANGUAGES.items():
            path=ROOT/'mechanics'/slug/lang/filename
            expected=render(slug,spec,lang)
            if args.check:
                if not path.exists() or path.read_text()!=expected: stale.append(str(path.relative_to(ROOT)))
            else:
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_text(expected)
    for slug in SPECS:
        path=ROOT/'mechanics'/slug/'c/mechanic.h'
        expected=render_header(slug)
        if args.check:
            if not path.exists() or path.read_text()!=expected: stale.append(str(path.relative_to(ROOT)))
        else: path.write_text(expected)
    if stale: parser.exit(1,'Stale ports: '+', '.join(stale)+'\n')
    print(('Checked' if args.check else 'Generated')+f' {len(SPECS)*len(LANGUAGES)} native ports')


if __name__=='__main__': main()
