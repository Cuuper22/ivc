#!/usr/bin/env python3
"""Split step 1: contexts of 850, 824, 001 and a two/three-profile clustering. Rule fixed before any number:
Occurrence = one sign in one DISTINCT first-catalogue text (the frame's training unit); features = left class, right class
(frame v2 base classes, '^' start '$' end, unknown when a neighbour is lost or an edge is broken), object kind, text-length
bucket. Model = mixture of K independent profiles (EM, 6 starts); K = 1, 2, 3 compared by held-out log-likelihood (5 folds of
TEXTS, so copies of a text never straddle). Then the fitted K=2 profiles are applied to copy events (one row per object,
moulded batches once; signlist_common.load_lipi) to give the clean context table with site.
Output: work_data/split/contexts_<sign>.csv, clusters.json, log_split_1.txt"""
from split_common import *
import json, signlist_common as sc
SIGNS = ['850', '824', '001']
rng = np.random.default_rng(11)
T = train_with_sites()
texts = [(x, c, k, st) for x, c, k, st in T]
KMAP = {'seals': 'seal', 'tablets': 'mtab', 'copper tablets': 'ctab', 'tags and sealings': 'tag', 'pots': 'pot'}
out = open(f'{SPL}/log_split_1.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); out.write(s + '\n'); out.flush()
EV = sc.load_lipi()
say(f'distinct texts {len(texts)}; copy events {len(EV)}')
res = {}
for s in SIGNS:
    occ = [(ti, i) for ti, t in enumerate(texts) for i, a in enumerate(t[0]) if a == s]
    X = np.array([ENC.enc(feat(texts[ti][0], i, texts[ti][1], texts[ti][2])) for ti, i in occ])
    tid = np.array([ti for ti, i in occ]); n = len(X)
    folds = rng.integers(0, 5, size=len(texts))[tid]
    cv = {}
    for K in (1, 2, 3):
        g = []
        for f in range(5):
            tr, te = X[folds != f], X[folds == f]
            if len(te) == 0: continue
            m = Mix(K, ENC.dims).fit(tr, np.random.default_rng(f)); g.append(m.loglik(te) / np.log(2))
        cv[K] = sum(g) / n
    say(f'sign {s}: {n} occurrences in distinct texts; held-out bits per occurrence (higher=better; K=1 is one profile): ' + ', '.join(f'K{K} {v:.3f}' for K, v in cv.items()) + f'; gain K2 over K1 {cv[2]-cv[1]:.3f}, K3 over K2 {cv[3]-cv[2]:.3f}')
    m2 = Mix(2, ENC.dims).fit(X, np.random.default_rng(5))
    m3 = Mix(3, ENC.dims).fit(X, np.random.default_rng(5))
    lab = m2.assign(X)
    # stability: refit with 5 other seeds, share of occurrences with the same grouping
    stab = []
    for sd in range(20, 25):
        m = Mix(2, ENC.dims).fit(X, np.random.default_rng(sd)); l2 = m.assign(X)
        stab.append(max((l2 == lab).mean(), (l2 != lab).mean()))
    say(f'  K=2 weights {m2.pi.round(2)}; sizes {np.bincount(lab, minlength=2)}; agreement across 5 refits {np.mean(stab):.3f} (min {np.min(stab):.3f})')
    for k in range(2):
        desc = ' | '.join(f'{ENC.names[j]}: ' + ', '.join(f'{[ENC.L, ENC.R, ENC.K, ENC.N][j][i]} {m2.th[j][k][i]:.2f}' for i in np.argsort(-m2.th[j][k])[:3]) for j in range(4))
        say(f'  group {k} (share {m2.pi[k]:.2f}): {desc}')
    res[s] = dict(cv=cv, pi=m2.pi.tolist(), th=[t.tolist() for t in m2.th], pi3=m3.pi.tolist(), th3=[t.tolist() for t in m3.th])
    # copy-event table (Lipi) with group assignment
    rows = []
    for e in EV:
        kind = KMAP.get(e['kind'], e['kind']); 
        for f, br in zip(e['faces'], e['broken']):
            x = tuple(f); 
            for i, a in enumerate(x):
                if a != s: continue
                clean = (not br) and not any(not sc.is_sign(b) for b in x)
                ft = feat(x, i, clean, kind)
                row = np.array([ENC.enc(ft)])
                rows.append(dict(event=e['ev'], site=e['site'], kind=ft[2], pos=i, length=len(x), pos_from_end=len(x) - 1 - i,
                                 left=ft[0], right=ft[1], left_sign=x[i-1] if i else '^', right_sign=x[i+1] if i < len(x)-1 else '$',
                                 group=int(m2.assign(row)[0]), group3=int(m3.assign(row)[0])))
    R = pd.DataFrame(rows); R.to_csv(f'{SPL}/contexts_{s}.csv', index=False)
    say(f'  copy events with {s}: {len(R)} rows; group sizes {R.group.value_counts().sort_index().tolist()}')
    for g in range(2):
        G = R[R.group == g]
        say(f'    group {g}: n {len(G)}; at text start {(G.pos==0).mean():.2f}, at end {(G.pos_from_end==0).mean():.2f}; kinds {G.kind.value_counts().head(3).to_dict()}; sites {G.site.value_counts().head(3).to_dict()}; left {G.left.value_counts().head(3).to_dict()}; right {G.right.value_counts().head(3).to_dict()}')
json.dump(res, open(f'{SPL}/clusters.json', 'w'))
