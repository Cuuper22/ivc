#!/usr/bin/env python3
"""lang_m2 step 1: signs -> (blind picture nouns, machine class) -> units.  Rules in lang_m2_common.py header.
Output: work_data/lang_m2/signs.csv (every Lipi sign reached through a rank-1 crosswalk pair) and work_data/lang_m2/units.csv."""
import sys, os, csv, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lang_m2_common import *

cw = [r for r in csv.DictReader(open(f'{ROOT}/work_data/lipi_mahadevan_crosswalk.csv', encoding='utf-8')) if r['rank_for_lipi_sign'] == '1']
pb = {r['glyph']: r for r in csv.DictReader(open(f'{ROOT}/work_data/pictures/pictures_blind.csv', encoding='utf-8'))}
cl = {r['sign']: r['hmm10'] for r in csv.DictReader(open(f'{ROOT}/work_data/frame/classes.csv', encoding='utf-8')) if r['hmm10']}
uses = {r['sign']: r['uses_distinct_texts'] for r in csv.DictReader(open(f'{ROOT}/work_data/frame/classes.csv', encoding='utf-8'))}
cl.update(MOVES)
rows = []
for r in cw:
    p = pb.get(r['mahadevan']); c = cl.get(r['lipi'])
    rows.append(dict(sign=r['lipi'], mahadevan=r['mahadevan'], level=p['level'] if p else 'no drawing', nouns=p['agreed_things'] if p else '',
                     cls=c or '', uses=uses.get(r['lipi'], 0)))
with open(f'{OUT}/signs.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(f'rank-1 crosswalk pairs: {len(cw)} Lipi signs -> {len({r["mahadevan"] for r in cw})} drawings; levels',
      dict(collections.Counter(r['level'] for r in rows)))
urows = []
for v, lv in VARIANTS.items():
    us = collections.OrderedDict()
    for r in rows:
        if r['level'] in lv and r['cls'] and r['nouns']:
            us.setdefault(('|'.join(sorted(r['nouns'].split(';'))), r['cls']), []).append(r['sign'])
    for (ns, c), ss in us.items(): urows.append(dict(variant=v, nouns=ns, cls=c, cls_name=CLASSES[c][0], signs='/'.join(ss)))
    nsg = sum(len(s) for s in us.values())
    grp = collections.defaultdict(set)
    for ns, c in us: grp[ns].add(c)
    movable = sum(sum(1 for ns2, c in us if ns2 == ns) for ns, cs in grp.items() if len(cs) > 1)
    print(f'{v}: {nsg} signs, {len(us)} units, {len(grp)} noun sets; units in noun sets with 2+ classes (control 4 can move): {movable}; '
          f'classes {dict(collections.Counter(c for _, c in us))}')
with open(f'{OUT}/units.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(urows[0])); w.writeheader(); w.writerows(urows)
