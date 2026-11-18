#!/usr/bin/env python3
"""COPPER step 5: sign swaps between copies of one copper text.

SWAP: two complete copper texts of the same length in one text family (copper_2_pairs.py) that differ in exactly one
place; the two signs in that place are a swap pair. Counted in the first catalogue (copies each way) and, apart, in
the second catalogue's own readings (copies each way, its own transcription mapped to first-catalogue numbers).
DRAWN ALIKE: the two signs share one shape description in work_data/sign_shapes.csv, or the second catalogue maps both
to one of its signs (work_data/lipi_mahadevan_crosswalk.csv rank 1). Otherwise DRAWN DIFFERENTLY.
SHARED NEIGHBOURS: over the whole first catalogue (distinct complete texts, every object kind), the set of
(left sign, right sign) frames each sign stands in; overlap = frames in common / smaller frame set. Control: each
sign of the pair replaced by a sign of about the same use count (within 30%), 5,000 draws.

Predictions written 2026-11-17 before the numbers:
 P5.1 The known swaps reappear (421/422/423/424, 904/905, 407/408, 231/220, 705/706, 744/747 or 760/717) and at least
      one new pair turns up.
 P5.2 Half or more of the pairs are drawn alike (one sign written two ways).
 P5.3 The drawn-differently pairs share frames elsewhere in the corpus at least twice as often as matched random pairs.
Writes work_data/copper/swaps.csv and log_5.txt.
"""
import sys; sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from copper_common import *
say = say_to(f'{OUT}/log_5.txt')
L = pd.read_csv(f'{OUT}/objects.csv', dtype=str).fillna('')
Mm = pd.read_csv(f'{OUT}/m77_objects.csv', dtype=str).fillna('')
exec(open(f'{ROOT}/work_scripts/copper_2_pairs.py').read().split('# ---- text families')[1].split('rng = np.random')[0])
SH = pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv', dtype=str).fillna('')
DESC = dict(zip(SH.lipi_wells_number, SH.shape_description))
CW = pd.read_csv(f'{ROOT}/work_data/lipi_mahadevan_crosswalk.csv', dtype=str).fillna('')
MAH = dict(zip(CW[CW.rank_for_lipi_sign == '1'].lipi, CW[CW.rank_for_lipi_sign == '1'].mahadevan))

def swaps(D):
    out = collections.Counter(); ex = collections.defaultdict(set)
    vc = D[~D.text.str.contains('000') & ~D.text.str.contains('X') & ~D.text.str.contains('ALT')].text.value_counts()
    for a, b in itertools.combinations(vc.index, 2):
        x, y = a.split('-'), b.split('-')
        if (FAM.get(a) is None or FAM.get(a) != FAM.get(b)) and min(len(x), len(y)) < 4: continue
        # one sign replaced by one sign, plus at most one sign added or dropped elsewhere (redesign: the buffalo and goat
        # copies swap a sign and also add a number stroke or a closing sign)
        import difflib
        ops = [o for o in difflib.SequenceMatcher(None, x, y, autojunk=False).get_opcodes() if o[0] != 'equal']
        rep = [o for o in ops if o[0] == 'replace' and o[2] - o[1] == 1 and o[4] - o[3] == 1]
        indel = [o for o in ops if o[0] in ('insert', 'delete') and max(o[2] - o[1], o[4] - o[3]) == 1]
        if len(rep) != 1 or len(ops) != len(rep) + len(indel) or len(indel) > 1: continue
        p, q = x[rep[0][1]], y[rep[0][3]]; key = tuple(sorted((p, q)))
        n = {p: vc[a], q: vc[b]}
        out[key] += 0; ex[key].add(f'{a} ({vc[a]}) ~ {b} ({vc[b]})')
        out[key] = out[key]
    return ex, vc
exL, vcL = swaps(L)
exM, vcM = swaps(Mm)
pairs = sorted(set(exL) | set(exM))

# frames in the whole first catalogue
ob = objs
seen = set(); frames = collections.defaultdict(set); use = collections.Counter()
for o in ob.itertuples():
    for f in o.faces:
        f = tuple(f)
        if f in seen or '000' in f: continue
        seen.add(f); t = ('^',) + f + ('$',)
        for i in range(1, len(t) - 1):
            frames[t[i]].add((t[i - 1], t[i + 1])); use[t[i]] += 1
def ov(a, b):
    A, B = frames[a], frames[b]
    return len(A & B) / min(len(A), len(B)) if A and B else 0.0
signs = [s for s in use if use[s] >= 1]
rng = np.random.default_rng(5)
def matched(s):
    n = use[s]; c = [x for x in signs if abs(use[x] - n) <= max(1, 0.3 * n) and x != s]
    return c
rows = []
for p, q in pairs:
    alike = (DESC.get(p) and DESC.get(p) == DESC.get(q)) or (MAH.get(p) and MAH.get(p) == MAH.get(q))
    o = ov(p, q); cp, cq = matched(p), matched(q)
    sims = np.array([ov(cp[rng.integers(len(cp))], cq[rng.integers(len(cq))]) for _ in range(5000)]) if cp and cq else np.array([0.0])
    rows.append(dict(a=p, b=q, drawn='alike' if alike else 'differently', shape_a=DESC.get(p, '')[:60], shape_b=DESC.get(q, '')[:60],
                     second_cat_a=MAH.get(p, ''), second_cat_b=MAH.get(q, ''), uses_a=use[p], uses_b=use[q],
                     in_first=' ; '.join(sorted(exL.get((p, q), []))), in_second=' ; '.join(sorted(exM.get((p, q), []))),
                     frame_overlap=round(o, 3), random_mean=round(sims.mean(), 3), P=round(float(np.mean(sims >= o)), 4)))
X = pd.DataFrame(rows); X.to_csv(f'{OUT}/swaps.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 90)
say('swap pairs:\n' + X[['a', 'b', 'drawn', 'uses_a', 'uses_b', 'frame_overlap', 'random_mean', 'P']].to_string(index=False))
for r in X.itertuples(): say(f'  {r.a}/{r.b}: first catalogue [{r.in_first}] second [{r.in_second}]')
dd = X[X.drawn == 'differently']
say(f'P5.2 drawn alike {(X.drawn == "alike").sum()} of {len(X)}')
if len(dd):
    say(f'P5.3 drawn differently: mean frame overlap {dd.frame_overlap.mean():.3f} against matched random {dd.random_mean.mean():.3f}; '
        f'pairs above their own random at P<=0.05: {(dd.P <= 0.05).sum()} of {len(dd)}')
