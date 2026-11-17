#!/usr/bin/env python3
"""TWINS step 6: one redesign for each line that went against or had no power, and one new idea.  Written 2026-11-17
after steps 3-4; predictions fixed here before the numbers.

R1 (prediction a had no power: 71 twin pairs with buildings, 0.27 expected in one building). Redesign: NEAR twins
   (texts of 3+ signs one sign apart, same length) as the house-level unit. Prediction: near twins sit in one building
   more than texts dealt within the site, and inside one building they differ in animal or stand more than chance.
R2 (one holder, several texts: 3 related of 269, under chance). Redesign: related = the two texts share any name sign
   (not a number, opener, slot, closer or title). Prediction: same-holder house-mates share a name sign more often than
   house-mates with different holder marks.
R3 (twins share the animal 1.17x within format; all of it unicorn+unicorn or text-only+text-only). Test: species-
   specific travel. Among twin pairs where at least one stone has a beast other than the unicorn, same species against
   dealing within site x length x format. Prediction (text + animal = one holder): above chance.
R4 NEW IDEA: the seal SIZE is the property of the text (a rank written into the stone's size), not of the holder.
   Twins are closer in face size than chance even when the size is dealt within site x length x FORMAT, and also
   across time bins. Prediction: yes on both.
R5 Second catalogue: share of twin pairs in one excavation locus (its findspot unit) against loci dealt within site x
   length. Prediction: at or below chance (the locus result of the first catalogue replicates).
"""
from twins_common import *
import itertools, collections
rng = np.random.default_rng(6); NR = 3000
S = pd.read_csv(f'{OUT}/seals.csv', dtype=str).fillna('')
S['n'] = S.n.astype(int); S['area_mm2'] = pd.to_numeric(S.area_mm2, errors='coerce')
NAMEJOB = {'CREST', 'PERSONAL', 'NAME_BACK', 'PLACE', 'THING', 'MEASURE', 'AFTER_M'}
def name_signs(signs, v2):
    x = signs.split('-'); c = v2.split('-')
    return {s for s, k in zip(x, c) if k in NAMEJOB} if len(x) == len(c) else set()
def lev(a, b):
    dp = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, len(b) + 1):
            cur = dp[j]; dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + (a[i - 1] != b[j - 1])); prev = cur
    return dp[-1]
C = S[S.complete == 'True'].drop_duplicates(['obj', 'signs']).reset_index(drop=True)
C['stratum'] = C.site + '|' + C.n.astype(str)
def deal(col, within, D=None):
    D = C if D is None else D
    v = D[col].values; out = v.copy()
    for _, ix in D.groupby(within).indices.items(): out[ix] = v[ix][rng.permutation(len(ix))]
    return out

# ---------------- R1
print('R1  NEAR TWINS (3+ signs, same length, one sign apart)')
L3 = C[C.n >= 3].reset_index(drop=True)
toks = [tuple(s.split('-')) for s in L3.signs]
near = []
by_len = L3.groupby('n').indices
for n_, ix in by_len.items():
    for i, j in itertools.combinations(ix, 2):
        if L3.obj[i] != L3.obj[j] and sum(a != b for a, b in zip(toks[i], toks[j])) == 1: near.append((i, j))
I = np.array([p[0] for p in near]); J = np.array([p[1] for p in near])
def sameb(v): a, b = v[I], v[J]; ok = (a != '') & (b != ''); return int(((a == b) & ok).sum()), int(ok.sum())
for col in ['building', 'block', 'area_key', 'site']:
    s, n = sameb(L3[col].values); arr = np.array([sameb(deal(col, 'stratum' if col != 'site' else 'n', L3))[0] for _ in range(NR)])
    print(f'   near-twin pairs {len(near)}; same {col}: {s} of {n} vs dealt {arr.mean():.2f}; ratio {s/arr.mean() if arr.mean() else float("nan"):.2f}; P_more {(np.sum(arr>=s)+1)/(NR+1):.4f}')
inb = [(i, j) for i, j in near if L3.building[i] != '' and L3.building[i] == L3.building[j]]
for i, j in inb:
    print(f'      {L3.building[i]}: {L3.cisi[i]} {L3.signs[i]} {L3.animal[i]}:{L3.stand5[i]}  |  {L3.cisi[j]} {L3.signs[j]} {L3.animal[j]}:{L3.stand5[j]}')
# position of the differing sign, by job
pos = collections.Counter()
for i, j in near:
    k = [q for q, (a, b) in enumerate(zip(toks[i], toks[j])) if a != b][0]
    c = L3.v2[i].split('-'); pos[c[k] if k < len(c) else '?'] += 1
