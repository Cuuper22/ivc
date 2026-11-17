#!/usr/bin/env python3
"""STEP 7 of abroad4: home seals of the foreign kind (round seals at home; home seals with the short-horned bull).
PREDICTIONS (written before running):
 P7a  Home round seals (15 faces) are harder to predict than matched home seals but less so than foreign round seals
      (between the two; difference from home 0.5 bit or more).
 P7b  Home short-horned-bull seals (about 100) score like home texts (difference under 0.4 bit), NOT like foreign ones:
      the animal alone does not make the text foreign; the round shape does.
 P7c  Home round seals sit at a few places (Mohenjo-daro, Dholavira, Harappa, trade-facing houses), not spread like all seals:
      Mohenjo-daro share of home round seals no larger than of all home seals; two or more in the same building: none.
Controls: home square seals of the same length (and for round seals the animal group); short-horned-bull seals are compared with
home seals of the same length whose animal is NOT the short-horned bull and which are not round. 2,000 draws.
Output: work_data/abroad4/homekind_*.csv
"""
from abroad4_common import *
pool = score_home_pool(); by = pool_index(pool)
home_seals = F[(F.tier == 'home') & (F.kind == 'seal')]
rnd = home_seals[home_seals['round']]
gaur = home_seals[(home_seals.animal == 'SHORTHORN')]
log(f'home seals {len(home_seals)} faces; round {len(rnd)}; short-horned bull {len(gaur)} ({int((gaur["round"]).sum())} of them round)')
# subjects from the pool (distinct texts)
def subj_from(rows):
    keys = set(rows.tok); return [t for t in pool if t.tok in keys and t.kind == 'seal' and t.n_step >= 1]
by_any = collections.defaultdict(list)
for j, t in enumerate(pool):
    if t.kind == 'seal' and t.n_step >= 1 and not t.meta.get('round') and t.ag != 'short-horned bull': by_any[('seal', 'X', t.n_step)].append(j)
rows = []
def run(label, subj, rule_by, seed):
    sub2 = [Scored(t.tok, t.kind, 'X' if rule_by is by_any else t.ag, t.id, t.tr, t.st, t.en, t.intact, t.meta) for t in subj]
    idx, lv = matched_draws(pool, rule_by, sub2, 2000, seed)
    row = dict(group=label, texts=len(subj), steps=sum(t.n_step for t in subj))
    for c, nm in enumerate(NMODEL):
        s = summarize(pooled_bits(subj, c), draws_bits(pool, idx, c))
        for k, v in s.items(): row[f'{nm}|{k}'] = v
    rows.append(row)
    log(f'{label:52s} n={row["texts"]:3d} steps={row["steps"]:3d} | sign pair {row["sign pair|real"]:.2f} vs {row["sign pair|ctrl_mean"]:.2f} (P hi {row["sign pair|P_real_higher"]:.4f}) | frame v2 {row["frame v2|real"]:.2f} vs {row["frame v2|ctrl_mean"]:.2f} (P {row["frame v2|P_real_higher"]:.4f})')
sub_r = subj_from(rnd); sub_g = subj_from(gaur); sub_gs = [t for t in sub_g if not t.meta.get('round')]
sub_man = [t for t in sub_r if any(s in ('090', '091') for s in t.tok)]
run('home round seals vs home non-round seals (any animal but short-horned bull)', sub_r, by_any, 1)
run('home short-horned-bull seals (all) vs same', sub_g, by_any, 2)
run('home short-horned-bull SQUARE seals vs same', sub_gs, by_any, 3)
run('home round seals carrying 090 or 091 vs same', sub_man, by_any, 4)
non_man = [t for t in sub_r if t not in sub_man]; run('home round seals without 090/091 vs same', non_man, by_any, 5)
# foreign for the scale
fs = [score_foreign(r) for r in F[F.tier == 'core'].itertuples()]
fr = [s for r, s in zip(F[F.tier == 'core'].itertuples(), fs) if s.n_step >= 1 and r.kind == 'seal' and r.round]
run('foreign round seals (core) vs same controls', fr, by_any, 6)
fsq = [s for r, s in zip(F[F.tier == 'core'].itertuples(), fs) if s.n_step >= 1 and r.kind == 'seal' and not r.round]
run('foreign square seals (core) vs same controls', fsq, by_any, 7)
pd.DataFrame(rows).to_csv(f'{OUT4}/homekind_summary.csv', index=False)
# per-text list of home round seals
pt = []
for t in sub_r:
    pt.append(dict(id=t.id, site=t.meta.get('site'), text='-'.join(t.tok), steps=t.n_step, bits_sign_pair=t.tr[:, 1].mean(), bits_frame_v2=t.tr[:, 2].mean()))
pd.DataFrame(pt).to_csv(f'{OUT4}/homekind_round_per_text.csv', index=False); print(pd.DataFrame(pt).round(2).to_string())
# findspots
def spots(rows_, label):
    print(f'--- {label}: by site'); print(rows_.groupby('site').size().sort_values(ascending=False).head(12).to_string())
    allb = home_seals.groupby('site').size()
    sh = rows_.groupby('site').size() / len(rows_); base = allb / allb.sum()
    cmp = pd.DataFrame(dict(n=rows_.groupby('site').size(), share=sh, share_of_all_home_seals=base)).dropna().sort_values('n', ascending=False).head(8)
    print(cmp.round(3).to_string())
    md = rows_[rows_.site == 'Mohenjo-daro']
    print(f'  Mohenjo-daro: {len(md)} faces; areas:', md['area-section'].value_counts().to_dict())
    print('  repeats of (site, area, block-house):', {k: v for k, v in collections.Counter(zip(rows_.site, rows_['area-section'], rows_['block-house'])).items() if v >= 2 and k[2] not in ('', '--')})
spots(rnd, 'home round seals (type C / CY)'); spots(gaur, 'home short-horned-bull seals')
# permutation: how often do 2+ home short-horned-bull seals share a building vs random home seals (same site)
def same_bld_pairs(rows_):
    b = [(s, a, h) for s, a, h in zip(rows_.site, rows_['area-section'], rows_['block-house']) if h not in ('', '--')]
    c = collections.Counter(b); return sum(v * (v - 1) // 2 for v in c.values())
rng = np.random.default_rng(7)
for label, rows_ in (('round', rnd), ('short-horned bull', gaur)):
    real_p = same_bld_pairs(rows_)
    dr = []
    for _ in range(2000):
        pick = []
        for st, g in rows_.groupby('site'):
            pool_s = home_seals[home_seals.site == st]
            pick.append(pool_s.iloc[rng.choice(len(pool_s), size=len(g), replace=False)])
        dr.append(same_bld_pairs(pd.concat(pick)))
    dr = np.array(dr); log(f'home {label} seals in the same building: {real_p} pairs; random seals of the same sites {dr.mean():.2f} (P real >= {(np.sum(dr >= real_p) + 1) / 2001:.3f})')
