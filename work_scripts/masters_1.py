"""Part 1: every X in `X jar <noun>`; agents per X, cities, animals, sizes. Writes work_data/masters/agents.csv"""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from masters_common import *
from collections import Counter
rows=[]
for r in D.itertuples():
    t=r.toks
    if t.count('740')!=1: continue
    j=t.index('740'); op,pre=split_open(t[:j])
    rows.append(dict(id=r.id,site=r.site,type=r.type,X='-'.join(pre),nxt=t[j+1] if j+1<len(t) else '',after='-'.join(t[j+1:]),opener=opener_type(op),sym=r.symbol,face=r.face,period=r.period,text=r.reading_order_text,cisi=r.cisi,mat=r.material))
R=pd.DataFrame(rows)
R['seal']=R.type.str.startswith('SEAL')
R.to_csv('/home/antigravity/Cuuper22/ivc/work_data/masters/jar_texts.csv',index=False)
NOUNS={'090':'man','400':'comb','679':'679','621':'621'}
A=R[R.nxt.isin(NOUNS)&(R.X!='')&~R.X.str.contains('000')].copy()
A['noun']=A.nxt.map(NOUNS)
A.to_csv('/home/antigravity/Cuuper22/ivc/work_data/masters/agents.csv',index=False)
own=R[(R.nxt=='')&(R.X!='')&~R.X.str.contains('000')]
print('agent objects',len(A),'distinct X',A.X.nunique(),'owner objects',len(own),'distinct X',own.X.nunique())
for n in NOUNS.values():
    a=A[A.noun==n]; c=a.X.value_counts()
    print(n,'objects',len(a),'X',a.X.nunique(),'X with 1:',(c==1).sum(),'X with>=2:',(c>=2).sum(),'>=3:',(c>=3).sum(),'cities of X>=2',)
a=A[A.noun=='man']; c=a.X.value_counts()
print(c.head(40))
# cumulative share
print('top5 share',c.head(5).sum()/len(a),'top10',c.head(10).sum()/len(a))
for x in c.index[:25]:
    s=a[a.X==x]; print(x,len(s),dict(Counter(s.site)),dict(Counter(s.sym)),dict(Counter(s.opener)),round(s.face.median()))
# first sign / last sign of X
print('first sign',a.X.str.split('-').str[0].value_counts().head(12).to_dict())
print('last sign',a.X.str.split('-').str[-1].value_counts().head(12).to_dict())
print('X length',a.X.str.count('-').add(1).value_counts().to_dict())
