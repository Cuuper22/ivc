#!/usr/bin/env python3
"""Sign list step 1: four kinds of same-sign evidence plus the co-occurrence check, for every pair of Lipi signs with
5+ uses each (uses counted over copy events, signlist_common). All rules below were written before any number was seen.

(a) SWAPS. Faces with no lost sign, no broken edge, 3+ signs. Two faces that are identical except at one position form a
    swap at that position; the FRAME is (signs before, signs after). Frames are pooled over both catalogues in Lipi
    numbering (the second catalogue through its reading_lipi), as a set, so one frame seen in both catalogues counts once and
    moulded copies (one event) count once. Score = number of distinct frames.
    FIRES when frames >= 2 AND frames is above the 99th percentile of frames among all eligible pairs in the same
    frequency-band cell (5 quantile bands of uses; a cell = the unordered pair of bands).
(b) NEIGHBOURS. First catalogue events only (the second re-transcribes mostly the same objects). For every sign, counts
    of its left neighbour (start-of-text '^' when the face edge is not broken) and right neighbour ('$' end). Weighting:
    positive pointwise mutual information (PPMI) of sign x context. Similarity = mean of the cosine of the left vectors and
    the cosine of the right vectors. To keep (b) apart from (a), the pair's own swap-frame faces are taken out of both
    signs' counts before its similarity is computed (leave-out similarity).
    FIRES when the leave-out similarity is at or above the 99th percentile of (full) similarity among all eligible pairs in
    the same band cell.
(c) DRAWING. From work_data/sign_shapes.csv (the shape list: a shape code and a written description per sign).
    FIRES when the two signs have the same shape code, or when the word sets of their descriptions (lower case, words of
    3+ letters, without stop words) overlap with Jaccard >= 0.6.
    NUMERAL VETO (negative drawing evidence): the descriptions differ but become identical once number words are removed:
    the same shape with a different count of strokes is a different numeral, never one sign.
(d) THE OTHER CATALOGUE LUMPS THEM. Crosswalk rows with share_of_lipi_sign >= 0.25: FIRES when both Lipi signs have one
    Mahadevan number in common at that share.
CO-OCCURRENCE (negative evidence). Number of first-catalogue events holding both signs (any face, any place) against the
    expectation sum over events of p_a * p_b, p_x = 1 - (1 - f_x)^L (f_x = share of all sign uses, L = known signs in the
    event). VETO when observed > expected and Poisson P(X >= observed) < 0.05.
Output: work_data/signlist/pairs.csv (every eligible pair), signs.csv (eligible signs), swap_frames.csv (every swap
frame of every pair, incl. ineligible signs), log_evidence.txt.
"""
import itertools, math
from scipy.stats import poisson
from signlist_common import *

say = logger('evidence')
L = load_lipi(); Mx = load_mahadevan('lipi')
U = uses(L)
ELIG = sorted(s for s, n in U.items() if n >= 5)
BAND = bands(U, ELIG)
CL = v2classes()
say(f'first catalogue: {len(L)} copy events, {len(U)} signs, {sum(U.values())} uses; eligible (5+ uses): {len(ELIG)}')

# ---------------- (a) swaps ----------------
frames = collections.defaultdict(set)        # (a,b) -> set of frame keys
frame_faces = collections.defaultdict(set)   # frame key -> Lipi (event idx, face idx) carrying it
for evs, cat in ((L, 'L'), (Mx, 'M')):
    groups = collections.defaultdict(dict)
    for ei, e in enumerate(evs):
        for fi, (f, br) in enumerate(zip(e['faces'], e['broken'])):
            if br or len(f) < 3 or not all(is_sign(s) for s in f): continue
            for i in range(len(f)):
                key = (f[:i], f[i + 1:])
                groups[key].setdefault(f[i], []).append((cat, ei, fi))
    for key, d in groups.items():
        if len(d) < 2: continue
        for s, locs in d.items():
            for (c, ei, fi) in locs:
                if c == 'L': frame_faces[key].add((ei, fi))
        for a, b in itertools.combinations(sorted(d), 2):
            frames[(a, b)].add(key)
