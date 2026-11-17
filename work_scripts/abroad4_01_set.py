#!/usr/bin/env python3
"""STEP 1 of abroad4: the set of objects found outside the Indus region, row by row.
PREDICTIONS (written before running): 41 core objects (16 Gulf faces, 11 Mesopotamia, 11 Iran, 3 Central Asia); 7 more
round/cylinder seals at site Unknown; the second catalogue adds a handful of West-Asian lines with no Lipi partner.
Round seals are about 60% of the core seals and mostly carry the short-horned bull (Gaur).
Output: work_data/abroad4/foreign_set.csv
"""
from abroad4_common import *
rows = []
for r in F[F.tier.isin(['core', 'unk_round'])].itertuples():
    why = ('Lipi region = ' + r.region) if r.tier == 'core' else 'Lipi site Unknown, round/cylinder seal (overseas shape); no findspot'
    rows.append(dict(id=r.id, tier=r.tier, site=r.site, region=r.region, kind=r.kind, shape='round' if r.round else ('square' if r.kind == 'seal' else r.type),
                     type=r.type, animal=r.animal or r.symbol, material=r.material, complete=r.complete, text='-'.join(r.tok), why=why))
# second catalogue West-Asian lines with no partner
Mw = M[(M.site == 'WA') & (~M.partnered)]
for r in Mw.itertuples():
    rows.append(dict(id=f'M{r.textnum}', tier='M_only', site='West Asia (Mahadevan)', region='West Asia', kind=r.kind, shape='?', type=r.cls, animal='', material='',
                     complete=r.complete, text='-'.join(r.tok), why='second catalogue site WA, no partner in Lipi'))
S = pd.DataFrame(rows); S.to_csv(f'{OUT4}/foreign_set.csv', index=False)
pd.set_option('display.width', 250, 'display.max_rows', 200, 'display.max_colwidth', 50)
print(S.to_string())
print(S.groupby(['tier', 'kind', 'shape']).size())
core = S[S.tier == 'core']; print(core.groupby('region').size())
hr = F[(F.tier == 'home') & F['round']]
print('home round seals (type C/CY, Indus region):', len(hr)); print(hr[['id','site','area-section','block-house','room-grid','animal','complete']].assign(text=[ '-'.join(t) for t in hr.tok]).to_string())
