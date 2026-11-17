#!/usr/bin/env python3
"""SIZE step 1: how much of a seal's size is in its text?  Written 2026-11-17 before any number.

Models (fixed here), all predicting logA of a complete seal face, trained on the training half, scored on the test half:
  (a) length only            (b) length + site + format = BASELINE
  (c) baseline + which frame-v2 job classes are present (14 yes/no columns, ridge)
  (d) baseline + one weight per sign (yes/no per sign seen in 2+ training seals, ridge)
  (e) baseline + one weight per fixed phrase (136 phrases of jobs/out/phrases.md, ridge)
  (d+e) both.   Extra checks: (b+bin) baseline + time bin; (d+bin); (d+stand+animal) to see what the stone marks add.
Decoys, 20 each: (d) token dealing within frequency band and cell dealing of sizes; (c) class dealing; (e) phrase dealing.
Outside set: seals whose text has no partner in the second catalogue (that catalogue has no sizes), scored by models
trained on the partnered training half.

PREDICTIONS (committed before running):
  P1  (b) beats (a) clearly (format: bars and round seals differ in size).
  P2  (d) beats (b) on the test half by at least 0.03 of held-out R2, and beats all 20 token-dealt decoys.
  P3  (c) adds less than (d) but more than its class decoys (the closer / title classes carry the rank).
  P4  (e) adds something but less than (d).
  P5  On the outside set (d) still beats (b).
  P6  Over 20 random splits (d) beats (b) in at least 17.
"""
from size_common import *

S = table()
log('S1', f'complete seal faces with a size: {len(S)}; partnered with the second catalogue: {int(S.partnered.sum())}; '
          f'not partnered (outside set): {int((~S.partnered).sum())}')
log('S1', 'second-catalogue new texts with a size: 0 (the second catalogue carries no measurement field)')
y = S.logA.values
band, cnt = freq_bands(list(S.tok))


def fit_all(S, tr, te, toks=None, cmap=None, phrases=None, which=('a', 'b', 'c', 'd', 'e', 'de'), seed=0, extra=None):
    toks = list(S.tok) if toks is None else toks
    cmap = V2 if cmap is None else cmap
    phrases = PHRASES if phrases is None else phrases
    Bf, lv = base_X(S)
    B = Bf.values
    La = Bf[[c for c in Bf.columns if c.startswith('L=')]].values
    if extra is not None: B = np.hstack([B, extra])
    out = {}
    g = S.signs.values
    trc = collections.Counter(s for t, k in zip(toks, tr) if k for s in set(t))
    signs = sorted(s for s, n in trc.items() if n >= 2)
    Zs = {'a': None, 'b': np.zeros((len(S), 0)), 'c': class_X(toks, cmap) if 'c' in which else None,
          'd': sign_X(toks, signs) if ('d' in which or 'de' in which) else None,
          'e': phrase_X(toks, phrases) if ('e' in which or 'de' in which) else None}
    for m in which:
        if m == 'a':
            wb, wz = ridge_fit(La[tr], np.zeros((tr.sum(), 0)), y[tr], 0)
            p = ridge_pred(La[te], np.zeros((te.sum(), 0)), wb, wz)
        else:
            Z = np.hstack([Zs['d'], Zs['e']]) if m == 'de' else Zs[m]
            lam = ridge_cv(B[tr], Z[tr], y[tr], g[tr], seed)
            wb, wz = ridge_fit(B[tr], Z[tr], y[tr], lam)
            p = ridge_pred(B[te], Z[te], wb, wz)
        out[m] = r2(y[te], p)
    return out


tr = split(S, 0); te = ~tr
log('S1', f'headline split: training {tr.sum()} faces ({S.signs[tr].nunique()} texts), test {te.sum()} ({S.signs[te].nunique()} texts)')
R = fit_all(S, tr, te)
log('S1', 'held-out share of size variation:', {k: round(v, 3) for k, v in R.items()})

