#!/usr/bin/env python3
"""How many complete texts are fully sounded (every sign a number, a base value or a 'building' value) under the
second list and the third list, for all objects and for goods objects (everything that is not a seal).
Lipi faces, distinct texts and objects.  Writes work_data/sound_v3/coverage.csv."""
import csv
from sound_v3_common import *
from sound_v3_values import TIER3, OLDTIER
rows = []
for name, T, allow in [('second list', OLDTIER, ('base', 'building')), ('third list', TIER3, ('base', 'building')),
                       ('third list incl. testing', TIER3, ('base', 'building', 'testing'))]:
    ok = lambda x: len(x) >= 2 and '000' not in x and 'ALT' not in x and all(a in VAL or T.get(a) in allow for a in x)
    for grp, m in [('all objects', d.complete_txt), ('goods objects (not seals)', d.complete_txt & (d.kind != 'seal'))]:
        sub = d[m]; hit = sub.tok.apply(ok)
        rows.append(dict(list=name, group=grp, faces=int(hit.sum()), of_faces=len(sub), distinct=len(set(sub.tok[hit])), of_distinct=len(set(sub.tok)),
                         objects=sub[hit].obj.nunique()))
df = pd.DataFrame(rows); print(df.to_string(index=False)); df.to_csv(f'{OUT3}/coverage.csv', index=False)
