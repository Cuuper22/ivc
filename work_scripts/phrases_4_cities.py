#!/usr/bin/env python3
"""PHRASES step 4: inter-city. Fixed 2026-11-17 before the run.
  CITY = the object's site (site 'Unknown' left out). Phrase cities = distinct sites among its carriers.
  MANY-CITY = found in 5 or more cities; ONE-CITY = exactly one city (among phrases with 8 or more carriers).
  SMALL SITE = a site with fewer than 100 objects in the catalogue (Mohenjo-daro, Harappa, Dholavira, Kalibangan, Lothal are large).
Tests:
  T1 (one-city phrases): in which cities are they? Control: draws of the same number of objects (same kind mix) from the whole catalogue:
     chance that all land in one city, and chance that all land in a small site. Expectation written first: the one-city phrases sit in
     Mohenjo-daro or Harappa (large sites), not small sites, because phrases with 8+ carriers can only be one-city where the sample is big.
  T2 (many-city phrases and the overseas animal): among SEALS carrying the phrase, share with the short-horned bull with trough (Gaur) vs
     seals drawn at random from the same sites (within-site shuffle, 5,000 draws). Pooled over all many-city phrases and one by one.
     Expectation: many-city phrases carry the overseas animal MORE than their sites predict.
  T3 (found abroad): carriers in the Gulf, Mesopotamia, Iran, Central Asia vs the base rate of abroad objects among carriers' kind mix
     (binomial, per phrase) and which phrases sit on abroad seals.
  T4: do phrases with more cities carry the overseas animal more? Spearman correlation of cities vs share of Gaur seals over the top 100;
     control: shuffle the Gaur counts among phrases of the same carrier-count band 5,000 times.
Output: work_data/phrases/intercity.csv, intercity_abroad.csv, log_4.txt
"""
from phrases_common import *
from scipy.stats import spearmanr, binom
LOG = open(f'{OUTP}/log_4.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()
rng = np.random.default_rng(4)
O = build_objects(); O = O[O.site != 'Unknown'].copy()
size = O.site.value_counts(); SMALL = set(size[size < 100].index)
say('sites', len(size), 'large:', size[size >= 100].to_dict())
A = pd.read_csv(f'{OUTP}/atlas_all.csv', dtype={'phrase': str}); At = pd.read_csv(f'{OUTP}/atlas.csv', dtype={'phrase': str})
CAR = pd.read_csv(f'{OUTP}/carriers.csv', dtype={'phrase': str}); CAR['obj'] = CAR.obj.astype(str)
CAR = CAR[CAR.obj.isin(O.index)]
base_abroad = O.abroad.mean(); base_shorthorn = (O[O.kind == 'seal'].animal == SHORTHORN).mean()
say('base rates: abroad objects', round(base_abroad, 4), ' Gaur among seals', round(base_shorthorn, 4))
rows = []
for r in A.itertuples():
    S = O.loc[CAR[CAR.phrase == r.phrase].obj]
    sc = S.site.value_counts()
    seals = S[S.kind == 'seal']
    rows.append(dict(phrase=r.phrase, group=r.group, n_objects=len(S), n_cities=len(sc), cities='; '.join(f'{k} {v}' for k, v in sc.items()),
                     top_city=sc.index[0], small_city_objects=int(S.site.isin(SMALL).sum()), n_seals=len(seals),
                     gaur_seals=int((seals.animal == SHORTHORN).sum()), abroad=int(S.abroad.sum()),
                     bult_seals=int((seals.animal == 'Bult').sum()), in_top100=r.phrase in set(At.phrase)))
I = pd.DataFrame(rows)
# T1
one = I[(I.n_cities == 1) & (I.n_objects >= 8)]
say('\nT1 one-city phrases (8+ carriers):', len(one))
kind_pool = {k: O[O.kind == k].index.values for k in O.kind.unique()}
for r in one.itertuples():
    S = O.loc[CAR[CAR.phrase == r.phrase].obj]; km = S.kind.value_counts()
    D = 3000; n1 = ns = 0
    for t in range(D):
        sel = np.concatenate([rng.choice(kind_pool[k], n, replace=False) for k, n in km.items()])
        st = O.loc[sel, 'site']
        n1 += st.nunique() == 1; ns += st.isin(SMALL).all()
    say(f'  {r.phrase:14s} city {r.top_city:14s} objects {r.n_objects:3d} city is small: {r.top_city in SMALL}; random same-kind draw all in one city {(n1 + 1) / (D + 1):.4f}, all in small sites {(ns + 1) / (D + 1):.4f}')
I.loc[one.index, 'one_city'] = True
# one-city but weaker: share in the top city >= 90% with 8+ carriers
near = I[(I.n_objects >= 8) & (I.n_cities > 1)].copy()
near['top_share'] = [max(int(x.split()[-1]) for x in c.split('; ')) / n for c, n in zip(near.cities, near.n_objects)]
say('\nphrases with 90%+ in one city (8+ carriers, 2+ cities):', int((near.top_share >= 0.9).sum()), near[near.top_share >= 0.9][['phrase', 'top_city', 'top_share', 'cities']].to_string())
small_only = I[(I.small_city_objects / I.n_objects >= 0.5) & (I.n_objects >= 8)]
say('\nphrases whose carriers are mostly (50%+) at small sites (8+ carriers):', len(small_only), small_only[['phrase', 'n_objects', 'small_city_objects', 'cities']].to_string())
# T2
many = I[I.n_cities >= 5]
say('\nT2 many-city phrases (5+ cities):', len(many), 'of', len(I), ' in top 100:', int(many.in_top100.sum()))
def gaur_test(rowsel, D=5000):
    obs = int(rowsel.gaur_seals.sum()); n_sites = collections.Counter(); 
    for ph in rowsel.phrase:
        S = O.loc[CAR[CAR.phrase == ph].obj]; S = S[S.kind == 'seal']
        n_sites.update(S.site.tolist())
    pools = {s: (O[(O.site == s) & (O.kind == 'seal')].animal == SHORTHORN).values for s in n_sites}
    null = np.zeros(D)
    for t in range(D):
        null[t] = sum(rng.choice(pools[s], n, replace=n > len(pools[s])).sum() for s, n in n_sites.items())
    return obs, float(null.mean()), (np.sum(null >= obs) + 1) / (D + 1), sum(n_sites.values())
o, e, p, n = gaur_test(many); say(f'  pooled many-city: Gaur seals {o} of {n} seal-carriers (within-site expectation {e:.1f}), P {p:.4f}')
few = I[(I.n_cities < 5) & (I.n_objects >= 8)]
o, e, p, n = gaur_test(few); say(f'  pooled fewer than 5 cities: Gaur seals {o} of {n} seal-carriers (within-site expectation {e:.1f}), P {p:.4f}')
say('  one by one (many-city), Gaur seals / seals, expected, P:')
many_rows = []
for r in many.itertuples():
    o, e, p, n = gaur_test(many[many.phrase == r.phrase], D=2000)
    many_rows.append((r.phrase, o, n, e, p)); say(f'    {r.phrase:14s} {o}/{n}  expected {e:.2f}  P {p:.4f}  cities {r.n_cities}  abroad {r.abroad}')
many = many.copy(); many['gaur_expected'] = [x[3] for x in many_rows]; many['gaur_P'] = [x[4] for x in many_rows]
# T3
say('\nT3 abroad objects by phrase (binomial vs base rate of the whole catalogue):')
ab = []
for r in I[I.n_objects >= 8].itertuples():
    pb = 1 - binom.cdf(r.abroad - 1, r.n_objects, base_abroad) if r.abroad else 1.0
    if r.abroad: ab.append(dict(phrase=r.phrase, n_objects=r.n_objects, abroad=r.abroad, expected=round(r.n_objects * base_abroad, 2), P=pb, group=r.group))
AB = pd.DataFrame(ab).sort_values('P'); AB.to_csv(f'{OUTP}/intercity_abroad.csv', index=False)
say(AB.head(15).to_string())
say('total abroad objects in catalogue', int(O.abroad.sum()), ' abroad carriers of any listed phrase:', CAR[CAR.obj.isin(O[O.abroad].index)].obj.nunique())
# the abroad objects: which phrases do they carry
ao = CAR[CAR.obj.isin(O[O.abroad].index)]
say(ao.groupby('phrase').obj.nunique().sort_values(ascending=False).head(10).to_string())
# T4
T = I[I.in_top100 & (I.n_seals >= 5)].copy()
T['gshare'] = T.gaur_seals / T.n_seals
rho, pr = spearmanr(T.n_cities, T.gshare)
D = 5000; nul = np.zeros(D)
T['band'] = pd.qcut(T.n_seals, 4, labels=False, duplicates='drop')
for t in range(D):
    g = T.gaur_seals.values.copy()
    for b in T.band.unique():
        ix = np.where(T.band.values == b)[0]; g[ix] = rng.permutation(g[ix])
    nul[t] = spearmanr(T.n_cities, g / T.n_seals)[0]
say(f'\nT4 Spearman(cities, Gaur share) over {len(T)} phrases: rho {rho:.3f}; shuffled (Gaur counts mixed within carrier-count band) mean {np.nanmean(nul):.3f}, P(rho >= obs) {(np.sum(nul >= rho) + 1) / (D + 1):.4f}')
I = I.merge(many[['phrase', 'gaur_expected', 'gaur_P']], on='phrase', how='left')
I.to_csv(f'{OUTP}/intercity.csv', index=False)
say('\nCity-count table over all 136:', I.n_cities.value_counts().sort_index().to_dict())
say('top 100 city-count table:', I[I.in_top100].n_cities.value_counts().sort_index().to_dict())