say(f'(a) sign pairs that swap at least once: {len(frames)}; in 2+ frames: {sum(len(v) >= 2 for v in frames.values())}')
with open(f'{OUT}/swap_frames.csv', 'w') as fh:
    fh.write('a,b,frames,examples\n')
    for (a, b), fr in sorted(frames.items(), key=lambda kv: -len(kv[1])):
        ex = ' | '.join('-'.join(p) + '-[ ]-' + '-'.join(q) for p, q in list(fr)[:4])
        fh.write(f'{a},{b},{len(fr)},{ex}\n')

# ---------------- (b) neighbours ----------------
IDX = {s: i for i, s in enumerate(ELIG)}
ctx = ['^', '$'] + sorted(s for s in U if is_sign(s))
CI = {c: i for i, c in enumerate(ctx)}
nS, nC = len(ELIG), len(ctx)
Lc = np.zeros((nS, nC)); Rc = np.zeros((nS, nC))

def face_ctx(f, br):
    out = []   # (sign, side, context)
    for i, s in enumerate(f):
        if s not in IDX: continue
        if i > 0:
            if is_sign(f[i - 1]): out.append((s, 0, f[i - 1]))
        elif not br: out.append((s, 0, '^'))
        if i < len(f) - 1:
            if is_sign(f[i + 1]): out.append((s, 1, f[i + 1]))
        elif not br: out.append((s, 1, '$'))
    return out

for e in L:
    for f, br in zip(e['faces'], e['broken']):
        for s, side, c in face_ctx(f, br):
            (Lc if side == 0 else Rc)[IDX[s], CI[c]] += 1

def ppmi(C, tot_c, tot):
    rs = C.sum(1, keepdims=True)
    with np.errstate(divide='ignore', invalid='ignore'):
        P = np.log((C * tot) / (rs * tot_c[None, :]))
    P[~np.isfinite(P)] = 0; P[P < 0] = 0
    return P

totL = Lc.sum(0) + 1e-9; totR = Rc.sum(0) + 1e-9; TL = Lc.sum(); TR = Rc.sum()
def vecs(lc, rc):
    pl = ppmi(lc, totL, TL); pr = ppmi(rc, totR, TR)
    nl = pl / (np.linalg.norm(pl, axis=1, keepdims=True) + 1e-12); nr = pr / (np.linalg.norm(pr, axis=1, keepdims=True) + 1e-12)
    return nl, nr
nl, nr = vecs(Lc, Rc)
SIM = 0.5 * (nl @ nl.T + nr @ nr.T)
say('(b) neighbour similarity matrix built')

# ---------------- (c) drawing ----------------
SH = shapes()
STOP = {'the', 'and', 'with', 'from', 'out', 'one', 'side', 'its', 'that', 'this', 'see', 'also', 'into', 'like', 'possibly', 'small', 'large'}
NUMW = {'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'single', 'simple', 'pair', 'pairs',
        'double', 'triple', 'multiple', 'stacked', 'adjacent', 'rows', 'row', 'strokes', 'stroke', 'lines', 'line'}
def words(t): return {w for w in re.findall(r'[a-z]{3,}', t.lower()) if w not in STOP}
def numfree(t): return re.sub(r'\b(one|two|three|four|five|six|seven|eight|nine|ten|single|simple|1|2|3|4|5|6|7|8|9)\b', '#', t.lower()).replace('strokes', 'stroke').replace('lines', 'line')
def drawing(a, b):
    if a not in SH or b not in SH: return 'no description', False, False
    (ca, ta), (cb, tb) = SH[a], SH[b]
    numveto = ta != tb and numfree(ta) == numfree(tb)
    if numveto: return 'same shape, different count', False, True
    if ca == cb: return f'same shape code {ca}', True, False
    wa, wb = words(ta), words(tb)
    j = len(wa & wb) / max(1, len(wa | wb))
    if j >= 0.6: return f'descriptions overlap {j:.2f}', True, False
    return f'descriptions overlap {j:.2f}', False, False

# ---------------- (d) crosswalk ----------------
X = crosswalk(); X = X[X.share >= 0.25]
L2M = collections.defaultdict(set)
for l, m in zip(X.lipi, X.mahadevan): L2M[l].add(m)

# ---------------- co-occurrence ----------------
tot = sum(U.values()); F = {s: U[s] / tot for s in ELIG}
ev_sets = []; ev_len = []
for e in L:
    ss = [s for f in e['faces'] for s in f if is_sign(s)]
    ev_sets.append(set(ss) & set(ELIG)); ev_len.append(len(ss))
