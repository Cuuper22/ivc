#!/usr/bin/env python3
"""STEP 1. Jobs by machine. Fixed before running (2026-11-17):

  Method A (main): hidden-state sequence model (HMM) on distinct Lipi texts in reading order, K = 6, 8, 10, 12 states,
    10 random starts each, up to 300 Baum-Welch rounds, best log-likelihood kept. Lost / unclear signs are unseen
    tokens (no emission). End of text modelled on clean faces only. A sign's machine class = the state that emits most
    of its uses (posterior counts). K = 10 is the main machine frame (same number of classes as the hand jobs) and
    is the one carried into steps 2 to 5; the other K are reported beside it.
  Method B (cross-check): k-means on sign vectors (signs with 3+ uses), 30 starts, same K. Vector blocks, each scaled
    to equal weight, square-rooted shares: position (first / last / middle / alone, mean relative position);
    left and right neighbour over the 60 commonest signs + start/end + other; object kind (9 kinds);
    short / tall count stroke on the left / right; signs on the OTHER faces of the same object (60 commonest + other).
    Signs with 1-2 uses get the nearest centre.
  Method C (second cross-check): exchange clustering: hard classes that maximise the class-bigram likelihood
    (each sign moved to its best class until nothing moves; 5 starts, best kept), same K.
  Agreement with the hand jobs (frame_common.HAND): adjusted Rand index (ARI: 0 = chance, 1 = identical partitions)
    and normalised mutual information (NMI: 0 = independent, 1 = identical), over signs with 10+ uses in training,
    plus token-weighted versions. Null 1: hand labels shuffled among those signs (1,000 times). Null 2: hand labels
    dealt within frequency bands (1,000 times; the decoy dealing).
  Token level: each token's HMM state (posterior argmax in its own text) against its parser job (gloss2 role).
  Disagreements: signs (10+ uses) whose hand job differs from the hand job that holds most uses in their machine class.
    Which the data backs: the hand-class bigram model's training log-likelihood with the sign in its hand job against
    the sign moved to the machine-implied job (bits per use of the sign; positive = the data backs the machine).
"""
from frame_common import *
from sklearn.metrics import adjusted_rand_score as ARI, normalized_mutual_info_score as NMI
from sklearn.cluster import KMeans

KS = [6, 8, 10, 12]; MAIN_K = 10; MINUSE = 10
T = train_texts(); vocab, idx = vocab_of(T); V = len(vocab)
C = counts(T, idx)
O, mask = pad([x for x, c, k in T], idx); clean = np.array([c for x, c, k in T])
use = C['uni']
log(f'training: {len(T)} distinct texts, {V} signs, {int(use.sum())} sign uses; signs with {MINUSE}+ uses:', int((use >= MINUSE).sum()))

# ---------------- A: HMM
hmm_maps, hmm_models, hmm_ll = {}, {}, {}
for K in KS:
    best = None
    for r in range(10):
        h = HMM(K, V, 1000 * K + r); ll = h.fit(O, mask, clean, iters=300)
        if best is None or ll > best[0]: best = (ll, h)
    ll, h = best; hmm_ll[K] = ll; hmm_models[K] = h
    Cn = h.sign_state_counts(O, mask, clean)
    hmm_maps[K] = {s: f'H{K}_{int(np.argmax(Cn[i]))}' for i, s in enumerate(vocab)}
    log(f'HMM K={K}: best log-likelihood {ll:.1f} (nats) over 10 starts')
np.save(f'{OUT}/hmm10_params.npy', dict(pi=hmm_models[10].pi, A=hmm_models[10].A, B=hmm_models[10].B, vocab=vocab), allow_pickle=True)

# ---------------- B: k-means on sign vectors
log('building sign vectors for k-means ...')
top = [vocab[i] for i in np.argsort(-use)[:60]]; ti = {s: i for i, s in enumerate(top)}
KINDS = ['seal', 'mtab', 'pot', 'tag', 'ctab', 'other', 'bangle', 'rod', 'tool']
SHORT = {f'{i:03d}' for i in range(1, 8)} | {'012'} | {f'{i:03d}' for i in range(13, 19)}
TALL = {f'{i:03d}' for i in range(31, 37)}
F = {b: np.zeros((V, n)) for b, n in [('pos', 5), ('left', 63), ('right', 63), ('kind', 9), ('cnt', 4), ('obj', 61)]}
def nb(s, edge):
    if s is None: return 60 if edge == 'L' else 61
    return ti.get(s, 62)
