#!/usr/bin/env python3
"""TWINS step 3: what varies inside a twin set and what stays.  Written 2026-11-17; predictions fixed before the run.

Unit: a PAIR of different stones inside one twin set (identical complete text). For every attribute the null deals that
attribute among ALL complete seals of the same site and the same text length (5,000 deals), keeping the pairs fixed;
P = share of deals at least as extreme as the real count in the predicted direction (one-sided), ratio = real / dealt mean.
City is dealt among seals of the same text length (it cannot be dealt inside a site).

Attributes: animal (species; 'none' = inscription-only seal is a value of its own; unrecorded left out), stand letter
(unicorn seals with W/J/S/I/L), seal face size (|log ratio| of the two faces; small = alike), time bin, city.

Predictions (written before the numbers):
 P0 overall: twins share the animal no more than chance (the animal belongs to the stone, not the text) -> ratio ~1.0;
    they share the stand letter no more than chance; size no more alike than chance; same time bin at chance.
 Pa SAME BUILDING: twins in one building differ in animal-or-stand MORE often than chance (two holders of one house
    need different stones).
 Pb DIFFERENT TIME BINS: twins in different bins are no more alike in animal than chance (ratio ~1).
 Pc DIFFERENT CITIES: if text + animal is one travelling person, same-animal ratio > 1; if the text is an office held
    locally, ratio < 1. Committed guess: ratio < 1 for count lines and front formulas (local offices), > 1 for name texts.
 P-city: twins sit in different cities MORE often than seals of the same length dealt at random (the stamps finding
    for impressions carried over to seal-seal pairs).
Second catalogue replication: same animal test with its field-symbol code (code only, sub-type dropped).
Writes work_data/twins/pairs.csv, vary.csv, log_3.txt.
"""
from twins_common import *
import itertools
rng = np.random.default_rng(3)
NR = 5000
S = pd.read_csv(f'{OUT}/seals.csv', dtype=str).fillna('')
S['n'] = S.n.astype(int); S['area_mm2'] = pd.to_numeric(S.area_mm2, errors='coerce')
C = S[S.complete == 'True'].drop_duplicates(['obj', 'signs']).reset_index(drop=True)
Mem = pd.read_csv(f'{OUT}/members.csv', dtype=str).fillna('')
C = C[~C.obj.isin(set(C.obj) - set(Mem.obj)) | ~C.signs.isin(set(Mem.signs))]       # drop merged double entries from sets
C['in_set'] = C.signs.isin(set(Mem.signs)) & C.obj.isin(set(Mem.obj))
C = C[(~C.signs.isin(set(Mem.signs))) | C.in_set].reset_index(drop=True)
C['stratum'] = C.site + '|' + C.n.astype(str)
idx = {}
pairs = []
for t, g in C[C.in_set].groupby('signs'):
    for i, j in itertools.combinations(g.index, 2): pairs.append((i, j))
I = np.array([p[0] for p in pairs]); J = np.array([p[1] for p in pairs])
log('t3', f'stones in twin sets {int(C.in_set.sum())}, pairs {len(pairs)}, background seals {len(C)}')

def deal(col, within):
    v = C[col].values.copy(); out = v.copy()
    for _, ix in C.groupby(within).indices.items():
        out[ix] = v[ix][rng.permutation(len(ix))]
    return out

def pair_df():
    P = pd.DataFrame({'i': I, 'j': J})
    for c in ['signs', 'kind', 'site', 'building', 'area_key', 'bin', 'animal', 'stand5', 'cisi', 'n']:
        P[c + '_a'] = C[c].values[I]; P[c + '_b'] = C[c].values[J]
    P['same_building'] = (P.building_a != '') & (P.building_a == P.building_b)
    P['same_city'] = P.site_a == P.site_b
    P['both_bin'] = (P.bin_a != '') & (P.bin_b != '')
    P['diff_bin'] = P.both_bin & (P.bin_a != P.bin_b)
    P['same_bin'] = P.both_bin & (P.bin_a == P.bin_b)
    return P
P = pair_df()
P['kind'] = P.kind_a
P.to_csv(f'{OUT}/pairs.csv', index=False)

def stat_same(vals, mask):
    a = vals[I]; b = vals[J]; ok = (a != '') & (b != '') & mask
    return int(((a == b) & ok).sum()), int(ok.sum())

subsets = {'all pairs': np.ones(len(P), bool), 'same building': P.same_building.values, 'same city, other building': (P.same_city & ~P.same_building).values,
           'different cities': (~P.same_city).values, 'same time bin': P.same_bin.values, 'different time bins': P.diff_bin.values}
for k in ['count line', 'front formula', 'name + closer', 'bare name']:
    subsets[f'kind: {k}'] = (P.kind == k).values
    subsets[f'kind: {k}, different cities'] = ((P.kind == k) & ~P.same_city).values

rows = []
def run(col, within, label, direction_note):
    real = {k: stat_same(C[col].values, m) for k, m in subsets.items()}
    sims = {k: [] for k in subsets}
    for r in range(NR):
        v = deal(col, within)
        for k, m in subsets.items(): sims[k].append(stat_same(v, m)[0])
    for k in subsets:
        s, n = real[k]; arr = np.array(sims[k]); mu = arr.mean()
        rows.append(dict(attribute=label, subset=k, pairs=n, same=s, share=s / n if n else np.nan, dealt_mean=mu,
                         ratio=s / mu if mu else np.nan, P_more=(np.sum(arr >= s) + 1) / (NR + 1), P_less=(np.sum(arr <= s) + 1) / (NR + 1)))
    log('t3', f'{label} done')

