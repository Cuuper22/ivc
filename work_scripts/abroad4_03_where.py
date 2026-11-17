#!/usr/bin/env python3
"""STEP 3 of abroad4: where does the difference sit (front / middle / ending), which signs are over- and under-used,
rare signs, signs found only abroad.
PREDICTIONS (written before running):
 P3a  On texts with both edges intact, the ending costs more abroad than at home (the jar and the after-jar titles are missing)
      and the front costs more abroad (no front words 861 / 817 / 820); the middle costs more only for round seals.
 P3b  Share of tokens in the front-word class (OPEN) is lower abroad than in matched home texts; the share in the closer class
      (jar 740 and the other closers) is lower abroad; the jar 740 itself: round seals 0 of 15 with man; plain jar present on
      far fewer round seals than at home.
 P3c  Fish name signs (220 231 233 235 240) under-used abroad; count strokes (short strokes) over-used on round seals.
 P3d  Rare signs (home distinct-text uses under 5, own text left out) are a larger share of tokens abroad than in matched home
      texts, and about 5 or more signs occur only abroad (091 twin men first among them).
Matching: same kind, same animal group (seals), same number of real signs; 2,000 draws; for the edge buckets: intact home
texts of the same kind, animal group, number of steps.
Output: work_data/abroad4/where_*.csv
"""
from abroad4_common import *
pool = score_home_pool(); by = pool_index(pool)
shapes = pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv', dtype=str).set_index('lipi_wells_number').shape_description.to_dict()
core_rows = list(F[F.tier == 'core'].itertuples())
fs = [(r, score_foreign(r)) for r in core_rows]
rng = np.random.default_rng(33)

# ------------------------------------------------------------ A. edge buckets on intact texts
def buckets(t, col):
    """front = start event; middle = steps into signs 2..n-1; last = step into the last sign; end = end event."""
    tr = t.tr[:, col]
    return dict(front=t.st[col], middle=tr[:-1].tolist(), last=tr[-1] if len(tr) else np.nan, end=t.en[col])
rowsA = []
for label, f in (('all intact', lambda r: True), ('round seals', lambda r: r.kind == 'seal' and r.round), ('square seals', lambda r: r.kind == 'seal' and not r.round)):
    subj = [s for r, s in fs if f(r) and s.intact and s.n_step >= 1]
    if not subj: continue
    intact_pool = [j for j, t in enumerate(pool) if t.intact and t.n_step >= 1]
    by_i = pool_index([t if t.intact else Scored((), t.kind, t.ag, t.id, np.zeros((0, 4)), t.st, t.en, False) for t in pool])
    idx, lv = matched_draws(pool, by_i, subj, 2000, 77, shape_rule=lambda t: t.intact)
    for c in (1, 2):
        nm = NMODEL[c]
        def agg(texts):
            b = [buckets(t, c) for t in texts]
            mid = [x for q in b for x in q['middle']]
            return dict(front=np.nanmean([q['front'] for q in b]), middle=np.mean(mid) if mid else np.nan,
                        last=np.nanmean([q['last'] for q in b]), end=np.nanmean([q['end'] for q in b]))
        realv = agg(subj)
        dr = {k: [] for k in realv}
        for row in idx[::4]:     # 500 of the 2000 draws for speed
            a = agg([pool[j] for j in row])
            for k in realv: dr[k].append(a[k])
        for k in realv:
            s = summarize(realv[k], np.array(dr[k]))
            rowsA.append(dict(group=label, texts=len(subj), model=nm, bucket=k, **s))
A = pd.DataFrame(rowsA); A.to_csv(f'{OUT4}/where_edges.csv', index=False)
log('A. edge buckets (bits per sign / event)'); print(A.round(3).to_string())

# ------------------------------------------------------------ B. class shares and named signs, token level
def real_signs(tok): return [s for s in tok if real(s)]
clean_pool = [t for t in pool if t.intact]
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
def draw_idx(subj, nd=2000, seed=5):
    r = np.random.default_rng(seed)
    cs = [np.array(cand_n(rr.kind, rr.ag, max(1, len(real_signs(rr.tok))))) for rr in subj]
    return np.stack([r.choice(c, size=nd) for c in cs], 1)
