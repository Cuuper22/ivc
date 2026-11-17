#!/usr/bin/env python3
"""STEP 6 of abroad4: do foreign texts share phrases among themselves, and do they obey regularities of their own?
PREDICTIONS (written before running):
 P6a  Pairs and triples (adjacent signs, in order) that recur in 2+ foreign objects and are NOT among the 136 home phrases:
      more than in order-shuffled foreign texts (the round seals share a man-sign + stroke habit: 001-090 / 090-001 / 004-002 style).
      Against random home samples of the same size and kinds the foreign set shares FEWER non-phrase pairs (home samples draw on one system).
 P6b  Region: Gulf texts share with other Gulf texts more than with Mesopotamia (the Gulf round seals are one local set).
 P6c  Leave-one-out sign-pair model trained on the other foreign texts only predicts a held-out foreign text better than
      sign frequencies of the same set (gain over 0.5 bit per step) : the foreign texts have regularities of their own
      even though home rules do not fit them.
Output: work_data/abroad4/internal_*.csv
"""
from abroad4_common import *
from phrases_common import runs
pool = score_home_pool()
PL = pd.read_csv(f'{ROOT}/work_data/phrases/phrase_list.csv', dtype=str)
PH = [tuple(p.split('-')) for p in PL.phrase]
HOMEPAIRS = set()
for p in PH:
    for k in (2, 3):
        for i in range(len(p) - k + 1): HOMEPAIRS.add(p[i:i + k])
def grams(tok, ks=(2, 3)):
    out = set()
    for r in runs(tok):
        for k in ks:
            for i in range(len(r) - k + 1):
                g = r[i:i + k]
                if g not in HOMEPAIRS: out.add(g)
    return out
rng = np.random.default_rng(66)
core = list(F[F.tier == 'core'].itertuples()); unk = list(F[F.tier == 'unk_round'].itertuples())
class R: pass
mo = []
for r in M[(M.site == 'WA') & (~M.partnered)].itertuples():
    q = R(); q.tok = tuple(r.tok); q.kind = 'seal'; q.ag = 'other beast'; q.id = f'M{r.textnum}'; q.rgroup = 'West Asia'; q.site = 'West Asia'; q.round = False; mo.append(q)
def stat(toks):
    c = collections.Counter()
    for x in toks:
        for g in grams(x): c[g] += 1
    sh = {g: n for g, n in c.items() if n >= 2}
    return len(sh), sh
def shuf(toks):
    out = []
    for x in toks:
        y = list(x); rng.shuffle(y); out.append(tuple(y))
    return out
# home matched samples
byn = collections.defaultdict(list)
for j, t in enumerate(pool):
    if t.intact: byn[(t.kind, t.ag, len(t.tok))].append(j)
def cand_n(kind, ag, n):
    c = byn.get((kind, ag, n), [])
    if len(c) >= 5: return c
    c = [j for m in (n - 1, n, n + 1) for j in byn.get((kind, ag, m), [])]
    if len(c) >= 5: return c
    return [j for (k2, a2, m), L in byn.items() if abs(m - n) <= 1 for j in L]
rows = []
for label, rr in (('core 41', core), ('core + unknown-site round', core + unk), ('core + unknown + second-catalogue-only', core + unk + mo),
                  ('round seals (core + unknown)', [r for r in core + unk if r.kind == 'seal' and r.round]), ('core square seals', [r for r in core if r.kind == 'seal' and not r.round])):
    toks = [r.tok for r in rr]
    n_real, sh = stat(toks)
    ds = np.array([stat(shuf(toks))[0] for _ in range(1000)])
    cs = [np.array(cand_n(r.kind, r.ag, max(1, len([s for s in r.tok if real(s)])))) for r in rr]
    dh = np.array([stat([pool[rng.choice(c)].tok for c in cs])[0] for _ in range(1000)])
    row = dict(group=label, texts=len(rr), recurring_grams=n_real, shuffled_mean=ds.mean(), shuffled_max=ds.max(), P_more_than_shuffled=(np.sum(ds >= n_real) + 1) / 1001,
               home_sample_mean=dh.mean(), home_sample_lo=np.percentile(dh, 2.5), P_fewer_than_home=(np.sum(dh <= n_real) + 1) / 1001)
    rows.append(row)
    log(f'{label:42s} recurring non-home grams {n_real} | order-shuffled {ds.mean():.2f} (max {ds.max():.0f}, P {row["P_more_than_shuffled"]:.3f}) | home samples {dh.mean():.1f} (2.5th pct {row["home_sample_lo"]:.0f}, P fewer {row["P_fewer_than_home"]:.3f})')
    if label.startswith('core + unknown-site'):
        print('  the recurring grams:', {'-'.join(g): n for g, n in sorted(sh.items(), key=lambda x: -x[1])})
