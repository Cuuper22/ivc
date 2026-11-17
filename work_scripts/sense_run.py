#!/usr/bin/env python3
"""sense_run.py -- runs the whole sense test and writes work_data/sense/results.json (+ csv tables).
Steps: (1) load signs, senses, embeddings, objects; (2) real scores; (3) N_SHUF shuffles of each kind (A: same class and band; B: also same
number of senses); (4) per-sign real-vs-shuffle; (5) mass run: every candidate word allowed for the sign's job class, real vs scrambled corpus;
(6) the control (English sentences with WordNet senses), same code.
Usage: /tmp/senv/bin/python sense_run.py [N_SHUF]   (background job; progress lines print as it goes)"""
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from sense_core import *
ROOT = '/home/claude/ivc'; D = f'{ROOT}/work_data/sense'
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
VERS = ['ov', 'lift', 'cos']
def log(*a): print(time.strftime('%H:%M:%S'), '[sense_run]', *a, flush=True)
T0 = time.time()
# ------------------------------------------------------------------ Indus problem
S = pd.read_csv(f'{D}/signs.csv', dtype={'sign': str}).fillna(''); SS = pd.read_csv(f'{D}/senses.csv').fillna('')
EM = np.load(f'{D}/senses_emb.npy').astype(np.float32)
words = sorted(S.word.unique()); senses = {}; emb = {}
for w, g in SS.groupby('word', sort=False):
    senses[w] = [(r.phrase, [c for c in r.cats.split('|') if c]) for r in g.itertuples()]
    emb[w] = EM[g.index.values]
sidx = {s: i for i, s in enumerate(S.sign)}
rng0 = np.random.default_rng(20261117)
def make_texts(evfile, fold_mode):
    ev = json.load(open(f'{D}/{evfile}')); agg = collections.defaultdict(float); n_ev = 0; n_txt = 0
    for e in ev:
        fold = int(rng0.integers(0, 2)) if fold_mode == 'cross' else 2
        faces = []
        for f in e['faces']:
            us = list(dict.fromkeys(sidx[x] for x in f if x in sidx))
            if len(us) >= 2 and len({S.word.iloc[u] for u in us}) >= 2: faces.append(us)
        if not faces: continue
        n_ev += 1
        for us in faces: agg[(fold, tuple(sorted(us)))] += 1 / len(faces); n_txt += 1
    log(evfile, 'events with a scorable text', n_ev, 'face-texts', n_txt, 'distinct texts', len(agg))
    return agg
A1 = make_texts('events_lipi.json', 'cross'); A2 = make_texts('events_new.json', 'new')
keys = list(A1) + list(A2)
texts = [list(k[1]) for k in keys]; tw = [(A1.get(k) or A2.get(k)) for k in keys]; tf = [k[0] for k in keys]
P = Prob(words, senses, emb, list(S.sign), list(S.word), list(S.cls), list(S.band), texts, tw, tf, lmax=10, name='indus')
log('Indus problem: words', len(P.words), 'max senses', P.S, 'texts', len(texts), 'texts truncated at 10 signs', P.trunc)
grp_new = (P.tfold == 2).astype(float); grp_lip = (P.tfold < 2).astype(float)
log('weights: new texts', grp_new @ P.tw, 'Lipi', grp_lip @ P.tw)
P.build(VERS); log('similarity tables built', f'{time.time() - T0:.0f}s')
# strongest 30: status strict, DEDR number given, not a number sign class, ranked by Lipi faces
cand = S[(S.status == 'strict') & (S.dedr != '') & (~S.cls.str.startswith('NUM'))].sort_values('faces', ascending=False)
strong = list(cand.head(30).sign); log('strongest-labelled pool', len(cand), 'taken', len(strong))
sub30 = np.isin(P.units, strong)
def run_set(P, groups, sub, asg, vers=VERS):
    out = {}; um = {}
    for v in vers:
        fit, ok = P.fits(asg, v)
        for gname, g in groups.items():
            r = P.total(fit, ok, g, sub)
            out[(v, gname, 'all')] = r['all']
            if sub is not None: out[(v, gname, 'sub')] = r['sub']
        um[v] = P.unit_means(fit, ok, groups['all'] if 'all' in groups else list(groups.values())[0])
    return out, um
