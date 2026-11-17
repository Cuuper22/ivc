#!/usr/bin/env python3
"""Per-seal orientation decision for round seals, using non-man signs only (man signs would be circular). margin 1.0 log-odds."""
from abroad_orient import *
hs2=hs.copy(); hs2['rd']=hs2.text.apply(rd); call=prof(hs2.rd)
res=[]
for r in ab[ab.cat=='round'].itertuples():
    t=r.rd; core=[x for x in t if x not in MAN]; l=llr(core,call) if len([x for x in core if x!='000'])>=2 else 0.0
    dec='HOME' if l>=1 else 'MIRROR' if l<=-1 else 'undecided'
    final=t if dec!='MIRROR' else t[::-1]
    man=[i for i,x in enumerate(final) if x in MAN]
    res.append((r.id,r.site,d.loc[r.Index,'dir.'],'-'.join(t),round(l,2),dec,'-'.join(final),man,len(final)))
for x in res: print(x)
import collections
print(collections.Counter(x[5] for x in res))
# man position after decision (decided seals only)
c=collections.Counter()
for x in res:
    for i in x[7]:
        n=x[8]; c[(x[5],'first' if i==0 else 'last' if i==n-1 else 'mid')]+=1
print(c)
