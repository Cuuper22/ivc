#!/usr/bin/env python3
"""Name-slot analysis (questions 1-5). Needs work_data/name_rows.csv (name_slot_build.py).
Prints tables; the numbers go into jobs/out/name_slot.md. Name segment = signs between opener block and class block
with roles who/house/house-marker/fixed-ending/phrase/head/second-slot/mark."""
import pandas as pd, numpy as np, collections, random, itertools, math, re
from scipy import stats
random.seed(7); np.random.seed(7)
ROOT='/home/claude/ivc'
o=pd.read_csv(f'{ROOT}/work_data/name_rows.csv',dtype=str).fillna('')
sh=pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv',dtype=str).set_index('lipi_wells_number').shape_description.to_dict()
def S(s): return f'{s} ({sh.get(s,"?")[:38]})'
for c in ['tight','contiguous','has_class']: o[c]=o[c]=='True'
o['seglen']=o.seglen.astype(int); o['nwho']=o.nwho.astype(int)
T=o[o.tight&o.has_class&(o.seglen>=1)].copy()
T['segl']=T.seg.str.split('-')
print('tight seals with a name segment:',len(T),'objects',T.obj.nunique())
# ---------- Q1
print('\n== Q1 lengths'); print(T.seglen.value_counts().sort_index().to_string())
dis=T.drop_duplicates('seg'); print('distinct segments',len(dis))
first=collections.Counter(); last=collections.Counter(); alone=collections.Counter(); allc=collections.Counter(); mid=collections.Counter()
for l in T.segl:
    for s in l: allc[s]+=1
    if len(l)==1: alone[l[0]]+=1
    else:
        first[l[0]]+=1; last[l[-1]]+=1
        for s in l[1:-1]: mid[s]+=1
n_multi=sum(first.values()); print('multi-sign names',n_multi,'single',sum(alone.values()))
def tab(c,k=15,den=None):
    for s,n in c.most_common(k): print(f'  {S(s):55s} {n:4d}  as share of this sign total {n/allc[s]:.2f}')
print('-- name-FIRST (names of 2+ signs)'); tab(first)
print('-- name-LAST (names of 2+ signs)'); tab(last)
print('-- STANDALONE (names of 1 sign)'); tab(alone)
print('-- concentration: first-sign types',len(first),'top5 share',sum(n for _,n in first.most_common(5))/n_multi,
      '; last-sign types',len(last),'top5 share',sum(n for _,n in last.most_common(5))/n_multi)
# enders/starters enrichment: sign with >=8 in multi names, share last vs expectation
print('-- signs in 2+ names, by tendency to END (n>=8 in multi)')
rows=[]
for s in allc:
    m=first[s]+last[s]+mid[s]
    if m>=8: rows.append((last[s]/m,first[s]/m,m,s))
for f,fi,m,s in sorted(rows,reverse=True)[:12]: print(f'  last {f:.2f} first {fi:.2f} n={m} {S(s)}')
print('-- by tendency to START')
for f,fi,m,s in sorted(rows,key=lambda r:-r[1])[:12]: print(f'  first {fi:.2f} last {f:.2f} n={m} {S(s)}')
# ---------- Q2 houses
M=T[(T.site=='Mohenjo-daro')&~T.bh.isin(['--','-',''])].copy()
M['hk']=M.area+'|'+M.bh; M['rk']=M.area+'|'+M.bh+'|'+M.room
def depth(s):
    m=re.search(r'(-?\d+(\.\d+)?)\s*ft',s); return float(m.group(1)) if m else None
