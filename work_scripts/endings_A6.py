#!/usr/bin/env python3
"""A6: size controlled for sign count; do houses (Mohenjo-daro area+block-house) keep one ending or mix?"""
import pandas as pd, numpy as np, collections, re
from scipy import stats
R='/home/claude/ivc'
d=pd.read_csv(f'{R}/work_data/endings/A5_seals.csv',dtype=str,keep_default_na=False)
d['face']=pd.to_numeric(d.face,errors='coerce'); d['ntok']=d.reading_order_text.str.split('-').str.len()
x=d[d.face.notna()&d.E.isin(['jar','jar+man','spear','porter','comb'])].copy()
# face against sign count within each ending (OLS by hand) and ending residuals
x['lf']=np.log(x.face)
import numpy.linalg as la
X=pd.get_dummies(x.E)[['jar','jar+man','spear','porter','comb']].astype(float)
X['ntok']=x.ntok.astype(float)
b=la.lstsq(X.values,x.lf.values,rcond=None)[0]; res=dict(zip(X.columns,b))
print('log face ~ ending + sign count: ending intercepts (exp, mm2 at 0 signs) and slope per sign',{k:round(np.exp(v),1) if k!='ntok' else round(v,3) for k,v in res.items()})
for e in ['jar+man','spear','porter','comb']:
    base=res['jar']; print(e,'vs jar, same sign count: face x',round(np.exp(res[e]-base),3))
# sign count by ending
print(x.groupby('E').ntok.agg(['mean','median','count']).round(2))
# median face within sign count 4,5,6
for k in (3,4,5,6):
    row={e:((round(x[(x.E==e)&(x.ntok==k)].face.median()) if ((x.E==e)&(x.ntok==k)).any() else None),len(x[(x.E==e)&(x.ntok==k)])) for e in ['jar','jar+man','spear','porter','comb']}
    print('signs',k,row)
# houses
h=d[(d.house!='')&d.E.isin(['jar','jar+man','spear','porter','comb'])].copy()
h['dep']=h.depth.map(lambda s:(lambda m: float(m.group(0)) if m else np.nan)(re.search(r'-?\d+\.?\d*',s)))
h['dband']=(h.dep.abs()//3).fillna(-1)
h['E1']=h.E.replace({'jar+man':'jar'})
g=h.groupby('house'); multi=[k for k,v in g if len(v)>=2]
print('MD houses with ending known:',g.ngroups,' with >=2 seals:',len(multi))
mixed=[k for k in multi if h[h.house==k].E1.nunique()>=2]
print('houses mixing endings (jar/spear/porter/comb):',len(mixed))
# shuffle labels among seals of same area and depth band
rng=np.random.default_rng(0)
key=(h['area-section']+'|'+h.dband.astype(str)).values; lab=h.E1.values; hs=h.house.values
def count_mixed(l):
    dd=collections.defaultdict(set); cc=collections.Counter(hs)
    for a,b in zip(hs,l): dd[a].add(b)
    return sum(1 for k in dd if cc[k]>=2 and len(dd[k])>=2)
obs=count_mixed(lab); idx=collections.defaultdict(list)
for i,k in enumerate(key): idx[k].append(i)
sims=[]
for _ in range(2000):
    l=lab.copy()
    for k,ii in idx.items(): l[ii]=rng.permutation(lab[ii])
    sims.append(count_mixed(l))
print('houses mixing: observed',obs,'shuffled within area+depth band mean',round(np.mean(sims),1),'P(sim<=obs)',round(np.mean(np.array(sims)<=obs),3))
# pair level: two seals in one house, same ending?
def pairs(l):
    s=t=0
    for k in multi:
        ii=np.where(hs==k)[0]
        for a in range(len(ii)):
            for b in range(a+1,len(ii)): t+=1; s+=l[ii[a]]==l[ii[b]]
    return s,t
o=pairs(lab); sp=[]
for _ in range(2000):
    l=lab.copy()
    for k,ii in idx.items(): l[ii]=rng.permutation(lab[ii])
    sp.append(pairs(l)[0])
print('house-mate pairs same ending: observed',o,'shuffled mean',round(np.mean(sp),1),'P(sim>=obs)',round(np.mean(np.array(sp)>=o[0]),3))
# non-jar pairs: both spear/porter/comb in same house (same non-jar ending)
for e in ['spear','porter','comb']:
    n=sum(1 for a,b in [(i,j) for k in multi for i in np.where(hs==k)[0] for j in np.where(hs==k)[0] if i<j] if lab[a]==e and lab[b]==e)
    ns=[]
    for _ in range(1000):
        l=lab.copy()
        for k,ii in idx.items(): l[ii]=rng.permutation(lab[ii])
        ns.append(sum(1 for k in multi for i in np.where(hs==k)[0] for j in np.where(hs==k)[0] if i<j and l[i]==e and l[j]==e))
    print(e,'both seals of a house carry',e,': observed',n,'shuffled',round(np.mean(ns),2),'P',round(np.mean(np.array(ns)>=n),3))
# house table
rows=[]
for k in multi:
    v=h[h.house==k]; rows.append(dict(house=k,n=len(v),endings=dict(collections.Counter(v.E)),cisi=' '.join(v.cisi)))
H=pd.DataFrame(rows).sort_values('n',ascending=False); H.to_csv(f'{R}/work_data/endings/A6_houses.csv',index=False)
print(H[H.endings.map(lambda e: len([k for k in e if k!='jar'])>0).astype(bool)].head(40).to_string(index=False))
# house size (seals in the house, from all seals, not only ending) vs ending share
allh=d[d.house!=''].groupby('house').size()
h['housesize']=h.house.map(allh)
print(h.groupby('E1').housesize.agg(['mean','median','count']).round(2))
