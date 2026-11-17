#!/usr/bin/env python3
"""CLASH 335: A = ur "town" against B = kuTu "bin, grain receptacle" (DEDR 1883).

PREDICTIONS, written before this script was first run.  Honest note: the first-catalogue profile of 335 (tablets 62%,
grain header 413 on 15 of 21 tablet lines, jar 12 / maka 8 after it, 575 before and 711 after) was printed in
eight_signs.md and sound_list_v4.md and I had read it; so the first-catalogue numbers are not clean.  The new texts
(6 faces carry 335) were never used to choose a value, so that column is the clean one, but it is tiny.
'high'/'low' = more / less often than ANY sign does it, in the same catalogue.

 id  what is counted                                           A (town)   B (bin)
 K1  a count sign right before or after 335                    low        high     (a bin is a counted container: chest 590 22%, 575 32%)
 K2  a tall-stroke (container series) count right beside it    low        high     (pot 711: 71%)
 K3  face is a tablet (miniature or copper)                    low        high     (stores / accounts)
 K4  grain header 413 on the face                              low        high
 K5  a cup / pot / measure word on the face (700 711 320 171 540 705 706) high? no: A low, B high
 K6  a trade / price / tax word on the face (892 824 890 055 175 176)      A high     B low  (a town is where goods come from or go to)
 K7  jar 740 or maka 760/752 right after it                    high       low      (town as the name part "of X-town's house / child of X-town"; a thing in a goods line is not owned)
 K8  Mohenjo-daro house-mates share it                          low        high     (a house emblem repeats inside a house; a town does not mark a house)
 K9  Harappa objects from mound F (granary area)                low        high     (416 and 605 sit there)
 K10 right after 575 the slot is filled by a house/place word (740 741 742 745 803) rather than a container word (590 605 711 540 705 226 595): A high B low
 K11 335 is a goods-line word with one fixed neighbour pair: distinct texts that carry it, compared with faces (copy inflation check, reported, no side)
Decision rule: a test counts for a word when the observed direction matches it and P <= 0.1; 'direction only' otherwise.
Each test is run on faces and on distinct texts, first catalogue (L) and new texts (Mu).
Outputs: work_data/clash/335_tests.csv
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clash_common import *

S = '335'
NAMES = {'A': 'ur town', 'B': 'kuTu bin', 'none': '-'}
MEAS = {'700', '711', '320', '171', '540', '705', '706'}
TRADE = {'892', '824', '890', '055', '175', '176'}
TAB = ('mtab', 'ctab')
CONT = {'590', '605', '711', '540', '705', '226', '595'}
PLACE = {'740', '741', '742', '745', '803'}

tests = [
    ('K1', 'count sign right before/after', lambda r, i: (i > 0 and r.tok[i - 1] in CNTS) or (i + 1 < len(r.tok) and r.tok[i + 1] in CNTS), 'occ', dict(A='low', B='high')),
    ('K2', 'tall-stroke count right before/after', lambda r, i: (i > 0 and r.tok[i - 1] in TALL) or (i + 1 < len(r.tok) and r.tok[i + 1] in TALL), 'occ', dict(A='low', B='high')),
    ('K3', 'face is a tablet', lambda r, i: r.kind in TAB, 'face', dict(A='low', B='high')),
    ('K4', 'grain header 413 on the face', lambda r, i: '413' in r.tok, 'face', dict(A='low', B='high')),
    ('K5', 'cup/pot/measure word on the face', lambda r, i: bool(MEAS & set(r.tok)), 'face', dict(A='low', B='high')),
    ('K6', 'trade/price/tax word on the face', lambda r, i: bool(TRADE & set(r.tok)), 'face', dict(A='high', B='low')),
    ('K7', 'jar or maka right after', lambda r, i: i + 1 < len(r.tok) and r.tok[i + 1] in ('740', '760', '752'), 'occ', dict(A='high', B='low')),
]
rows = []
print('[clash_335] running tests ...', flush=True)
for tag, lab, fn, scope, says in tests:
    for cat in ('L', 'Mu'):
        for unit in ('faces', 'distinct'):
            res = occ_test(S, fn, cat, unit, scope)
            r = line(tag, lab, says, res, NAMES); r['catalogue'] = cat; r['unit'] = unit
            rows.append(r)

# K8: house-mates (Mohenjo-daro seals; first catalogue only, uses the shared shuffle test)
hs = house_share(S, where='any', seals=False)
print('K8 house_share:', hs, flush=True)
rows.append(dict(test='K8', what='Mohenjo-daro house-mates share it', k='', n='', share='', base='', P=f'{hs[1]:.2g}' if hs else '',
                 points_to=('kuTu bin' if hs and hs[0] and hs[1] <= 0.1 else 'ur town (no repeat)' if hs else 'no uses'),
                 strength=hs[2] if hs else '', catalogue='L', unit='objects'))

# K9: Harappa mound F share
def mound(r, pre): return str(r.area).startswith(pre)
res = occ_test(S, lambda r, i: mound(r, 'F'), 'L', 'faces', 'face', sub=lambda r: r.site == 'Harappa')
rr = line('K9', 'Harappa faces from mound F', dict(A='low', B='high'), res, NAMES); rr.update(catalogue='L', unit='faces'); rows.append(rr)
for pre in ('E', 'AB'):
    res = occ_test(S, lambda r, i, p=pre: mound(r, p), 'L', 'faces', 'face', sub=lambda r: r.site == 'Harappa')
    rr = line('K9-' + pre, f'Harappa faces from mound {pre} (reported, no side)', dict(A='low', B='high'), res, NAMES); rr.update(catalogue='L', unit='faces'); rows.append(rr)

# K10: slot after 575
cnt = collections.Counter()
for r in FACES[FACES.cat.isin(['L', 'Mu'])].drop_duplicates('tok').itertuples():
    for i, t in enumerate(r.tok[:-1]):
        if t == '575': cnt[r.tok[i + 1]] += 1
pl = sum(v for s, v in cnt.items() if s in PLACE); co = sum(v for s, v in cnt.items() if s in CONT)
print('K10 slot after 575 (distinct texts, both catalogues):', dict(cnt.most_common(12)), 'place-class', pl, 'container-class', co, flush=True)
rows.append(dict(test='K10', what='slot after 575: place-class vs container-class fillers (distinct texts)', k=pl, n=pl + co, share=f'{pl}/{pl + co}',
                 base='', P='', points_to='ur town' if pl > co else 'kuTu bin', strength='count only', catalogue='L+Mu', unit='distinct'))

# K11 copy inflation
n_faces = int(sum(S in r.tok for r in FACES[FACES.cat == 'L'].itertuples())); n_dist = len({r.tok for r in FACES[FACES.cat == 'L'].itertuples() if S in r.tok})
print(f'K11 335 faces in L {n_faces}, distinct texts {n_dist}', flush=True)
rows.append(dict(test='K11', what='copy inflation: faces / distinct texts', k=n_faces, n=n_dist, share='', base='', P='', points_to='-', strength='report', catalogue='L', unit=''))

df = pd.DataFrame(rows)
df.to_csv(f'{OUTC}/335_tests.csv', index=False)
print(df[['test', 'what', 'catalogue', 'unit', 'k', 'n', 'share', 'base', 'P', 'points_to', 'strength']].to_string(index=False))

# tally: distinct-text rows plus tablet-type mix
t = df[(df.unit == 'distinct') & (df.strength == 'P<=0.1')]
print('\nTALLY distinct texts, P<=0.1:', t.groupby('points_to').size().to_dict())
t = df[(df.unit == 'faces') & (df.strength == 'P<=0.1')]
print('TALLY faces, P<=0.1:', t.groupby('points_to').size().to_dict())
t = df[(df.catalogue == 'Mu') & (df.strength.isin(['P<=0.1', 'direction only']))]
print('NEW TEXTS, any direction:', t.groupby('points_to').size().to_dict(), flush=True)

# K12 (added after the run above; post hoc, labelled so): the two roles of 335 split apart.
# role G = 335 right after 575 (the grain-line formula); role N = every other use of 335.
print('\nK12 (post hoc) role split, distinct texts, both catalogues', flush=True)
G, N_ = [], []
for r in FACES.drop_duplicates('tok').itertuples():
    for i, t in enumerate(r.tok):
        if t == S: (G if i > 0 and r.tok[i - 1] == '575' else N_).append((r, i))
def summ(L, nm):
    n = len(L)
    f = lambda c: sum(c(r, i) for r, i in L)
    print(f"  {nm}: uses {n}; tablet {f(lambda r,i: r.kind in TAB)}; 413 on face {f(lambda r,i: '413' in r.tok)}; cup/measure word {f(lambda r,i: bool(MEAS & set(r.tok)))}; "
          f"jar/maka right after {f(lambda r,i: i+1<len(r.tok) and r.tok[i+1] in ('740','760','752'))}; 711 right after {f(lambda r,i: i+1<len(r.tok) and r.tok[i+1]=='711')}; "
          f"seal {f(lambda r,i: r.kind=='seal')}; sites {sorted({r.site for r,i in L})}", flush=True)
summ(G, 'G (575-335 grain-line role)'); summ(N_, 'N (all other uses)')
