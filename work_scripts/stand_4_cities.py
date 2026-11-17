#!/usr/bin/env python3
"""Step 2c: city mixes of the letter, stones whose text looks like another city's, and same-hand twins.

Plain words: CITY MIX = share of each letter among a city's unicorn seals. TEXT-HOME SCORE = how much a seal's text
looks like a Harappa text rather than a Mohenjo-daro text, from a sign-count model (naive Bayes: each sign's rate in
the other texts of each city, the seal itself left out). HAND = same or different carver, judged on photos in the
twins job (work_data/twins/photo_tally.csv).

PREDICTIONS, fixed first:
 WORKSHOP: each city has its own mix (chi-square P < 0.001 across the big cities, holding in each time bin);
   Mohenjo-daro seals with the most Harappa-like texts carry Harappa's mix (more W) because they were cut there
   and carried; twin pairs judged same hand share the letter (>= 4 of the same-hand unicorn pairs).
 HOUSEHOLD: city mixes differ only through size (W is big); Harappa-like texts at Mohenjo-daro carry the
   Mohenjo-daro mix; same hand says nothing about the letter.
"""
from stand_common import *
from scipy.stats import chi2_contingency, fisher_exact
rng = np.random.default_rng(4)
S = stand_seals()
u = S[S.stand5 != ''].drop_duplicates('obj').reset_index(drop=True)
big = u[u.site.isin(['Mohenjo-daro', 'Harappa', 'Lothal', 'Chanhu-daro', 'Dholavira', 'Kalibangan'])]
ct = pd.crosstab(big.site, big.stand5); chi, p, dof, _ = chi2_contingency(ct)
log('mix', f'chi2 {chi:.1f} dof {dof} P {p:.2g}'); print((ct.div(ct.sum(1), axis=0) * 100).round(0).assign(n=ct.sum(1)).to_string())
ct.to_csv(f'{OUT}/city_mix.csv')
for b in ['early', 'middle', 'late']:
    g = big[(big.bin == b) & big.site.isin(['Mohenjo-daro', 'Harappa'])]
    c = pd.crosstab(g.site, g.stand5)
    if c.shape[0] == 2: log('mix by bin', b, c.to_dict('index'), 'P', f'{chi2_contingency(c)[1]:.2g}')
# size held: city mix inside size thirds (pooled thirds over MD + Harappa)
g = big[big.site.isin(['Mohenjo-daro', 'Harappa']) & big.logsz.notna()].copy()
g['s3'] = pd.qcut(g.logsz, 3, labels=['small', 'mid', 'big'])
for s3, h in g.groupby('s3'):
    c = pd.crosstab(h.site, h.stand5); log('mix by size third', s3, 'W share MD %.2f HP %.2f' % (c.loc['Mohenjo-daro', 'W'] / c.loc['Mohenjo-daro'].sum(), c.loc['Harappa', 'W'] / c.loc['Harappa'].sum()), 'P', f'{chi2_contingency(c)[1]:.2g}')

# text-home score
A = S[S.site.isin(['Mohenjo-daro', 'Harappa']) & (S.signs != '')].drop_duplicates('face')
from collections import Counter
cnt = {c: Counter() for c in ['Mohenjo-daro', 'Harappa']}; tot = Counter(); ntxt = Counter()
for s, c in zip(A.signs, A.site):
    for x in set(s.split('-')): cnt[c][x] += 1
    ntxt[c] += 1
V = len(set(cnt['Mohenjo-daro']) | set(cnt['Harappa']))
def score(signs, site):
    sc = np.log((ntxt['Harappa'] - (site == 'Harappa')) / (ntxt['Mohenjo-daro'] - (site == 'Mohenjo-daro')))
    for x in set(signs.split('-')):
        if x == '000': continue
        h = cnt['Harappa'][x] - (site == 'Harappa'); m = cnt['Mohenjo-daro'][x] - (site == 'Mohenjo-daro')
        sc += np.log((h + 0.5) / (ntxt['Harappa'] + V * 0.0 + 1)) - np.log((m + 0.5) / (ntxt['Mohenjo-daro'] + 1))
    return sc