print('   job of the one differing sign: ' + str(pos.most_common()))
a, b = L3.animal.values[I], L3.animal.values[J]; ok = (a != '') & (b != '')
arr = []
for _ in range(NR):
    v = deal('animal', 'stratum', L3); arr.append(int(((v[I] == v[J]) & ok).sum()))
s = int(((a == b) & ok).sum()); arr = np.array(arr)
print(f'   near twins same animal {s} of {int(ok.sum())} vs dealt {arr.mean():.1f}; ratio {s/arr.mean():.2f}; P_more {(np.sum(arr>=s)+1)/(NR+1):.4f}')
st1, st2 = L3.stand5.values[I], L3.stand5.values[J]; ok2 = (st1 != '') & (st2 != '')
arr = []
for _ in range(NR):
    v = deal('stand5', 'stratum', L3); arr.append(int(((v[I] == v[J]) & ok2).sum()))
s = int(((st1 == st2) & ok2).sum()); arr = np.array(arr)
print(f'   near twins same stand letter {s} of {int(ok2.sum())} vs dealt {arr.mean():.1f}; ratio {s/arr.mean():.2f}; P_more {(np.sum(arr>=s)+1)/(NR+1):.4f}')
pd.DataFrame([dict(a=L3.cisi[i], b=L3.cisi[j], text_a=L3.signs[i], text_b=L3.signs[j], site_a=L3.site[i], site_b=L3.site[j], building_a=L3.building[i], building_b=L3.building[j],
                   animal_a=L3.animal[i], animal_b=L3.animal[j], stand_a=L3.stand5[i], stand_b=L3.stand5[j], bin_a=L3.bin[i], bin_b=L3.bin[j]) for i, j in near]).to_csv(f'{OUT}/near_twins.csv', index=False)

# ---------------- R2
print('\nR2  ONE HOLDER: house-mates sharing a name sign')
A2 = S[(S.signs != '') & (S.lost == '0') & (S.building != '')].drop_duplicates(['obj', 'signs']).reset_index(drop=True)
NS = [name_signs(s, v) for s, v in zip(A2.signs, A2.v2)]
sh, oh = [], []
for b, g in A2.groupby('building'):
    for i, j in itertools.combinations(g.index, 2):
        if A2.obj[i] == A2.obj[j] or A2.animal[i] == '' or A2.animal[j] == '': continue
        if A2.animal[i] == 'unicorn' and A2.animal[j] == 'unicorn' and A2.stand5[i] != '' and A2.stand5[i] == A2.stand5[j]: sh.append((i, j))
        elif A2.animal[i] != A2.animal[j] or (A2.stand5[i] != '' and A2.stand5[j] != '' and A2.stand5[i] != A2.stand5[j]): oh.append((i, j))
def shared(pp, ns): return sum(1 for i, j in pp if ns[i] & ns[j])
print(f'   same holder: {shared(sh, NS)} of {len(sh)} share a name sign ({shared(sh, NS)/len(sh):.1%}); other holder: {shared(oh, NS)} of {len(oh)} ({shared(oh, NS)/len(oh):.1%})')
arr = []
site_ix = A2.groupby('site').indices
for _ in range(1000):
    perm = np.arange(len(A2))
    for _, ix in site_ix.items(): perm[ix] = ix[rng.permutation(len(ix))]
    ns2 = [NS[k] for k in perm]; arr.append(shared(sh, ns2))
arr = np.array(arr); s = shared(sh, NS)
print(f'   same-holder pairs sharing a name sign {s} vs texts dealt within site {arr.mean():.1f}; ratio {s/arr.mean():.2f}; P_more {(np.sum(arr>=s)+1)/1001:.4f}')
arr = []
for _ in range(1000):
    perm = np.arange(len(A2))
    for _, ix in site_ix.items(): perm[ix] = ix[rng.permutation(len(ix))]
    ns2 = [NS[k] for k in perm]; arr.append(shared(oh, ns2))
arr = np.array(arr); s = shared(oh, NS)
print(f'   other-holder house-mates sharing a name sign {s} vs dealt {arr.mean():.1f}; ratio {s/arr.mean():.2f}; P_more {(np.sum(arr>=s)+1)/1001:.4f}')

# ---------------- R3 and R4 on exact twin pairs
Mem = pd.read_csv(f'{OUT}/members.csv', dtype=str).fillna('')
keyM = set(zip(Mem.obj, Mem.signs))
C['in_set'] = [(o, s) in keyM for o, s in zip(C.obj, C.signs)]
C = C[(~C.signs.isin(set(Mem.signs))) | C.in_set].reset_index(drop=True)
C['sf'] = C.site + '|' + C.n.astype(str) + '|' + C.fmt
pairs = [(i, j) for t, g in C[C.in_set].groupby('signs') for i, j in itertools.combinations(g.index, 2)]
I = np.array([p[0] for p in pairs]); J = np.array([p[1] for p in pairs])
print('\nR3  SPECIES-SPECIFIC TRAVEL')
an = C.animal.values
mask = (an[I] != '') & (an[J] != '') & (an[I] != 'none') & (an[J] != 'none') & ~((an[I] == 'unicorn') & (an[J] == 'unicorn'))
s = int(((an[I] == an[J]) & mask).sum()); arr = []
for _ in range(NR):
    v = deal('animal', 'sf'); m2 = (v[I] != '') & (v[J] != '') & (v[I] != 'none') & (v[J] != 'none') & ~((v[I] == 'unicorn') & (v[J] == 'unicorn'))
    arr.append(int(((v[I] == v[J]) & m2).sum()))
