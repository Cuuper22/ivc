# Do room-mates / house-mates share the sign written right before the closing jar sign (Lipi 740)?
# Reading order = reverse of stored order, so the jar is stored first and the sign before it is stored second.
import csv,collections,re,random
import numpy as np
random.seed(31)
r=list(csv.DictReader(open('research/data/open_prototype/lipi/metadata_filtered.csv',encoding='utf-8')))
objs={}
for x in r:
    if x['site']!='Mohenjo-daro' or not x['type'].startswith('SEAL'): continue
    o=objs.setdefault(x['id'].split('.')[0],dict(area=x['area-section'],house=x['block-house'],room=x['room-grid'],toks=[],depth=x['depth'],cisi=x['cisi'],sym=x['symbol']))
    o['toks']+=re.findall(r'\d{3}',x['text'])
def dep(s):
    m=re.search(r'(-?\d+(\.\d+)?)\s*ft',s); return float(m.group(1)) if m else None
U=[]
for o in objs.values():
    t=o['toks']
    if o['house'] in('--','-','') or len(t)<3 or t[0]!='740' or t[1]=='000' or dep(o['depth']) is None: continue
    o['pre']=t[1]; o['d']=dep(o['depth']); o['hk']=(o['area'],o['house']); o['rk']=(o['area'],o['house'],o['room']) if o['room'] not in('--','-','') else None
    U.append(o)
pre=collections.Counter(o['pre'] for o in U)
print('jar-final seals with house+depth:',len(U),'| distinct pre-jar signs:',len(pre),'| top:',pre.most_common(12))
def count(hk,rk,show=False):
    c=collections.Counter(); idx=collections.defaultdict(list)
    for i,h in enumerate(hk): idx[h].append(i)
    for mem in idx.values():
        for a in range(len(mem)):
            for b in range(a+1,len(mem)):
                i,j=mem[a],mem[b]
                if abs(U[i]['d']-U[j]['d'])>5: continue
                same=U[i]['pre']==U[j]['pre']
                kind='room' if rk[i] is not None and rk[i]==rk[j] else 'house_other_room'
                c[kind,'pairs']+=1; c[kind,'same']+=same
                if show and same: print('   ',kind,U[i]['cisi'],'-'.join(U[i]['toks'][::-1]),'|',U[j]['cisi'],'-'.join(U[j]['toks'][::-1]),'| pre-jar',U[i]['pre'],'(on',pre[U[i]['pre']],'jar-final seals)')
    return c
hk=[o['hk'] for o in U]; rk=[o['rk'] for o in U]
obs=count(hk,rk,True)
strata=collections.defaultdict(list)
for i,o in enumerate(U): strata[(o['area'],int(o['d']//3))].append(i)
null=collections.defaultdict(list)
for t in range(3000):
    ph=hk[:];pr=rk[:]
    for idx in strata.values():
        sh=idx[:]; random.shuffle(sh)
        for i,j in zip(idx,sh): ph[i]=hk[j]; pr[i]=rk[j]
    c=count(ph,pr)
    for k in ('room','house_other_room'): null[k].append(c[k,'same'])
for k in ('room','house_other_room'):
    a=np.array(null[k]); print(k,'pairs',obs[k,'pairs'],'same pre-jar sign: observed',obs[k,'same'],'chance %.2f'%a.mean(),'P %.4f'%((1+np.sum(a>=obs[k,'same']))/3001))
