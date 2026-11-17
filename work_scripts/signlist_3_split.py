#!/usr/bin/env python3
"""Sign list step 3: SPLITS. Does a catalogue sign behave as two? Rule fixed before any number:

OCCURRENCE FEATURES (first catalogue, copy events): left neighbour's frame-v2 class ('^' text start, '?' lost sign or broken
  edge), right neighbour's class ('$' text end, '?'), object kind (seal, tablet, copper tablet, tag/sealing, pot, other).
MODELS: one profile = the three features independent; two profiles = a 2-component mixture of such profiles (EM, 4 starts,
  60 iterations, add-0.5 smoothing).
STATISTIC G: held-out gain in log-likelihood per occurrence (bits) of two profiles over one: fit on a random half, score the
  other half, both ways, 6 random halvings, mean.
CONTROLS per sign s (top 100 signs by uses, n = uses of s):
  ONE-PROFILE resamples (the "random halves of one sign" side: one sign with one profile, which should not split):
     12 pseudo-signs of n occurrences drawn from s's own one-profile fit.
  POOLED pairs (should split): 12 pseudo-signs made of n/2 occurrences of each of two random other top-150 signs.
RULE: s behaves as two when G_s >= 95th percentile of its one-profile resamples AND G_s >= the median of its pooled pairs.
Each flagged sign is then described: the two profiles (top left / right / kind of each), and whether the second catalogue
  splits it (one Lipi sign read as two Mahadevan numbers at share >= 0.25 each, crosswalk).
REDESIGN (run with argument 'clean', written after the first run): the first run let '?' (broken edge or lost neighbour)
  be a context, so damaged faces on tablets and pots formed a profile of their own (many flagged profiles read L:? R:?).
  The clean run drops every occurrence that touches a broken edge or a lost sign; everything else is unchanged.
Output: work_data/signlist/splits.csv (splits_clean.csv for the redesign), log_split.txt (log_split_clean.txt)
"""
from signlist_common import *

CLEAN = len(sys.argv) > 1 and sys.argv[1] == 'clean'
say = logger('split_clean' if CLEAN else 'split')
L = load_lipi(); U = uses(L); CL = v2classes()
KIND = {'seals': 'seal', 'tablets': 'tablet', 'copper tablets': 'copper', 'tags and sealings': 'tag', 'pots': 'pot'}
occ = collections.defaultdict(list)
for e in L:
    k = KIND.get(e['kind'], 'other')
    for f, br in zip(e['faces'], e['broken']):
        for i, s in enumerate(f):
            if not is_sign(s): continue
            if i == 0: l = '?' if br else '^'
            else: l = CL.get(f[i - 1], 'PERSONAL') if is_sign(f[i - 1]) else '?'
            if i == len(f) - 1: r = '?' if br else '$'
            else: r = CL.get(f[i + 1], 'PERSONAL') if is_sign(f[i + 1]) else '?'
            if CLEAN and '?' in (l, r): continue
            occ[s].append((l, r, k))
VL = sorted({o[0] for v in occ.values() for o in v}); VR = sorted({o[1] for v in occ.values() for o in v}); VK = sorted({o[2] for v in occ.values() for o in v})
DIMS = [len(VL), len(VR), len(VK)]
IL = {x: i for i, x in enumerate(VL)}; IR = {x: i for i, x in enumerate(VR)}; IK = {x: i for i, x in enumerate(VK)}
def enc(lst): return np.array([(IL[a], IR[b], IK[c]) for a, b, c in lst], dtype=int)
ARR = {s: enc(v) for s, v in occ.items()}

def fit(X, K, rng, starts=4, iters=60):
    n = len(X); best = None
    for _ in range(starts if K > 1 else 1):
        R = rng.dirichlet(np.ones(K), n) if K > 1 else np.ones((n, 1))
        for _ in range(iters if K > 1 else 1):
            pi = R.sum(0) + 1e-9; pi = pi / pi.sum()
            th = []
            for j, D in enumerate(DIMS):
                M = np.full((K, D), 0.5)
                for k in range(K): np.add.at(M[k], X[:, j], R[:, k])
                th.append(M / M.sum(1, keepdims=True))
            if K == 1: break
            lp = np.log(pi)[None, :] + sum(np.log(th[j][:, X[:, j]].T) for j in range(3))
            m = lp.max(1, keepdims=True); R = np.exp(lp - m); R /= R.sum(1, keepdims=True)
        ll = loglik(X, pi, th)
        if best is None or ll > best[0]: best = (ll, pi, th)
    return best[1], best[2]

