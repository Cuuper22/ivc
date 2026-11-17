#!/usr/bin/env python3
"""A2: each ending against seal size, animal, material, type, zone, period, region, name length, crest type."""
import pandas as pd, numpy as np, collections, random
from scipy import stats
R='/home/claude/ivc'
d=pd.read_csv(f'{R}/work_data/endings/A_seals.csv',dtype=str,keep_default_na=False)
for c in ['face','hmm','vmm']: d[c]=pd.to_numeric(d[c],errors='coerce')
d['th']=pd.to_numeric(d['thickness(mm)'],errors='coerce')
d['clean']=~d.name.str.contains('000|ALT')
d['animal']=d.symbol.str.split(':').str[0].replace({'':'none','-':'none','None':'none'})
d['animal']=d.animal.replace({'Bult':'Bull1','Bull':'Bull1'})
top=d.animal.value_counts().index[:6]; d['animal6']=np.where(d.animal.isin(top),d.animal,'other')
d['mat']=d.material.str.lower().replace({'-':'unk','terracotta':'terracotta'})
d['per']=np.where(d.period.isin(['Early','Intermediate','Late']),d.period,np.where(d.time.str.startswith('Period'),d.time.str.extract(r'(Period \w)')[0].fillna(''),'unk'))
d['per']=d.per.replace('', 'unk')
d['zone']=np.where(d.site.isin(['Mohenjo-daro','Harappa'])&(d['area-section']!='--'),d.site.str[0]+':'+d['area-section'],'')
d['fishcrest']=np.where(d.nlen.astype(int)>=2,np.where(d.crest.isin(['235','240','233','231']),'fish-crest','other-crest'),'one-sign')
d['E']=d.E.replace({'jar':'jar','jar+man':'jar+man'})
ENDS=['jar','jar+man','spear','porter','comb']
d=d[d.E.isin(ENDS)]
print(len(d)); 
rows=[]
for e in ENDS:
    x=d[d.E==e]; rows.append(dict(ending=e,n=len(x),face_med=x.face.median(),face_n=x.face.notna().sum(),thick_med=x.th.median(),
      steatite=(x.mat=='steatite').mean(),faience=(x.mat=='faience').mean(),clay=(x.mat=='clay').mean(),copper=(x.mat=='copper').mean(),
      typeR=(x.type=='SEAL:R').mean(),shape_square=(x['shape']=='square').mean(),animal_any=(x.animal!='none').mean(),
      unicorn=(x.animal=='Bull1').mean(),site_MD=(x.site=='Mohenjo-daro').mean(),site_H=(x.site=='Harappa').mean(),
      lower_indus=(x.region=='Lower Indus').mean(),name_len=x.nlen.astype(int).mean(),
      len1=(x.nlen.astype(int)==1).mean(),fishcrest=(x.fishcrest=='fish-crest').mean()))
T=pd.DataFrame(rows).round(3); print(T.T.to_string()); T.to_csv(f'{R}/work_data/endings/A2_covariates.csv',index=False)
# animal distribution
print(pd.crosstab(d.E,d.animal6,normalize='index').round(2))
print(pd.crosstab(d.E,d.per,normalize='index').round(2))
print(pd.crosstab(d.E,d.mat).T)
# permutation P for categorical association (chi-square statistic, permuting ending labels), Cramer V
def chi_codes(a,b,na,nb):
    ct=np.zeros((na,nb)); np.add.at(ct,(a,b),1)
    ct=ct[ct.sum(1)>0][:,ct.sum(0)>0]
    e=np.outer(ct.sum(1),ct.sum(0))/ct.sum()
    return ((ct-e)**2/e).sum(),min(ct.shape)-1
def perm(var,n=3000,seed=0):
    x=d[d[var]!='']
    a=pd.factorize(x.E)[0]; b=pd.factorize(x[var])[0]
    obs,df=chi_codes(a,b,a.max()+1,b.max()+1); V=np.sqrt(obs/(len(x)*df))
    rng=np.random.default_rng(seed); k=0
    for _ in range(n):
        k+=chi_codes(rng.permutation(a),b,a.max()+1,b.max()+1)[0]>=obs
    return len(x),round(V,3),(k+1)/(n+1)
print('variable, n, CramerV, perm P')
out=[]
for v in ['animal6','mat','type','shape','per','region','site','fishcrest','nlen','zone']:
    r=perm(v); out.append((v,)+r); print(v,r)
# face area kruskal and pairwise
fa={e:d[(d.E==e)&d.face.notna()].face.values for e in ENDS}
print('Kruskal face',stats.kruskal(*fa.values()))
for a in ENDS:
    for b in ENDS:
        if a<b: print(a,b,round(np.median(fa[a])),round(np.median(fa[b])),'MWU p',round(stats.mannwhitneyu(fa[a],fa[b]).pvalue,4))
pd.DataFrame(out,columns=['var','n','V','P']).to_csv(f'{R}/work_data/endings/A2_assoc.csv',index=False)
d.to_csv(f'{R}/work_data/endings/A2_seals.csv',index=False)
