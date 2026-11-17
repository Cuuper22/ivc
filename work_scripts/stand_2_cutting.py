#!/usr/bin/env python3
"""Step 2a: what the stand letter goes with on the stone itself (cutting features), and the photo check stats.

PREDICTIONS, written before any number:
 P-photo: if the letter is a STAND pattern, my blind photo kinds (cage+plain bowl, cage+patterned bowl, dome,
   small box+cup ...) line up with the letter (one kind dominates each letter, >= 8 of 12). If the letter is a
   CARVING STYLE, the bull's drawing (neck folds, saddle outline) lines up with the letter better than the stand does.
 P-cut (workshop): within one site the letter goes with the catalogue's stand-drawing code (cult: top S/R/H,
   middle A/B/C, end N/F), boss subtype (PB / PBSG / ...), material, thickness, size: each at shuffle P < 0.01.
 P-cut (household): only size (a rank / wealth effect) goes with the letter; boss, material, thickness at chance.
Shuffle = letters dealt at random among unicorn seals of the same site, 2,000 times. V = Cramer's V (0 none, 1 total).
"""
from stand_common import *
from scipy.stats import chi2_contingency, fisher_exact
rng = np.random.default_rng(1)
# ---- photo check stats
m = pd.read_csv(f'{OUT}/stand_photo_unblind.csv', dtype=str)
r = m[m.kind != 'unreadable']
def purity(col, sub):
    ct = pd.crosstab(sub[col], sub.stand5); return ct.max(0).sum() / ct.values.sum(), ct
pk, ctk = purity('kind', r)
log('photo', f'readable stands {len(r)} of 60; best-kind share inside each letter {pk:.2f}')
log('photo', 'unreadable per letter', m[m.kind == 'unreadable'].stand5.value_counts().to_dict())
f = m[m.folds.isin(['0', '1'])]
a = ((f.stand5.isin(['I', 'W'])) & (f.folds == '1')).sum(); b = ((f.stand5.isin(['I', 'W'])) & (f.folds == '0')).sum()
c = ((f.stand5.isin(['J', 'S'])) & (f.folds == '1')).sum(); d_ = ((f.stand5.isin(['J', 'S'])) & (f.folds == '0')).sum()
log('photo', f'neck folds: I+W {a} of {a+b}, J+S {c} of {c+d_}; Fisher P {fisher_exact([[a,b],[c,d_]])[1]:.2g}')
log('photo', 'folds by letter', pd.crosstab(f.stand5, f.folds).to_dict('index'))
h = m[m.saddle == 'heart']; log('photo', 'heart-shaped shoulder mark on letters', h.stand5.value_counts().to_dict(), 'of', len(h))
# shuffle test of purity: letter labels dealt among readable photos
def kind_purity(lab, kind):
    ct = pd.crosstab(kind, lab); return ct.max(0).sum()
real = kind_purity(r.stand5.values, r.kind.values)
sims = [kind_purity(rng.permutation(r.stand5.values), r.kind.values) for _ in range(2000)]
log('photo', f'stand kind purity real {real} against dealt {np.mean(sims):.1f} (P {np.mean(np.array(sims)>=real):.3f})')
f2 = m[m.folds.isin(['0','1']) & m.saddle.isin(['0','1','heart'])].copy()
f2['style'] = f2.folds + '/' + f2.saddle.replace({'heart': '1'})
real = kind_purity(f2.stand5.values, f2['style'].values)
sims = [kind_purity(rng.permutation(f2.stand5.values), f2['style'].values) for _ in range(2000)]
log('photo', f'bull style purity real {real} of {len(f2)} against dealt {np.mean(sims):.1f} (P {np.mean(np.array(sims)>=real):.3f})')

# ---- catalogue cutting features
S = stand_seals()
u = S[(S.stand5 != '')].drop_duplicates('obj').copy()
u['cut_top'] = u.cultc.str[:1].where(u.cultc.str[:1].isin(['S', 'R', 'H']), '')
u['cut_mid'] = u.cultc.str[1:2].where(u.cultc.str[1:2].isin(['A', 'B', 'C']), '')
u['cut_end'] = u.cultc.str[2:3].where(u.cultc.str[2:3].isin(['N', 'F']), '')
u['boss2'] = u.bossk.where(u.bossk.isin(['PB', 'PBSG']), np.where(u.bossk != '', 'other', ''))
u['matk'] = u.mat.where(u.mat.isin(['steatite']), np.where(u.mat != '', 'other', ''))
u['thick3'] = ''
u['size3'] = ''
for st, g in u.groupby('site'):
    if g.thick.notna().sum() >= 6: u.loc[g.index, 'thick3'] = pd.qcut(g.thick, 3, labels=['thin', 'mid', 'thick'], duplicates='drop').astype(str).replace('nan', '')
    if g.logsz.notna().sum() >= 6: u.loc[g.index, 'size3'] = pd.qcut(g.logsz, 3, labels=['small', 'mid', 'big'], duplicates='drop').astype(str).replace('nan', '')
rows = []
for col in ['cut_top', 'cut_mid', 'cut_end', 'boss2', 'matk', 'thick3', 'size3', 'condition', 'bin']:
    g = u[(u[col] != '') & u[col].notna()].reset_index(drop=True)
    g = g[g.site.map(g.site.value_counts()) >= 5].reset_index(drop=True)
    def V(lab):
        ct = pd.crosstab(g[col], lab); ct = ct.loc[ct.sum(1) > 0, ct.sum(0) > 0]
        chi = chi2_contingency(ct, correction=False)[0]; return np.sqrt(chi / (ct.values.sum() * (min(ct.shape) - 1)))
    rv = V(g.stand5.values); st = strata_idx(g.site.values)
    sims = np.array([V(perm_within(g.stand5.values, st, rng)) for _ in range(1000)])
    rows.append(dict(feature=col, seals=len(g), V=round(rv, 3), dealt=round(sims.mean(), 3), P=(sims >= rv).mean()))
    log('cut', rows[-1])
    print(pd.crosstab(g[col], g.stand5).to_string())
pd.DataFrame(rows).to_csv(f'{OUT}/cutting_assoc.csv', index=False)

# Thickness with face size taken out: is the stone's PROPORTION (how thick for its face) a letter trait?
# Prediction (workshop): yes, P < 0.01 (a shop cuts its blanks to its own proportion).
g = u[u.thick.notna() & u.logsz.notna()].reset_index(drop=True)
g['lthk'] = np.log(g.thick)
res = np.empty(len(g))
for st_, ix in g.groupby('site').groups.items():
    ix = np.array(list(ix)); X = np.c_[np.ones(len(ix)), g.logsz.values[ix]]
    beta = np.linalg.lstsq(X, g.lthk.values[ix], rcond=None)[0]; res[ix] = g.lthk.values[ix] - X @ beta
g['tres'] = res
def spread(lab): return pd.Series(g.tres.values).groupby(lab).mean().var()
rs = spread(g.stand5.values); stt = strata_idx(g.site.values)
ss = np.array([spread(perm_within(g.stand5.values, stt, rng)) for _ in range(2000)])
log('proportion', f'{len(g)} seals; thickness for its face, mean by letter (log units): ' + str(pd.Series(g.tres.values).groupby(g.stand5.values).agg(["mean", "count"]).round(3).to_dict("index")))
log('proportion', f'spread {rs:.5f} against dealt {ss.mean():.5f}, P {np.mean(ss >= rs):.4f}')
