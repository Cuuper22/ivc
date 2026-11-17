"""B1: two-sign 'count X' faces (tablets, pots, tags): which signs behave like the cup; bare counts on pots."""
import warnings; warnings.filterwarnings('ignore')
from dm_common import *
d=load()
face=d[~d.broken&~d.lost].copy()
face['n']=face.toks.map(len)
# bare count faces: single count-sign text
bare=face[(face.n==1)&face.toks.map(lambda t:t[0] in CNT)]
bare['lab']=bare.toks.map(lambda t:lab(t[0]))
print('BARE one-count texts by type (complete)'); print(pd.crosstab(bare.type,bare.lab))
pots=face[face.ispot]
print('pots complete',len(pots),'lengths',pots.n.value_counts().sort_index().to_dict())
# pot 2-token texts "count X" or "X count"
pc=collections.Counter()
for t in pots.toks:
    if len(t)==2:
        if t[0] in CNT: pc[('n',lab(t[0]),t[1])]+=1
        elif t[1] in CNT: pc[('x',t[0],lab(t[1]))]+=1
print('POT 2-token count+sign',pc.most_common(25))
# every 2-token 'count sign' face on tablets and non-pots
pc2=collections.Counter()
for r in face[face.istab|(face.type.str.startswith('TAG'))].itertuples():
    t=r.toks
    if len(t)==2 and t[0] in CNT and t[1] not in CNT: pc2[(t[1],lab(t[0]))]+=1
bysign=collections.defaultdict(dict)
for (s,c),n in pc2.items(): bysign[s][c]=n
rows=sorted(bysign.items(),key=lambda kv:-sum(kv[1].values()))[:25]
print('\nTABLET/TAG 2-token faces [count][sign], by sign')
for s,cs in rows: print(s,sum(cs.values()),dict(sorted(cs.items(),key=lambda z:-z[1])))
# generalise: any text ending in "count sign" where count full-height & sign terminal on tablets: sign x F-count incl. longer faces
pc3=collections.defaultdict(collections.Counter)
for r in face[face.istab].itertuples():
    t=r.toks
    if len(t)>=2 and t[-2] in CNT and t[-1] not in CNT:
        pc3[t[-1]][lab(t[-2])]+=1
print('\ntablet faces ending in [count][sign]: sign, total, F5/F6 cases')
for s,c in sorted(pc3.items(),key=lambda kv:-sum(kv[1].values()))[:20]: print(s,sum(c.values()),dict(c))
print('\nsigns appearing with F5/F6/F7 before them anywhere')
c5=collections.defaultdict(collections.Counter)
for r in d.itertuples():
    t=r.toks
    for i in range(1,len(t)):
        if t[i-1] in('035','036') and t[i] not in CNT: c5[t[i]][lab(t[i-1])]+=1
    for i in range(0,len(t)-1):
        if t[i+1] in('035','036') and t[i] not in CNT: c5[t[i]]['after-'+lab(t[i+1])]+=1
for s,c in sorted(c5.items(),key=lambda kv:-sum(kv[1].values()))[:15]: print(s,dict(c))
