"""B3: the 'big number + 2 jars + tally' faces next to cup faces; cup count vs the big number; pots with jar counts."""
import warnings; warnings.filterwarnings('ignore')
from dm_common import *
d=load()
T=d[d.istab&(d.cisi!='-')]
rows=[]
for cisi,g in T.groupby('cisi'):
    cup=None; jar=None
    for toks in g.toks:
        for i,x in enumerate(toks):
            if x=='700' and i>0 and lab(toks[i-1]) and lab(toks[i-1]).startswith('F'): cup=int(lab(toks[i-1])[1])
            if x=='740' and i>1 and toks[i-1]=='032': jar=toks[i-2]
    if jar: rows.append((cisi,cup,jar,g['area-section'].iloc[0],' | '.join(' '.join(t) for t in g.toks)))
J=pd.DataFrame(rows,columns=['cisi','cup','bignum','area','faces'])
print(len(J)); print(pd.crosstab(J.bignum,J.cup.fillna(0)))
# all contexts of 'X 032 740' on every object type, X distribution
c=collections.Counter(); 
for r in d.itertuples():
    t=r.toks
    for i in range(2,len(t)):
        if t[i]=='740' and t[i-1]=='032': c[(t[i-2],r.type[:3])]+=1
print(c.most_common(20))
# jar counts anywhere on tablets by n
jc=collections.Counter()
for r in d[d.istab].itertuples():
    t=r.toks
    for i in range(1,len(t)):
        if t[i]=='740' and t[i-1] in CNT: jc[lab(t[i-1])]+=1
print('tablet jar counts',dict(sorted(jc.items())))
# 25-29 signs contexts
for r in d.itertuples():
    t=r.toks
    if any(x in('025','026','027','028','029') for x in t): print(r.cisi,r.type,r.site,' '.join(t))
