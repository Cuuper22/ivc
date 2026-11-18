#!/usr/bin/env python3
"""SPOTS lead 3, redesign of (c): copies removed, and does the amount follow depth?
Plain words: in (c) 20 identical copies of one tablet count as 190 pairs and swamp everything. Here each (name face,
amount face, trench) counts ONCE. Question 1: among distinct (name, amount, trench) triples, do names with 2+ triples
show different amounts more or less than chance (amounts mixed among triples of the same site)? Question 2: for the
name 176-740-400 (31 records), does the cup count move with depth (Spearman rank correlation, P by shuffling depths)?
PREDICTION: an account running over time means the amount changes with depth: negative or positive Spearman with P<0.1.
Writes work_data/spots/s3b_log.txt.
"""
import pandas as pd, numpy as np, re
from scipy.stats import spearmanr
ROOT='/home/antigravity/Cuuper22/ivc'; OUT=f'{ROOT}/work_data/spots'
LOG=open(f'{OUT}/s3b_log.txt','w')
def say(*a):
    s=' '.join(str(x) for x in a); print(s,flush=True); LOG.write(s+'\n')
O=pd.read_csv(f'{OUT}/s3_objects.csv',dtype={'obj':str}).fillna('')
N=O[(O.types=='amount+name')&(O.lostfree)&(O.name_face!='')&(O.amt_face!='')].copy()
def cups(a):
    m=re.findall(r'\d{3}',a); v={'032':2,'033':3,'034':4,'002':2,'003':3,'004':4,'001':1,'031':1}
    return sum(v.get(x,0) for x in m if x!='700')
N['cups']=N.amt_face.map(cups); N['place']=N.site+'|'+N.area
T=N.drop_duplicates(['name_face','amt_face','place']).copy()
say(f'distinct (name, amount, trench) triples: {len(T)} from {len(N)} records')
def same_diff(df):
    s=d=0
    for n,g in df.groupby('name_face'):
        a=list(g.amt_face)
        for i in range(len(a)):
            for j in range(i+1,len(a)):
                s+=a[i]==a[j]; d+=a[i]!=a[j]
    return s,d
s0,d0=same_diff(T); rng=np.random.default_rng(1); nl=[]
for t in range(3000):
    X=T.copy()
    for st,ix in X.groupby('site').groups.items(): X.loc[ix,'amt_face']=rng.permutation(X.loc[ix,'amt_face'].values)
    nl.append(same_diff(X)[0])
nl=np.array(nl)
say(f'pairs of triples with one name: same amount {s0}, different {d0}; shuffled same-amount {nl.mean():.1f} (P high {(1+(nl>=s0).sum())/3001:.4f}, P low {(1+(nl<=s0).sum())/3001:.4f})')
g=N[(N.name_face=='176-740-400')&(N.depth_ft!='')].copy(); g['depth_ft']=g.depth_ft.astype(float)
r,p=spearmanr(g.depth_ft,g.cups)
nl=np.array([spearmanr(rng.permutation(g.depth_ft.values),g.cups)[0] for _ in range(3000)])
say(f'176-740-400: {len(g)} records with depth; cups by depth Spearman {r:+.3f}, shuffle P two-sided {(1+(abs(nl)>=abs(r)).sum())/3001:.4f}')
for c,gg in g.groupby('cups'): say(f'   cups {c}: n {len(gg)}, depth median {gg.depth_ft.median():.1f} ft, range {gg.depth_ft.min():.1f}-{gg.depth_ft.max():.1f}')
# all same-name groups with depth: pooled within-name rank correlation
rows=[]
for n,gg in N[N.depth_ft!=''].assign(depth_ft=lambda x:x.depth_ft.astype(float)).groupby('name_face'):
    if len(gg)>=4 and gg.cups.nunique()>=2:
        rr=spearmanr(gg.depth_ft,gg.cups)[0]; rows.append((n,len(gg),rr))
say('names with 4+ depth-dated records and 2+ amounts:',[(n,k,round(rr,2)) for n,k,rr in rows])
# formats: do moulded (B) and incised (I) copies of the same signature sit in the same trench?
say('176-740-400 records by format and amount:',dict(N[N.name_face=='176-740-400'].groupby(['type','amt_face']).size()))
LOG.close()
