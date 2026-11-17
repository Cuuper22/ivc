#!/usr/bin/env python3
"""STEPS 2, 3, 5. Prediction on new texts, fill-the-gap, decoy frame. Fixed before any score (2026-11-17):

STEP 2  Train on distinct first-catalogue texts (frame_common.train_texts). Score the new texts (second-catalogue lines
  with no partner, complete, no lost sign, no unmapped sign, every sign seen in training) in bits per sign
  (-log2 probability of the whole line including the end-of-text event, divided by its number of signs; a second
  figure leaves the end event out). Models: unigram; sign bigram; class grammars with the hand jobs, HMM K=10 classes,
  k-means K=10, exchange K=10 (and HMM K=6/8/12 classes for the record); the soft HMM K=10; mixes of bigram with a
  class grammar (0.5/0.5).
  Controls on the same lines: (i) order shuffled within each line (10 shuffles, mean); (ii) each sign replaced by a
  same-frequency sign (sign types dealt among signs of the same training-frequency band, 10 deals, mean).
  Share of order captured by jobs = (unigram - class) / (unigram - bigram) bits.
STEP 3  Gap test items from the crosswalk text pairs: one side has exactly one lost sign, the other side has the same
  text complete, same length, every other position equal (main set); a second set allows one other mismatch.
  Training for the gap test leaves out every Lipi face whose text is a test text or the completed answer.
  Gap posterior by forward-backward over the sign chain of each model (edges counted as text start / end).
  Scores: true sign in top 1 / 5 / 10, against a frequency-only guess (training unigram order). Job class:
  argmax of the posterior summed by class, scored against the true sign's class in the same map; baseline = the most
  common class. Items whose true sign never occurs in training count as misses for every model.
  Restorations: all lost / unclear tokens on the 2,079 damaged first-catalogue faces, full training set, the model with
  the best top-5 on the main gap set; predicted hand job (from the hand-class grammar posterior) and machine class;
  edges are counted only on faces with no broken edge.
STEP 5  Decoy frames: the hand jobs dealt to other signs of the same training-frequency band (20 deals, seeds 500+).
  Each decoy class grammar is scored exactly like the real hand grammar in steps 2 and 3.
"""
from frame_common import *

KMAIN = 10; NDECOY = 20; NCTRL = 10
cls = pd.read_csv(f'{OUT}/classes.csv', dtype=str).fillna('')
MAPS = {'hand jobs': dict(zip(cls.sign, cls.hand_job))}
for c in ['hmm10', 'kmeans10', 'exchange10', 'hmm6', 'hmm8', 'hmm12']: MAPS[c] = dict(zip(cls.sign, cls[c]))
for k in list(MAPS['hand jobs']):
    if not MAPS['hand jobs'][k]: MAPS['hand jobs'].pop(k)
hp = np.load(f'{OUT}/hmm10_params.npy', allow_pickle=True).item()


def build_models(T, decoy_seeds=range(500, 500 + NDECOY)):
    vocab, idx = vocab_of(T); C = counts(T, idx)
    uni = unigram_model(C); big = bigram_model(C)
    ms = {'unigram': uni, 'sign bigram': big}
    cinfo = {}
    for name, mp in MAPS.items():
        m, info = class_model(C, mp, f'class grammar: {name}', vocab); ms[m.name] = m; cinfo[name] = info
    ms['mix: bigram + hand jobs'] = mix_model(big, ms['class grammar: hand jobs'], 0.5, 'mix: bigram + hand jobs')
    ms['mix: bigram + hmm10'] = mix_model(big, ms['class grammar: hmm10'], 0.5, 'mix: bigram + hmm10')
    band = freq_band({s: int(C['uni'][idx[s]]) for s in vocab})
    dec = {}
    for q in decoy_seeds:
        dm = deal_within_bands({s: MAPS['hand jobs'][s] for s in vocab if s in MAPS['hand jobs']}, band, q)
        m, info = class_model(C, dm, f'decoy {q}', vocab); dec[q] = (m, dm)
    return vocab, idx, C, ms, dec, band, cinfo