A = A.assign(hs=[score(s, c) for s, c in zip(A.signs, A.site)])
from sklearn.metrics import roc_auc_score
log('text-home', f'score separates Harappa from Mohenjo-daro texts (left-one-out) AUC {roc_auc_score(A.site == "Harappa", A.hs):.3f}')
um = u[(u.site == 'Mohenjo-daro') & (u.signs != '')].copy(); um['hs'] = [score(s, 'Mohenjo-daro') for s in um.signs]
uh = u[(u.site == 'Harappa') & (u.signs != '')].copy(); uh['hs'] = [score(s, 'Harappa') for s in uh.signs]
q = um.hs.quantile(0.9); top = um[um.hs >= q]; rest = um[um.hs < q]
wt, wr = (top.stand5 == 'W').mean(), (rest.stand5 == 'W').mean()
# within size: compare W share of top decile with rest, matched on size third
um['s3'] = pd.qcut(um.logsz, 3, labels=False)
exp = sum(((rest.assign(s3=um.s3)[um.s3.loc[rest.index] == k].stand5 == 'W').mean()) * (um.loc[top.index].s3 == k).sum() for k in range(3)) / um.loc[top.index].s3.notna().sum()
log('outliers', f'Mohenjo-daro seals, most Harappa-like tenth of texts ({len(top)} seals): W {wt:.2f} against {wr:.2f} for the rest; size-matched expectation {exp:.2f}; Harappa itself W {(uh.stand5=="W").mean():.2f}')
sims = [(rng.permutation(um.stand5.values)[:len(top)] == 'W').mean() for _ in range(5000)]
log('outliers', f'dealt W share for {len(top)} random MD seals {np.mean(sims):.2f}, P(as high) {np.mean(np.array(sims) >= wt):.3f}')
print(pd.crosstab(um.hs >= q, um.stand5).to_string())
qh = uh.hs.quantile(0.1); toph = uh[uh.hs <= qh]
log('outliers', f'Harappa seals, most MD-like tenth ({len(toph)}): W {(toph.stand5=="W").mean():.2f} against {(uh[uh.hs>qh].stand5=="W").mean():.2f}')
pd.concat([top.assign(group='MD most Harappa-like'), toph.assign(group='HP most MD-like')])[['group', 'cisi', 'site', 'signs', 'stand5', 'hs', 'area_mm2', 'building']].to_csv(f'{OUT}/city_outliers.csv', index=False)

# same-hand twins
t = pd.read_csv(f'{ROOT}/work_data/twins/photo_tally.csv', dtype=str).fillna('')
tt = t[(t.stand_a != '') & (t.stand_b != '')]
for h, g in tt.groupby('hand'):
    log('twins hand', h, f'{(g.stand_a == g.stand_b).sum()} of {len(g)} share the letter', g[['a', 'b', 'stand_a', 'stand_b', 'cross']].values.tolist())

# Rival check: is the text-home score just a detector of texts that W seals carry anywhere?
# If so, inside Harappa itself the more Harappa-like texts would also carry more W.
med = uh.hs.median()
log('rival', f'inside Harappa: W share upper half of score {(uh[uh.hs>=med].stand5=="W").mean():.2f} ({(uh.hs>=med).sum()}), lower half {(uh[uh.hs<med].stand5=="W").mean():.2f}')
from scipy.stats import spearmanr
log('rival', 'inside Mohenjo-daro without the top tenth: Spearman score vs W', spearmanr(rest.hs, rest.stand5 == 'W'))
log('rival', 'top-tenth MD texts with W:', top[top.stand5 == 'W'][['cisi', 'signs']].values.tolist()[:40])
