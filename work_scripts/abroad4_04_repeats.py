#!/usr/bin/env python3
"""STEP 4 of abroad4: signs repeated inside one text, and home phrases read in reverse abroad.
PREDICTIONS (written before running):
 P4a  A sign repeated inside one text is rare at home in short texts (4 to 6 signs). Abroad the share of texts with a repeat is
      at least twice the matched-home share, and round seals carry most of it.
 P4b  Reversed home phrases: the earlier lead (7 against 5) was noise. Among the 136 home phrases, the number of objects abroad
      holding a phrase in its HOME order is equal to or lower than in order-shuffled foreign texts, and the number holding
      it REVERSED is no higher than in shuffled texts (P above 0.2).
Matching for P4a: same kind, same animal group, same number of real signs (clean home distinct texts), 2,000 draws.
Output: work_data/abroad4/repeats_*.csv
"""
from abroad4_common import *
from phrases_common import find_in
pool = score_home_pool()
def rs(tok): return [s for s in tok if real(s)]
def has_rep(tok):
    r = rs(tok); return len(r) != len(set(r))
def has_adj(tok):
    return any(a == b and real(a) for a, b in zip(tok, tok[1:]))
clean_idx = collections.defaultdict(list)
for j, t in enumerate(pool):
    if t.intact: clean_idx[(t.kind, t.ag, len(t.tok))].append(j)
def cands(kind, ag, n):
    for key in ((lambda: clean_idx.get((kind, ag, n), [])),):
        c = key()
        if len(c) >= 5: return c
    c = [j for m in (n - 1, n, n + 1) for j in clean_idx.get((kind, ag, m), [])]
    if len(c) >= 5: return c
    c = [j for (k2, a2, m), L in clean_idx.items() if k2 == kind and abs(m - n) <= 1 for j in L]
    if len(c) >= 5: return c
    return [j for (k2, a2, m), L in clean_idx.items() if abs(m - n) <= 1 for j in L]
rng = np.random.default_rng(404)
repH = np.array([has_rep(t.tok) for t in pool]); adjH = np.array([has_adj(t.tok) for t in pool])
# home context: repeat share by length (all distinct clean home texts)
ctx = []
for n in range(2, 12):
    js = [j for j, t in enumerate(pool) if t.intact and len(t.tok) == n]
    if js: ctx.append(dict(length=n, texts=len(js), with_repeat=int(repH[js].sum()), share=repH[js].mean(), with_adjacent_double=int(adjH[js].sum())))
pd.DataFrame(ctx).to_csv(f'{OUT4}/repeats_home_by_length.csv', index=False); log('home: share of distinct clean texts with a repeated sign, by length'); print(pd.DataFrame(ctx).round(3).to_string())
def test(label, rows, minlen=3):
    sub = [r for r in rows if len(rs(r.tok)) >= minlen]
    if not sub: return None
    cs = [np.array(cands(r.kind, r.ag, len(rs(r.tok)))) for r in sub]
    out = dict(group=label, texts=len(sub), real_repeat=sum(has_rep(r.tok) for r in sub), real_adjacent=sum(has_adj(r.tok) for r in sub))
    dr = np.array([[repH[rng.choice(c)] for c in cs] for _ in range(2000)]).sum(1)
    da = np.array([[adjH[rng.choice(c)] for c in cs] for _ in range(2000)]).sum(1)
    out.update(ctrl_repeat_mean=dr.mean(), ctrl_repeat_hi=np.percentile(dr, 97.5), P_repeat=(np.sum(dr >= out['real_repeat']) + 1) / 2001,
               ctrl_adj_mean=da.mean(), P_adjacent=(np.sum(da >= out['real_adjacent']) + 1) / 2001)
    return out
core = list(F[F.tier == 'core'].itertuples()); unk = list(F[F.tier == 'unk_round'].itertuples())
class R: pass
mo = []
for r in M[(M.site == 'WA') & (~M.partnered)].itertuples():
    q = R(); q.tok = tuple(r.tok); q.kind = 'seal'; q.ag = 'other beast'; mo.append(q)
