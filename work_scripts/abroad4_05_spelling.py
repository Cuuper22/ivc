#!/usr/bin/env python3
"""STEP 5 of abroad4: does the foreign text look like signs spelling names by sound?
THREE MEASURES FIXED IN ADVANCE (spelling direction in brackets):
  M1 flatness = Shannon entropy in bits of the pooled sign counts of the set (flatter = higher) [spelling: higher than home].
  M2 class regularity = bits per step saved by frame v2 against sign frequencies alone (unigram minus frame v2), pooled
     [spelling: smaller than home: fewer class-to-class rules].
  M3 repeats = share of texts (3+ real signs) holding a sign more than once [spelling: higher than home].
Controls: home distinct texts matched on kind, animal group and length, 2,000 draws (M1 and M3: matched on number of real
signs; M2: matched on number of steps, same as step 2).
PREDICTIONS (before running): round seals abroad meet 2 of 3 (M1 higher, M2 smaller) and M3 higher; square seals abroad
meet none (they are home texts). All 41 together: M2 smaller (the clear one), M1 and M3 near the home values.
Output: work_data/abroad4/spelling.csv
"""
from abroad4_common import *
pool = score_home_pool(); by = pool_index(pool)
core = list(F[F.tier == 'core'].itertuples()); unk = list(F[F.tier == 'unk_round'].itertuples())
def rs(tok): return [s for s in tok if real(s)]
tokcnt = np.array([np.bincount([GIDX[s] for s in rs(t.tok)], minlength=len(GV)) if True else 0 for t in pool])
byn = collections.defaultdict(list)
for j, t in enumerate(pool):
    if t.intact: byn[(t.kind, t.ag, len(t.tok))].append(j)
def cand_n(kind, ag, n):
    c = byn.get((kind, ag, n), [])
    if len(c) >= 5: return c
    c = [j for m in (n - 1, n, n + 1) for j in byn.get((kind, ag, m), [])]
    if len(c) >= 5: return c
    c = [j for (k2, a2, m), L in byn.items() if k2 == kind and abs(m - n) <= 1 for j in L]
    if len(c) >= 5: return c
    return [j for (k2, a2, m), L in byn.items() if abs(m - n) <= 1 for j in L]
def ent(c):
    c = c[c > 0]; p = c / c.sum(); return float(-(p * np.log2(p)).sum())
rep = np.array([len(rs(t.tok)) != len(set(rs(t.tok))) for t in pool])
rows = []
def run(label, rr, seed):
    rng = np.random.default_rng(seed)
    toks = [r.tok for r in rr]
    # M1 over all tokens
    fc = collections.Counter(s for x in toks for s in rs(x)); fv = np.zeros(len(GV) + 400)   # foreign-only signs get own cells
    allsigns = sorted(set(fc) | set(GV)); ai = {s: i for i, s in enumerate(allsigns)}
    arr = np.zeros(len(allsigns)); 
    for s, n in fc.items(): arr[ai[s]] = n
    e_real = ent(arr)
    cs = [np.array(cand_n(r.kind, r.ag, max(1, len(rs(r.tok))))) for r in rr]
    idx = np.stack([rng.choice(c, size=2000) for c in cs], 1)
    dm1 = np.array([ent(tokcnt[idx[k]].sum(0).astype(float)) for k in range(0, 2000)])
    # M3
    sub = [i for i, r in enumerate(rr) if len(rs(r.tok)) >= 3]
    m3_real = np.mean([len(rs(rr[i].tok)) != len(set(rs(rr[i].tok))) for i in sub]) if sub else np.nan
    dm3 = rep[idx[:, sub]].mean(1) if sub else np.array([np.nan])
    # M2 from steps
    sc = [score_foreign(r) for r in rr]; sc = [s for s in sc if s.n_step >= 1]
    idx2, lv = matched_draws(pool, by, sc, 2000, seed + 1)
    g_real = pooled_bits(sc, 0) - pooled_bits(sc, 2)
    gd = draws_bits(pool, idx2, 0) - draws_bits(pool, idx2, 2)
    gp_real = pooled_bits(sc, 0) - pooled_bits(sc, 1); gpd = draws_bits(pool, idx2, 0) - draws_bits(pool, idx2, 1)
    r1 = summarize(e_real, dm1); r2 = summarize(g_real, gd); r3 = summarize(m3_real, dm3) if sub else {}
    r2p = summarize(gp_real, gpd)
    rows.append(dict(group=label, texts=len(rr), tokens=int(arr.sum()), M1_entropy=e_real, M1_home=r1['ctrl_mean'], M1_P_higher=r1['P_real_higher'],
                     M2_gain_v2=g_real, M2_home=r2['ctrl_mean'], M2_P_lower=r2['P_real_lower'], M2b_gain_signpair=gp_real, M2b_home=r2p['ctrl_mean'], M2b_P_lower=r2p['P_real_lower'],
                     M3_repeat_share=m3_real, M3_home=r3.get('ctrl_mean', np.nan), M3_P_higher=r3.get('P_real_higher', np.nan), M3_texts=len(sub)))
    q = rows[-1]
    log(f'{label:40s} n={q["texts"]:2d} | M1 entropy {q["M1_entropy"]:.2f} vs home {q["M1_home"]:.2f} (P higher {q["M1_P_higher"]:.3f}) | M2 v2 gain {q["M2_gain_v2"]:.2f} vs {q["M2_home"]:.2f} (P lower {q["M2_P_lower"]:.3f}); sign-pair gain {q["M2b_gain_signpair"]:.2f} vs {q["M2b_home"]:.2f} (P lower {q["M2b_P_lower"]:.3f}) | M3 repeat share {q["M3_repeat_share"]:.2f} vs {q["M3_home"]:.2f} (P higher {q["M3_P_higher"]:.3f}, n={q["M3_texts"]})')
run('all 41 core', core, 1)
run('core round seals', [r for r in core if r.kind == 'seal' and r.round], 2)
run('core square seals', [r for r in core if r.kind == 'seal' and not r.round], 3)
run('all round seals (core + unknown site)', [r for r in core + unk if r.kind == 'seal' and r.round], 4)
pd.DataFrame(rows).to_csv(f'{OUT4}/spelling.csv', index=False)
