#!/usr/bin/env python3
"""Task 2 (marked fish against houses, cities, animals, counts) and task 4 (names spelled two ways; names readable
in full with the sound table). Output: work_data/sound/fish.csv, spell2.csv, readable_names.csv (printed summary)."""
import sys, os, collections
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gloss2 import load2, learn, parse_face
from sound_values import ALL_SOUNDS
ROOT = '/home/claude/ivc'; OUT = f'{ROOT}/work_data/sound'
VAL = {f'{i:03d}': i for i in range(1, 8)}; VAL.update({'012': 2}); VAL.update({f'{i:03d}': i - 10 for i in range(13, 19)}); VAL.update({f'{i:03d}': i - 30 for i in range(31, 37)})
print('stage 1/3: parsing ...', flush=True)
d = load2(); lex = learn(d); d['P'] = [parse_face(x, lex) for x in d.tok]
FISH = ['220', '235', '240', '233', '231', '226', '236']
rows = []
for f in FISH:
    sites = collections.Counter(); anim = collections.Counter(); cnt = collections.Counter(); pos = collections.Counter(); nxt = collections.Counter()
    n = 0
    for x, s, a, P in zip(d.tok, d.site, d.symbol, d.P):
        for i, t in enumerate(x):
            if t != f: continue
            n += 1; sites[s] += 1; anim[(a or '-').split(':')[0]] += 1
            if i > 0 and x[i - 1] in VAL and not (i == 2 and x[0] in ('861', '817', '820')): cnt[VAL[x[i - 1]]] += 1
            pos[P['roles'][i]] += 1; nxt[x[i + 1] if i + 1 < len(x) else '$'] += 1
    rows.append(dict(fish=f, n=n, sites='; '.join(f'{k} {v}' for k, v in sites.most_common(5)), animals='; '.join(f'{k} {v}' for k, v in anim.most_common(4)),
                     counts_before='; '.join(f'{k}:{v}' for k, v in sorted(cnt.items())), roles='; '.join(f'{k} {v}' for k, v in pos.most_common(4)),
                     next='; '.join(f'{k} {v}' for k, v in nxt.most_common(4))))
pd.DataFrame(rows).to_csv(f'{OUT}/fish.csv', index=False)
print(pd.DataFrame(rows).to_string())

print('stage 2/3: names spelled two ways ...', flush=True)
names = collections.defaultdict(set)   # name tuple -> set of (site, cisi)
for x, c, s, ci, P in zip(d.tok, d.complete_txt, d.site, d.cisi, d.P):
    if not c: continue
    for g in P['names']:
        if g and all(t not in ('000', 'ALT') for t in g): names[tuple(g)].add((s, ci))
by_len = collections.defaultdict(list)
for nm in names: by_len[len(nm)].append(nm)
subs = collections.defaultdict(list)
for L in by_len:
    for a in by_len[L]:
        for b in by_len.get(L + 1, []):
            for k in range(L):
                P, S = a[:k], a[k + 1:]
                if b[:k] == P and b[k + 2:] == S and (P or S) and b[k] != a[k] and b[k + 1] != a[k]:
                    same = {s for s, _ in names[a]} & {s for s, _ in names[b]}
                    subs[(a[k], b[k], b[k + 1])].append(('-'.join(a), '-'.join(b), ','.join(sorted(same)) or 'different sites'))
sp = []
for (x, y, z), lst in subs.items():
    frames = len(lst)
    sx, sy, sz = (ALL_SOUNDS.get(t, ('', ''))[0] for t in (x, y, z))
    sp.append(dict(one=x, two=f'{y}-{z}', frames=frames, sound_one=sx, sound_two=f'{sy}+{sz}' if sy and sz else '',
                   examples=' | '.join(f'{a} ~ {b} ({s})' for a, b, s in lst[:4])))
sp = pd.DataFrame(sp).sort_values('frames', ascending=False); sp.to_csv(f'{OUT}/spell2.csv', index=False)
print(sp.head(25).to_string())

print('stage 3/3: names readable in full ...', flush=True)
rd = []
for nm, where in names.items():
    if all(t in ALL_SOUNDS and ALL_SOUNDS[t][0] not in ('?', '') and not ALL_SOUNDS[t][0].startswith('(') for t in nm):
        rd.append(dict(name='-'.join(nm), objects=len(where), sites=len({s for s, _ in where}), read=' '.join(ALL_SOUNDS[t][0] for t in nm),
                       gloss=' '.join(ALL_SOUNDS[t][1] for t in nm), example=sorted(where)[0][1]))
rd = pd.DataFrame(rd).sort_values('objects', ascending=False); rd.to_csv(f'{OUT}/readable_names.csv', index=False)
tot = sum(len(v) for v in names.values()); cov = rd.objects.sum()
print(f'distinct names {len(names)}, readable in full {len(rd)}; name tokens {tot}, readable {cov} ({cov / tot:.0%})')
print(rd.head(40).to_string())
