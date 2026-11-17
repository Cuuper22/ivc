#!/usr/bin/env python3
"""History job, redesign after the flat first pass (time_1_trends.py gave almost no change through time).

Why redesign: shuffling inside site x area throws away every area that was dug in one period only (all of Harappa
E Trench 11 is 3B/C), so most of the data cannot speak. Two new designs, predictions written before running:
 D1  FINE RANK in the one long dug sequence: Mackay's DK-G area at Mohenjo-daro, seven levels Early I -> Late I
     (catalogue rank 3 .. 9). Prediction: agents (jar+man), office opening and Boxed-cotton seals climb level by level;
     no-animal seals climb (harappa.com: inscription-only seals are a 3C type).
 D2  FIRST APPEARANCE: for the office opening 920-060-741, Boxed-cotton 590-390, ship 705-500, short-horned bull,
     list every dated object with its site and rank. Prediction: each starts at Mohenjo-daro (rank <= 4) and turns up
     at Harappa / Dholavira / Kalibangan only at a later rank.
 D3  UNSHUFFLED all-site contrast early vs late (Fisher), labelled as not area-controlled, for the main features.
 NEW IDEA D4: a tablet that carries an account (a cup count) dies out late; the record moves to seals. Prediction:
     share of dated Harappa tablets with a cup count falls from 3B to 3C-3/4.
Outputs: work_data/time/dkg_levels.csv, first_appearance.csv, contrast.csv
"""
from time_common import *
from scipy.stats import fisher_exact, spearmanr

AB = pd.read_csv(f'{ROOT}/work_data/animal/animal_base.csv', dtype=str).fillna('').drop_duplicates('obj').set_index('obj')
D['animal_grp'] = AB.animal.reindex(D.index)
D['office'] = D.faces.apply(lambda fs: has_seq(fs, ('920', '060', '741')))
D['boxcot'] = D.faces.apply(lambda fs: has_seq(fs, ('590', '390')))
D['ship'] = D.faces.apply(lambda fs: has_seq(fs, ('705', '500')) or has_seq(fs, ('706', '500')) or any('500' in f for f in fs))
D['agent'] = D.ending == 'jar+man'
D['short'] = D.animal_grp == 'SHORTHORN'
D['noanimal'] = D.animal_grp == 'NONE'
D['cup'] = D.faces.apply(lambda fs: any('700' in f for f in fs))
D['fishcrest'] = D.name.apply(lambda n: len(n) > 0 and n[0] in MARKED)

# ---- D1 DK-G level by level ----
G = D[(D.site == 'Mohenjo-daro') & D.area.str.startswith('DKG') & (D.rule == 'B layer-map')].copy()
LV = {'Early I': 0, 'Intermediate III': 1, 'Intermediate II': 2, 'Intermediate I': 3, 'Late III': 4, 'Late II': 5, 'Late I': 6, 'Late IA': 6, 'Late IB': 6}
G['lvl'] = (G.period.str.strip() + ' ' + G.phase.str.strip()).map(LV)
G = G[G.lvl.notna()]
Sg = G[G.seal]
rows = []
for l, sub in Sg.groupby('lvl'):
    e = sub[sub.ending != 'none']
    rows.append(dict(level=int(l), seals=len(sub), agent=f'{e.agent.sum()}/{len(e)}', office=int(sub.office.sum()), boxcot=int(sub.boxcot.sum()),
                     noanimal=f'{sub.noanimal.sum()}/{len(sub)}', short=int(sub.short.sum()), fishcrest=f'{sub.fishcrest.sum()}/{len(sub)}',
                     median_mm2=sub.face_mm2.median(), median_ft=sub.ft.median()))
L = pd.DataFrame(rows); L.to_csv(f'{OUTT}/dkg_levels.csv', index=False); print(L.to_string())
for c in ['agent', 'office', 'boxcot', 'noanimal', 'short', 'fishcrest']:
    sub = Sg if c != 'agent' else Sg[Sg.ending != 'none']
    rho, p = spearmanr(sub.lvl, sub[c].astype(float))
    print(f'D1 DK-G seals {c:10s} Spearman rho {rho:+.3f} P {p:.4f} (n {len(sub)})')
rho, p = spearmanr(Sg.lvl, Sg.face_mm2, nan_policy='omit'); print(f'D1 DK-G seal size rho {rho:+.3f} P {p:.4f}')

# ---- D2 first appearance ----
fa = []
for c in ['office', 'boxcot', 'ship', 'short']:
    sub = D[D[c]].sort_values('rank')
    for o, r in sub.iterrows():
        fa.append(dict(feature=c, obj=o, cisi=r.cisi, site=r.site, kind=r.kind, area=r.area, time=r.time, rank=r['rank'], bin=r.bin, rule=r.rule,
                       text=' | '.join('-'.join(f) for f in r.faces)))
FA = pd.DataFrame(fa); FA.to_csv(f'{OUTT}/first_appearance.csv', index=False)
for c, sub in FA.groupby('feature'):
    print(f'\nD2 {c}: n {len(sub)}; by site and bin:'); print(pd.crosstab(sub.site, sub.bin).to_string())
    print(' earliest:', sub.head(5)[['cisi', 'site', 'time', 'rule']].values.tolist())

# ---- D3 unshuffled contrast ----
out = []
for c, base in [('agent', D.seal & (D.ending != 'none')), ('fishcrest', D.seal & (D.name.str.len() > 0)), ('office', D.seal), ('boxcot', D.seal),
                ('short', D.seal & D.animal_grp.ne('')), ('noanimal', D.seal & D.animal_grp.ne('')), ('ship', D.index == D.index), ('cup', D.kind == 'mtab')]:
    x = D[base]
    a = x[x.bin == 'early'][c]; b = x[x.bin == 'late'][c]
    odds, p = fisher_exact([[a.sum(), len(a) - a.sum()], [b.sum(), len(b) - b.sum()]])
    out.append(dict(feature=c, early=f'{a.sum()}/{len(a)}', late=f'{b.sum()}/{len(b)}', early_pct=a.mean() * 100, late_pct=b.mean() * 100, p=p))
C = pd.DataFrame(out); C.to_csv(f'{OUTT}/contrast.csv', index=False); print('\nD3 unshuffled early vs late, all sites\n', C.round(4).to_string())

# ---- D4 cup accounts on Harappa tablets by period ----
H = D[(D.site == 'Harappa') & (D.kind == 'mtab')]
print('\nD4 Harappa tablets with a cup sign, by period code:')
print(H.groupby('time').cup.agg(['sum', 'count', 'mean']).sort_index(key=lambda s: s.map(RANK)).to_string())
rho, p = spearmanr(H['rank'], H.cup.astype(float)); print(f'D4 rho {rho:+.3f} P {p:.2g} (n {len(H)})')
Hs = D[(D.site == 'Harappa') & D.seal]
print('Harappa seals no-animal by period:'); print(Hs.groupby('time').noanimal.agg(['sum', 'count']).sort_index(key=lambda s: s.map(RANK)).to_string())
print('Harappa dated objects by kind and period:'); print(pd.crosstab(D[D.site == 'Harappa'].time, D[D.site == 'Harappa'].kind).sort_index(key=lambda s: s.map(RANK)).to_string())
