#!/usr/bin/env python3
"""Recheck 14 (added by the coordinator): jobs/out/chits.md.
  (a) seals of comb-chit names end in the comb: 5 of 60 against 0.80 (chits_2_names.py)
  (b) names carried with two endings, comb + man: 4 against 17.71; jar-only + comb 33 against 66.13; jar-only + man
      14 against 33.97 (chits_1_titles.py)

Plain words: COMB CHIT = a Harappa tablet ending jar 740 + comb 400. A NAME is the signs before the jar. ENDING = what
follows the jar (nothing = jar only, 400 comb, 090 man ...). CHANCE = endings dealt among objects of the same site
(and object kind). COPY EVENT = all objects of one site + area + full text (moulded or batch-made copies) counted once.

Checks: (1) faces as objects (the old scripts keep one row per object and ending: fine); (2) the deal pool; (c)
batches of identical tablets: in the deal, each copy carries its ending to a different name, so 20 identical comb
tablets spread the comb over up to 20 names by chance while in the data they are one name: the chance figure for
"names with two endings" is pushed up.
Run: python3 recheck_14_chits.py   (about 1-2 minutes)
"""
import sys, io, contextlib, collections
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
import numpy as np, pandas as pd
from recheck_common import *
say = log_to(f'{OUT}/r14_log.txt')
with contextlib.redirect_stdout(io.StringIO()):
    from chits_common import load, name_rows
    O = load(); N = name_rows(O)
f2s, _ = stone_map(); o2s = {k.split('.')[0]: v for k, v in f2s.items()}
N['stone'] = N.obj.astype(str).map(lambda o: o2s.get(o, o))
full = O.set_index('obj').sig.to_dict() if 'sig' in O else {}
N['full'] = N.obj.map(full).fillna(N.text)
rng = np.random.default_rng(22)
say(f'jar faces {len(N)} on {N.obj.nunique()} objects; stones {N.stone.nunique()}')

# ---------------- (a) ----------------
say('\n(a) comb-chit names: their seals end in the comb (old 5 of 60 against 0.80)')
HT = N[(N.site == 'Harappa') & (N.kind == 'mtab') & ~N.lost & (N.name != '')]
def run_a(SE, label):
    hit = sorted(set(HT[HT.after == '400'].name) & set(SE.name))
    S = SE[SE.name.isin(hit)]; obs = int((S.after == '400').sum())
    SEi = SE.reset_index(drop=True); grp = SEi.groupby('site').indices; msk = SEi.name.isin(hit).values
    nul = []
    for _ in range(4000):
        a = SEi.after.values.copy()
        for g_, ix in grp.items(): a[ix] = rng.permutation(a[ix])
        nul.append(int((a[msk] == '400').sum()))
    nul = np.array(nul)
    say(f'  {label}: {obs} of {len(S)} seals end in the comb against {nul.mean():.2f} (P {pvalue_hi(nul, obs):.4f}); comb seals: '
        + ', '.join(f'{r.cisi} ({r.area or "-"})' for r in S[S.after == "400"].itertuples()))
    return obs, len(S), nul.mean(), pvalue_hi(nul, obs)
SE0 = N[(N.kind == 'seal') & ~N.lost & (N.name != '')].drop_duplicates('obj')
a0 = run_a(SE0, 'A  as run (one row per seal object)')
SE1 = SE0.drop_duplicates('stone').drop_duplicates(['site', 'area', 'full'])
a1 = run_a(SE1, f'B  clean: identical seals of one site + area once ({len(SE0) - len(SE1)} removed)')

# ---------------- (b) ----------------
say('\n(b) names carried with two endings (old comb+man 4 against 17.71; jar+comb 33 against 66.13; jar+man 14 against 33.97)')
def shared(df):
    g = df.groupby('name').after.apply(set); out = collections.Counter()
    for s in g:
        s = sorted(s)
        for i in range(len(s)):
            for j in range(i + 1, len(s)): out[(s[i] or 'jar', s[j] or 'jar')] += 1
    return out
KEYS = [('090', '400'), ('jar', '400'), ('jar', '090')]
def run_b(NN, label):
    NN = NN.reset_index(drop=True); obs = shared(NN); grp = NN.groupby(['site', 'kind']).indices
    null = {k: [] for k in KEYS}
    for it in range(2000):
        a = NN.after.values.copy()
        for g_, ix in grp.items(): a[ix] = rng.permutation(a[ix])
        s = shared(NN.assign(after=a))
        for k in KEYS: null[k].append(s.get(k, 0))
    out = {}
    for k in KEYS:
        nv = np.array(null[k]); o = obs.get(k, 0)
        say(f'  {label} {k[0]}+{k[1]}: {o} names against {nv.mean():.2f} (P low {pvalue_lo(nv, o):.4f})')
        out['+'.join(k)] = (o, nv.mean(), pvalue_lo(nv, o))
    return out
NO = N.drop_duplicates(['obj', 'after'])
NN0 = NO[~NO.lost & (NO.name != '')]
b0 = run_b(NN0, 'A  as run (objects)')
NN1 = NN0.drop_duplicates(['stone', 'after']).drop_duplicates(['site', 'area', 'full', 'after'])
say(f'  copy events: {len(NN0)} object rows -> {len(NN1)}')
b1 = run_b(NN1, 'B  clean (copies of one site + area once)')
import json
json.dump(dict(a=[a0, a1], b=[b0, b1]), open(f'{OUT}/r14.json', 'w'), default=float, indent=1)