# extras: bin, stand, animal
def dummies(col):
    lv = sorted(S[col].astype(str).unique())
    return np.column_stack([(S[col].astype(str) == v).astype(float) for v in lv[1:]])
for nm, ex in [('bin', dummies('bin')), ('stand+animal', np.hstack([dummies('stand5'), dummies('animal')])),
               ('bin+stand+animal', np.hstack([dummies('bin'), dummies('stand5'), dummies('animal')]))]:
    Rx = fit_all(S, tr, te, which=('b', 'd'), extra=ex)
    log('S1', f'  with {nm} added to the baseline: b {Rx["b"]:.3f}  d {Rx["d"]:.3f}  (text adds {Rx["d"]-Rx["b"]:+.3f})')
    R[f'b+{nm}'] = Rx['b']; R[f'd+{nm}'] = Rx['d']

# outside set: train on partnered training half, score on all unpartnered
trp = tr & S.partnered.values; teo = ~S.partnered.values
Ro = fit_all(S, trp, teo, which=('a', 'b', 'c', 'd', 'e'))
log('S1', f'outside set ({teo.sum()} faces, texts the second catalogue never had):', {k: round(v, 3) for k, v in Ro.items()})

# decoys
NDEC = 20
dec = collections.defaultdict(list)
for q in range(NDEC):
    tk = deal_tokens(list(S.tok), band, cnt, 700 + q)
    dec['d tokens dealt'].append(fit_all(S, tr, te, toks=tk, which=('d',))['d'])
    dec['c classes dealt'].append(fit_all(S, tr, te, cmap=deal_classes(band, 700 + q), which=('c',))['c'])
    dec['e phrases dealt'].append(fit_all(S, tr, te, phrases=deal_phrases(list(S.tok), PHRASES, 700 + q), which=('e',))['e'])
    # cell dealing: shuffle y within site x length x format
    r = np.random.default_rng(900 + q); yy = y.copy()
    for _, ix in S.groupby(['siteg', 'L', 'fmt']).indices.items():
        yy[ix] = y[r.permutation(ix)]
    y_save = y; y = yy
    Rc = fit_all(S, tr, te, which=('b', 'd'))
    y = y_save
    dec['d sizes dealt in cell (extra over b)'].append(Rc['d'] - Rc['b'])
    log('S1', f'  decoy {q+1}/{NDEC}: d-tokens {dec["d tokens dealt"][-1]:.3f}  c-classes {dec["c classes dealt"][-1]:.3f}  '
              f'e-phrases {dec["e phrases dealt"][-1]:.3f}  cell-dealt extra {dec["d sizes dealt in cell (extra over b)"][-1]:+.3f}')

# 20 random splits
spl = []
for s_ in range(1, 21):
    t_ = split(S, s_); Rs = fit_all(S, t_, ~t_, which=('a', 'b', 'c', 'd', 'e'))
    spl.append(Rs); log('S1', f'  split {s_}: ' + ' '.join(f'{k} {v:.3f}' for k, v in Rs.items()))
SP = pd.DataFrame(spl)

rows = []
for k, v in R.items(): rows.append(dict(set='test half (seed 0)', model=k, r2=v))
for k, v in Ro.items(): rows.append(dict(set='outside set (no second-catalogue partner)', model=k, r2=v))
for k in SP: rows.append(dict(set='20 splits mean', model=k, r2=SP[k].mean(), lo=SP[k].min(), hi=SP[k].max()))
for k, v in dec.items():
    v = np.array(v); rows.append(dict(set='decoys (20)', model=k, r2=v.mean(), lo=v.min(), hi=v.max()))
pd.DataFrame(rows).to_csv(f'{OUT}/models.csv', index=False)
log('S1', 'P6: d beats b in', int((SP.d > SP.b).sum()), 'of 20 splits; mean extra', round((SP.d - SP.b).mean(), 3))
for k, v in dec.items(): log('S1', f'decoy {k}: mean {np.mean(v):.3f} max {np.max(v):.3f}')
log('S1', 'done -> work_data/size/models.csv')