# ================================================================ STEP 2
log('STEP 2: training on all distinct first-catalogue texts ...')
T = train_texts()
vocab, idx, C, MS, DEC, band, CINFO = build_models(T)
log(f'vocabulary {len(vocab)} signs; models: {list(MS)} + {len(DEC)} decoy frames')
# soft HMM (vocab of the saved model is the same training set)
assert list(hp['vocab']) == vocab
hmm = HMM(10, len(vocab), 0); hmm.pi, hmm.A, hmm.B = hp['pi'], hp['A'], hp['B']

Mu = M[~M.partnered]
cand = [(tuple(x), k) for x, c, k in zip(Mu.tok, Mu.complete_b, Mu.kind) if c and x and not (set(x) & UNK) and not any(s.startswith('X') for s in x)]
NEW = [(x, k) for x, k in cand if all(s in idx for s in x)]
log(f'new texts: {len(Mu)} lines; complete with every sign mapped {len(cand)}; every sign seen in training {len(NEW)} (scored); distinct {len(set(x for x, k in NEW))}')
rng = np.random.default_rng(2026)


def score(m, lines, use_end=True):
    lp = 0.0; n = 0
    for x in lines:
        ids = [idx[s] for s in x]; lp += m.logprob(ids, use_end); n += len(ids)
    return -lp / n


def score_hmm(lines, use_end=True):
    O, mk = pad(list(lines), idx)
    if use_end: lp = hmm.logprob2(O, mk).sum()
    else:
        # without end: forward with end factor 1
        al, be, sc, E, ll, gam, endf, zend = hmm.forward_backward(O, mk, np.zeros(len(O), bool)); lp = ll.sum() / np.log(2)
    return -lp / mk.sum()


lines = [x for x, k in NEW]
shuf = [[tuple(rng.permutation(list(x))) for x in lines] for _ in range(NCTRL)]
def freq_deal(seed):
    r = np.random.default_rng(seed); by = collections.defaultdict(list)
    for s in vocab: by[band[s]].append(s)
    mp = {}
    for b, ss in by.items():
        p = r.permutation(len(ss))
        for s, q in zip(ss, p): mp[s] = ss[q]
    return mp
fdeals = [freq_deal(700 + q) for q in range(NCTRL)]
freqrep = [[tuple(mp[s] for s in x) for x in lines] for mp in fdeals]

rows = []
for name, m in list(MS.items()):
    r = dict(model=name, real=score(m, lines), real_no_end=score(m, lines, False),
             order_shuffled=np.mean([score(m, L) for L in shuf]), freq_replaced=np.mean([score(m, L) for L in freqrep]))
    rows.append(r); log(f'  {name:34s} real {r["real"]:.3f} bits/sign | order shuffled {r["order_shuffled"]:.3f} | same-frequency signs {r["freq_replaced"]:.3f} | no end {r["real_no_end"]:.3f}')
r = dict(model='hidden-state model K=10 (soft)', real=score_hmm(lines), real_no_end=score_hmm(lines, False),
         order_shuffled=np.mean([score_hmm(L) for L in shuf]), freq_replaced=np.mean([score_hmm(L) for L in freqrep]))
rows.append(r); log(f'  {r["model"]:34s} real {r["real"]:.3f} | order shuffled {r["order_shuffled"]:.3f} | same-frequency {r["freq_replaced"]:.3f}')
dec_real = []
for q, (m, dm) in DEC.items():
    dec_real.append(dict(seed=q, real=score(m, lines), real_no_end=score(m, lines, False), order_shuffled=np.mean([score(m, L) for L in shuf[:3]])))
dd = pd.DataFrame(dec_real); dd.to_csv(f'{OUT}/decoy_bits.csv', index=False)
rows.append(dict(model=f'DECOY class grammar (hand jobs dealt within frequency bands), mean of {NDECOY}', real=dd.real.mean(), real_no_end=dd.real_no_end.mean(), order_shuffled=dd.order_shuffled.mean()))
rows.append(dict(model=f'DECOY best of {NDECOY}', real=dd.real.min(), real_no_end=dd.real_no_end.min()))
B = pd.DataFrame(rows); B.to_csv(f'{OUT}/bits_per_sign.csv', index=False)
log(f'  decoy class grammars: mean {dd.real.mean():.3f}, best {dd.real.min():.3f}, worst {dd.real.max():.3f} bits/sign; real hand-job grammar {B.set_index("model").loc["class grammar: hand jobs", "real"]:.3f}')
u = B.set_index('model').real
for nm in ['class grammar: hand jobs', 'class grammar: hmm10', 'class grammar: kmeans10', 'class grammar: exchange10']:
    log(f'  share of the bigram gain captured by {nm}: {(u["unigram"] - u[nm]) / (u["unigram"] - u["sign bigram"]):.1%}')
