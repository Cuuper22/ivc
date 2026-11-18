#!/usr/bin/env python3
"""Slot summary of each of the eight signs: every slot, neighbours, object kinds, sites, findspots, counts after/before."""
import sys, collections
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from holes_common import *
ls = lines(True)
base_kind = collections.Counter(kind(L['type']) for L in ls)
base_site = collections.Counter(L['site'] for L in ls)
nl = sum(1 for _ in ls)
def tag(s): return f"{s}[{snd(s) or '?'}]"
out = []
for sg in EIGHT + ['705', '706', '435']:
    U = uses(sg, ls); n = len(U)
    if not n: out.append(f'## {sg}: no uses'); continue
    pos = collections.Counter(); L_ = collections.Counter(); R_ = collections.Counter(); K = collections.Counter(); S = collections.Counter(); A = collections.Counter()
    ln = collections.Counter(); objs_ = set(); lone = 0
    for i, p in U:
        L = ls[i]; t = L['toks']; m = len(t)
        pos['alone' if m == 1 else 'first' if p == 0 else 'last' if p == m - 1 else 'inner'] += 1
        L_[t[p-1] if p > 0 else '^'] += 1; R_[t[p+1] if p < m-1 else '$'] += 1
        K[kind(L['type'])] += 1; S[L['site']] += 1; A[L['animal']] += 1; ln[m] += 1; objs_.add(L['obj'])
    out.append(f'## {sg} {SH.get(sg,"")[:90]}  uses {n} in {len(objs_)} objects')
    out.append(f'slots {dict(pos)}  line lengths {dict(sorted(ln.items()))}')
    out.append('left  : ' + ', '.join(f'{tag(k)} {v}' for k, v in L_.most_common(10)))
    out.append('right : ' + ', '.join(f'{tag(k)} {v}' for k, v in R_.most_common(10)))
    out.append('kinds : ' + ', '.join(f'{k} {v} (exp {base_kind[k]*n/nl:.1f})' for k, v in K.most_common(8)))
    out.append('sites : ' + ', '.join(f'{k} {v}' for k, v in S.most_common(10)))
    out.append('animal: ' + ', '.join(f'{k} {v}' for k, v in A.most_common(6)))
open(f'{HOLES}/slots_first_look.txt', 'w').write('\n'.join(out))
print('\n'.join(out))