run('animal', 'stratum', 'same animal', '')
C['animal_beast'] = C.animal.where(C.animal != 'none', '')
run('animal_beast', 'stratum', 'same animal (seals with a beast only)', '')
run('stand5', 'stratum', 'same stand letter (unicorns)', '')
run('bin', 'stratum', 'same time bin', '')
C['nstr'] = C.n.astype(str)
run('site', 'nstr', 'same city', '')
# size: mean |log ratio| (lower = more alike)
la = np.log(C.area_mm2.values)
def size_stat(v, m):
    a = v[I]; b = v[J]; ok = ~np.isnan(a) & ~np.isnan(b) & m
    return np.abs(a - b)[ok].mean() if ok.sum() else np.nan, int(ok.sum())
realsz = {k: size_stat(la, m) for k, m in subsets.items()}
simsz = {k: [] for k in subsets}
grp = C.groupby('stratum').indices
for r in range(NR):
    v = la.copy()
    for _, ix in grp.items(): v[ix] = la[ix][rng.permutation(len(ix))]
    for k, m in subsets.items(): simsz[k].append(size_stat(v, m)[0])
for k in subsets:
    s, n = realsz[k]; arr = np.array(simsz[k]); arr = arr[~np.isnan(arr)]
    rows.append(dict(attribute='size gap |log ratio| (lower = more alike)', subset=k, pairs=n, same=np.nan, share=s, dealt_mean=arr.mean() if len(arr) else np.nan,
                     ratio=s / arr.mean() if len(arr) else np.nan, P_more=(np.sum(arr >= s) + 1) / (len(arr) + 1) if len(arr) else np.nan,
                     P_less=(np.sum(arr <= s) + 1) / (len(arr) + 1) if len(arr) else np.nan))
log('t3', 'size done')
# Pa: same building -> differ in animal OR stand
def differ_stat(an, st, m):
    a1, b1, a2, b2 = an[I], an[J], st[I], st[J]
    ok = (a1 != '') & (b1 != '') & m
    diff = (a1 != b1) | ((a2 != '') & (b2 != '') & (a2 != b2))
    return int((diff & ok).sum()), int(ok.sum())
for k in ['all pairs', 'same building', 'same city, other building', 'different cities']:
    m = subsets[k]; s, n = differ_stat(C.animal.values, C.stand5.values, m); arr = []
    for r in range(2000):
        an = deal('animal', 'stratum'); st = np.where(an == 'unicorn', deal('stand5', 'stratum'), '')
        arr.append(differ_stat(an, st, m)[0])
    arr = np.array(arr)
    rows.append(dict(attribute='differ in animal or stand', subset=k, pairs=n, same=s, share=s / n if n else np.nan, dealt_mean=arr.mean(),
                     ratio=s / arr.mean() if arr.mean() else np.nan, P_more=(np.sum(arr >= s) + 1) / 2001, P_less=(np.sum(arr <= s) + 1) / 2001))
V = pd.DataFrame(rows); V.to_csv(f'{OUT}/vary.csv', index=False)
pd.set_option('display.width', 250)
print(V.round(3).to_string(index=False))

# ---------------- second catalogue replication (animal = field-symbol code)
MS = pd.read_csv(f'{OUT}/mah_sets.csv', dtype=str).fillna('')
P2 = pd.read_csv(f'{ROOT}/work_data/mahadevan_parsed.csv', dtype=str).fillna('')
from mah_common import field_symbol
allm = P2[(P2.cls == 'seal')].drop_duplicates('textnum').copy()
allm['code'] = [field_symbol(f)[0] or 'none' for f in allm.fs]
MS['code'] = [field_symbol(f)[0] or 'none' for f in MS.fs]
MS['L'] = MS.L.astype(int)
code_by = dict(zip(allm.textnum, allm.code)); strat = {t: f'{s}|{n}' for t, s, n in zip(allm.textnum, allm.site, allm.n)}
pr = []
for t, g in MS.groupby('mtext'):
    for a, b in itertools.combinations(list(g.textnum), 2): pr.append((a, b, g.site.iloc[0] if g.site.nunique() == 1 else 'x', ))
pool = collections_d = {}
import collections
bystr = collections.defaultdict(list)
for tn, c in code_by.items(): bystr[strat[tn]].append(tn)
real = sum(code_by[a] == code_by[b] for a, b, _ in pr)
arr = []
for r in range(NR):
    newc = {}
    for st, tns in bystr.items():
        vals = [code_by[t] for t in tns]; perm = rng.permutation(len(vals))
        for t, k in zip(tns, perm): newc[t] = vals[k]
    arr.append(sum(newc[a] == newc[b] for a, b, _ in pr))
arr = np.array(arr)
print(f'\nSECOND CATALOGUE: twin pairs {len(pr)}; same field symbol {real} ({real/len(pr):.1%}); dealt within site x length {arr.mean():.1f}; ratio {real/arr.mean():.2f}; P_more {(np.sum(arr>=real)+1)/(NR+1):.4f}; P_less {(np.sum(arr<=real)+1)/(NR+1):.4f}')
