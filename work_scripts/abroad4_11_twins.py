#!/usr/bin/env python3
"""STEP 11 of abroad4 (after jobs/out/twins.md): does a foreign text have an identical twin on a home object?
PREDICTION (written before running): intact square seals abroad have an exact home twin (the same complete text on a home object)
about as often as matched home texts have a twin on ANOTHER home object; intact round seals abroad have none (0 of 9); the 590-390-740
seals (Kish 1971.1, Gonur 4155.1 have longer texts, so no exact twin) are the near-twin cases.
Twin = identical sign string, a different object. Near twin = same length, 3+ signs, one position differs.
Output: work_data/abroad4/twins.csv
"""
from abroad4_common import *
pool = score_home_pool()
hf = F[F.tier == 'home']
objs_of = collections.defaultdict(set)
for x, o in zip(hf.tok, hf.obj): objs_of[x].add(o)
def near(x, y): return len(x) == len(y) and len(x) >= 3 and sum(a != b for a, b in zip(x, y)) == 1
homeset = list(objs_of)
rng = np.random.default_rng(1111)
core = [r for r in F[F.tier == 'core'].itertuples() if r.clean and edge_ok(r.tok) and len(r.tok) >= 2]
unk = [r for r in F[F.tier == 'unk_round'].itertuples() if r.clean and edge_ok(r.tok) and len(r.tok) >= 2]
byn = collections.defaultdict(list)
for t in pool:
    if t.intact and len(t.tok) >= 2: byn[(t.kind, t.ag, len(t.tok))].append(t.tok)
def cand_n(kind, ag, n):
    c = byn.get((kind, ag, n), [])
    if len(c) >= 5: return c
    c = [x for m in (n - 1, n, n + 1) for x in byn.get((kind, ag, m), [])]
    return c if len(c) >= 5 else [x for (k2, a2, m), L in byn.items() if abs(m - n) <= 1 for x in L]
def twin_home(x, own=None): return len(objs_of.get(x, set()) - ({own} if own else set())) >= 1
rows = []
for label, sub in (('intact core texts (2+ signs)', core), ('intact round seals (core + unknown)', [r for r in core + unk if r.kind == 'seal' and r.round]), ('intact square seals', [r for r in core if r.kind == 'seal' and not r.round])):
    ex = sum(twin_home(r.tok) for r in sub); nr = sum(any(near(r.tok, y) for y in homeset) for r in sub)
    cs = [cand_n(r.kind, r.ag, len(r.tok)) for r in sub]
    # control: matched home text; twin = identical text on at least 2 home objects (another object besides itself)
    dex = []; dnr = []
    for _ in range(1000):
        pick = [c[rng.integers(len(c))] for c in cs]
        dex.append(sum(len(objs_of[x]) >= 2 for x in pick))
        dnr.append(sum(any(near(x, y) for y in homeset if y != x) for x in pick[:40]) * len(pick) / min(40, len(pick)))
    dex = np.array(dex); dnr = np.array(dnr)
    rows.append(dict(group=label, texts=len(sub), exact_twin_at_home=ex, matched_home_mean=dex.mean(), P_fewer=(np.sum(dex <= ex) + 1) / 1001, near_twin_at_home=nr, matched_near_mean=dnr.mean()))
    log(f'{label:38s} n={len(sub):2d}: exact home twin {ex} (matched home texts have another-object twin {dex.mean():.1f}, P fewer {rows[-1]["P_fewer"]:.3f}); near twin {nr} (matched ~{dnr.mean():.1f}, sampled)')
    for r in sub:
        if twin_home(r.tok): print('   twin:', r.id, r.site, '-'.join(r.tok), 'home objects', sorted(objs_of[r.tok])[:5])
pd.DataFrame(rows).to_csv(f'{OUT4}/twins.csv', index=False)
