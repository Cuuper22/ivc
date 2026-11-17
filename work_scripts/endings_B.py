#!/usr/bin/env python3
"""B. Head of house: `[name] jar man` seals at Mohenjo-daro with a known house. Does the head's name match the house crest /
names on the other seals of the same house, against chance (house labels shuffled among seals of the same area and 3-ft depth band)?
One head per house? Heads in bigger houses?  Output tables work_data/endings/B_*.csv"""
import pandas as pd, numpy as np, collections, re
R='/home/claude/ivc'
f=pd.read_csv(f'{R}/work_data/endings/faces.csv',dtype=str,keep_default_na=False)
f=f[(f.isseal=='True')&(f.site=='Mohenjo-daro')].copy()
f['face']=pd.to_numeric(f.face,errors='coerce')
f['house']=np.where((f['block-house']!='--')&(f['area-section']!='--'),f['area-section']+'|'+f['block-house'],'')
f['area']=f['area-section']
f['dep']=f.depth.map(lambda s:(lambda m: abs(float(m.group(0))) if m else np.nan)(re.search(r'-?\d+\.?\d*',s)))
f['dband']=(f.dep//3).fillna(-1).astype(int)
f['head']=(f.end=='jar')&(f.endsub=='090')
f['clean']=(f.name!='')&~f.name.str.contains('000|ALT')
f['first']=f.name.str.split('-').str[0]; f['last']=f.name.str.split('-').str[-1]
f['nsig']=f.name.map(lambda s:len(s.split('-')) if s else 0)
H=f[f.house!=''].copy(); print('MD seals with house',len(H),'houses',H.house.nunique(),'head seals with house',H['head'].sum(),'clean-name heads',(H['head']&H.clean).sum())
# comparison groups: heads, owners (jar, nothing after), other seals
H['kind']=np.where(H['head'],'head',np.where((H.end=='jar')&(H.endsub==''),'owner-jar',np.where(H.end=='none','other','spear/porter/comb/jar+other')))
print(H.kind.value_counts())
rng=np.random.default_rng(0)
C=H[H.clean].reset_index(drop=True)
def match_stats(houses,mask):
    """for each seal in mask: does another seal (any kind) of the same house, clean name, share (crest=first sign / full name / any sign)?"""
    byh=collections.defaultdict(list)
    for i,h in enumerate(houses): byh[h].append(i)
    cr=nm=anys=n=0
    for i in np.where(mask)[0]:
        mates=[j for j in byh[houses[i]] if j!=i]
        if not mates: continue
        n+=1; s=C.name[i].split('-')
        cr+= any(C['first'][j]==C['first'][i] for j in mates)
        nm+= any(C.name[j]==C.name[i] for j in mates)
        anys+= any(set(C.name[j].split('-'))&set(s) for j in mates)
    return n,cr,nm,anys
# multi-sign names for crest test (crest defined only on names of 2+ signs, mates also 2+)
def match_crest(houses,mask,multi=True):
    byh=collections.defaultdict(list)
    for i,h in enumerate(houses): byh[h].append(i)
    n=k=0
    for i in np.where(mask)[0]:
        if C.nsig[i]<2: continue
        mates=[j for j in byh[houses[i]] if j!=i and C.nsig[j]>=2]
        if not mates: continue
        n+=1; k+=any(C['first'][j]==C['first'][i] for j in mates)
    return n,k
houses=C.house.values; key=(C.area+'|'+C.dband.astype(str)).values
idx=collections.defaultdict(list)
for i,k in enumerate(key): idx[k].append(i)
def shuffled():
    h=houses.copy()
    for k,ii in idx.items(): h[ii]=rng.permutation(houses[ii])
    return h
res=[]
for kind in ['head','owner-jar']:
    mask=(C.kind if 'kind' in C else None)
C['kind']=H[H.clean].reset_index(drop=True).kind
for kind in ['head','owner-jar']:
    mask=(C.kind==kind).values
    obs=match_stats(houses,mask); oc=match_crest(houses,mask)
    sims=[];simc=[]
    for _ in range(300):
        h=shuffled(); sims.append(match_stats(h,mask)[1:]); simc.append(match_crest(h,mask)[1])
    sims=np.array(sims)
    print(f'\n{kind}: seals with a house-mate {obs[0]}')
    for j,lab in enumerate(['first sign = first sign of a mate','whole name identical to a mate','any sign shared with a mate']):
        print(f'  {lab}: observed {obs[1+j]} ({obs[1+j]/obs[0]:.2f}), shuffled mean {sims[:,j].mean():.1f}, P(sim>=obs) {np.mean(sims[:,j]>=obs[1+j]):.3f}')
    print(f'  crest test, multi-sign names only: n {oc[0]} observed {oc[1]} shuffled mean {np.mean(simc):.1f} P {np.mean(np.array(simc)>=oc[1]):.3f}')
# list head seals with matches
rows=[]
byh=collections.defaultdict(list)
for i,h in enumerate(houses): byh[h].append(i)
for i in np.where((C.kind=='head').values)[0]:
    mates=[j for j in byh[houses[i]] if j!=i]
    nm=C.name[i]; s=set(nm.split('-'))
    m_cr=[C.cisi[j] for j in mates if C['first'][j]==C['first'][i]]
    m_nm=[C.cisi[j] for j in mates if C.name[j]==nm]
    m_any=[C.cisi[j] for j in mates if set(C.name[j].split('-'))&s]
    rows.append(dict(head=C.cisi[i],reading=C.reading_order_text[i],name=nm,house=houses[i],room=C['room-grid'][i],depth=C.depth[i],face=C.face[i],mates=len(mates),
        first_match=' '.join(m_cr),same_name=' '.join(m_nm),any_sign=' '.join(m_any),mate_names=' | '.join(f'{C.cisi[j]}:{C.name[j]}' for j in mates)))
B=pd.DataFrame(rows); B.to_csv(f'{R}/work_data/endings/B_heads.csv',index=False)
print('\nheads with clean name and a house-mate:',(B.mates>0).sum(),' with first-sign match',(B.first_match!='').sum(),' same name',(B.same_name!='').sum(),' any sign',(B.any_sign!='').sum())
print(B[(B.any_sign!='')][['head','name','house','first_match','same_name','any_sign']].to_string(index=False))
# area-level: head's first sign among other seals in the same area (not the house)
byarea=collections.defaultdict(list)
for i,a in enumerate(C.area.values): byarea[a].append(i)
def area_match(h_hom,mask):
    n=k=0
    for i in np.where(mask)[0]:
        mates=[j for j in byarea[C.area[i]] if j!=i and C.house[j]!=C.house[i]]
        if not mates: continue
        n+=1; k+=any(C['first'][j]==C['first'][i] for j in mates)
    return n,k
for kind in ['head','owner-jar']:
    mask=(C.kind==kind).values; print(kind,'first sign found on a seal of another house in the same area (n,k)',area_match(None,mask))
# one head per house
Hh=H[H['head']]; c=Hh[Hh.house!=''].groupby('house').size()
allh=H.groupby('house').size()
print('\nhouses with a head seal',len(c),'with 2+',(c>=2).sum(),' distribution',c.value_counts().to_dict())
hs=H.groupby('house').agg(n=('id','size'),heads=('head','sum'))
hs['area']=[h.split('|')[0] for h in hs.index]
print('house size: houses with head',hs[hs.heads>0].n.mean().round(2),hs[hs.heads>0].n.median(),' without',hs[hs.heads==0].n.mean().round(2),hs[hs.heads==0].n.median())
# chance: heads placed on random seals within the same area
rng2=np.random.default_rng(1); obsmean=hs[hs.heads>0].n.mean()
Hl=H.reset_index(drop=True); sz=Hl.house.map(allh).values; sims=[]
arr=Hl.area.values; headmask=Hl['head'].values
aidx=collections.defaultdict(list)
for i,a in enumerate(arr): aidx[a].append(i)
for _ in range(2000):
    m=np.zeros(len(Hl),bool)
    for a,ii in aidx.items():
        k=headmask[ii].sum()
        if k: m[rng2.choice(ii,k,replace=False)]=True
    sims.append(sz[m].mean())
print('mean house size seen by a head seal',round(sz[headmask].mean(),2),'vs random seal of the same area',round(np.mean(sims),2),'P(sim>=obs)',np.mean(np.array(sims)>=sz[headmask].mean()))
sz_o=sz[(Hl.kind=='owner-jar').values]; print('mean house size of owner-jar seals',sz_o.mean().round(2))
# share of heads among seals by house size class
hs['sizeclass']=pd.cut(hs.n,[0,1,2,4,8,100],labels=['1','2','3-4','5-8','9+'])
print(hs.groupby('sizeclass',observed=True).agg(houses=('n','size'),seals=('n','sum'),heads=('heads','sum')).assign(heads_per_100_seals=lambda t:(100*t.heads/t.seals).round(1)))
hs.to_csv(f'{R}/work_data/endings/B_house_sizes.csv')
# ten largest head seals
big=f[f['head']&f.face.notna()].sort_values('face',ascending=False).head(10)
print(big[['cisi','reading_order_text','face','hmm','vmm','symbol','material','house','area-section','room-grid']].to_string(index=False))
big.to_csv(f'{R}/work_data/endings/B_top10_heads.csv',index=False)