ev_len = np.array(ev_len)
pres = {s: 1 - (1 - F[s]) ** ev_len for s in ELIG}
co = collections.Counter()
for st in ev_sets:
    for a, b in itertools.combinations(sorted(st), 2): co[(a, b)] += 1

# ---------------- percentiles per band cell, leave-out similarity ----------------
pairs = list(itertools.combinations(ELIG, 2))
cell = collections.defaultdict(list)
for a, b in pairs:
    k = tuple(sorted((BAND[a], BAND[b])))
    cell[k].append((len(frames.get((a, b), ())), SIM[IDX[a], IDX[b]]))
thrA = {k: np.quantile([x[0] for x in v], 0.99) for k, v in cell.items()}
thrB = {k: np.quantile([x[1] for x in v], 0.99) for k, v in cell.items()}
say('99th-percentile thresholds per band cell (bands 0 = rarest):')
for k in sorted(cell): say(f'   cell {k}: {len(cell[k])} pairs; swap frames > {thrA[k]:.1f}; similarity >= {thrB[k]:.3f}')

def leave_out_sim(a, b):
    fr = frames.get((a, b))
    if not fr: return SIM[IDX[a], IDX[b]]
    lc = Lc.copy(); rcm = Rc.copy()
    seen = set()
    for key in fr:
        for (ei, fi) in frame_faces.get(key, ()):
            if (ei, fi) in seen: continue
            seen.add((ei, fi))
            f = L[ei]['faces'][fi]; br = L[ei]['broken'][fi]
            for s, side, c in face_ctx(f, br):
                if s in (a, b): (lc if side == 0 else rcm)[IDX[s], CI[c]] -= 1
    ia, ib = IDX[a], IDX[b]
    sub = [ia, ib]
    pl = ppmi(lc[sub], totL, TL); pr = ppmi(rcm[sub], totR, TR)
    def cos(P): return float(P[0] @ P[1] / (np.linalg.norm(P[0]) * np.linalg.norm(P[1]) + 1e-12))
    return 0.5 * (cos(pl) + cos(pr))

rows = []
for i, (a, b) in enumerate(pairs):
    bar(i, len(pairs), 'scoring pairs')
    k = tuple(sorted((BAND[a], BAND[b])))
    nf = len(frames.get((a, b), ()))
    fa = nf >= 2 and nf > thrA[k]
    sim = SIM[IDX[a], IDX[b]]
    slo = leave_out_sim(a, b) if nf else sim
    fb = slo >= thrB[k]
    ck, fc, nv = drawing(a, b)
    dm = sorted(L2M[a] & L2M[b]); fd = bool(dm)
    o = co.get((a, b), 0); E = float((pres[a] * pres[b]).sum())
    veto = o > E and poisson.sf(o - 1, E) < 0.05
    rows.append(dict(a=a, b=b, uses_a=U[a], uses_b=U[b], band_cell=f'{k[0]}{k[1]}', class_a=CL.get(a, ''), class_b=CL.get(b, ''),
                     swap_frames=nf, a_fire=fa, sim=round(float(sim), 4), sim_leaveout=round(float(slo), 4), b_fire=fb,
                     drawing=ck, c_fire=fc, numeral_veto=nv, mahadevan_shared='|'.join(dm), d_fire=fd,
                     cooc=o, cooc_exp=round(E, 3), cooc_veto=veto, n_kinds=int(fa) + int(fb) + int(fc) + int(fd)))
P = pd.DataFrame(rows); P.to_csv(f'{OUT}/pairs.csv', index=False)
pd.DataFrame(dict(sign=ELIG, uses=[U[s] for s in ELIG], band=[BAND[s] for s in ELIG], v2=[CL.get(s, '') for s in ELIG])).to_csv(f'{OUT}/signs.csv', index=False)
say(f'pairs scored: {len(P)}')
for c in ['a_fire', 'b_fire', 'c_fire', 'd_fire', 'numeral_veto', 'cooc_veto']: say(f'   {c}: {int(P[c].sum())}')
say('pairs by number of agreeing kinds:', P.n_kinds.value_counts().sort_index().to_dict())
