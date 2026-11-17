#!/usr/bin/env python3
"""STEP 1, one redesign of the k-means cross-check (written after it came out at chance: NMI 0.154 against 0.131 shuffled).
Diagnosis fixed before rerun: the first version fitted on every sign with 3+ uses, where rare signs' noisy vectors
pull most signs into one big cluster. Redesign: fit only on the 166 signs with 10+ uses, neighbour blocks only
(left neighbour, right neighbour, position), the neighbour vocabulary = those same 166 signs + start/end, PCA to 20
dimensions, k-means (50 starts) and Ward clustering, K = 6, 8, 10, 12. Same agreement measure and shuffle null."""
from frame_common import *
from sklearn.metrics import adjusted_rand_score as ARI, normalized_mutual_info_score as NMI
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA

T = train_texts(); vocab, idx = vocab_of(T); C = counts(T, idx); use = C['uni']
S = [s for s in vocab if use[idx[s]] >= 10 and s in HAND]; si = {s: i for i, s in enumerate(S)}; n = len(S)
L = np.zeros((n, n + 2)); R = np.zeros((n, n + 2)); P = np.zeros((n, 4))
for x, c, k in T:
    m = len(x)
    for i, s in enumerate(x):
        if s not in si: continue
        a = si[s]
        l = x[i - 1] if i else '^'; r = x[i + 1] if i + 1 < m else '$'
        L[a, si.get(l, n) if l != '^' else n + 1] += 1
        R[a, si.get(r, n) if r != '$' else n + 1] += 1
        P[a] += [i == 0, i == m - 1, 0 < i < m - 1, m == 1]
X = np.hstack([np.sqrt(B / np.maximum(B.sum(1, keepdims=True), 1)) for B in (L, R, P)])
Xp = PCA(20, random_state=0).fit_transform(X)
h = [HAND[s] for s in S]; rng = np.random.default_rng(3)
nulls = [rng.permutation(h) for _ in range(1000)]
rows = []
for K in [6, 8, 10, 12]:
    for name, lab in [('k-means', KMeans(K, n_init=50, random_state=K).fit_predict(Xp)), ('Ward', AgglomerativeClustering(K).fit_predict(Xp))]:
        nmi = NMI(h, lab); sh = np.array([NMI(z, lab) for z in nulls])
        rows.append(dict(method=name, K=K, ARI=ARI(h, lab), NMI=nmi, NMI_shuffled_mean=sh.mean(), NMI_shuffled_max=sh.max(), P=(np.sum(sh >= nmi) + 1) / 1001,
                         biggest_cluster_share=np.bincount(lab).max() / n))
        log(f'{name} K={K}: ARI {ARI(h, lab):.3f} NMI {nmi:.3f} (shuffled {sh.mean():.3f}, max {sh.max():.3f}); biggest cluster {np.bincount(lab).max()} of {n} signs')
        if K == 10 and name == 'k-means':
            for c in range(K):
                mem = [S[i] for i in np.where(lab == c)[0]]
                log(f'   cluster {c}: ' + ' '.join(f'{s}:{HAND[s][:4]}' for s in sorted(mem, key=lambda s: -use[idx[s]])[:12]))
pd.DataFrame(rows).to_csv(f'{OUT}/agreement_kmeans_redesign.csv', index=False)
