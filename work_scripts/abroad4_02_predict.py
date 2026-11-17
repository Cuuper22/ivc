#!/usr/bin/env python3
"""STEP 2 of abroad4: are texts found abroad harder to predict than matched home texts?
PREDICTIONS (written before any foreign score was computed):
 P2a  Foreign texts (all 41 core, steps scored) cost MORE bits per step than matched home texts under the sign-pair model,
      by at least 0.5 bits, and the real value lies above the 97.5th percentile of the 2,000 matched draws.
 P2b  Round seals abroad are the harder ones (difference 1.0 bit or more); square seals abroad are close to home (difference
      under 0.5, interval of the draws covers them).
 P2c  Frame v2 (job classes) shows the same direction; the gap under frame v2 is LARGER than under the sign-pair model
      for round seals (they break the job order, not only sign-pair habits).
 P2d  Home round seals (15 faces) score like home texts (difference under 0.5), not like foreign round seals.
Models trained on home texts only, cross-fitted 10 folds (see abroad4_common.py). Unit: bits per step between neighbouring
usable signs; lost / unclear / never-seen-at-home signs cut the text and are not scored.
Output: work_data/abroad4/predict_summary.csv, predict_per_text.csv, predict_draws.npz
"""
from abroad4_common import *
pool = score_home_pool(); by = pool_index(pool)
log(f'home pool {len(pool)} distinct texts, {sum(t.n_step>=1 for t in pool)} with >=1 step')

def fscored(tiers):
    out = []
    for r in F[F.tier.isin(tiers)].itertuples():
        out.append((r, score_foreign(r)))
    return out
core = fscored(['core']); unk = fscored(['unk_round'])
# second-catalogue lines
mo = []
for r in M[(M.site == 'WA') & (~M.partnered)].itertuples():
    class R: pass
    q = R(); q.tok = tuple(r.tok); q.kind = 'seal'; q.clean = False; q.ag = 'ANY'; q.id = f'M{r.textnum}'; q.site = 'West Asia'
    mo.append((q, score_foreign(q)))
def isround(r): return bool(getattr(r, 'round', False)) if not isinstance(r, tuple) else False
def sel(lst, f): return [s for r, s in lst if f(r) and s.n_step >= 1]
subsets = collections.OrderedDict([
  ('all 41 core', sel(core, lambda r: True)),
  ('core round seals (18)', sel(core, lambda r: r.kind == 'seal' and r.round)),
  ('core square seals (15)', sel(core, lambda r: r.kind == 'seal' and not r.round)),
  ('core non-seals (8)', sel(core, lambda r: r.kind != 'seal')),
  ('core Gulf', sel(core, lambda r: r.rgroup == 'Gulf')),
  ('core Mesopotamia', sel(core, lambda r: r.rgroup == 'Mesopotamia')),
  ('core Iran', sel(core, lambda r: r.rgroup == 'Iran')),
  ('core Central Asia', sel(core, lambda r: r.rgroup == 'Central Asia')),
  ('core + unknown-site round seals', sel(core, lambda r: True) + sel(unk, lambda r: True)),
  ('all round seals (core + unknown site)', sel(core, lambda r: r.kind == 'seal' and r.round) + sel(unk, lambda r: True)),
  ('core + unknown round + second-catalogue-only', sel(core, lambda r: True) + sel(unk, lambda r: True) + sel(mo, lambda r: True)),
])
# home round seals: subjects from the pool, controls from non-round pool texts
home_round = [t for t in pool if t.meta.get('round') and t.n_step >= 1 and t.kind == 'seal']
subsets_home = {'home round seals (distinct texts)': home_round}
rows = []; store = {}
def run(name, subj, nodraw_round=False, seed=11):
    rule = (lambda t: not t.meta.get('round')) if nodraw_round else None
    idx, lv = matched_draws(pool, by, subj, 2000, seed, shape_rule=rule)
    row = dict(subset=name, texts=len(subj), steps=sum(t.n_step for t in subj), widened=int(sum(1 for l in lv if l > 0)))
    for c, nm in enumerate(NMODEL):
        s = summarize(pooled_bits(subj, c), draws_bits(pool, idx, c))
        for k, v in s.items(): row[f'{nm}|{k}'] = v
    rows.append(row); store[name] = idx
    log(f'{name:48s} n={row["texts"]:3d} steps={row["steps"]:3d} | sign pair {row["sign pair|real"]:.2f} vs {row["sign pair|ctrl_mean"]:.2f} (P hi {row["sign pair|P_real_higher"]:.4f}) | frame v2 {row["frame v2|real"]:.2f} vs {row["frame v2|ctrl_mean"]:.2f} (P {row["frame v2|P_real_higher"]:.4f}) | unigram {row["unigram|real"]:.2f} vs {row["unigram|ctrl_mean"]:.2f}')
for nm, sb in subsets.items(): run(nm, sb)
for nm, sb in subsets_home.items(): run(nm, sb, nodraw_round=True)
pd.DataFrame(rows).to_csv(f'{OUT4}/predict_summary.csv', index=False)
pt = []
for lst, tag in ((core, 'core'), (unk, 'unk_round'), (mo, 'M_only')):
    for r, s in lst:
        pt.append(dict(tier=tag, id=r.id, site=r.site, kind=r.kind, shape=('round' if getattr(r, 'round', False) else 'square') if r.kind == 'seal' else r.kind, n_step=s.n_step,
                       bits_unigram=s.tr[:, 0].mean() if s.n_step else np.nan, bits_sign_pair=s.tr[:, 1].mean() if s.n_step else np.nan,
                       bits_frame_v2=s.tr[:, 2].mean() if s.n_step else np.nan, bits_mix=s.tr[:, 3].mean() if s.n_step else np.nan, text='-'.join(s.tok)))
pd.DataFrame(pt).to_csv(f'{OUT4}/predict_per_text.csv', index=False)
# how the home pool itself looks (for scale)
allp = [t for t in pool if t.n_step >= 1]
log('home pool pooled bits: ' + ' | '.join(f'{nm} {pooled_bits(allp, c):.2f}' for c, nm in enumerate(NMODEL)))
home_matchfree = {}
