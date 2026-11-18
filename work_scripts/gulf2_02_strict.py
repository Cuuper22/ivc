#!/usr/bin/env python3
"""gulf2 step 2: person-sign test using only the texts where a man sign is clear on the page or stated by the authors
(G2-09 two men drawn clearly, G2-13 Jalalabad authors name #90, G2-14 BM photo). Same matched-home draw as gulf2_01 over the 12 texts of set A."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from abroad4_common import *
import csv
rows=[r for r in csv.DictReader(open('/home/antigravity/Cuuper22/ivc/work_data/gulf2/sequences.csv')) if r['dup_status']=='new' and 'pseudo' not in r['flag'] and len([t for t in r['signs_best'].split('-') if t and t!='-'])>=2]
lens=[len(r['signs_best'].split('-')) for r in rows]
hd=[x for x,v in home_distinct.items() if v[1]=='seal' and len([s for s in x if real(s)])>=2]
bylen=collections.defaultdict(list)
for x in hd: bylen[min(len([s for s in x if real(s)]),9)].append(x)
rng=np.random.default_rng(5); sims=[]
for _ in range(20000):
    sims.append(sum(any(s in('090','091') for s in bylen[min(L,9)][rng.integers(len(bylen[min(L,9)]))]) for L in lens))
sims=np.array(sims)
for k in (3,4,9):
    print(f'P(home draw of {len(lens)} matched texts holds a person sign in >= {k}) = {(np.sum(sims>=k)+1)/(len(sims)+1):.5f}; mean {sims.mean():.2f}')
