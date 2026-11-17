#!/usr/bin/env python3
"""PHRASES step 8: do phrases drift through time? Written 2026-11-17 before the run.
  For each of the 136 phrases: among its dated carriers, trend = (late - early) / dated carriers. Control: the bin labels shuffled among
  objects of the same site and excavation area (the 'shuffle within area' of history.md), 5,000 shuffles; two-sided P on |trend|.
  Counts: phrases with P <= 0.05 against 5% expected by chance; phrases present in all three bins; phrases first seen (earliest dated
  carrier) in the early bin.
PREDICTION (history.md found the formula did not drift): at most 10% of phrases (about 14 of 136) fall under P 0.05; at least 60% of the phrases with
  8+ dated carriers have a carrier in every bin.
Output: work_data/phrases/time_trends.csv, log_8.txt
"""
from phrases_common import *
LOG = open(f'{OUTP}/log_8.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()
rng = np.random.default_rng(8)
O = build_objects(); O = O[O.bin != '']
CAR = pd.read_csv(f'{OUTP}/carriers.csv', dtype={'phrase': str}); CAR['obj'] = CAR.obj.astype(str); CAR = CAR[CAR.obj.isin(O.index)]
phr = sorted(CAR.phrase.unique()); pos = {o: i for i, o in enumerate(O.index)}
M_ = np.zeros((len(phr), len(O)), dtype=np.int8)
pi = {p: i for i, p in enumerate(phr)}
for p, o in zip(CAR.phrase, CAR.obj): M_[pi[p], pos[o]] = 1
val = O.bin.map({'early': -1, 'middle': 0, 'late': 1}).values
grp = pd.factorize(O.site + '|' + O.area)[0]
groups = [np.where(grp == g)[0] for g in np.unique(grp)]
n = M_.sum(1); obs = (M_ @ val) / np.maximum(n, 1)
D = 5000; ge = np.zeros(len(phr))
for t in range(D):
    v = val.copy()
    for ix in groups:
        if len(ix) > 1: v[ix] = v[rng.permutation(ix)]
    s = (M_ @ v) / np.maximum(n, 1); ge += np.abs(s) >= np.abs(obs) - 1e-12
P = (ge + 1) / (D + 1)
b = {k: (M_ * (val == x)).sum(1) for k, x in (('early', -1), ('middle', 0), ('late', 1))}
R = pd.DataFrame(dict(phrase=phr, dated=n, early=b['early'], middle=b['middle'], late=b['late'], trend=np.round(obs, 3), P=P))
R.to_csv(f'{OUTP}/time_trends.csv', index=False)
t = R[R.dated >= 8]
say('phrases with 8+ dated carriers:', len(t), ' P<=0.05:', int((t.P <= 0.05).sum()), '(chance', round(0.05 * len(t), 1), ') P<=0.01:', int((t.P <= 0.01).sum()))
say('present in all three bins:', int(((t.early > 0) & (t.middle > 0) & (t.late > 0)).sum()), 'of', len(t), ' in two or more bins:', int(((t.early > 0).astype(int) + (t.middle > 0) + (t.late > 0) >= 2).sum()))
say(t.sort_values('P').head(10).to_string(index=False))
say('overall mean trend of phrase carriers vs all dated objects (late-early share):', round(float(obs[n >= 8].mean()), 3), ' all objects', round(float(val.mean()), 3))
