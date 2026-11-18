#!/usr/bin/env python3
"""Recheck 7: text twins (twins_6_redesign.py R4 and R5).
  (i)  second catalogue: twin pairs in the same excavation locus 48 against 28.6 (dealt within site x length, P 0.004)
  (ii) size closeness of twins: faces differ by 71% against 88% (log gap 0.537 against 0.630, P 0.016)

Plain words: TWINS = two different seals with the identical complete text. LOCUS = the second catalogue's findspot
code (Mahadevan 1977; one code can be a large excavation sector: locus 31 at Mohenjo-daro holds 505 seals). SIZE GAP =
difference of the log face areas of two twins; chance = sizes dealt among seals of the same site, length and format.

Checks: (1) a pair of objects counted more than once because they share more than one identical face (two-sided
objects); (2) the deal pool holds seals with no locus / no size; (c) a batch of identical objects in one locus counted
as many pairs.
Run: python3 recheck_07_twins.py   (about 2 minutes)
"""
import sys, itertools, collections
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
import numpy as np, pandas as pd
from recheck_common import *
say = log_to(f'{OUT}/r07_log.txt')
rng = np.random.default_rng(6); NR = 3000

say('(i) second catalogue, twins in one locus (old 48 against 28.6, P 0.004)')
P2 = pd.read_csv(f'{ROOT}/work_data/mahadevan_parsed.csv', dtype=str).fillna('')
MS = pd.read_csv(f'{ROOT}/work_data/twins/mah_sets.csv', dtype=str).fillna('')
allm = P2[P2.cls == 'seal'].copy()
objn = allm.groupby('textnum').n.apply(lambda s: sum(int(v) for v in s))
allm = allm.drop_duplicates('textnum').reset_index(drop=True)
allm['lo'] = allm.site + '|' + allm.locus
pos = {t: k for k, t in enumerate(allm.textnum)}

def deal(v, strata):
    out = v.copy()
    for ix in strata: out[ix] = v[ix][rng.permutation(len(ix))]
    return out

def locus_test(pairs, D, stratcol, label, events=False, texts=None):
    I = np.array([p[0] for p in pairs]); J = np.array([p[1] for p in pairs])
    lo = D.lo.values
    strata = list(D.groupby(stratcol).indices.values())
    def stat(v):
        if not events: return int((v[I] == v[J]).sum())
        # one event per (twin text, locus) holding 2+ of the text's stones
        ev = set()
        for i, j, t in zip(I, J, texts):
            if v[i] == v[j]: ev.add((t, v[i]))
        return len(ev)
    s = stat(lo); arr = np.array([stat(deal(lo, strata)) for _ in range(NR)])
    say(f'  {label}: {len(pairs)} pairs; {"events" if events else "same-locus pairs"} {s} against {arr.mean():.2f} '
        f'(ratio {s / arr.mean():.2f}, P {pvalue_hi(arr, s):.4f})')
    return s, arr.mean(), pvalue_hi(arr, s)

allm['stratum'] = allm.site + '|' + allm.n
pp_old = [(pos[a], pos[b]) for t, g in MS.groupby('mtext') for a, b in itertools.combinations(list(g.textnum), 2) if a in pos and b in pos]
o0 = locus_test(pp_old, allm, 'stratum', 'A  as run (pairs per matching face, all seals in the deal)')
cnt = collections.Counter(tuple(sorted(p)) for p in pp_old)
dup = {p: c for p, c in cnt.items() if c > 1}
say(f'  object pairs counted more than once (two identical faces): {len(dup)} pairs, {sum(c - 1 for c in dup.values())} extra counts: '
    + '; '.join(f'{allm.textnum[a]}+{allm.textnum[b]} x{c}' for (a, b), c in dup.items()))
# clean: one row per object pair; deal only among seals with a locus code; strata = site x object length
D = allm[allm.locus.str.strip() != ''].reset_index(drop=True)
say(f'  seals without a locus code removed from the deal: {len(allm) - len(D)}')
D['L'] = D.textnum.map(objn).astype(str); D['stratum2'] = D.site + '|' + D.L
pos2 = {t: k for k, t in enumerate(D.textnum)}
txt = {}
pairs = set()
for t, g in MS.groupby('mtext'):
    for a, b in itertools.combinations(list(g.textnum), 2):
        if a in pos2 and b in pos2:
            key = tuple(sorted((pos2[a], pos2[b])))
            if key not in pairs: pairs.add(key); txt[key] = t
