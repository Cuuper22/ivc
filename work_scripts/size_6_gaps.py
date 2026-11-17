#!/usr/bin/env python3
"""SIZE step 6: does size help restore a lost sign?  Written 2026-11-17 before any number.

Gap items: the 77 fill-the-gap texts of frame v2 (frame2_score.py rule: a crosswalk pair where one catalogue lost one
sign that the other has). Sign model: sign pairs mixed 0.5/0.5 with the pushed v2 class grammar (pooled), trained with
the gap faces left out (the restorations_v2 model). Size model: model (d) (length + site + format + ridge sign weights)
trained on complete seals whose text is not a gap text or its answer; sigma = its residual spread.
Items scored with size: those whose first-catalogue object is a SEAL with a face size. Combined score of candidate c:
log P_signs(c) + log Normal(logA_seal ; prediction with c in the gap, sigma). Control: sizes dealt among the scored
items' seals (20 deals).
Also: on all 1,971 restorations (restorations_v2.csv), how often does size change the top candidate on seals with size.

PREDICTIONS:
  G1  Top-1 rises by at least 2 points with size; top-5 does not fall.
  G2  With dealt sizes, top-1 does not rise.
REDESIGN (added after G1 went against, before its run): the per-sign weight is replaced by the size weight of the
candidate's frame-v2 job (mean ridge weight of the job's signs in 4+ seals, ladder_all.csv), and size only reorders the
sign model's top 10.
"""
from size_common import *
with contextlib.redirect_stdout(io.StringIO()):
    from frame2_common import *   # d, M, pairs, train_texts, vocab_of, kind_counts, bigram_model, class_model_kind, ...
from size_common import table, base_X, sign_X, ridge_cv, ridge_fit, ridge_pred, OUT, log, V2

c2 = pd.read_csv(f'{ROOT}/work_data/frame/classes_v2.csv', dtype=str).fillna('')
PUSH = dict(zip(c2.sign, c2.v2_pushed))
mah2lipi = dict(zip(M.reading_mah, M.tok))
items = []; seen = set()
for g_, lt, mt in zip(pairs.group, pairs.lipi_text, pairs.mahadevan_text):
    L = tuple(lt.split('-')); Mt = mah2lipi.get(mt)
    if Mt is None or len(L) != len(Mt): continue
    for gapped, full_ in ((L, Mt), (Mt, L)):
        lost = [i for i, s in enumerate(gapped) if s == '000']
        if len(lost) != 1 or set(full_) & UNK or any(s.startswith('X') for s in full_): continue
        p = lost[0]
        if any(gapped[i] != full_[i] for i in range(len(L)) if i != p): continue
        key = (gapped, full_[p])
        if key in seen: continue
        seen.add(key); items.append(dict(lipi_text=lt, context=gapped, pos=p, true=full_[p], answer='-'.join(full_)))
log('S6', f'gap items: {len(items)}')
excl_text = {it['lipi_text'] for it in items} | {it['answer'] for it in items}
excl_ids = {i for i, x in zip(d.id, d.tok) if '-'.join(x) in excl_text}
Tg = train_texts(frozenset(excl_ids)); gv, gidx = vocab_of(Tg); gC, gCK = kind_counts(Tg, gidx)
gbig = bigram_model(gC)
gm = class_model_kind(gC, gCK, {s: PUSH.get(s, 'UNSEEN') for s in gv}, 'v2 pushed', gv, pooled_only=True)
mix = mix_kind(FixedKind(gbig), gm, 0.5, 'mix')

# size model
St = table()
Sall = St.copy()
St = St[~St.signs.isin(excl_text)].reset_index(drop=True)
toks = list(St.tok); cnt = collections.Counter(s for t in toks for s in set(t)); signs = sorted(s for s, n in cnt.items() if n >= 2)
Bf, lv = base_X(St); B = Bf.values; Z = sign_X(toks, signs); y = St.logA.values
lam = ridge_cv(B, Z, y, St.signs.values, 0); wb, wz = ridge_fit(B, Z, y, lam)
sig = np.std(y - ridge_pred(B, Z, wb, wz))
W = dict(zip(signs, wz))
log('S6', f'size model on {len(St)} seals, penalty {lam}, residual sigma {sig:.3f}')

