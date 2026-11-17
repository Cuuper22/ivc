#!/usr/bin/env python3
"""SIZE step 3b, redesign of the city-stability test (written 2026-11-17 after step 3 went against, before this run).
Change: only title/closer signs with 5+ seals on BOTH sides (thin cells removed), and the null compares to random sets
of other signs with 5+ on both sides. Prediction: Mohenjo-daro vs Harappa Spearman above 0.5 with the thin signs gone.
New idea run alongside: the comb 400 effect alone, city by city (is 'comb = small' the one stable rung?)."""
from size_common import *
import importlib.util, sys
from scipy.stats import spearmanr
spec = importlib.util.spec_from_file_location('t3', f'{ROOT}/work_scripts/size_3_titles.py')
S = table()
TC = [s for s, v in V2.items() if v in ('TITLE', 'CLOSER')]
def resid(Sub):
    Bf, _ = base_X(Sub); B = Bf.values; y = Sub.logA.values
    wb, _ = ridge_fit(B, np.zeros((len(Sub), 0)), y, 0)
    return y - ridge_pred(B, np.zeros((len(Sub), 0)), wb, np.zeros(0))
def ladder(Sub):
    r = resid(Sub); t = list(Sub.tok); c = collections.Counter(s for x in t for s in set(x))
    return {s: (r[[s in x for x in t]].mean(), c[s]) for s in c}
for minn in (5, 8):
  for nmA, A, nmB, B in [('MD', S[S.siteg == 'MD'], 'HP', S[S.siteg == 'HP']),
                         ('MD', S[S.siteg == 'MD'], 'all other cities', S[S.siteg != 'MD']),
                         ('early+middle', S[S.bin.isin(['early', 'middle'])], 'late', S[S.bin == 'late'])]:
    la, lb = ladder(A), ladder(B)
    both = [s for s in la if s in lb and la[s][1] >= minn and lb[s][1] >= minn]
    tc = [s for s in both if s in TC]; other = [s for s in both if s not in TC]
    if len(tc) < 3: print(minn, nmA, nmB, 'too few', tc); continue
    rho = spearmanr([la[s][0] for s in tc], [lb[s][0] for s in tc]).correlation
    rr = np.random.default_rng(5); null = np.array([spearmanr(*zip(*[(la[s][0], lb[s][0]) for s in rr.choice(other, len(tc), replace=False)])).correlation for _ in range(2000)])
    print(f'min {minn}: {nmA} vs {nmB}: signs {" ".join(tc)}: rho {rho:.2f}; random other-sign sets mean {np.nanmean(null):.2f}, share at or above {np.nanmean(null >= rho):.3f}')
    print('    ', '  '.join(f'{s}:{la[s][0]:+.2f}/{lb[s][0]:+.2f}' for s in tc))
S['res'] = resid(S)
for site in ['MD', 'HP', 'DHO', 'LOT', 'CHD', 'KLB', 'other']:
    sub = S[S.siteg == site]; r = resid(sub); m = sub.tok.map(lambda t: '400' in t).values
    if m.sum(): print(f'comb 400 at {site}: {m.sum()} seals, mean residual {r[m].mean():+.3f}; seals without {r[~m].mean():+.3f}')
