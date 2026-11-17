#!/usr/bin/env python3
"""Job 1, step 1: which signs are tied to one picture type far above chance?
Unit = one distinct text with its picture (copies collapsed). Chance = picture labels shuffled among units of the same
site and object kind (1000 shuffles). Cells with 2+ units only. Writes work_data/sound_v6/picture_scan.csv."""
from sound_v6_common import *
U = units()
print(f'units (distinct text + picture): {len(U)}; by kind', collections.Counter(u[0].split('|')[1] for u in U), flush=True)
pics = sorted(set(u[1] for u in U)); pi = {p: i for i, p in enumerate(pics)}
signs = sorted(set(a for u in U for a in u[2])); si = {s: i for i, s in enumerate(signs)}
X = np.zeros((len(U), len(signs)), np.float32)
for r, u in enumerate(U):
    for a in u[2]: X[r, si[a]] = 1
lab = np.array([pi[u[1]] for u in U]); strata = collections.defaultdict(list)
for r, u in enumerate(U): strata[u[0]].append(r)
def onehot(l):
    H = np.zeros((len(l), len(pics)), np.float32); H[np.arange(len(l)), l] = 1; return H
obs = onehot(lab).T @ X
cells = np.argwhere(obs >= 2)
NS = 1000; ge = np.zeros(len(cells)); tot = np.zeros(len(cells))
for k in range(NS):
    l = lab.copy()
    for ii in strata.values():
        ii = np.array(ii); l[ii] = rng.permutation(l[ii])
    sim = onehot(l).T @ X
    v = sim[cells[:, 0], cells[:, 1]]; tot += v; ge += v >= obs[cells[:, 0], cells[:, 1]]
    if k % 200 == 0: print(f'  shuffle {k}/{NS}', flush=True)
rows = []
for j, (p, s) in enumerate(cells):
    o = obs[p, s]; e = tot[j] / NS
    rows.append(dict(picture=pics[p], picture_en=PIC_EN.get(pics[p], pics[p]), sign=signs[s], units_with_both=int(o), expected=round(e, 2),
                     ratio=round(o / max(e, 0.01), 1), p=(ge[j] + 1) / (NS + 1), units_with_picture=int((lab == p).sum()), units_with_sign=int(X[:, s].sum())))
R = pd.DataFrame(rows).sort_values(['p', 'ratio'], ascending=[True, False])
R.to_csv(f'{OUT6}/picture_scan.csv', index=False)
print(f'cells tested {len(R)}; at P<=0.01: {(R.p <= 0.01).sum()} (about {len(R) * 0.01:.1f} by chance); at P<=0.002: {(R.p <= 0.002).sum()} (about {len(R) * 0.002:.1f})')
pd.set_option('display.width', 200)
print(R[(R.p <= 0.01) & (R.ratio >= 2)].head(60).to_string(index=False))
