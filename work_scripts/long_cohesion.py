#!/usr/bin/env python3
"""Pair cohesion over all distinct corpus lines and recurring n-grams.  Import: from long_cohesion import COH, ngram_units"""
import collections
from long_common import *
objs = build_objects()
LINES = set()
for ob in objs.values():
    for f in ob['faces']:
        for l in f['lines']:
            if l and '000' not in l: LINES.add(tuple(l))
C1 = collections.Counter(); C2 = collections.Counter()
for l in LINES:
    for s in l: C1[s] += 1
    for a, b in zip(l, l[1:]): C2[(a, b)] += 1
def coh(a, b):
    c = C2[(a, b)]
    return c / max(1, C1[a] + C1[b] - c)
NG = collections.defaultdict(set)
for i, l in enumerate(LINES):
    pass
LL = list(LINES)
NGC = collections.Counter()
for l in LL:
    seen = set()
    for n in (2, 3, 4, 5):
        for k in range(len(l) - n + 1):
            seen.add(l[k:k + n])
    for g in seen: NGC[g] += 1
def ngram_units(x, minc2=6, minc3=3):
    """Recurring n-grams (>=3 signs, >=3 distinct lines; or 2 signs >=6) found in x, longest first, non-overlapping greedy."""
    n = len(x); res = []; used = [False] * n
    cands = []
    for L in (5, 4, 3, 2):
        for k in range(n - L + 1):
            g = tuple(x[k:k + L]); c = NGC.get(g, 0)
            if (L >= 3 and c >= minc3) or (L == 2 and c >= minc2): cands.append((L, c, k, g))
    cands.sort(key=lambda t: (-t[0], -t[1]))
    for L, c, k, g in cands:
        if not any(used[k:k + L]):
            for q in range(k, k + L): used[q] = True
            res.append((k, g, c))
    return sorted(res)
def soft_cuts(x, thr=0.12):
    cs = []
    for i in range(1, len(x)):
        if coh(x[i - 1], x[i]) < thr: cs.append(i)
    return cs
if __name__ == '__main__':
    print(len(LL))
    x = ('032','632','125','390','002','235','240','032','220','255','435','690','740')
    print([(i, round(coh(x[i-1], x[i]),3)) for i in range(1,len(x))])
    print(ngram_units(x))
