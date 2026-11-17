#!/usr/bin/env python3
"""Sign list step 4, redesign for the marks that did not pass the written-out test (cage, brackets, joined object, other).
Rule fixed before the run: if the mark is a separate unit sitting in front of / around the base, the compound should END
like its base (its right neighbours are the base's right neighbours) while it may START differently. Score per compound with
5+ uses (first catalogue, copy events): cosine of right-neighbour PPMI vectors (signlist_1_evidence weighting) between the
compound and its base, against the cosine with every other base of the family list (dealt base). Per mark type: mean real
cosine against the mean over 5,000 deals of one random other base per compound; P = share of deals >= real.
The same for LEFT neighbours (a mark in front should make the compound start differently from its base: real left cosine
below the right one).
NEW IDEA run alongside: the caged sign as a plural or a count (four strokes around): caged compounds should sit after a
number less often than their uncaged bases (a count already written in), measured as the share of uses right after a
number sign, caged against base. Output: work_data/signlist/mark_redesign.csv, log_marks_redesign.txt
"""
from signlist_common import *
say = logger('marks_redesign')
F = pd.read_csv(f'{OUT}/mark_families.csv', dtype=str)
L = load_lipi(); U = uses(L); CL = v2classes()
sig = sorted(s for s in U if U[s] >= 5); I = {s: i for i, s in enumerate(sig)}
ctx = ['^', '$'] + sorted(s for s in U if is_sign(s)); C = {c: i for i, c in enumerate(ctx)}
Lc = np.zeros((len(sig), len(ctx))); Rc = np.zeros((len(sig), len(ctx))); after_num = collections.Counter()
NUMC = {'NUM_SHORT', 'NUM_TALL', 'NUM_NAME'}
for e in L:
    for f, br in zip(e['faces'], e['broken']):
        for i, s in enumerate(f):
            if s not in I: continue
            if i > 0 and is_sign(f[i - 1]):
                Lc[I[s], C[f[i - 1]]] += 1
                if CL.get(f[i - 1], '') in NUMC: after_num[s] += 1
            elif i == 0 and not br: Lc[I[s], 0] += 1
            if i < len(f) - 1 and is_sign(f[i + 1]): Rc[I[s], C[f[i + 1]]] += 1
            elif i == len(f) - 1 and not br: Rc[I[s], 1] += 1
def norm(M):
    tot = M.sum(0) + 1e-9; T = M.sum(); rs = M.sum(1, keepdims=True) + 1e-9
    with np.errstate(divide='ignore', invalid='ignore'): P = np.log(M * T / (rs * tot))
    P[~np.isfinite(P)] = 0; P[P < 0] = 0
    return P / (np.linalg.norm(P, axis=1, keepdims=True) + 1e-12)
NL, NR = norm(Lc), norm(Rc)
F = F[F.compound.isin(I) & F.base.isin(I)]
bases = sorted(set(F.base))
rng = np.random.default_rng(8); rows = []
for t, g in list(F.groupby('mark_type')) + [('all', F)]:
    pairs = list(zip(g.compound, g.base))
    for side, N in (('right', NR), ('left', NL)):
        real = np.mean([N[I[c]] @ N[I[b]] for c, b in pairs])
        D = [np.mean([N[I[c]] @ N[I[rng.choice([x for x in bases if x != b])]] for c, b in pairs]) for _ in range(5000)]
        rows.append(dict(mark_type=t, side=side, compounds=len(pairs), real_cosine=round(real, 3), dealt_mean=round(float(np.mean(D)), 3), P=pvalue_hi(D, real)))
        say(f'{t} ({len(pairs)} compounds), {side} neighbours: compound-base cosine {real:.3f} against dealt bases {np.mean(D):.3f}, P {pvalue_hi(D, real):.4f}')
cg = F[F.mark_type == 'cage']
for c, b in zip(cg.compound, cg.base):
    say(f'   new idea, cage: {c} after a number {after_num[c]}/{U[c]} ({after_num[c] / U[c]:.1%}) against its base {b} {after_num[b]}/{U[b]} ({after_num[b] / U[b]:.1%})')
    rows.append(dict(mark_type='cage after a number', side=f'{c} vs {b}', compounds=1, real_cosine=round(after_num[c] / U[c], 3), dealt_mean=round(after_num[b] / U[b], 3), P=''))
pd.DataFrame(rows).to_csv(f'{OUT}/mark_redesign.csv', index=False)
