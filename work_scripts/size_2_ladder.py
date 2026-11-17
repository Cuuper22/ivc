#!/usr/bin/env python3
"""SIZE step 2: the ladder of signs.  Written 2026-11-17 before any number.

Model (d) (baseline length + site + format, one ridge weight per sign) fitted on ALL complete seals with a size, penalty
by 5-fold CV over texts; 400 bootstrap refits (texts resampled with replacement, same penalty) give each sign's 90%
interval. Signs in 4+ seals are ranked.
Held-out check: weights fitted on half A only; the 25 biggest and 25 smallest signs (4+ seals in A); in half B each seal
carrying one is compared to the median logA of half-B seals of its own site, length and format (fallback site x length,
then length). Share above the median: expected 50% if the sign says nothing.
Job of each sign from frame v2; pictures from the blind describers (crosswalk) or the shape list.

PREDICTIONS:
  Q1  The big end is dominated by after-jar titles and the jar-then-man ending (090, 400?, 679, 621) and front words;
      the small end by porters (151-158), comb-count signs and count-line things (390, 156).
  Q2  On half B, seals carrying a top-25 big sign sit above their cell median at least 60% of the time; top-25 small
      below it at least 60%.
  Q3  Big signs are over-represented in the TITLE and CLOSER classes against their share of all ranked signs.
"""
from size_common import *

S = table(); y = S.logA.values; g = S.signs.values
toks = list(S.tok)
Bf, lv = base_X(S); B = Bf.values
cnt = collections.Counter(s for t in toks for s in set(t))
signs = sorted(s for s, n in cnt.items() if n >= 2)
Z = sign_X(toks, signs)
lam = ridge_cv(B, Z, y, g, 0)
wb, wz = ridge_fit(B, Z, y, lam)
log('S2', f'{len(S)} seals, {len(signs)} signs in 2+ seals, penalty {lam}')
NB = 400
ug = np.unique(g); gi = {t: np.where(g == t)[0] for t in ug}
r = np.random.default_rng(1)
BW = np.zeros((NB, len(signs)))
for b in range(NB):
    pick = r.choice(ug, len(ug)); ix = np.concatenate([gi[t] for t in pick])
    _, BW[b] = ridge_fit(B[ix], Z[ix], y[ix], lam)
    if (b + 1) % 100 == 0: log('S2', f'  bootstrap {b+1}/{NB}')
# raw residual from baseline (no sign weights) for each sign, as a plain second view
wb0, _ = ridge_fit(B, np.zeros((len(S), 0)), y, 0); res = y - ridge_pred(B, np.zeros((len(S), 0)), wb0, np.zeros(0))
S['resid'] = res
L = pd.DataFrame(dict(sign=signs, seals=[cnt[s] for s in signs], weight=wz, lo=np.percentile(BW, 5, 0), hi=np.percentile(BW, 95, 0),
                      mean_resid=[res[Z[:, j] > 0].mean() for j in range(len(signs))]))
L['job'] = L.sign.map(job); L['v2'] = L.sign.map(lambda s: V2.get(s, 'PERSONAL')); L['picture'] = L.sign.map(pic_book)
L['pct_bigger'] = (np.exp(L.weight) - 1) * 100
L = L.sort_values('weight', ascending=False)
L.to_csv(f'{OUT}/ladder_all.csv', index=False)
R4 = L[L.seals >= 4].copy()
log('S2', f'ranked signs (4+ seals): {len(R4)}; interval clear of 0: above {int((R4.lo > 0).sum())}, below {int((R4.hi < 0).sum())}')

# held-out check
tr = split(S, 0); te = ~tr
cntA = collections.Counter(s for t, k in zip(toks, tr) if k for s in set(t))
sA = sorted(s for s, n in cntA.items() if n >= 2)
ZA = sign_X([t for t, k in zip(toks, tr) if k], sA)
lamA = ridge_cv(B[tr], ZA, y[tr], g[tr], 0)
_, wA = ridge_fit(B[tr], ZA, y[tr], lamA)
WA = pd.Series(wA, sA)
elig = [s for s in sA if cntA[s] >= 4]
big = list(WA[elig].sort_values(ascending=False).index[:25]); small = list(WA[elig].sort_values().index[:25])
SB = S[te].copy(); medB = cell_medians(SB, SB.logA.values); SB['above'] = SB.logA.values > medB; SB['tie'] = SB.logA.values == medB
rows = []
for grp, lst in (('big', big), ('small', small)):
    for s in lst:
        m = SB[SB.tok.map(lambda t: s in t) & ~SB.tie]
        rows.append(dict(group=grp, sign=s, weight_A=WA[s], seals_A=cntA[s], seals_B=len(m), above_B=int(m.above.sum())))
