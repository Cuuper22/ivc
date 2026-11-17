"""A1: every count that goes with 861, 817, 820; where; interchangeability."""
from dm_common import *
d=load()
SIG=['861','817','820']
rows=[]
for r in d.itertuples():
    t=r.toks
    for i,x in enumerate(t):
        if x in SIG:
            nxt=t[i+1] if i+1<len(t) else 'END'
            nxt2=t[i+2] if i+2<len(t) else 'END'
            prv=t[i-1] if i>0 else 'START'
            rows.append(dict(id=r.id,cisi=r.cisi,sign=x,pos=i,n=len(t),prev=prv,nxt=nxt,nxt2=nxt2,site=r.site,type=r.type,mat=r.material,symbol=r.symbol,sides=r.sides,broken=r.broken,lost=r.lost))
O=pd.DataFrame(rows); O.to_csv(f'{ROOT}/work_data/diamond_occ.csv',index=False)
print('occurrences',len(O),O.sign.value_counts().to_dict())
# after-count
O['after']=O.nxt.map(lambda x:lab(x) or ('END' if x=='END' else 'other'))
O['before']=O.prev.map(lambda x:lab(x) or ('START' if x=='START' else 'other'))
print('\nAFTER (count immediately after sign, reading order)')
print(pd.crosstab(O.sign,O.after))
print('\nBEFORE (count immediately before sign)')
print(pd.crosstab(O.sign,O.before))
print('\nposition (0=first)'); print(pd.crosstab(O.sign,O.pos.clip(upper=4)))
print('\nby type x sign'); print(pd.crosstab(O.type,O.sign))
# restrict to seals: full text count signatures
for s in SIG:
    X=O[(O.sign==s)&(O.type.str.startswith('SEAL'))]
    print('\n',s,'seals',len(X),'after',X.after.value_counts().to_dict())
    # as opener (pos 0) vs elsewhere
    Y=X[X.pos==0]; print(' pos0 n',len(Y),Y.after.value_counts().to_dict())
    Z=X[X.pos>0]; print(' pos>0 n',len(Z),Z.after.value_counts().to_dict())
# two-stroke opener: what follows the count
print('\nWhat follows opener+count (seals, pos0)')
for s in SIG:
    X=O[(O.sign==s)&(O.pos==0)&(O.after=='S2')]
    print(s,len(X),X.nxt2.value_counts().head(12).to_dict())
# on tablets: contexts
print('\nTablets contexts')
for s in SIG:
    X=O[(O.sign==s)&(O.type.str.startswith('TAB'))]
    print(s,len(X),'after',X.after.value_counts().to_dict(),'before',X.before.value_counts().to_dict(),'n',X.n.value_counts().to_dict())
# other count after sign in non-strokes (e.g., 861 F counts)
for s in SIG:
    X=O[O.sign==s]
    print(s,'all-count-after',X.after.value_counts().to_dict())
# where: site/type
for s in SIG:
    X=O[O.sign==s]; print(s,X.site.value_counts().head(6).to_dict(),X.type.value_counts().head(6).to_dict(),X.mat.value_counts().head(4).to_dict())
