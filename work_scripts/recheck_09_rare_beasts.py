#!/usr/bin/env python3
"""Recheck 9: rare beasts are spread one per building: two non-unicorn beast seals in one building carry the same
species 13 times against 20.8 (stand_6_animals.py Q3, P 0.085).

Plain words: RARE BEAST = any animal on a seal other than the unicorn (short-horned bull, zebu, elephant, rhinoceros,
tiger, buffalo, goat, composite). A PAIR = two rare-beast seals found in one building. CHANCE (old) = species labels,
including 'unicorn' and 'none' (no animal carved), dealt among ALL seals of the city: that changes how many rare-beast
pairs exist in each deal and lets 'none' land on stones that are beast seals and the reverse.

Checks: (1) one row per stone (the old script kept one face per object: fine); (2) the deal pool; (c) identical
texts in one building once. Clean run: the species dealt only among the rare-beast stones of the same city (and of
the same city x format), so the 91-odd pairs stay fixed and only the species moves.
Run: python3 recheck_09_rare_beasts.py   (about 1 minute)
"""
import sys, io, contextlib
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
import numpy as np, pandas as pd
from recheck_common import *
say = log_to(f'{OUT}/r09_log.txt')
with contextlib.redirect_stdout(io.StringIO()):
    from stand_common import stand_seals, perm_within, strata_idx
rng = np.random.default_rng(6)
f2s, _ = stone_map()
S = stand_seals()
d = S.drop_duplicates('obj').reset_index(drop=True)
d['stone'] = d.face.map(f2s); d = d.drop_duplicates('stone')
G = {'unicorn': 'unicorn', 'short-horned bull': 'short-horned bull', 'zebu': 'zebu', 'elephant': 'elephant', 'rhinoceros': 'rhinoceros',
     'tiger': 'tiger', 'buffalo': 'buffalo', 'goat': 'goat', 'Bull3': 'goat', 'none': 'none'}
for k in ['Comp', 'CompBull', 'Mult', 'T-A-T', 'T-M-T', 'Htgr', 'Phyt']: G[k] = 'composite'
d['sp'] = [G.get(a, 'other' if a else '') for a in d.animal]
d = d[d.sp != '']
BEAST = {'short-horned bull', 'zebu', 'elephant', 'rhinoceros', 'tiger', 'buffalo', 'goat', 'composite'}
b = d[(d.building != '')].reset_index(drop=True)
nb = len(b); b = b.drop_duplicates(['building', 'signs']).reset_index(drop=True)
say(f'stones with a building and a species: {nb}; identical texts in one building removed: {nb - len(b)}')
I, J = np.triu_indices(len(b), 1); same = b.building.values[I] == b.building.values[J]; I, J = I[same], J[same]
lab = np.asarray(b.sp.values, dtype=object)

def beast_same(l):
    nu = np.array([x in BEAST for x in l]); both = nu[I] & nu[J]
    return int(both.sum()), int((l[I] == l[J])[both].sum())

def run(strata, label, nsh=5000):
    rp, rs = beast_same(lab); sims = np.array([beast_same(perm_within(lab, strata, rng)) for _ in range(nsh)])
    say(f'  {label}: rare-beast pairs in one building {rp}, same species {rs}; dealt pairs {sims[:, 0].mean():.1f}, same species {sims[:, 1].mean():.2f} '
        f'(ratio {rs / sims[:, 1].mean():.2f}, P fewer {pvalue_lo(sims[:, 1], rs):.4f})')
    return rs, sims[:, 1].mean(), pvalue_lo(sims[:, 1], rs), rp
r0 = run(strata_idx(b.site.values), 'A  old design (all species labels dealt among all seals of the city)')
isb = np.array([x in BEAST for x in lab])
key = np.where(isb, b.site.values, 'x' + np.arange(len(b)).astype(str))       # non-beast stones stay fixed
r1 = run(strata_idx(key), 'B  clean: species dealt only among rare-beast stones of the same city')
key2 = np.where(isb, (b.site + '|' + b.fmt).values, 'x' + np.arange(len(b)).astype(str))
r2 = run(strata_idx(key2), 'C  clean, within city x format')
import json
json.dump(dict(old=r0, clean=r1, clean_fmt=r2), open(f'{OUT}/r09.json', 'w'), default=float, indent=1)
# the companion number "two rare-beast seals share a building 91 times against 118": beast/not dealt among stones that
# can carry a carved animal (inscription-only formats left fixed), within city x format
hasan = lab != 'none'
key3 = np.where(hasan, (b.site + '|' + b.fmt).values, 'x' + np.arange(len(b)).astype(str))
sims = np.array([beast_same(perm_within(lab, strata_idx(key3), rng))[0] for _ in range(3000)])
rp = beast_same(lab)[0]
say(f'  D  rare-beast pairs in one building {rp} against {sims.mean():.1f} when species are dealt only among stones with a carved animal, '
    f'within city x format (P fewer {pvalue_lo(sims, rp):.4f})')
