#!/usr/bin/env python3
"""Step 3 rescue: the raw sum test went against (10 of 70 against 14.9 shuffled). Two different tries.

PREDICTIONS (written before the first run).
 R1 (better test) Seals hold names with numbers in them, which are not accounts. Restrict to account objects
    (miniature tablets, copper tablets, tags, pots) and to numbers standing by a measure unit or a counted good.
    On two-number account objects the two numbers are EQUAL (one line per crew member / per load) or in the ladder
    ratio more often than shuffled between objects.
 R2 (new idea) Batches of copies: tablets sharing one front text but carrying different cup counts. If cups are
    shares of a kalam (12), the cups written across one batch add up to a whole number of kalam (multiple of 12)
    more often than the 1-in-12 chance; or to 4 (a tūṇi) / 6 (half kalam).
"""
from measures_common import *
from measures_3_sums import obj_numbers, sum_hit
import contextlib, io

ACC = {'mtab', 'ctab', 'tag', 'pot'}
on = {}
on.update(obj_numbers('L')); on.update(obj_numbers('Mu'))
two = {k: v for k, v in on.items() if len(v) == 2 and k[2] in ACC and k[0] not in ('-', '')}
pairs = [(v[0]['value'], v[1]['value']) for v in two.values()]
eq = sum(a == b for a, b in pairs)
rng = np.random.default_rng(3); pool = [x for p in pairs for x in p]
sims = []
for _ in range(5000):
    s = rng.permutation(pool); sims.append(sum(s[2 * i] == s[2 * i + 1] for i in range(len(pairs))))
sims = np.array(sims)
print(f'R1 two-number account objects: {len(pairs)}; equal {eq} against {sims.mean():.1f} shuffled; P {(np.sum(sims >= eq) + 1) / 5001:.3g}')
eqrows = collections.Counter()
for k, v in two.items():
    if v[0]['value'] == v[1]['value']:
        eqrows[(v[0]['value'], v[0]['unit'], v[1]['unit'])] += 1
for (val, u1, u2), n in eqrows.most_common(15): print(f'   equal {val}: {u1} / {u2}  x{n}')
three = {k: v for k, v in on.items() if len(v) >= 3 and k[2] in ACC and k[0] not in ('-', '')}
print('R1b account objects with 3+ numbers:', len(three), ' sum relation:', sum(sum_hit([r['value'] for r in v]) is not None for v in three.values()))

# R2: batches = Lipi tablets whose non-cup faces are identical text, carrying a cup count
fr = collections.defaultdict(list)
for cisi, g in d[d.kind == 'mtab'].groupby('cisi'):
    if cisi in ('-', ''): continue
    cups = []; front = []
    for t in g.tok:
        R = [r for r in runs(t) if r[1] < len(t) and t[r[1]] == '700' and r[2]]
        if R: cups.append(R[0][2])
        else: front.append(' '.join(t))
    if len(cups) == 1 and front:
        fr[' | '.join(sorted(front))].append((cisi, cups[0], g['area-section'].iloc[0]))
rows = []
for f, L in fr.items():
    if len(L) < 3: continue
    tot = sum(c for _, c, _ in L)
    rows.append(dict(front=f, n=len(L), cups=' '.join(str(c) for _, c, _ in L), total=tot, mod12=tot % 12,
                     areas=' '.join(sorted({a for *_, a in L}))))
B = pd.DataFrame(rows).sort_values('n', ascending=False); B.to_csv(f'{OUTM}/batch_totals.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 60)
print('\nR2 batches (same front, 3+ tablets):'); print(B.to_string(index=False))
k = int((B.mod12 == 0).sum()); n = len(B)
if n: print(f'R2 batch totals that are whole kalam (multiple of 12): {k} of {n}; chance 1/12 -> P {binomtest(k, n, 1 / 12, alternative="greater").pvalue:.3g}')
