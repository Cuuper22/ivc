"""Job: the travelled name. Step 5: can an Indus sign group write Meluhha = Dravidian mel-akam ("high place")? Candidate halves: hill/peak signs (503 malai, 480 kunru, 482 kodu, 460/463 three-peaks) + house 803 (il ~ akam). Also: do 2-sign groups of that shape recur, and where.
Also searches the sesame sign 838 (ellu/ilu loan) and carnelian-like commodity contexts. Run: python3 travelled_5_meluhha.py"""
import pandas as pd, collections, numpy as np
from scipy import stats
R='/home/antigravity/Cuuper22/ivc/'
G=pd.read_csv(R+'work_data/gloss2_all.csv',dtype=str)
M=pd.read_csv(R+'research/data/open_prototype/lipi/metadata_filtered.csv',dtype=str)
D=G.merge(M[['id','region']],on='id'); D['toks']=D.reading_order_text.str.split('-')
O=D.drop_duplicates('object'); N=len(O)
hill={'503','480','482','460','463'}
def pairs(t,A,B): return [(t[i],t[i+1]) for i in range(len(t)-1) if t[i] in A and t[i+1] in B]
for A,B,name in [(hill,{'803'},'hill + house 803'),({'803'},hill,'house 803 + hill'),({'900','920'},{'803'},'month/crescent + 803')]:
    objs=set();c=collections.Counter();sites=collections.Counter()
    for o,s,t in zip(D.object,D.site,D.toks):
        pp=pairs(t,A,B)
        if pp and o not in objs:
            objs.add(o); sites[s]+=1
            for p in pp: c[p]+=1
    # expected under independence of adjacency: count of adjacent slots = total adjacent positions
    tot=sum(max(len(t)-1,0) for t in D.toks)
    nA=sum(x in A for t in D.toks for x in t); nB=sum(x in B for t in D.toks for x in t); L=sum(len(t) for t in D.toks)
    exp=nA*nB/L*(tot/L)
    print(name,'objects',len(objs),'pairs',dict(c),'sites',dict(sites),'| expected adjacent pairs under shuffle ~',round(exp,1))
# every 803 neighbour
c=collections.Counter()
for t in D.toks:
    for i,x in enumerate(t):
        if x=='803':
            c[('before',t[i-1] if i else '^')]+=1; c[('after',t[i+1] if i+1<len(t) else '$')]+=1
print('803 neighbours (top)',c.most_common(14))
# sesame sign 838
s=D[D.toks.map(lambda t:'838' in t)]
print('838 sesame objects',s.object.nunique(),collections.Counter(s.type).most_common(5),collections.Counter(s.site).most_common(5))
print(s[['cisi','site','type','reading_order_text']].head(12).to_string(index=False))
# seals that open with the commonest openers and also carry hill-sign: skip
