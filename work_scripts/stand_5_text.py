#!/usr/bin/env python3
"""Step 3: does the letter go with the text?
Features of a seal's text: frame-v2 KIND (name seal = bare name, name + closer, name + title, name + closer + title,
front formula, count line); the AFTER-JAR TITLE (sign right after jar 740); the FRONT WORD (first sign when it is a
front word); each of the 136 FIXED PHRASES (work_data/phrases/atlas.csv) present in the text; each SIGN present.
Chance: letters dealt among unicorn letter seals of the same site and size third, 4,000 times. For each (feature,
letter) cell: carriers with that letter, dealt mean, two-sided P; q = Benjamini-Hochberg over all cells.
PREDICTIONS, fixed first:
 WORKSHOP (my call): no text feature goes with the letter beyond what size and site carry: kind P > 0.05, no cell
   at q < 0.1 (the same null result as the species scan), because the cutter's style does not read the text.
 HOUSEHOLD/OFFICE: titles or front words (offices) go with a letter (q < 0.1).
"""
from stand_common import *
rng = np.random.default_rng(5)
S = stand_seals()
u = S[(S.stand5 != '') & (S.signs != '')].drop_duplicates('obj').reset_index(drop=True)
u['size3'] = ''
for st, g in u.groupby('site'):
    if g.logsz.notna().sum() >= 6: u.loc[g.index, 'size3'] = pd.qcut(g.logsz, 3, labels=['s', 'm', 'b'], duplicates='drop').astype(str)
strata = strata_idx((u.site + '|' + u.size3.astype(str)).values)
toks = u.signs.str.split('-')
ph = pd.read_csv(f'{ROOT}/work_data/phrases/atlas.csv', dtype=str).phrase.tolist()
OPEN = {'820', '861', '817', '920', '692', '880', '824', '545', '091', '550', '360', '556'}
F = {}
for k in u.kind.unique():
    if k: F[f'kind={k}'] = (u.kind == k).values
title = [t[t.index('740') + 1] if '740' in t and t.index('740') + 1 < len(t) else '' for t in toks]
for t in set(title) - {''}: F[f'after-jar={t}'] = np.array([x == t for x in title])
front = [t[0] if t[0] in OPEN else '' for t in toks]
for t in set(front) - {''}: F[f'front={t}'] = np.array([x == t for x in front])
for p in ph: F[f'phrase={p}'] = np.array([('-' + s + '-').find('-' + p + '-') >= 0 for s in u.signs])
from collections import Counter
c = Counter(x for t in toks for x in set(t))
for x, n in c.items():
    if n >= 8 and x != '000': F[f'sign={x}'] = np.array([x in t for t in toks])
F = {k: v for k, v in F.items() if v.sum() >= 5}
names = list(F); M = np.array([F[k] for k in names], dtype=float)   # features x seals
lab = np.asarray(u.stand5.values, dtype=object); L = np.array(L5, dtype=object)
def tab(l): return M @ (l[:, None] == L[None, :]).astype(float)       # features x letters
real = tab(lab); sims = np.zeros((4000,) + real.shape)
for i in range(4000):
    sims[i] = tab(perm_within(lab, strata, rng))
    if i % 1000 == 0: log('deal', i)
mu = sims.mean(0); dev = np.abs(sims - mu); P = (dev >= np.abs(real - mu) - 1e-9).mean(0)
rows = []
for fi, k in enumerate(names):
    for li, l in enumerate(L5):
        rows.append(dict(feature=k, carriers=int(M[fi].sum()), letter=l, real=int(real[fi, li]), dealt=round(mu[fi, li], 2), ratio=round(real[fi, li] / mu[fi, li], 2) if mu[fi, li] else np.nan, P=P[fi, li]))
R = pd.DataFrame(rows)
def bh(p):
    p = np.asarray(p); n = len(p); o = np.argsort(p); q = np.empty(n)
    q[o] = np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]; return np.minimum(q, 1)
R['q'] = bh(R.P.clip(1 / 4000))
R.sort_values('P').to_csv(f'{OUT}/text_scan.csv', index=False)
log('scan', f'{len(names)} features, {len(R)} cells; cells P<0.001: {(R.P<0.001).sum()} (expected {len(R)*0.001:.1f}); P<0.01: {(R.P<0.01).sum()} (expected {len(R)*0.01:.1f}); q<0.1: {(R.q<0.1).sum()}')
print(R.sort_values('P').head(20).to_string(index=False))
print(R[R.feature.str.startswith('kind=')].to_string(index=False))
# omnibus for kind: chi-square-like distance real vs dealt
def chi(T, E): return (((T - E) ** 2) / np.maximum(E, 1e-9)).sum()
kk = [i for i, k in enumerate(names) if k.startswith('kind=')]
rc = chi(real[kk], mu[kk]); sc = np.array([chi(s[kk], mu[kk]) for s in sims])
log('kind omnibus', f'distance {rc:.1f} against dealt {sc.mean():.1f}, P {np.mean(sc >= rc):.3f}')
tt = [i for i, k in enumerate(names) if k.startswith('after-jar=') or k.startswith('front=')]
rc = chi(real[tt], mu[tt]); sc = np.array([chi(s[tt], mu[tt]) for s in sims])
log('title+front omnibus', f'distance {rc:.1f} against dealt {sc.mean():.1f}, P {np.mean(sc >= rc):.3f}')
pp = [i for i, k in enumerate(names) if k.startswith('phrase=')]
rc = chi(real[pp], mu[pp]); sc = np.array([chi(s[pp], mu[pp]) for s in sims])
log('phrase omnibus', f'{len(pp)} phrases: distance {rc:.1f} against dealt {sc.mean():.1f}, P {np.mean(sc >= rc):.3f}')
