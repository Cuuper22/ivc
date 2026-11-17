#!/usr/bin/env python3
"""Repairs for the signs that damage the long readings; each new value is checked on texts of 5 signs or fewer (or on objects outside the 41)."""
import collections, math
from long_cohesion import LL
from long_common import *
from long_vessels import side_stats, TALL, SHORT
objs = build_objects()
short_lines = [l for l in LL if 2 <= len(l) <= 5]
print('lines total', len(LL), 'short (2-5 signs)', len(short_lines))
# ---------- A. 705 / 706 / 711: count-after vessels with a fixed three
def tall_share(lines, s):
    n, c, val = side_stats(s, lines)
    t = c['after tall'] + c['before tall']; sh = c['after short'] + c['before short']
    return n, t, sh, c, val
# baseline: for non-number signs with an adjacent count: share tall
base_t = base_s = 0
for l in LL:
    for i, a in enumerate(l):
        if a in CNT: continue
        for nb in ((l[i - 1] if i else None), (l[i + 1] if i + 1 < len(l) else None)):
            if nb in TALL: base_t += 1
            elif nb in SHORT: base_s += 1
print(f'A. baseline over all signs: tall {base_t}, short {base_s}, tall share {base_t/(base_t+base_s):.2f}')
for s in ('705', '706', '711', '700', '590', '220'):
    for nm, lines in (('all lines', LL), ('short 2-5', short_lines)):
        n, t, sh, c, val = tall_share(lines, s)
        aft = sum(v for (k, _), v in val.items() if k == 'a'); three = val.get(('a', 3), 0)
        print(f'   {s} {snd(s)} {nm}: n {n}, adjacent counts tall {t} short {sh} (tall share {t/max(1,t+sh):.2f}); count after {aft}, of them three {three}')
# left neighbour of 705/706 in short lines: fish or house word?
FISHC = {'220', '235', '240', '233', '231', '226', '236'}
for s in ('705', '706'):
    L = collections.Counter(); 
    for l in short_lines:
        for i, a in enumerate(l):
            if a == s: L['fish' if i and l[i - 1] in FISHC else '^' if i == 0 else 'other'] += 1
    print(f'   {s} in short lines: left neighbour', dict(L))
# which object faces carry 705 / 706 -- other face?
two = collections.Counter()
for o in objs.values():
    if len(o['faces']) == 2:
        sg = [set(s for l in f['lines'] for s in l) for f in o['faces']]
        for a, b in ((0, 1), (1, 0)):
            if '705' in sg[a] or '706' in sg[a]:
                two['has 705/706 face'] += 1
                if '700' in sg[b] or any(x in TALL for x in sg[b]): two['other face has cup or tall count'] += 1
print('   two-face objects:', dict(two))
n2 = sum(1 for o in objs.values() if len(o['faces']) == 2); c2 = sum(1 for o in objs.values() if len(o['faces']) == 2 and any(('700' in {s for l in f['lines'] for s in l}) for f in o['faces']))
print('   two-face objects with a cup 700 on some face', c2, 'of', n2)
# ---------- B. 413 header
first = last = tot = 0; nxt = collections.Counter(); T2 = collections.Counter()
for o in objs.values():
    for fi, f in enumerate(o['faces']):
        for l in f['lines']:
            for i, a in enumerate(l):
                if a == '413':
                    tot += 1; first += (i == 0)
                    nxt[l[i + 1] if i + 1 < len(l) else '$'] += 1
print(f'B. 413: n {tot}, line-first {first} ({first/tot:.0%}); next sign', nxt.most_common(6))
# 413 faces on tablets: the other face
og = collections.Counter()
for o in objs.values():
    if o['type'].startswith('TAB') and len(o['faces']) == 2:
        sg = [[s for l in f['lines'] for s in l] for f in o['faces']]
        for a, b in ((0, 1), (1, 0)):
            if sg[a] and sg[a][0] == '413':
                og['413-initial face'] += 1
                if any(x in TALL for x in sg[b]) or '700' in sg[b]: og['other face has cup/tall count'] += 1
