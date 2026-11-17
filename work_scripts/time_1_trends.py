#!/usr/bin/env python3
"""History job, step 2: what changes through time, against shuffles of the period labels within site x area.

PREDICTIONS, written before any number below was computed:
 H1  agents ("X's man", jar + man ending) grow as a share of seals with an ending: early < middle < late (administration thickens).
 H2  fish-crest names (marked fish 231/233/235/240/236 first in the name) grow: the great houses consolidate.
 H3  the 7-city office opening 920-060-741 is absent or rare early and appears from the middle bin on;
     it starts at Mohenjo-daro and is found at other cities only later.
 H4  the Boxed-cotton house 590-390 is a middle-bin trading house: its share peaks in the middle bin (the overseas trade);
     it starts at one city and is in more cities later.
 H5  the short-horned bull (overseas seal) and the ship words (705 before 500 sail, or 500 alone) peak in the middle bin
     (ca. 2300-2000 BC, the Mesopotamian trade window, which is the late 3B / 3B/C / early 3C stretch).
 H6  the unicorn stand letter W (the large format) rises into the late bin.
 H7  texts get longer with time (more administration per stamp).
 H8  seals get smaller late and the share of seals with no animal rises late (harappa.com: rectangular inscription-only
     seals appear only in 3C).
 H9  endings: jar+man and spear rise, comb flat, porter (carrier) flat; the 3-kalam chief formula 705-033-520 rises.
 H10 goods words: cotton 390 rises, grain 413 flat, copper 850 rises late (copper tablets appear in 3C), ivory 923 late.
 H11 star names (a number + fish inside the name: 016/003/004/032 before a fish) rise.
 H12 spelling: a marked fish written as two signs ([mark] + plain fish 220: 415-220, 240-220 ...) is early; one sign later.
Outputs: work_data/time/trends.csv, houses.csv, house_site.csv
"""
from time_common import *

AB = pd.read_csv(f'{ROOT}/work_data/animal/animal_base.csv', dtype=str).fillna('')
AB = AB.drop_duplicates('obj').set_index('obj')
D['animal_grp'] = AB.animal.reindex(D.index)
D['stand'] = AB.stand_sfx.reindex(D.index)

S = D[D.seal].copy()
S['main'] = S.apply(rd, axis=1)
S['nm'] = S.name.apply(lambda n: [a for a in n if a not in ('000',)])
rows = []
def add(label, df, col, pred, pct=True):
    o = shuffle_trend(df, col)
    rows.append(dict(test=label, prediction=pred, n=o['n'] if o else 0,
                     early=o['early'][0] if o else None, n_early=o['early'][1] if o else None,
                     middle=o['middle'][0] if o else None, n_mid=o['middle'][1] if o else None,
                     late=o['late'][0] if o else None, n_late=o['late'][1] if o else None,
                     r=o['r'] if o else None, p=o['p'] if o else None))
    print(f'{label:42s} {fmt_tr(o, pct)}', flush=True)
    return o

E = S[S.ending != 'none'].copy()
for e in ['jar+man', 'jar', 'spear', 'porter', 'comb']:
    E[e] = (E.ending == e).astype(float)
    add(f'ending {e} (seals with an ending)', E, e, 'H1/H9')
S['fishcrest'] = S.nm.apply(lambda n: float(len(n) > 0 and n[0] in MARKED)).where(S.nm.str.len() > 0)
add('fish-crest first in name (seals)', S, 'fishcrest', 'H2 rise')
S['anyfish'] = S.nm.apply(lambda n: float(any(a in FISHALL for a in n))).where(S.nm.str.len() > 0)
add('any fish in name (seals)', S, 'anyfish', 'H2 rise')

A = D.copy()
A['office'] = A.faces.apply(lambda fs: float(has_seq(fs, ('920', '060', '741'))))
A['boxcot'] = A.faces.apply(lambda fs: float(has_seq(fs, ('590', '390'))))
add('office opening 920-060-741 (all objects)', A, 'office', 'H3 rise from middle')
add('Boxed-cotton 590-390 (all objects)', A, 'boxcot', 'H4 middle peak')
S['office'] = A.office.reindex(S.index); S['boxcot'] = A.boxcot.reindex(S.index)
add('office opening (seals)', S, 'office', 'H3')
add('Boxed-cotton (seals)', S, 'boxcot', 'H4')

B = S[S.animal_grp.notna() & (S.animal_grp != '')].copy()
for g in ['UNICORN', 'SHORTHORN', 'ELEPHANT', 'ZEBU', 'GOAT', 'COMPOSITE', 'NONE']:
    B[g] = (B.animal_grp == g).astype(float)
    add(f'animal {g} (seals)', B, g, 'H5 shorthorn middle; H8 NONE late')
U = B[(B.animal_grp == 'UNICORN') & B.stand.isin(list('WJSIL'))].copy()
for l in 'WJSIL':
    U[l] = (U.stand == l).astype(float)
    add(f'unicorn stand letter {l}', U, l, 'H6 W late')

