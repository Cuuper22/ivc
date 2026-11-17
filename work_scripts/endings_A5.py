#!/usr/bin/env python3
"""A5: head-to-head. Which variable carries information about the ending? Adjusted mutual information
(observed MI minus mean MI after shuffling the ending labels), as a share of the ending's entropy.
 'cases'     -> the name itself (last sign, first sign, whole name) should NOT matter much; free choice
 'office'    -> seal size, animal, house (rank/size of house), name type
 'thing'     -> object type, material, shape, findspot zone, period
Also a multinomial logistic regression with cross-validation as a second view."""
import pandas as pd, numpy as np, collections
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.preprocessing import OneHotEncoder
R='/home/claude/ivc'
d=pd.read_csv(f'{R}/work_data/endings/A3_seals.csv',dtype=str,keep_default_na=False)
for c in ['face']: d[c]=pd.to_numeric(d[c],errors='coerce')
d['E1']=d.E.replace({'jar+man':'jar'})          # case-level ending: jar / spear / porter / comb
fish={'220','233','240','235','231','226'}
d['fishfinal']=d['last'].isin(fish).map({True:'fish',False:'notfish'})
def rare(s,k=5):
    c=s.value_counts(); return s.where(s.map(c)>=k,'rare')
d['last_r']=rare(d['last']); d['first_r']=rare(d['first']); d['name_r']=rare(d.name,3)
d['toklen']=d.reading_order_text.str.split('-').str.len().astype(str)
d['facebin']=pd.qcut(d.face,4,labels=False,duplicates='drop').astype('Int64').astype(str).replace('<NA>','unk')
d['house']=np.where((d.site=='Mohenjo-daro')&(d['block-house']!='--')&(d['area-section']!='--'),d['area-section']+'|'+d['block-house'],'')
d['areaonly']=np.where(d['area-section']!='--',d.site+'|'+d['area-section'],'')
d['depthband']=''
V={'last name sign':'last_r','first name sign':'first_r','whole name':'name_r','fish-final name':'fishfinal','name length':'nlen',
 'text length':'toklen','seal size (quartile)':'facebin','animal':'animal6','object type':'type','material':'mat','shape':'shape',
 'site':'site','region':'region','period':'per','findspot area (MD/H)':'zone','house (MD)':'house'}
def mi(a,b):
    ct=np.zeros((a.max()+1,b.max()+1)); np.add.at(ct,(a,b),1); p=ct/ct.sum()
    pa=p.sum(1,keepdims=True); pb=p.sum(0,keepdims=True); nz=p>0
    return (p[nz]*np.log(p[nz]/(pa@pb)[nz])).sum()
def H(a): 
    p=np.bincount(a)/len(a); p=p[p>0]; return -(p*np.log(p)).sum()
rng=np.random.default_rng(0); rows=[]
for lab,col in V.items():
    x=d[d[col]!=''] if col in('house','zone') else d
    x=x[x[col]!='unk'] if col in ('per',) else x
    a=pd.factorize(x.E1)[0]; b=pd.factorize(x[col])[0]
    o=mi(a,b); sims=[mi(rng.permutation(a),b) for _ in range(300)]
    adj=o-np.mean(sims); p=(np.sum(np.array(sims)>=o)+1)/301
    rows.append((lab,len(x),b.max()+1,round(100*adj/H(a),1),round(p,3)))
T=pd.DataFrame(rows,columns=['variable','n','levels','adj MI as % of ending entropy','perm P']).sort_values('adj MI as % of ending entropy',ascending=False)
print(T.to_string(index=False)); T.to_csv(f'{R}/work_data/endings/A5_adjMI.csv',index=False)
# cross-validated logistic: ending (jar/spear/porter/comb) from feature groups, on seals with clean names
groups={'name (last,first sign,nlen)':['last_r','first_r','nlen'],'fish-final only':['fishfinal'],
 'object (type,material,shape,animal)':['type','mat','shape','animal6'],'findspot+period+site':['site','region','per','zone'],
 'size (face quartile)':['facebin'],'text length':['toklen'],'house (MD)':['house']}
y=pd.factorize(d.E1)[0]; skf=StratifiedKFold(5,shuffle=True,random_state=0)
base=np.bincount(y).max()/len(y)
def logloss(P,y): return -np.mean(np.log(P[np.arange(len(y)),y]+1e-9))
p0=np.bincount(y)/len(y); ll0=-np.mean(np.log(p0[y]))
print('baseline (always jar) accuracy',round(base,3),'null log-loss',round(ll0,3))
res=[]
for g,cols in groups.items():
    x=d if g!='house (MD)' else d[d.house!='']
    yy=pd.factorize(x.E1)[0]
    X=OneHotEncoder(handle_unknown='ignore').fit_transform(x[cols])
    P=cross_val_predict(LogisticRegression(C=0.5,max_iter=2000),X,yy,cv=StratifiedKFold(5,shuffle=True,random_state=0),method='predict_proba')
    pp=np.bincount(yy)/len(yy); l0=-np.mean(np.log(pp[yy]))
    res.append((g,len(x),round((P.argmax(1)==yy).mean(),3),round(np.bincount(yy).max()/len(yy),3),round(l0,3),round(logloss(P,yy),3),round(100*(l0-logloss(P,yy))/l0,1)))
R2=pd.DataFrame(res,columns=['features','n','cv accuracy','majority','null logloss','cv logloss','logloss gain %'])
print(R2.to_string(index=False)); R2.to_csv(f'{R}/work_data/endings/A5_cv.csv',index=False)
d.to_csv(f'{R}/work_data/endings/A5_seals.csv',index=False)
