#!/usr/bin/env python3
"""Rescue for lead (b), written after the first run gave 8 of 14 distinct texts (shuffle 6.0, P 0.19).
Redesign, prediction written before rerunning: a person count is only a count standing right before a person sign
that is NOT itself followed by the jar 740 (a sign + jar is a house name: "of the one-Tax house"), not the opener
861-002 ("two shares") at the start of a face, and not a count that stands right after a kalam sign 705/706
(that is a kalam count). With heads counted this way, distinct texts multiply to 6 or 12 in most cases.
New idea tried beside it: the product is a whole number of paTi-days (cups x 8 x heads divisible by 30 = a month)?"""
import collections
from measures_common import *
rng2 = np.random.default_rng(9)
C = pd.read_csv(f'{OUTM}/m2_crew.csv', dtype=str)
PEOPLE = {'817', '861', '156', '154', '151', '158', '140', '142', '176', '097', '137', '100', '090'}
rows = []
for r in C.itertuples():
    faces = [tuple(f.split('-')) for f in r.text.split(' | ')]
    cups, ppl = [], []
    for t in faces:
        for (a, b, v, s) in runs(t):
            if not v: continue
            right = t[b] if b < len(t) else 'END'; left = t[a - 1] if a else 'START'
            if left in ('705', '706'): continue
            if right == '700': cups.append(v); continue
            if right in PEOPLE and not (b + 1 < len(t) and t[b + 1] == '740'): ppl.append((v, right))
            elif right == 'END' and left in PEOPLE and not (left == '861' and a == 1): ppl.append((v, left))
    if cups and ppl: rows.append(dict(obj=r.obj, text=r.text, cup=cups[0], person=ppl[0][0], who=ppl[0][1], prod=cups[0] * ppl[0][0]))
R = pd.DataFrame(rows); R['hit'] = R['prod'].isin([6, 12]); R.to_csv(f'{OUTM}/m2_crew_rescue.csv', index=False)
for lab, df in [('all tablets', R), ('distinct texts', R.drop_duplicates('text'))]:
    k = np.array([np.isin(rng2.permutation(df.cup.values) * df.person.values, [6, 12]).sum() for _ in range(20000)])
    print(f'{lab}: {df.hit.sum()} of {len(df)} multiply to 6 or 12; shuffled {k.mean():.1f}; P {(k >= df.hit.sum()).mean():.4f}')
print(R.drop_duplicates('text').to_string())
print('products (all tablets):', collections.Counter(R['prod']).most_common())
