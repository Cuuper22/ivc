#!/usr/bin/env python3
"""Recheck 15 (added by the coordinator): jobs/out/copper.md finding 6, copies of one copper-tablet set share one
register lot 6 times against 0.83 (P 0.0005), and lie within 100 register numbers 15 times against 7.60 (P 0.013)
(copper_6_spots.py T6.1a/b).

Plain words: COPPER TABLET SET = copper tablets with one text (and picture). REGISTER LOT = the excavator's find number
(DK 3447, HR 4337 ...); the first catalogue sometimes gives it with the plate reference of the dig report glued on
(DK344793.9 = DK 3447, plate 93 no. 9). CHANCE = set labels dealt among tablets of the same register series.

Check: the first catalogue lists some Mohenjo-daro copper tablets twice: once from the corpus volume (an M- number)
and once, without a corpus number, from the dig report's plates. Two rows of ONE tablet with one register number would
be a "pair of copies in one lot" that always shares. Rule: two rows are one tablet when they have the same register
series and number, no conflicting letter suffix (a / b mark two finds), the same set, and sizes within 1.5 mm on both
sides (where both are given). Two faces of one tablet: the table has one row per object (checked).
Run: python3 recheck_15_copper_lots.py   (about 1 minute)
"""
import sys, itertools
sys.path.insert(0, '/home/claude/ivc/work_scripts')
import numpy as np, pandas as pd
from recheck_common import *
say = log_to(f'{OUT}/r15_log.txt')
L = pd.read_csv(f'{ROOT}/work_data/copper/spots_objects.csv', dtype=str).fillna('')
say(f'rows {len(L)}, objects {L.obj.nunique()} (one row per object: two faces of one tablet cannot pair)')
d = faces()
info = d.groupby('obj').agg(h=('horizontal(mm)', 'first'), v=('vertical(mm)', 'first'), exc=('excavation-idno', 'first'))
L['h'] = pd.to_numeric(L.obj.map(info.h), errors='coerce').fillna(0); L['v'] = pd.to_numeric(L.obj.map(info.v), errors='coerce').fillna(0)
L['exc'] = L.obj.map(info.exc)
R = L[L.regno != ''].copy(); R['regno'] = R.regno.astype(float)
# one-tablet rule
parent = {o: o for o in R.obj}
def find(x):
    while parent[x] != x: x = parent[x]
    return x
merged = []
for (s, n), g in R.groupby(['series', 'regno']):
    for a, b in itertools.combinations(g.index, 2):
        A, B = R.loc[a], R.loc[b]
        if A.fam != B.fam: continue
        if A.regsuf and B.regsuf and A.regsuf != B.regsuf: continue
        if any(x and y and abs(x - y) > 1.5 for x, y in ((A.h, B.h), (A.v, B.v))): continue
        parent[find(A.obj)] = find(B.obj)
        merged.append(f'{A.cisi or "row " + A.obj} ({A.exc}, {A.h:g}x{A.v:g}) = {B.cisi or "row " + B.obj} ({B.exc}, {B.h:g}x{B.v:g})')
say(f'rows judged to be one tablet listed twice: {len(merged)}')
for m in merged: say('   ' + m)
R['tablet'] = R.obj.map(find)
rng = np.random.default_rng(9)
def pair_test(D, close, label, n=10000):
    D = D.reset_index(drop=True); fam = D.fam.values
    idx = [(i, j) for i, j in itertools.combinations(range(len(D)), 2) if D.series[i] == D.series[j]]
    I = np.array([i for i, _ in idx]); J = np.array([j for _, j in idx])
    cl = np.array([close(D.iloc[i], D.iloc[j]) for i, j in idx])
    def stat(f): return cl[f[I] == f[J]].sum()
    s = stat(fam); groups = D.series.values; sims = []
    for _ in range(n):
        f = fam.copy()
        for g in set(groups):
            m = np.where(groups == g)[0]; f[m] = rng.permutation(f[m])
        sims.append(stat(f))
    sims = np.array(sims)
    say(f'  {label}: {s} against {sims.mean():.2f} (ratio {s / sims.mean():.2f}, P {pvalue_hi(sims, s):.4f})')
    return int(s), sims.mean(), pvalue_hi(sims, s)
lot = lambda a, b: a.series == b.series and a.regno == b.regno
w100 = lambda a, b: a.series == b.series and abs(a.regno - b.regno) <= 100
say('A  as run (every catalogue row)')
r0 = [pair_test(R, lot, 'same register lot'), pair_test(R, w100, 'within 100 numbers')]
Rc = R.drop_duplicates('tablet')
say(f'B  clean: rows of one tablet merged ({len(R) - len(Rc)} rows removed)')
r1 = [pair_test(Rc, lot, 'same register lot'), pair_test(Rc, w100, 'within 100 numbers')]
import json
json.dump(dict(run=r0, clean=r1, merged=merged), open(f'{OUT}/r15.json', 'w'), default=float, indent=1)
