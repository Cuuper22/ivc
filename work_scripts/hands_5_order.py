#!/usr/bin/env python3
"""HANDS step 4: 40 seals for the making order. Written 2026-11-17. Rule: seal faces with a photo, an animal, square (SEAL:S),
preservation 'complete', condition Fair/Good/Fine, 3+ signs, none lost; stratified draw seed 2201: 18 Mohenjo-daro, 8 Harappa,
6 Lothal, 4 Kalibangan, 4 Chanhu-daro (fewer if a city lacks them; the rest filled from Mohenjo-daro). For each: (1) CRAMPED:
text cramped against the animal (signs squeezed, run into horns or back, animal untouched) = animal first; animal cramped under
the text (animal shrunk, legs/back flattened, clipped by the text band, text band sits clear and even) = text first; neither
= even; (2) GUIDE: a ruled line or scratch under the text or around the field; (3) ERASED: a ghost sign, a doubled stroke or a
patch. Predictions (written first): text first 15-25 of 40, animal first at most 5, rest even; guide lines in at most 4;
erased/ghost signs in at most 3."""
import sys; sys.path.insert(0, "/home/claude/ivc/work_scripts")
from hands_common import *
S = load(); S['n'] = S.n.astype(int)
E = S[(S.photo != '') & (~S.animal.isin(['none', ''])) & (S.type == 'SEAL:S') & (S.preservation == 'complete') & S.condition.isin(['Fair', 'Good', 'Fine'])
      & (S.n >= 3) & (S.lost == '0')].drop_duplicates('cisi')
quota = {'Mohenjo-daro': 18, 'Harappa': 8, 'Lothal': 6, 'Kalibangan': 4, 'Chanhu-daro': 4}
random.seed(2201); pick = []
for s, q in quota.items():
    ids = list(E[E.site == s].index); random.shuffle(ids); pick += ids[:q]
rest = [i for i in E[E.site == 'Mohenjo-daro'].index if i not in pick]; random.shuffle(rest)
pick += rest[:40 - len(pick)]
P = E.loc[pick].copy(); P = P.sample(frac=1, random_state=2202); P['oid'] = [f'Z{k:02d}' for k in range(1, len(P) + 1)]
P[['oid', 'cisi', 'site', 'animal', 'n', 'signs', 'hmm', 'vmm', 'photo']].to_csv(f'{OUT}/order_key.csv', index=False)
print(len(P), P.site.value_counts().to_dict())
items = [(f'{r.oid} ({r.n} signs)', r.photo) for r in P.itertuples()]
for k in range(0, 40, 8): sheet(items[k:k+8], f'{OUT}/order_sheet_{k//8+1}.jpg', cols=4, W=300, H=300)