for x, c, k in T:
    n = len(x)
    for i, s in enumerate(x):
        if s in UNK: continue
        a = idx[s]
        F['pos'][a, 0] += i == 0; F['pos'][a, 1] += i == n - 1; F['pos'][a, 2] += 0 < i < n - 1; F['pos'][a, 3] += n == 1
        F['pos'][a, 4] += (i / (n - 1)) if n > 1 else 0.5
        L = x[i - 1] if i else None; R = x[i + 1] if i + 1 < n else None
        if not (L in UNK): F['left'][a, nb(L, 'L')] += 1
        if not (R in UNK): F['right'][a, nb(R, 'R')] += 1
        F['kind'][a, KINDS.index(k) if k in KINDS else 5] += 1
        F['cnt'][a, 0] += L in SHORT; F['cnt'][a, 1] += L in TALL; F['cnt'][a, 2] += R in SHORT; F['cnt'][a, 3] += R in TALL
# co-occurrence on other faces of the same object (all Lipi faces)
for o, g in d.groupby('obj'):
    if len(g) < 2: continue
    faces = list(g.tok)
    for fi, x in enumerate(faces):
        others = [s for fj, y in enumerate(faces) if fj != fi for s in y if s not in UNK]
        for s in set(x):
            if s in UNK or s not in idx: continue
            for t in others: F['obj'][idx[s], ti.get(t, 60)] += 1
X = []
for b, A in F.items():
    if b == 'pos':
        tot = np.maximum(use, 1)[:, None]; B = A / tot
    elif b == 'cnt':
        B = A / np.maximum(use, 1)[:, None]
    else:
        B = A / np.maximum(A.sum(1, keepdims=True), 1)
    B = np.sqrt(B)
    B = B / max(np.linalg.norm(B, axis=1).mean(), 1e-9)
    X.append(B)
X = np.hstack(X)
km_maps = {}
fit_rows = use >= 3
for K in KS:
    km = KMeans(K, n_init=30, random_state=K).fit(X[fit_rows])
    lab = km.predict(X)
    km_maps[K] = {s: f'K{K}_{lab[i]}' for i, s in enumerate(vocab)}
    log(f'k-means K={K} done')

# ---------------- C: exchange clustering
def class_ll(cid, K):
    Z = np.zeros((V, K)); Z[np.arange(V), cid] = 1
    cb = Z.T @ C['big'] @ Z; cs = C['st'] @ Z; ce = C['en'] @ Z; cu = use @ Z
    M2 = np.zeros((K + 1, K + 1)); M2[:K, :K] = cb; M2[K, :K] = cs; M2[:K, K] = ce
    return obj_from(M2, cu, K)   # class transitions + emissions (in-class counts = cu)

def xlogx(a): a = a[a > 0]; return (a * np.log(a)).sum()
BIG = C['big']; ST = C['st']; EN = C['en']
def obj_from(M2, cu, K):
    return xlogx(M2) - xlogx(M2.sum(1)) + xlogx(use) - xlogx(cu)

def exchange(K, seed, sweeps=12):
    r = np.random.default_rng(seed)
    cid = r.integers(0, K, V)
    Z = np.zeros((V, K)); Z[np.arange(V), cid] = 1
    M2 = np.zeros((K + 1, K + 1)); M2[:K, :K] = Z.T @ BIG @ Z; M2[K, :K] = ST @ Z; M2[:K, K] = EN @ Z; cu = use @ Z
    order = np.argsort(-use); best = obj_from(M2, cu, K)
    for sw in range(sweeps):
        moved = 0
        for a in order:
            if use[a] < 1: continue
            k0 = cid[a]
            row = np.bincount(cid, weights=BIG[a], minlength=K); col = np.bincount(cid, weights=BIG[:, a], minlength=K)
            sl = BIG[a, a]; row[k0] -= sl; col[k0] -= sl
            # remove a
            M2[k0, :K] -= row; M2[:K, k0] -= col; M2[k0, k0] -= sl; M2[K, k0] -= ST[a]; M2[k0, K] -= EN[a]; cu[k0] -= use[a]
            scores = []
            for k in range(K):
                Mt = M2.copy(); Mt[k, :K] += row; Mt[:K, k] += col; Mt[k, k] += sl; Mt[K, k] += ST[a]; Mt[k, K] += EN[a]
                ct = cu.copy(); ct[k] += use[a]; scores.append(obj_from(Mt, ct, K))
            k = int(np.argmax(scores)); cid[a] = k
            M2[k, :K] += row; M2[:K, k] += col; M2[k, k] += sl; M2[K, k] += ST[a]; M2[k, K] += EN[a]; cu[k] += use[a]
            if k != k0: moved += 1
            best = scores[k]
        if moved == 0: break
    return best, cid.copy()
