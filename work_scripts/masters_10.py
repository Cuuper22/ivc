"""Part 2: tablet-head X's against the trench they come from and the cup count on the back."""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from masters_common import *
from collections import Counter
import numpy as np, random
H=pd.read_csv('/home/claude/ivc/work_data/masters/tablet_heads.csv',dtype=str,keep_default_na=False)
H=H[H.grp=='tablet'].copy()
def cup(b):
    for s in b.split('|'):
        t=s.split('-')
        if '700' in t:
            i=t.index('700')
            for j in (i-1,i+1):
                if 0<=j<len(t) and t[j] in('031','032','033','034','036'): return int(t[j][-1])
            return 0
    return None
H['cup']=H.back.map(cup)
H['tr']=H['area-section']
# all cup tablets in the corpus by trench: faces with 700 and count
allc=[]
for obj,g in D[D.type.str.startswith('TAB')].groupby('object'):
    for t,i in zip(g.reading_order_text,g.id):
        c=cup(t)
        if c: allc.append((obj,i,c))
AC=pd.DataFrame(allc,columns=['object','id','cup']).merge(M[['id','area-section']],on='id')
print('cup tablets',len(AC)); print(pd.crosstab(AC['area-section'],AC.cup).loc[lambda d:d.sum(axis=1)>=15].to_string())
# heads with a cup back
HC=H[H.cup.notna()&(H.cup>0)]
print('tablet heads with a counted cup back',len(HC))
for X,g in HC.groupby('X'):
    if len(g)>=4:
        trs=Counter(g.tr)
        # compare to the trench's own cup distribution
        base=AC[AC['area-section'].isin(trs)]
        print(X,'n',len(g),'cups',dict(Counter(g.cup)),'trenches',dict(trs),'| base same trenches cup',dict(Counter(base.cup)))
# X purity of cup within X vs shuffle
X=HC.X.values; c=HC.cup.values
def purity(X,c):
    s=0;n=0
    for x in set(X):
        k=Counter(c[X==x]); 
        if sum(k.values())>=2: s+=max(k.values()); n+=sum(k.values())
    return s/n,n
obs=purity(X,c); sims=[purity(X,np.random.permutation(c))[0] for _ in range(500)]
print('cup-count purity within X (X with >=2 tablets):',obs,'shuffle mean',np.mean(sims),'max',max(sims))
# same within trench shuffle
tr=HC.tr.values; sims2=[]
for _ in range(500):
    cc=c.copy()
    for t in set(tr):
        idx=np.where(tr==t)[0]; cc[idx]=np.random.permutation(c[idx])
    sims2.append(purity(X,cc)[0])
print('shuffle within trench: mean',np.mean(sims2),'max',max(sims2),'p',(sum(s>=obs[0] for s in sims2)+1)/501)
# X vs trench purity
def trpur(X,tr):
    s=0;n=0
    for x in set(X):
        k=Counter(tr[X==x])
        if sum(k.values())>=2: s+=max(k.values()); n+=sum(k.values())
    return s/n,n
Hh=H[H.noun.isin(['090','400'])]
Xs=Hh.X.values; trs=Hh.tr.values
o=trpur(Xs,trs); sm=[trpur(Xs,np.random.permutation(trs))[0] for _ in range(500)]
print('X(jar man/comb) vs trench purity',o,'shuffle',np.mean(sm),max(sm))
