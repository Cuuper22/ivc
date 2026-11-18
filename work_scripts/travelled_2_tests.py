"""Job: the travelled name 590-390. Step 2: test four readings (personal name / title / trading house / commodity) with the data.
Reading order = stored order reversed (gloss2_all is already in reading order). Objects (not faces) are the unit; copies of one stone count once per object id.
Run: python3 travelled_2_tests.py"""
import pandas as pd, numpy as np, re, random, collections, math
from scipy import stats
R='/home/antigravity/Cuuper22/ivc/'
random.seed(7); np.random.seed(7)
G=pd.read_csv(R+'work_data/gloss2_all.csv',dtype=str)
M=pd.read_csv(R+'research/data/open_prototype/lipi/metadata_filtered.csv',dtype=str)
D=G.merge(M[['id','region','area-section','block-house','room-grid','period','phase','depth','symbol','horizontal(mm)','vertical(mm)']],on='id',how='left',suffixes=('','_m'))
D['toks']=D.reading_order_text.str.split('-')
def grp(t):
    if t.startswith('SEAL'): return 'seal'
    if t.startswith('TAB:C'): return 'copper'
    if t.startswith('TAB'): return 'tablet'
    if t.startswith('TAG'): return 'tag'
    if t.startswith('POT'): return 'pot'
    return 'other'
D['grp']=D.type.map(grp)
ABROAD={'Persian Gulf','Mesopotamia','Iranian Plateau','Central Asia'}
D['abroad']=D.region.isin(ABROAD)
def has(t,p):
    n=len(p); return any(t[i:i+n]==p for i in range(len(t)-n+1))
def pos(t,p):
    n=len(p)
    for i in range(len(t)-n+1):
        if t[i:i+n]==p: return i
O=D.drop_duplicates('object').copy()          # one row per object
N=len(O)
tgt=['590','390']
hit=O[O.toks.map(lambda t:has(t,tgt))]
# object-level: an object counts if any face has it
hobj=set(D[D.toks.map(lambda t:has(t,tgt))].object)
O['hit']=O.object.isin(hobj)
H=O[O.hit]
n=len(H)
print('corpus objects',N,'| 590-390 objects',n)

out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)

# ---------- A. where: site mix against corpus ----------
base=O.site.value_counts(normalize=True)
obs=H.site.value_counts()
P('\n== A. site mix (objects) ==')
P('site | 590-390 | share | corpus share | expected')
for s,c in obs.items(): P(s,c,f'{c/n:.3f}',f'{base[s]:.3f}',f'{base[s]*n:.1f}')
tv=0.5*sum(abs(obs.get(s,0)/n-base[s]) for s in base.index)
sims=[]
pool=O.site.values
for _ in range(20000):
    smp=np.random.choice(pool,n,replace=False)
    c=collections.Counter(smp)
    sims.append(0.5*sum(abs(c.get(s,0)/n-base[s]) for s in base.index))
sims=np.array(sims)
P(f'total variation distance of site mix from corpus: {tv:.3f}; random {n}-object draws give mean {sims.mean():.3f}, 95th pct {np.percentile(sims,95):.3f}; P(draw >= observed) = {(sims>=tv).mean():.3f}')
named=lambda df: df[df.site!='Unknown'].site.nunique()
ns=[len(set(np.random.choice(pool[pool!='Unknown'],n,replace=False))) for _ in range(5000)]
P(f'named sites carrying it: {named(H)}; random draws of {n} objects reach {np.mean(ns):.1f} on average, {np.percentile(ns,95):.0f} at the 95th percentile')

# ---------- B. abroad / ports / gateways ----------
P('\n== B. abroad, ports, gateways ==')
ab=H.abroad.sum(); pa=O.abroad.mean()
P(f'abroad objects: {ab} of {n} against corpus rate {O.abroad.sum()}/{N} = {pa:.4f}; binomial P(>= {ab}) = {stats.binom.sf(ab-1,n,pa):.3f}')
# among SQUARE seals found abroad (home-style stones): how often is it 590-390
sq=O[(O.abroad)&(O.type=='SEAL:S')]
P(f'square seals abroad: {len(sq)}; with 590-390: {sq.hit.sum()}  (Kish 1971.1, Gonur 4155.1)')
sealrate=O[O.type=='SEAL:S'].hit.mean()
P(f'590-390 rate on all square seals: {sealrate:.4f}; chance of >= {sq.hit.sum()} of {len(sq)} abroad = {stats.binom.sf(sq.hit.sum()-1,len(sq),sealrate):.4f}')
# add Altyn Depe 415-390 as variant
alt=O[(O.site=='Altyn Depe')]
P('Altyn Depe text:',alt.reading_order_text.tolist())
PORTS={'Lothal','Dholavira','Allahdino','Bala-kot','Gola Dhoro (Bagasra)','Kanmer','Shikarpur','Chanhu-daro','Nausharo'}
GATE={'Lothal','Dholavira','Allahdino','Bala-kot','Gola Dhoro (Bagasra)'}   # coast / Kutch gateway sites
for name,S in [('coast+Kutch gateways (Lothal, Dholavira, Allahdino, Balakot, Gola Dhoro)',GATE)]:
    k=H.site.isin(S).sum(); p=O.site.isin(S).mean()
    P(f'{name}: {k} of {n} = {k/n:.3f} against corpus {p:.3f}; binomial P(>= {k}) = {stats.binom.sf(k-1,n,p):.3f}')