pd.DataFrame(rows).to_csv(f'{OUT4}/internal_shared.csv', index=False)
# which objects share which gram
allr = core + unk + mo
G = {r.id: grams(r.tok) for r in allr}
share = collections.defaultdict(list)
for r in allr:
    for g in G[r.id]: share[g].append(r)
print('shared grams with their objects:')
listing = []
for g, rs_ in sorted(share.items(), key=lambda kv: -len(kv[1])):
    if len(rs_) >= 2:
        listing.append(dict(gram='-'.join(g), objects=len(rs_), where='; '.join(f'{r.id} {r.site} ({getattr(r,"rgroup","")})' for r in rs_)))
        print('  ', listing[-1]['gram'], listing[-1]['objects'], listing[-1]['where'])
pd.DataFrame(listing).to_csv(f'{OUT4}/internal_grams.csv', index=False)
# by region: text pairs sharing a non-home gram, within and across regions
def rg(r): return getattr(r, 'rgroup', '') or ('Unknown' if r.site == 'Unknown' else '')
regs = {r.id: (r.rgroup if r.rgroup else ('Unknown site' if r.site == 'Unknown' else 'West Asia')) for r in allr}
pairs_ = collections.Counter(); npairs = collections.Counter()
ids = [r.id for r in allr]
for i in range(len(ids)):
    for j in range(i + 1, len(ids)):
        a, b = regs[ids[i]], regs[ids[j]]
        key = tuple(sorted((a, b))); npairs[key] += 1
        if G[ids[i]] & G[ids[j]]: pairs_[key] += 1
reg_rows = [dict(regions=' x '.join(k), text_pairs=npairs[k], pairs_sharing=pairs_[k], share=pairs_[k] / npairs[k]) for k in sorted(npairs)]
# permutation: region labels shuffled among texts
lab = np.array([regs[i] for i in ids]); gs = [G[i] for i in ids]
sharemat = np.array([[bool(gs[i] & gs[j]) if i != j else False for j in range(len(ids))] for i in range(len(ids))])
def within_share(l):
    same = (l[:, None] == l[None, :]); np.fill_diagonal(same, False)
    return sharemat[same].sum() / 2, same.sum() / 2
w_real, w_n = within_share(lab)
pw = np.array([within_share(rng.permutation(lab))[0] for _ in range(2000)])
log(f'same-region text pairs sharing a non-home gram: {w_real:.0f} of {w_n:.0f}; region labels shuffled {pw.mean():.2f}; P (real >= shuffled) {(np.sum(pw >= w_real) + 1) / 2001:.4f}')
pd.DataFrame(reg_rows).to_csv(f'{OUT4}/internal_regions.csv', index=False); print(pd.DataFrame(reg_rows).round(3).to_string())
# ---------------------- own-rules test: leave one out, foreign-only bigram vs foreign-only unigram
V = len(GV) + 50
def loo_gain(texts_tok):
    runs_ = [[s for s in r] for x in texts_tok for r in runs(x)]
    texts_runs = [runs(x) for x in texts_tok]
    uni = collections.Counter(); big = collections.Counter(); out = collections.Counter()
    for tr in texts_runs:
        for r in tr:
            for s in r: uni[s] += 1
            for a, b in zip(r, r[1:]): big[(a, b)] += 1; out[a] += 1
    bu = bb = 0.0; n = 0
    types = collections.defaultdict(set)
    for (a, b) in big: types[a].add(b)
    N = sum(uni.values())
    for i, tr in enumerate(texts_runs):
        u2 = uni.copy(); b2 = big.copy(); o2 = out.copy(); t2 = {a: set(v) for a, v in types.items()}
        N2 = N
        for r in tr:
            for s in r: u2[s] -= 1; N2 -= 1
            for a, b in zip(r, r[1:]):
                b2[(a, b)] -= 1; o2[a] -= 1
        for r in tr:
            for a, b in zip(r, r[1:]):
                pu = (u2[b] + 0.5) / (N2 + 0.5 * V)
                nt = sum(1 for (x, y), c in b2.items() if x == a and c > 0) if o2[a] > 0 else 0
                lam = o2[a] / (o2[a] + nt) if o2[a] > 0 else 0.0
                pb = lam * (b2[(a, b)] / o2[a] if o2[a] > 0 else 0) + (1 - lam) * pu
                bu += -np.log2(pu); bb += -np.log2(pb); n += 1
    return (bu - bb) / n if n else np.nan, n
