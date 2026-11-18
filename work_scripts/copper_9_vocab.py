#!/usr/bin/env python3
"""COPPER step 9 (new angle): do copper tablets speak their own vocabulary?

For each object kind at Mohenjo-daro (copper tablets, clay tablets, tags, seals), the distinct adjacent sign pairs in its
complete faces; share of those pairs that occur anywhere on an object of ANOTHER kind (any site). Control for size: the
same share for random samples of seal pairs of the same number as the copper pairs (seals are the big kind), 2,000 draws.
Also the share of each kind's distinct signs that occur on other kinds.

Prediction written 2026-11-17 before the numbers:
 P9.1 Copper pairs occur on other kinds of object less than half as often as clay-tablet pairs do: the copper tablets
      carry a closed set of phrases used nowhere else.
Writes work_data/copper/vocab.csv, log_9.txt.
"""
import sys; sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from copper_common import *
say = say_to(f'{OUT}/log_9.txt')
pairs_by_kind = collections.defaultdict(set); signs_by_kind = collections.defaultdict(set)
md = collections.defaultdict(set); mds = collections.defaultdict(set)
for o in objs.itertuples():
    for f in o.faces:
        f = [s for s in f]
        if '000' in f: continue
        P = {(a, b) for a, b in zip(f, f[1:])}
        pairs_by_kind[o.kind] |= P; signs_by_kind[o.kind] |= set(f)
        if o.site == 'Mohenjo-daro': md[o.kind] |= P; mds[o.kind] |= set(f)
rows = []
for k in ('ctab', 'mtab', 'tag', 'seal'):
    other = set().union(*[v for kk, v in pairs_by_kind.items() if kk != k])
    others = set().union(*[v for kk, v in signs_by_kind.items() if kk != k])
    P = md[k]; S = mds[k]
    rows.append(dict(kind=k, distinct_pairs=len(P), pairs_on_other_kinds=len(P & other), share=round(len(P & other) / max(len(P), 1), 3),
                     distinct_signs=len(S), signs_on_other_kinds=len(S & others), sign_share=round(len(S & others) / max(len(S), 1), 3)))
V = pd.DataFrame(rows); V.to_csv(f'{OUT}/vocab.csv', index=False)
say('\n' + V.to_string(index=False))
rng = np.random.default_rng(17)
seal_list = sorted(md['seal']); other = set().union(*[v for kk, v in pairs_by_kind.items() if kk != 'seal'])
n = len(md['ctab'])
sims = [np.mean([seal_list[i] in other for i in rng.choice(len(seal_list), n, replace=False)]) for _ in range(2000)]
say(f'random {n} seal pairs found on other kinds: mean {np.mean(sims):.3f}, min {np.min(sims):.3f}')
oth = set().union(*[v for kk, v in pairs_by_kind.items() if kk != 'ctab'])
only = sorted(p for p in md['ctab'] if p not in oth)
say(f'copper-only pairs ({len(only)}): ' + ' '.join(f'{a}-{b}' for a, b in only))

# redesign after P9.1 went against (written after the first run): count objects, not distinct pairs. Share of
# Mohenjo-daro objects of each kind whose text carries at least one pair found on no other kind of object.
for k in ('ctab', 'mtab', 'tag'):
    oth = set().union(*[v for kk, v in pairs_by_kind.items() if kk != k])
    n = h = 0
    for o in objs[(objs.kind == k) & (objs.site == 'Mohenjo-daro')].itertuples():
        P = {(a, b) for f in o.faces if '000' not in f for a, b in zip(f, f[1:])}
        if not P: continue
        n += 1; h += bool(P - oth)
    say(f'redesign: {k} objects with a pair found on no other kind: {h} of {n} ({h / max(n, 1):.3f})')