def pairs_for(df,key,nulltrials=3000):
    df=df.reset_index(drop=True); L=list(df.segl); n=len(df)
    freq=collections.Counter(s for l in L for s in set(l)); 
    def posset(l):
        d={}
        k=len(l)
        for i,s in enumerate(l):
            d.setdefault(s,set()).add('first' if i==0 else 'last' if i==k-1 else 'mid')
            if k==1: d[s].add('only')
        return d
    P=[posset(l) for l in L]
    def count(keys):
        idx=collections.defaultdict(list)
        for i,h in enumerate(keys): idx[h].append(i)
        c=collections.Counter()
        for m in idx.values():
            for a in range(len(m)):
                for b in range(a+1,len(m)):
                    i,j=m[a],m[b]
                    if L[i]==L[j]: c['whole name']+=1
                    sh=set(P[i])&set(P[j])
                    if sh: c['any shared sign']+=1
                    seen=set()
                    for s in sh:
                        for p in P[i][s]:
                            for q in P[j][s]:
                                if len(L[i])>1 and len(L[j])>1: 
                                    k=(p,q)
                                    if k not in seen: seen.add(k); c[f'multi: {p} in A, {q} in B']+=1
                    if sh and (len(L[i])==1 or len(L[j])==1): c['pair with a one-sign name sharing']+=1
        return c
    keys=list(df[key]); obs=count(keys)
    # shuffle house labels inside area x 3ft depth band strata
    strata=collections.defaultdict(list)
    for i,r in df.iterrows():
        d=depth(r.depth); strata[(r.area,int(d//3) if d is not None else -9)].append(i)
    null=collections.defaultdict(list)
    for t in range(nulltrials):
        p=keys[:]
        for idx in strata.values():
            x=idx[:]; random.shuffle(x)
            for i,j in zip(idx,x): p[i]=keys[j]
        c=count(p)
        for k in obs: null[k].append(c.get(k,0))
    return obs,null
for key,name in [('hk','HOUSE (area+block-house)'),('rk','ROOM (area+block-house+room)')]:
    sub=M[M.groupby(key)['obj'].transform('nunique')>=2]
    print(f'\n== Q2 {name}: seals in groups of 2+: {len(sub)} in {sub[key].nunique()} groups')
    obs,null=pairs_for(sub,key,2000)
    for k in sorted(obs):
        a=np.array(null[k]); print(f'  {k:45s} obs {obs[k]:3d} chance {a.mean():6.2f} ratio {obs[k]/max(a.mean(),1e-9):5.2f}  P {(1+np.sum(a>=obs[k]))/(len(a)+1):.4f}')
# same, but using only the parser's who-sign (name without house slot) is in report; skip
# whole segments occurring on >=3 seals
print('\n== segments on 3+ seals')
g=T.groupby('seg')
big=[]
for s,d in g:
    if d.obj.nunique()>=3: big.append((d.obj.nunique(),s,d))
for n,s,d in sorted(big,key=lambda x:(-x[0],x[1])):
    sites=collections.Counter(d.site); houses=sorted(set((r.area+' '+r.bh).strip() for r in d.itertuples() if r.bh not in('--','-','')))
    print(f'  {n:3d} seals  {s:22s} sites {dict(sites)} houses[{len(houses)}] {houses[:6]}')
print('segments on 3+ seals:',len(big),'covering seals',sum(b[0] for b in big),'of',T.obj.nunique())
multi_site=[(s,d.site.nunique()) for n,s,d in big if d.site.nunique()>1]
print('of those, on 2+ sites:',len(multi_site))
T0=T.drop(columns=['segl'])
allseg=T0.groupby('seg')['obj'].nunique()
ssite=T0.groupby('seg').site.nunique(); sl=pd.Series({k:len(k.split('-')) for k in allseg.index})
print('distinct segments',len(allseg),'| on 2+ seals',int((allseg>=2).sum()),'| on 2+ sites',int((ssite>=2).sum()),'| multi-sign segments on 2+ sites',int(((ssite>=2)&(sl>=2)).sum()),'| multi-sign segments on 2+ seals',int(((allseg>=2)&(sl>=2)).sum()),'| multi-sign on 3+ seals',int(((allseg>=3)&(sl>=2)).sum()))

# ---- Q2 variants: rare signs only, and who-only names
tokfreq=collections.Counter(s for l in T.segl for s in l)
def variant(label,fn,keep=lambda d:d.seglen>=1):
    D=M.copy(); D['segl']=[fn(r) for r in D.itertuples()]; D=D[D.segl.map(len)>=1]
    sub=D[D.groupby('hk')['obj'].transform('nunique')>=2]
    print(f'\n== Q2 variant {label}: HOUSE seals {len(sub)}')
    obs,null=pairs_for(sub,'hk',2000)
    for k in sorted(obs):
        a=np.array(null[k]); print(f'  {k:45s} obs {obs[k]:3d} chance {a.mean():6.2f} ratio {obs[k]/max(a.mean(),1e-9):5.2f}  P {(1+np.sum(a>=obs[k]))/(len(a)+1):.4f}')
variant('rare signs only (<=40 name-slot tokens), order kept',lambda r:[x for x in r.segl if tokfreq[x]<=40])
variant('rare signs only (<=15 tokens)',lambda r:[x for x in r.segl if tokfreq[x]<=15])
variant('who-role signs only',lambda r:[x for x,ro in zip(r.segl,r.segroles.split()) if ro=='who'])
variant('segment minus house-markers 100/760',lambda r:[x for x in r.segl if x not in('100','760')])
T0.to_pickle('/tmp/T.pkl')
