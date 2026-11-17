#!/usr/bin/env python3
"""Profile of chosen signs over all distinct lines: neighbours (with sounds), object types, line position, counts around, long vs short."""
import sys, collections
from long_cohesion import LL
from long_common import *
objs = build_objects()
def prof(s, k=7):
    L = collections.Counter(); R = collections.Counter(); pos = collections.Counter(); ty = collections.Counter(); site = collections.Counter(); n = 0
    for o in objs.values():
        hit = False
        for f in o['faces']:
            for l in f['lines']:
                for i, a in enumerate(l):
                    if a != s: continue
                    hit = True; n += 1
                    L[l[i - 1] if i else '^'] += 1; R[l[i + 1] if i + 1 < len(l) else '$'] += 1
                    pos['first' if i == 0 else 'last' if i == len(l) - 1 else 'mid'] += 1
        if hit: ty[o['type'].split(':')[0]] += 1; site[o['site']] += 1
    f = lambda c: ', '.join(f'{a}{"/" + snd(a) if a in V2 and snd(a) else ""} {b}' for a, b in c.most_common(k))
    return f'sign {s} ({shape_words(s)[:60]}) n={n}; position {dict(pos)}; types {dict(ty.most_common(5))}; sites {dict(site.most_common(4))}\n   left: {f(L)}\n   right: {f(R)}'
if __name__ == '__main__':
    for s in sys.argv[1:]: print(prof(s)); print()
