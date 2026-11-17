#!/usr/bin/env python3
"""STEP 8 of abroad4: which of (a) ordinary home texts that travelled, (b) home system with local formulas dropped (names only),
(c) the signs used to write something else, is each kind of foreign object?
PREDICTIONS (written before running):
 (a) Square seals abroad: at least 7 of 11 scorable texts sit inside the home range (under the 90th percentile of matched home
     texts) and the share holding a home phrase is 40% or more of what matched home seals show.
 (b) Square seals abroad lack closers (jar-class) more than home seals do (share of texts ending in a closer or after-jar title
     below the matched home share) while front words stay at the home rate.
 (c) Round seals abroad: 10 or more of 15 scorable texts above the 90th percentile of matched home texts; none holds a home
     phrase in order except by chance (at most 1 of 18).
Per-text percentile: the foreign text's bits per step (sign-pair model) against 2,000 matched home texts (same kind, animal group,
steps); percentile = share of those home texts that cost less.
Output: work_data/abroad4/verdict_*.csv
"""
from abroad4_common import *
from phrases_common import find_in
pool = score_home_pool(); by = pool_index(pool)
PL = pd.read_csv(f'{ROOT}/work_data/phrases/phrase_list.csv', dtype=str); PH = [tuple(p.split('-')) for p in PL.phrase]
def has_phrase(tok): return any(find_in(tok, p) for p in PH)
log('flagging home pool texts that hold a home phrase ...')
# the 136 phrases were found on all home texts, so every home text is "in sample" for phrase presence: flagged with leave-in; noted in report
hp = np.array([has_phrase(t.tok) for t in pool])
log(f'home distinct texts with a phrase: {hp.mean():.1%}')
rows = []; rng = np.random.default_rng(88)
core = list(F[F.tier == 'core'].itertuples())
for r in core:
    s = score_foreign(r)
    shape = 'round seal' if (r.kind == 'seal' and r.round) else ('square seal' if r.kind == 'seal' else r.kind)
    row = dict(id=r.id, site=r.site, shape=shape, text='-'.join(r.tok), n_step=s.n_step, phrase=has_phrase(r.tok))
    if s.n_step >= 1:
        c, lv = candidates(by, pool, s.kind, s.ag, s.n_step)
        hb = np.array([pool[j].tr[:, 1].mean() for j in c])
        row['bits_sign_pair'] = s.tr[:, 1].mean(); row['percentile_vs_home'] = float((hb < row['bits_sign_pair']).mean()); row['n_controls'] = len(c)
        row['home_phrase_share_controls'] = float(hp[c].mean())
    rows.append(row)
V = pd.DataFrame(rows); V.to_csv(f'{OUT4}/verdict_per_object.csv', index=False)
print(V[['id', 'site', 'shape', 'text', 'n_step', 'bits_sign_pair', 'percentile_vs_home', 'phrase']].round(2).to_string())
out = []
for shape, g in V.groupby('shape'):
    sc = g[g.n_step >= 1]
    exp_ph = sum(g.home_phrase_share_controls.fillna(hp.mean()))   # expected number of phrase-holding objects if they were matched home texts
    out.append(dict(shape=shape, objects=len(g), scorable=len(sc), above_90th=int((sc.percentile_vs_home >= 0.9).sum()), above_95th=int((sc.percentile_vs_home >= 0.95).sum()),
                    below_median=int((sc.percentile_vs_home < 0.5).sum()), mean_percentile=sc.percentile_vs_home.mean(), holding_home_phrase=int(g.phrase.sum()), expected_if_home=exp_ph))
O = pd.DataFrame(out); O.to_csv(f'{OUT4}/verdict_by_shape.csv', index=False); print(O.round(2).to_string())
tot = V[V.n_step >= 1]
log(f'all scorable {len(tot)}: above 90th {int((tot.percentile_vs_home>=.9).sum())} (5% would be 10% expected at the 90th line: {0.1*len(tot):.1f}), above 95th {int((tot.percentile_vs_home>=.95).sum())} (expected {0.05*len(tot):.1f})')
# phrase presence matched: draws, 41 objects
def phrase_draw(sub):
    exp = []
    cs = []
    for r in sub.itertuples():
        s = score_foreign([x for x in core if x.id == r.id][0]) if r.n_step >= 1 else None
    return None
# matched on kind, animal group, number of real signs (not steps) so that texts with 0 steps count too
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
rows = []
for label, f in (('all 41 core', lambda r: True), ('round seals', lambda r: r.kind == 'seal' and r.round), ('square seals', lambda r: r.kind == 'seal' and not r.round), ('other objects', lambda r: r.kind != 'seal')):
    sub = [r for r in core if f(r)]
    cs = [np.array(cand_n(r.kind, r.ag, max(1, len([s for s in r.tok if real(s)])))) for r in sub]
    dr = np.array([sum(hp[rng.choice(c)] for c in cs) for _ in range(2000)])
    real_n = sum(has_phrase(r.tok) for r in sub)
    rows.append(dict(group=label, objects=len(sub), holding_home_phrase=real_n, matched_home_mean=dr.mean(), matched_lo=np.percentile(dr, 2.5), P_fewer=(np.sum(dr <= real_n) + 1) / 2001))
    log(f'objects holding a home phrase, {label}: {real_n} of {len(sub)} (matched home texts {dr.mean():.1f}, 2.5th percentile {np.percentile(dr,2.5):.0f}, P fewer {rows[-1]["P_fewer"]:.4f})')
pd.DataFrame(rows).to_csv(f'{OUT4}/verdict_phrase_presence.csv', index=False)
# (b) front / ending by class on non-round vs round, intact-or-not first/last real sign: use texts with the edge sign adjacent to a true edge
# front: first token is a usable sign and the face is not broken at the front end: use complete texts (clean) only
cl = lambda s: V2CLASS.get(s, 'PERSONAL')
def edge_shares(sub):
    cl_ok = [r for r in sub if r.clean and edge_ok(r.tok)]
    f_open = sum(cl(r.tok[0]) in ('OPEN',) for r in cl_ok); e_close = sum(cl(r.tok[-1]) in ('CLOSER', 'TITLE') for r in cl_ok)
    cs = [np.array(cand_n(r.kind, r.ag, len(r.tok))) for r in cl_ok]
    d_f = np.array([sum(cl(pool[rng.choice(c)].tok[0]) == 'OPEN' for c in cs) for _ in range(2000)])
    d_e = np.array([sum(cl(pool[rng.choice(c)].tok[-1]) in ('CLOSER', 'TITLE') for c in cs) for _ in range(2000)])
    return len(cl_ok), f_open, d_f.mean(), (np.sum(d_f <= f_open) + 1) / 2001, e_close, d_e.mean(), (np.sum(d_e <= e_close) + 1) / 2001
rows = []
for label, f in (('all intact', lambda r: True), ('round seals', lambda r: r.kind == 'seal' and r.round), ('square seals', lambda r: r.kind == 'seal' and not r.round)):
    n, fo, dfm, pf, ec, dem, pe = edge_shares([r for r in core if f(r)])
    rows.append(dict(group=label, intact_texts=n, start_with_front_word=fo, home_matched_front=dfm, P_front_fewer=pf, end_with_closer_or_title=ec, home_matched_end=dem, P_end_fewer=pe))
    log(f'intact {label:13s} n={n:2d}: begin with a front word {fo} (home {dfm:.1f}, P fewer {pf:.3f}) | end in a closer/after-jar title {ec} (home {dem:.1f}, P fewer {pe:.3f})')
pd.DataFrame(rows).to_csv(f'{OUT4}/verdict_edges.csv', index=False)
