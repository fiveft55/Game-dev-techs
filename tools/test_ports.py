"""Compile/run the common native-port fixtures. Missing tools fail unless --allow-missing.

Examples:
  python3 tools/test_ports.py --languages javascript,c
  python3 tools/test_ports.py --languages all
Use --mechanic <id> to run one mechanic in the selected languages.
"""
import argparse
import concurrent.futures
import ctypes.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/ports'))
from generate import LANGUAGES, class_name
from specs import SPECS

BUILD=ROOT/'.build/ports'
TOOLS=Path(os.environ.get('GAME_DEV_TOOLS','/workspace/.game-dev-tools'))


def find(name, fallback=None):
    return shutil.which(name) or (str(fallback) if fallback and fallback.exists() else None)


def run(command, cwd=ROOT, env=None, timeout=120):
    result=subprocess.run([str(c) for c in command], cwd=cwd, env=env, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    if result.returncode:
        raise RuntimeError('Command failed: '+ ' '.join(map(str,command))+'\n'+result.stdout[-10000:])
    return result.stdout


def write(path, content):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content)
    return path


def nums(values): return ','.join(repr(float(v)) for v in values)


def cases(specs):
    return [(slug,i,data,expected) for slug,spec in specs.items()
            for i,(data,expected) in enumerate(spec['cases'])]


def test_javascript(specs, typescript=False):
    node=find('node')
    if not node: return None
    base=ROOT/'mechanics'
    filename='javascript/mechanic.js'
    if typescript:
        compiler=find('tsc',TOOLS/'node_modules/.bin/tsc')
        if not compiler: return None
        sources=[ROOT/'mechanics'/slug/'typescript/mechanic.ts' for slug in specs]
        base=BUILD/'typescript'
        run([compiler,'--strict','--target','ES2020','--module','commonjs','--rootDir',ROOT/'mechanics','--outDir',base,*sources])
        filename='typescript/mechanic.js'
    checks=[]
    for slug,index,data,expected in cases(specs):
        checks.append('check('+json.dumps(str(base/slug/filename))+','+json.dumps(data)+','+json.dumps(expected)+','+json.dumps(f'{slug} #{index}')+');')
    runner=write(BUILD/('test_ts.js' if typescript else 'test_js.js'),'''
const assert=require('node:assert/strict');
function check(path,input,expected,label) {
  const original=input.slice();
  const actual=require(path).compute(input);
  assert.equal(actual.length,expected.length,label+' length');
  actual.forEach((value,i)=>assert.ok(Number.isFinite(value) && Math.abs(value-expected[i])<=1e-8*Math.max(1,Math.abs(expected[i])),label+' value '+i));
  assert.deepEqual(input,original,label+' mutated input');
}
'''+ '\n'.join(checks)+f'\nconsole.log("{len(checks)} fixtures passed");\n')
    return run([node,runner])


