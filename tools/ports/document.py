"""Refresh port contracts, fixtures and catalog links without changing Python APIs."""
import json
from pathlib import Path
from generate import LANGUAGES, class_name
from specs import SPECS
from explanations import EXPLANATIONS

ROOT=Path(__file__).resolve().parents[2]


def render_contract(slug,spec):
    first_input,first_output=spec['cases'][0]
    purpose,steps=EXPLANATIONS[slug]
    lines=[
        '# '+slug+': portable language versions', '',
        '## Plain-English explanation', '', purpose, '',
        *[str(i)+'. '+step for i,step in enumerate(steps,1)], '',
        '[New to code? Start with the beginner guide.](../../docs/beginner-guide.md)', '',
        'These are independent native educational kernels, not wrappers that call Python. '
        'They share one explicit numeric-array contract across eight languages. '
        'The existing Python module retains its original API; the portable API is a separate interface and may expose a smaller core operation as explained below.', '',
        '## Contract', '',
        '- Input: `'+spec['inputs']+'`',
        '- Output: `'+spec['outputs']+'`', '',
        spec['notes'], '',
        'Supply finite, correctly shaped numeric data. Integer indices/counts/IDs must be exact and within the safe binary64 range. '
        'Do not pass raw network or unvalidated save data directly. Bounds checks are present, but these kernels do not implement a comprehensive schema validator. '
        'C vectors have a default capacity of 4096 values; exceeding it triggers an assertion rather than truncation. '
        'An entire C program must use the same `PORT_CAPACITY`. See [language conventions](../../docs/language-ports.md) for numeric, state, performance and API differences.', '',
        '## Native source', '', '| Language | File | Entry point |', '|---|---|---|',
    ]
    for lang,filename in LANGUAGES.items():
        entry='Compute(data)' if lang in ('go','csharp') else 'compute(data)'
        if lang=='c': entry='game_'+slug.replace('-','_')+'_compute(input)'
        if lang=='csharp': entry=class_name(slug)+'.Compute(data)'
        lines.append(f'| {lang} | [{filename}]({lang}/{filename}) | `{entry}` |')
    lines+=['', 'C users include [mechanic.h](c/mechanic.h) and compile the matching `.c` as a separate translation unit. '
            'Namespaced entry points allow multiple mechanics to link together. Other languages isolate mechanics with modules/classes/packages.', '',
            '## Working fixture', '', 'Input:', '', '```json', json.dumps(first_input), '```', '', 'Expected output:', '', '```json', json.dumps(first_output), '```', '',
            f'All {len(spec["cases"])} hand-authored cases are in [the shared fixture data](../../tests/port-fixtures.json), keyed by `{slug}`. '
            'Each case is run against every native language by the test runner.', '',
            'From the repository root:', '', '```sh',
            f'python3 tools/test_ports.py --mechanic {slug} --languages all',
            f'python3 tools/test_ports.py --mechanic {slug} --languages javascript,c', '```', '',
            'The runner fails on a missing toolchain by default. `--allow-missing` explicitly records missing tools; it does not mark them passed. '
            'Generated build artifacts stay under `.build/`. See [toolchain setup](../../docs/toolchains.md).', '',
            '## Editing and reuse', '',
            'For your own project, copy the native source (and the C header) with the MIT license, adapt the input decoding into named engine types, '
            'then extend the behavioral tests for your rules. Batched event ports start a fresh session per call; they are not automatically persistent service objects. '
            'To update this repository consistently, edit [the specification](../../tools/ports/specs.py), run '
            '`python3 tools/ports/generate.py` and `python3 tools/ports/document.py`, then run the native checks. '
            'Generation is a maintenance aid; the generated files have no Python runtime dependency.', '',
            'All algorithms and adapters are original code under the root [MIT license](../../LICENSE). No third-party game source or assets are bundled.']
    return '\n'.join(lines)+'\n'


def render_fixtures():
    return json.dumps({slug:[{'input':data,'expected':expected} for data,expected in spec['cases']]
                       for slug,spec in SPECS.items()},indent=2)+'\n'


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    outputs={'tests/port-fixtures.json':render_fixtures()}
    for slug,spec in SPECS.items(): outputs[f'mechanics/{slug}/PORTS.md']=render_contract(slug,spec)
    stale=[]
    for path,text in outputs.items():
        target=ROOT/path
        if args.check:
            if not target.exists() or target.read_text()!=text: stale.append(path)
        else: target.write_text(text)
    if stale: parser.exit(1,'Stale contracts/fixtures: '+', '.join(stale)+'\n')
    if not args.check:
        import re
        for slug,(purpose,steps) in EXPLANATIONS.items():
            path=ROOT/'mechanics'/slug/'README.md'
            text=path.read_text()
            section=('<!-- BEGIN PLAIN ENGLISH -->\n## Plain-English explanation\n\n'+purpose+'\n\n'
                     +'\n'.join(str(i)+'. '+step for i,step in enumerate(steps,1))
                     +'\n\nSee [PORTS.md](PORTS.md) for actual inputs, outputs and a worked example. '
                     'The [beginner guide](../../docs/beginner-guide.md) explains common coding words.\n'
                     +'<!-- END PLAIN ENGLISH -->\n')
            if '<!-- BEGIN PLAIN ENGLISH -->' in text:
                text=re.sub(r'<!-- BEGIN PLAIN ENGLISH -->.*?<!-- END PLAIN ENGLISH -->\n',lambda _:section,text,flags=re.S)
            else:
                title,rest=text.split('\n',1)
                text=title+'\n\n'+section+rest
            path.write_text(text)
        catalog=json.loads((ROOT/'catalog.json').read_text())
        for entry in catalog:
            slug=entry['id']
            for lang,file in LANGUAGES.items(): entry['implementations'][lang]=f'mechanics/{slug}/{lang}/{file}'
            entry['portable_contract']=f'mechanics/{slug}/PORTS.md'
            entry['portable_fixtures']='tests/port-fixtures.json#'+slug
            entry['portable_api']='numeric-kernel; see contract for differences from original Python API'
        (ROOT/'catalog.json').write_text(json.dumps(catalog,indent=2)+'\n')
    print('Port contracts and fixtures '+('match' if args.check else 'updated'))


if __name__=='__main__': main()
