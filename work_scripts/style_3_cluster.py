#!/usr/bin/env python3
"""STYLE step 3: cluster the coded unicorn stones into styles. Rules written before running:
- Features: those KEPT in agreement.csv (self-agreement >= 0.75 on >= 15 stones read twice).
- Stones pooled: main 300 + the 65 twin-only stones (same coding scheme, coded blind the same way).
- Core set: stones with >= 6 kept features read. Distance = share of mismatches over features read on both stones
  (Gower distance for categories). Average-linkage hierarchical clustering on the core set.
- k chosen among 3..8: highest mean silhouette among k whose smallest group has >= 8 stones (if none qualifies, highest
  silhouette overall).
- Stones with 3-5 kept features read are assigned to the group with the lowest mean distance to its core members
  (assigned = 'late'); < 3 features read: no style.
Output: work_data/style/styles.csv (one row per object with codes, style, catalogue fields) and log_3.txt.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_common import *
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
A = pd.read_csv(f'{OUT}/agreement.csv'); KEEP = list(A[A.kept].feature)
def load(tag):
    C = pd.read_csv(f'{OUT}/codes_{tag}.csv', dtype=str); K = pd.read_csv(f'{OUT}/key_{tag}.csv', dtype=str)
    return C.merge(K[['num', 'obj', 'cisi']], on='num').assign(src=tag)
D = pd.concat([load('main'), load('twins')], ignore_index=True)
O = objects(); O['obj'] = O.obj.astype(str)
D = D.merge(O[['obj', 'site', 'city', 'stand5', 'area_mm2', 'bin', 'building', 'signs', 'kind', 'n', 'condition']], on='obj', how='left')
D['letter'] = D.stand5.fillna('').replace({'': '-'})
X = D[KEEP].values; R = X != '?'; D['nread'] = R.sum(1)
def dist(i, j):
    m = R[i] & R[j]
    return (X[i][m] != X[j][m]).mean() if m.sum() >= 2 else 0.5
core = np.where(D.nread >= 6)[0]; n = len(core)
M = np.zeros((n, n))
for a in range(n):
    for b in range(a + 1, n): M[a, b] = M[b, a] = dist(core[a], core[b])
Z = linkage(squareform(M), 'average')
def silhouette(lab):
    s = []
    for i in range(n):
        own = lab == lab[i]; own[i] = False
        if own.sum() == 0: s.append(0); continue
        a = M[i, own].mean(); b = min(M[i, lab == g].mean() for g in set(lab) if g != lab[i]); s.append((b - a) / max(a, b))
    return float(np.mean(s))
log = [f'kept features: {KEEP}', f'stones: {len(D)}, core (>=6 read): {n}']
best = None; table = []
for k in range(3, 9):
    lab = fcluster(Z, k, 'maxclust'); sizes = np.bincount(lab)[1:]; sil = silhouette(lab)
    table.append((k, sil, sorted(sizes, reverse=True))); log.append(f'k={k} silhouette={sil:.3f} sizes={sorted(sizes, reverse=True)}')
ok = [t for t in table if min(t[2]) >= 8]
k = max(ok or table, key=lambda t: t[1])[0]; log.append(f'chosen k={k}')
lab = fcluster(Z, k, 'maxclust')
# rename groups by size: S1 largest
order = {g: f'S{r + 1}' for r, g in enumerate(pd.Series(lab).value_counts().index)}
D['sty'] = ''; D['assigned'] = ''
D.loc[D.index[core], 'sty'] = [order[g] for g in lab]; D.loc[D.index[core], 'assigned'] = 'core'
for i in np.where((D.nread >= 3) & (D.nread < 6))[0]:
    best = None
    for g in sorted(set(order.values())):
        mem = core[np.array([order[x] for x in lab]) == g]
        d = np.mean([dist(i, j) for j in mem])
        if best is None or d < best[1]: best = (g, d)
    D.loc[D.index[i], 'sty'] = best[0]; D.loc[D.index[i], 'assigned'] = 'late'
# profile
for g in sorted(set(order.values())):
    sub = D[D.sty == g]; log.append(f'\n{g}: {len(sub)} stones ({(sub.assigned == "core").sum()} core)')
    for f in KEEP:
        vc = sub[f][sub[f] != '?'].value_counts(normalize=True).round(2)
        log.append(f'  {f}: ' + ', '.join(f'{v} {p}' for v, p in vc.items()))
D.to_csv(f'{OUT}/styles.csv', index=False)
open(f'{OUT}/log_3.txt', 'w').write('\n'.join(log)); print('\n'.join(log))