def test_c(specs):
    compiler=find('cc')
    if not compiler: return None
    def compile_one(item):
        slug,spec=item
        lines=['#include "'+str(ROOT/'mechanics'/slug/'c/mechanic.c')+'"', '#include <stdio.h>', 'int main(void) {']
        for index,(data,expected) in enumerate(spec['cases']):
            lines.append('{ PortVector input={.values={'+nums(data)+'}, .count='+str(len(data))+'};')
            lines.append('PortVector actual=game_'+slug.replace('-','_')+'_compute(input);')
            lines.append('double expected[]={'+(nums(expected) or '0')+'};')
            lines.append(f'if(actual.count!={len(expected)}) {{ fprintf(stderr,"{slug} #{index} length\\n"); return 1; }}')
            lines.append(f'for(size_t i=0;i<actual.count;i++) if(!isfinite(actual.values[i]) || fabs(actual.values[i]-expected[i])>1e-8*fmax(1,fabs(expected[i]))) {{ fprintf(stderr,"{slug} #{index} value %zu\\n",i); return 1; }} }}')
        lines+=['return 0;','}']
        path=write(BUILD/'c'/f'{slug}.c','\n'.join(lines)+'\n')
        binary=path.with_suffix('')
        # UBSan and bounds assertions stay enabled for every C test build.
        run([compiler,'-std=c11','-O1','-g','-Wall','-Wextra','-Werror','-fsanitize=undefined','-fno-sanitize-recover=all',path,'-lm','-o',binary])
        run([binary])
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(compile_one,specs.items()))
    # Link all selected modules together, using their public headers and unique symbols.
    link_lines=['#include <math.h>']
    for slug in specs:
        link_lines.append('#include "'+str(ROOT/'mechanics'/slug/'c/mechanic.h')+'"')
    link_lines.append('int main(void) {')
    for slug,spec in specs.items():
        data,expected=spec['cases'][0]
        link_lines.append('{ PortVector input={.values={'+nums(data)+'}, .count='+str(len(data))+'};')
        link_lines.append('PortVector output=game_'+slug.replace('-','_')+'_compute(input);')
        link_lines.append('if(output.count!='+str(len(expected))+') return 1; }')
    link_lines += ['return 0;','}']
    link_main=write(BUILD/'c/link-all.c','\n'.join(link_lines)+'\n')
    linked=BUILD/'c/link-all'
    run([compiler,'-std=c11','-O1','-Wall','-Wextra','-Werror','-fsanitize=undefined','-fno-sanitize-recover=all',
         link_main,*[ROOT/'mechanics'/slug/'c/mechanic.c' for slug in specs],'-lm','-o',linked])
    run([linked])
    return f'{len(cases(specs))} fixtures passed; public headers and all selected modules linked together; UBSan enabled\n'


def test_lua(specs):
    cli=find('lua') or find('lua5.4')
    if not cli and not ctypes.util.find_library('lua5.4'): return None
    lines=['''local function check(path,input,expected,label)
    local module=assert(loadfile(path))()
    local original={}
    for i,v in ipairs(input) do original[i]=v end
    local actual=module.compute(input)
    assert(#actual==#expected,label.." length")
    for i,v in ipairs(actual) do
        assert(v==v and math.abs(v-expected[i])<=1e-8*math.max(1,math.abs(expected[i])),label.." value "..i)
    end
    for i,v in ipairs(input) do assert(v==original[i],label.." mutated input") end
end''']
    for slug,index,data,expected in cases(specs):
        path=json.dumps(str(ROOT/'mechanics'/slug/'lua/mechanic.lua'))
        lines.append('check('+path+',{'+nums(data)+'},{'+nums(expected)+'},'+json.dumps(f'{slug} #{index}')+')')
    lines.append(f'print("{len(cases(specs))} fixtures passed")')
    runner=write(BUILD/'test.lua','\n'.join(lines)+'\n')
    return run([cli,runner] if cli else [sys.executable,ROOT/'tools/run_lua.py',runner])