pairs = sorted(pairs)
c1 = locus_test(pairs, D, 'stratum2', 'B  clean: one count per object pair, only seals with a locus, dealt within site x length')
c2 = locus_test(pairs, D, 'stratum2', 'C  clean + a batch of one text in one locus = one event', events=True, texts=[txt[p] for p in pairs])
lo = D.lo.values
by = collections.Counter(lo[i] for i, j in pairs if lo[i] == lo[j])
say(f'  where the same-locus pairs sit: {dict(by)}; seals in Mohenjo-daro locus 31: {(D.lo == "MD|31").sum()} of {(D.site == "MD").sum()} MD seals')

say('\n(ii) size closeness of twins (old: log gap 0.537 = 71% against 0.630 = 88%, P 0.016)')
S = pd.read_csv(f'{ROOT}/work_data/twins/seals.csv', dtype=str).fillna('')
S['n'] = S.n.astype(int); S['area_mm2'] = pd.to_numeric(S.area_mm2, errors='coerce')
C = S[S.complete == 'True'].drop_duplicates(['obj', 'signs']).reset_index(drop=True)
Mem = pd.read_csv(f'{ROOT}/work_data/twins/members.csv', dtype=str).fillna('')
keyM = set(zip(Mem.obj, Mem.signs))
C['in_set'] = [(o, s) in keyM for o, s in zip(C.obj, C.signs)]
C = C[(~C.signs.isin(set(Mem.signs))) | C.in_set].reset_index(drop=True)
C['sf'] = C.site + '|' + C.n.astype(str) + '|' + C.fmt
f2s, _ = stone_map(); C['stone'] = C.face.map(f2s)
def size_test(C, label, eligible_only):
    C = C.reset_index(drop=True)
    pairs = [(i, j) for t, g in C[C.in_set].groupby('signs') for i, j in itertools.combinations(g.index, 2) if C.stone[i] != C.stone[j]]
    seen = set(); P_ = []
    for i, j in pairs:   # one count per stone pair
        k = tuple(sorted((C.stone[i], C.stone[j])))
        if k in seen: continue
        seen.add(k); P_.append((i, j))
    I = np.array([p[0] for p in P_]); J = np.array([p[1] for p in P_])
    la = np.log(C.area_mm2.values); ok = ~np.isnan(la[I]) & ~np.isnan(la[J]); real = np.abs(la[I] - la[J])[ok].mean()
    if eligible_only:
        strata = [ix[~np.isnan(la[ix])] for ix in C.groupby('sf').indices.values()]
    else:
        strata = list(C.groupby('sf').indices.values())
    arr = []
    for _ in range(NR):
        v = deal(la, strata); okk = ~np.isnan(v[I]) & ~np.isnan(v[J]) & ok if eligible_only else ~np.isnan(v[I]) & ~np.isnan(v[J])
        arr.append(np.abs(v[I] - v[J])[okk].mean())
    arr = np.array(arr)
    say(f'  {label}: {int(ok.sum())} pairs with both sizes; gap {real:.3f} ({np.exp(real) * 100 - 100:.0f}%) against {arr.mean():.3f} '
        f'({np.exp(arr.mean()) * 100 - 100:.0f}%), P (closer) {pvalue_lo(arr, real):.4f}')
    return real, arr.mean(), pvalue_lo(arr, real), int(ok.sum()), len(pairs) - len(P_)
s0 = size_test(C, 'A  as run', False)
s1 = size_test(C, 'B  clean: one count per stone pair, sizes dealt only among seals with a size', True)
say(f'  stone pairs counted more than once in A: {s0[4]}')
import json
json.dump(dict(locus_run=o0, locus_clean=c1, locus_events=c2, size_run=s0, size_clean=s1), open(f'{OUT}/r07.json', 'w'), default=float, indent=1)
