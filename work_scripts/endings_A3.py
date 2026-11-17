#!/usr/bin/env python3
"""A3: the sign right before each ending; sub-endings; which name last-signs are 'jar names', 'spear names', 'porter names'."""
import pandas as pd, numpy as np, collections
R='/home/claude/ivc'
d=pd.read_csv(f'{R}/work_data/endings/A2_seals.csv',dtype=str,keep_default_na=False)
for c in ['face']: d[c]=pd.to_numeric(d[c],errors='coerce')
d=d[~d.name.str.contains('000|ALT')].copy()
d['last']=d.name.str.split('-').str[-1]; d['first']=d.name.str.split('-').str[0]
d['sub']=np.where(d.E=='porter',d.toks.str.split('-').str[-1] if False else d.endsub,d.E)
d['sub']=[ (e if e!='porter' else 'p'+s) for e,s in zip(d.E,d.endsub)]
print(d['sub'].value_counts())
sh=pd.read_csv(f'{R}/work_data/sign_shapes.csv',dtype=str,index_col=0).shape_description
ct=pd.crosstab(d['last'],d['sub']); ct['n']=ct.sum(axis=1)
ct=ct[ct.n>=6].sort_values('n',ascending=False)
ct['shape']=[sh.get(i,'')[:34] for i in ct.index]
print(ct.to_string())
# share of seals whose last name sign decides ending 100%
d2=d[d['last'].isin(ct.index)]
best=d2.groupby('last')['E'].agg(lambda s: s.value_counts().iloc[0]/len(s))
print('signs (>=6 seals) where one ending covers >=90%:',(best>=.9).sum(),'of',len(best))
# purity: predict ending from last sign (leave-one-out majority) vs overall majority
from collections import Counter
def loo(df,key):
    ok=0;n=0
    for k,gp in df.groupby(key):
        c=Counter(gp.E)
        for e in gp.E:
            c[e]-=1
            if sum(c.values())>0:
                pred=c.most_common(1)[0][0]; ok+=pred==e; n+=1
            c[e]+=1
    return ok,n
print('leave-one-out ending prediction by last sign',loo(d,'last'),' by first sign',loo(d,'first'),' by whole name',loo(d,'name'))
print('majority baseline',d.E.value_counts(normalize=True).iloc[0])
# ending vs rest, on seals where last sign is rare vs common
d.to_csv(f'{R}/work_data/endings/A3_seals.csv',index=False)
# fish before spear
fish={'220','233','240','235','231','226'}
for e in ['spear','jar','porter','comb','jar+man']:
    x=d[d.E==e]; print(e,len(x),'last name sign a fish',round(x['last'].isin(fish).mean(),3),'name has a fish anywhere',round(x.name.map(lambda s:any(t in fish for t in s.split('-'))).mean(),3))
x=d[(d.E=='spear')]; print('spear last-sign top',x['last'].value_counts().head(12).to_dict()); print('spear first-sign top',x['first'].value_counts().head(8).to_dict())
