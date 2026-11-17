"""A3: head-to-head: same body, different opener? same room, same opener? twins 861/817 vs wheel."""
import warnings; warnings.filterwarnings('ignore')
from dm_common import *
from scipy import stats
import random
d=load()
s=d[d.isseal&~d.broken&~d.lost&(d.toks.map(len)>=3)].copy()
def op(t):
    if t[0] in('861','817','820') and len(t)>1 and t[1] in('002','001'): return t[0]+'-'+t[1][-1]
    if t[0] in('861','817','820'): return t[0]+'-?'
    if t[0]=='060' or (t[0] in('920','692','550') and len(t)>1 and t[1]=='060'): return 'CAP'
    return 'none'
s['op']=s.toks.map(op)
def body(t):
    if t[0] in('861','817','820') and len(t)>1 and t[1] in('002','001'): return tuple(t[2:])
    return None
s['body']=s.toks.map(body)
print(s.op.value_counts().to_dict())
# 1. bodies repeated on several seals
B=s[s.body.notna()&(s.body.map(lambda b:b is not None and len(b)>=2))]
grp=B.groupby('body')
multi=[g for _,g in grp if len(g)>=2]
print('bodies (>=2 signs) on >=2 seals',len(multi),'seals',sum(len(g) for g in multi))
same=diff=0
pairs=[]
for g in multi:
    ops=list(g.op)
    for i in range(len(ops)):
        for j in range(i+1,len(ops)):
            pairs.append((ops[i],ops[j]))
same=sum(a==b for a,b in pairs); print('pairs',len(pairs),'same opener',same)
# chance: shuffle openers among all opener-bearing seals
allops=list(B.op)
rates=[]
random.seed(1)
idx=[]
k=0
for g in multi:
    idx.append(list(range(k,k+len(g)))); k+=len(g)
# reindex: build flat in group order
flat=[o for g in multi for o in g.op]
for _ in range(2000):
    sh=flat[:]; random.shuffle(sh); c=0;k=0
    for g in multi:
        n=len(g); o=sh[k:k+n];k+=n
        c+=sum(o[i]==o[j] for i in range(n) for j in range(i+1,n))
    rates.append(c)
print('chance same-opener pairs mean %.1f sd %.1f; observed %d'%(np.mean(rates),np.std(rates),same))
print('pair types',collections.Counter(tuple(sorted(p)) for p in pairs).most_common(12))
# list repeated bodies with differing openers
dd=[(b,list(g.op),list(g.cisi),list(g.site)) for b,g in grp if len(g)>=2 and len(set(g.op))>1]
print('bodies with DIFFERENT openers',len(dd))
for b,o,c,si in dd[:15]: print(' ',' '.join(b),o,c)
# full text duplicates with same opener
# 2. same-room opener sharing (Mohenjo + Harappa trench)
def room(r):
    if r.site=='Mohenjo-daro' and r['block-house'] not in('--','-') :
        return ('M',r['area-section'],r['block-house'],r['room-grid'])
    return None
s['room']=s.apply(room,axis=1)
R=s[s.room.notna()&(s.op!='none')|s.room.notna()]
def paircount(R,key):
    same=tot=0
    for _,g in R.groupby('room'):
        v=list(g[key]); 
        for i in range(len(v)):
            for j in range(i+1,len(v)): tot+=1; same+=(v[i]==v[j])
    return same,tot
for key,label in [('op','opener category (incl none)')]:
    obs=paircount(R,key)
    sims=[]
    for _ in range(500):
        R2=R.copy(); R2[key]=np.random.permutation(R2[key].values); sims.append(paircount(R2,key)[0])
    print(label,'same-room pairs same',obs[0],'of',obs[1],'chance %.1f sd %.1f'%(np.mean(sims),np.std(sims)))
# only opener-bearing pairs
R3=R[R.op!='none']
obs=paircount(R3,'op'); sims=[]
for _ in range(500):
    R2=R3.copy(); R2['op']=np.random.permutation(R2['op'].values); sims.append(paircount(R2,'op')[0])
print('opener-bearing only: same-room pairs same',obs[0],'of',obs[1],'chance %.1f sd %.1f'%(np.mean(sims),np.std(sims)))
# 3. twins vs wheel: counts after
O=pd.read_csv(f'{ROOT}/work_data/diamond_occ.csv',dtype=str,keep_default_na=False)
O['pos']=O.pos.astype(int)
O['after']=O.nxt.map(lambda x:lab(x) or ('END' if x=='END' else 'o'))
for a,b in [('861','817'),('861','820'),('817','820')]:
    X=O[O.sign.isin([a,b])]
    ct=pd.crosstab(X.sign,X.after); chi,p,dof,_=stats.chi2_contingency(ct)
    print(a,b,'after-category chi2 %.1f dof %d p %.3g'%(chi,dof,p))
# restrict to pos-0 seal openers
X=O[(O.pos==0)&O.type.str.startswith('SEAL')]
for a,b in [('861','817'),('861','820'),('817','820')]:
    Y=X[X.sign.isin([a,b])]; ct=pd.crosstab(Y.sign,Y.after.map(lambda x:lab(x) or ('END' if x=='END' else 'o')))
    chi,p,dof,_=stats.chi2_contingency(ct); print('opener seals',a,b,'chi2 %.1f p %.3g'%(chi,p)); print(ct)
# 4. third sign (sign after opener+2) divergence
def third(sig):
    c=collections.Counter()
    for t in s.toks:
        if t[0]==sig and len(t)>2 and t[1]=='002': c[t[2]]+=1
    return c
T={k:third(k) for k in ['861','817','820']}
def jsd(a,b):
    keys=set(a)|set(b);pa=np.array([a[k] for k in keys],float);pb=np.array([b[k] for k in keys],float);pa/=pa.sum();pb/=pb.sum();m=(pa+pb)/2
    kl=lambda p,q:np.sum(p[p>0]*np.log2(p[p>0]/q[p>0]));return .5*kl(pa,m)+.5*kl(pb,m)
import itertools
for a,b in itertools.combinations(T,2):
    obs=jsd(T[a],T[b]); pool=[];
    la=sum(T[a].values()); allv=[k for k,v in (T[a]+T[b]).items() for _ in range(v)]
    sims=[]
    for _ in range(500):
        np.random.shuffle(allv); ca=collections.Counter(allv[:la]); cb=collections.Counter(allv[la:]); sims.append(jsd(ca,cb))
    print('3rd sign JSD',a,b,'obs %.3f shuffle %.3f (sd %.3f)'%(obs,np.mean(sims),np.std(sims)))
print({k:T[k].most_common(8) for k in T})
