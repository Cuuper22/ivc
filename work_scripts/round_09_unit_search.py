#!/usr/bin/env python3
"""ROUND SEALS, step 9 (new idea): where else does the unit [short stroke][person sign] live? Search all distinct non-round home texts of every object kind.
PREDICTION written after step 7 found it on 6 round texts: it lives almost nowhere else (home <= 5 of 3,400 distinct texts).
Short strokes = 001 002 003 004 005 055; person signs = 090 091 093 095. Output: log_9.txt
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abroad4_common import *
RL = set(pd.read_csv(f'{ROOT}/work_data/round/round_list.csv', dtype=str).id)
PERSON = {'090', '091', '093', '095'}; SHORT = {'001', '002', '003', '004', '005', '055'}
h = F[(F.tier == 'home') & (~F.id.isin(RL))]
seen = {}
for r in h.itertuples():
    if r.tok not in seen: seen[r.tok] = (r.kind, r.site, r.id)
hit = [(k, s, i, '-'.join(t)) for t, (k, s, i) in seen.items() if any(a in SHORT and b in PERSON for a, b in zip(t, t[1:]))]
print('distinct non-round home texts', len(seen), 'with [short][person]', len(hit)); [print(x) for x in hit]
hit2 = [(k, s, '-'.join(t)) for t, (k, s, i) in seen.items() if any(a in PERSON and b in SHORT for a, b in zip(t, t[1:]))]
print('reverse [person][short]', len(hit2), collections.Counter(k for k, _, _ in hit2))
