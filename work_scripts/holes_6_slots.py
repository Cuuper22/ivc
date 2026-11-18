#!/usr/bin/env python3
"""One row per hole sign: every slot, counts before/after, jar, object kinds, sites, neighbours, second-catalogue partner.  -> work_data/holes/slots_eight.csv"""
import sys, collections
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from holes_common import *
import pandas as pd
ls = lines(True)
cw = pd.read_csv(f'{ROOT}/work_data/lipi_mahadevan_crosswalk.csv', dtype=str)
M = mah_lines()
rows = []
for sg in EIGHT + ['526', '527', '705', '706', '435']:
    U = uses(sg, ls); n = len(U)
    pos = collections.Counter(); cb = ca = bj = jl = 0
    K = collections.Counter(); S = collections.Counter(); L_ = collections.Counter(); R_ = collections.Counter()
    for i, p in U:
        t = ls[i]['toks']; m = len(t)
        pos['alone' if m == 1 else 'first' if p == 0 else 'last' if p == m - 1 else 'inner'] += 1
        cb += p > 0 and t[p - 1] in CNT; ca += p + 1 < m and t[p + 1] in CNT
        bj += p + 1 < m and t[p + 1] in ('740', '741', '742', '745'); jl += '740' in t[p + 1:]
        K[kind(ls[i]['type'])] += 1; S[ls[i]['site']] += 1
        L_[t[p - 1] if p else '^'] += 1; R_[t[p + 1] if p + 1 < m else '$'] += 1
    mp = [int(x) for x in cw[cw.lipi == sg].mahadevan]
    mu = sum(1 for r in M for s in r['toks'] if s in mp)
    f = lambda c, k=3: '; '.join(f'{a}[{snd(a) or "?"}] {b}' for a, b in c.most_common(k))
    rows.append(dict(sign=sg, uses=n, objects=len({ls[i]['obj'] for i, _ in U}), first=pos['first'], inner=pos['inner'], last=pos['last'], alone=pos['alone'],
                     count_before=cb, count_after=ca, next_is_jar_or_ward_jar=bj, jar_later_in_line=jl,
                     kinds='; '.join(f'{k} {v}' for k, v in K.most_common(4)), sites='; '.join(f'{k} {v}' for k, v in S.most_common(4)),
                     left_top3=f(L_), right_top3=f(R_), mahadevan_partner=mp, mahadevan_uses=mu))
d = pd.DataFrame(rows); d.to_csv(f'{HOLES}/slots_eight.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 70)
print(d.drop(columns=['left_top3', 'right_top3']).to_string())