core={'Mohenjo-daro','Harappa'}
k=H.site.isin(core).sum(); p=O.site.isin(core).mean()
P(f'Mohenjo-daro + Harappa: {k} of {n} = {k/n:.3f} against corpus {p:.3f}')

# ---------- C. what kind of object: tags, pots, counts ----------
P('\n== C. object type ==')
tb=O.grp.value_counts(normalize=True)
P('group | 590-390 | share | corpus share')
for g,c in H.grp.value_counts().items(): P(g,c,f'{c/n:.3f}',f'{tb[g]:.3f}')
k=(H.grp=='tag').sum(); p=tb['tag']
P(f'tags: {k} of {n}; binomial P(>= {k}) = {stats.binom.sf(k-1,n,p):.3f}')
lo=O[O.site=='Lothal']; lh=lo[lo.hit]
P(f'Lothal: {len(lh)} of {len(lo)} objects carry it, all tags: {(lh.grp=="tag").sum()}; Lothal tags are {(lo.grp=="tag").mean():.3f} of Lothal objects; P(all {len(lh)} are tags) = {((lo.grp=="tag").mean())**len(lh):.4f}')
# count sign directly before 590 (full-height strokes 031/032/033 = containers; short strokes 001-005)
COUNT={'001','002','003','004','005','031','032','033','034'}
def before_sign(t,p):
    i=pos(t,p); return t[i-1] if i and i>0 else None
rows=D[D.toks.map(lambda t:has(t,tgt))]
bs=[before_sign(t,tgt) for t in rows.toks]
P('sign right before 590-390 (faces):',collections.Counter(bs).most_common(14))
cnt=sum(b in COUNT for b in bs); cnt_tall=sum(b in {'031','032','033'} for b in bs)
P(f'faces with a count stroke right before it: {cnt} of {len(rows)} (tall strokes {cnt_tall}); tall strokes are {sum(b=="032" for b in bs)} two-strokes')
# same measure for 590 elsewhere and for ordinary names
oth=D[D.toks.map(lambda t:'590' in t and not has(t,tgt))]
bo=[ (t[t.index('590')-1] if t.index('590')>0 else None) for t in oth.toks]
P(f'590 not followed by 390: {len(oth)} faces; tall-stroke count right before it: {sum(b in {"031","032","033"} for b in bo)} ({sum(b in {"031","032","033"} for b in bo)/len(oth):.3f}) against {cnt_tall/len(rows):.3f} for 590-390')
# Lothal tags detail
P('Lothal tags with 590-390:',lh[['cisi','reading_order_text']].to_string(index=False))
# fraction of faces whose count is a tall-stroke 032 right before, by object group
g=rows.assign(b=bs)
P('tall-stroke count before 590-390 by group:',g.groupby('grp').apply(lambda x:(x.b.isin(['031','032','033']).sum(),len(x))).to_dict())

