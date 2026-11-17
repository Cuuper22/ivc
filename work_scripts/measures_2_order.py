#!/usr/bin/env python3
"""Step 2: lines (faces) with two or more measure signs. Is the order fixed, big unit before small?

PREDICTIONS (written before the first run).
 O1 Tamil sizes: kōṭṭai 575 (21 marakkāl) > kalam 705/706 (12) > paṟai 540 (? placed by the data) > bin 335 / pot 711
    (containers) > cup 700 (1 marakkāl) > paṭi 320 (1/8) > kāl 061 (a quarter). On a line the bigger unit comes
    first in reading order in 80%+ of ordered pairs (accounting scripts write big to small).
 O2 Each pair that meets 3+ times keeps one order in 80%+ of its meetings; chance for a pair is 50/50 (binomial).
 O3 The ladder built from the orders alone (rank by wins) matches the Tamil size order above.
Jar 740 is left out of the ladder (it closes most texts as "house of"), hand 817/861 too (opener); both are
reported in a side table.
"""
from measures_common import *

LADDER_UNITS = {'575': 'kotTai', '705': 'kalam', '706': 'kalam', '704': 'kalam', '540': 'paRai', '335': 'bin',
                '711': 'pot', '605': 'granary-bin', '590': 'chest', '700': 'cup', '703': 'cup', '320': 'paTi',
                '061': 'kAl', '063': 'kAl', '171': 'niRai', '055': 'dozen', '048': 'seven', '413': 'grain(header)'}
TAMIL_RANK = {'kotTai': 1, 'kalam': 2, 'cup': 5, 'paTi': 6, 'kAl': 7}

def pairs_of(flist, units):
    pc = collections.Counter(); ex = collections.defaultdict(list)
    for f in flist:
        t = f['tok']; pos = [(i, units[s]) for i, s in enumerate(t) if s in units]
        seen = set()
        for (i, a), (j, b) in itertools.combinations(pos, 2):
            if a == b: continue
            key = (a, b)
            if (key, f['cisi']) in seen: continue
            seen.add((key, f['cisi'])); pc[key] += 1; ex[key].append(f"{f['cisi']}: {' '.join(t)}")
    return pc, ex

F = faces('L') + faces('Mu')
DISTINCT = len(sys.argv) > 1 and sys.argv[1] == 'distinct'
if DISTINCT:   # each different sign string once (copies of one chit count once)
    _s = set(); F2 = []
    for f in F:
        if f['tok'] in _s: continue
        _s.add(f['tok']); F2.append(f)
    F = F2
    print('DISTINCT TEXTS ONLY')
pc, ex = pairs_of(F, LADDER_UNITS)
names = sorted({u for k in pc for u in k})
rows = []
for a, b in itertools.combinations(names, 2):
    ab, ba = pc[(a, b)], pc[(b, a)]
    if ab + ba == 0: continue
    p = binomtest(max(ab, ba), ab + ba, 0.5).pvalue
    first = a if ab >= ba else b
    rows.append(dict(pair=f'{a}/{b}', a_first=ab, b_first=ba, n=ab + ba, usual_first=first,
                     share=round(max(ab, ba) / (ab + ba), 2), P=round(p, 4),
                     example=(ex[(a, b)] or ex[(b, a)])[0][:90]))
R = pd.DataFrame(rows).sort_values('n', ascending=False)
R.to_csv(f'{OUTM}/order_pairs' + ('_distinct' if DISTINCT else '') + '.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 90)
print(R.to_string(index=False))

# O2 overall
big = R[R.n >= 3]
print(f'\nO2 pairs meeting 3+ times: {len(big)}; keep one order 80%+: {(big.share >= 0.8).sum()}')
tot = R.n.sum(); kept = (R[['a_first', 'b_first']].max(axis=1)).sum()
print(f'All ordered meetings: {kept} of {tot} follow the usual order of their pair ({kept / tot:.0%})')

# order-only ladder: rank by (wins - losses) / meetings, wins = this unit first
score = collections.defaultdict(lambda: [0, 0])
for (a, b), n in pc.items():
    score[a][0] += n; score[b][1] += n
lad = sorted(score, key=lambda u: -(score[u][0] - score[u][1]) / (score[u][0] + score[u][1]))
print('\nO3 ladder from order alone (first = written first):')
for u in lad:
    w, l = score[u]; print(f'  {u:14s} first {w:3d}  second {l:3d}  net {(w - l) / (w + l):+.2f}')

# O1: Tamil pairs only
k = n = 0
for (a, b), c in pc.items():
    if a in TAMIL_RANK and b in TAMIL_RANK:
        n += c; k += c * (TAMIL_RANK[a] < TAMIL_RANK[b])
print(f'\nO1 Tamil-ranked pairs: bigger first {k} of {n}' + (f' ({k / n:.0%}), P {binomtest(k, n, 0.5).pvalue:.3g}' if n else ''))

# shuffle control: permute the unit signs' order inside each line, how often is the total kept share this high?
rng = np.random.default_rng(1)
lines = [[LADDER_UNITS[s] for s in f['tok'] if s in LADDER_UNITS] for f in F]
lines = [l for l in lines if len(set(l)) >= 2]
def kept_share(L):
    c = collections.Counter()
    for l in L:
        for x, y in itertools.combinations(l, 2):
            if x != y: c[(x, y)] += 1
    tot = sum(c.values()); kp = sum(max(c[(x, y)], c[(y, x)]) for (x, y) in {tuple(sorted(k)) for k in c})
    return kp / tot
obs = kept_share(lines)
sims = [kept_share([list(rng.permutation(l)) for l in lines]) for _ in range(500)]
print(f'shuffle control: kept share {obs:.3f} against {np.mean(sims):.3f} +- {np.std(sims):.3f}; '
      f'P {(np.sum(np.array(sims) >= obs) + 1) / 501:.3g} (lines with 2+ different units: {len(lines)})')

# side table: with jar and hand
SIDE = dict(LADDER_UNITS); SIDE.update({'740': 'jar', '817': 'hand', '861': 'hand'})
pc2, _ = pairs_of(F, SIDE)
print('\nSide table (jar, hand):')
for u in ('jar', 'hand'):
    for v in sorted({b for (a, b) in pc2 if a == u} | {a for (a, b) in pc2 if b == u}):
        if v in ('jar', 'hand') and v == u: continue
        print(f'  {u} before {v}: {pc2[(u, v)]}   {v} before {u}: {pc2[(v, u)]}')
