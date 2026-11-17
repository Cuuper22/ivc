#!/usr/bin/env python3
"""Step 2b: household against workshop, by where and when seals sharing a letter lie, and by crest.

Plain words: a PAIR is two unicorn seals with a letter from one city. SHARE = both carry the same letter.
Depth gap is only used when both seals come from the same excavation area (raw depths are not comparable across areas).
'near' = depth gap <= 3 ft (about the same generation), 'far' = gap >= 6 ft (generations apart).
Chance: letters dealt at random among unicorn seals of the same city (A), and of the same city and size third (B),
2,000 times; ratio = real shares / dealt mean; P = share of deals with at least as many shares.

PREDICTIONS, fixed before any number:
 HOUSEHOLD: same building far in depth shares as much as same building near (family keeps its mark across
   generations); neighbours in the same block at the same depth but another building share little (ratio < 1.2);
   same building, different crests still share (the house mark is above the family name in the text).
 WORKSHOP: same time matters more than same building: different building, same block, near depth shares at a ratio
   close to same building near; same building far depth falls toward 1; same crest across buildings or cities at chance.
 MY COMMITTED CALL: workshop. The letter is a carving style (photo check: neck folds and saddle follow the letter,
   the stand drawing does not), so the near-time neighbours will share it and the far-depth house-mates will not.
"""
from stand_common import *
rng = np.random.default_rng(2)
S = stand_seals()
u = S[S.stand5 != ''].drop_duplicates('obj').reset_index(drop=True)
u['size3'] = ''
for st, g in u.groupby('site'):
    if g.logsz.notna().sum() >= 6: u.loc[g.index, 'size3'] = pd.qcut(g.logsz, 3, labels=['s', 'm', 'b'], duplicates='drop').astype(str)
u['sz'] = u.site + '|' + u.size3.astype(str)
I, J = np.triu_indices(len(u), 1)
same_site = (u.site.values[I] == u.site.values[J]); I, J = I[same_site], J[same_site]
def eq(col): a = u[col].values; return (a[I] == a[J]) & (a[I] != '') & pd.notna(a[I])
room, bld, blk, area = eq('room'), eq('building'), eq('block'), eq('area')
dg = np.abs(u.depth.values[I] - u.depth.values[J]); hasd = ~np.isnan(dg) & area
near, far = hasd & (dg <= 3), hasd & (dg >= 6)
crest_same = eq('crest'); crest_known = (u.crest.values[I] != '') & (u.crest.values[J] != '')
bin_same = eq('bin'); bin_known = (u.bin.values[I] != '') & (u.bin.values[J] != '')
cells = {
 'same room': room,
 'same building, near depth': bld & near,
 'same building, far depth (6+ ft)': bld & far,
 'other building same block, near depth': blk & ~bld & near,
 'other building same block, far depth': blk & ~bld & far,
 'other block same area, near depth': area & ~blk & near,
 'other block same area, far depth': area & ~blk & far,
 'other area same city, same time bin': ~area & bin_known & bin_same,
 'other area same city, other time bin': ~area & bin_known & ~bin_same,
 'same building, same crest': bld & crest_known & crest_same,
 'same building, different crests': bld & crest_known & ~crest_same,
 'same crest, other building same city': ~bld & crest_known & crest_same & (u.building.values[I] != '') & (u.building.values[J] != ''),
 'different crest, other building same city': ~bld & crest_known & ~crest_same & (u.building.values[I] != '') & (u.building.values[J] != ''),
}
lab = u.stand5.values
def counts(l): sh = l[I] == l[J]; return {k: int(sh[m].sum()) for k, m in cells.items()}
real = counts(lab)
res = {}
for nm, keys in [('A city', u.site.values), ('B city x size third', u.sz.values)]:
    st = strata_idx(keys); sims = {k: [] for k in cells}
    for it in range(2000):
        c = counts(perm_within(lab, st, rng))
        for k in cells: sims[k].append(c[k])
        if it % 500 == 0: log('deal', nm, it)
    res[nm] = {k: (np.mean(v), np.mean(np.array(v) >= real[k])) for k, v in sims.items()}
rows = []
for k, m in cells.items():
    r = dict(cell=k, pairs=int(m.sum()), share=real[k], rate=round(real[k] / max(m.sum(), 1), 3))
    for nm in res:
        e, p = res[nm][k]; r[f'{nm[0]}_dealt'] = round(e, 1); r[f'{nm[0]}_ratio'] = round(real[k] / e, 2) if e else np.nan; r[f'{nm[0]}_P'] = p
    rows.append(r); log('cell', r)
pd.DataFrame(rows).to_csv(f'{OUT}/places_pairs.csv', index=False)

# Cross-city: same crest in different cities; expected from each city's own letter mix
X = []
for i in range(len(u)):
    pass
cr = u[u.crest != '']
pairs = [(a, b) for a, b in zip(*np.triu_indices(len(cr), 1)) if cr.site.values[a] != cr.site.values[b]]
mix = u.groupby('site').stand5.value_counts(normalize=True).unstack(fill_value=0)
sc = sp = ec = ep = 0; nc = npair = 0
for a, b in pairs:
    sa, sb = cr.site.values[a], cr.site.values[b]
    e = float((mix.loc[sa] * mix.loc[sb]).sum()); s = cr.stand5.values[a] == cr.stand5.values[b]
    if cr.crest.values[a] == cr.crest.values[b]: sc += s; ec += e; nc += 1
    else: sp += s; ep += e; npair += 1
log('cross-city', f'same crest: {sc} of {nc} share against {ec:.1f} from city mixes (ratio {sc/ec:.2f}); different crest: {sp} of {npair} against {ep:.1f} (ratio {sp/ep:.2f})')
with open(f"{OUT}/places_crosscity.txt", "w") as fh:
    fh.write(f'same crest other city: {sc} of {nc} against {ec:.1f}\ndifferent crest other city: {sp} of {npair} against {ep:.1f}\n')

