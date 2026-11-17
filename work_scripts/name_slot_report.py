#!/usr/bin/env python3
"""Assemble jobs/out/name_slot.md from name_rows.csv and the 25-seal table. Run after name_slot_build.py and name_slot_account.py."""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, collections
ROOT='/home/claude/ivc'
o=pd.read_csv(f'{ROOT}/work_data/name_rows.csv',dtype=str).fillna('')
sh=pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv',dtype=str).set_index('lipi_wells_number').shape_description.to_dict()
for c in ['tight','has_class']: o[c]=o[c]=='True'
o['seglen']=o.seglen.astype(int)
T=o[o.tight&o.has_class&(o.seglen>=1)].copy(); T['segl']=T.seg.str.split('-')
def W(s,n=34): return sh.get(s,'?')[:n].replace('|','/')
# starters / enders / alone
first=collections.Counter(); last=collections.Counter(); alone=collections.Counter(); mid=collections.Counter()
for l in T.segl:
    if len(l)==1: alone[l[0]]+=1
    else:
        first[l[0]]+=1; last[l[-1]]+=1
        for s in l[1:-1]: mid[s]+=1
def rank(c,k,extra=None):
    r=['| sign | shape | seals |','|---|---|---|']
    for s,n in c.most_common(k): r.append(f'| {s} | {W(s)} | {n} |')
    return '\n'.join(r)
# enders by lock
multi=sg=[s for s in set(first)|set(last)|set(mid) if first[s]+last[s]+mid[s]>=8]
lk=['| sign | shape | in 2+ sign names | first | middle | last |','|---|---|---|---|---|---|']
for s in sorted(sg,key=lambda s:-(last[s]/(first[s]+last[s]+mid[s]))):
    n=first[s]+last[s]+mid[s]
    if last[s]/n>=0.75 or first[s]/n>=0.75: lk.append(f'| {s} | {W(s)} | {n} | {first[s]} | {mid[s]} | {last[s]} |')
# 3+ seals
big=[]
for s,d in T.drop(columns=['segl']).groupby('seg'):
    n=d.obj.nunique()
    if n>=3:
        hs=sorted(set((r.area+' '+r.bh).strip() for r in d.itertuples() if r.bh not in('--','-','')))
        st=d.groupby('site').obj.nunique().sort_values(ascending=False)
        big.append((n,s,st,hs))
big.sort(key=lambda x:(-x[0],x[1]))
bt=['| seals | name segment | shapes | sites (seals) | houses with a seal of it |','|---|---|---|---|---|']
for n,s,st,hs in big:
    bt.append(f'| {n} | {s} | '+' + '.join(W(x,20) for x in s.split('-'))+' | '+', '.join(f'{k} {v}' for k,v in st.items())+f' | {len(hs)} |')
# families
fam=collections.defaultdict(lambda: collections.defaultdict(set))
for r in T.itertuples():
    l=r.segl
    if len(l)<2: continue
    for k in range(len(l)):
        fam[tuple(l[:k])+('*',)+tuple(l[k+1:])][l[k]].add(r.obj)
rows=[(len(f),sum(len(v) for v in f.values()),pat,f) for pat,f in fam.items() if len(f)>=2]
rows.sort(key=lambda x:(-x[0],-x[1]))
ft=['| # | frame | frame in words | fillers (seals) | n fillers | n seals |','|---|---|---|---|---|---|']
for i,(nf,ns,pat,f) in enumerate(rows[:30],1):
    fill=sorted(f,key=lambda x:-len(f[x]))
    ft.append(f'| {i} | {"-".join(pat)} | '+' + '.join(W(p,24) if p!='*' else '_' for p in pat)+' | '+', '.join(f'{x}({len(f[x])})' for x in fill[:14])+(' ...' if len(fill)>14 else '')+f' | {nf} | {ns} |')
L=T.seglen.value_counts().sort_index(); N=len(T)
lens=' ; '.join(f'{k} sign: {v} ({v/N:.0%})' for k,v in L.items())
seals25=open(f'{ROOT}/jobs/out/name_slot_tabs/seals25.md').read()
md=open(f'{ROOT}/work_scripts/name_slot_template.md').read()
md=(md.replace('{{LENS}}',lens).replace('{{STARTERS}}',rank(first,14)).replace('{{ENDERS}}',rank(last,14)).replace('{{ALONE}}',rank(alone,14))
   .replace('{{LOCK}}','\n'.join(lk)).replace('{{BIG}}','\n'.join(bt)).replace('{{FAMS}}','\n'.join(ft)).replace('{{SEALS25}}',seals25).replace('{{NBIG}}',str(len(big))))
open(f'{ROOT}/jobs/out/name_slot.md','w').write(md); print('written',len(md))
