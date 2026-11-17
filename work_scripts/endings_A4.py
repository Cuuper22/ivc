#!/usr/bin/env python3
"""A4: every clean name that occurs with two or more endings (listed), with objects, sites, houses; shuffle test; sign-level."""
import pandas as pd, numpy as np, collections, random
R='/home/claude/ivc'
d=pd.read_csv(f'{R}/work_data/endings/A3_seals.csv',dtype=str,keep_default_na=False)
d['E1']=d.E.replace({'jar+man':'jar'})
d['loc']=d.apply(lambda r: f"{r.site[:5]} {r['area-section']} {r['block-house']}".replace(' -- ',' ').strip() if r.site!='Unknown' else 'unk',axis=1)
by=d.groupby('name')
out=[]
for nm,gp in by:
    if len(gp)>=2 and gp.E1.nunique()>=2:
        c=collections.Counter(gp.E); 
        out.append((nm,len(gp),dict(c),'; '.join(f"{r.cisi}={r.E}({r.loc})" for r in gp.itertuples())))
out.sort(key=lambda x:-x[1])
print('clean names on >=2 seals:',sum(1 for _,g in by if len(g)>=2),' of which with >=2 endings (jar+man merged into jar):',len(out))
rows=[]
for nm,n,c,s in out:
    print(nm,n,c); print('   ',s[:400])
    rows.append(dict(name=nm,n=n,endings=c,seals=s))
pd.DataFrame(rows).to_csv(f'{R}/work_data/endings/A4_mixed_names_clean.csv',index=False)
# shuffle: how many multi-seal names mix, vs shuffled endings
names=list(d.name); lab=list(d.E1); cnt=collections.Counter(names)
def nm(l):
    g=collections.defaultdict(set)
    for n,x in zip(names,l): g[n].add(x)
    return sum(1 for n in g if cnt[n]>=2 and len(g[n])>=2)
obs=nm(lab); rng=random.Random(2); sims=[]
for _ in range(2000):
    l=lab[:]; rng.shuffle(l); sims.append(nm(l))
print('mixed names obs',obs,'shuffled mean',round(np.mean(sims),1),'range',min(sims),max(sims))
# the same, only names whose seals are all non-jar capable: count non-jar endings among repeats
nj=d[d.E1!='jar']; print('seals with spear/porter/comb',len(nj),'names among them seen on another seal:',sum(1 for n in nj.name.unique() if cnt[n]>=2))
# for names that carry a non-jar ending on one seal: does another seal with the same name carry the same ending?
same=diff=0
for n,gp in d.groupby('name'):
    if len(gp)<2: continue
    for i,r in enumerate(gp.itertuples()):
        if r.E1=='jar': continue
        others=[x.E1 for j,x in enumerate(gp.itertuples()) if j!=i]
        same+=sum(o==r.E1 for o in others); diff+=sum(o!=r.E1 for o in others)
print('for each spear/porter/comb seal, other seals with the identical name: same ending',same,' different',diff)
# chance of "same" if the others were drawn at random from all seals
p=d.E1.value_counts(normalize=True); print(p.round(3).to_dict())
tot=same+diff
for e in ['spear','porter','comb']:
    s=0;t=0
    for n,gp in d.groupby('name'):
        if len(gp)<2: continue
        L=list(gp.E1)
        for i,x in enumerate(L):
            if x!=e: continue
            for j,y in enumerate(L):
                if j!=i: t+=1; s+=y==e
    print(e,'seal with identical-name partner: partner has same ending',s,'of',t,'=',round(s/max(t,1),3),'; base rate',round(p[e],3))
