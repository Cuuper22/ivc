"""A4: every non-(opener+2) count context for 861/817/820, listed with object info."""
import warnings; warnings.filterwarnings('ignore')
from dm_common import *
d=load()
out=[]
for r in d.itertuples():
    t=r.toks
    for i,x in enumerate(t):
        if x in('861','817','820'):
            b=lab(t[i-1]) if i>0 else None; a=lab(t[i+1]) if i+1<len(t) else None
            kind=None
            if a and not (a=='S2' and i==0): kind=f'{x} then {a}'
            if b: kind=f'{b} then {x}'
            if kind and not (i==0 and a=='S2'):
                out.append((x,kind,r.cisi,r.type,r.site,r._5,r.material,' '.join(t)))
O=pd.DataFrame(out,columns=['sign','ctx','cisi','type','site','area','mat','text'])
O.to_csv(f'{ROOT}/work_data/diamond_counts_contexts.csv',index=False)
for s in ['861','817','820']:
    X=O[O.sign==s]; print('\n',s,len(X)); print(X.ctx.value_counts().to_dict())
    print(X[~X.ctx.isin([f'{s} then S2',f'S3 then {s}'])][['ctx','cisi','type','site','text']].head(40).to_string())
# tablets: 861/817/820 as the ONLY thing on a face
print()
for s in ['861','817','820']:
    f=d[d.istab&d.toks.map(lambda t:s in t and len(t)<=2)]
    print(s,'faces <=2 signs on tablets',len(f),collections.Counter(' '.join(t) for t in f.toks).most_common(8))