HD = collections.Counter(s for x in home_distinct for s in x if real(s))      # distinct-text token counts at home
subjB = [r for r, s in fs]
IDXB = draw_idx(subjB)
cls_of = lambda s: V2MAP.get(s, 'PERSONAL')
def tally(toks_list):
    c = collections.Counter(); t = collections.Counter(); n = 0
    for toks in toks_list:
        rs = real_signs(toks); n += len(rs)
        for s in rs: c[s] += 1
        for s in set(rs): t[s] += 1
    return c, t, n
fc, ft, fn = tally([r.tok for r in subjB])
nd = IDXB.shape[0]
hc = np.zeros((nd, len(GV))); ht = np.zeros((nd, len(GV))); hn = np.zeros(nd)
tokcnt = [np.bincount([GIDX[s] for s in real_signs(t.tok)], minlength=len(GV)) for t in pool]
tokcnt = np.array(tokcnt); presence = (tokcnt > 0).astype(int); ntok = tokcnt.sum(1)
for k in range(IDXB.shape[1]):
    hc += tokcnt[IDXB[:, k]]; ht += presence[IDXB[:, k]]; hn += ntok[IDXB[:, k]]
log(f'B. foreign core tokens (real signs) {fn}; matched home tokens per draw {hn.mean():.1f}')
# class shares
cls_names = V2_CLASSES
cidx = {c: [GIDX[s] for s in GV if cls_of(s) == c] for c in cls_names}
rowsB = []
for c in cls_names:
    real_n = sum(v for s, v in fc.items() if cls_of(s) == c)
    dr = hc[:, cidx[c]].sum(1) / hn
    s = summarize(real_n / fn, dr); rowsB.append(dict(item='class ' + c, abroad_tokens=real_n, abroad_share=real_n / fn, **s))
for s_ in ['740', '400', '090', '861', '817', '820', '220', '231', '233', '235', '240', '001', '002', '003', '004', '031', '032', '033', '060', '091']:
    real_n = fc.get(s_, 0)
    if s_ in GIDX: dr = hc[:, GIDX[s_]] / hn
    else: dr = np.zeros(nd)
    s = summarize(real_n / fn, dr); rowsB.append(dict(item='sign ' + s_, abroad_tokens=real_n, abroad_share=real_n / fn, **s))
# fish group, short-stroke counts group
grp = {'fish signs 220 231 233 235 240': ['220', '231', '233', '235', '240'], 'count strokes (class NUM_SHORT+NUM_TALL+NUM_NAME)': [s for s in GV if cls_of(s) in ('NUM_SHORT', 'NUM_TALL', 'NUM_NAME')],
       'after-jar titles 400 090': ['400', '090']}
for nm, ss in grp.items():
    real_n = sum(fc.get(s, 0) for s in ss); dr = hc[:, [GIDX[s] for s in ss if s in GIDX]].sum(1) / hn
    s = summarize(real_n / fn, dr); rowsB.append(dict(item=nm, abroad_tokens=real_n, abroad_share=real_n / fn, **s))
B = pd.DataFrame(rowsB); B.to_csv(f'{OUT4}/where_classes_signs.csv', index=False); print(B.round(4).to_string())

# per-sign scan: over-used and under-used abroad
rowsS = []
for s, n in fc.most_common():
    if s in GIDX:
        dr = hc[:, GIDX[s]]
        rowsS.append(dict(sign=s, abroad=n, abroad_texts=ft[s], home_expected=dr.mean(), ratio=n / max(dr.mean(), 1e-9), P_abroad_more=(np.sum(dr >= n) + 1) / (nd + 1), home_uses=HD[s], shape=shapes.get(s, '')[:60]))
    else:
        rowsS.append(dict(sign=s, abroad=n, abroad_texts=ft[s], home_expected=0.0, ratio=np.inf, P_abroad_more=1 / (nd + 1), home_uses=0, shape=shapes.get(s, '')[:60]))