log(f'  share captured by the decoy frame (mean): {(u["unigram"] - dd.real.mean()) / (u["unigram"] - u["sign bigram"]):.1%}')

# by object kind (real lines only)
kr = []
for kd in ['seal', 'tag', 'mtab', 'ctab', 'pot']:
    L = [x for x, k in NEW if k == kd]
    if len(L) < 5: continue
    row = dict(kind=kd, lines=len(L), signs=sum(map(len, L)))
    for nm in ['unigram', 'sign bigram', 'class grammar: hand jobs', 'class grammar: hmm10', 'mix: bigram + hand jobs']: row[nm] = score(MS[nm], L)
    row['decoy mean'] = np.mean([score(m, L) for m, _ in DEC.values()])
    kr.append(row)
pd.DataFrame(kr).to_csv(f'{OUT}/bits_by_kind.csv', index=False)
log('  by kind: ' + ' | '.join(f'{r["kind"]} n={r["lines"]}: uni {r["unigram"]:.2f} big {r["sign bigram"]:.2f} hand {r["class grammar: hand jobs"]:.2f} hmm {r["class grammar: hmm10"]:.2f} decoy {r["decoy mean"]:.2f}' for r in kr))

# ================================================================ STEP 3
log('STEP 3: building the gap-test items from the crosswalk pairs ...')
mah2lipi = dict(zip(M.reading_mah, M.tok))
items = {'main': [], 'one_mismatch': []}
for g, lt, mt in zip(pairs.group, pairs.lipi_text, pairs.mahadevan_text):
    L = tuple(lt.split('-')); Mt = mah2lipi.get(mt)
    if Mt is None or len(L) != len(Mt): continue
    for side, gapped, full in (('Lipi lost, second catalogue complete', L, Mt), ('second catalogue lost, Lipi complete', Mt, L)):
        lost = [i for i, s in enumerate(gapped) if s == '000']
        if len(lost) != 1 or set(full) & UNK or any(s.startswith('X') for s in full): continue
        p = lost[0]
        mism = sum(1 for i in range(len(L)) if i != p and gapped[i] != full[i])
        it = dict(side=side, lipi_text=lt, mah_text=mt, context=gapped, pos=p, true=full[p], answer='-'.join(full))
        if mism == 0: items['main'].append(it)
        if mism <= 1: items['one_mismatch'].append(it)
for k, v in items.items():
    # identical items (same context and answer) counted once
    seen = set(); u_ = []
    for it in v:
        key = (it['context'], it['true'])
        if key not in seen: seen.add(key); u_.append(it)
    items[k] = u_
    log(f'  gap items {k}: {len(u_)} distinct (' + ', '.join(f'{s}: {n}' for s, n in collections.Counter(i["side"] for i in u_).items()) + ')')
excl_text = {it['lipi_text'] for v in items.values() for it in v} | {it['answer'] for v in items.values() for it in v}
excl_ids = {i for i, x in zip(d.id, d.tok) if '-'.join(x) in excl_text}
Tg = train_texts(frozenset(excl_ids))
log(f'  gap-test training leaves out {len(excl_ids)} Lipi faces; {len(Tg)} distinct texts remain')
gv, gidx, gC, GMS, GDEC, gband, _ = build_models(Tg)
# gap-test HMM: refit K=10 on the reduced training (same recipe, 10 starts)
Og, mg = pad([x for x, c, k in Tg], gidx); cg = np.array([c for x, c, k in Tg])
bestg = None
for r_ in range(10):
    h_ = HMM(10, len(gv), 31000 + r_); ll_ = h_.fit(Og, mg, cg, iters=300)
    if bestg is None or ll_ > bestg[0]: bestg = (ll_, h_)
