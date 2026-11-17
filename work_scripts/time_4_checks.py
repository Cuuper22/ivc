#!/usr/bin/env python3
"""History job: does the time axis see what the excavators saw? harappa.com: inscription-only (no animal) seals
appear in 3C. PREDICTION written first: at Harappa the share of seals with no animal climbs with period rank, within area.
Also: career test. PREDICTION: names seen in 2+ bins keep their ending (lineage) in most cases; where it changes,
the later ending is jar+man or spear (a promotion)."""
from time_common import *
from scipy.stats import spearmanr
AB = pd.read_csv(f'{ROOT}/work_data/animal/animal_base.csv', dtype=str).fillna('').drop_duplicates('obj').set_index('obj')
D['grp'] = AB.animal.reindex(D.index)
H = D[(D.site == 'Harappa') & D.seal & D.grp.ne('') & D.grp.notna() & D['rank'].notna()].copy()
H['none'] = (H.grp == 'NONE').astype(float)
rho, p = spearmanr(H['rank'], H.none); print(f'Harappa seals: no-animal against period rank rho {rho:+.3f} P {p:.2g} (n {len(H)})')
o = shuffle_trend(H, 'none'); print('within-area shuffle:', fmt_tr(o))
e = H[H['rank'] <= 4]; l = H[H['rank'] >= 7]
print(f'Harappa no-animal seals: up to 3B/C {int(e.none.sum())}/{len(e)}, 3C-3 and later {int(l.none.sum())}/{len(l)}')
M_ = D[(D.site == 'Mohenjo-daro') & D.seal & D.grp.ne('') & D.grp.notna()].copy(); M_['none'] = (M_.grp == 'NONE').astype(float)
print('Mohenjo-daro:', fmt_tr(shuffle_trend(M_, 'none')))
# careers
R = pd.read_csv(f'{OUTT}/recurring_names.csv')
R = R[R.nbins >= 2]
ch = 0; same = 0; up = []
for r in R.itertuples():
    parts = [x.split(':') for x in r.endings.split(' ; ')]
    ends = [set(p[1].split(',')) - {'none'} for p in parts]
    ends = [e for e in ends if e]
    if len(ends) < 2: continue
    if all(e == ends[0] for e in ends): same += 1
    else: ch += 1; up.append((r.name, r.endings, r.sites))
print(f'names in 2+ bins with endings: same ending in every bin {same}, changed {ch}')
for u in up: print('  ', u)

# A house that falls at one city and rises at another. PREDICTION: at least one of the 15 biggest houses has opposite
# within-area trends at Harappa and Mohenjo-daro, each at P < 0.1.
H = D.copy()
H['house'] = H.name.apply(lambda n: n[0] if len([a for a in n if a != '000']) >= 2 and n[0] != '000' else None)
H = H[H.house.notna()]
top = H.house.value_counts().head(15).index
print('\nhouse trends by city (within-area shuffle):')
for h in top:
    line = f'  {h}:'
    for site in ['Harappa', 'Mohenjo-daro']:
        X = H[H.site == site].copy(); X['_x'] = (X.house == h).astype(float)
        o = shuffle_trend(X, '_x', nshuf=2000)
        line += f'  {site} r {o["r"]:+.3f} P {o["p"]:.3f} ({int(X._x.sum())})' if o else f'  {site} too few'
    print(line)