# seals (any completeness) with a size, per Lipi text string (stored text incl. 000)
with contextlib.redirect_stdout(io.StringIO()):
    from twins_common import seals
A = seals(); A = A[A.area_mm2.notna()].copy(); A['logA'] = np.log(A.area_mm2)
A['siteg'] = A.site.map({'Mohenjo-daro': 'MD', 'Harappa': 'HP', 'Dholavira': 'DHO', 'Lothal': 'LOT', 'Chanhu-daro': 'CHD', 'Kalibangan': 'KLB'}).fillna('other')
A['L'] = A.n.clip(upper=8).astype(int)


def base_pred(row):
    one = pd.DataFrame([row])
    X, _ = base_X(one, lv)
    for c in Bf.columns:
        if c not in X: X[c] = 0.0
    return wb[0] + X[Bf.columns].values[0] @ wb[1:]


def size_term(row, ctx, pos, cand_ids, logA):
    known = sum(W.get(s, 0.0) for i, s in enumerate(ctx) if i != pos and s != '000')
    pb = base_pred(row) + known
    wc = np.array([W.get(gv[c], 0.0) for c in cand_ids])
    return -((logA - pb - wc) ** 2) / (2 * sig ** 2)


scored = []
for it in items:
    m = A[A.signs == it['lipi_text']]
    if not len(m): continue
    row = m.iloc[0]
    ids = [gidx.get(s) if s != '000' else None for s in it['context']]
    tr_ = gidx.get(it['true'])
    if tr_ is None or any(i is None for j, i in enumerate(ids) if j != it['pos']): continue
    p = gap_posteriors(mix.get('seal'), ids, True)[it['pos']]
    scored.append(dict(it=it, row=row, p=p, tr=tr_, logA=float(m.logA.mean())))
log('S6', f'gap items whose first-catalogue object is a seal with a size: {len(scored)} of {len(items)}')


def score(logAs):
    h0 = np.zeros(3); h1 = np.zeros(3)
    for s, la in zip(scored, logAs):
        lp = np.log(s['p'] + 1e-300)
        st = size_term(s['row'], s['it']['context'], s['it']['pos'], np.arange(len(gv)), la)
        comb = lp + st
        for h, sc in ((h0, lp), (h1, comb)):
            rk = int((sc > sc[s['tr']]).sum()); h += [rk < 1, rk < 5, rk < 10]
    return h0 / len(scored), h1 / len(scored)
real = [s['logA'] for s in scored]
h0, h1 = score(real)
log('S6', f'without size: top1/5/10 {h0.round(3)}; with size {h1.round(3)}')
rr = np.random.default_rng(31); dec = []
for q in range(20):
    dec.append(score(list(rr.permutation(real)))[1])
dec = np.array(dec)
log('S6', f'with sizes dealt among the item seals (20 deals): mean {dec.mean(0).round(3)} max top1 {dec[:,0].max():.3f}')
rows = [dict(model='signs only', top1=h0[0], top5=h0[1], top10=h0[2]), dict(model='signs + size', top1=h1[0], top5=h1[1], top10=h1[2]),
        dict(model='signs + dealt size (mean of 20)', top1=dec[:, 0].mean(), top5=dec[:, 1].mean(), top10=dec[:, 2].mean())]
# per item detail
det = []
for s in scored:
    lp = np.log(s['p'] + 1e-300); st = size_term(s['row'], s['it']['context'], s['it']['pos'], np.arange(len(gv)), s['logA'])
    det.append(dict(text=s['it']['answer'], pos=s['it']['pos'], true=s['it']['true'], top_signs=gv[int(np.argmax(lp))],
                    top_with_size=gv[int(np.argmax(lp + st))], rank_signs=int((lp > lp[s['tr']]).sum()) + 1,
                    rank_with_size=int((lp + st > (lp + st)[s['tr']]).sum()) + 1, true_weight=W.get(s['it']['true'], 0.0)))
