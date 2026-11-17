#!/usr/bin/env python3
"""ROUND SEALS, step 2b: one redesign of the tally test after A/B/C went against (they match the sign stock, not an order).
REDESIGN: condition on the texts that hold BOTH a person sign and a stroke sign; ask how many of them put one next to the other
(either order), against the same texts with signs shuffled inside the text (10,000). PREDICTION (now): if round texts are
person+count units, adjacency in those texts beats the shuffle (P < 0.05) and the stroke goes one way round (all [person][stroke] or all [stroke][person]).
Also: stroke runs. For texts with a person sign, the stroke signs next to it: how many are 'small' (001-004) against tall (031-036)?
Output: log_2b.txt
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'round_02_structure.py')).read().split('# ---------------- shared first')[0].split('rows = []')[0])
both = [(i, t) for i, t in RT.items() if len(t) >= 2 and any(s in PERSON for s in t) and any(s in STROKES for s in t)]
def adj(t):
    t = cls(t); return any((a in PERSON and b in STROKES) or (a in STROKES and b in PERSON) for a, b in zip(t, t[1:]) if a and b)
real_n = sum(adj(t) for _, t in both)
sh = [sum(adj(tuple(rng.permutation(np.array(t, dtype=object)))) for _, t in both) for _ in range(10000)]
print('texts with person and stroke:', len(both), [i for i, _ in both]); print('adjacent in', real_n, 'shuffled mean', np.mean(sh), 'P higher', (np.sum(np.array(sh) >= real_n) + 1) / 10001)
ab = [adj(t) for _, t in both]; print([(i, adj(t), '-'.join(t)) for i, t in both])
order = collections.Counter()
for _, t in both:
    c = cls(t)
    for a, b in zip(c, c[1:]):
        if a and b and a in PERSON and b in STROKES: order['person then stroke'] += 1
        if a and b and a in STROKES and b in PERSON: order['stroke then person'] += 1
print(order)
