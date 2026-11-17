#!/usr/bin/env python3
"""SPOTS lead 2, redesign of (a) and (d): location-only spread (does not depend on which family holds the sign).
Plain words: take the objects carrying a sign; count how many DIFFERENT blocks (or areas) they sit in. Compare with the
same number of named objects drawn at random from the same city (many thousand draws). More different places than
random draws = the sign's holders are spread out, one to a quarter; fewer = they cluster.
PREDICTION (written before running): 142 objects at Mohenjo-daro occupy more distinct blocks than random draws of the
same size (P high < 0.1); at least one other sign shows the same at P < 0.01 on 8+ located objects.
Writes work_data/spots/s2b_*.csv and s2b_log.txt.  Run: python3 spots_2b_spread.py (about 1 min)
"""
import os, random, collections
import numpy as np, pandas as pd
random.seed(5); np.random.seed(5)
ROOT = '/home/claude/ivc'; OUT = f'{ROOT}/work_data/spots'
LOG = open(f'{OUT}/s2b_log.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n')
A = pd.read_csv(f'{ROOT}/work_data/registry/names_all.csv', dtype=str).fillna('')
A = A[(A.damaged == 'False') & (A.goods_line == 'False')].drop_duplicates('object_id').copy()
A['sig'] = (A.opener + '-' + A.name_full + '-' + A.ending_signs).str.split('-')
N = 4000
def spread(S, pool_locs, lev):
    locs = list(S[lev]); k = len(locs); obs = len(set(locs))
    a = np.array([len(set(random.sample(pool_locs, k))) for _ in range(N)])
    return obs, k, a.mean(), (1 + (a >= obs).sum()) / (N + 1), (1 + (a <= obs).sum()) / (N + 1)
rows = []
for site in ('Mohenjo-daro', 'Harappa'):
    for lev in ('block', 'area_key'):
        pool = A[(A.site == site) & (A[lev] != '')]
        pl = list(pool[lev])
        for sg in ['142'] + ['061']:
            S = pool[pool.sig.map(lambda t: sg in t)]
            if len(S) < 4: continue
            o, k, m, ph, pl_ = spread(S, pl, lev)
            say(f'  {site:12s} {lev:8s} sign {sg}: {k} objects sit in {o} different places; random draws {m:.1f} (P more spread {ph:.3f}, P more clustered {pl_:.3f}); city has {len(set(pl))} places')
            rows.append(dict(site=site, level=lev, sign=sg, objects=k, places=o, random=m, P_spread=ph, P_cluster=pl_))
say('\nAll signs, Mohenjo-daro blocks (8+ located objects), spread P (more different blocks than random draws):')
pool = A[(A.site == 'Mohenjo-daro') & (A.block != '')]; pl = list(pool.block)
cnt = collections.Counter(s for t in pool.sig for s in set(t) if s and s not in ('000',) and not s.startswith('0') or s in ('061', '142'))
cnt = collections.Counter(s for t in pool.sig for s in set(t) if s and s != '000')
cands = [s for s, c in cnt.items() if c >= 8]
res = []
for s in cands:
    S = pool[pool.sig.map(lambda t: s in t)]
    o, k, m, ph, pc = spread(S, pl, 'block')
    res.append((s, k, o, m, ph, pc, S.house_key.nunique()))
R = pd.DataFrame(res, columns=['sign', 'objects', 'blocks', 'random', 'P_spread', 'P_cluster', 'crests']).sort_values('P_spread')
R.to_csv(f'{OUT}/s2b_signs_block.csv', index=False)
say(f'  signs tested {len(R)}; spread P<=0.05: {(R.P_spread <= 0.05).sum()}, <=0.01: {(R.P_spread <= 0.01).sum()}; cluster P<=0.05: {(R.P_cluster <= 0.05).sum()} (chance gives ~{0.05 * len(R):.1f} each)')
say(R.head(12).to_string(index=False)); say('  clustered most:'); say(R.sort_values('P_cluster').head(8).to_string(index=False))
LOG.close()
