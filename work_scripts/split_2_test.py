#!/usr/bin/env python3
"""Split step 2: refit the frame with a sign split into its uses and score on held-out texts, against the unsplit frame and
40 decoys. Usage: split_2_test.py <sign>. Rules fixed before any number (see split_common.py for the scoring):
SPLIT DEFINITIONS per sign: mix2 (two-profile mixture on left class, right class, kind, length; fitted on the training part only),
  mix3 (three profiles), pos (text start vs elsewhere), kind (seal vs every other object kind).
HELD-OUT SET 1: first catalogue, 5 folds of distinct texts, 2 different random partitions = 10 fold fits; the clustering is
  refit inside each training part. Held-out texts with a sign not in the training part are dropped for every model alike.
HELD-OUT SET 2: the 482 new texts (second catalogue, no first-catalogue partner), models fitted on the whole first catalogue.
FRAMES: U0 = unsplit v2 frame; U1 = unsplit, sign as its own class; real split; DECOYS A (20) = the real labels permuted
  among occurrences within the same site and object kind (sizes and kind/site mix kept); DECOYS B (20) = permuted over all
  occurrences (same sizes). Both schemes S1 (variants one-sign classes; compared with U1) and S2 (variants join best v2 class;
  compared with U0). Pooled class grammar (headline) for everything; by-kind grammar for real/U0/U1 only.
Output: work_data/split/test_<sign>.csv, log_split_2_<sign>.txt"""
from split_common import *
import time
SIGN = sys.argv[1]
TAG = '_' + sys.argv[2] if len(sys.argv) > 2 else ''
NDEC = 20
T4 = train_with_sites(); T3 = [(x, c, k) for x, c, k, st in T4]; SITE = [st for x, c, k, st in T4]
vocab_all, idx_all = vocab_of(T3)
NEW, _, _ = new_texts(idx_all)
log_f = open(f'{SPL}/log_split_2_{SIGN}{TAG}.txt', 'w'); t0 = time.time()
def say(*a):
    s = f'[{time.time()-t0:6.0f}s] ' + ' '.join(str(x) for x in a); print(s, flush=True); log_f.write(s + '\n'); log_f.flush()

DEFS = ['mix2', 'mix3', 'pos', 'kind'] if SIGN != '824' else ['mix2', 'pos', 'kind']
if len(sys.argv) > 2: DEFS = [sys.argv[2]]   # redesign run: 'left' = counting context on the left

def labels_for(defn, tr_texts, occ, rng):
    n = len(occ)
    if defn == 'pos': return np.array([0 if i == 0 else 1 for ti, i in occ]), 2
    if defn == 'left':
        CNT_ = {'NUM_SHORT', 'NUM_TALL', 'NUM_NAME', 'THING', 'MEASURE', 'AFTER_M'}
        return np.array([1 if (i > 0 and base_of(tr_texts[ti][0][i - 1]) in CNT_) else 0 for ti, i in occ]), 2
    if defn == 'kind': return np.array([0 if tr_texts[ti][2] == 'seal' else 1 for ti, i in occ]), 2
    K = 2 if defn == 'mix2' else 3
    X = np.array([ENC.enc(feat(tr_texts[ti][0], i, tr_texts[ti][1], tr_texts[ti][2])) for ti, i in occ])
    m = Mix(K, ENC.dims).fit(X, rng)
    return m.assign(X), K

def decoys(lab, occ, sites, texts, seed, stratified):
    r = np.random.default_rng(seed); out = lab.copy()
    if stratified:
        strata = collections.defaultdict(list)
        for j, (ti, i) in enumerate(occ): strata[(sites[ti], texts[ti][2])].append(j)
        for js in strata.values(): out[js] = lab[r.permutation(js)]
    else: out = lab[r.permutation(len(lab))]
    return out

def run_variant(tr, tr_sites, lab, K, scheme, pooled, lines):
    """fit with labels lab on training texts tr; score lines (label-free). returns (lp array, n array)."""
    occ = occurrences(tr, SIGN)
    texts_exp = expand(tr, SIGN, occ, lab, K)
    variants = [f'{SIGN}@{g}' for g in range(K) if (lab == g).any()]
    present = [g for g in range(K) if (lab == g).any()]
    vcl = best_classes(tr, occ, lab, K, SIGN) if scheme == 'S2' else None
    vcl = [vcl[g] for g in present] if vcl else None
    m, vocab, idx = build(texts_exp, None, variants, vcl, scheme, pooled)
    return score_lattice(m, idx, lines, SIGN, variants)