# ---------- D. house and era ----------
P('\n== D. one house, one era? ==')
MD=O[(O.site=='Mohenjo-daro')&(O['block-house'].notna())&(~O['block-house'].isin(['--','-','']))&(O.type.str.startswith('SEAL'))].copy()
MD['hk']=MD['area-section']+'|'+MD['block-house']
mh=MD[MD.hit]
P(f'Mohenjo-daro seals with a house recorded: {len(MD)}; with 590-390: {len(mh)} in {mh.hk.nunique()} distinct houses')
def pairs_same(df):
    c=collections.Counter(df.hk); return sum(v*(v-1)//2 for v in c.values())
obsp=pairs_same(mh)
sim=[pairs_same(MD.sample(len(mh))) for _ in range(5000)]
P(f'same-house pairs: {obsp} observed against {np.mean(sim):.2f} for random draws of the same size (P(draw >= obs) = {(np.array(sim)>=obsp).mean():.3f})')
P('houses:',mh.hk.tolist())
# area-level (district) mix
P('Mohenjo-daro 590-390 areas:',mh['area-section'].value_counts().to_dict(),'| all MD seals with house:',MD['area-section'].value_counts().head(6).to_dict())
# era
for site in ['Mohenjo-daro','Harappa']:
    s=O[O.site==site]
    colp='period' if site=='Mohenjo-daro' else 'phase'
    P(site,'period',colp,'590-390:',dict(collections.Counter(s[s.hit][colp])),'| corpus:',dict(collections.Counter(s[colp]).most_common(8)))
# Mohenjo-daro era Early/Intermediate/Late
mdp=O[(O.site=='Mohenjo-daro')&(O.period.isin(['Early','Intermediate','Late']))]
P('Mohenjo-daro dated (Early/Intermediate/Late) corpus:',mdp.period.value_counts().to_dict(),'| 590-390:',mdp[mdp.hit].period.value_counts().to_dict())
# depth in ft at Mohenjo-daro/Harappa
def dep(s):
    m=re.search(r'(-?\d+(\.\d+)?)\s*ft',str(s)); return float(m.group(1)) if m else None
for site in ['Mohenjo-daro','Harappa']:
    s=O[(O.site==site)]; d_all=[abs(dep(x)) for x in s.depth if dep(x) is not None]; d_h=[abs(dep(x)) for x in s[s.hit].depth if dep(x) is not None]
    P(site,'depth ft (abs) 590-390: n',len(d_h),'range',min(d_h),max(d_h),'median',np.median(d_h),'| corpus n',len(d_all),'median',np.median(d_all),'range of middle 90%',np.percentile(d_all,5),np.percentile(d_all,95))
# preceding-sign diversity vs. other recurring 2-grams
P('\n== E. how varied is the company it keeps, against other recurring pairs? ==')
def ngram_rows(p):
    return D[D.toks.map(lambda t:has(t,p))]
# all adjacent sign pairs with >= 15 objects, no lost signs, no jar, no pure count strokes
pairs=collections.defaultdict(set)
for obj,t in zip(D.object,D.toks):
    for i in range(len(t)-1):
        a,b=t[i],t[i+1]
        if re.fullmatch(r'\d{3}',a) and re.fullmatch(r'\d{3}',b): pairs[(a,b)].add(obj)
SKIP={'000','740','001','002','003','004','005','031','032','033','034','016','017','018'}
cand=[p for p,s in pairs.items() if len(s)>=15 and not (set(p)&SKIP)]
P('pairs with >= 15 objects and no jar / count / lost sign:',len(cand))
rowsE=[]
Dobj=D.set_index('object',drop=False)
for p in cand:
    objs=pairs[p]; sub=O[O.object.isin(objs)]
    # preceding sign per face
    bef=[];aft=[]
    for t in D[D.object.isin(objs)].toks:
        i=pos(t,list(p))
        if i is None: continue
        bef.append(t[i-1] if i>0 else '^'); aft.append(t[i+2] if i+2<len(t) else '$')
    bs_=collections.Counter(bef); as_=collections.Counter(aft)
    cc=collections.Counter(sub.site); k=len(sub)
    tvp=0.5*sum(abs(cc.get(s,0)/k-base[s]) for s in base.index)
    rowsE.append(dict(pair='-'.join(p),objects=k,sites=len(cc),tv=tvp,beforeDistinctPerFace=len(bs_)/len(bef),afterDistinctPerFace=len(as_)/len(aft),
        topBefore=bs_.most_common(1)[0][1]/len(bef),tag=(sub.grp=='tag').mean(),abroad=int(sub.abroad.sum()),mdshare=(sub.site=='Mohenjo-daro').mean(),hshare=(sub.site=='Harappa').mean()))
E=pd.DataFrame(rowsE).sort_values('objects',ascending=False)
E.to_csv(R+'work_scripts/travelled_out/pair_profiles.csv',index=False)
me=E[E.pair=='590-390'].iloc[0]
P(E.head(25).round(3).to_string(index=False))
for col in ['objects','sites','tv','beforeDistinctPerFace','afterDistinctPerFace','tag','abroad']:
    P(f'{col}: 590-390 = {me[col]:.3f}; rank {int((E[col]>me[col]).sum())+1} of {len(E)} (1 = highest)')
open(R+'work_scripts/travelled_out/tests_log.txt','w').write('\n'.join(out))
