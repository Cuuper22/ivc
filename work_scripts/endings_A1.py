#!/usr/bin/env python3
"""A. Endings: which names take which ending; do names take several. Output printed + work_data/endings/A1_*.csv"""
import pandas as pd, numpy as np, random, collections
R='/home/antigravity/Cuuper22/ivc'
d=pd.read_csv(f'{R}/work_data/endings/faces.csv',dtype=str,keep_default_na=False)
for c in ['face','hmm','vmm']: d[c]=pd.to_numeric(d[c],errors='coerce')
d['jarman']=d.jarman=='True'; d['isseal']=d.isseal=='True'
t=d.toks=d.reading_order_text.str.split('-')
# man alone as closer (plain person class)
def e2(r):
    if r.end!='none': return r.end
    tk=r.toks
    return 'man' if tk and tk[-1]=='090' else 'none'
d['toks']=t
d['E']=d.apply(e2,axis=1)
d.loc[d.jarman,'E']='jar+man'
d.loc[(d.E=='jar')&(d.endsub=='090'),'E']='jar+man'
s=d[d.isseal&d.E.isin(['jar','jar+man','spear','porter','comb','man'])&(d.name!='')].copy()
s['E1']=s.E.replace({'jar+man':'jar'})   # case-level ending
print('seals with name and ending',len(s)); print(s.E.value_counts())
s.to_csv(f'{R}/work_data/endings/A_seals.csv',index=False)
# names with 2+ endings
by=s.groupby('name')
rows=[]
for nm,gp in by:
    if len(gp)>=2 and gp.E1.nunique()>=2:
        rows.append(dict(name=nm,n=len(gp),endings=dict(collections.Counter(gp.E1)),
            seals='; '.join(f"{r.cisi}[{r.E}/{r.site}/{r.area_section if hasattr(r,'area_section') else ''}]" for r in gp.itertuples())))
mix=pd.DataFrame(rows).sort_values('n',ascending=False)
print('names with >=2 seals',(by.size()>=2).sum(),' mixed',len(mix))
mix.to_csv(f'{R}/work_data/endings/A1_mixed_names.csv',index=False)
# chance: shuffle endings among seals (global, and within site)
def nmixed(labels,names):
    gg=collections.defaultdict(set); cnt=collections.Counter(names)
    for n,l in zip(names,labels): gg[n].add(l)
    return sum(1 for n in gg if cnt[n]>=2 and len(gg[n])>=2)
names=list(s.name); lab=list(s.E1)
obs=nmixed(lab,names)
random.seed(1); sims=[]
for _ in range(2000):
    l=lab[:]; random.shuffle(l); sims.append(nmixed(l,names))
print('mixed names obs',obs,'shuffled mean',np.mean(sims),'max',max(sims),'P(sim<=obs)',np.mean(np.array(sims)<=obs))
# within site
sites=list(s.site); idx=collections.defaultdict(list)
for i,x in enumerate(sites): idx[x].append(i)
sims2=[]
for _ in range(2000):
    l=lab[:]
    for x,ii in idx.items():
        v=[lab[i] for i in ii]; random.shuffle(v)
        for i,y in zip(ii,v): l[i]=y
    sims2.append(nmixed(l,names))
print('within-site shuffle mean',np.mean(sims2),'P(sim<=obs)',np.mean(np.array(sims2)<=obs))
# pairs of seals with identical names: same ending rate vs chance
ps=0;pt=0
gg=s.groupby('name').E1.apply(list)
for L in gg:
    for i in range(len(L)):
        for j in range(i+1,len(L)):
            pt+=1; ps+=L[i]==L[j]
p=s.E1.value_counts(normalize=True); print('identical-name seal pairs',pt,'same ending',ps,ps/pt,'chance',(p**2).sum())
# same by last sign and first sign, 2+ sign names
for pos,fn in (('last',lambda x:x.split('-')[-1]),('first',lambda x:x.split('-')[0])):
    ss=s[s.nlen.astype(int)>=2].copy(); ss['k']=ss.name.map(fn)
    ct=pd.crosstab(ss.k,ss.E1); ct=ct[ct.sum(axis=1)>=8]
    print(pos,'sign x ending (signs with >=8 seals)'); print(ct.assign(n=ct.sum(axis=1)).sort_values('n',ascending=False).head(25))
