#!/usr/bin/env python3
"""Step 3b: test the new count-attachment rule (corpus_build2.reattach) against the old parser, on batches of near-identical objects.
PREDICTION (written first): the right attachment makes every copy read the same. Copies of one tablet are the same string, so the
test that bites is on BATCHES: faces with the same non-count signs (the 'skeleton') but different count signs (other numbers, or the
number on the other side). If a rule attaches the count to the right thing, the set of signs that receive a count is the same in every
variant of the batch. Score = share of batches (2+ distinct count patterns, 2+ distinct texts) where all variants agree.
Also: how many faces change; how decisive the side score is on the first catalogue and on the new texts."""
from odd_common import *
import corpus_build2 as C
F = faces()
def targets(x, R):
    out = []
    n = len(x)
    for i, r in enumerate(R):
        if r == 'counted':
            nb = []
            if i > 0 and R[i-1] == 'count': nb.append('L')
            if i + 1 < n and R[i+1] == 'count': nb.append('R')
            out.append((x[i], ''.join(nb)))
    return tuple(sorted(out))
def skeleton(x): return tuple(a for a in x if a not in CNT)
groups = collections.defaultdict(list)
changed = tot = 0
for f in F:
    x, P = f['x'], f['P']
    if f['kind'] == 'seal' or not any(a in CNT for a in x): continue
    old = targets(x, P['roles']); new = targets(x, C.reattach(x, P['roles']))
    tot += 1; changed += old != new
    groups[skeleton(x)].append((x, old, new, f['cat']))
def score(idx):
    ok = n = 0
    for sk, L in groups.items():
        texts = {x for x, *_ in L}
        if len(texts) < 2: continue
        pats = {tuple(a for a in x if a in CNT) for x in texts}
        if len(pats) < 2: continue
        n += 1; ok += len({l[idx] for l in L}) == 1
    return ok, n
for cat in ('both',):
    print(f'goods faces with a count: {tot}; attachment changed by the new rule on {changed} ({changed/tot:.1%})')
    o, n = score(1); nn, n2 = score(2)
    print(f'batches (same skeleton, 2+ different count patterns): {n}; every variant gives the same counted signs: old rule {o} ({o/n:.1%}), new rule {nn} ({nn/n2:.1%})')
    # sign-test between rules on the batches where they differ
    b = w = 0
    for sk, L in groups.items():
        texts = {x for x, *_ in L}
        if len(texts) < 2 or len({tuple(a for a in x if a in CNT) for x in texts}) < 2: continue
        so = len({l[1] for l in L}) == 1; sn = len({l[2] for l in L}) == 1
        if sn and not so: b += 1
        if so and not sn: w += 1
    print(f'batches that only the new rule makes consistent: {b}; only the old rule: {w}; sign-test P {pbin(b, b+w, 0.5):.4g}')
# decisiveness + new texts: how many ambiguous runs and how often the sides disagree strongly
amb = strong = 0
for f in F:
    if f['cat'] != 'Mu': continue
    x = f['x']; R = f['roles']
    for i in range(1, len(x) - 1):
        pass
print('see tables in work_data/odd/count_sides.csv for the per-sign edge counts')
# show the biggest changes
ex = collections.Counter()
for sk, L in groups.items():
    for x, old, new, cat in L:
        if old != new: ex[('-'.join(x), str(old), str(new))] += 1
print('most frequent changed faces (text, old targets, new targets):')
for k, v in ex.most_common(14): print('  ', v, k)
