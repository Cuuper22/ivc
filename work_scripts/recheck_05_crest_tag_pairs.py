#!/usr/bin/env python3
"""Recheck 5: seal pairs of one crest share a building 1.41 to 1.43 times chance; same-tag pairs 1.11; at Harappa
same-tag pairs share a trench 1.68 times (registry_tests.py, parts G and c).

Plain words: CREST (house key) = first sign of the name; TAG = last name sign before the ending. A PAIR = two seals of
one city with the same crest (or the same tag and different crests). SHARE = both found in the same building
(Mohenjo-daro area + house) or the same area (excavation trench). CHANCE = findspots shuffled among the seals of the
city that have a findspot at that level.

Checks: (1) people.csv has one row per FACE (1,190 rows, 1,174 stones): a two-faced seal with one crest on both faces
is a same-crest pair that always shares its building; (2) the shuffle pool; (c) identical texts in one place once.
Clean run: one row per stone (first face with a name kept), identical full texts in one place once.
Run: python3 recheck_05_crest_tag_pairs.py   (about 2 minutes)
"""
import sys, collections, random
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
import numpy as np, pandas as pd
from recheck_common import *
say = log_to(f'{OUT}/r05_log.txt')
f2s, _ = stone_map()
R = f'{ROOT}/work_data/registry'
P0 = pd.read_csv(f'{R}/people.csv', dtype=str).fillna('')
P0['stone'] = P0.face_id.map(f2s)
full = faces().groupby('obj').text.apply(lambda s: '|'.join(sorted(s))).to_dict()
P0['full'] = P0.stone.map(full)
H = pd.read_csv(f'{R}/houses.csv', dtype=str).fillna(''); H['seals'] = H.seals.astype(int)
H['objects_all'] = H.objects_all.astype(int); H['n_cities'] = H.n_cities.astype(int)
TITLES = {'142', '151', '152', '153', '154', '155', '156', '157', '158', '161', '368', '525', '526', '527', '842', '617', '717', '097', '137', '090'}
TOP = list(H[(H.seals >= 5) & (~H.house_key.isin(TITLES))].sort_values(['objects_all', 'n_cities'], ascending=False).head(20).house_key)
two = P0[P0.stone.duplicated(keep=False)]
same_crest_twice = sum(1 for _, g in two.groupby('stone') if g.house_key.nunique() == 1)
say(f'people.csv: {len(P0)} rows, {P0.stone.nunique()} stones; stones with two face rows {two.stone.nunique()}, '
    f'of them with one crest on both rows {same_crest_twice}')

def pairstats(S, level, rel, nsh, seed):
    rnd = random.Random(seed)
    S = S.reset_index(drop=True)
    hk, tg, loc, st = list(S.house_key), list(S.tag), list(S[level]), list(S.stone)
    pairs = []
    n = len(S)
    for i in range(n):
        for j in range(i + 1, n):
            if rel == 'crest' and hk[i] == hk[j]: pairs.append((i, j))
            elif rel == 'top20' and hk[i] == hk[j] and hk[i] in TOP: pairs.append((i, j))
            elif rel == 'tag' and tg[i] and tg[i] == tg[j] and hk[i] != hk[j]: pairs.append((i, j))
    obs = sum(loc[i] == loc[j] for i, j in pairs)
    onestone = sum(st[i] == st[j] for i, j in pairs)
    nl = []
    for t in range(nsh):
        sh = loc[:]; rnd.shuffle(sh); nl.append(sum(sh[i] == sh[j] for i, j in pairs))
    a = np.array(nl)
    return len(pairs), obs, a.mean(), pvalue_hi(a, obs), onestone

cases = [('Mohenjo-daro', 'building', 'top20', '1.41 (23 vs 16.3, P 0.080)'), ('Mohenjo-daro', 'building', 'crest', '1.43 (28 vs 19.54, P 0.056)'),
         ('Mohenjo-daro', 'building', 'tag', '1.11 (16 vs 14.40, P 0.35)'), ('Harappa', 'area_key', 'tag', '1.68 (32 vs 19.07, P 0.011)'),
         ('Harappa', 'area_key', 'crest', '1.11 (22 vs 19.75)')]
out = []
for site, level, rel, old in cases:
    S = P0[(P0.city == site) & (P0[level] != '')]
    n, o, e, p, one = pairstats(S, level, rel, 1000, 7)
    Ss = S.drop_duplicates('stone')
    n1, o1, e1, p1, _ = pairstats(Ss, level, rel, 2000, 8)
    Sc = Ss.drop_duplicates([level, 'full'])
    n2, o2, e2, p2, one2 = pairstats(Sc, level, rel, 2000, 8)
    say(f'{site:12s} {level:8s} same {rel:5s} | old {old} | as run: {o} of {n} pairs vs {e:.2f} ({o / e:.2f}), pairs that are one stone {one} | '
        f'stones only: {o1} of {n1} vs {e1:.2f} (ratio {o1 / e1:.2f}, P {p1:.4f}) | CLEAN: {o2} of {n2} vs {e2:.2f} (ratio {o2 / e2:.2f}, P {p2:.4f}); rows dropped {len(S) - len(Sc)}')
    out.append(dict(site=site, level=level, pair=rel, old=old, run_obs=o, run_exp=e, one_stone_pairs=one, stones_obs=o1, stones_exp=e1, stones_P=p1, clean_obs=o2, clean_pairs=n2, clean_exp=e2, clean_P=p2))
pd.DataFrame(out).to_csv(f'{OUT}/r05_table.csv', index=False)
