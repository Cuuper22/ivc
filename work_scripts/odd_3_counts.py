#!/usr/bin/env python3
"""Step 3a: which neighbour does a count belong to? For every run of stroke signs, record the stroke style (short 001-007, stacked
012-018, tall 031-036) and the signs beside it. Per sign: how often each style stands right AFTER it (sign then count: a measure
word taking its count) or right BEFORE it (count then thing). Prediction written first: tall strokes follow measure signs
(700, 705, 320, 575, 540, 171, 711, 061, 817?) and precede counted containers; short and stacked strokes precede the counted thing.
Output work_data/odd/count_sides.csv"""
from odd_common import *
F = faces()
after = collections.defaultdict(collections.Counter); before = collections.defaultdict(collections.Counter)
tot = collections.Counter()
for f in F:
    x = f['x']; n = len(x); i = 0
    while i < n:
        if x[i] in CNT:
            j = i
            while j + 1 < n and x[j+1] in CNT: j += 1
            sty = {stype(a) for a in x[i:j+1]}; sty = sty.pop() if len(sty) == 1 else 'mixed'
            if sty == 'mixed' and any(a in CNT and CNT[a][0] == 'comb' for a in x[i:j+1]): sty = 'comb'
            tot[sty] += 1
            if i > 0 and x[i-1] not in CNT: after[x[i-1]][sty] += 1      # run stands AFTER sign x[i-1]
            if j + 1 < n and x[j+1] not in CNT: before[x[j+1]][sty] += 1  # run stands BEFORE sign x[j+1]
            i = j + 1
        else: i += 1
print('runs by style:', dict(tot))
rows = []
for t in set(after) | set(before):
    a = after[t]; b = before[t]
    rows.append(dict(sign=t, a_short=a['short']+a['stacked'], a_tall=a['tall'], b_short=b['short']+b['stacked'], b_tall=b['tall'], n=sum(a.values())+sum(b.values())))
R = pd.DataFrame(rows).sort_values('n', ascending=False); R.to_csv(f'{OUT}/count_sides.csv', index=False)
print(R.head(45).to_string())
