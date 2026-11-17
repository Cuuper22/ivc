#!/usr/bin/env python3
"""Step 4: the other animals. What the species goes with, and whether holders in one building avoid each other's beast.
Species groups: unicorn, short-horned bull (Gaur), zebu, elephant, rhinoceros, tiger, buffalo, goat (goat + Bull3),
composite (Comp, CompBull, Mult, T-A-T, T-M-T, Htgr, Phyt), none (inscription-only), other (scene, gharial, hare, ...).
One row per stone. Chance: species dealt among seals of the same site (and format where said), 2,000 times.
PREDICTIONS, fixed first:
 Q1 size: zebu and elephant stones bigger than unicorns at one site and format; goat and short-horned smaller.
 Q2 material, time bin, text kind: species goes with time bin (short-horned drop late) and kind (composite with short
    texts), not with material (P > 0.05).
 Q3 PERSONAL-MARK test (avoidance): inside one building, two non-unicorn beast seals carry the same species LESS than
    chance (ratio < 0.8), and buildings hold more different species than dealt. My call: the species is a personal
    mark chosen to set holders apart, so avoidance shows.
 Q4 same crest, same building: different animals more than chance (members of one family pick different beasts).
"""
from stand_common import *
from scipy.stats import chi2_contingency
rng = np.random.default_rng(6)
S = stand_seals()
d = S.drop_duplicates('obj').reset_index(drop=True)
G = {'unicorn': 'unicorn', 'short-horned bull': 'short-horned bull', 'zebu': 'zebu', 'elephant': 'elephant', 'rhinoceros': 'rhinoceros',
     'tiger': 'tiger', 'buffalo': 'buffalo', 'goat': 'goat', 'Bull3': 'goat', 'none': 'none'}
for k in ['Comp', 'CompBull', 'Mult', 'T-A-T', 'T-M-T', 'Htgr', 'Phyt']: G[k] = 'composite'
d['sp'] = [G.get(a, 'other' if a else '') for a in d.animal]
d = d[d.sp != ''].reset_index(drop=True)
log('base', d.sp.value_counts().to_dict())
# Q1 size residual: log size minus the median of its site x format
d['res'] = d.logsz - d.groupby(['site', 'fmt']).logsz.transform('median')
sq = d[(d.fmt == 'square') & d.res.notna()]
tab = sq.groupby('sp').res.agg(['count', 'median']).round(3)
st = strata_idx(sq.site.values)
sims = []
for _ in range(2000):
    p = perm_within(sq.sp.values, st, rng); sims.append(pd.Series(sq.res.values).groupby(p).median())
sims = pd.DataFrame(sims)
tab['dealt_median'] = sims.mean().round(3); tab['P_bigger'] = [(sims[s] >= tab.loc[s, 'median']).mean() for s in tab.index]
tab['pct'] = (np.exp(tab['median']) * 100 - 100).round(0)
log('Q1 size (square seals, log size against site x format median)'); print(tab.to_string())
tab.to_csv(f'{OUT}/animals_size.csv')
# Q2 associations
rows = []
for col in ['mat', 'bin', 'kind', 'fmt']:
    g = d[(d[col] != '') & d[col].notna() & (d.sp != 'other')].reset_index(drop=True)
    if col == 'mat': g = g.assign(mat=g.mat.where(g.mat.isin(['steatite', 'faience', 'terracotta', 'clay']), 'other'))
    if col == 'kind': g = g[g.kind.isin(['bare name', 'name + closer', 'name + title', 'name + closer + title', 'front formula', 'count line'])].reset_index(drop=True)
    stv = strata_idx((g.site + ('' if col == 'fmt' else '|' + g.fmt)).values)
    def V(lab):
        ct = pd.crosstab(g[col], lab); ct = ct.loc[ct.sum(1) > 0, ct.sum(0) > 0]
        return np.sqrt(chi2_contingency(ct, correction=False)[0] / (ct.values.sum() * (min(ct.shape) - 1)))
    rv = V(g.sp.values); s_ = np.array([V(perm_within(g.sp.values, stv, rng)) for _ in range(500)])
    rows.append(dict(feature=col, seals=len(g), V=round(rv, 3), dealt=round(s_.mean(), 3), P=(s_ >= rv).mean())); log('Q2', rows[-1])
    ct = pd.crosstab(g.sp, g[col]); print((ct.div(ct.sum(1), axis=0) * 100).round(0).assign(n=ct.sum(1)).to_string())
pd.DataFrame(rows).to_csv(f'{OUT}/animals_assoc.csv', index=False)
# Q3 avoidance inside buildings
b = d[(d.building != '')].reset_index(drop=True)
I, J = np.triu_indices(len(b), 1); same = b.building.values[I] == b.building.values[J]; I, J = I[same], J[same]
lab = np.asarray(b.sp.values, dtype=object); st = strata_idx(b.site.values)
BEAST = {'short-horned bull', 'zebu', 'elephant', 'rhinoceros', 'tiger', 'buffalo', 'goat', 'composite'}
def stats(l):
    nu = np.array([x in BEAST for x in l])
    both = nu[I] & nu[J]; anyb = (l[I] != 'none') & (l[J] != 'none')
    out = dict(beast_pairs=int(both.sum()), beast_same=int((l[I] == l[J])[both].sum()), all_same=int((l[I] == l[J]).sum()),
               animal_pairs=int(anyb.sum()), animal_same=int((l[I] == l[J])[anyb].sum()))
    out['species_per_building'] = pd.Series(l).groupby(b.building.values).nunique().pipe(lambda s: s[b.building.value_counts().reindex(s.index) >= 3]).sum()
    return out
real = stats(lab); sims = [stats(perm_within(lab, st, rng)) for _ in range(2000)]
sm = pd.DataFrame(sims)
for k in real:
    lo = (sm[k] <= real[k]).mean(); hi = (sm[k] >= real[k]).mean()
    log('Q3 building', f'{k}: real {real[k]} dealt {sm[k].mean():.1f} P(fewer) {lo:.3f} P(more) {hi:.3f}')
# same building + format strata (bars vs beasts cluster by building)
st2 = strata_idx((b.site + '|' + b.fmt).values)
sims2 = pd.DataFrame([stats(perm_within(lab, st2, rng)) for _ in range(2000)])
for k in ['beast_same', 'animal_same', 'species_per_building']:
    log('Q3 building (site x format)', f'{k}: real {real[k]} dealt {sims2[k].mean():.1f} P(fewer) {(sims2[k]<=real[k]).mean():.3f} P(more) {(sims2[k]>=real[k]).mean():.3f}')
# Q4 same crest same building
cr = (b.crest.values[I] == b.crest.values[J]) & (b.crest.values[I] != '')
anyb = (lab[I] != 'none') & (lab[J] != 'none') & cr
r4 = int((lab[I] == lab[J])[anyb].sum())
s4 = [int((p[I] == p[J])[anyb].sum()) for p in (perm_within(lab, st2, rng) for _ in range(2000))]
log('Q4', f'same building same crest, both with an animal: same species {r4} of {int(anyb.sum())} against {np.mean(s4):.1f} (P fewer {np.mean(np.array(s4)<=r4):.3f})')
