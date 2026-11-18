#!/usr/bin/env python3
"""COPPER step 2: one text, one picture?

Unit: one copper tablet with a legible picture of a kind of thing (species or motif). Two independent label sources:
  A = first catalogue, the lead's eye reading where looked at (an unclear 'quadruped' counts as no label), else the
      catalogue's own specific code; B = second catalogue field-symbol code fs80 (three digits, used as written).
Texts: the set text (damaged copies placed). TEXT FAMILY: texts that differ only by one sign in the same place or by
one sign added at the end are one family (706-033-923-740 and 706-033-923-740-001), merged by single linkage.

Measures: (1) among pairs of copies with the same text, share that carry the same picture; (2) number of texts with 2+
pictured copies that carry exactly one picture; (3) number of pictures (with 2+ copies) found with exactly one text
family. Control: picture labels dealt at random among the pictured copper tablets of the same catalogue, 10,000 deals.

Predictions written 2026-11-17 before the numbers:
 P2.1 Same-text pairs share the picture in more than 95% of pairs in both sources, against under 25% for random deals.
 P2.2 Every text with 2+ pictured copies has one picture (source A); source B shows at most one exception, a code
      sub-type split (145 against 147 on the stag set).
 P2.3 Pictures with 2+ copies sit with one text family in most cases; the exceptions are pictures used for several
      different texts (rhinoceros, composite beast), and those exceptions share a name sign (the rhinoceros texts share
      222 or 233, the composite texts share 585 or 597).
Writes work_data/copper/pairs_A.csv, pairs_B.csv, exceptions.csv, log_2.txt.
"""
import sys; sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from copper_common import *
say = say_to(f'{OUT}/log_2.txt')
L = pd.read_csv(f'{OUT}/objects.csv', dtype=str).fillna('')
Mm = pd.read_csv(f'{OUT}/m77_objects.csv', dtype=str).fillna('')
UNCLEAR = {'quadruped', ''}
A = L[(L.pic_src.isin(['eye', 'catalogue'])) & ~L.pic.isin(UNCLEAR)][['cisi', 'set_text', 'pic']].copy()
E = L[(L.pic_src == 'eye') & ~L.pic.isin(UNCLEAR)][['cisi', 'set_text', 'pic']].copy()
B = Mm[Mm.fs != ''][['textnum', 'set_text', 'fs']].rename(columns={'fs': 'pic'}).copy()

# ---- text families
texts = sorted(set(L.set_text) | set(Mm.set_text))
EQ = {frozenset(x) for x in (('405', '407'), ('705', '706'))}
def near(a, b):
    a, b = a.split('-'), b.split('-')
    if len(a) == len(b):
        diff = [(x, y) for x, y in zip(a, b) if x != y and '000' not in (x, y) and frozenset((x, y)) not in EQ]
        known = sum(1 for x, y in zip(a, b) if '000' not in (x, y))
        return len(diff) <= 1 and known >= 2
    if abs(len(a) - len(b)) == 1:
        s, l = (a, b) if len(a) < len(b) else (b, a)
        return l[:-1] == s or l[1:] == s
    return False
full_t = [t for t in texts if '000' not in t]
par = {t: t for t in full_t}
def find(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for a, b in itertools.combinations(full_t, 2):
    if near(a, b): par[find(a)] = find(b)
FAM = {t: find(t) for t in full_t}
for t in texts:                      # a damaged text joins a family only if it fits complete texts of exactly one family
    if t in FAM: continue
    hit = {FAM[f] for f in full_t if near(t, f)}
    FAM[t] = hit.pop() if len(hit) == 1 else t
fams = collections.defaultdict(list)
for t in texts: fams[FAM[t]].append(t)
pd.DataFrame([dict(family=k, texts=' | '.join(v)) for k, v in fams.items() if len(v) > 1]).to_csv(f'{OUT}/text_families.csv', index=False)
say('text families with 2+ texts:', sum(1 for v in fams.values() if len(v) > 1))

rng = np.random.default_rng(7)
def stats(T, P):
    by = collections.defaultdict(list)
    for t, p in zip(T, P): by[t].append(p)
    same = tot = 0; one = multi = 0
    for t, ps in by.items():
        if len(ps) < 2: continue
        c = collections.Counter(ps)
        same += sum(v * (v - 1) // 2 for v in c.values()); tot += len(ps) * (len(ps) - 1) // 2
        if len(c) == 1: one += 1
        else: multi += 1
    return same, tot, one, multi
def pic_side(T, P):
    by = collections.defaultdict(set); n = collections.Counter(P)
    for t, p in zip(T, P): by[p].add(FAM[t])
    k = [p for p in by if n[p] >= 2]
    return sum(1 for p in k if len(by[p]) == 1), len(k)

for nm, D in (('E eye only (photos read by the lead)', E), ('A first catalogue (eye + specific code)', A), ('B second catalogue code', B)):
    T, P = list(D.set_text), list(D.pic)
    s, tot, one, multi = stats(T, P); p1, k = pic_side(T, P)
    sims = []; sims2 = []
    for _ in range(10000):
        Q = list(rng.permutation(P)); ss, tt, o, m = stats(T, Q); sims.append((ss / tt if tt else 0, o)); sims2.append(pic_side(T, Q)[0])
    sims = np.array(sims); sims2 = np.array(sims2)
    say(f'[{nm}] tablets {len(D)}; texts with 2+ pictured copies {one + multi}')
    say(f'   same-text pairs with the same picture: {s} of {tot} = {s / tot:.3f}; random deals mean {sims[:, 0].mean():.3f}, '
        f'max {sims[:, 0].max():.3f}; P {np.mean(sims[:, 0] >= s / tot):.4f}')
    say(f'   texts with exactly one picture: {one} of {one + multi}; random mean {sims[:, 1].mean():.2f}, P {np.mean(sims[:, 1] >= one):.4f}')
    say(f'   pictures (2+ tablets) with one text family: {p1} of {k}; random mean {sims2.mean():.2f}, P {np.mean(sims2 >= p1):.4f}')
    D.to_csv(f'{OUT}/pairs_{nm[0]}.csv', index=False)

# ---- exceptions
rows = []
for nm, D in (('E', E), ('A', A), ('B', B)):
    for t, g in D.groupby('set_text'):
        c = collections.Counter(g.pic)
        if len(c) > 1: rows.append(dict(source=nm, kind='text with two pictures', key=t, detail=dict(c)))
    for p, g in D.groupby('pic'):
        f = collections.Counter(FAM[t] for t in g.set_text)
        if len(f) > 1: rows.append(dict(source=nm, kind='picture with two text families', key=p,
                                        detail={k: dict(collections.Counter(x for x in g.set_text if FAM[x] == k)) for k in f}))
X = pd.DataFrame(rows); X.to_csv(f'{OUT}/exceptions.csv', index=False)
for r in X.itertuples(): say(f'   EXC [{r.source}] {r.kind}: {r.key} -> {r.detail}')