def plain(tr, pooled, singleton, lines):
    m, vocab, idx = fit_plain(tr, pooled, singleton)
    return score_lattice(m, idx, lines, SIGN, [])

def evaluate(tr, tr_sites, lines, defn, seedbase, tag):
    """returns dict name -> (lp, n) for U0, U1, real(S1,S2), decoys; lines already filtered to the training vocabulary."""
    res = {}
    rng = np.random.default_rng(seedbase)
    occ = occurrences(tr, SIGN)
    lab, K = labels_for(defn, tr, occ, rng)
    res['U0'] = plain(tr, True, None, lines); res['U1'] = plain(tr, True, SIGN, lines)
    res['U0k'] = plain(tr, False, None, lines); res['U1k'] = plain(tr, False, SIGN, lines)
    res['sizes'] = np.bincount(lab, minlength=K)
    for sch in ('S1', 'S2'):
        res[f'real_{sch}'] = run_variant(tr, tr_sites, lab, K, sch, True, lines)
        res[f'realk_{sch}'] = run_variant(tr, tr_sites, lab, K, sch, False, lines)
        for st, nm in ((True, 'A'), (False, 'B')):
            for j in range(NDEC):
                dl = decoys(lab, occ, tr_sites, tr, 1000 * (1 if st else 2) + j + 17 * seedbase, st)
                res[f'dec{nm}{j}_{sch}'] = run_variant(tr, tr_sites, dl, K, sch, True, lines)
    return res

rows = []
for defn in DEFS:
    acc = collections.defaultdict(lambda: [0.0, 0, 0.0, 0, 0])   # name -> lp_all, n_all, lp_s, n_s, n_occ_s
    nf = 0; wins = collections.Counter(); tot = collections.Counter()
    for rep in range(2):
        r = np.random.default_rng(100 + rep); fold = r.integers(0, 5, size=len(T3))
        for f in range(5):
            tr = [t for t, g in zip(T3, fold) if g != f]; trs = [st for st, g in zip(SITE, fold) if g != f]
            va = [t for t, g in zip(T3, fold) if g == f]
            v, ix = vocab_of(tr)
            lines = [(x, k) for x, c, k in va if all(a in ix for a in x if a not in UNK) and not (set(x) & UNK)]
            res = evaluate(tr, trs, lines, defn, 7 * rep + f, 'cv')
            has = np.array([SIGN in x for x, k in lines]); nocc = np.array([x.count(SIGN) for x, k in lines])
            nf += 1
            for name, val in res.items():
                if name == 'sizes': continue
                lp, n = val
                a = acc[name]; a[0] += lp.sum(); a[1] += n.sum(); a[2] += lp[has].sum(); a[3] += n[has].sum(); a[4] += nocc.sum()
            for sch, base in (('S1', 'U1'), ('S2', 'U0')):
                tot[sch] += 1; wins[sch] += res[f'real_{sch}'][0].sum() > res[base][0].sum()
            say(f'{defn} rep {rep} fold {f}: sizes {res["sizes"]}; held-out texts {len(lines)} ({int(has.sum())} with {SIGN}); real S2 {-res["real_S2"][0].sum()/res["real_S2"][1].sum():.4f} U0 {-res["U0"][0].sum()/res["U0"][1].sum():.4f} bits/sign')
    for name, a in acc.items():
        rows.append(dict(sign=SIGN, split=defn, heldout='first catalogue 10 fold fits', name=name, bits_all=-a[0] / a[1], n_all=a[1], bits_with_sign=-a[2] / max(a[3], 1), n_with_sign=a[3], occ_with_sign=a[4], folds_real_beats_base_S1=wins['S1'], folds_real_beats_base_S2=wins['S2'], folds=tot['S2']))
    # new texts
    tr, trs = T3, SITE
    lines = NEW
    res = evaluate(tr, trs, lines, defn, 999, 'new')
    has = np.array([SIGN in x for x, k in lines]); nocc = np.array([x.count(SIGN) for x, k in lines])
    for name, val in res.items():
        if name == 'sizes': continue
        lp, n = val
        rows.append(dict(sign=SIGN, split=defn, heldout='new texts', name=name, bits_all=-lp.sum() / n.sum(), n_all=n.sum(), bits_with_sign=(-lp[has].sum() / n[has].sum()) if has.any() else np.nan, n_with_sign=n[has].sum(), occ_with_sign=nocc.sum(), sizes=str(res['sizes'].tolist())))
    say(f'{defn}: new-text real S2 {rows[-1]["bits_all"]:.4f}; done')
    pd.DataFrame(rows).to_csv(f'{SPL}/test_{SIGN}{TAG}.csv', index=False)
say('finished')
