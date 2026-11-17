#!/usr/bin/env python3
"""Name-slot analysis, questions 3-5. Reads work_data/name_rows.csv. Prints tables."""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, collections, random, re, math
from scipy import stats
random.seed(11); np.random.seed(11)
ROOT='/home/claude/ivc'
o=pd.read_csv(f'{ROOT}/work_data/name_rows.csv',dtype=str).fillna('')
sh=pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv',dtype=str).set_index('lipi_wells_number').shape_description.to_dict()
def W(s,n=30): return f'{s} [{sh.get(s,"?")[:n]}]'
for c in ['tight','has_class']: o[c]=o[c]=='True'
o['seglen']=o.seglen.astype(int)
T=o[o.tight&o.has_class&(o.seglen>=1)].copy(); T['segl']=T.seg.str.split('-')
# ---------------- Q3 families
print('== Q3 families of names differing in one slot (same length, 2+ signs)')
fam=collections.defaultdict(lambda: collections.defaultdict(set))   # (len,pos,pattern) -> filler -> objs
for r in T.itertuples():
    l=r.segl
    if len(l)<2: continue
    for k in range(len(l)):
        pat=tuple(l[:k])+('*',)+tuple(l[k+1:])
        fam[pat][l[k]].add(r.obj)
rows=[]
for pat,f in fam.items():
    if len(f)>=2: rows.append((len(f),sum(len(v) for v in f.values()),pat,f))
rows.sort(key=lambda x:(-x[0],-x[1]))
print('families with 2+ fillers:',len(rows),'; with 3+:',sum(1 for r in rows if r[0]>=3),'; 4+:',sum(1 for r in rows if r[0]>=4))
for nf,ns,pat,f in rows[:30]:
    fill=sorted(f,key=lambda x:-len(f[x]))
    print(f'  {"-".join(pat):16s} {nf} fillers {ns} seals | frame: '+' + '.join(W(p,22) if p!='*' else '_' for p in pat)+' | fillers: '+', '.join(f'{x}({len(f[x])})' for x in fill))
# which slot varies
vs=collections.Counter(); 
for nf,ns,pat,f in rows:
    L=len(pat); k=pat.index('*'); vs[(L,'first' if k==0 else 'last' if k==L-1 else 'mid')]+=1
print('families by (length, varying slot):',dict(vs))
# fixed-first vs fixed-last strength: number of distinct seg partners
fp=collections.defaultdict(set); lp=collections.defaultdict(set)
for l in set(map(tuple,T.segl)):
    if len(l)>=2:
        fp[l[0]].add(l[1:]); lp[l[-1]].add(l[:-1])
print('first signs with 4+ distinct continuations:',sum(1 for v in fp.values() if len(v)>=4),'; last signs with 4+ distinct lead-ins:',sum(1 for v in lp.values() if len(v)>=4))
print('top first signs by distinct continuations:',[(a,len(b)) for a,b in sorted(fp.items(),key=lambda x:-len(x[1]))[:10]])
print('top last signs by distinct lead-ins:',[(a,len(b)) for a,b in sorted(lp.items(),key=lambda x:-len(x[1]))[:10]])
# ---------------- Q4
T['animal']=T.symbol.map(lambda s:(s.split(':')[0] if s.strip() not in('','-') else 'none'))
T['animal']=T.animal.replace({'Bull1':'Bull','Bult':'Bull','Bull2':'Bull','Mult':'Mult'})
topan=T.animal.value_counts(); T['animal']=T.animal.where(T.animal.map(topan)>=20,'other')
def optype(x):
    if x in('861','817'): return 'diamond+2strokes'
    if x=='820': return 'wheel'
    if x.endswith('060'): return '060-cap'
    return 'none'
