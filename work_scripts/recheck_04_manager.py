#!/usr/bin/env python3
"""Recheck 4: [crest] jar man seals ("managers") share a building with an owner object of the same crest
(registry_tests2.py (a), spots_1_manager.py (a) and (b)).
Old: Mohenjo-daro building 5 of 24 against 2.09; block 9 of 24 against 5.28; pooled block 11 of 30 against 6.35;
those buildings hold 9 same-crest objects against 2.94.

Plain words: MANAGER = a seal whose text ends jar 740 + man 090; its CREST is the first sign of the name before the jar.
OWNER OBJECT = any undamaged object (seal, tablet, tag, pot ...) with a name of that crest closed by another ending.
HIT = the manager's building (or block) also holds an owner object of his crest. CHANCE = the manager's findspot
replaced by the findspot of a seal drawn at random from the same city (the old design), 5,000 times.

Checks: (1) the tables (people.csv, names_all.csv) have one row per FACE: a two-faced seal sits twice in the pool,
a two-faced owner tablet counts twice in a building's tally; (2) the pool the manager's findspot is drawn from;
(c) moulded copies with one text in one building counted once (they swell the "objects in the building" tally).
Clean run: one row per stone; owner tally counts copy events (same building + same full text = 1); manager's
findspot drawn from stones (not faces) of the same city.
Run: python3 recheck_04_manager.py   (about 1 minute)
"""
import sys, re, collections, random
sys.path.insert(0, '/home/claude/ivc/work_scripts')
import numpy as np, pandas as pd
from recheck_common import *
say = log_to(f'{OUT}/r04_log.txt')
random.seed(101)
f2s, _ = stone_map()
R = f'{ROOT}/work_data/registry'
P = pd.read_csv(f'{R}/people.csv', dtype=str).fillna('')
A = pd.read_csv(f'{R}/names_all.csv', dtype=str).fillna('')
A = A[(A.damaged == 'False') & (A.goods_line == 'False')].copy()
P['site'] = P.city; P['is_agent'] = P.master != ''
A['is_agent'] = A.ending.str.startswith("X's man")
P['stone'] = P.face_id.map(f2s); A['stone'] = A.face_id.map(f2s)
say(f'people.csv rows {len(P)}, stones {P.stone.nunique()}; names_all rows (undamaged) {len(A)}, stones {A.stone.nunique()}')
ag_twice = P[P.is_agent].stone.duplicated().sum()
say(f'  managers that sit twice in people.csv (two faces): {ag_twice}')
full = faces().groupby('obj').text.apply(lambda s: '|'.join(sorted(s))).to_dict()
A['full'] = A.stone.map(full)
LEVELS = ['building', 'block']

def homes_of(own, mode):
    h = {lev: collections.defaultdict(collections.Counter) for lev in LEVELS}
    for lev in LEVELS:
        if mode == 'faces':
            it = zip(own.house_key, own[lev])
        else:
            o2 = own[own[lev] != ''].drop_duplicates('stone')
            if mode == 'events': o2 = o2.drop_duplicates([lev, 'full'])
            it = zip(o2.house_key, o2[lev])
        for k, z in it:
            if z: h[lev][k][z] += 1
    return h

def run(Ptab, homes, lev, sites, nsh=5000):
    sub = Ptab[Ptab.is_agent & (Ptab[lev] != '') & Ptab.site.isin(sites)]
    pool = Ptab[(Ptab[lev] != '') & Ptab.site.isin(sites)]
    bycity = collections.defaultdict(list)
    for b, c in zip(pool[lev], pool.site): bycity[c].append(b)
    keys, cities, locs = list(sub.house_key), list(sub.site), list(sub[lev])
    obs = sum(homes[lev].get(k, {}).get(b, 0) > 0 for k, b in zip(keys, locs))
    tot = sum(homes[lev].get(k, {}).get(b, 0) for k, b in zip(keys, locs))
    nl = np.zeros(nsh); nt = np.zeros(nsh)
    for t in range(nsh):
        draws = [random.choice(bycity[c]) for c in cities]
        nl[t] = sum(homes[lev].get(k, {}).get(b, 0) > 0 for k, b in zip(keys, draws))
        nt[t] = sum(homes[lev].get(k, {}).get(b, 0) for k, b in zip(keys, draws))
    return obs, len(sub), nl.mean(), pvalue_hi(nl, obs), tot, nt.mean(), pvalue_hi(nt, tot)

own = A[~A.is_agent]
MD = ['Mohenjo-daro']; ALL = sorted(set(P.site))
res = {}
for label, Ptab, mode in (('OLD  (faces, as run)', P, 'faces'),
                          ('CLEAN (stones; owner copies in one building once)', P.drop_duplicates('stone'), 'events')):
    H = homes_of(own, mode)
    say(f'\n{label}')
    for nm, sites, lev in (('Mohenjo-daro', MD, 'building'), ('Mohenjo-daro', MD, 'block'), ('pooled', ALL, 'building'), ('pooled', ALL, 'block')):
        o, n, mu, p, tot, tmu, tp = run(Ptab, H, lev, sites)
        res[(label[:5], nm, lev)] = (o, n, mu, p, tot, tmu, tp)
        say(f'  {nm:12s} {lev:8s}: {o} of {n} managers sit with an owner object of their crest; chance {mu:.2f} (ratio {o / mu:.2f}, P {p:.4f}) | '
            f'owner objects of the crest in those places {tot} against {tmu:.2f} (P {tp:.4f})')
# what the copies were
H0 = homes_of(own, 'faces'); H1 = homes_of(own, 'events')
for _, r in P[P.is_agent & (P.building != '') & (P.site == 'Mohenjo-daro')].drop_duplicates('stone').iterrows():
    a, b = H0['building'].get(r.house_key, {}).get(r.building, 0), H1['building'].get(r.house_key, {}).get(r.building, 0)
    if a: say(f'   {r.cisi:8s} {r.building:34s} crest {r.house_key}: owner objects counted {a} as faces, {b} as copy events')
import json
json.dump({' | '.join(k): v for k, v in res.items()}, open(f'{OUT}/r04.json', 'w'), default=float, indent=1)