rows = []
for label, rr in (('core, texts with 3+ signs', core), ('core round seals', [r for r in core if r.kind == 'seal' and r.round]), ('core square seals', [r for r in core if r.kind == 'seal' and not r.round]),
                  ('core + unknown-site round', core + unk), ('all round seals (core + unknown site)', [r for r in core + unk if r.kind == 'seal' and r.round]),
                  ('second-catalogue-only West Asia lines', mo)):
    o = test(label, rr)
    if o: rows.append(o); log(f'{label:44s} n={o["texts"]:2d} repeats {o["real_repeat"]} vs {o["ctrl_repeat_mean"]:.2f} home (97.5th pct {o["ctrl_repeat_hi"]:.0f}, P {o["P_repeat"]:.4f}) | adjacent doubles {o["real_adjacent"]} vs {o["ctrl_adj_mean"]:.2f} (P {o["P_adjacent"]:.4f})')
pd.DataFrame(rows).to_csv(f'{OUT4}/repeats_foreign.csv', index=False)
# list the repeating foreign texts
print('foreign texts with a repeated sign:')
for r in core + unk:
    if has_rep(r.tok): print('  ', r.id, r.site, 'round' if r.round else r.kind, '-'.join(r.tok))
for r in M[(M.site == 'WA') & (~M.partnered)].itertuples():
    if has_rep(r.tok): print('  M', r.textnum, '-'.join(r.tok))

# ------------------------------------------------------------ B. home phrases forward and reversed
PL = pd.read_csv(f'{ROOT}/work_data/phrases/phrase_list.csv', dtype=str)
PH = [tuple(p.split('-')) for p in PL.phrase]
PHR = [p[::-1] for p in PH]
palin = [p for p in PH if p == p[::-1]]
def count_set(texts):
    fw = sum(any(find_in(t, p) for t in [x]) for x in texts for p in PH) if False else 0
    f = r_ = 0; fp = set(); rp = set()
    for x in texts:
        for p, q in zip(PH, PHR):
            if find_in(x, p): f += 1; fp.add(p)
            if find_in(x, q): r_ += 1; rp.add(p)
    return f, r_, len(fp), len(rp)
def shuffled(texts, rng):
    out = []
    for x in texts:
        y = list(x); rng.shuffle(y); out.append(tuple(y))
    return out
rows = []
for label, texts in (('core 41', [r.tok for r in core]), ('core + unknown-site round', [r.tok for r in core + unk]),
                     ('core + unknown + second-catalogue-only', [r.tok for r in core + unk] + [q.tok for q in mo]),
                     ('core round seals', [r.tok for r in core if r.kind == 'seal' and r.round]), ('core square seals', [r.tok for r in core if r.kind == 'seal' and not r.round])):
    f, rv, nf, nr = count_set(texts)
    sh = np.array([count_set(shuffled(texts, rng))[:2] for _ in range(1000)])
    row = dict(group=label, texts=len(texts), home_order_hits=f, reversed_hits=rv, phrases_found_home_order=nf, phrases_found_reversed=nr,
               shuf_home_order_mean=sh[:, 0].mean(), shuf_reversed_mean=sh[:, 1].mean(),
               P_home_order_more=(np.sum(sh[:, 0] >= f) + 1) / 1001, P_reversed_more=(np.sum(sh[:, 1] >= rv) + 1) / 1001, P_reversed_fewer=(np.sum(sh[:, 1] <= rv) + 1) / 1001,
               P_homeorder_fewer=(np.sum(sh[:, 0] <= f) + 1) / 1001)
    rows.append(row); log(f'{label:44s} phrase hits home order {f} (shuffled {row["shuf_home_order_mean"]:.2f}, P more {row["P_home_order_more"]:.3f}, fewer {row["P_homeorder_fewer"]:.3f}) | reversed {rv} (shuffled {row["shuf_reversed_mean"]:.2f}, P more {row["P_reversed_more"]:.3f}) | distinct phrases {nf} / {nr}')
pd.DataFrame(rows).to_csv(f'{OUT4}/repeats_phrases_reversed.csv', index=False)
log(f'palindromic phrases in list: {palin}')
print('which phrases hit abroad (home order / reversed):')
for r in core + unk:
    for p, q in zip(PH, PHR):
        if find_in(r.tok, p): print('  home order', r.id, r.site, '-'.join(p), ' text', '-'.join(r.tok))
        if find_in(r.tok, q): print('  REVERSED  ', r.id, r.site, '-'.join(p), ' text', '-'.join(r.tok))
