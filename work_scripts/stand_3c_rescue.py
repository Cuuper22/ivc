#!/usr/bin/env python3
"""Step 2b-rescue: the room effect fell to chance once each stone counts once and letters are dealt only among
letter seals (log_3b.txt: room 29.8% against 27.1%). Redesigns, predictions fixed first:
 R1 (cleaner labels): drop L (7 of 12 L photos unreadable: the letter may mark a poorly seen stand) and worn stones
    (condition Poor); predicted: room ratio rises above 1.3 if the letter is a household mark blurred by bad labels.
 R2 (new idea, the style axis the photos found): fold the letters into two carving styles, FOLDS = I + W (neck folds
    in 18 of 22 photos) and SMOOTH = J + S (smooth neck 16 of 22). Predicted (workshop): same-room and same-building
    pairs share the style above chance (ratio >= 1.15); neighbours at the same depth share it as much as house-mates.
 R3 the twins figure (same city, other building, same letter 9 of 22 against 4.9) redone with the proper deal.
"""
from stand_common import *
rng = np.random.default_rng(31)
S = stand_seals()
u0 = S[S.stand5 != ''].drop_duplicates('obj').reset_index(drop=True)
def grid(u, col, tag):
    I, J = np.triu_indices(len(u), 1); k = u.site.values[I] == u.site.values[J]; I, J = I[k], J[k]
    def eq(c): a = u[c].values; return (a[I] == a[J]) & (a[I] != '')
    room, bld, blk, area = eq('room'), eq('building'), eq('block'), eq('area')
    dg = np.abs(u.depth.values[I] - u.depth.values[J]); near = area & ~np.isnan(dg) & (dg <= 3); far = area & ~np.isnan(dg) & (dg >= 6)
    cells = {'same room': room, 'same building': bld, 'same building near depth': bld & near, 'same building far depth': bld & far,
             'other building same block near': blk & ~bld & near, 'other block same area near': area & ~blk & near}
    lab = u[col].values; st = strata_idx(u.site.values)
    real = {c: int((lab[I] == lab[J])[m].sum()) for c, m in cells.items()}
    sims = {c: [] for c in cells}
    for _ in range(2000):
        p = perm_within(lab, st, rng); sh = p[I] == p[J]
        for c, m in cells.items(): sims[c].append(sh[m].sum())
    out = []
    for c, m in cells.items():
        e = np.mean(sims[c]); out.append(dict(test=tag, cell=c, pairs=int(m.sum()), share=real[c], dealt=round(e, 1), ratio=round(real[c] / e, 2) if e else np.nan, P=round(np.mean(np.array(sims[c]) >= real[c]), 4)))
        log(tag, out[-1])
    return out
rows = []
u1 = u0[(u0.stand5 != 'L') & ~u0.condition.isin(['Poor'])].reset_index(drop=True)
rows += grid(u1, 'stand5', 'R1 no L, no worn')
u2 = u0.copy(); u2['style'] = u2.stand5.map({'I': 'folds', 'W': 'folds', 'J': 'smooth', 'S': 'smooth', 'L': ''})
u2 = u2[u2['style'] != ''].reset_index(drop=True)
rows += grid(u2, 'style', 'R2 folds vs smooth')
pd.DataFrame(rows).to_csv(f'{OUT}/places_rescue.csv', index=False)
# R3 twins
P = pd.read_csv(f'{ROOT}/work_data/twins/pairs.csv', dtype=str).fillna('')
log('R3', 'twins pairs columns', list(P.columns)[:30])
P = P[(P.stand5_a != '') & (P.stand5_b != '')]
mix = u0.groupby('site').stand5.value_counts(normalize=True).unstack(fill_value=0)
for nm, g in [('same city other building', P[(P.site_a == P.site_b) & (P.same_building != 'True')]), ('different cities', P[P.site_a != P.site_b])]:
    e = sum(float((mix.loc[a] * mix.loc[b]).sum()) for a, b in zip(g.site_a, g.site_b))
    log('R3', f'twins {nm}: same letter {(g.stand5_a == g.stand5_b).sum()} of {len(g)} against {e:.1f} from the cities\' letter mixes')
