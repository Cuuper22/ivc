#!/usr/bin/env python3
"""SIZE step 8: what is size?  Written 2026-11-17 after steps 1-7, before this run.

Held-out share of size variation over the same 20 text splits as step 1, adding one block at a time:
  length -> + site + format -> + time bin -> + text (one ridge weight per sign) -> + stone marks (stand letter, animal,
  material). And: baseline + the comb 400 alone (one column), to see how much of the text's share is one sign.
New idea for the restoration line (step 6 went against): can size alone tell a comb-ending seal (740-400 / ...400) from
a jar-ending seal (...740)? Share of pairs (one comb-ending, one jar-ending, same site-length-format residual) in which
the comb seal is the smaller (0.5 = no help).
PREDICTIONS:  D1 the stone-mark block adds more than the text block (step 5 suggests it).  D2 comb alone carries at
least a third of the text block.  D3 the comb seal is the smaller in at least 65% of pairs.
"""
from size_common import *

S = table(); y = S.logA.values; toks = list(S.tok)
def dummies(col):
    lv = sorted(S[col].astype(str).unique()); return np.column_stack([(S[col].astype(str) == v).astype(float) for v in lv[1:]])
Bf, _ = base_X(S); Bb = Bf.values
La = Bf[[c for c in Bf.columns if c.startswith('L=')]].values
BIN = dummies('bin'); MARK = np.hstack([dummies('stand5'), dummies('animal'), dummies('material')])
COMB = np.array([[1.0 if '400' in t else 0.0] for t in toks])
rows = []
for sd in range(1, 21):
    tr = split(S, sd); te = ~tr
    c = collections.Counter(s for t, k in zip(toks, tr) if k for s in set(t)); sg = sorted(s for s, n in c.items() if n >= 2)
    Z = sign_X(toks, sg); g = S.signs.values
    res = {}
    def run(B, Zp, name):
        lam = ridge_cv(B[tr], Zp[tr], y[tr], g[tr], 0) if Zp.shape[1] else 0
        wb, wz = ridge_fit(B[tr], Zp[tr], y[tr], lam); res[name] = r2(y[te], ridge_pred(B[te], Zp[te], wb, wz))
    E = np.zeros((len(S), 0))
    run(La, E, '1 length'); run(Bb, E, '2 + site + format'); run(np.hstack([Bb, BIN]), E, '3 + time bin')
    run(np.hstack([Bb, BIN]), Z, '4 + text (sign weights)'); run(np.hstack([Bb, BIN, MARK]), Z, '5 + stand, animal, material')
    run(np.hstack([Bb, BIN, MARK]), E, '5b site, format, bin + stone marks, no text')
    run(np.hstack([Bb, COMB]), E, 'b + comb 400 only'); run(Bb, Z, 'b + text')
    rows.append(res)
R = pd.DataFrame(rows)
log('S8', 'held-out share of size variation, mean (min-max) over 20 text splits:\n' +
    pd.DataFrame(dict(mean=R.mean(), lo=R.min(), hi=R.max())).round(3).to_string())
R.to_csv(f'{OUT}/decide_splits.csv', index=False)
log('S8', f'text block: {(R["4 + text (sign weights)"]-R["3 + time bin"]).mean():+.3f}; stone-mark block: {(R["5 + stand, animal, material"]-R["4 + text (sign weights)"]).mean():+.3f}; '
          f'comb alone over baseline {(R["b + comb 400 only"]-R["2 + site + format"]).mean():+.3f} of text over baseline {(R["b + text"]-R["2 + site + format"]).mean():+.3f}')
# comb vs jar pairs
wb, _ = ridge_fit(Bb, np.zeros((len(S), 0)), y, 0); S['res'] = y - ridge_pred(Bb, np.zeros((len(S), 0)), wb, np.zeros(0))
cm = S[S.tok.map(lambda t: t[-1] == '400')].res.values; jr = S[S.tok.map(lambda t: t[-1] == '740')].res.values
auc = np.mean(cm[:, None] < jr[None, :]) + 0.5 * np.mean(cm[:, None] == jr[None, :])
log('S8', f'comb-final seals {len(cm)} vs jar-final {len(jr)}: comb seal smaller in {auc:.1%} of pairs (residual size)')
with open(f'{OUT}/decide.txt', 'w') as f:
    f.write(pd.DataFrame(dict(mean=R.mean(), lo=R.min(), hi=R.max())).round(4).to_string() + f'\ncomb smaller than jar in {auc:.4f} of pairs; n comb {len(cm)} jar {len(jr)}\n')
