#!/usr/bin/env python3
"""Pick the 40 longest distinct texts (+ Dholavira signboard), segment into phrases, parse, read. Writes work_data/long_texts/texts.json and sections.md"""
import json, collections
from long_common import *
objs = build_objects()
sig = collections.defaultdict(list)
for o, ob in objs.items(): sig[obj_signature(ob)].append(ob)
rows = []
for s, obl in sig.items():
    ob = obl[0]
    rows.append((n_legible(ob), n_total(ob), ob, len(obl), [x['cisi'] or x['obj'] for x in obl]))
rows.sort(key=lambda t: (-t[0], -t[1]))
top = rows[:40]
sb = [r for r in rows if r[2]['obj'] == '144']
print('cutoff legible', top[-1][0], 'signboard rank', rows.index(sb[0]) + 1 if sb else None)
out = []
def analyse(ob):
    phr = []
    for fi, f in enumerate(ob['faces'], 1):
        for li, line in enumerate(f['lines'], 1):
            x = tuple(line)
            for a, b in segment(x):
                p = x[a:b]; P = parse_phrase(p)
                sd, en = read_phrase(p, P)
                nm = P['names']
                unk = [s for s in p if s not in CNT and s != '806' and not snd(s)]
                ob_ = [br for g in nm for br in order_breaks(g)]
                phr.append(dict(face=fi, line=li, signs=list(p), roles=P['roles'], kind=phrase_kind(p, P), sound=sd, english=en,
                                unvalued=unk, order_breaks=ob_, names=nm, template=' '.join(P['roles'])))
    return phr
for k, (nl, nt, ob, ncop, cop) in enumerate(top + sb, 1):
    out.append(dict(rank=k, legible=nl, total=nt, copies=ncop, copy_ids=cop[:12], cisi=ob['cisi'], obj=ob['obj'], site=ob['site'], type=ob['type'],
                    area=ob['area'], block=ob['block'], depth=ob['depth'], animal=ob['animal'], size=f"{ob['h']}x{ob['v']}",
                    faces=[dict(id=f['id'], lines=f['lines'], broken=f['broken']) for f in ob['faces']], phrases=analyse(ob)))
json.dump(out, open(f'{OUTDIR}/texts.json', 'w'), ensure_ascii=False, indent=1)
for t in out[:6] + out[-1:]:
    print(t['rank'], t['cisi'], t['site'], t['type'], t['legible'], t['copies'])
    for p in t['phrases']: print('   ', p['face'], p['line'], '-'.join(p['signs']), '|', p['kind'], '|', p['english'], '|', p['unvalued'], p['order_breaks'])
