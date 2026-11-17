#!/usr/bin/env python3
"""PHRASES step 5c: which count values stand in the numbered slots? Written 2026-11-17 before the run.
For each counted sign X (fish 220, trees 390 / 405 / 407, leaf-on-tree 806), the number sign (v2 class NUM_SHORT, NUM_TALL, NUM_NAME) standing right before X
in distinct first-catalogue texts, with the stroke value of each number sign (from work_data/sign_shapes.csv descriptions). Control: the same
number signs' share before ALL other signs (the general count-sign mix); chi-square of the before-X mix against that general mix, P from 5,000
shuffles of the sign that follows each number sign. PREDICTION: before fish the mix is 2 (tall), 3, 6 and little else (not the general mix of
1, 2, 3, 4); before trees 3, 4, 5, 6; the mixes differ from the general mix (P < 0.01).
Output: work_data/phrases/series_values.csv, log_5c.txt
"""
from phrases_common import *
from frame2_pictures import pic
LOG = open(f'{OUTP}/log_5c.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()
rng = np.random.default_rng(58)
NUMC = {'NUM_SHORT', 'NUM_TALL', 'NUM_NAME'}
T = distinct_texts()
pairs = []   # (number sign, next sign)
for x in T:
    for r in runs(x):
        for a, b in zip(r, r[1:]):
            if v2c(a) in NUMC: pairs.append((a, b))
say('number-sign + next-sign pairs in distinct texts:', len(pairs))
gen = collections.Counter(a for a, b in pairs); nums = sorted(gen)
rows = []
for X in ['220', '390', '405', '407', '806', '700']:
    sub = collections.Counter(a for a, b in pairs if b == X)
    if sum(sub.values()) < 8: continue
    n = sum(sub.values())
    def chi(cnt): return sum((cnt.get(s, 0) - n * gen[s] / len(pairs)) ** 2 / (n * gen[s] / len(pairs)) for s in nums)
    obs = chi(sub); nextarr = np.array([b for a, b in pairs]); numarr = np.array([a for a, b in pairs]); null = np.zeros(5000)
    for t in range(5000):
        sh = rng.permutation(nextarr); c = collections.Counter(numarr[sh == X]); null[t] = chi(c)
    P = (np.sum(null >= obs) + 1) / 5001
    say(f'\nbefore {X} ({pic(X)}): {n} cases; chi2 {obs:.1f} vs shuffle mean {null.mean():.1f}, P {P:.4f}')
    say('  ' + '; '.join(f'{s} {pic(s)} {c} ({c / n:.0%}; general {gen[s] / len(pairs):.0%})' for s, c in sub.most_common()))
    rows.append(dict(counted=X, pic=pic(X), cases=n, chi2=round(obs, 1), null_mean=round(null.mean(), 1), P=P, values='; '.join(f'{s}:{c}' for s, c in sub.most_common())))
pd.DataFrame(rows).to_csv(f'{OUTP}/series_values.csv', index=False)