S['len'] = S.main.apply(lambda f: float(len([a for a in f if a != '000'])))
add('text length (seals, signs)', S, 'len', 'H7 rise', pct=False)
Q = S[S.face_mm2.notna() & (S.face_mm2 > 0)].copy()
Q['logsize'] = np.log(Q.face_mm2)
add('seal face size (log mm2)', Q, 'logsize', 'H8 fall', pct=False)
Q['mm2'] = Q.face_mm2
add('seal face size (mm2)', Q, 'mm2', 'H8 fall', pct=False)
A['chief3'] = A.faces.apply(lambda fs: float(has_seq(fs, ('705', '033', '520'))))
add('3-kalam chief 705-033-520 (all)', A, 'chief3', 'H9 rise')
A['len'] = A.faces.apply(lambda fs: float(sum(len([a for a in f if a != '000']) for f in fs)))
add('text length (all objects, all faces)', A, 'len', 'H7', pct=False)

GOODS = {'cotton 390': {'390'}, 'grain 413': {'413'}, 'copper 850': {'850'}, 'ivory 923': {'923'},
         'sail 500': {'500'}, 'kalam 705/706': {'705', '706'}, 'cup 700': {'700'}, 'thread 405': {'405'}, 'kindred/cloth 407': {'407'},
         'sesame/produce 838': {'838'}, 'chest 590': {'590'}, 'dozen 055': {'055'}}
for k, v in GOODS.items():
    A[k] = A.signs.apply(lambda z: float(bool(z & v)))
    add(f'goods {k} (all objects)', A, k, 'H10')
A['ship'] = A.faces.apply(lambda fs: float(has_seq(fs, ('705', '500')) or has_seq(fs, ('706', '500'))))
add('ship 705-500 kalam pAy (all)', A, 'ship', 'H5 middle')

def starname(n):
    for i in range(len(n) - 1):
        if n[i] in ('016', '003', '004', '032', '002', '017', '013', '014') and n[i + 1] in FISHALL: return 1.0
    return 0.0
S['starname'] = S.main.apply(starname)
add('star name (number + fish, seals)', S, 'starname', 'H11 rise')
S['iru'] = S.main.apply(lambda f: float(has_seq([f], ('032', '220'))))
add('iru-mIn 032-220 (seals)', S, 'iru', 'H11')
S['aru'] = S.main.apply(lambda f: float(has_seq([f], ('016', '220')) or any(has_seq([f], ('016', x)) for x in FISHALL)))
add('aRu-mIn six + fish (seals)', S, 'aru', 'H11')

TWO = {'415', '240', '413', '416', '803', '617', '235', '786', '603'}
def spelling(fs):
    one = sum(a in MARKED for f in fs for a in f)
    two = sum(1 for f in fs for i in range(len(f) - 1) if f[i] in TWO and f[i + 1] == '220')
    if one + two == 0: return np.nan
    return two / (one + two)
A['twosign'] = A.faces.apply(spelling)
add('marked fish as two signs (share of fish spellings)', A, 'twosign', 'H12 early')
A['twosign415'] = A.faces.apply(lambda fs: np.nan if not any(('415' in f) or ('220' in f) or any(a in MARKED for a in f) for f in fs)
                                else float(has_seq(fs, ('415', '220'))))
add('barred fish written 415-220 (fish objects)', A, 'twosign415', 'H12 early')

pd.DataFrame(rows).to_csv(f'{OUTT}/trends.csv', index=False)

# ---------- houses: first name sign of names of 2+ signs, all object kinds ----------
H = D.copy()
H['house'] = H.name.apply(lambda n: n[0] if len([a for a in n if a != '000']) >= 2 and n[0] != '000' else None)
H = H[H.house.notna()]
tab = pd.crosstab(H.house, H.bin).reindex(columns=BINS, fill_value=0)
tab['total'] = tab.sum(axis=1)
base = H.bin.value_counts(normalize=True).reindex(BINS)
tab = tab.sort_values('total', ascending=False)
from scipy.stats import chisquare
out = []
for h, r in tab.head(25).iterrows():
    exp = base.values * r.total
    sub = H[H.house == h]
    sites = sub.groupby('bin').site.apply(lambda s: '/'.join(sorted(set(s))))
    # within-area shuffle trend for this house
    H['_x'] = (H.house == h).astype(float)
    o = shuffle_trend(H, '_x', nshuf=2000)
    out.append(dict(house=h, early=r.early, middle=r.middle, late=r.late, total=r.total,
                    exp_early=round(exp[0], 1), exp_middle=round(exp[1], 1), exp_late=round(exp[2], 1),
                    r=round(o['r'], 3), p=round(o['p'], 4),
                    sites_early=sites.get('early', ''), sites_middle=sites.get('middle', ''), sites_late=sites.get('late', '')))
HT = pd.DataFrame(out); HT.to_csv(f'{OUTT}/houses.csv', index=False)
print(HT.to_string())
hs = pd.crosstab([H.house, H.site], H.bin).reindex(columns=BINS, fill_value=0)
hs = hs[hs.sum(axis=1) >= 3]; hs.to_csv(f'{OUTT}/house_site.csv')
print('house base shares', base.round(3).to_dict(), 'houses dated', len(H))
