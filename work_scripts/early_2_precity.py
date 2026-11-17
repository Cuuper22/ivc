#!/usr/bin/env python3
"""EARLY job, step 2: writing before the cities. What do the inscribed objects from Early Harappan levels carry?

PLAIN WORDS
- Pre-city set = every object in the first catalogue that the dating of the history job puts before the Mature city phase
  (Harappa Periods 1 and 2, ca. 3300-2600 BC, and Dholavira stages I and II, ca. 2650-2500 BC), plus the three objects that the
  catalogue itself labels Early at other sites (Rehman Dheri `Rhd-1` period I and `Rhd-269` 'Early'; Kalibangan `K-94`, period I,
  which the catalogue maps to Harappa Period 3A). The second catalogue has no period field, so it adds nothing here.
- A sign's CLASS: NUMBER = a stroke sign (short strokes 001-007, stacked, tall strokes 031-036, the A-comb series);
  MEASURE = the cup 700; HOUSE = the jar 740 ("house of") or a fish sign (the crest signs); GOODS = grain 413, wheat shaft 411,
  tree 390 (cotton), produce 806; OTHER = the rest (unnamed shapes, e.g. 697, 698, 893 have no drawing in the sign table).
- The "later" comparison group is the same kind of object (pots with the same catalogue type) from the cities, so a change in the
  kind of object is not what is being measured.

PREDICTIONS (written before this script was run):
 P1  most pre-city objects (60% or more) carry a number stroke, alone or with one other sign (counting comes first).
 P2  a house word (jar or fish) is rare before the cities (under 15% of objects) and rises through the periods.
 P3  goods signs (grain, wheat shaft, tree) already stand on at least three pre-city objects, almost always with a number or alone,
     never with a jar.
 P4  the cup 700 is the only measure sign present before the cities.
 P5  texts are one sign long on at least half of the pre-city objects; a text of 5 or more signs appears only on the Dholavira seal.
Outputs: work_data/early/precity_objects.csv, precity_classes.csv, log_2.txt
"""
import sys, os, io, contextlib, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    from time_common import *
from scipy.stats import fisher_exact

OUTE = f'{ROOT}/work_data/early'
os.makedirs(OUTE, exist_ok=True)
SH = pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv', dtype=str).set_index('lipi_wells_number').shape_description.to_dict()
FISHSET = {'220', '226', '231', '233', '235', '236', '240', '241'}
GOODS = {'413': 'grain', '411': 'wheat shaft', '390': 'tree (cotton)', '806': 'produce'}


def klass(s):
    if s in NUM: return 'number'
    if s == '700': return 'measure'
    if s == '740': return 'house'
    if s in FISHSET: return 'house'
    if s in GOODS: return 'goods'
    if s in ('000', 'ALT'): return 'lost'
    return 'other'


T['txt'] = T.faces.apply(lambda fs: ' | '.join('-'.join(f) for f in fs))
T['toks'] = T.faces.apply(lambda fs: [a for f in fs for a in f])
extra_ids = {'Rhd-1', 'Rhd-269', 'K-94'}
pre = T[(T['rank'] == 0) | T.cisi.isin(extra_ids) | ((T.site == 'Rahman-deri') & (T.period.astype(str).str.strip().isin(['I', 'Early'])))].copy()
pre = pre[~pre.index.duplicated()]
pre['group'] = np.where(pre['rank'] == 0, 'Harappa/Dholavira before the cities', 'other Early Harappan label')


def sign_counts(tk):
    ks = [klass(a) for a in tk]
    return dict(n_signs=len([a for a in tk if a not in ('000', 'ALT')]), number=ks.count('number'), measure=ks.count('measure'),
                house=ks.count('house'), goods=ks.count('goods'), other=ks.count('other'), lost=ks.count('lost'),
                has_jar='740' in tk, has_fish=any(a in FISHSET for a in tk), has_marked=any(a in MARKED for a in tk))


rows = []
for o, r in pre.iterrows():
    p = sign_counts(r.toks); p.update(obj=o, cisi=r.cisi, site=r.site, kind=r.kind, period=r.period if r.time == '-' else r.time, group=r.group, text=r.txt)
    rows.append(p)
P = pd.DataFrame(rows)
P['class'] = np.select([(P.number + P.measure > 0) & (P.house == 0) & (P.goods == 0) & (P.other == 0),
                        (P.house > 0), (P.goods > 0), (P.number + P.measure > 0)],
                       ['counting only', 'carries a house word', 'carries a goods sign', 'counting + unnamed sign'], 'unnamed sign(s) only')
P.to_csv(f'{OUTE}/precity_objects.csv', index=False)

print(f'PRE-CITY SET: {len(P)} objects: {P.group.value_counts().to_dict()}; kinds {P.kind.value_counts().to_dict()}; sites {P.site.value_counts().to_dict()}')
print('signs per object:', dict(sorted(collections.Counter(P.n_signs).items())))
print('\nEVERY OBJECT')
print(P[['cisi', 'site', 'kind', 'period', 'text', 'class']].sort_values(['site', 'period']).to_string(index=False))
print('\nCLASS COUNTS'); print(P['class'].value_counts().to_string())
tot = len(P)
for k in ['number', 'measure', 'house', 'goods', 'other']:
    print(f'  objects with a {k} sign: {int((P[k] > 0).sum())} of {tot}')
