#!/usr/bin/env python3
"""HANDS step 1: unfinished stones. Written 2026-11-17, predictions BEFORE any photo was opened.
RULE (fixed first): pool A = seal faces with a photo on disk, catalogue animal field empty ('none' = symbol blank, not '-'),
and the shape and size of an animal seal: catalogue type SEAL:S (square), or measured sides both >= 15 mm with long/short
side ratio <= 1.35. Bars (rectangular, ratio > 1.35), cylinders and round seals are out. Fragments are kept (they go to
'cannot tell' or 'broken'). Catalogue has NO free-text note and no unfinished/blank/recut code: type codes are only
SEAL:S/R/C/CY/L; so the rule is shape and size only. If pool A > 80, 80 are drawn with random.seed(1701).
Pool B (the (d) side, animal cut / text empty): seal faces with a photo, an animal, and a text that is entirely lost
(only 000 / ALT signs); up to 20 drawn with random.seed(1702).
PREDICTIONS (written before looking): of pool A, 6-12 will be unfinished (a: text cut, animal field smooth), most of the
rest inscription-only by design (b) or worn (c); (d) animal-cut / text-empty will be 0-2 in pool B (a:d at least 4:1, so
text is cut first). Unfinished ones will be SCATTERED in houses, not in workshop clusters, with Lothal the one city
over-represented (>= 3 of the (a) ones against ~2.9 by share of pool). Within-site shuffle will not make the clusters
look unusual (P > 0.1)."""
import sys; sys.path.insert(0, "/home/antigravity/Cuuper22/ivc/work_scripts")
from hands_common import *
S = load(); S['n'] = S.n.astype(int)
A = S[(S.photo != '') & (S.animal == 'none')].copy()
mx = np.maximum(A.hmm_f, A.vmm_f); mn = np.minimum(A.hmm_f, A.vmm_f); A['ratio'] = mx / mn
A = A[(A.type == 'SEAL:S') | ((mn >= 15) & (A.ratio <= 1.35))].copy()
print('pool A', len(A), A.site.value_counts().to_dict())
random.seed(1701)
idx = sorted(A.index.tolist()); random.shuffle(idx); idx = idx[:80]
A = A.loc[sorted(idx)]
B = S[(S.photo != '') & (~S.animal.isin(['none', ''])) & S.signs.map(lambda s: bool(s) and all(t in ('000', 'ALT') for t in s.split('-')))].copy()
print('pool B', len(B))
random.seed(1702)
bi = sorted(B.index.tolist()); random.shuffle(bi); B = B.loc[sorted(bi[:20])]
A['pool'] = 'A'; B['pool'] = 'B'
C = pd.concat([A, B])
C['cand'] = range(1, len(C) + 1)
C[['cand', 'pool', 'cisi', 'site', 'area', 'house', 'building', 'animal', 'type', 'hmm', 'vmm', 'signs', 'preservation', 'photo']].to_csv(f'{OUT}/cand_list.csv', index=False)
items = [(f"#{r.cand} {r.cisi} {r.site[:4]} {r.hmm}x{r.vmm}", r.photo) for r in C.itertuples()]
for k in range(0, len(items), 8):
    sheet(items[k:k + 8], f'{OUT}/cand_sheet_{k//8+1:02d}.jpg', cols=4, W=300, H=300)
print(len(items), 'sheets', (len(items) + 7) // 8)
