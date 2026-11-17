#!/usr/bin/env python3
"""ROUND SEALS, step 2: structure inside the round texts, against shuffles and matched square seals. Written 2026-11-17.
No word on any sign. ROUND SET = the 41 round faces (39 objects; two objects have two faces); texts with 2+ tokens enter the pattern tests.
A token that is a lost sign (000), unclear (ALT) or never-seen sign counts as a GAP: it breaks adjacency.
PERSON = 090 091 093 095 (person pictures). STROKE = the stroke sign set used in abroad4_09 (all counting-stroke classes + 001-005, 031-033, 055, 013).
THREE PATTERNS FIXED BEFORE ANY COUNT (reading order, adjacent signs only):
  A "tally of persons": [person][stroke][anything or end]  -> person at i, stroke at i+1.
  B "X's man":          [sign that is neither person nor stroke][person] with the person as the LAST token of the text.
  C "n persons":        [stroke][person] adjacent anywhere (number first, person second).
PREDICTIONS (written now): the round seals are lists of people with counts, so A or C holds in at least 5 round texts against at most 1.5
in length-matched square seals; B holds in 3 or more (a person ending the text). No first, last or middle sign is shared beyond shuffles
(the earlier job found no shared runs). The man 090 sits mostly at the end or the front, the strokes next to it.
CONTROLS: (1) matched square seals: for each round text a home square-seal distinct text with the same token count, 2,000 draws;
(2) shuffle: signs of each round text rearranged within the text, 5,000 shuffles (gaps move with the signs).
Output: work_data/round/structure_patterns.csv, structure_share.csv, structure_positions.csv, log_2.txt
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abroad4_common import *
OUTR = f'{ROOT}/work_data/round'
PERSON = {'090', '091', '093', '095'}
STROKES = {s for s in GV if V2CLASS.get(s) in ('NUM_SHORT', 'NUM_TALL', 'NUM_NAME')} | {'001', '002', '003', '004', '005', '031', '032', '033', '055', '013'}
RL = pd.read_csv(f'{OUTR}/round_list.csv', dtype=str)
RT = {r.id: tuple(d.set_index('id').loc[r.id, 'tok']) for r in RL.itertuples()}
def u(s): return s if (real(s) and s in GIDX) else None
def cls(tok): return [u(s) for s in tok]
def pat_A(t):
    t = cls(t); return any(a in PERSON and b in STROKES for a, b in zip(t, t[1:]) if a and b)
def pat_B(t):
    t = cls(t)
    return len(t) >= 2 and t[-1] in PERSON and t[-2] is not None and t[-2] not in PERSON and t[-2] not in STROKES
def pat_C(t):
    t = cls(t); return any(a in STROKES and b in PERSON for a, b in zip(t, t[1:]) if a and b)
PATS = {'A [person][stroke]': pat_A, 'B [other][person] at end': pat_B, 'C [stroke][person]': pat_C}
rt = [t for t in RT.values() if len(t) >= 2]
# matched square pool: home square-seal distinct texts by token count
sq = F[(F.tier == 'home') & (F.kind == 'seal') & (~F['round'])]
pool = collections.defaultdict(list)
for x in set(sq.tok):
    if len(x) >= 2: pool[len(x)].append(x)
rng = np.random.default_rng(2026)
def draw():
    return [pool[min(max(len(t), 2), max(pool))][rng.integers(len(pool[min(max(len(t), 2), max(pool))]))] for t in rt]
real_c = {k: sum(f(t) for t in rt) for k, f in PATS.items()}
real_any = sum(any(f(t) for f in PATS.values()) for t in rt)
rows = []
sqd = {k: [] for k in PATS}; sqany = []
for _ in range(2000):
    D = draw()
    for k, f in PATS.items(): sqd[k].append(sum(f(t) for t in D))
    sqany.append(sum(any(f(t) for f in PATS.values()) for t in D))
shd = {k: [] for k in PATS}; shany = []
for _ in range(5000):
    S = [tuple(rng.permutation(np.array(t, dtype=object))) for t in rt]
    for k, f in PATS.items(): shd[k].append(sum(f(t) for t in S))
    shany.append(sum(any(f(t) for f in PATS.values()) for t in S))
def p_hi(v, arr): arr = np.array(arr); return (np.sum(arr >= v) + 1) / (len(arr) + 1)
for k in PATS:
    rows.append(dict(pattern=k, texts=len(rt), round_real=real_c[k], square_matched_mean=np.mean(sqd[k]), P_vs_square=p_hi(real_c[k], sqd[k]), shuffled_mean=np.mean(shd[k]), P_vs_shuffle=p_hi(real_c[k], shd[k])))
rows.append(dict(pattern='any of A B C', texts=len(rt), round_real=real_any, square_matched_mean=np.mean(sqany), P_vs_square=p_hi(real_any, sqany), shuffled_mean=np.mean(shany), P_vs_shuffle=p_hi(real_any, shany)))
P = pd.DataFrame(rows); P.to_csv(f'{OUTR}/structure_patterns.csv', index=False); print(P.to_string())
print('texts fitting each pattern:')
for k, f in PATS.items(): print(k, [i for i, t in RT.items() if len(t) >= 2 and f(t)])
# also home-only and abroad-only counts
tier = dict(zip(RL.id, RL.tier))
for g in ['home', 'abroad', 'unknown site']:
    ids = [i for i, t in RT.items() if len(t) >= 2 and tier[i] == g]
    print(g, len(ids), {k: sum(f(RT[i]) for i in ids) for k, f in PATS.items()})

# ---------------- shared first / last / any sign
def first(t): return t[0] if u(t[0]) else None
def last(t): return t[-1] if u(t[-1]) else None
def pairs_same(vals): c = collections.Counter(v for v in vals if v); return sum(n * (n - 1) // 2 for n in c.values()), c.most_common(4)
def mid_pairs(ts):
    sets = [set(s for s in t[1:-1] if u(s)) for t in ts]
    return sum(1 for i in range(len(sets)) for j in range(i + 1, len(sets)) if sets[i] & sets[j])
def any_pairs(ts):
    sets = [set(s for s in t if u(s)) for t in ts]
    return sum(1 for i in range(len(sets)) for j in range(i + 1, len(sets)) if sets[i] & sets[j])
def stats(ts): return dict(first=pairs_same([first(t) for t in ts])[0], last=pairs_same([last(t) for t in ts])[0], mid=mid_pairs(ts), anyshare=any_pairs(ts))
rs = stats(rt); print('round shared', rs, pairs_same([first(t) for t in rt])[1], pairs_same([last(t) for t in rt])[1])
sqS = {k: [] for k in rs}
for _ in range(2000):
    s = stats(draw())
    for k in rs: sqS[k].append(s[k])
alltok = [s for t in rt for s in t]; shS = {k: [] for k in rs}
lens = [len(t) for t in rt]
for _ in range(5000):                       # redeal all signs among round texts, lengths kept
    p = rng.permutation(np.array(alltok, dtype=object)); out = []; k0 = 0
    for L_ in lens: out.append(tuple(p[k0:k0 + L_])); k0 += L_
    s = stats(out)
    for k in rs: shS[k].append(s[k])
SH = pd.DataFrame([dict(measure=k, round_real=rs[k], square_matched_mean=np.mean(sqS[k]), P_vs_square_higher=p_hi(rs[k], sqS[k]), P_vs_square_lower=(np.sum(np.array(sqS[k]) <= rs[k]) + 1) / 2001, redeal_mean=np.mean(shS[k]), P_vs_redeal_higher=p_hi(rs[k], shS[k])) for k in rs])
SH.to_csv(f'{OUTR}/structure_share.csv', index=False); print(SH.to_string())
# ---------------- where 090 091 and strokes sit
pos = []
for sg_name, S in [('090', {'090'}), ('091', {'091'}), ('093/095', {'093', '095'}), ('strokes', STROKES)]:
    c = collections.Counter()
    for t in rt:
        n = len(t)
        for i, s in enumerate(t):
            if s in S: c['first' if i == 0 else ('last' if i == n - 1 else 'middle')] += 1
    tot = sum(c.values())
    # within-text shuffle expectation of 'last' and 'first'
    ex = collections.Counter()
    for _ in range(2000):
        for t in rt:
            tt = list(rng.permutation(np.array(t, dtype=object))); n = len(tt)
            for i, s in enumerate(tt):
                if s in S: ex['first' if i == 0 else ('last' if i == n - 1 else 'middle')] += 1
    pos.append(dict(group=sg_name, tokens=tot, first=c['first'], middle=c['middle'], last=c['last'], shuffled_first=ex['first'] / 2000, shuffled_middle=ex['middle'] / 2000, shuffled_last=ex['last'] / 2000))
PO = pd.DataFrame(pos); PO.to_csv(f'{OUTR}/structure_positions.csv', index=False); print(PO.to_string())
# 090 and 091 in the same text, person+stroke counts
print('texts with a person sign:', sum(any(s in PERSON for s in t) for t in rt), 'of', len(rt))
print('texts with a stroke:', sum(any(s in STROKES for s in t) for t in rt))
print('both person and stroke:', sum(any(s in PERSON for s in t) and any(s in STROKES for s in t) for t in rt))
