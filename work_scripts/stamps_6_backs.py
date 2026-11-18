#!/usr/bin/env python3
"""STAMPS step 6: the back of the sealing (what it was pressed on) against the kind of stamp.
Prediction written before the counts: the soft-package subtype (TAG:L, the subtype of the cloth-backed Umma sealing)
carries the quantity stamps and the agent (jar + man) stamps more than other impressions; plain-backed round tokens
(TAG:P) carry names and offices, not quantities.
BACKS_SEEN = what the back photographs in the CISI image set show (looked at one by one on 2026-11-17).
"""
import pandas as pd, re
from scipy.stats import fisher_exact
OUT = '/home/antigravity/Cuuper22/ivc/work_data/stamps'
BACKS_SEEN = {
 'L-162': ('TAG:B', 'straight edge and corner: wooden box'), 'L-168': ('TAG:B', 'curved profile wrapped over an edge: box lid'),
 'M-1383': ('TAG:R', 'impression sits on the shoulder of a large storage jar (whole-jar photo)'),
 'H-830': ('TAG:P', 'smooth flat round back: no packing'), 'L-220': ('TAG:P', 'smooth flat round back: no packing'),
 'M-427': ('TAG:P', 'smooth round back, small central dimple'), 'M-437': ('TAG:P', 'smooth flat square back'),
 'M-426': ('TAG:W', 'flat back'), 'Rgr-3': ('TAG:W', 'broad channel across the back: pressed over a rod or peg'),
 'M-1391': ('TAG:O', 'flat back'), 'L-146': ('TAG:O', 'ridged back (cane packing, published)'),
 'M-1427': ('TAG:O', 'waisted, bobbin-shaped lump'),
 'L-124': ('TAG:L', 'rough lumpy back'), 'K-80': ('TAG:L', 'wrinkled fibrous back: cloth or sack'),
 'K-85': ('TAG:L', 'parallel ridges: reeds or cords bundled'), 'M-1388': ('TAG:L', 'crossing lines: cord or weave'),
 'M-429': ('TAG:L', 'raised square block with crossing edges: tied knot or cord'),
 'L-190': ('TAG', 'long straight groove: cord or stick'), 'L-143': ('TAG', 'striated layers: cloth folds or reeds'),
 'K-69': ('TAG', 'flat bar edge (one of seven copies of one text)'),
}
pd.DataFrame([dict(cisi=k, type=v[0], back=v[1]) for k, v in BACKS_SEEN.items()]).to_csv(f'{OUT}/backs_seen.csv', index=False)
I = pd.read_csv(f'{OUT}/impressions.csv', dtype=str).fillna('')
cnt = I.signs.str.contains(r'(?:^|-)(?:001|002|003|004|005|016|031|033|034)-(?:156|390|405|407|700)(?:-|$)')
agent = I.signs.str.contains('740-090')
L = I.type == 'TAG:L'
for nm, m in [('count line ([number][thing])', cnt), ('agent (jar + man)', agent)]:
    a, b = int((m & L).sum()), int((~m & L).sum()); c, d = int((m & ~L).sum()), int((~m & ~L).sum())
    print(f'{nm}: on TAG:L {a} of {a+b}; on other impressions {c} of {c+d}; Fisher P {fisher_exact([[a,b],[c,d]])[1]:.2g}')
print(I[cnt][['cisi', 'type', 'site', 'signs']].to_string(index=False))
P = I.type == 'TAG:P'
print('TAG:P texts:', ' ; '.join(I[P].signs))