T['optype']=T.opener.map(optype)
T['clsg']=T.cls_last.where(T.cls_last.map(T.cls_last.value_counts())>=20,'other-class')
print('\nn',len(T)); print(T.animal.value_counts().to_dict()); print(T.optype.value_counts().to_dict()); print(T.clsg.value_counts().to_dict())
def assoc(unitcol,catcol,K=25,trials=2000,label=''):
    d=T[[unitcol,catcol]].copy()
    top=d[unitcol].value_counts().head(K).index
    d['u']=d[unitcol].where(d[unitcol].isin(top),'other')
    uc=pd.factorize(d.u)[0]; cc=pd.factorize(d[catcol])[0]; nu,nc=uc.max()+1,cc.max()+1
    def chi(cc):
        tab=np.zeros((nu,nc)); np.add.at(tab,(uc,cc),1)
        e=np.outer(tab.sum(1),tab.sum(0))/tab.sum(); m=e>0
        return ((tab-e)[m]**2/e[m]).sum()
    obs=chi(cc); v=math.sqrt(obs/(len(d)*(min(nu,nc)-1)))
    null=[chi(np.random.permutation(cc)) for _ in range(trials)]
    p=(1+sum(x>=obs for x in null))/(trials+1)
    print(f'  {label:30s} n {len(d):4d} chi2 {obs:7.1f} (shuffle mean {np.mean(null):6.1f}) CramerV {v:.3f} P {p:.4f}')
print('\n== Q4 associations (top-25 signs, others pooled; label shuffle)')
T['first1']=T.segl.map(lambda l:l[0]); T['last1']=T.segl.map(lambda l:l[-1]); T['segstr']=T.seg
for unit in ['first1','last1']:
    for cat in ['animal','clsg','optype']:
        assoc(unit,cat,25,2000,f'{unit} vs {cat}')
# sign-in-name presence vs category enrichment
def enrich(cat,k=8):
    out=[]
    N=len(T)
    for s in set(x for l in T.segl for x in l):
        has=T.segl.map(lambda l:s in l)
        if has.sum()<12: continue
        for c in T[cat].unique():
            a=int((has&(T[cat]==c)).sum()); b=int(has.sum()); cc=int((T[cat]==c).sum())
            if a<4: continue
            ex=b*cc/N; p=stats.hypergeom.sf(a-1,N,cc,b)
            out.append((p,s,c,a,b,ex))
    out.sort()
    for p,s,c,a,b,ex in out[:k]: print(f'    {W(s)} in {cat}={c}: {a} of {b} seals vs {ex:.1f} expected (P {p:.1e})')
for cat in ['animal','clsg','optype']:
    print(f'  -- top enrichments name sign x {cat}'); enrich(cat)
