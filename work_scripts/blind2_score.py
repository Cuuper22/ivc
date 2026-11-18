#!/usr/bin/env python3
"""Scores the side-by-side (forced choice) test.

Usage: python3 blind2_score.py grades_A.csv grades_B.csv grades_C.csv     (each: item,best,worst,reason; paths, or names inside work_data/blind2/)
Reads work_data/blind2/choice_set.csv and KEY_do_not_open.csv.

What is counted (identical lines handled fairly): an option "is the real line" if its English text equals the real line's text. So if a scramble
came out identical to the real line, picking it counts as picking the real line, and that item's chance of a real pick is (number of options with
the real text) / 4 instead of 1/4. Chance for the whole set is the sum over items; the exact P comes from the exact distribution of the number of
real picks when each item i is an independent pick with chance c_i (Poisson-binomial, computed exactly).
For each reader and for all readers pooled it prints:
  real picked BEST  : share of items where the reader's best line was the real line. Chance is about 25%. Above chance means the real word list
                      reads more like a real label than the scrambles; P is one-sided (probability of this many or more real picks by luck).
  real picked WORST : share where the reader's worst line was the real line. Below chance means readers rarely thought the real line the worst.
  split by object kind (seal / tablet / the rest together).
  who got picked best: real, S1 (free shuffle), S2 and S2b (two independent same-job shuffles). Chance is 25% each (a bit different with identical lines).
    S2 against S2b tells how big the luck of one same-job shuffle is; real above both is the comparison that matters.
  agreement: share of items where two readers chose the same best letter (chance about 25%), and share of items where at least two readers
    picked the real line (and where all picked it)."""
import csv, sys, os, itertools, collections
D = '/home/antigravity/Cuuper22/ivc/work_data/blind2'
LET = 'abcd'

def pb_tail(ps, k):
    """exact P(X >= k) and P(X <= k) for X = sum of independent Bernoulli(ps)"""
    dist = [1.0]
    for p in ps:
        nd = [0.0] * (len(dist) + 1)
        for i, v in enumerate(dist): nd[i] += v * (1 - p); nd[i + 1] += v * p
        dist = nd
    return sum(dist[k:]), sum(dist[:k + 1])
def pct(a, n): return f'{100 * a / n:5.1f}%' if n else '  n/a'

choice = {r['item']: r for r in csv.DictReader(open(f'{D}/choice_set.csv', newline=''))}
key = {r['item']: r for r in csv.DictReader(open(f'{D}/KEY_do_not_open.csv', newline=''))}
TYPES = {'real': 'real_option', 'S1': 'S1_option', 'S2': 'S2_option', 'S2b': 'S2b_option'}
def text(item, letter): return choice[item]['option_' + letter]
def real_letters(item):
    rt = text(item, key[item]['real_option'])
    return [l for l in LET if text(item, l) == rt]
def kind_group(item):
    k = key[item]['object kind']; return k if k in ('seal', 'tablet') else 'rest (tags, pots, copper tablets, other)'

readers = {}
for path in sys.argv[1:]:
    p = path if os.path.exists(path) else f'{D}/{path}'
    g = {}
    for r in csv.DictReader(open(p, newline='')):
        it = r['item'].strip(); b = r['best'].strip().lower(); w = r['worst'].strip().lower()
        if it not in choice: sys.exit(f'{path}: item {it} is not in the choice set')
        if b not in LET or w not in LET: sys.exit(f'{path}: item {it}: best/worst must be one of a, b, c, d (got {b!r}, {w!r})')
        g[it] = (b, w)
    miss = [i for i in choice if i not in g]
    if miss: print(f'WARNING {path}: {len(miss)} items have no grade: {miss[:10]}')
    readers[os.path.basename(path)] = g
if not readers: sys.exit('give at least one grades file')

def report(name, g, items):
    items = [i for i in items if i in g]
    if not items: return
    ps = [len(real_letters(i)) / 4 for i in items]
    n = len(items)
    hits = sum(g[i][0] in real_letters(i) for i in items)
    wh = sum(g[i][1] in real_letters(i) for i in items)
    ex = sum(ps)
    p1, _ = pb_tail(ps, hits)
    _, pw = pb_tail(ps, wh)
    print(f'  {name:42s} items {n:3d} | real BEST {hits:3d} = {pct(hits, n)} (chance {100 * ex / n:4.1f}%, one-sided P {p1:.4g}) | real WORST {wh:3d} = {pct(wh, n)} (chance {100 * ex / n:4.1f}%, P(this few or fewer) {pw:.4g})')
