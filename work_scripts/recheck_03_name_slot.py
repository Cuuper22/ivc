#!/usr/bin/env python3
"""Recheck 3: "Name = crest + personal part + tag".
  (i)  the same fish variant first among house-mates: 15 of 23 pairs against 36% by chance (name_slot_account.py);
  (ii) name-slot (who) signs repeat inside houses: 19 pairs against 7.8 (gloss_report.py, 'who-sign, area-section +
       block-house').

Plain words: HOUSE = excavation area + block-house at Mohenjo-daro. A NAME is the run of signs between the opening
and the closing sign (template parser). FISH-FIRST = the name starts with one of the four fish signs 231/233/235/240.
WHO-SIGN = the last sign the parser puts in the personal-name slot. CHANCE = house labels dealt at random.

Checks: (1) do the tables have one row per face, so that two faces of one seal can make a pair? (2) is the deal
confined to seals that can carry the property? (c) identical texts in one house counted once.
Run: python3 recheck_03_name_slot.py   (about 1-2 minutes)
"""
import sys, re, collections, itertools, random
sys.path.insert(0, '/home/claude/ivc/work_scripts')
import numpy as np, pandas as pd
from recheck_common import *
say = log_to(f'{OUT}/r03_log.txt')
f2s, _ = stone_map()
NSH = 3000
FISH = {'235', '240', '233', '231'}

def depth(s):
    m = re.search(r'(-?\d+(\.\d+)?)\s*ft', s); return float(m.group(1)) if m else None

# ---------------- (i) fish-first ----------------
say('(i) same fish first among house-mates (old: 15 of 23 = 65% against 36%, P 0.003)')
o = pd.read_csv(f'{ROOT}/work_data/name_rows.csv', dtype=str).fillna('')
for c in ['tight', 'has_class']: o[c] = o[c] == 'True'
o['seglen'] = o.seglen.astype(int)
T = o[o.tight & o.has_class & (o.seglen >= 1)].copy(); T['segl'] = T.seg.str.split('-')
say(f'  name_rows.csv: {len(o)} rows, {o.obj.nunique()} objects (rows are faces); the old fish test kept one face per object '
    f'(drop_duplicates on obj), so fault 1 cannot enter it.')
M = T[(T.site == 'Mohenjo-daro') & ~T.bh.isin(['--', '-', ''])].copy()
M['stone'] = M.id.map(f2s)
M = M.drop_duplicates('stone'); M['hk'] = M.area + ' ' + M.bh
M['band'] = [(a, int(depth(d) // 3) if depth(d) is not None else -9) for a, d in zip(M.area, M.depth)]
M['full'] = M.reading

def fish_test(D, label, rng_seed=5):
    random.seed(rng_seed)
    D = D.reset_index(drop=True); hk = list(D.hk); L = list(D.segl)
    strata = collections.defaultdict(list)
    for i, b in enumerate(D.band): strata[b].append(i)
    def stat(keys):
        idx = collections.defaultdict(list)
        for i, h in enumerate(keys): idx[h].append(i)
        fp = fs = 0
        for m in idx.values():
            for a, b in itertools.combinations(m, 2):
                if L[a][0] in FISH and L[b][0] in FISH: fp += 1; fs += L[a][0] == L[b][0]
        return fp, fs
    obs = stat(hk); rates = []; fss = []
    for t in range(NSH):
        p = hk[:]
        for idx in strata.values():
            x = idx[:]; random.shuffle(x)
            for i, j in zip(idx, x): p[i] = hk[j]
        a, b = stat(p)
        if a: rates.append(b / a); fss.append(b)
    r = obs[1] / obs[0]; rates = np.array(rates)
    say(f'  {label}: {len(D)} seals; fish-first pairs in one house {obs[0]}, same fish {obs[1]} ({r:.0%}) against {rates.mean():.0%} by chance '
        f'(P {pvalue_hi(rates, r):.4f})')
    return obs, rates.mean(), pvalue_hi(rates, r)

Mm = M[M.seglen >= 2]
r0 = fish_test(Mm, 'A  old design (multi-sign names, all dealt within area x 3-ft band)')
# clean: identical full texts in one house once; deal only among fish-first seals
Mc = Mm.drop_duplicates(['hk', 'full'])
say(f'  identical texts in one house removed: {len(Mm) - len(Mc)}')
r1 = fish_test(Mc[Mc.segl.map(lambda l: l[0] in FISH)], 'B  clean (stones, identical texts once, deal only among fish-first seals)')

# ---------------- (ii) who-sign repeats ----------------
say('\n(ii) who-signs repeat inside houses (old: 19 pairs against 7.8, P 0.002)')
from gloss import load, lexicon_from, gloss_text
d = load(); lex = lexicon_from(d)
d['roles'] = [gloss_text(x, lex, f) for x, f in zip(d.tok, d.flg)]
def slot_signs(x, r, role): return [s for s, q in zip(x, r) if q == role]
d['house_sign'] = [(slot_signs(x, r, 'house') or [None])[0] for x, r in zip(d.tok, d.roles)]
d['who1'] = [(slot_signs(x, r, 'who') or [None])[-1] for x, r in zip(d.tok, d.roles)]
bad = lambda v: v in ('', '--', '-')
mo = d[(d.site == 'Mohenjo-daro') & d.complete_txt & d.house_sign.notna() & (d.group == 'seal') & d.who1.notna()].copy()
mo = mo[[not (bad(a) or bad(b)) for a, b in zip(mo['area-section'], mo['block-house'])]].copy()
mo['unit'] = mo['area-section'] + '|' + mo['block-house']
rng = np.random.default_rng(7)

def pairtest(df, label, strat=None):
    sg = df.who1.values; un = df.unit.values
    def stat(u):
        t = pd.DataFrame({'u': u, 's': sg}); ng = t.groupby(['u', 's']).size(); return int((ng * (ng - 1) // 2).sum())
    obs = stat(un); null = []
    groups = [np.where(df[strat].values == v)[0] for v in pd.unique(df[strat])] if strat else None
    for _ in range(NSH):
        if groups is None: null.append(stat(rng.permutation(un)))
        else:
            u2 = un.copy()
            for g in groups: u2[g] = un[rng.permutation(g)]
            null.append(stat(u2))
    null = np.array(null)
    say(f'  {label}: {len(df)} rows; pairs sharing the who-sign {obs} against {null.mean():.2f} (ratio {obs / null.mean():.2f}, P {pvalue_hi(null, obs):.4f})')
    return obs, null.mean(), pvalue_hi(null, obs)

old = mo.drop_duplicates(['unit', 'tok'])
s0 = pairtest(old, 'A  old design (one row per FACE, identical texts in a house once, dealt over the whole city)')
old['stone'] = old.id.map(f2s)
dupl = old[old.stone.duplicated(keep=False)]
say(f'  rows that are a second face of a stone already in the table: {old.stone.duplicated().sum()}; '
    f'same-house same-who pairs that are one stone: '
    f'{sum(1 for _, g in dupl.groupby("stone") if g.who1.nunique() == 1)}')
cl = old.drop_duplicates('stone').copy()
cl['area'] = cl['area-section']
s1 = pairtest(cl, 'B  clean: one row per stone, identical texts once, dealt over the whole city')
s2 = pairtest(cl, 'C  clean, dealt within excavation area', strat='area')
import json
json.dump(dict(fish_old=r0, fish_clean=r1, who_old=s0, who_clean=s1, who_clean_area=s2), open(f'{OUT}/r03.json', 'w'), default=float, indent=1)
