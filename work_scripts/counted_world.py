"""Tie counted things to metadata: for each counted sign, enrichment of object type / material / site / area / animal
among objects where it is counted, against all objects in the corpus (and against all objects carrying the sign).
Prints top over-represented attributes with binomial p. Output work_data/counted/world_<frame>.csv"""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from counted_common import *
from scipy.stats import binomtest
d=pd.read_csv(f'{ROOT}/work_data/counted/instances_resolved.csv',dtype=str,keep_default_na=False)
allr=pd.read_csv(DATA,dtype=str,keep_default_na=False)
def norm(df):
    df=df.copy()
    df['type']=df['type'].str.split(':').str[0]
    df['area']=df['site']+'|'+df['area-section']
    df['animal']=df['symbol'].str.split(':').str[0]
    return df
allr=norm(allr); d=norm(d)
d['mat']=d['material']; allr['mat']=allr['material']
attrs=['type','mat','site','area','animal']
out=[]
for frame in('B','A'):
    X=d[d.frame==frame].drop_duplicates(['id','sign'])   # one hit per object per sign
    cnt=X.sign.value_counts()
    for s in cnt[cnt>=12].index:
        Y=X[X.sign==s]; n=len(Y)
        for a in attrs:
            base=allr[a].value_counts(normalize=True)
            for v,k in Y[a].value_counts().items():
                if v in('-','--','|--','None') or k<4: continue
                p0=base.get(v,0)
                p=binomtest(k,n,p0,alternative='greater').pvalue
                out.append(dict(frame=frame,sign=s,n=n,attr=a,val=v,k=k,share=round(k/n,3),base=round(p0,3),lift=round(k/n/p0,2),p=p))
W=pd.DataFrame(out); W.to_csv(f'{ROOT}/work_data/counted/world_enrich.csv',index=False)
S=W[(W.p<0.002)&(W.lift>1.6)].sort_values(['frame','sign','p'])
pd.set_option('display.width',250)
print(S.to_string(index=False))
