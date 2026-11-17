#!/usr/bin/env python3
"""Extra tests for the repairs: 255-435 seal size, 060 next to the jar, 413 lines with a count, 705/706 in the 41."""
import collections, statistics, json
from long_cohesion import LL
from long_common import *
objs = build_objects()
def area(o):
    try:
        h = float(o['h']); v = float(o['v']); return h * v if h > 0 and v > 0 else None
    except: return None
seal = [o for o in objs.values() if o['type'].startswith('SEAL')]
def has(o, pat):
    for f in o['faces']:
        for l in f['lines']:
            t = tuple(l)
            for i in range(len(t) - len(pat) + 1):
                if t[i:i + len(pat)] == tuple(pat): return True
    return False
def med(lst): lst = [a for a in lst if a]; return (round(statistics.median(lst)), len(lst)) if lst else None
allm = med([area(o) for o in seal])
print('seal face median, all seals', allm)
for pat in (('255', '435'), ('255', '435', '690'), ('255',), ('070',)):
    sel = [o for o in seal if has(o, pat)]
    print('  seals with', '-'.join(pat), med([area(o) for o in sel]))
n255 = [o for o in seal if has(o, ('255',)) and not has(o, ('255', '435'))]
print('  seals with 255 but not 255-435', med([area(o) for o in n255]))
# 060 then jar directly
c = sum(1 for l in LL for i in range(len(l) - 1) if l[i] == '060' and l[i + 1] == '740'); print('060 immediately before the jar:', c, 'of', sum(1 for l in LL for a in l if a == '060'))
# 413 lines containing a tall count or cup
n = k = 0
for l in LL:
    if '413' in l:
        n += 1; k += any(a in {f'{x:03d}' for x in range(31, 37)} or a == '700' for a in l)
print('413 lines (no lost sign):', n, 'with a tall count or cup in the same line:', k)
n = k = 0
for o in objs.values():
    for f in o['faces']:
        for l in f['lines']:
            if '413' in l:
                n += 1; k += any(a in {f'{x:03d}' for x in range(31, 37)} or a == '700' for a in l)
print('413 lines (all):', n, 'with tall count or cup:', k)
# 413-892 incl. broken lines
print('413 then 892 (all lines incl. broken):', sum(1 for o in objs.values() for f in o['faces'] for l in f['lines'] for i in range(len(l) - 1) if l[i] == '413' and l[i + 1] == '892'))
# texts of the 41 holding 705/706/435
T = json.load(open(f'{OUTDIR}/read.json'))
for s in ('705', '706', '435', '413', '060', '335'):
    print(s, 'in', [t['cisi'] or t['obj'] for t in T if any(s in p['signs'] for p in t['read'])])
