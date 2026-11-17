#!/usr/bin/env python3
"""Recheck 6: tablets as issue chits (spots_3_records.py, spots_3b_rescue.py, stamps_5_more.py P7b).
  (i)   a name keeps its own amount: 38 pairs against 21.6 (P 0.003)
  (ii)  the same name with a different amount in one trench: 9 pairs against 3.5 (P 0.011)
  (iii) count-line seal and record pairs in one area with the same [number][thing]: 89 against 69.5 (P 0.003)

Plain words: a RECORD = an object with 2+ faces (mostly small tablets); NAME face / AMOUNT face = the face with a name,
the face with only numbers and measure signs. TRIPLE = (name face, amount face, trench). COUNT-LINE SEAL = a seal whose
whole text is a number and a counted thing (e.g. 033-700 = three tall strokes + cup). COPY EVENT = all objects of one
site and one trench with the same full text: counted once.

Checks: (1) faces counted as objects; (2) the shuffle pool; (c) moulded copies in one trench counted as many objects.
Run: python3 recheck_06_tablets.py   (about 2 minutes)
"""
import sys, re, collections
sys.path.insert(0, '/home/claude/ivc/work_scripts')
import numpy as np, pandas as pd
from recheck_common import *
say = log_to(f'{OUT}/r06_log.txt')
f2s, merges = stone_map()
o2s = {k.split('.')[0]: v for k, v in f2s.items()}
rng = np.random.default_rng(1)
O = pd.read_csv(f'{ROOT}/work_data/spots/s3_objects.csv', dtype={'obj': str}).fillna('')
O['stone'] = O.obj.map(o2s)
say(f'(i)-(ii) s3_objects.csv: {len(O)} rows = {O.obj.nunique()} objects (one row per object: faces already joined); '
    f'stones after merging duplicate catalogue rows {O.stone.nunique()}')
O = O.drop_duplicates('stone')
N = O[(O.types == 'amount+name') & (O.lostfree) & (O.name_face != '') & (O.amt_face != '')].copy()
N['place'] = N.site + '|' + N.area

def same_diff(df):
    s = d = 0
    for n, g in df.groupby('name_face'):
        a = list(g.amt_face)
        for i in range(len(a)):
            for j in range(i + 1, len(a)): s += a[i] == a[j]; d += a[i] != a[j]
    return s, d

def keep_test(T, label, nsh=3000):
    s0, d0 = same_diff(T); nl = []
    for t in range(nsh):
        X = T.copy()
        for st, ix in X.groupby('site').groups.items(): X.loc[ix, 'amt_face'] = rng.permutation(X.loc[ix, 'amt_face'].values)
        nl.append(same_diff(X)[0])
    nl = np.array(nl)
    say(f'  {label}: {len(T)} units; same-name pairs with the same amount {s0} (different {d0}) against {nl.mean():.1f} (ratio {s0 / nl.mean():.2f}, P {pvalue_hi(nl, s0):.4f})')
    return s0, nl.mean(), pvalue_hi(nl, s0)
say('(i) a name keeps its own amount (old 38 against 21.6, P 0.003)')
k1 = keep_test(N.drop_duplicates(['name_face', 'amt_face', 'place']), 'clean: one unit per (name, amount, trench), stones merged')
k2 = keep_test(N.drop_duplicates(['name_face', 'amt_face', 'site']), 'stricter: one unit per (name, amount, site)')

say('\n(ii) same name, different amount, one trench (old 9 against 3.5, P 0.011)')
Ob = O[O.lostfree & (O.area != '')].copy(); Ob['place'] = Ob.site + '|' + Ob.area
B = Ob.groupby(['place', 'sig']).agg(types=('types', 'first'), name_face=('name_face', 'first'), amt_face=('amt_face', 'first'),
                                     n=('obj', 'size')).reset_index()
Bn = B[(B.types == 'amount+name') & (B.name_face != '') & (B.amt_face != '')].reset_index(drop=True)
def canon(a):   # an amount written in the other direction (700-034 for 034-700) is the same amount
    return '|'.join(sorted('-'.join(sorted(f.split('-'))) for f in a.split('|')))