groups = {'new': grp_new, 'lipi': grp_lip, 'all': np.ones(len(P.tw))}
real, real_um = run_set(P, groups, sub30, P.real)
for k, v in real.items(): log('REAL', k, round(float(v), 5))
# ------------------------------------------------------------------ shuffles
def shuffles(P, groups, sub, matched, n, seed, tag):
    rng = np.random.default_rng(seed); rec = collections.defaultdict(list); umr = {v: [] for v in VERS}; t = time.time(); ds = []
    for i in range(n):
        a = P.shuffle(rng, matched=matched); ds.append(np.abs(P.nsens[a] - P.nsens[P.real]).mean())
        o, um = run_set(P, groups, sub, a)
        for k, v in o.items(): rec[k].append(float(v))
        for v in VERS: umr[v].append(um[v][0])
        if (i + 1) % 50 == 0: log(f'{tag}: {i + 1}/{n} shuffles ({time.time() - t:.0f}s)')
    return rec, umr, float(np.mean(ds))
SH = {}
for matched, tag in ((False, 'A'), (True, 'B')):
    rec, umr, dsens = shuffles(P, groups, sub30, matched, N, 777 + matched, tag)
    SH[tag] = dict(rec={'|'.join(k): v for k, v in rec.items()}, dsens=dsens)
    np.save(f'{D}/unit_means_shuf_{tag}.npy', np.stack([np.stack(umr[v]) for v in VERS]).astype(np.float32))
    SH[tag]['mean_abs_sense_change'] = dsens
    log(tag, 'mean |change in sense count| per sign vs real:', dsens)
np.save(f'{D}/unit_means_real.npy', np.stack([real_um[v][0] for v in VERS]).astype(np.float32))
np.save(f'{D}/unit_counts_real.npy', real_um['ov'][1].astype(np.float32))
res = dict(N=N, real={'|'.join(k): float(v) for k, v in real.items()}, shuf=SH, strong=strong, n_units=len(P.units),
           weights=dict(new=float(grp_new @ P.tw), lipi=float(grp_lip @ P.tw)), n_texts=len(texts))
json.dump(res, open(f'{D}/results_core.json', 'w'))
log('core results saved', f'{time.time() - T0:.0f}s')
# ------------------------------------------------------------------ mass run
def mass(P, ver, X, tw, pool_mode, rng_unused=None):
    """for every sign u with >=3 texts in X: score of each candidate word c in u's pool with the neighbours' real words kept.
    returns per-sign dict(real_rank_pct, top1, top10, C, ...)"""
    M2 = P.M2[ver][2]; out = {}
    pools = {}
    for u in range(len(P.units)):
        if pool_mode == 'class': pools[u] = sorted({P.real[v] for v in P.cell_cls[P.cls[u]]})
        elif pool_mode == 'all': pools[u] = list(range(len(P.words)))
    for u in range(len(P.units)):
        rows = np.where((X == u).any(1))[0]
        if len(rows) < 3: continue
        cands = np.array(pools[u]); wr = P.real[u]
        if wr not in cands: cands = np.append(cands, wr)
        sc = np.zeros(len(cands)); den = np.zeros(len(cands))
        for t in rows:
            nb = np.array([P.real[x] for x in X[t] if x >= 0 and x != u]); 
            if len(nb) == 0: continue
            G = M2[cands[:, None], nb[None, :], :]                    # [C, n, S]
            m = (nb[None, :] != cands[:, None])                        # [C, n]
            cnt = m.sum(1); avg = (G * m[..., None]).sum(1) / np.maximum(cnt, 1)[:, None]
            avg = np.where(P.valid[cands], avg, -1e9); best = avg.max(1)
            ok = cnt > 0; sc += np.where(ok, best, 0) * tw[t]; den += ok * tw[t]
        sc = np.where(den > 0, sc / np.maximum(den, 1e-9), -1e9)
        i_real = int(np.where(cands == wr)[0][0]); r = sc[i_real]
        if r < -1e8: continue
        def stats(mask):
            c = sc[mask]; n = len(c); below = (c < r - 1e-9).sum(); ties = (np.abs(c - r) <= 1e-9).sum() - 1
            pct = (below + 0.5 * ties) / max(n - 1, 1)            # 0 = worst, 1 = best, 0.5 = chance
            g = int((c > r + 1e-9).sum()); rank = 1 + g + ties / 2               # mid-rank: ties share the places
            top10 = max(1, int(np.ceil(0.1 * n)))
            p1 = min(max((1 - g) / (ties + 1), 0), 1); p10 = min(max((top10 - g) / (ties + 1), 0), 1)   # chance of being first / in top 10% when ties are broken at random
            return dict(pct=float(pct), rank=float(rank), n=int(n), top1=float(p1), top10=float(p10),
                        chance_top1=1 / n, chance_top10=top10 / n)
        full = np.ones(len(cands), bool)
        nsr = P.nsens[wr]; near = (np.abs(P.nsens[cands] - nsr) <= 3) | ((P.nsens[cands] >= 20) & (nsr >= 20))
        out[u] = dict(all=stats(full), matched=stats(near))
    return out
