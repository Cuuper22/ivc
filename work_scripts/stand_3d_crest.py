#!/usr/bin/env python3
"""Step 2b-crest: same crest in different cities, chance from each city's letter mix inside the stone's size third,
lost-sign crest '000' removed (same-crest names share size, and size goes with W).
Prediction (workshop): the raw excess (1,218 of 3,777 against 1,094.1, ratio 1.11, stand_3_places.py) falls to about 1."""
from stand_common import *
S = stand_seals()
u = S[S.stand5 != ''].drop_duplicates('obj').reset_index(drop=True)
u['size3'] = ''
for st, g in u.groupby('site'):
    if g.logsz.notna().sum() >= 6: u.loc[g.index, 'size3'] = pd.qcut(g.logsz, 3, labels=['s', 'm', 'b'], duplicates='drop').astype(object)
u['size3'] = u.size3.fillna('').astype(str)

# Redo of the cross-city crest test: lost-sign crest '000' removed, chance from each city's letter mix INSIDE the
# stone's size third (same-crest names share size, size goes with W). Prediction (workshop): ratio falls to about 1.
cr = u[(u.crest != '') & (u.crest != '000') & ~u.size3.isin(['', 'nan'])].reset_index(drop=True)
mix3 = u[~u.size3.isin(['', 'nan'])].groupby(['site', 'size3']).stand5.value_counts(normalize=True).unstack(fill_value=0)
sc = ec = nc = 0
A, B_ = np.triu_indices(len(cr), 1)
k = (cr.site.values[A] != cr.site.values[B_]) & (cr.crest.values[A] == cr.crest.values[B_])
for a, b in zip(A[k], B_[k]):
    e = float((mix3.loc[(cr.site[a], cr.size3[a])] * mix3.loc[(cr.site[b], cr.size3[b])]).sum())
    sc += cr.stand5[a] == cr.stand5[b]; ec += e; nc += 1
log('cross-city size-held', f'same crest other city: {sc} of {nc} against {ec:.1f} (ratio {sc/ec:.2f})')
with open(f'{OUT}/places_crosscity.txt', 'a') as fh: fh.write(f'size-held, lost crest removed: same crest other city {sc} of {nc} against {ec:.1f}\n')
# Shuffle check: letters dealt within city x size third, 2,000 times, same pairs.
rng = np.random.default_rng(33)
a_, b_ = A[k], B_[k]
st = strata_idx((cr.site + '|' + cr.size3).values); lab = np.asarray(cr.stand5.values, dtype=object)
real = int((lab[a_] == lab[b_]).sum())
sims = np.array([(lambda p: (p[a_] == p[b_]).sum())(perm_within(lab, st, rng)) for _ in range(2000)])
log('cross-city size-held', f'shuffle: real {real} against {sims.mean():.1f}, ratio {real/sims.mean():.2f}, P {np.mean(sims >= real):.4f}')
# which crests carry it
rows = []
for c, g in cr.groupby('crest'):
    if g.site.nunique() < 2 or len(g) < 4: continue
    ii, jj = np.triu_indices(len(g), 1); x = g.site.values[ii] != g.site.values[jj]
    rows.append(dict(crest=c, stones=len(g), cities=g.site.nunique(), letters=' '.join(f'{k}{v}' for k, v in g.stand5.value_counts().items()), cross_pairs=int(x.sum()), cross_share=int((g.stand5.values[ii] == g.stand5.values[jj])[x].sum())))
R = pd.DataFrame(rows).sort_values('cross_pairs', ascending=False); R.to_csv(f'{OUT}/crest_crosscity.csv', index=False); print(R.head(12).to_string(index=False))
with open(f'{OUT}/places_crosscity.txt', 'a') as fh: fh.write(f'shuffle within city x size third: real {real} against {sims.mean():.1f}, P {np.mean(sims >= real):.4f}\n')