hmmg = bestg[1]
log('  gap-test HMM refitted')
freq_order = list(np.argsort(-gC['uni']))
GJ = {'class grammar: hand jobs': MAPS['hand jobs'], 'class grammar: hmm10': MAPS['hmm10'], 'class grammar: kmeans10': MAPS['kmeans10'], 'class grammar: exchange10': MAPS['exchange10']}


def hmm_gap(h, ids, pos):
    """posterior over signs at the lost position under the soft HMM: P(state | rest) x emission."""
    x = [gv[i] if i is not None else '000' for i in ids]
    O1, m1 = pad([x], gidx)
    gam = h.forward_backward(O1, m1, np.array([True]))[5][0][pos]
    p = gam @ h.B; return p / p.sum()


def run_gap(its, models, decs):
    res = collections.defaultdict(lambda: np.zeros(4)); jobres = collections.defaultdict(lambda: np.zeros(3)); n = 0
    for it in its:
        ids = [gidx.get(s) if s != '000' else None for s in it['context']]
        # context signs unseen in training act as unknown context, the lost position is it['pos']
        lost_pos = it['pos']
        tr = gidx.get(it['true']); n += 1
        posts = {nm: gap_posteriors(m, ids, True)[lost_pos] for nm, m in models.items()}
        posts['hidden-state model K=10 (soft)'] = hmm_gap(hmmg, ids, lost_pos)
        for q, (m, dm) in decs.items(): posts[f'decoy {q}'] = gap_posteriors(m, ids, True)[lost_pos]
        posts['frequency only'] = gC['uni'] / gC['uni'].sum()
        for nm, p in posts.items():
            if tr is None: res[nm] += [0, 0, 0, 1]; continue
            rank = int((p > p[tr]).sum())
            res[nm] += [rank < 1, rank < 5, rank < 10, 1]
        # job class accuracy
        for nm, mp in list(GJ.items()) + [(f'decoy {q}', dm) for q, (m, dm) in decs.items()]:
            if tr is None or it['true'] not in mp: jobres[nm] += [0, 0, 1]; continue
            labs = sorted(set(mp.get(s, 'UNSEEN') for s in gv))
            agg = collections.defaultdict(float)
            for i, s in enumerate(gv): agg[mp.get(s, 'UNSEEN')] += posts[nm][i]
            pred = max(agg, key=agg.get)
            cu_ = collections.Counter()
            for i, s in enumerate(gv): cu_[mp.get(s, 'UNSEEN')] += gC['uni'][i]
            base = cu_.most_common(1)[0][0]
            jobres[nm] += [pred == mp[it['true']], base == mp[it['true']], 1]
        # the sign bigram's posterior read as a hand job (does the full model also know the job?)
        if tr is not None and it['true'] in MAPS['hand jobs']:
            agg = collections.defaultdict(float)
            for i, s in enumerate(gv): agg[MAPS['hand jobs'].get(s, 'UNSEEN')] += posts['sign bigram'][i]
            jobres['sign bigram read as hand job'] += [max(agg, key=agg.get) == MAPS['hand jobs'][it['true']], 0, 1]
    return res, jobres


gap_rows = []; job_rows = []
models_g = {k: v for k, v in GMS.items() if not k.endswith(('hmm6', 'hmm8', 'hmm12'))}
for setname, its in items.items():
    res, jobres = run_gap(its, models_g, GDEC)
    for nm, (a1, a5, a10, n) in res.items():
        if nm.startswith('decoy'): continue
        gap_rows.append(dict(set=setname, model=nm, items=int(n), top1=a1 / n, top5=a5 / n, top10=a10 / n))
    dk = np.array([res[f'decoy {q}'] for q in GDEC]) / max(len(its), 1)
    gap_rows.append(dict(set=setname, model=f'DECOY class grammar, mean of {NDECOY}', items=len(its), top1=dk[:, 0].mean(), top5=dk[:, 1].mean(), top10=dk[:, 2].mean()))
    gap_rows.append(dict(set=setname, model=f'DECOY class grammar, best of {NDECOY} (by top-5)', items=len(its), top1=dk[dk[:, 1].argmax(), 0], top5=dk[:, 1].max(), top10=dk[dk[:, 1].argmax(), 2]))
    for nm, (ok, base, n) in jobres.items():
        if nm.startswith('decoy'): continue
        job_rows.append(dict(set=setname, map=nm, items=int(n), job_accuracy=ok / n, most_common_class_baseline=base / n if 'bigram' not in nm else np.nan))
    dj = np.array([jobres[f'decoy {q}'] for q in GDEC])
    job_rows.append(dict(set=setname, map=f'DECOY mean of {NDECOY}', items=int(dj[0, 2]), job_accuracy=(dj[:, 0] / dj[:, 2]).mean(), most_common_class_baseline=(dj[:, 1] / dj[:, 2]).mean()))
    log(f'  [{setname}] ' + ' | '.join(f'{r["model"]}: {r["top1"]:.0%}/{r["top5"]:.0%}/{r["top10"]:.0%}' for r in gap_rows if r['set'] == setname))
    log(f'  [{setname}] job accuracy: ' + ' | '.join(f'{r["map"]}: {r["job_accuracy"]:.0%} (base {r["most_common_class_baseline"]:.0%})' for r in job_rows if r['set'] == setname))