def best_types(g, items):
    c = collections.Counter(); n = 0
    for i in items:
        if i not in g: continue
        b = g[i][0]; n += 1
        if b in real_letters(i): c['real'] += 1; continue
        for t in ('S1', 'S2', 'S2b'):
            if key[i][TYPES[t]] == b: c[t] += 1
    return c, n

allitems = list(choice)
print('MEANING: "real BEST" = how often the reader called the real line the most label-like one; chance is about 25% (more where scrambles equal the real line).')
print('         "real WORST" = how often the reader called the real line the worst; chance is the same ~25%; low is good for the real list.\n')
for name, g in readers.items():
    print(f'READER {name}')
    report('all items', g, allitems)
    for kg in ('seal', 'tablet', 'rest (tags, pots, copper tablets, other)'):
        report(kg, g, [i for i in allitems if kind_group(i) == kg])
    c, n = best_types(g, allitems)
    print('  who was picked best (share of items): ' + ', '.join(f'{t} {c[t]} = {pct(c[t], n)}' for t in ('real', 'S1', 'S2', 'S2b')) + '   (chance 25% each)')
    print()

if len(readers) > 1:
    print('ALL READERS POOLED (each reader-item is one pick; picks of one item by different readers are not independent, so the P is a guide)')
    ps = []; hits = wh = 0; n = 0; c = collections.Counter()
    for g in readers.values():
        for i in allitems:
            if i not in g: continue
            ps.append(len(real_letters(i)) / 4); n += 1
            hits += g[i][0] in real_letters(i); wh += g[i][1] in real_letters(i)
        cc, _ = best_types(g, allitems); c.update(cc)
    p1, _ = pb_tail(ps, hits); _, pw = pb_tail(ps, wh)
    print(f'  real BEST {hits} of {n} = {pct(hits, n)} (chance {100 * sum(ps) / n:.1f}%, one-sided P {p1:.4g}); real WORST {wh} of {n} = {pct(wh, n)} (P(this few or fewer) {pw:.4g})')
    print('  who was picked best: ' + ', '.join(f'{t} {c[t]} = {pct(c[t], n)}' for t in ('real', 'S1', 'S2', 'S2b')))
    for kg in ('seal', 'tablet', 'rest (tags, pots, copper tablets, other)'):
        its = [i for i in allitems if kind_group(i) == kg]; ps = []; h = w_ = m = 0
        for g in readers.values():
            for i in its:
                if i in g: ps.append(len(real_letters(i)) / 4); m += 1; h += g[i][0] in real_letters(i); w_ += g[i][1] in real_letters(i)
        p1, _ = pb_tail(ps, h)
        print(f'  {kg:42s} reader-items {m:3d} | real BEST {pct(h, m)} (P {p1:.4g}) | real WORST {pct(w_, m)}')
    print('\nAGREEMENT (items graded by both readers). "same best" = both chose the same letter, chance about 25%.')
    for (a, ga), (b, gb) in itertools.combinations(readers.items(), 2):
        its = [i for i in allitems if i in ga and i in gb]
        same = sum(ga[i][0] == gb[i][0] for i in its)
        both_real = sum(ga[i][0] in real_letters(i) and gb[i][0] in real_letters(i) for i in its)
        print(f'  {a} vs {b}: same best {same} of {len(its)} = {pct(same, len(its))}; both picked the real line {both_real}')
    its = [i for i in allitems if all(i in g for g in readers.values())]
    k = len(readers)
    cnt = [sum(g[i][0] in real_letters(i) for g in readers.values()) for i in its]
    print(f'  items where at least two of {k} readers picked the real line: {sum(x >= 2 for x in cnt)} of {len(its)} = {pct(sum(x >= 2 for x in cnt), len(its))}; all {k} picked it: {sum(x == k for x in cnt)}; none: {sum(x == 0 for x in cnt)}')
    # chance for "at least two" under independent picks with the per-item chance
    ex = 0.0
    for i in its:
        p = len(real_letters(i)) / 4
        from math import comb
        ex += sum(comb(k, j) * p ** j * (1 - p) ** (k - j) for j in range(2, k + 1))
    print(f'    expected by luck for "at least two": {ex:.1f} items = {pct(ex, len(its))}')