def test_csharp(specs):
    dotnet=find('dotnet',TOOLS/'dotnet/dotnet')
    if not dotnet: return None
    folder=BUILD/'csharp'
    includes='\n'.join('<Compile Include="'+str(ROOT/'mechanics'/slug/'csharp/Mechanic.cs')+'" />' for slug in specs)
    write(folder/'Ports.csproj','<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><OutputType>Exe</OutputType><TargetFramework>net8.0</TargetFramework><EnableDefaultCompileItems>false</EnableDefaultCompileItems></PropertyGroup><ItemGroup><Compile Include="Program.cs"/>'+includes+'</ItemGroup></Project>\n')
    # No packages: avoid implicit contacting of NuGet feeds on new machines.
    write(folder/'NuGet.Config','<configuration><packageSources><clear/></packageSources></configuration>\n')
    lines=['using System;','using System.Collections.Generic;','class PortTests {', '''static void Check(List<double> actual,double[] expected,string label) {
    if(actual.Count!=expected.Length) throw new Exception(label+" length");
    for(int i=0;i<actual.Count;i++) if(!double.IsFinite(actual[i]) || Math.Abs(actual[i]-expected[i])>1e-8*Math.Max(1,Math.Abs(expected[i]))) throw new Exception(label+" value "+i);
}''','static void Main() {']
    for slug,index,data,expected in cases(specs):
        lines.append('Check('+class_name(slug)+'.Compute(new List<double>{'+nums(data)+'}),new double[]{'+nums(expected)+'},'+json.dumps(f'{slug} #{index}')+');')
    lines += [f'Console.WriteLine("{len(cases(specs))} fixtures passed");','}','}']
    write(folder/'Program.cs','\n'.join(lines)+'\n')
    (BUILD/'tmp').mkdir(parents=True,exist_ok=True)
    env=dict(os.environ, TMPDIR=str(BUILD/'tmp'), DOTNET_CLI_HOME=str(BUILD/'dotnet-home'),DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1',DOTNET_CLI_TELEMETRY_OPTOUT='1',NUGET_PACKAGES=str(BUILD/'nuget'))
    # Invoke the SDK compiler directly: no NuGet restore or first-run migration mutex.
    # This is the same Roslyn compiler used by dotnet build, with installed net8 refs.
    sdk_root=Path(dotnet).resolve().parent
    compilers=sorted(sdk_root.glob('sdk/*/Roslyn/bincore/csc.dll'))
    references=sorted(sdk_root.glob('packs/Microsoft.NETCore.App.Ref/*/ref/net8.0'))
    if not compilers or not references:
        return run([dotnet,'run','--project',folder/'Ports.csproj','--configuration','Release'],env=env)
    assembly=folder/'PortTests.dll'
    source_files=[ROOT/'mechanics'/slug/'csharp/Mechanic.cs' for slug in specs]
    run([dotnet,compilers[-1],'-nologo','-target:exe','-out:'+str(assembly),
         *['-r:'+str(p) for p in references[-1].glob('*.dll')],folder/'Program.cs',*source_files],env=env)
    write(folder/'PortTests.runtimeconfig.json',json.dumps({'runtimeOptions':{
        'tfm':'net8.0','framework':{'name':'Microsoft.NETCore.App','version':'8.0.0'}}}))
    return run([dotnet,assembly],env=env)


def test_gdscript(specs):
    godot=find('godot') or find('godot4')
    if not godot: return None
    lines=['extends SceneTree', '', '''func check_case(path: String, data: Array, expected: Array, label: String) -> bool:
    var script = load(path)
    if script == null or not script.can_instantiate():
        push_error(label + " script load failed")
        return false
    var actual = script.compute(data)
    if not actual is Array or actual.size() != expected.size():
        push_error(label + " length or return type")
        return false
    for i in range(actual.size()):
        if not is_finite(float(actual[i])) or absf(float(actual[i])-float(expected[i])) > 1e-8*maxf(1.0,absf(float(expected[i]))):
            push_error(label + " value " + str(i))
            return false
    return true
''','func _initialize() -> void:']
    for slug,index,data,expected in cases(specs):
        path=f'res://mechanics/{slug}/gdscript/mechanic.gd'
        lines.append('    if not check_case('+json.dumps(path)+','+json.dumps(data)+','+json.dumps(expected)+','+json.dumps(f'{slug} #{index}')+'):')
        lines+=['        quit(1)','        return']
    lines += [f'    print("{len(cases(specs))} fixtures passed")','    quit(0)']
    runner=write(BUILD/'test.gd','\n'.join(lines)+'\n')
    env=dict(os.environ,XDG_CACHE_HOME=str(BUILD/'cache'),XDG_DATA_HOME=str(BUILD/'data'),XDG_CONFIG_HOME=str(BUILD/'config'))
    return run([godot,'--headless','--path',ROOT,'--script',runner],env=env,timeout=90)


def test_rust(specs):
    rustc=find('rustc',TOOLS/'cargo/bin/rustc')
    if not rustc: return None
    env=dict(os.environ,RUSTUP_HOME=str(TOOLS/'rustup'),CARGO_HOME=str(TOOLS/'cargo')) if str(TOOLS) in rustc else None
    lines=['fn check(actual: Vec<f64>, expected: &[f64], label: &str) {',
           'assert_eq!(actual.len(),expected.len(),"{} length",label);',
           'for (a,b) in actual.iter().zip(expected) { assert!(a.is_finite() && (a-b).abs()<=1e-8*b.abs().max(1.0),"{} value {} != {}",label,a,b); }','}']
    for slug in specs:
        lines.append('#[path = '+json.dumps(str(ROOT/'mechanics'/slug/'rust/mechanic.rs'))+'] mod '+slug.replace('-','_')+';')
    lines.append('fn main() {')
    for slug,index,data,expected in cases(specs):
        lines.append('check('+slug.replace('-','_')+'::compute(&['+nums(data)+']),&['+nums(expected)+'],'+json.dumps(f'{slug} #{index}')+');')
    lines += [f'println!("{len(cases(specs))} fixtures passed");','}']
    runner=write(BUILD/'test.rs','\n'.join(lines)+'\n')
    binary=BUILD/'test-rust'
    run([rustc,'--edition','2021',runner,'-o',binary],env=env)
    return run([binary])


def test_go(specs):
    go=find('go',TOOLS/'go/bin/go')
    if (TOOLS/'go/bin/go').exists(): go=str(TOOLS/'go/bin/go')
    if not go: return None
    folder=BUILD/'go'
    # Rebuild this isolated module so --mechanic cannot accidentally run stale packages.
    if folder.exists(): shutil.rmtree(folder)
    write(folder/'go.mod','module gameports\n\ngo 1.20\n')
    for slug,spec in specs.items():
        target=folder/slug
        write(target/'mechanic.go',(ROOT/'mechanics'/slug/'go/mechanic.go').read_text())
        lines=['package mechanic','import ("testing"; "math")','func TestFixtures(t *testing.T) {']
        for index,(data,expected) in enumerate(spec['cases']):
            lines+=['{ actual:=Compute([]float64{'+nums(data)+'}); expected:=[]float64{'+nums(expected)+'}',
                    f'if len(actual)!=len(expected) {{ t.Fatal("fixture {index} length") }}',
                    f'for i,v:=range actual {{ if math.IsNaN(v) || math.IsInf(v,0) || math.Abs(v-expected[i])>1e-8*math.Max(1,math.Abs(expected[i])) {{ t.Fatalf("fixture {index} value %d: %v != %v",i,v,expected[i]) }} }}','}']
        lines.append('}')
        write(target/'mechanic_test.go','\n'.join(lines)+'\n')
    env=dict(os.environ,GOCACHE=str(BUILD/'go-cache'),GOMODCACHE=str(BUILD/'go-mod-cache'),GOTOOLCHAIN='local',GOPROXY='off')
    output=run([go,'test','-count=1','-p','4','./...'],cwd=folder,env=env)
    return output+f'{len(cases(specs))} fixtures passed\n'


RUNNERS={'javascript':lambda s:test_javascript(s), 'typescript':lambda s:test_javascript(s,True),
         'c':test_c,'lua':test_lua,'csharp':test_csharp,'gdscript':test_gdscript,'rust':test_rust,'go':test_go}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--languages',default='all')
    parser.add_argument('--mechanic',choices=sorted(SPECS))
    parser.add_argument('--allow-missing',action='store_true')
    args=parser.parse_args()
    languages=list(RUNNERS) if args.languages=='all' else args.languages.split(',')
    if not set(languages)<=set(RUNNERS): parser.error('unknown language')
    specs={args.mechanic:SPECS[args.mechanic]} if args.mechanic else SPECS
    BUILD.mkdir(parents=True,exist_ok=True)
    results=[]
    for lang in languages:
        print('Testing '+lang+' ...',flush=True)
        start=time.monotonic()
        try:
            output=RUNNERS[lang](specs)
            status='passed' if output is not None else 'missing-tool'
            if output: print(output.strip(),flush=True)
            result={'language':lang,'status':status,'mechanics':len(specs),'fixtures':len(cases(specs)) if output is not None else 0}
        except (RuntimeError,subprocess.TimeoutExpired) as error:
            print(str(error),flush=True)
            result={'language':lang,'status':'failed','error':str(error),'mechanics':len(specs),'fixtures':0}
        result['seconds']=round(time.monotonic()-start,2)
        results.append(result)
    report=BUILD/('results-'+('-'.join(languages))+'.json')
    report.write_text(json.dumps(results,indent=2)+'\n')
    print('Report: '+str(report.relative_to(ROOT)))
    bad=any(r['status']=='failed' or (r['status']=='missing-tool' and not args.allow_missing) for r in results)
    return 1 if bad else 0


if __name__=='__main__': sys.exit(main())