pd.DataFrame(det).to_csv(f'{OUT}/gaps_items.csv', index=False)
pd.DataFrame(rows).to_csv(f'{OUT}/gaps.csv', index=False)

# restorations on broken seals: does size change the top candidate?
R = pd.read_csv(f'{ROOT}/work_data/frame/restorations_v2.csv', dtype=str).fillna('')
R = R[R.object_kind == 'seals']
ch = 0; n = 0; ex = []
Af = A.set_index('face')
for _, r in R.iterrows():
    row = Af.loc[r.face] if r.face in Af.index else None
    if row is None or isinstance(row, pd.DataFrame): continue
    cands = [r.cand1, r.cand2, r.cand3]; ps = np.array([float(r.p1 or 0), float(r.p2 or 0), float(r.p3 or 0)])
    if ps.sum() == 0: continue
    ctx = r.signs.split('-'); pos = int(r.position)
    known = sum(W.get(s, 0.0) for i, s in enumerate(ctx) if i != pos and s not in ('000', 'ALT'))
    row2 = row.copy(); pb = base_pred(row2) + known
    sc = np.log(ps + 1e-12) - ((row.logA - pb - np.array([W.get(c, 0.0) for c in cands])) ** 2) / (2 * sig ** 2)
    n += 1
    if int(np.argmax(sc)) != 0: ch += 1; ex.append((r.cisi, r.signs, pos, cands[0], cands[int(np.argmax(sc))]))
log('S6', f'restorations on seals with a size: {n}; size changes the top candidate (among the top 3) in {ch}')
for e in ex[:15]: log('S6', '   ', e)
pd.DataFrame(ex, columns=['cisi', 'signs', 'position', 'top_without_size', 'top_with_size']).to_csv(f'{OUT}/gaps_restorations_changed.csv', index=False)

# ---------------- redesign: job-level size, top-10 only
LA = pd.read_csv(f'{OUT}/ladder_all.csv', dtype={'sign': str})
JW = LA[LA.seals >= 4].groupby('v2').weight.mean().to_dict()
def jw(s): return JW.get(V2.get(s, 'PERSONAL'), 0.0)
def score2(logAs):
    h0 = np.zeros(3); h1 = np.zeros(3)
    for s, la in zip(scored, logAs):
        lp = np.log(s['p'] + 1e-300)
        ctx, pos = s['it']['context'], s['it']['pos']
        pb = base_pred(s['row']) + sum(jw(x) for i, x in enumerate(ctx) if i != pos and x != '000')
        top = np.argsort(-lp)[:10]
        comb = lp.copy()
        comb[top] = lp[top] - ((la - pb - np.array([jw(gv[c]) for c in top])) ** 2) / (2 * sig ** 2)
        for h, sc in ((h0, lp), (h1, comb)):
            rk = int((sc > sc[s['tr']]).sum()); h += [rk < 1, rk < 5, rk < 10]
    return h0 / len(scored), h1 / len(scored)
g0, g1 = score2(real)
dec2 = np.array([score2(list(rr.permutation(real)))[1] for q in range(20)])
log('S6', f'REDESIGN job-level size on top 10: without {g0.round(3)} with {g1.round(3)}; dealt sizes mean {dec2.mean(0).round(3)}')
pd.DataFrame(rows + [dict(model='redesign: signs + job-level size (top 10)', top1=g1[0], top5=g1[1], top10=g1[2]),
                     dict(model='redesign with dealt sizes (mean of 20)', top1=dec2[:, 0].mean(), top5=dec2[:, 1].mean(), top10=dec2[:, 2].mean())]).to_csv(f'{OUT}/gaps.csv', index=False)
