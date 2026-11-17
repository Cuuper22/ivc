#!/usr/bin/env python3
"""SIZE step 5: size against the other marks of a stone.  Written 2026-11-17 before any number.

Residual = logA minus model (d) fit on all complete seals (length + site + format + one ridge weight per sign), so the
text is taken out. Marks: stand letter (unicorn seals: W J S I L), animal, pierced / not, boss / no boss, material,
time bin. For each mark: group means of the residual, and the between-group spread against 2,000 deals of the mark
within site x format.
Twin sets (work_data/twins/members.csv, identical text on 2+ stones): size minus the set's mean size (text held fixed
exactly); the same group means and deals within the sets.

PREDICTIONS:
  M1  Stand W is bigger than J, S, I, L with the text taken out (W = the big late format), and W is late.
  M2  Animal matters with text taken out: unicorn and zebu bigger than inscription-only ('none') square seals.
  M3  Inside twin sets, W stones are bigger than their twins with another stand, and beast stones bigger than
      inscription-only twins.
"""
from size_common import *

S = table(); y = S.logA.values; toks = list(S.tok)
Bf, _ = base_X(S); B = Bf.values
cnt = collections.Counter(s for t in toks for s in set(t)); signs = sorted(s for s, n in cnt.items() if n >= 2)
Z = sign_X(toks, signs); lam = ridge_cv(B, Z, y, S.signs.values, 0)
wb, wz = ridge_fit(B, Z, y, lam); S['res'] = y - ridge_pred(B, Z, wb, wz)
S['animal2'] = S.animal.replace('', 'not recorded')
S['material2'] = S.material.where(S.material.isin(['Steatite', 'Faience', 'Clay', 'Terracotta']), 'other/unknown')
rr = np.random.default_rng(21)
def between(r, lab):
    df = pd.DataFrame(dict(r=r, c=lab)); g = df.groupby('c').r.agg(['mean', 'size'])
    return (g['size'] * (g['mean'] - df.r.mean()) ** 2).sum()
def test(D, col, within, label, minn=5):
    D = D[D[col] != ''].reset_index(drop=True)
    keep = D[col].value_counts(); D = D[D[col].isin(keep[keep >= minn].index)].reset_index(drop=True)
    real = between(D.res.values, D[col].values); null = []
    groups = list(D.groupby(within).indices.values())
    for _ in range(2000):
        lab = D[col].values.copy()
        for ix in groups: lab[ix] = lab[rr.permutation(ix)]
        null.append(between(D.res.values, lab))
    g = D.groupby(col).res.agg(['mean', 'size', 'median']).sort_values('mean', ascending=False)
    p = np.mean(np.array(null) >= real)
    log('S5', f'{label}: {col} spread {real:.2f} vs dealt {np.mean(null):.2f}, P {p:.4f}\n' + g.round(3).to_string())
    g = g.reset_index().rename(columns={col: 'value'}); g['mark'] = col; g['set'] = label; g['P_spread'] = p
    return g
out = []
for col in ('stand5', 'animal2', 'pierced', 'knob', 'material2', 'bin'):
    out.append(test(S, col, ['siteg', 'fmt'], 'all seals, text taken out'))
# square seals only for animal (beast vs none on the same format)
out.append(test(S[S.fmt == 'square'], 'animal2', ['siteg'], 'square seals only, text taken out'))
# W by bin
U = S[S.stand5 != '']
log('S5', 'stand by bin (unicorn seals with a stand letter):\n' + pd.crosstab(U.stand5, U.bin).to_string())

# twin sets
Mb = pd.read_csv(f'{ROOT}/work_data/twins/members.csv', dtype=str).fillna('')
Mb['area_mm2'] = pd.to_numeric(Mb.area_mm2, errors='coerce'); Mb = Mb[Mb.area_mm2 > 0].copy()
Mb['logA'] = np.log(Mb.area_mm2)
Mb['res'] = Mb.logA - Mb.groupby('set').logA.transform('mean')
Mb = Mb[Mb.groupby('set').logA.transform('size') >= 2]
Mb['animal2'] = Mb.animal.replace('', 'not recorded')
log('S5', f'twin stones with a size: {len(Mb)} in {Mb.set.nunique()} sets')
for col in ('stand5', 'animal2', 'fmt', 'bin', 'pierced'):
    out.append(test(Mb, col, ['set'], 'twin sets (text fixed exactly)', minn=4))
# direct pair checks in twin sets: beast vs inscription-only, W vs other stand
pairs = []
for st_, g in Mb.groupby('set'):
    g = g.reset_index(drop=True)
    for i in range(len(g)):
        for j in range(i + 1, len(g)):
            a, b = g.loc[i], g.loc[j]
            pairs.append(dict(set=st_, a_an=a.animal2, b_an=b.animal2, a_st=a.stand5, b_st=b.stand5, a_fmt=a.fmt, b_fmt=b.fmt, d=a.logA - b.logA))
P = pd.DataFrame(pairs)
def pair_side(cond_a, cond_b, label):
    m1 = P[cond_a(P, 'a') & cond_b(P, 'b')]; m2 = P[cond_a(P, 'b') & cond_b(P, 'a')]
    d = np.r_[m1.d.values, -m2.d.values]
    if len(d): log('S5', f'twin pairs {label}: {len(d)} pairs, first bigger in {(d>0).sum()}, mean gap {d.mean():+.3f} (x{np.exp(d.mean()):.2f})')
    return dict(test=label, pairs=len(d), first_bigger=int((d > 0).sum()), mean_gap=d.mean() if len(d) else np.nan)
pt = [pair_side(lambda P, s: ~P[f'{s}_an'].isin(['none', 'not recorded']), lambda P, s: P[f'{s}_an'] == 'none', 'beast stone vs inscription-only stone'),
      pair_side(lambda P, s: P[f'{s}_st'] == 'W', lambda P, s: P[f'{s}_st'].isin(['J', 'S', 'I', 'L']), 'stand W vs other stand'),
      pair_side(lambda P, s: P[f'{s}_fmt'] == 'square', lambda P, s: P[f'{s}_fmt'] == 'rectangular', 'square vs rectangular bar')]
pd.DataFrame(pt).to_csv(f'{OUT}/marks_twin_pairs.csv', index=False)
pd.concat(out).to_csv(f'{OUT}/marks.csv', index=False)
