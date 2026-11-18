#!/usr/bin/env python3
"""Name-slot account: (a) rate test of first vs last sign agreement among same-house seals, (b) fish-first test,
(c) round seals abroad, (d) builds the 25-seal table. Needs work_data/name_rows.csv."""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, collections, itertools, random, re
random.seed(5)
ROOT='/home/antigravity/Cuuper22/ivc'
o=pd.read_csv(f'{ROOT}/work_data/name_rows.csv',dtype=str).fillna('')
sh=pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv',dtype=str).set_index('lipi_wells_number').shape_description.to_dict()
for c in ['tight','has_class']: o[c]=o[c]=='True'
o['seglen']=o.seglen.astype(int)
T=o[o.tight&o.has_class&(o.seglen>=1)].copy(); T['segl']=T.seg.str.split('-')
M=T[(T.site=='Mohenjo-daro')&~T.bh.isin(['--','-',''])].drop_duplicates('obj').copy(); M['hk']=M.area+' '+M.bh
def depth(s):
    m=re.search(r'(-?\d+(\.\d+)?)\s*ft',s); return float(m.group(1)) if m else None
M['band']=[(a,int(depth(d)//3) if depth(d) is not None else -9) for a,d in zip(M.area,M.depth)]
Mm=M[M.seglen>=2].reset_index(drop=True)
hk=list(Mm.hk); L=list(Mm.segl)
strata=collections.defaultdict(list)
for i,b in enumerate(Mm.band): strata[b].append(i)
def stat(keys):
    idx=collections.defaultdict(list)
    for i,h in enumerate(keys): idx[h].append(i)
    n=ff=ll=fish_same=fish_pairs=0; FISH={'235','240','233','231'}
    for m in idx.values():
        for a,b in itertools.combinations(m,2):
            n+=1; ff+=L[a][0]==L[b][0]; ll+=L[a][-1]==L[b][-1]
            if L[a][0] in FISH and L[b][0] in FISH: fish_pairs+=1; fish_same+=L[a][0]==L[b][0]
    return n,ff,ll,fish_pairs,fish_same
obs=stat(hk); null=[]
for t in range(3000):
    p=hk[:]
    for idx in strata.values():
        x=idx[:]; random.shuffle(x)
        for i,j in zip(idx,x): p[i]=hk[j]
    null.append(stat(p))
nl=np.array(null)
print('multi-sign names at Mohenjo-daro with a house:',len(Mm),'houses',Mm.hk.nunique())
print('same-house pairs',obs[0])
for k,lab in [(1,'same FIRST sign'),(2,'same LAST sign'),(4,'same fish sign, given both fish-first')]:
    print(f'  {lab}: observed {obs[k]} | chance mean {nl[:,k].mean():.2f} | ratio {obs[k]/max(nl[:,k].mean(),1e-9):.2f} | P {(1+(nl[:,k]>=obs[k]).sum())/3001:.4f}')
print('  pairs where both names start with a fish sign:',obs[3],'| chance',nl[:,3].mean().round(2))
# fish sign share of multi-sign name starts
F=T[T.seglen>=2]; fs=F.segl.map(lambda l:l[0] in {'235','240','233','231'})
print('multi-sign names starting with one of 4 fish signs (231/233/235/240):',int(fs.sum()),'of',len(F),f'({fs.mean():.0%})')
print('same, Mohenjo houses only:',int(Mm.segl.map(lambda l:l[0] in {"235","240","233","231"}).sum()),'of',len(Mm))
# ender particles
for s in ['760','100']:
    h=T[T.segl.map(lambda l:s in l)]
    print(s,'seals',len(h),'last-in-name',int(h.segl.map(lambda l:l[-1]==s).sum()),'alone',int((h.seglen==1).sum()),'class mix',h.cls_last.value_counts().head(4).to_dict(),'sites',h.site.nunique())
    print('   preceding sign:',collections.Counter(l[-2] for l in h.segl if len(l)>=2 and l[-1]==s).most_common(8))
# round seals abroad
d=pd.read_csv(f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv',dtype=str).fillna('')
AB=['Persian Gulf','Mesopotamia','Iranian Plateau','Central Asia']
ab=d[d.region.isin(AB)].copy(); ab['rd']=[t.strip('+[]').split('-')[::-1] for t in ab.text]
rd=ab[ab.type.isin(['SEAL:C','SEAL:CY'])]
print('\nabroad objects',len(ab),'; round/cylinder seals',len(rd),'; square seals',int(ab.type.eq('SEAL:S').sum()))
for s in ['090','091']:
    pos=[(i,len(x)) for x in ab.rd for i,t in enumerate(x) if t==s]
    print(s,'on abroad objects',len(pos),'; first sign of text',sum(1 for i,n in pos if i==0),'; second',sum(1 for i,n in pos if i==1),'; last',sum(1 for i,n in pos if i==n-1))
home=d[~d.region.isin(AB)&d.type.str.startswith('SEAL')]
hr=[t.strip('+[]').split('-')[::-1] for t in home.text]
for s in ['090','091']:
    pos=[(i,len(x)) for x in hr for i,t in enumerate(x) if t==s]
    print(s,'at home seals',len(pos),'; first',sum(1 for i,n in pos if i==0),'; last',sum(1 for i,n in pos if i==n-1))
print('round seals with 090/091 anywhere:',sum(1 for x in rd.rd if '090' in x or '091' in x),'of',len(rd))
print('round-seal texts containing a man sign: first-sign count',sum(1 for x in rd.rd if x and x[0] in('090','091')))

# ---- rate P for same-fish given both fish-first; positional lock of signs
rate_obs=obs[4]/obs[3]; rn=[(x[4]/x[3]) for x in null if x[3]>0]
print('\nsame-fish rate among fish-first same-house pairs: %d/%d = %.0f%% vs chance mean %.0f%% ; P %.4f'%(obs[4],obs[3],100*rate_obs,100*np.mean(rn),(1+sum(r>=rate_obs for r in rn))/(len(rn)+1)))
first=collections.Counter(); last=collections.Counter(); mid=collections.Counter()
for l in T.segl:
    if len(l)>=2:
        first[l[0]]+=1; last[l[-1]]+=1
        for s in l[1:-1]: mid[s]+=1
sg=[s for s in set(first)|set(last)|set(mid) if first[s]+last[s]+mid[s]>=8]
lock=[s for s in sg if max(first[s],last[s])/(first[s]+last[s]+mid[s])>=0.75]
both=[s for s in sg if first[s]/(first[s]+last[s]+mid[s])>=0.2 and last[s]/(first[s]+last[s]+mid[s])>=0.2]
print('signs seen 8+ times inside 2+ sign names:',len(sg),'| locked to first or last (>=75%):',len(lock),'| used both first and last (each >=20%):',len(both),both)
print('first-locked:',[s for s in lock if first[s]>last[s]]); print('last-locked:',[s for s in lock if last[s]>=first[s]])
# ---- 25-seal table
PICK=[('DKE Trench E-',['M-1738','M-47','M-323','M-865']),('DKG. (S) 1I',['M-1988','M-228','M-651','M-1680']),('DKG. (S) 4-',['M-1977','M-708','M-319']),
('DKG First Street-',['-','M-199','M-850','M-238','M-986']),('DKG. (N) 18-',['M-1849','M-217']),('DKG. (S) 7II',['M-1726','M-1746']),('DKG. (S) 6I',['M-1760','M-326']),('DKE Trench EI',['M-1814']),('DKG. (S) 8A-',['M-1753','M-208'])]
OVERRIDE={'M-1680':'717','M-850':'-'}
FIRSTPOOL={'235','240','233','231','798','806','140','013','590','017'}
SIGNW={'861':'diamond+small diamond','817':'diamond+small diamond','820':'six-spoke wheel','002':'two short strokes','740':'jar','520':'spear','390':'tree','400':'comb','090':'plain person','151':'carrier','156':'carrier','154':'carrier','001':'one stroke','031':'one long stroke','032':'two long strokes','033':'three long strokes','700':'cup'}
def w(s): return (SIGNW.get(s) or sh.get(s,'?')[:42]).replace('|',' ')
out=[]; n=0
alln=pd.read_csv(f'{ROOT}/work_data/name_rows.csv',dtype=str).fillna('')
for hk_,ids in PICK:
    for c in ids:
        sub=alln[(alln.cisi==c)&((alln.area+' '+alln.bh)==hk_)&(alln.site=='Mohenjo-daro')]
        if c=='-': sub=alln[(alln.cisi=='-')&((alln.area+' '+alln.bh)==hk_)&(alln.reading.str.contains('240-637'))]
        if len(sub)==0: print('MISSING',hk_,c); continue
        r=sub.iloc[0]; n+=1
        toks=r.reading.split('-'); roles=r.roles.split()
        out.append((n,c if c!='-' else '(no CISI no.)',hk_,r.depth,r.symbol,toks,roles,r.seg))
lines=[]
for n_,c,h,dp,sym,toks,roles,seg in out:
    segl=seg.split('-'); hh=OVERRIDE.get(c,segl[0])
    ko=[k for k,x in enumerate(roles) if x in('opener','opener-strokes','cap','cap-selector')]
    kc=[k for k,x in enumerate(roles) if x in('class','class-tail')]
    a=(ko[-1]+1) if ko else 0; b=kc[0] if kc else len(toks)
    pre=' + '.join(f'{toks[k]} {w(toks[k])}' for k in ko)
    nm=[]; nmk=[k for k in range(a,b) if roles[k] in('who','house','house-marker')]; first_name,last_name=nmk[0],nmk[-1]
    if c not in OVERRIDE and segl[0] not in FIRSTPOOL: hh='-'
    for k in range(a,b):
        t=toks[k]
        if roles[k] in('count','amount','counted-thing','title-phrase') and not (roles[k]=='counted-thing' and first_name<k<last_name): nm.append(f'{t} {w(t)} [not name: {roles[k]}]'); continue
        if roles[k]=='counted-thing' and first_name<k<last_name: nm.append(f'{t} {w(t)} [PERSONAL (parser: counted-thing)]'); continue
        tag='HOUSEHOLD' if t==hh else 'ENDER' if (t in('760','100','923') and k==b-1 and len(segl)>1) else 'PERSONAL'
        nm.append(f'{t} {w(t)} [{tag}]')
    cl=[f'{t} {w(t)}' for t,ro in zip(toks,roles) if ro in('class',)]
    tail=[f'{t} {w(t)}' for t,ro in zip(toks,roles) if ro=='class-tail']
    lines.append(f'| {n_} | {c} | {h} ({dp.strip()}) | {sym or "none"} | {pre or "none"} | '+' ; '.join(nm)+' | '+(cl[-1] if cl else '?')+f' | {"-".join(toks)} |')
open('/home/antigravity/Cuuper22/ivc/jobs/out/name_slot_tabs/seals25.md','w').write('\n'.join(lines))
for x in out: print(x[0],x[1],x[2],x[3],x[4],'|','-'.join(x[5]),'|',' '.join(x[6]))
