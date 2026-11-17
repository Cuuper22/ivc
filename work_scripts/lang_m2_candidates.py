#!/usr/bin/env python3
"""lang_m2 step 8: runs ONLY for a family whose summary row (primary variant) has clears_bar = True.
Candidates: units that hit in that family's pooled cells that beat all four controls; expected by chance = sum of those units'
hit rates under C3 in the same cells.  Decoy list (for a later blind check): for every candidate unit one REAL pairing (a picture
word and a sound-alike carrying the unit's class keyword, from evidence.csv; first listed) and one DECOY pairing (the whole picture word +
sound-alike pairing of another candidate unit of the same class, or of any class if none), rows
shuffled; the key file says which is which.  Nothing here is a value.
Output: work_data/lang_m2/candidates.csv, decoy_candidates.csv, decoy_key.csv"""
import sys, os, csv, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lang_m2_common import *
rng = np.random.default_rng(20261121)
S = [r for r in csv.DictReader(open(f'{OUT}/summary.csv', encoding='utf-8')) if r['variant'] == PRIMARY and r['clears_bar'] == 'True']
if not S:
    print('no family clears the bar: step 8 not run'); sys.exit(0)
G = list(csv.DictReader(open(f'{OUT}/grid.csv', encoding='utf-8')))
UH = list(csv.DictReader(open(f'{OUT}/unit_hits.csv', encoding='utf-8')))
EV = list(csv.DictReader(open(f'{OUT}/evidence.csv', encoding='utf-8')))
cand, dec, key = [], [], []
for s in S:
    fam = s['family']; names = FAMILIES[fam]
    cells = {(r['dist'], r['breadth']) for r in G if r['variant'] == PRIMARY and r['unit'] == f'FAMILY {fam}'
             and (r['share_all4'] == 'True' or r['hits_all4'] == 'True')}
    rows = [u for u in UH if u['variant'] == PRIMARY and u['family'] == fam and (u['dist'], u['breadth']) in cells]
    exp = sum(float(u['c3_hit_rate']) for u in rows); hit = [u for u in rows if u['real_hit'] == '1']
    print(f'{fam}: cells {sorted(cells)}; candidate unit-cells {len(hit)}, expected by chance {exp:.1f}')
    for u in hit: cand.append(dict(family=fam, expected_in_cells=round(exp, 2), **u))
    seen = collections.OrderedDict()
    for u in hit: seen.setdefault((u['nouns'], u['cls']), u)
    pool = collections.defaultdict(list)
    ev = [e for e in EV if e['dict'] in names]
    for (ns, c), u in seen.items():
        for e in ev:
            if e['noun'] in ns.split('|') and e['cls'] == c: pool[(ns, c)].append(e)
    keys = [k for k in seen if pool[k]]
    for i, k in enumerate(keys):
        real = pool[k][0]
        others = [k2 for k2 in keys if k2 != k and k2[1] == k[1]] or [k2 for k2 in keys if k2 != k]
        if not others: continue
        o = pool[others[rng.integers(len(others))]][0]
        pair = [('real', real), ('decoy', o)]
        for j in rng.permutation(2):
            kind, e = pair[j]; rid = f'{fam[:3]}{len(dec) + 1:03d}'
            dec.append(dict(id=rid, family=fam, signs=seen[k]['signs'], cls=k[1], cls_name=CLASSES[k[1]][0], proposed_word=e['picture_word'],
                            word_gloss=e['picture_gloss'], proposed_soundalike=e['soundalike'], soundalike_gloss=e['soundalike_gloss'],
                            dictionary=e['dict']))
            key.append(dict(id=rid, kind=kind))
for fn, data in (('candidates.csv', cand), ('decoy_candidates.csv', dec), ('decoy_key.csv', key)):
    if data:
        with open(f'{OUT}/{fn}', 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
print('written', len(cand), 'candidate unit-cells,', len(dec), 'decoy rows')
