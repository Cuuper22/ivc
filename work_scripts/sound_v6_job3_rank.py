#!/usr/bin/env python3
"""Job 3, step 1: the next 25 signs by how many more complete faces each alone would let read whole (gain) under the
sixth wide list after jobs 1-2; for each, ONLY the picture (shape description, second-catalogue sign) and the slot
(first / middle / last share, how often counted, how often right before the jar) are printed, nothing else.
Writes work_data/sound_v6/gains_v6.csv."""
from sound_v6_common import *
from sound_v6_values import V6, TIER6
T = {s: t for s, t in TIER6.items()}
g, gd, gs = gains(T)
cw = pd.read_csv(f'{ROOT}/work_data/lipi_mahadevan_crosswalk.csv', dtype=str)
mm = cw.groupby('lipi').mahadevan.apply(lambda s: '/'.join(s)).to_dict()
rows = []
for s, n in g.most_common():
    if s in V6: continue
    rows.append(dict(sign=s, gain_faces=n, gain_distinct=len(gd[s]), gain_seals=gs[s], shape=SH.get(s, ''), mahadevan=mm.get(s, '')))
G = pd.DataFrame(rows); G.to_csv(f'{OUT6}/gains_v6.csv', index=False)
top = G.head(25)
for r in top.itertuples():
    pos = collections.Counter(); cnt = jar = n = 0
    for x, P, st, gg in faces_all('LM'):
        for i, a in enumerate(x):
            if a != r.sign: continue
            n += 1; pos['first' if i == 0 else 'last' if i == len(x) - 1 else 'mid'] += 1
            cnt += (i > 0 and x[i - 1] in VAL) or (i + 1 < len(x) and x[i + 1] in VAL)
            jar += i + 1 < len(x) and x[i + 1] == '740'
    print(f'{r.sign} gain {r.gain_faces} faces ({r.gain_distinct} distinct, {r.gain_seals} seals) | M{r.mahadevan} | {r.shape[:90]} | uses {n}: first {pos["first"]} mid {pos["mid"]} last {pos["last"]}; counted {cnt}; before jar {jar}')