def loglik(X, pi, th):
    lp = np.log(pi)[None, :] + sum(np.log(th[j][:, X[:, j]].T) for j in range(3))
    m = lp.max(1, keepdims=True)
    return float((m[:, 0] + np.log(np.exp(lp - m).sum(1))).sum())

def G(X, rng, halvings=6):
    gains = []
    for _ in range(halvings):
        idx = rng.permutation(len(X)); A, B = X[idx[:len(X) // 2]], X[idx[len(X) // 2:]]
        for tr, te in ((A, B), (B, A)):
            p1, t1 = fit(tr, 1, rng); p2, t2 = fit(tr, 2, rng)
            gains.append((loglik(te, p2, t2) - loglik(te, p1, t1)) / len(te) / np.log(2))
    return float(np.mean(gains))

def one_profile_sample(X, n, rng):
    p1, t1 = fit(X, 1, rng)
    return np.stack([rng.choice(DIMS[j], n, p=t1[j][0]) for j in range(3)], 1)

top = [s for s, _ in sorted(U.items(), key=lambda kv: -kv[1]) if is_sign(s) and len(occ[s]) >= 10]
TOP100, TOP150 = top[:100], top[:150]
X2 = crosswalk(); X2 = X2[X2.share >= 0.25]
L2M = collections.defaultdict(list)
for l, m, sh in zip(X2.lipi, X2.mahadevan, X2.share): L2M[l].append(f'{m}({sh:.2f})')
rng = np.random.default_rng(31)
rows = []
for i, s in enumerate(TOP100):
    X = ARR[s]; n = len(X)
    g = G(X, rng)
    neg = [G(one_profile_sample(X, n, rng), rng, 3) for _ in range(12)]
    pos = []
    for _ in range(12):
        a, b = rng.choice([t for t in TOP150 if t != s], 2, replace=False)
        h = max(2, n // 2)
        XA = ARR[a][rng.choice(len(ARR[a]), min(h, len(ARR[a])), replace=False)]
        XB = ARR[b][rng.choice(len(ARR[b]), min(h, len(ARR[b])), replace=False)]
        pos.append(G(np.vstack([XA, XB]), rng, 3))
    flag = g >= np.quantile(neg, 0.95) and g >= np.median(pos)
    # describe the two profiles on the whole sign
    p2, t2 = fit(X, 2, rng)
    def desc(k):
        return ' '.join(f'{nm}:' + ','.join(f'{V[i]}' for i in np.argsort(-t2[j][k])[:2]) for j, (nm, V) in enumerate((('L', VL), ('R', VR), ('K', VK))))
    rows.append(dict(sign=s, uses=n, v2=CL.get(s, ''), G=round(g, 4), neg_p95=round(float(np.quantile(neg, 0.95)), 4),
                     pos_median=round(float(np.median(pos)), 4), pos_share_beating_neg=round(float(np.mean([p >= np.quantile(neg, 0.95) for p in pos])), 2),
                     behaves_as_two=flag, weights=f'{p2[0]:.2f}/{p2[1]:.2f}', profile_1=desc(0), profile_2=desc(1),
                     mahadevan_reads_as='|'.join(L2M.get(s, [])), mahadevan_splits=len(L2M.get(s, [])) >= 2))
    say(f'{i + 1}/100 sign {s} (n {n}): G {g:.3f} bits; one-profile 95th {np.quantile(neg, 0.95):.3f}; pooled-pair median {np.median(pos):.3f}; '
        f'{"TWO" if flag else "one"}')
R = pd.DataFrame(rows); R.to_csv(f'{OUT}/splits_clean.csv' if CLEAN else f'{OUT}/splits.csv', index=False)
say(f'signs that behave as two: {int(R.behaves_as_two.sum())} of 100; G above one-profile 95th only: {int((R.G >= R.neg_p95).sum())}')
say(f'positive control: pooled pairs beat the one-profile 95th in {R.pos_share_beating_neg.mean():.2%} of cases (sensitivity)')
say(f'second catalogue splits {int(R.mahadevan_splits.sum())} of the 100; of the flagged: {int(R[R.behaves_as_two].mahadevan_splits.sum())}')
