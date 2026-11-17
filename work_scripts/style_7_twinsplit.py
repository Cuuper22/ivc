#!/usr/bin/env python3
"""STYLE step 7 (after the fact, exploring): twin and near-twin pairs split by same city / two cities.
Chance for a same-city pair = sum of squared style shares of that city (main styles), averaged over the pairs;
P = binomial upper tail at that mean chance."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_common import *
from scipy.stats import binom
P = pd.read_csv(f'{OUT}/twin_styles.csv', dtype=str).fillna('')
S = pd.read_csv(f'{OUT}/styles.csv', dtype=str).fillna('')
S = S[S.sty.isin(['S1', 'S2', 'S3', 'S4', 'S5'])]
sh = pd.crosstab(S.city, S.sty, normalize='index'); ch = (sh ** 2).sum(1)
P['same'] = P.sa == P.sb; P['one_city'] = P.ca == P.cb
for (oc, k), g in P.groupby(['one_city', 'kind']):
    if oc: c = g.ca.map(ch).mean()
    else: c = np.mean([sum(sh.loc[a].get(s, 0) * sh.loc[b].get(s, 0) for s in sh.columns) for a, b in zip(g.ca, g.cb)])
    n = len(g); x = int(g.same.sum())
    print(f'{"same city" if oc else "two cities"} {k}: {x} of {n} same style, chance {c:.2f} ({c * n:.1f}), P {binom.sf(x - 1, n, c):.3f}')