allt = sum(1 for o in objs.values() if o['type'].startswith('TAB') and len(o['faces']) == 2)
allc = sum(1 for o in objs.values() if o['type'].startswith('TAB') and len(o['faces']) == 2 and any(any(x in TALL or x == '700' for l in f['lines'] for x in l) for f in o['faces']))
print('   two-face tablets: with cup/tall count on some face', allc, 'of', allt, '|', dict(og))
# 413-892 'grain sale'
c892 = sum(1 for l in LL for i in range(len(l) - 1) if l[i] == '413' and l[i + 1] == '892')
c892b = sum(1 for l in LL for i in range(len(l) - 1) if l[i + 1] == '892' and l[i] != '413')
print(f'   413-892: {c892} lines; 892 after something else: {c892b}')
# 892 elsewhere (not after 413): where
# ---------- C. 060 as a linking particle in short lines
HEAD = {'920', '692', '550', '820'}
c = collections.Counter()
for l in short_lines:
    for i, a in enumerate(l):
        if a == '060':
            c['060'] += 1
            c['head left'] += (i > 0 and l[i - 1] in HEAD)
            c['ward right'] += (i + 1 < len(l) and l[i + 1] in {'741', '742', '745'})
            c['name right'] += (i + 1 < len(l) and l[i + 1] not in {'741', '742', '745'})
print('C. 060 in short lines', dict(c))
allc = collections.Counter()
for l in LL:
    for i, a in enumerate(l):
        if a == '060':
            allc['060'] += 1; allc['head left'] += (i > 0 and l[i - 1] in HEAD); allc['ward right'] += (i + 1 < len(l) and l[i + 1] in {'741', '742', '745'})
print('   all lines', dict(allc))
# the four heads: do the same names follow? name set after 060 per head
afterhead = collections.defaultdict(collections.Counter)
for l in LL:
    for i, a in enumerate(l[:-2]):
        if a in HEAD and l[i + 1] == '060': afterhead[a][l[i + 2]] += 1
for h, cc in afterhead.items(): print(f'   {h} 060 -> next:', cc.most_common(6), 'n', sum(cc.values()))
# ---------- D. 435 against staff signs: neighbour-profile cosine
def vec(s):
    v = collections.Counter()
    for l in LL:
        for i, a in enumerate(l):
            if a == s:
                v['L' + (l[i - 1] if i else '^')] += 1; v['R' + (l[i + 1] if i + 1 < len(l) else '$')] += 1
    return v
def cos(a, b):
    d = sum(a[k] * b[k] for k in a); return d / math.sqrt(sum(x * x for x in a.values()) * sum(x * x for x in b.values()))
freq = collections.Counter(s for l in LL for s in l)
cand = [s for s, n in freq.items() if n >= 20 and s != '435' and s not in CNT and s != '000']
V = {s: vec(s) for s in cand + ['435']}
rank = sorted(((cos(V['435'], V[s]), s) for s in cand), reverse=True)
print('D. 435 nearest neighbours by context:', [(s, round(c, 2), snd(s) or '') for c, s in rank[:8]])
for s in ('142', '095', '070', '255', '690'):
    if s in V: print(f'   rank of {s} ({snd(s)}):', [i for i, (c, t) in enumerate(rank) if t == s], round(cos(V['435'], V[s]), 2), 'of', len(rank))
# the block 255-435-690
blk = collections.Counter()
for l in LL:
    for i in range(len(l) - 2):
        if l[i:i + 3] == ('255', '435', '690'): blk['255-435-690'] += 1; blk['then jar'] += (i + 3 < len(l) and l[i + 3] == '740'); blk['line-final'] += (i + 3 == len(l))
        if l[i:i + 3] == ('255', '435', '156'): blk['255-435-156'] += 1
print('   block', dict(blk), '; in short lines:', sum(1 for l in short_lines for i in range(len(l) - 1) if l[i:i + 2] == ('255', '435')))
