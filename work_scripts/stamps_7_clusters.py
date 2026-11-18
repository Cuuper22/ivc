#!/usr/bin/env python3
"""STAMPS step 7: redesign of P4 (receiver or own-stores?).  Prediction kept from P4: Lothal SRG 3GX 10 and Kalibangan
KLB-1 hold MORE different texts than the same number of complete impression faces drawn from the other impression
places; DK-G fewer.  Redesign: distinct complete texts in the cluster against 5,000 draws of the same number of
complete impression faces from all other areas (each other area contributes its faces; repeats inside a place count).
New idea: impression texts that name a house (a crest) at Lothal against Lothal's own seals: how many of the crests
stamped in the warehouse square are crests of Lothal seals?
"""
import numpy as np, pandas as pd
OUT = '/home/antigravity/Cuuper22/ivc/work_data/stamps'; rng = np.random.default_rng(53)
I = pd.read_csv(f'{OUT}/impressions.csv', dtype=str).fillna(''); I['lost'] = I.lost.astype(int)
C = I[(I.lost == 0) & (I.area != '')]
for (site, area) in [('Lothal', 'SRG 3GX 10'), ('Kalibangan', 'KLB-1'), ('Mohenjo-daro', 'DKG. (S)'), ('Harappa', 'FTrench 43'), ('Mohenjo-daro', 'DK')]:
    g = C[(C.site == site) & (C.area == area)]; rest = C[~((C.site == site) & (C.area == area))].signs.values
    k = len(g); real = g.signs.nunique()
    dr = np.array([len(set(rng.choice(rest, k, replace=False))) for _ in range(5000)])
    print(f'{site} {area}: {k} complete faces, {real} different texts; draws from other places {dr.mean():.2f} '
          f'(P fewer-or-equal {(dr <= real).mean():.4f}, P more-or-equal {(dr >= real).mean():.4f})')
O = pd.read_csv(f'{OUT}/objects.csv', dtype=str).fillna('')
NA = pd.read_csv('/home/antigravity/Cuuper22/ivc/work_data/registry/names_all.csv', dtype=str).fillna('')
cr = dict(zip(NA.face_id, NA.crest))
L = I[I.site == 'Lothal']; Ls = O[(O.site == 'Lothal') & (O.tier == 'seal')]
ci = {cr.get(f, '') for f in L.face} - {''}; cs = {cr.get(f, '') for f in Ls.face} - {''}
allseal = {cr.get(f, '') for f in O[O.tier == 'seal'].face} - {''}
print(f'Lothal impressions name {len(ci)} crests; {len(ci & cs)} of them on Lothal seals ({sorted(ci & cs)}); '
      f'{len(ci & allseal)} on seals anywhere; Lothal seals carry {len(cs)} crests')
print('crests on Lothal impressions:', sorted(ci))