H = pd.DataFrame(rows); H.to_csv(f'{OUT}/ladder_heldout.csv', index=False)
from math import comb
def binom_p(k, n, more=True):
    if n == 0: return float('nan')
    return sum(comb(n, i) for i in (range(k, n + 1) if more else range(0, k + 1))) / 2 ** n
for grp in ('big', 'small'):
    lst = big if grp == 'big' else small
    m = SB[SB.tok.map(lambda t: any(s in t for s in lst)) & ~SB.tie]
    if grp == 'big': m = m[~m.tok.map(lambda t: any(s in t for s in small))]
    else: m = m[~m.tok.map(lambda t: any(s in t for s in big))]
    k = int(m.above.sum()); n = len(m)
    log('S2', f'held-out half B, seals with a top-25 {grp} sign (and none of the other list): {k} of {n} above their cell median '
              f'({k/max(n,1):.1%}); one-sided P {binom_p(k, n, grp == "big"):.2g}')
    signs_ok = H[H.group == grp]; ok = ((signs_ok.above_B / signs_ok.seals_B.replace(0, np.nan)) > 0.5) if grp == 'big' else ((signs_ok.above_B / signs_ok.seals_B.replace(0, np.nan)) < 0.5)
    log('S2', f'   signs pointing the predicted way on half B: {int(ok.sum())} of {int(signs_ok.seals_B.gt(0).sum())} with half-B seals')
    with open(f'{OUT}/ladder_heldout_summary.txt', 'a') as f: f.write(f'{grp}: {k} of {n} above cell median; P {binom_p(k, n, grp == "big"):.3g}; signs right way {int(ok.sum())} of {int(signs_ok.seals_B.gt(0).sum())}\n')

# top / bottom 25 (full data)
T25 = pd.concat([R4.head(25).assign(end='big'), R4.tail(25).iloc[::-1].assign(end='small')])
T25.to_csv(f'{OUT}/ladder_top25.csv', index=False)
for _, x in T25.iterrows():
    log('S2', f'{x.end:5s} {x.sign} {x.picture[:28]:28s} {x.job:20s} n={x.seals:3d} w={x.weight:+.3f} [{x.lo:+.3f},{x.hi:+.3f}] resid {x.mean_resid:+.3f}')
# Q3: job mix
allj = R4.v2.value_counts(normalize=True)
for e in ('big', 'small'):
    mix = T25[T25.end == e].v2.value_counts()
    log('S2', f'{e} end job mix: ' + ', '.join(f'{k} {v} (exp {allj.get(k,0)*25:.1f})' for k, v in mix.items()))
# by class: mean weight with sign-dealt control (class labels dealt over ranked signs, 2000)
cls_mean = R4.groupby('v2').weight.agg(['mean', 'size'])
rr = np.random.default_rng(3); labs = R4.v2.values; w = R4.weight.values
null = collections.defaultdict(list)
for _ in range(2000):
    p = rr.permutation(labs)
    for c in cls_mean.index: null[c].append(w[p == c].mean())
cls_mean['p_high'] = [np.mean(np.array(null[c]) >= cls_mean.loc[c, 'mean']) for c in cls_mean.index]
cls_mean['p_low'] = [np.mean(np.array(null[c]) <= cls_mean.loc[c, 'mean']) for c in cls_mean.index]
cls_mean.sort_values('mean', ascending=False).to_csv(f'{OUT}/ladder_by_job.csv')
log('S2', 'mean size weight by job (signs in 4+ seals), P from 2000 label deals:\n' + cls_mean.sort_values('mean', ascending=False).round(3).to_string())