P.cell_cls = collections.defaultdict(list)
for u in range(len(P.units)): P.cell_cls[P.cls[u]].append(u)
newrows = np.where(P.tfold == 2)[0]
Xn = P.X[newrows].copy(); twn = np.zeros(len(P.tw)); twn[:] = P.tw
def scramble(rng):
    """destroy which signs sit together: pool every sign occurrence of the new texts and deal them out again (same text lengths, same sign totals)"""
    toks = Xn[Xn >= 0]; rng.shuffle(toks); Y = -np.ones_like(Xn); k = 0
    for t in range(len(Xn)):
        n = int((Xn[t] >= 0).sum()); seg = list(dict.fromkeys(toks[k:k + n])); k += n
        Y[t, :len(seg)] = seg
    return Y
def summarize(o, ptag):
    r = {}
    for key in ('all', 'matched'):
        v = [x[key] for x in o.values()]
        if not v: continue
        r[key] = dict(n_signs=len(v), mean_pct=float(np.mean([x['pct'] for x in v])), top1=float(np.mean([x['top1'] for x in v])),
                      chance_top1=float(np.mean([x['chance_top1'] for x in v])), top10=float(np.mean([x['top10'] for x in v])),
                      chance_top10=float(np.mean([x['chance_top10'] for x in v])), mean_rank=float(np.mean([x['rank'] for x in v])),
                      mean_pool=float(np.mean([x['n'] for x in v])))
    return r
MASS = {}
rngm = np.random.default_rng(555)
# mass() reads texts through X/tw of the new rows only
def mass_run(ver, pm, X, tw):
    return mass(P, ver, X, tw, pm)
for ver in VERS:
    for pm in ('class', 'all'):
        t = time.time()
        o = mass_run(ver, pm, Xn, P.tw[newrows])
        real_s = summarize(o, 'real')
        scr = []
        for k in range(10):
            Y = scramble(rngm); oo = mass_run(ver, pm, Y, P.tw[newrows]); scr.append(summarize(oo, 'scr'))
        MASS[f'{ver}|{pm}'] = dict(real=real_s, scrambled={key: {m: float(np.mean([s[key][m] for s in scr if key in s])) for m in scr[0][key]} for key in scr[0]},
                                   per_sign={P.units[u]: o[u]['all'] for u in o})
        log('MASS', ver, pm, 'real', {k: round(v, 3) for k, v in real_s['all'].items()}, f'{time.time() - t:.0f}s')
json.dump(MASS, open(f'{D}/results_mass.json', 'w'))
log('mass run saved', f'{time.time() - T0:.0f}s')