arr = np.array(arr)
print(f'   pairs with a beast on both and not both unicorn: {int(mask.sum())}; same species {s}; dealt {arr.mean():.2f}; P_fewer {(np.sum(arr<=s)+1)/(NR+1):.4f}')
for i, j in zip(I[mask], J[mask]): print(f'      {C.signs[i]:16s} {C.cisi[i]} {an[i]} ({C.site[i]})  |  {C.cisi[j]} {an[j]} ({C.site[j]})')
uu = (an[I] == 'unicorn') & (an[J] == 'unicorn'); arr = []
for _ in range(NR):
    v = deal('animal', 'sf'); arr.append(int(((v[I] == 'unicorn') & (v[J] == 'unicorn')).sum()))
arr = np.array(arr)
print(f'   both unicorn: {int(uu.sum())} vs dealt within site x length x format {arr.mean():.1f}; P_more {(np.sum(arr>=uu.sum())+1)/(NR+1):.4f}')
print('\nR4  SIZE AS A PROPERTY OF THE TEXT')
la = np.log(C.area_mm2.values)
bins_ = C.bin.values
for label, m in [('all twin pairs', np.ones(len(I), bool)), ('different cities', C.site.values[I] != C.site.values[J]),
                 ('different time bins', (bins_[I] != '') & (bins_[J] != '') & (bins_[I] != bins_[J])),
                 ('square with a beast, both', (C.fmt.values[I] == 'square') & (C.fmt.values[J] == 'square') & (an[I] != 'none') & (an[J] != 'none'))]:
    ok = ~np.isnan(la[I]) & ~np.isnan(la[J]) & m; real = np.abs(la[I] - la[J])[ok].mean(); arr = []
    grp = C.groupby('sf').indices
    for _ in range(NR):
        v = la.copy()
        for _, ix in grp.items(): v[ix] = la[ix][rng.permutation(len(ix))]
        okk = ~np.isnan(v[I]) & ~np.isnan(v[J]) & m; arr.append(np.abs(v[I] - v[J])[okk].mean())
    arr = np.array(arr)
    print(f'   {label}: pairs {int(ok.sum())}; mean size gap {real:.3f} (= faces differ by {np.exp(real)*100-100:.0f}%) vs dealt within site x length x format {arr.mean():.3f} ({np.exp(arr.mean())*100-100:.0f}%); P_closer {(np.sum(arr<=real)+1)/(NR+1):.4f}')

# ---------------- R5
print('\nR5  SECOND CATALOGUE: same locus')
P2 = pd.read_csv(f'{ROOT}/work_data/mahadevan_parsed.csv', dtype=str).fillna('')
MS = pd.read_csv(f'{OUT}/mah_sets.csv', dtype=str).fillna('')
allm = P2[P2.cls == 'seal'].drop_duplicates('textnum').reset_index(drop=True)
allm['stratum'] = allm.site + '|' + allm.n
pos = {t: k for k, t in enumerate(allm.textnum)}
pp = [(pos[a], pos[b]) for t, g in MS.groupby('mtext') for a, b in itertools.combinations(list(g.textnum), 2) if a in pos and b in pos]
I2 = np.array([p[0] for p in pp]); J2 = np.array([p[1] for p in pp])
lo = (allm.site + '|' + allm.locus).values; allm['lo'] = lo
s = int((lo[I2] == lo[J2]).sum()); arr = np.array([int((deal('lo', 'stratum', allm)[I2] == deal('lo', 'stratum', allm)[J2]).sum()) for _ in range(1)])
arr = []
for _ in range(NR):
    v = deal('lo', 'stratum', allm); arr.append(int((v[I2] == v[J2]).sum()))
arr = np.array(arr)
ss = int((allm.site.values[I2] == allm.site.values[J2]).sum())
print(f'   twin pairs {len(pp)}; same site {ss}; same locus {s} vs dealt within site x length {arr.mean():.1f}; ratio {s/arr.mean():.2f}; P_more {(np.sum(arr>=s)+1)/(NR+1):.4f}; P_fewer {(np.sum(arr<=s)+1)/(NR+1):.4f}')
