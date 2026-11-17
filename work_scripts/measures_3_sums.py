#!/usr/bin/env python3
"""Step 3: do the numbers on one object add up?

Object = every face of one Lipi object (same cisi), or every line of one second-catalogue text. For each object we
list each number run with the unit it stands by (the sign after a count-first run, the sign before a count-after
run; units from measures_common.UNITS, else the neighbour sign itself).

PREDICTIONS (written before the first run).
 S1 Raw sums: on objects with 3+ numbers, one number equals the sum of the others more often than when the
    numbers are shuffled between objects of the same size (a total line exists).
 S2 Under the ladder (kalam = 12 cups, kōṭṭai = 21 cups, paṭi = 1/8 cup, kāl = 1/4), objects that mix units
    give a total in cup units on one face (sum of the others) at least once.
 S3 The 22 ration tablets (3 hands | 3 loads | 4 cups): 4 cups is not a sum of 3 and 3; it is a fixed issue for
    the crew. Predicted: the per-head amount 4/3 cup is NOT a whole number of paṭi (32/3), so the issue is per
    crew, not per head; the 4 cups = 1 tūṇi (Tamil 4 marakkāl) is the issued unit.
 S4 Product relation: a number on one face equals the product of two others (crew x ration) more than shuffled.
"""
from measures_common import *

TO_CUP = {'cup': 1, 'kalam': 12, 'kotTai': 21, 'paTi': 1 / 8, 'kAl': 1 / 4}

def obj_numbers(cat):
    out = collections.defaultdict(list)
    for f in faces(cat):
        t = f['tok']
        for (a, b, v, ser) in runs(t):
            if v is None: continue
            left = t[a - 1] if a > 0 else 'START'; right = t[b] if b < len(t) else 'END'
            # pick the owner: a unit sign if one is adjacent, else the right-hand sign (count-first default)
            if right in UNITS: own, side = right, 'n X'
            elif left in UNITS: own, side = left, 'X n'
            else: own, side = right, 'n X'
            out[(f['cisi'], f['site'], f['kind'])].append(dict(face=f['fid'], value=v, series=ser, owner=own,
                                                                unit=UNIT_OF.get(own, own), text=' '.join(t)))
    return out

objs_n = {}
objs_n.update(obj_numbers('L')); objs_n.update(obj_numbers('Mu'))
multi = {k: v for k, v in objs_n.items() if len(v) >= 2 and k[0] not in ('-', '')}
print('objects with 2+ numbers:', len(multi), ' with 3+:', sum(len(v) >= 3 for v in multi.values()))

def sum_hit(vals):
    for i, x in enumerate(vals):
        rest = vals[:i] + vals[i + 1:]
        if len(rest) >= 2 and abs(x - sum(rest)) < 1e-9: return i
    return None

def prod_hit(vals):
    for i, x in enumerate(vals):
        rest = vals[:i] + vals[i + 1:]
        for a, b in itertools.combinations(rest, 2):
            if abs(x - a * b) < 1e-9 and a > 1 and b > 1: return i
    return None

three = {k: v for k, v in multi.items() if len(v) >= 3}
hits = []
for k, v in three.items():
    vals = [r['value'] for r in v]
    i = sum_hit(vals)
    if i is not None: hits.append((k, v, i, 'sum'))
    j = prod_hit(vals)
    if j is not None: hits.append((k, v, j, 'product'))
nsum = sum(h[3] == 'sum' for h in hits); nprod = sum(h[3] == 'product' for h in hits)
# shuffle control: draw values from the pool of all values on 3+ objects, keep object sizes
pool = [r['value'] for v in three.values() for r in v]
rng = np.random.default_rng(2); ss = []; sp = []
for _ in range(2000):
    s = p = 0
    for v in three.values():
        vals = list(rng.choice(pool, len(v)))
        s += sum_hit(vals) is not None; p += prod_hit(vals) is not None
    ss.append(s); sp.append(p)
ss, sp = np.array(ss), np.array(sp)
print(f'S1 raw sum relation on 3+ objects: {nsum} of {len(three)} against {ss.mean():.1f} shuffled; P {(np.sum(ss >= nsum) + 1) / 2001:.3g}')
print(f'S4 product relation: {nprod} of {len(three)} against {sp.mean():.1f} shuffled; P {(np.sum(sp >= nprod) + 1) / 2001:.3g}')

rows = []
for k, v, i, kind in hits:
    rows.append(dict(obj=k[0], site=k[1], kind=k[2], relation=kind, total=f"{v[i]['value']} {v[i]['unit']}",
                     parts=' + '.join(f"{r['value']} {r['unit']}" for j, r in enumerate(v) if j != i) if kind == 'sum'
                     else ' x '.join(f"{r['value']} {r['unit']}" for j, r in enumerate(v) if j != i),
                     faces=' | '.join(dict.fromkeys(r['text'] for r in v))))
H = pd.DataFrame(rows); H.to_csv(f'{OUTM}/sum_hits.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 80); pd.set_option('display.max_rows', 200)
print(H.groupby(['relation', 'total', 'parts']).agg(n=('obj', 'size'), example=('obj', 'first'), faces=('faces', 'first')).reset_index().to_string(index=False))

# S2 converted sums for mixed-unit objects
print('\nS2 mixed-unit objects (2+ ladder units):')
conv = 0
for k, v in multi.items():
    us = {r['unit'] for r in v if r['unit'] in TO_CUP}
    if len(us) < 2: continue
    cv = [r['value'] * TO_CUP[r['unit']] for r in v if r['unit'] in TO_CUP]
    i = sum_hit(cv)
    print(' ', k[0], k[1], [(r['value'], r['unit']) for r in v], 'in cups', cv, '-> total' if i is not None else '')
    conv += i is not None
print('converted sums found:', conv)

# all two-number objects: equal / one double / one = other + 1 (diagnostic table)
rel = collections.Counter()
for k, v in multi.items():
    if len(v) != 2: continue
    a, b = sorted(r['value'] for r in v)
    rel['equal' if a == b else 'double' if b == 2 * a else 'other'] += 1
print('\ntwo-number objects:', dict(rel))
pd.DataFrame([dict(obj=k[0], site=k[1], kind=k[2], numbers=' ; '.join(f"{r['value']} {r['unit']}({r['series']})" for r in v),
                   faces=' | '.join(dict.fromkeys(r['text'] for r in v))) for k, v in multi.items()]).to_csv(
    f'{OUTM}/multi_number_objects.csv', index=False)
