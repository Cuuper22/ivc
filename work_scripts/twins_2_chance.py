#!/usr/bin/env python3
"""TWINS step 2: at what text length is a twin no longer chance?  Written 2026-11-17 before the run.

Two nulls, 300 rounds each, on the 1,5xx complete seal faces of the first catalogue (one face per stone per text):
  N1 'token shuffle': every sign of every text is dealt at random over all text positions (each text keeps its length,
     the corpus keeps its sign counts). Order and grammar are destroyed.
  N2 'sign-pair generator': each text is regenerated at its own length from the sign-pair table of the same seals
     (first sign from the first-sign counts, each next sign from what follows the sign before). Keeps short-range grammar,
     so it is generous to chance.
Prediction: N1 gives many 1-sign and some 2-sign twin sets and almost none at 3+; N2 gives more at 2 and 3 and
essentially none at 5+. Real twin sets at length 4+ are then not chance under either null; at length 2 they are partly
chance under N2. Twin sets counted as in step 1 (2+ different stones with the identical text).
"""
from twins_common import *
import collections
rng = np.random.default_rng(17)
S = pd.read_csv(f'{OUT}/seals.csv', dtype=str).fillna('')
C = S[S.complete == 'True'].drop_duplicates(['obj', 'signs'])
texts = [tuple(t.split('-')) for t in C.signs]
L = np.array([len(t) for t in texts])
def count_sets(tt):
    c = collections.Counter(tt); out = collections.Counter(); seals = collections.Counter()
    for t, n in c.items():
        if n >= 2: out[min(len(t), 6)] += 1; seals[min(len(t), 6)] += n
    return out, seals
real, realseals = count_sets(texts)
tok = np.array([s for t in texts for s in t])
first = collections.Counter(t[0] for t in texts)
nxt = collections.defaultdict(collections.Counter)
for t in texts:
    for a, b in zip(t, t[1:]): nxt[a][b] += 1
F = (np.array(list(first.keys())), np.array(list(first.values()), float))
NX = {a: (np.array(list(c.keys())), np.array(list(c.values()), float)) for a, c in nxt.items()}
uni = collections.Counter(tok); U = (np.array(list(uni.keys())), np.array(list(uni.values()), float))
def draw(p): k, w = p; return k[rng.choice(len(k), p=w / w.sum())]
R = 300; n1 = collections.defaultdict(list); n2 = collections.defaultdict(list)
for r in range(R):
    perm = rng.permutation(tok); i = 0; tt = []
    for l in L: tt.append(tuple(perm[i:i + l])); i += l
    a, _ = count_sets(tt)
    tt2 = []
    for l in L:
        x = [draw(F)]
        while len(x) < l: x.append(draw(NX[x[-1]]) if x[-1] in NX else draw(U))
        tt2.append(tuple(x))
    b, _ = count_sets(tt2)
    for k in range(1, 7): n1[k].append(a[k]); n2[k].append(b[k])
    if (r + 1) % 50 == 0: log('t2', f'round {r+1}/{R}')
rows = []
for k in range(1, 7):
    rows.append(dict(length=k if k < 6 else '6+', texts=int(((L == k) if k < 6 else (L >= 6)).sum()), real_sets=real[k], real_seals=realseals[k],
                     shuffle_mean=np.mean(n1[k]), shuffle_max=max(n1[k]), P_shuffle=(np.sum(np.array(n1[k]) >= real[k]) + 1) / (R + 1),
                     pairgen_mean=np.mean(n2[k]), pairgen_max=max(n2[k]), P_pairgen=(np.sum(np.array(n2[k]) >= real[k]) + 1) / (R + 1)))
T = pd.DataFrame(rows); T.to_csv(f'{OUT}/chance_by_length.csv', index=False)
print(T.round(3).to_string(index=False))