S = pd.DataFrame(rowsS)
S['P_abroad_less'] = np.nan
rowsU = []
for s_ in GV:
    dr = hc[:, GIDX[s_]]; o = fc.get(s_, 0)
    if dr.mean() >= 1.5:
        rowsU.append(dict(sign=s_, abroad=o, abroad_texts=ft.get(s_, 0), home_expected=dr.mean(), ratio=o / dr.mean(), P_abroad_less=(np.sum(dr <= o) + 1) / (nd + 1), home_uses=HD[s_], shape=shapes.get(s_, '')[:60]))
U = pd.DataFrame(rowsU)
S.to_csv(f'{OUT4}/where_sign_scan.csv', index=False); U.to_csv(f'{OUT4}/where_sign_under.csv', index=False)
log('over-used abroad (P<0.05, abroad>=2):'); print(S[(S.P_abroad_more < 0.05) & (S.abroad >= 2)].sort_values('P_abroad_more').round(3).to_string())
log('signs expected >=1.5 in matched home texts, abroad count and P(home draws <= abroad count) lowest 12:'); print(U.sort_values('P_abroad_less').head(12).round(3).to_string())
log(f'tested {len(U)} signs for under-use; with P<0.05: {(U.P_abroad_less<0.05).sum()}')

# ------------------------------------------------------------ D. rare signs and signs found only abroad
def rare_share(toks, own, thr=5):
    r = [s for s in real_signs(toks)]
    return sum(1 for s in r if HD[s] - own.get(s, 0) < thr), len(r)
rows_D = []
for label, f in (('all 41 core', lambda r: True), ('round seals', lambda r: r.kind == 'seal' and r.round), ('square seals', lambda r: r.kind == 'seal' and not r.round)):
    sub = [i for i, r in enumerate(subjB) if f(r)]
    for thr, nmz in ((5, 'home uses under 5'), (1, 'never at home')):
        a = sum(rare_share(subjB[i].tok, {}, thr)[0] for i in sub); n = sum(len(real_signs(subjB[i].tok)) for i in sub)
        # home matched: own text left out
        dr = []
        for k in range(0, nd, 4):
            tot = 0; nn = 0
            for col, i in enumerate(sub):
                t = pool[IDXB[k, i]]; own = collections.Counter(real_signs(t.tok))
                a_, n_ = rare_share(t.tok, own, thr); tot += a_; nn += n_
            dr.append(tot / nn)
        s = summarize(a / n, np.array(dr)); rows_D.append(dict(group=label, measure=nmz, abroad_tokens=a, of=n, **s))
D = pd.DataFrame(rows_D); D.to_csv(f'{OUT4}/where_rare.csv', index=False); log('D. rare signs'); print(D.round(4).to_string())
tiers_all = F[F.tier.isin(['core', 'unk_round'])]
Mo = M[(M.site == 'WA') & (~M.partnered)]
Mh = M[(M.site != 'WA')]
m_home_signs = collections.Counter(s for x in Mh.tok for s in x if real(s))
rows_O = []
sc = collections.defaultdict(list)
for r in tiers_all.itertuples():
    for s in set(real_signs(r.tok)):
        sc[s].append((r.id, r.tier, r.site))
for s, lst in sc.items():
    if HD[s] == 0:
        rows_O.append(dict(sign=s, abroad_objects=len(lst), where='; '.join(f'{i} {st}' for i, t, st in lst), in_second_catalogue_home_lines=m_home_signs.get(s, 0), shape=shapes.get(s, '(no entry)')))
for r in Mo.itertuples():
    for s_ in set(real_signs(r.tok)):
        if HD[s_] == 0: rows_O.append(dict(sign=s_, abroad_objects=1, where=f'M{r.textnum} second catalogue West Asia', in_second_catalogue_home_lines=m_home_signs.get(s_, 0), shape=shapes.get(s_, '(no entry)')))
O = pd.DataFrame(rows_O); O.to_csv(f'{OUT4}/where_abroad_only_signs.csv', index=False); log('E. signs found only abroad (Lipi, core + unknown-site round)'); print(O.to_string())
