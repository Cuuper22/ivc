#!/usr/bin/env python3
"""PHRASES step 3b: redesigned house test (pooled) and P-only place / goods flags, from kinds.csv. Written 2026-11-17 before the run.
Why: single phrases have 10-70 carriers with a findspot among hundreds of buildings, so the shared-building test has little power per phrase;
pooling over the phrases of one group gives it power. PREDICTION: names show excess shared buildings, most of it from copies of one object
(identical text, same building) that vanishes with copies removed; front, ending and count-line phrases show none.
  Z = sum over phrases (observed shared-building carriers - null mean) / sqrt(sum of null variances), 2,000 draws each, building and block,
  raw and with copies removed. P(Z) one-sided from the normal. Also: P-histograms of the city, goods and house tests over the top 100
  (expected under no effect: 5% below 0.05, 0.5% below 0.005), and the PLACE_P / GOODS_P flags (P <= 0.005, any share).
Output: work_data/phrases/kinds_pooled.csv, log_3b.txt
"""
from phrases_common import *
from scipy.stats import norm
LOG = open(f'{OUTP}/log_3b.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()
K = pd.read_csv(f'{OUTP}/kinds.csv', dtype={'phrase': str})
rows = []
for g, X in list(K.groupby('group')) + [('ALL', K)]:
    for lvl, o_, m_, s_, o2, m2, s2 in (('building', 'rep_bld', 'null_rep_bld', 'null_sd_bld', 'rep_bld_dd', 'null_bld_dd', 'null_sd_bld_dd'),
                                         ('block', 'rep_blk', 'null_rep_blk', 'null_sd_blk', 'rep_blk_dd', 'null_blk_dd', 'null_sd_blk_dd')):
        for tag, a, b, c in (('raw', o_, m_, s_), ('copies removed', o2, m2, s2)):
            z = (X[a] - X[b]).sum() / np.sqrt((X[c] ** 2).sum())
            rows.append(dict(group=g, level=lvl, version=tag, phrases=len(X), observed=int(X[a].sum()), expected=round(X[b].sum(), 1), Z=round(z, 2), P=round(1 - norm.cdf(z), 5)))
R = pd.DataFrame(rows); R.to_csv(f'{OUTP}/kinds_pooled.csv', index=False); say(R.to_string(index=False))
for t, col in (('house (min building/block)', 'P_house'), ('city', 'P_city'), ('goods', 'P_goods')):
    p = K[col].dropna(); say(f'{t}: phrases {len(p)}; P<=0.05 {int((p <= 0.05).sum())} (chance {0.05 * len(p):.1f}); P<=0.005 {int((p <= 0.005).sum())} (chance {0.005 * len(p):.2f})')
pl = K[K.P_city <= 0.005]; say('PLACE_P (P_city <= 0.005):', pl[['phrase', 'group', 'top_city', 'top_city_share', 'null_city_share', 'P_city', 'n_obj']].to_string(index=False))
gd = K[K.P_goods <= 0.005]; say('GOODS_P (P_goods <= 0.005):', gd[['phrase', 'group', 'nonseal_share', 'null_nonseal_share', 'P_goods', 'n_obj', 'top_city']].to_string(index=False))
pa = K[(K.P_area <= 0.005)]; say('mound tie P_area <= 0.005:', pa[['phrase', 'top_area', 'top_area_share', 'P_area', 'n_area_known']].to_string(index=False))