print(f'  with a jar: {int(P.has_jar.sum())}; with any fish sign: {int(P.has_fish.sum())}; with a marked fish crest: {int(P.has_marked.sum())}')
c = collections.Counter(a for t in P.text for a in t.replace(' | ', '-').split('-') if a not in ('000', 'ALT'))
print('SIGNS in the pre-city set (count, class, shape):')
for s, n in c.most_common():
    print(f'   {s}  x{n:<3d} {klass(s):8s} {SH.get(s, "(no drawing in the sign table)")[:80]}')
nm = collections.Counter(a for t in P.text for a in t.replace(' | ', '-').split('-') if a in NUM)
print('number signs by value series:', dict(nm))

# ---- the same measures through the periods, pots against pots (same catalogue kind), and all objects
D2 = T[T['rank'].notna()].copy()
D2['stage'] = pd.cut(D2['rank'], [-1, 0, 3, 6, 20], labels=['before cities (P1-2)', '3A-3B (2600-2200)', '3B/C-3C-2', '3C-3 and later'])
for k in ['all objects', 'pots', 'tablets (mtab)', 'seals']:
    sub = D2 if k == 'all objects' else D2[D2.kind == {'pots': 'pot', 'tablets (mtab)': 'mtab', 'seals': 'seal'}[k]]
    print(f'\n{k}: share of objects with ...')
    out = []
    for st, g in sub.groupby('stage', observed=True):
        tk = g.toks
        out.append(dict(stage=st, n=len(g), one_sign=int((tk.apply(lambda t: len([a for a in t if a not in ('000', 'ALT')])) == 1).sum()),
                        number=int(tk.apply(lambda t: any(a in NUM for a in t)).sum()), cup=int(tk.apply(lambda t: '700' in t).sum()),
                        jar=int(tk.apply(lambda t: '740' in t).sum()), fish=int(tk.apply(lambda t: any(a in FISHSET for a in t)).sum()),
                        marked=int(tk.apply(lambda t: any(a in MARKED for a in t)).sum()), goods=int(tk.apply(lambda t: any(a in GOODS for a in t)).sum()),
                        five_plus=int((tk.apply(lambda t: len([a for a in t if a not in ('000', 'ALT')])) >= 5).sum())))
    O = pd.DataFrame(out); print(O.to_string(index=False)); O.to_csv(f'{OUTE}/precity_stage_{k.split()[0]}.csv', index=False)


def fe(sub_a, sub_b, f, lab):
    a = int(sub_a.apply(f).sum()); b = int(sub_b.apply(f).sum())
    t = [[a, len(sub_a) - a], [b, len(sub_b) - b]]
    print(f'  {lab}: before cities {a}/{len(sub_a)} against later {b}/{len(sub_b)}; Fisher P {fisher_exact(t)[1]:.3g}')


pp = D2[(D2.kind == 'pot')]
pa, pb = pp[pp['rank'] == 0].toks, pp[pp['rank'] >= 1].toks
print('\nPOTS ONLY, before the cities against the cities')
fe(pa, pb, lambda t: any(a in NUM for a in t), 'a number stroke')
fe(pa, pb, lambda t: '740' in t, 'the jar')
fe(pa, pb, lambda t: any(a in FISHSET for a in t), 'a fish sign')
fe(pa, pb, lambda t: len([a for a in t if a not in ('000', 'ALT')]) == 1, 'a one-sign text')
fe(pa, pb, lambda t: any(a in GOODS for a in t), 'a goods sign')
aa, ab = D2[D2['rank'] == 0].toks, D2[D2['rank'] >= 1].toks
print('ALL OBJECT KINDS')
fe(aa, ab, lambda t: any(a in NUM for a in t), 'a number stroke')
fe(aa, ab, lambda t: '740' in t, 'the jar')
fe(aa, ab, lambda t: any(a in FISHSET for a in t), 'a fish sign')
fe(aa, ab, lambda t: any(a in MARKED for a in t), 'a marked fish crest')

# ---- order of first appearance of sign classes, by period rank, all sites
print('\nFIRST APPEARANCE OF SIGN CLASSES BY DATED PERIOD (all dated objects; rank 0 = before the cities)')
first = {}
for o, r in D2.sort_values('rank').iterrows():
    for a in set(r.toks):
        first.setdefault(a, (r['rank'], r.time, r.cisi, r.site))
for lab, sset in [('stroke numbers (short 001-007)', {f'{i:03d}' for i in range(1, 8)}), ('tall strokes 031-035', {f'{i:03d}' for i in range(31, 36)}),
                  ('cup 700', {'700'}), ('jar 740', {'740'}), ('plain fish 220', {'220'}), ('marked fish crests', MARKED), ('grain 413', {'413'}),
                  ('wheat shaft 411', {'411'}), ('tree 390', {'390'}), ('produce 806', {'806'}), ('diamond 817/861', {'817', '861'}), ('man 090', {'090'}),
                  ('spear 520', {'520'}), ('comb 400', {'400'}), ('cap 060/920', {'060', '920'}), ('child-of 760', {'760'}), ('kalam 705/706', {'705', '706'})]:
    got = sorted([first[a] for a in sset if a in first])
    print(f'  {lab:32s} earliest dated object: {got[0][1]} ({got[0][3]} {got[0][2]})' if got else f'  {lab:32s} none')
