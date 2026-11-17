#!/usr/bin/env python3
"""Second tries.  PREDICTIONS fixed before this script was run (2026-11-17), after the first-try numbers in tests_first_try.txt:
692 went half against 'street' (it shares lines with the month sign 920 at 7 against 2.1 expected).  New word nāṭu "district, land" (DEDR 3638).
   R692a (second catalogue): Mahadevan 150 (=692) and the Mahadevan partner of 920 share a line at 2.0 times chance or more.
   R692b: of the lines with both 692 and 920, in 5 of 7 the month sign comes first or the 692-060 comes first, but never inside the same name: i.e. the two are in separate phrases
          (no case of 692 and 920 directly adjacent).
842 went against 'helper, junior' (seal faces 1340-2209 mm2 against 605 for all seals).  Same word, better meaning: tuṇai = deputy, associate of a chief.
   R842a: 3 of 5 texts that end in 842 carry a chief sign (520 spear, 255, 388) earlier in the text; base rate in seal texts of 4+ signs is under 25%.
   R842b: every measured 842 seal is above the 75th percentile of all seal face areas.
525/526/527 (katavu "door"): first try showed 526 and 527 stand after the gate sign only 37% of the time.
   R525a: the three drawings replace each other in otherwise identical frames: 3 or more such frames in the Lipi table (like 705/706: 6 frames).
   R525b: the sign before the 52x group in the other 60% is a name-end word of the fish/house kind (class HOUSE or SELF) in 70% or more, i.e. '[name] door'.
335/711: R335a: in lines where 335 ends a house name ("335 760 740", "335 740"), the 335 is a house emblem: the same 335 house name repeats on 2 or more different objects at one site.
         R711a: lines with 711 and no cup/jar after the count still carry a tall count (2 of 2).
"""
import sys, collections, math, statistics
sys.path.insert(0, '/home/claude/ivc/work_scripts')
from holes_common import *
import pandas as pd
ls = lines(True); N = len(ls)
out = []
def P(s): out.append(s); print(s)
M = mah_lines()
cw = pd.read_csv(f'{ROOT}/work_data/lipi_mahadevan_crosswalk.csv', dtype=str)
m920 = set(int(x) for x in cw[cw.lipi == '920'].mahadevan); P(f'crosswalk partners of 920: {sorted(m920)}')
n150 = sum(1 for r in M if 150 in r['toks']); n920 = sum(1 for r in M if set(r['toks']) & m920)
both = sum(1 for r in M if 150 in r['toks'] and set(r['toks']) & m920)
exp = n150 * n920 / len(M)
P(f'R692a  Mahadevan lines {len(M)}: with 150 {n150}, with the month partner {n920}, both {both}, expected {exp:.2f}, ratio {both/exp:.2f}')
adj = 0; rows = []
for L in ls:
    t = L['toks']
    if '692' in t and '920' in t:
        a = t.index('692'); b = t.index('920'); adj += abs(a - b) == 1; rows.append((L['cisi'], a, b))
P(f'R692b  lines with both: {rows}; directly adjacent {adj}')
# 842
U = [(i, p) for i, L in enumerate(ls) for p, s in enumerate(L['toks']) if s == '842']
chief = {'520', '255', '388'}
def has_chief(t): return any(s in chief for s in t)
# the 842 seals: whole object text (all lines) because chief may be on line 1
objtexts = collections.defaultdict(list)
for L in ls: objtexts[L['obj']].append(L)
k = 0
for i, p in U:
    ot = [s for L in sorted(objtexts[ls[i]['obj']], key=lambda z: (z['face'], z['line'])) for s in L['toks']]
    h = has_chief([s for s in ot if s != '842']); k += h
    P(f'R842a  {ls[i]["cisi"]}: chief sign in the text {h}   text {"-".join(ot)}')
base = [h for h in (has_chief([s for L in v for s in L['toks']]) for o, v in objtexts.items() if kind(v[0]['type']) == 'SEAL' and sum(len(L['toks']) for L in v) >= 4)]
P(f'R842a  {k} of {len(U)} have a chief sign; base rate over seals of 4+ signs {sum(base)/len(base):.3f} ({sum(base)} of {len(base)})')
raw = pd.read_csv(f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv', dtype=str).fillna('')
raw['obj'] = raw.id.str.split('.').str[0]
def area(r):
    try: return float(r['horizontal(mm)']) * float(r['vertical(mm)'])
    except: return 0
seal_areas = [area(r) for _, r in raw.iterrows() if r['type'].startswith('SEAL') and area(r) > 0]
q75 = statistics.quantiles(seal_areas, n=4)[2]; med = statistics.median(seal_areas)
P(f'R842b  seal faces measured {len(seal_areas)}; median {med:.0f}, 75th percentile {q75:.0f}')
ar = []
for i, _ in U:
    r = raw[raw.obj == ls[i]['obj']].iloc[0]; a = area(r); ar.append(a)
    pct = sum(1 for x in seal_areas if x < a) / len(seal_areas) if a else None
    P(f'R842b  {ls[i]["cisi"]}: area {a:.0f} mm2, percentile {pct}')
# 525 family frames
fam = {'525', '526', '527'}
frames = collections.defaultdict(set)
for L in ls:
    t = L['toks']
    for p, s in enumerate(t):
        if s in fam: frames[(t[:p], t[p + 1:])].add((s, L['cisi']))
sw = [(k_, v) for k_, v in frames.items() if len({s for s, _ in v}) >= 2]
P(f'R525a  frames in which two of 525/526/527 replace each other: {len(sw)}')
for k_, v in sw: P('        ' + '-'.join(k_[0]) + ' _ ' + '-'.join(k_[1]) + '  ' + str(sorted(v)))
# R525b: sign before the family when not after 550
cl = collections.Counter(); n = 0
from sound_v2_tiers import CLASS
for L in ls:
    t = L['toks']
    for p, s in enumerate(t):
        if s in fam and p > 0 and t[p - 1] != '550':
            n += 1; cl[CLASS.get(t[p - 1], 'unvalued')] += 1
P(f'R525b  sign before 52x when not 550: {n} cases; classes {dict(cl.most_common())}')
# 335 house name repeat
hn = collections.defaultdict(list)
for L in ls:
    t = L['toks']
    for p, s in enumerate(t):
        if s == '335' and p + 1 < len(t) and t[p + 1] in ('740', '760'):
            hn[(t[p - 1] if p else '^', '335', t[p + 1])].append((L['cisi'], L['site']))
P('R335a  335 before 740/760 with its left neighbour: ' + str({k_: v for k_, v in hn.items()}))
cnt = [(L['cisi'], '-'.join(L['toks'])) for L in ls if '711' in L['toks'] and L['toks'][-1] in ('033',)]
P(f'R711a  lines ending in 711+count with no cup/jar: {cnt}')
open(f'{HOLES}/tests_second_try.txt', 'w').write('\n'.join(out))
