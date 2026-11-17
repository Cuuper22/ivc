#!/usr/bin/env python3
"""U-shaped signs and containers: which side their count sits on, which stroke series, which number."""
import collections, sys
from long_cohesion import LL
from long_common import *
TALL = {f'{k:03d}' for k in range(31, 37)}; SHORT = {f'{k:03d}' for k in list(range(1, 8)) + list(range(13, 19)) + [12]}
def side_stats(s, lines):
    c = collections.Counter(); val = collections.Counter(); n = 0
    for l in lines:
        for i, a in enumerate(l):
            if a != s: continue
            n += 1
            L = l[i - 1] if i else None; R = l[i + 1] if i + 1 < len(l) else None
            if L in TALL: c['before tall'] += 1; val[('b', num_of(L))] += 1
            elif L in SHORT: c['before short'] += 1
            if R in TALL: c['after tall'] += 1; val[('a', num_of(R))] += 1
            elif R in SHORT: c['after short'] += 1
            if L not in TALL and L not in SHORT and R not in TALL and R not in SHORT: c['no count'] += 1
    return n, c, val
if __name__ == '__main__':
    for s in sys.argv[1:] or ['700', '705', '706', '711', '590', '595', '740', '575', '413', '806', '220']:
        n, c, val = side_stats(s, LL)
        print(s, snd(s), 'n', n, dict(c), 'values', dict(sorted(val.items())))