ex_maps = {}
for K in KS:
    res = [exchange(K, 77 * K + r, sweeps=8) for r in range(3)]
    ll, cid = max(res, key=lambda t: t[0])
    ex_maps[K] = {s: f'E{K}_{cid[i]}' for i, s in enumerate(vocab)}
    log(f'exchange K={K}: class-bigram log-likelihood {ll:.1f}')

# ---------------- agreement
band = freq_band({s: int(use[idx[s]]) for s in vocab})
S = [s for s in vocab if use[idx[s]] >= MINUSE and s in HAND]
w = np.array([use[idx[s]] for s in S])
h = [HAND[s] for s in S]
rng = np.random.default_rng(5)
def agree(m, h_, weights=None):
    a = [m[s] for s in S]
    if weights is None: return ARI(h_, a), NMI(h_, a)
    rep_a = np.repeat(a, weights.astype(int)); rep_h = np.repeat(h_, weights.astype(int))
    return ARI(rep_h, rep_a), NMI(rep_h, rep_a)
rows = []
nulls_sh = [list(rng.permutation(h)) for _ in range(1000)]
nulls_band = []
for q in range(1000):
    dd = deal_within_bands({s: HAND[s] for s in S}, band, 9000 + q); nulls_band.append([dd[s] for s in S])
for name, maps in [('hidden-state model', hmm_maps), ('k-means on neighbour vectors', km_maps), ('exchange clustering', ex_maps)]:
    for K in KS:
        m = maps[K]
        ari, nmi = agree(m, h); ariw, nmiw = agree(m, h, w)
        sh = np.array([agree(m, z) for z in nulls_sh]); bd = np.array([agree(m, z) for z in nulls_band])
        rows.append(dict(method=name, K=K, ARI=ari, NMI=nmi, ARI_tokens=ariw, NMI_tokens=nmiw,
                         ARI_shuffled_mean=sh[:, 0].mean(), ARI_shuffled_max=sh[:, 0].max(), NMI_shuffled_mean=sh[:, 1].mean(), NMI_shuffled_max=sh[:, 1].max(),
                         ARI_band_mean=bd[:, 0].mean(), ARI_band_max=bd[:, 0].max(), NMI_band_mean=bd[:, 1].mean(), NMI_band_max=bd[:, 1].max(),
                         P_shuffle=(np.sum(sh[:, 1] >= nmi) + 1) / 1001, P_band=(np.sum(bd[:, 1] >= nmi) + 1) / 1001))
        log(f'{name} K={K}: ARI {ari:.3f} (shuffled {sh[:,0].mean():.3f}, band-dealt {bd[:,0].mean():.3f}) | NMI {nmi:.3f} (shuffled {sh[:,1].mean():.3f}, max {sh[:,1].max():.3f}; band {bd[:,1].mean():.3f}) | token-weighted ARI {ariw:.3f} NMI {nmiw:.3f}')
# machine methods against each other (same K)
for K in KS:
    a = [hmm_maps[K][s] for s in S]; b = [km_maps[K][s] for s in S]; c = [ex_maps[K][s] for s in S]
    rows.append(dict(method='HMM vs k-means', K=K, ARI=ARI(a, b), NMI=NMI(a, b)))
    rows.append(dict(method='HMM vs exchange', K=K, ARI=ARI(a, c), NMI=NMI(a, c)))
    log(f'machine vs machine K={K}: HMM-kmeans NMI {NMI(a,b):.3f}, HMM-exchange NMI {NMI(a,c):.3f}')
pd.DataFrame(rows).to_csv(f'{OUT}/agreement.csv', index=False)

# ---------------- token level (HMM K=10 state per token vs parser job per token)
hm = hmm_models[MAIN_K]
tok_state, tok_job = [], []
for x, R in zip(d.tok, d.R):
    jobs = token_jobs(x, R)
    O1, m1 = pad([x], idx)
    gam = hm.forward_backward(O1, m1, np.array([False]))[5][0]
    for t, (s, j) in enumerate(zip(x, jobs)):
        if j is None or s not in idx: continue
        if s in CNT: j = 'NUMBER'
        elif s == '060': j = 'JOINER'
        tok_state.append(int(np.argmax(gam[t]))); tok_job.append(j)
