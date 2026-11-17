#!/usr/bin/env python3
"""SIZE step 4: crest houses by size.  Written 2026-11-17 before any number.

House = crest = first name sign (twins_common.crest_of: first sign after a front word + slot and any numbers).
Residual size = logA minus the baseline (length + site + format) fit on all complete seals.
House size = mean residual of the house's seals (agent seals [...] 740 090 left out of the house mean).
Spread test: between-house sum of squares (houses with 6+ seals) against 2,000 deals of the house labels among seals of
the same site.
Fame of a house: (1) agent seals naming it: complete seals ending 740-090 whose crest is the house, per house seal;
(2) cities: number of different sites with any inscribed object (any tier) carrying the house's crest;
(3) clay impressions: sealings and stamped pots (work_data/stamps/objects.csv) with that crest, per house seal.
Spearman of house size against each, P from 5,000 shuffles of the house sizes.

PREDICTIONS:
  K1  The spread between houses is larger than the deals give (P below 0.05).
  K2  Bigger-seal houses have more agents, more cities and more impressions (all three Spearman positive, at least
      one with P below 0.05).
  K3  The fish crests (220 231 233 235 240) sit above the median house.
"""
from size_common import *
from scipy.stats import spearmanr

S = table()
Bf, _ = base_X(S); B = Bf.values; y = S.logA.values
wb, _ = ridge_fit(B, np.zeros((len(S), 0)), y, 0); S['res'] = y - ridge_pred(B, np.zeros((len(S), 0)), wb, np.zeros(0))
S['agent'] = S.signs.str.endswith('740-090')
H = S[~S.agent & (S.crest != '')]
cnt = H.crest.value_counts(); houses = list(cnt[cnt >= 6].index)
log('S4', f'houses with 6+ non-agent complete seals: {len(houses)}')
Hh = H[H.crest.isin(houses)]
def between(res, lab):
    df = pd.DataFrame(dict(r=res, c=lab)); g = df.groupby('c').r.agg(['mean', 'size'])
    return (g['size'] * (g['mean'] - df.r.mean()) ** 2).sum()
real = between(Hh.res.values, Hh.crest.values)
rr = np.random.default_rng(11); null = []
for _ in range(2000):
    lab = Hh.crest.values.copy()
    for _, ix in Hh.reset_index(drop=True).groupby('siteg').indices.items(): lab[ix] = lab[rr.permutation(ix)]
    null.append(between(Hh.res.values, lab))
null = np.array(null)
log('S4', f'between-house spread {real:.2f} against dealt within site mean {null.mean():.2f} (max {null.max():.2f}); P {np.mean(null >= real):.4f}')

O = pd.read_csv(f'{ROOT}/work_data/stamps/objects.csv', dtype=str).fillna('')
O = O[O.signs != '']
O['crest'] = O.signs.map(crest_of)
imp = O[O.tier.isin(['sealing', 'stamped pot'])]
rows = []
for c in houses:
    m = Hh[Hh.crest == c]
    rows.append(dict(crest=c, picture=pic(c), blind=pic_book(c), job=job(c), seals=len(m), size=m.res.mean(),
                     se=m.res.std() / np.sqrt(len(m)), median_area=float(np.exp(m.logA).median()),
                     agents=int((S.agent & (S.crest == c)).sum()), cities=O[O.crest == c].site.nunique(),
                     impressions=int((imp.crest == c).sum()), all_objects=int((O.crest == c).sum())))
K = pd.DataFrame(rows).sort_values('size', ascending=False)
K['agents_per_seal'] = K.agents / K.seals; K['imp_per_seal'] = K.impressions / K.seals
K.to_csv(f'{OUT}/crests.csv', index=False)
log('S4', '\n' + K.round(3).to_string(index=False))
for col in ('agents_per_seal', 'agents', 'cities', 'imp_per_seal', 'impressions', 'all_objects'):
    rho = spearmanr(K['size'], K[col]).correlation
    nul = np.array([spearmanr(rr.permutation(K['size'].values), K[col]).correlation for _ in range(5000)])
    log('S4', f'house size vs {col}: Spearman {rho:+.3f}; P (shuffled house sizes) {np.mean(nul >= rho):.4f} for positive')
    with open(f'{OUT}/crests_tests.txt', 'a') as f: f.write(f'{col}: rho {rho:+.3f}, P positive {np.mean(nul >= rho):.4f}\n')
# cities control: cities rise with how many objects a house has; partial out by residual of log cities on log objects
from numpy.polynomial import polynomial as Pn
for col in ('cities', 'impressions', 'agents'):
    x = np.log1p(K.all_objects.values); v = np.log1p(K[col].values)
    b = np.polyfit(x, v, 1); rv = v - np.polyval(b, x)
    rho = spearmanr(K['size'], rv).correlation
    nul = np.array([spearmanr(rr.permutation(K['size'].values), rv).correlation for _ in range(5000)])
    log('S4', f'house size vs {col} beyond what its object count gives: Spearman {rho:+.3f}; P {np.mean(nul >= rho):.4f}')
fish = {'220', '231', '233', '235', '240', '226', '222', '243'}
log('S4', 'fish crests: ' + ', '.join(f'{c} {s:+.3f}' for c, s in zip(K.crest, K['size']) if c in fish) + f'; median house {K["size"].median():+.3f}')
