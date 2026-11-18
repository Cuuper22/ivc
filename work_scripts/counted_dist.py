"""Count distributions per counted thing: BEFORE (n X) and AFTER (X n) frames, series split.
Writes work_data/counted/before_table.csv, after_table.csv"""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from counted_common import *
import numpy as np
from scipy.stats import chi2_contingency
rows=load(); sh=shapes()
B=collections.defaultdict(collections.Counter); Af=collections.defaultdict(collections.Counter)
occ=collections.Counter(); seen=set()
for r,toks,broken in rows:
    for i,s in enumerate(toks):
        occ[s]+=1
        if s in CNT or s in('ALT','000'): continue
        if i>=1 and label(toks[i-1]): B[s][label(toks[i-1])]+=1
        if i+1<len(toks) and label(toks[i+1]): Af[s][label(toks[i+1])]+=1
labs=['S1','S2','S3','S4','S5','S6','S7','T2','T3','T4','T5','T6','T7','T8','F1','F2','F3','F4','F5','F6','A']
for name,T in(('before',B),('after',Af)):
    out=[]
    for s,c in T.items():
        n=sum(c.values())
        r=dict(sign=s,shape=sh.get(s,'')[:50],occ=occ[s],n=n,rate=round(n/occ[s],3))
        for l in labs:r[l]=c.get(l,0)
        r['S']=sum(c[l] for l in labs if l[0]=='S');r['T']=sum(c[l] for l in labs if l[0]=='T');r['F']=sum(c[l] for l in labs if l[0]=='F')
        out.append(r)
    df=pd.DataFrame(out).sort_values('n',ascending=False); df.to_csv(f'{ROOT}/work_data/counted/{name}_table.csv',index=False)
    print('=====',name); 
    print(df[df.n>=8][['sign','shape','occ','n','rate']+labs].to_string(index=False))