tari, tnmi = ARI(tok_job, tok_state), NMI(tok_job, tok_state)
sh = [NMI(rng.permutation(tok_job), tok_state) for _ in range(200)]
log(f'token level (all {len(tok_job)} Lipi tokens, HMM K=10 state vs parser job): ARI {tari:.3f} NMI {tnmi:.3f} (shuffled NMI mean {np.mean(sh):.4f} max {np.max(sh):.4f})')
ct = pd.crosstab(pd.Series(tok_job, name='parser job'), pd.Series(tok_state, name='HMM state'))
ct.to_csv(f'{OUT}/token_crosstab_hmm10.csv')
with open(f'{OUT}/token_level.txt', 'w') as f:
    f.write(f'tokens {len(tok_job)} ARI {tari:.4f} NMI {tnmi:.4f} shuffled NMI mean {np.mean(sh):.5f} max {np.max(sh):.5f}\n')

# ---------------- class table + disagreements (HMM K=10)
mainmap = hmm_maps[MAIN_K]
cl_major = {}
for c in sorted(set(mainmap.values())):
    jc = collections.Counter()
    for s in vocab:
        if mainmap[s] == c and s in HAND: jc[HAND[s]] += use[idx[s]]
    cl_major[c] = jc.most_common(1)[0][0] if jc else 'none'
    tot = sum(jc.values())
    mem = sorted([s for s in vocab if mainmap[s] == c], key=lambda s: -use[idx[s]])
    log(f'  {c}: {int(tot)} uses, hand jobs by uses ' + ', '.join(f'{j} {v/tot:.0%}' for j, v in jc.most_common(4)) + ' | top signs ' + ' '.join(mem[:14]))
hand_cid = {}
labs = sorted(set(HAND.values()) | {'UNSEEN'})
cidH = np.array([labs.index(HAND.get(s, 'UNSEEN')) for s in vocab])
base_ll = class_ll(cidH, len(labs))
dis = []
for s in S:
    mj = cl_major[mainmap[s]]
    if mj == HAND[s]: continue
    c2 = cidH.copy(); c2[idx[s]] = labs.index(mj)
    dl = (class_ll(c2, len(labs)) - base_ll) / np.log(2) / use[idx[s]]
    dis.append(dict(sign=s, uses=int(use[idx[s]]), hand_job=HAND[s], machine_class=mainmap[s], machine_implied_job=mj,
                    bits_per_use_if_moved=round(dl, 3), data_backs='machine' if dl > 0 else 'hand',
                    parser_token_jobs=' '.join(f'{k}:{v}' for k, v in HAND_TOKCOUNT[s].most_common(4))))
dis = pd.DataFrame(dis).sort_values('uses', ascending=False)
dis.to_csv(f'{OUT}/disagreements_hmm10.csv', index=False)
log(f'disagreements (signs with {MINUSE}+ uses): {len(dis)} of {len(S)}; data backs machine {int((dis.data_backs=="machine").sum())}, hand {int((dis.data_backs=="hand").sum())}')
# also: the best single move for every sign (what job does the class-bigram likelihood like best?)
best_rows = []
for s in S:
    sc = {}
    for j in labs:
        if j == 'UNSEEN': continue
        c2 = cidH.copy(); c2[idx[s]] = labs.index(j); sc[j] = class_ll(c2, len(labs))
    bj = max(sc, key=sc.get)
    best_rows.append(dict(sign=s, uses=int(use[idx[s]]), hand_job=HAND[s], likelihood_best_job=bj,
                          gain_bits_per_use=round((sc[bj] - sc[HAND[s]]) / np.log(2) / use[idx[s]], 3)))
bdf = pd.DataFrame(best_rows); bdf.to_csv(f'{OUT}/best_job_by_likelihood.csv', index=False)
log(f'signs whose own hand job is already the likelihood-best job: {(bdf.likelihood_best_job == bdf.hand_job).sum()} of {len(bdf)}')

# ---------------- save maps
cls = pd.DataFrame({'sign': vocab, 'uses_distinct_texts': use.astype(int), 'hand_job': [HAND.get(s, '') for s in vocab],
                    **{f'hmm{K}': [hmm_maps[K][s] for s in vocab] for K in KS},
                    **{f'kmeans{K}': [km_maps[K][s] for s in vocab] for K in KS},
                    **{f'exchange{K}': [ex_maps[K][s] for s in vocab] for K in KS},
                    'freq_band': [band[s] for s in vocab]})
cls['hmm10_implied_job'] = cls.hmm10.map(cl_major)
cls.to_csv(f'{OUT}/classes.csv', index=False)
log('wrote', f'{OUT}/classes.csv', f'{OUT}/agreement.csv', f'{OUT}/disagreements_hmm10.csv')