def run_ii(Bn, amtcol, label, nsh=3000):
    nm = pd.factorize(Bn.name_face)[0]; am = pd.factorize(Bn[amtcol])[0]
    site = pd.factorize(Bn.place.str.split('|').str[0])[0]; pl = pd.factorize(Bn.place)[0]
    iu = np.triu_indices(len(Bn), 1); M = ((nm[:, None] == nm[None, :]) & (am[:, None] != am[None, :]))[iu]
    def c(p): return int((M & (p[:, None] == p[None, :])[iu]).sum())
    obs = c(pl); nl = []
    for t in range(nsh):
        p2 = pl.copy()
        for s_ in np.unique(site):
            ix = np.where(site == s_)[0]; p2[ix] = rng.permutation(pl[ix])
        nl.append(c(p2))
    nl = np.array(nl)
    say(f'  {label}: {len(Bn)} signatures; pairs {obs} against {nl.mean():.2f} (P {pvalue_hi(nl, obs):.4f})')
    for i, j in zip(*iu):
        if nm[i] == nm[j] and am[i] != am[j] and pl[i] == pl[j]:
            say(f'     {Bn.place[i]:26s} {Bn.name_face[i]:22s} {Bn.amt_face[i]} x{Bn.n[i]}  vs  {Bn.amt_face[j]} x{Bn.n[j]}')
    return obs, nl.mean(), pvalue_hi(nl, obs)
r_ii = run_ii(Bn, 'amt_face', 'clean (stones, copies in a trench once, as in the old design)')
Bn['amt_c'] = Bn.amt_face.map(canon)
r_ii2 = run_ii(Bn, 'amt_c', 'amount read the same when only the stroke-cup order differs (700-034 = 034-700)')

say('\n(iii) count-line seal + record in one area with the same [number][thing] (old 89 against 69.5, P 0.003)')
D = pd.read_csv(LIPI, dtype=str).fillna('').set_index('id')
full = faces().groupby('obj').text.apply(lambda s: '|'.join(sorted(s))).to_dict()
CJ = pd.read_csv(f'{ROOT}/work_data/frame/corpus_jobs.csv', dtype=str).fillna('')
def clean(v): v = str(v).strip(); return '' if v in ('', '-', '--', '- -') else v.strip('-').strip()
NUMC = {'NUM_SHORT', 'NUM_TALL', 'NUM_NAME'}; rec = []
for r in CJ.itertuples():
    s = r.signs.split('-'); c = r.v2_classes.split('-')
    if len(s) != len(c): continue
    ps = {(s[i], s[i + 1]) for i in range(len(s) - 1) if c[i] in NUMC and c[i + 1] == 'THING'}
    if not ps: continue
    a = clean(D.at[r.face, 'area-section'])
    rec.append(dict(face=r.face, cisi=r.cisi, site=r.site, kind=r.object_kind, tk=r.text_kind, area=a, pairs=frozenset(ps),
                    stone=f2s[r.face]))
R = pd.DataFrame(rec); R = R[R.area != '']; R['full'] = R.stone.map(full)
def p7b(CLS, REC, label, nsh=2000):
    REC = REC.reset_index(drop=True)
    def colo(rp):
        c = 0
        for s in CLS.itertuples():
            for p, a, site in zip(rp, REC.area, REC.site):
                if site == s.site and a == s.area and (s.pairs & p): c += 1
        return c
    real = colo(list(REC.pairs)); sh = []
    groups = REC.groupby('site').groups
    for rep in range(nsh):
        newp = list(REC.pairs)
        for site, idx in groups.items():
            idx = list(idx); perm = rng.permutation(idx)
            for i, j in zip(idx, perm): newp[i] = REC.pairs[j]
        sh.append(colo(newp))
    sh = np.array(sh)
    say(f'  {label}: {len(CLS)} seals x {len(REC)} records; pairs {real} against {sh.mean():.1f} (ratio {real / sh.mean():.2f}, P {pvalue_hi(sh, real):.4f})')
    return real, sh.mean(), pvalue_hi(sh, real)
CLS0 = R[(R.kind == 'seals') & R.tk.isin(['bare count line', 'front word + count line'])]
REC0 = R[R.kind != 'seals']
say(f'  record rows {len(REC0)} = {REC0.stone.nunique()} stones; record copy events (site, trench, full text) '
    f'{REC0.drop_duplicates(["site", "area", "full"]).shape[0]}')
o3 = p7b(CLS0, REC0, 'A  as run (faces, every copy a separate record)')
REC1 = REC0.drop_duplicates('stone').drop_duplicates(['site', 'area', 'full'])
CLS1 = CLS0.drop_duplicates('stone')
c3 = p7b(CLS1, REC1, 'B  clean: stones, moulded copies in one trench once')
CLS2 = CLS1.drop_duplicates(['site', 'area', 'full'])
c4 = p7b(CLS2, REC1, 'C  clean + identical count-line seals in one trench once')
import json
json.dump(dict(keep=k1, keep_site=k2, ii=r_ii, ii_canon=r_ii2, p7b_run=o3, p7b_clean=c3, p7b_clean2=c4), open(f'{OUT}/r06.json', 'w'), default=float, indent=1)
