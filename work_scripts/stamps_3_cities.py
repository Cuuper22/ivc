#!/usr/bin/env python3
"""STAMPS step 3: texts of 4+ signs shared between cities, and the second catalogue as a replication.
Prediction (written before running): P5 in stamps_2 (Mohenjo-daro-Harappa most links in raw count; against corpus
sizes Mohenjo-daro with the outer towns over-linked).  P6: in the second catalogue too, a sealing's exact seal twin
(3+ signs) lies in another city more often than a random seal of that length would.
Link: a complete text (no lost sign) of 4+ signs on a SEAL in city A and on a seal or impression in city B (A != B).
Chance: the city labels of all complete 4+ sign seal and impression faces are dealt at random among those faces
(5,000 deals); expected links per city pair = mean over deals.  This keeps every city's size and every text's count.
Writes work_data/stamps/city_texts.csv, city_links.csv; stdout -> log_3.txt
"""
import collections, itertools, time
import numpy as np, pandas as pd
ROOT = '/home/claude/ivc'; OUT = f'{ROOT}/work_data/stamps'
T0 = time.time()
def log(*a): print(f'[stamps_3 {time.time()-T0:6.1f}s]', *a, flush=True)
rng = np.random.default_rng(23)
O = pd.read_csv(f'{OUT}/objects.csv', dtype=str).fillna('')
O['n'] = O.n.astype(int); O['lost'] = O.lost.astype(int)
F = O[O.tier.isin(['seal', 'sealing', 'stamped pot']) & (O.lost == 0) & (O.n >= 4) & (O.site != 'Unknown')].copy()
F['is_seal'] = F.tier == 'seal'
log(f'{len(F)} complete faces of 4+ signs ({F.is_seal.sum()} seals)')

def links(sites, isseal, texts):
    by = collections.defaultdict(lambda: [set(), set()])
    for s, k, t in zip(sites, isseal, texts):
        by[t][1].add(s)
        if k: by[t][0].add(s)
    L = collections.Counter()
    for t, (sealc, allc) in by.items():
        for a in sealc:
            for b in allc:
                if a < b or (b not in sealc and a != b):
                    L[tuple(sorted((a, b)))] += 1
    return L, by
real, by = links(F.site.values, F.is_seal.values, F.signs.values)
rows = []
for t, (sc, ac) in by.items():
    if len(ac) >= 2 and sc:
        g = F[F.signs == t]
        rows.append(dict(text=t, cities=' / '.join(sorted(ac)), seal_cities=' / '.join(sorted(sc)),
                         where=' ; '.join(f'{r.site}:{r.tier}:{r.cisi}:{r.area or "-"}' for r in g.itertuples())))
CT = pd.DataFrame(rows).sort_values('cities'); CT.to_csv(f'{OUT}/city_texts.csv', index=False)
print(f'texts of 4+ signs on a seal in one city and a seal or impression in another: {len(CT)}')
print(CT[['text', 'cities', 'where']].to_string(index=False))
sites = F.site.values.copy(); acc = collections.defaultdict(list)
for rep in range(5000):
    L, _ = links(rng.permutation(sites), F.is_seal.values, F.signs.values)
    for k in set(real) | set(L): acc[k].append(L.get(k, 0))
    if rep % 1000 == 0: log(f'deal {rep}')
rows = []
for k in acc:
    a = np.array(acc[k] + [0] * (5000 - len(acc[k])))
    rows.append(dict(city_a=k[0], city_b=k[1], links=real.get(k, 0), expected=round(a.mean(), 2),
                     ratio=round(real.get(k, 0) / a.mean(), 2) if a.mean() > 0 else np.nan, P_ge=(a >= real.get(k, 0)).mean()))
CL = pd.DataFrame(rows).sort_values(['links', 'expected'], ascending=False)
CL = CL[(CL.links > 0) | (CL.expected >= 0.5)]
CL.to_csv(f'{OUT}/city_links.csv', index=False)
print('\nCity pairs: links against city-label deals'); print(CL.to_string(index=False))
tot = sum(real.values()); A = np.array([sum(v[i] for v in acc.values() if i < len(v)) for i in range(5000)])
print(f'all cross-city links {tot}; deals mean {A.mean():.1f}, P(deal >= real) {(A >= tot).mean():.4f}')
print('faces per city in the 4+ sign set:', F.site.value_counts().head(10).to_dict())

# ---- replication on the second catalogue (Mahadevan 1977): sealing lines against seal lines
M = pd.read_csv(f'{ROOT}/work_data/mahadevan_parsed.csv', dtype=str).fillna('')
M = M[(M.complete == 'True') & (~M.reading_lipi.str.contains('000'))]
M['n'] = M.n.astype(int)
Ms = M[M.cls == 'seal']; Mi = M[(M.cls == 'sealing') & (M.site != 'HP')]
Mi_hp = M[(M.cls == 'sealing') & (M.site == 'HP')]
st = Ms.groupby('reading_lipi').site.apply(set).to_dict()
lenshare = Ms.groupby('n').site.value_counts(normalize=True)
for nm, X in [('sealings outside Harappa', Mi), ('Harappa "sealings" (mostly moulded tablets)', Mi_hp)]:
    for nmin in (2, 3):
        Y = X[(X.n >= nmin) & X.reading_lipi.isin(st)]
        same = sum(r.site in st[r.reading_lipi] for r in Y.itertuples())
        exp = np.mean([lenshare.get((r.n, r.site), 0) for r in Y.itertuples()]) if len(Y) else np.nan
        print(f'second catalogue, {nm}, {nmin}+ signs: {len(Y)} of {(X.n >= nmin).sum()} have an exact seal twin; '
              f'twin in the same city for {same}; a random seal of that length is in that city {exp*100:.1f}% of the time')
        if nmin == 3:
            for r in Y.itertuples(): print(f'    {r.textnum} {r.site} {r.reading_lipi} -> seal cities {sorted(st[r.reading_lipi])}')
log('done step 3')
