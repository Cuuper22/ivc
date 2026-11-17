# Where in a seal text do room-mates share signs? Reading order = reverse of stored Lipi order.
# For each slot (1st, 2nd, 3rd read sign ... and last, 2nd-last ...) count same-room pairs that share
# a sign sitting in that slot in both texts, against label shuffles within area x 3-ft depth band.
import csv,collections,re,random
import numpy as np
random.seed(21)
r=list(csv.DictReader(open('research/data/open_prototype/lipi/metadata_filtered.csv',encoding='utf-8')))
freq=collections.Counter()
for x in r:
    for t in set(re.findall(r'\d{3}',x['text'])):
        if t!='000': freq[t]+=1
objs={}
for x in r:
    if x['site']!='Mohenjo-daro' or not x['type'].startswith('SEAL'): continue
    o=objs.setdefault(x['id'].split('.')[0],dict(area=x['area-section'],house=x['block-house'],room=x['room-grid'],toks=[],depth=x['depth'],cisi=x['cisi']))
    o['toks']+=re.findall(r'\d{3}',x['text'])
def dep(s):
    m=re.search(r'(-?\d+(\.\d+)?)\s*ft',s); return float(m.group(1)) if m else None
U=[]
for o in objs.values():
    if o['house'] in('--','-','') or o['room'] in('--','-',''): continue
    rd=o['toks'][::-1]                       # reading order
    if len([t for t in rd if t!='000'])<3 or dep(o['depth']) is None: continue
    o['rd']=rd; o['d']=dep(o['depth']); o['rk']=(o['area'],o['house'],o['room']); U.append(o)
print('seals:',len(U))
CUT=150
def slots(o):
    n=len(o['rd']); out={}
    for i,t in enumerate(o['rd']):
        if t=='000' or freq[t]>CUT: continue
        out.setdefault(t,set()).update({('from_start',min(i+1,5)),('from_end',min(n-i,5)),('any',0),
                                        ('zone','open' if i==0 else 'close' if i==n-1 else 'middle')})
    return out
S=[slots(o) for o in U]
def count(rk):
    idx=collections.defaultdict(list)
    for i,h in enumerate(rk): idx[h].append(i)
    c=collections.Counter()
    for mem in idx.values():
        for a in range(len(mem)):
            for b in range(a+1,len(mem)):
                i,j=mem[a],mem[b]
                if abs(U[i]['d']-U[j]['d'])>5: continue
                keys=set()
                for t in S[i].keys()&S[j].keys(): keys|=S[i][t]&S[j][t]
                for k in keys: c[k]+=1
    return c
rk=[o['rk'] for o in U]
strata=collections.defaultdict(list)
for i,o in enumerate(U): strata[(o['area'],int(o['d']//3))].append(i)
obs=count(rk); null=collections.defaultdict(list)
for t in range(3000):
    p=rk[:]
    for idx in strata.values():
        sh=idx[:]; random.shuffle(sh)
        for i,j in zip(idx,sh): p[i]=rk[j]
    c=count(p)
    for k in obs: null[k].append(c.get(k,0))
print('slot (same slot in both texts), sign on <=%d rows: observed / chance / ratio / P'%CUT)
for k in sorted(obs):
    a=np.array(null[k]); print(f'  {k[0]:10s} {str(k[1]):7s} {obs[k]:3d} {a.mean():6.2f} {obs[k]/a.mean() if a.mean() else float("nan"):6.2f} {(1+np.sum(a>=obs[k]))/3001:.4f}')
# the shared signs themselves, and where they sit
idx=collections.defaultdict(list)
for i,h in enumerate(rk): idx[h].append(i)
shared=collections.Counter()
for mem in idx.values():
    for a in range(len(mem)):
        for b in range(a+1,len(mem)):
            i,j=mem[a],mem[b]
            if abs(U[i]['d']-U[j]['d'])>5: continue
            for t in S[i].keys()&S[j].keys():
                shared[t]+=1; print('   pair',U[i]['cisi'],'-'.join(U[i]['rd']),'|',U[j]['cisi'],'-'.join(U[j]['rd']),'| sign',t,freq[t])
print(shared.most_common())
# do the room-shared signs turn up on seals found abroad?
abroad=[x for x in r if x['region'] in('Persian Gulf','Mesopotamia','Iranian Plateau','Central Asia')]
ab=collections.Counter(t for x in abroad for t in set(re.findall(r'\d{3}',x['text'])) if t!='000')
print('abroad rows',len(abroad),'| room-shared signs seen abroad:',{t:ab[t] for t in shared if ab[t]})
