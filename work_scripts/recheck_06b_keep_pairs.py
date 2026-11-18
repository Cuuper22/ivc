#!/usr/bin/env python3
"""Recheck 6, add-on: which name faces carry the 38 same-amount pairs of 'a name keeps its own amount' (units =
(name, amount, trench)), and what is left when each name gives at most one same-amount pair per site.
Run: python3 recheck_06b_keep_pairs.py (seconds)"""
import sys, collections
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
import pandas as pd
from recheck_common import *
say = log_to(f'{OUT}/r06b_log.txt')
f2s, _ = stone_map(); o2s = {k.split('.')[0]: v for k, v in f2s.items()}
O = pd.read_csv(f'{ROOT}/work_data/spots/s3_objects.csv', dtype={'obj': str}).fillna('')
O['stone'] = O.obj.map(o2s); O = O.drop_duplicates('stone')
N = O[(O.types == 'amount+name') & (O.lostfree) & (O.name_face != '') & (O.amt_face != '')].copy()
N['place'] = N.site + '|' + N.area
T = N.drop_duplicates(['name_face', 'amt_face', 'place'])
c = collections.Counter()
for (n, a), g in T.groupby(['name_face', 'amt_face']):
    k = len(g); c[(n, a, ','.join(sorted(set(g.site))))] += k * (k - 1) // 2
say('same-amount pairs by (name face, amount face): ' + '; '.join(f'{n} + {a} [{s}] {v}' for (n, a, s), v in c.most_common() if v))