G = pd.DataFrame(gap_rows); G.to_csv(f'{OUT}/gap_test.csv', index=False)
pd.DataFrame(job_rows).to_csv(f'{OUT}/gap_job_test.csv', index=False)
dec_gap = []
for q in GDEC:
    pass

# ================================================================ restorations
main = G[(G.set == 'main') & ~G.model.str.startswith(('DECOY', 'frequency'))]
best_name = main.sort_values(['top5', 'top1'], ascending=False).iloc[0].model
log(f'restorations: model with the best top-5 on the main gap set = {best_name}')
best = MS.get(best_name)
rows = []; nfaces = 0; covered = set()
handm = MS['class grammar: hand jobs']; hmmc = MS['class grammar: hmm10']
for fid, x, f in zip(d.id, d.tok, d.flg):
    damaged = '000' in x or 'ALT' in x or bool(f & {'broken', 'lost', 'alt'})
    if not damaged: continue
    nfaces += 1
    ids = [idx.get(s) if s not in UNK else None for s in x]
    if all(i is not None for i in ids): continue
    edges = 'broken' not in f
    if best is not None: pb = gap_posteriors(best, ids, edges)
    else:
        pb = {}
        for t in [i for i, v in enumerate(ids) if v is None]:
            xx = [vocab[i] if i is not None else '000' for i in ids]; O1, m1 = pad([xx], idx)
            gam = hmm.forward_backward(O1, m1, np.array([edges]))[5][0][t]; p = gam @ hmm.B; pb[t] = p / p.sum()
    ph = gap_posteriors(handm, ids, edges); pm = gap_posteriors(hmmc, ids, edges)
    for t in sorted(pb):
        covered.add(fid)
        aj = collections.defaultdict(float)
        for i, s in enumerate(vocab): aj[MAPS['hand jobs'].get(s, 'UNSEEN')] += ph[t][i]
        jb = max(aj, key=aj.get)
        am = collections.defaultdict(float)
        for i, s in enumerate(vocab): am[MAPS['hmm10'][s]] += pm[t][i]
        mb = max(am, key=am.get)
        top = np.argsort(-pb[t])[:5]
        rows.append(dict(face=fid, reading_order_text='-'.join(x), position=t + 1, stored=x[t], edges_counted=edges,
                         predicted_job=JOB_PLAIN.get(jb, jb), job_prob=round(aj[jb], 3), machine_class=mb, machine_class_prob=round(am[mb], 3),
                         **{f'cand{r + 1}': vocab[top[r]] for r in range(5)}, **{f'p{r + 1}': round(float(pb[t][top[r]]), 3) for r in range(5)},
                         model=best_name))
R = pd.DataFrame(rows); R.to_csv(f'{OUT}/restorations.csv', index=False)
log(f'restorations: {len(R)} lost / unclear signs on {len(covered)} faces (of {nfaces} damaged faces; the rest are broken at an edge with no lost sign inside)')
log('  predicted jobs: ' + ', '.join(f'{k} {v}' for k, v in R.predicted_job.value_counts().items()))
log(f'  share with top candidate at p >= 0.5: {(R.p1 >= 0.5).mean():.1%}')