# ---- abroad
AB=['Persian Gulf','Mesopotamia','Iranian Plateau','Central Asia']
oo=o.copy(); oo['abroad']=oo.region.isin(AB)
oo['seglist']=oo.seg.str.split('-')
A=oo[oo.abroad]; H=oo[~oo.abroad&oo.has_class&(oo.seglen>=1)]
print(f'\n== Q4 abroad: seal faces parsed {len(A)}, with class and a name segment {(A.has_class&(A.seglen>=1)).sum()}; tight {(A.tight).sum()}')
Ab=A[A.has_class&(A.seglen>=1)]
print('abroad name segments:'); 
for r in Ab.itertuples(): print(f'   {r.cisi:12s} {r.site:22s} {r.region:16s} text {r.reading:28s} segment {r.seg:12s} class {r.cls_last} tight {r.tight}')
# all signs on abroad seals (any role) vs home: using raw metadata
d=pd.read_csv(f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv',dtype=str).fillna('')
ds=d[d.type.str.startswith('SEAL')]
ab=ds[ds.region.isin(AB)]; hm=ds[~ds.region.isin(AB)]
def sgn(df): return [set(re.findall(r'\d{3}',t))-{'000'} for t in df.text]
sa,shm=sgn(ab),sgn(hm)
ca=collections.Counter(x for s in sa for x in s); ch=collections.Counter(x for s in shm for x in s)
print(f'all seal faces: abroad {len(sa)} home {len(shm)}')
res=[]
for s in set(ca)|set(ch):
    a,b=ca[s],ch[s]
    if a<3: continue
    odds,p=stats.fisher_exact([[a,len(sa)-a],[b,len(shm)-b]]); res.append((p,s,a,b,a/len(sa),b/len(shm)))
res.sort()
print('signs most over-used on seals abroad (any slot), seals containing the sign:')
for p,s,a,b,fa,fh in res[:14]: print(f'   {W(s,34):48s} abroad {a}/{len(sa)} ({fa:.0%}) home {b}/{len(shm)} ({fh:.1%})  Fisher P {p:.1e}')
print('signs on abroad seals but never at home:',[s for s in ca if ch[s]==0])
# class of abroad seals
print('abroad class distribution:',Ab.cls_last.value_counts().to_dict(),' home:',H.cls_last.value_counts().head(6).to_dict())
# name signs only: abroad vs home
na=collections.Counter(x for l in Ab.seglist for x in l); nh=collections.Counter(x for l in H.seglist for x in l)
print('abroad name-segment signs:',dict(na.most_common(40)))
print('share of abroad name-segment signs that are also common home name signs (home count>=10):',sum(v for s,v in na.items() if nh[s]>=10),'of',sum(na.values()))
print('abroad name signs absent from home name slot:',[s for s in na if nh[s]==0])
# ---------------- Q5
print('\n== Q5 concentration')
def cover(counter,label):
    tot=sum(counter.values()); cs=np.cumsum(sorted(counter.values(),reverse=True))/tot
    n50,n80,n95=[int(np.searchsorted(cs,q)+1) for q in (.5,.8,.95)]
    single=sum(1 for v in counter.values() if v==1)
    print(f'  {label:44s} tokens {tot:5d} types {len(counter):4d} | cover 50%: {n50:3d}  80%: {n80:3d}  95%: {n95:3d} | seen once {single} ({single/len(counter):.0%} of types, unseen-mass {single/tot:.2f})')
    return n50,n80,n95
nameT=collections.Counter(x for l in T.segl for x in l)
whoT=collections.Counter(x for r in T.itertuples() for x,ro in zip(r.segl,r.segroles.split()) if ro=='who')
firstT=collections.Counter(l[0] for l in T.segl); lastT=collections.Counter(l[-1] for l in T.segl)
clsT=collections.Counter(c for c in T.cls_last if c)
# whole class slot over every clean seal with a class
allcls=collections.Counter(c for c in o[o.has_class].cls_last if c)
ded=T.drop_duplicates('reading')
nameD=collections.Counter(x for l in ded.segl for x in l); clsD=collections.Counter(c for c in ded.cls_last if c)
cover(nameT,'name slot, all signs (tight seals)'); cover(whoT,'  who-role signs only'); cover(firstT,'  first sign of name'); cover(lastT,'  last sign of name')
cover(clsT,'class slot (same seals)'); cover(allcls,'class slot (all clean seals w/ class)')
cover(nameD,'name slot, distinct texts only'); cover(clsD,'class slot, distinct texts only')
# size-matched
def sub(counter,n,reps=300):
    toks=[k for k,v in counter.items() for _ in range(v)]; r=[]
    for _ in range(reps):
        c=collections.Counter(random.sample(toks,n)); cs=np.cumsum(sorted(c.values(),reverse=True))/n
        r.append([len(c)]+[int(np.searchsorted(cs,q)+1) for q in (.5,.8,.95)])
    return np.mean(r,axis=0)
n=sum(clsT.values())
print(f'  size-matched to class tokens (n={n}): name types/50/80/95 =',np.round(sub(nameT,n),1),'; class =',np.round(sub(clsT,n),1))
# rarefaction + chao1
toks=[x for l in T.segl for x in l]
print('  rarefaction name types at n tokens:',{m:round(np.mean([len(set(random.sample(toks,m))) for _ in range(100)]),1) for m in (100,200,400,800,1200,len(toks))})
f1=sum(1 for v in nameT.values() if v==1); f2=sum(1 for v in nameT.values() if v==2)
print(f'  Chao1 estimate of total name-sign types: {len(nameT)+f1*f1/(2*f2):.0f} (observed {len(nameT)}, f1 {f1}, f2 {f2})')
# whole text signs in corpus for context
allsign=collections.Counter(x for r in o.itertuples() for x in r.reading.split('-'))
cover(allsign,'every sign in clean seal texts (context)')
# per-position sign inventories
print('  name signs by how often used in a position other than the name slot (share of all uses that are name-slot):')
tot_use=allsign
hi=[(nameT[s]/tot_use[s],s,nameT[s],tot_use[s]) for s in nameT if tot_use[s]>=25]
print('   mostly-name signs:',[f'{s}:{a}/{b}' for f,s,a,b in sorted(hi,reverse=True)[:12]])
print('   rarely name signs:',[f'{s}:{a}/{b}' for f,s,a,b in sorted(hi)[:8]])
T.drop(columns=['segl']).to_pickle('/tmp/T2.pkl')