rows = []
for label, rr, nsamp in (('all round seals (core + unknown)', [r for r in core + unk if r.kind == 'seal' and r.round], 300),
                         ('core square seals', [r for r in core if r.kind == 'seal' and not r.round], 300),
                         ('core + unknown (all)', core + unk, 200)):
    g, n = loo_gain([r.tok for r in rr])
    cs = [np.array(cand_n(r.kind, r.ag, max(1, len([s for s in r.tok if real(s)])))) for r in rr]
    dg = np.array([loo_gain([pool[rng.choice(c)].tok for c in cs])[0] for _ in range(nsamp)])
    rows.append(dict(group=label, texts=len(rr), steps=n, loo_gain_bits=g, home_sample_mean=dg.mean(), home_sample_lo=np.percentile(dg, 2.5), P_below_home=(np.sum(dg <= g) + 1) / (nsamp + 1)))
    log(f'own-rules, leave-one-out gain of pair model over frequencies, {label}: {g:.2f} bits per step over {n} steps; matched home samples of the same size {dg.mean():.2f} (2.5th pct {np.percentile(dg,2.5):.2f}), P(home <= foreign) {rows[-1]["P_below_home"]:.3f}')
pd.DataFrame(rows).to_csv(f'{OUT4}/internal_own_rules.csv', index=False)

# ---------------------- redesign (after P6a/P6b went against): signs together in a text, any order and distance
# PREDICTION written before this block ran: round seals share unordered sign pairs (man sign with a stroke) in 3 or more
# pairs of texts, above matched home samples' lower end; i.e. the sharing exists as co-occurrence even though adjacency is absent.
def cooc(tok):
    r = sorted(set(s for s in tok if real(s)))
    return {(a, b) for i, a in enumerate(r) for b in r[i + 1:]}
def cstat(toks):
    c = collections.Counter()
    for x in toks:
        for g in cooc(x): c[g] += 1
    return sum(1 for n in c.values() if n >= 2), c
rows = []
for label, rr in (('core 41', core), ('round seals (core + unknown)', [r for r in core + unk if r.kind == 'seal' and r.round]), ('core square seals', [r for r in core if r.kind == 'seal' and not r.round])):
    n_real, c = cstat([r.tok for r in rr])
    cs = [np.array(cand_n(r.kind, r.ag, max(1, len([s for s in r.tok if real(s)])))) for r in rr]
    dh = np.array([cstat([pool[rng.choice(cc)].tok for cc in cs])[0] for _ in range(1000)])
    rows.append(dict(group=label, texts=len(rr), shared_unordered_pairs=n_real, home_sample_mean=dh.mean(), home_lo=np.percentile(dh, 2.5), P_fewer=(np.sum(dh <= n_real) + 1) / 1001))
    log(f'unordered sign pairs in 2+ texts, {label}: {n_real} (home samples {dh.mean():.1f}, 2.5th pct {np.percentile(dh,2.5):.0f}, P fewer {rows[-1]["P_fewer"]:.3f})  ' + str({'-'.join(g): n for g, n in c.items() if n >= 2}))
pd.DataFrame(rows).to_csv(f'{OUT4}/internal_cooc.csv', index=False)
