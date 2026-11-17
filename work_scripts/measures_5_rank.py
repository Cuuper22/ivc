#!/usr/bin/env python3
"""Rescue for the pay-scale order (went against: monthly cups do not follow rank).
PREDICTION (written before the run): rank lives in the kalam count, not in the monthly cup ration. Seals naming
5 kalam are bigger than seals naming 3 kalam (median face area), and the 3-kalam seals bigger than seals with a
bare cup count; the chief sign 520 follows 3 kalam, a higher title or the jar-man ending follows 5 kalam."""
from measures_common import *
s = d[d.kind == 'seal'].copy()
s['A'] = pd.to_numeric(s['horizontal(mm)'], errors='coerce') * pd.to_numeric(s['vertical(mm)'], errors='coerce')
def kal(t):
    for (a, b, v, ser) in runs(t):
        if a > 0 and t[a - 1] in ('705', '706') and v and 'F' in ser: return v
    return None
s['kal'] = s.tok.apply(lambda t: kal(list(t)))
s['n'] = s.tok.apply(len)
allmed = s[s.A > 0].A.median()
for v, g in s[s.kal.notna()].groupby('kal'):
    g2 = g[g.A > 0]
    nxt = collections.Counter()
    for t in g.tok:
        t = list(t)
        for (a, b, vv, ser) in runs(t):
            if a > 0 and t[a - 1] in ('705', '706'): nxt[t[b] if b < len(t) else 'END'] += 1
    print(f'kalam {int(v)}: seals {len(g)}, measured {len(g2)}, median face {g2.A.median():.0f} mm2 (all seals {allmed:.0f}), '
          f'median length {g.n.median()}, after the count: {dict(nxt.most_common(5))}')
    if v == 5: print('   ', [(r.cisi, ' '.join(r.tok), r.A) for r in g.itertuples()])
