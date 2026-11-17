#!/usr/bin/env python3
"""Orientation test: is each abroad text better explained as home order (reading = stored reversed) or mirrored (reading = stored)?
Sign position profile (front half / back half in reading order) learned on home seals; score = sum of log odds."""
import math, collections, random
from abroad_seals import *
hs=home[home.type.str.startswith('SEAL')]
def halves(t):
    n=len(t); return [(s,'F' if i<n/2-0.5 else 'B' if i>n/2-0.5 else 'M') for i,s in enumerate(t)]
def prof(rows):
    c=collections.defaultdict(lambda:[0,0])
    for t in rows:
        t=[x for x in t if x!='000']
        if len(t)<2: continue
        for s,h in halves(t):
            if h=='F': c[s][0]+=1
            elif h=='B': c[s][1]+=1
    return c
def llr(t,c):
    # >0 means home order (A) favoured
    t=[x for x in t if x!='000']
    if len(t)<2: return 0.0
    tot=0
    for s,h in halves(t):
        if h=='M': continue
        f,b=c.get(s,[0,0]) if s in c else [0,0]
        lf=math.log((f+0.5)/(f+b+1)); lb=math.log((b+0.5)/(f+b+1))
        tot+= (lb-lf) if h=='B' else (lf-lb)
    return tot
if __name__=='__main__':
    # validation: train on home non-Mohenjo, test on Mohenjo seals complete, 3+ signs
    full=hs.copy(); full['rd']=full.text.apply(rd)
    tr=full[full.site!='Mohenjo-daro'].rd; te=full[(full.site=='Mohenjo-daro')&(full.complete=='Y')].rd
    c=prof(tr); te=[t for t in te if len([x for x in t if x!='000'])>=3]
    ok=sum(llr(t,c)>0 for t in te); ok2=sum(llr(t[::-1],c)<0 for t in te)
    print('validation Mohenjo seals',len(te),'home order wins',ok,'mirrored copy loses',ok2)
    # all home, by dir
    call=prof(full.rd)
    for dr,g in full.groupby('dir.'):
        tt=[t for t in g.rd if len([x for x in t if x!='000'])>=3]
        if len(tt)>=10: print('home dir',dr,len(tt),'home-order wins',sum(llr(t,call)>0 for t in tt))
    print()
    for catg in ['square','round','other']:
        print('==',catg)
        for r in ab[ab.cat==catg].itertuples():
            t=r.rd; n=len([x for x in t if x!='000'])
            if n<2: continue
            l=llr(t,call)
            print(f'{r.id:7} {r.site:16} n={n} dir={d.loc[r.Index,"dir."]:4} llr={l:+.2f} -> {"HOME order" if l>0 else "MIRRORED" if l<0 else "tie"} | reading {"-".join(t)}')
