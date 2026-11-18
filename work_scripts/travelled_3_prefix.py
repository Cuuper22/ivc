"""Job: the travelled name. Step 3: the three-sign prefix 920-060-741. All objects, what follows, which cities, the 741/742/745 selector, year-term tests.
Run: python3 travelled_3_prefix.py"""
import pandas as pd, numpy as np, collections, re
from scipy import stats
R='/home/antigravity/Cuuper22/ivc/'
np.random.seed(3)
G=pd.read_csv(R+'work_data/gloss2_all.csv',dtype=str)
M=pd.read_csv(R+'research/data/open_prototype/lipi/metadata_filtered.csv',dtype=str)
D=G.merge(M[['id','region','area-section','block-house','room-grid','period','phase','depth','symbol','material','horizontal(mm)','vertical(mm)','excavation-idno']],on='id',how='left',suffixes=('','_m'))
D['toks']=D.reading_order_text.str.split('-')
def has0(t,p): return t[:len(p)]==p
def has(t,p):
    n=len(p); return any(t[i:i+n]==p for i in range(len(t)-n+1))
def f(x):
    try: return float(x)
    except: return None
D['face']=[(f(a) or 0)*(f(b) or 0) or None for a,b in zip(D['horizontal(mm)'],D['vertical(mm)'])]
O=D.drop_duplicates('object')
N=len(O)
P=['920','060','741']
A=D[D.toks.map(lambda t:has(t,P))].copy()
print('faces',len(A),'objects',A.object.nunique())
print('at text start:',A.toks.map(lambda t:has0(t,P)).sum())
A['after']=A.toks.map(lambda t:'-'.join(t[[i for i in range(len(t)-2) if t[i:i+3]==P][0]+3:]))
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',50)
cols=['cisi','site','type','symbol','period','phase','area-section','block-house','depth','face','reading_order_text','after']
A=A.sort_values(['site','type','cisi'])
print(A[cols].to_string(index=False))
A.drop(columns=['toks']).to_csv(R+'work_scripts/travelled_out/prefix_920_060_741.csv',index=False)
obj=A.drop_duplicates('object')
base=O.site.value_counts()
print('\nby site: prefix objects | corpus objects | rate per 100')
tab=pd.DataFrame({'prefix':obj.site.value_counts(),'corpus':base}).fillna(0)
tab['prefix']=tab.prefix.astype(int)
tab['per100']=100*tab.prefix/tab.corpus
print(tab.sort_values('corpus',ascending=False).head(22).round(2).to_string())
# which large sites lack it
big=tab[tab.corpus>=25].sort_values('corpus',ascending=False)
n=len(obj)
print('\nsites with >=25 objects:',big.index.tolist())
print('expected objects at each if spread like corpus:')
for s,r in big.iterrows(): print(s,int(r.prefix),'observed','expected',round(n*r.corpus/N,1))
# type
def grp(t):
    if t.startswith('SEAL'): return 'seal'
    if t.startswith('TAB:C'): return 'copper'
    if t.startswith('TAB'): return 'tablet'
    if t.startswith('TAG'): return 'tag'
    if t.startswith('POT'): return 'pot'
    return 'other'
O2=O.assign(g=O.type.map(grp)); obj2=obj.assign(g=obj.type.map(grp))
print('\ngroup',obj2.g.value_counts().to_dict(),'corpus',O2.g.value_counts(normalize=True).round(3).to_dict())

# what follows: split into name (to jar) and ending
def X(t):
    i=[k for k in range(len(t)-2) if t[k:k+3]==P][0]
    r=[]
    for s in t[i+3:]:
        if s=='740': break
        r.append(s)
    return '-'.join(r)
A['X']=A.toks.map(X)
print('\nfirst sign after prefix:',collections.Counter(A.toks.map(lambda t:t[[k for k in range(len(t)-2) if t[k:k+3]==P][0]+3] if [k for k in range(len(t)-2) if t[k:k+3]==P][0]+3<len(t) else '$')).most_common(12))
print('X (name between prefix and jar):',A.X.value_counts().head(25).to_dict())
print('distinct X',A.X.nunique(),'of',len(A))
# ending
def end(t): return t[-1]
print('last sign:',collections.Counter(A.toks.map(end)).most_common(8))
print('ends in jar 740:',A.toks.map(lambda t:t[-1]=='740').sum(),' of ',len(A))

# whole 920-060 family: what comes third?
fam=D[D.toks.map(lambda t:has0(t,['920','060']))]
third=collections.Counter(t[2] if len(t)>2 else '$' for t in fam.toks)
print('\n920-060 at text start:',len(fam),'objects',fam.object.nunique(),' third sign:',third.most_common(10))
fam2=D[D.toks.map(lambda t:any(t[i:i+2] in (['692','060'],['550','060'],['820','060'],['920','060']) for i in range(len(t)-1)))]
rows=[]
for t in fam2.toks:
    for i in range(len(t)-1):
        if t[i:i+2] in (['692','060'],['550','060'],['820','060'],['920','060']):
            rows.append((t[i],t[i+2] if i+2<len(t) else '$'))
c=collections.Counter(rows)
print('cap head (920/692/550/820) -> sign after 060:'); 
for h in ['920','692','550','820']:
    print(h,{k[1]:v for k,v in c.items() if k[0]==h and v>=1})
# selector: 741/742/745 after 060
sel=collections.Counter()
for t in D.toks:
    for i in range(len(t)-2):
        if t[i+1]=='060' and t[i+2] in ('741','742','745') and t[i] in ('920','692','550','820'):
            sel[(t[i],t[i+2])]+=1
print('head x selector:',dict(sel))

# is the prefix tied to time? Mohenjo-daro period and Harappa phase
for site,col in [('Mohenjo-daro','period'),('Harappa','phase')]:
    s=O[O.site==site]; a=obj[obj.site==site]
    print(site,col,'prefix',dict(collections.Counter(a[col])),'corpus',dict(collections.Counter(s[col]).most_common(6)))
# depth
def dep(s):
    m=re.search(r'(-?\d+(\.\d+)?)\s*ft',str(s)); return abs(float(m.group(1))) if m else None
for site in ['Mohenjo-daro','Harappa']:
    a=[dep(x) for x in obj[obj.site==site].depth]; a=[x for x in a if x is not None]
    b=[dep(x) for x in O[O.site==site].depth]; b=[x for x in b if x is not None]
    print(site,'prefix depths ft',sorted(a),'median',np.median(a) if a else None,'corpus median',np.median(b))
# area (Mohenjo-daro)
print('Mohenjo-daro prefix areas',dict(collections.Counter(obj[obj.site=='Mohenjo-daro']['area-section'])),'corpus',dict(collections.Counter(O[O.site=='Mohenjo-daro']['area-section']).most_common(6)))
print('Harappa prefix areas',dict(collections.Counter(obj[obj.site=='Harappa']['area-section'])))
# animal
print('animals',dict(collections.Counter(obj.symbol)))
# seal size
sz=obj[(obj.type.str.startswith('SEAL'))].face.dropna()
allsz=O[O.type.str.startswith('SEAL')]
allsz=pd.to_numeric(allsz['horizontal(mm)'],errors='coerce')*pd.to_numeric(allsz['vertical(mm)'],errors='coerce')
print('prefix seal face median',sz.median(),'n',len(sz),'| all seals',allsz.median())
print('Mann-Whitney',stats.mannwhitneyu(sz,allsz.dropna(),alternative='two-sided'))
# same-name partners: names that appear WITH the prefix and WITHOUT it (the office stamps a master)
census=pd.read_csv(R+'work_data/masters/census.csv',dtype=str,keep_default_na=False)
names_with=set(A.X)-{''}
cnt=0
for x in sorted(names_with):
    w=census[(census.X==x)&(~census.text.str.startswith('920-060-741'))]
    if len(w)>0: print('name',x,'also without prefix on',len(w),'objects',dict(collections.Counter(w.site)))

# ---------------- extra tests ----------------
print('\n==== extra ====')
# 1. Harappa deficiency / Mohenjo excess
for s in ['Harappa','Mohenjo-daro']:
    k=(obj.site==s).sum(); p=(O.site==s).mean()
    print(s,'prefix objects',k,'expected',round(n*p,1),'binomial two-sided P',stats.binomtest(k,n,p).pvalue)
tab2=[[ (obj.site=='Mohenjo-daro').sum(), (obj.site=='Harappa').sum()],[(O.site=='Mohenjo-daro').sum(),(O.site=='Harappa').sum()]]
print('Mohenjo-daro vs Harappa rate ratio Fisher',stats.fisher_exact(tab2))
# 2. cap heads by site (family 'HEAD-060')
fam=collections.defaultdict(list)
for o,s,t in zip(D.object,D.site,D.toks):
    for i in range(len(t)-1):
        if t[i+1]=='060' and t[i] in ('920','692','550','820','795','201'):
            fam[t[i]].append((o,s)); break
for h in ('920','692','550','820'):
    v=list(set(fam[h])); c=collections.Counter(s for _,s in v)
    print(h,'-060 objects',len(v),dict(c.most_common(8)))
# 3. selector by site
sel_objs=collections.defaultdict(set)
for o,s,t in zip(D.object,D.site,D.toks):
    for i in range(len(t)-2):
        if t[i:i+2]==['920','060'] and t[i+2] in ('741','742','745'): sel_objs[t[i+2]].add((o,s))
for k in ('741','742','745'):
    print('920-060-'+k, len(sel_objs[k]), dict(collections.Counter(s for _,s in sel_objs[k]).most_common(8)))
# 4. what is after 742 / 745
for k in ('742','745'):
    rows=D[D.toks.map(lambda t:has(t,['920','060',k]))]
    print(k,[ (r.cisi,r.site,r.type,r.reading_order_text) for r in rows.itertuples()])
# 5. length of name after prefix vs after other caps
def namelen(t,P_):
    i=[k for k in range(len(t)-len(P_)+1) if t[k:k+len(P_)]==P_][0]
    r=[]
    for s in t[i+len(P_):]:
        if s=='740': break
        r.append(s)
    return len(r)
nl=[namelen(t,P) for t in A.toks]
print('name length after 920-060-741: mean',np.mean(nl),collections.Counter(nl))
allX=pd.read_csv(R+'work_data/masters/census.csv',dtype=str,keep_default_na=False)
allX['L']=allX.X.str.count('-')+1
allX.loc[allX.X=='','L']=0
print('name length across all jar-names mean',allX.L.mean(),collections.Counter(allX.L).most_common(6))
# 6. 590-390 co-occurrence with the 060 cap family
tgt=['590','390']
H=D[D.toks.map(lambda t:has(t,tgt))]
def cap(t): return any(t[i+1]=='060' for i in range(min(3,len(t)-1)))
hc=H[H.toks.map(cap)].drop_duplicates('object')
allc=O[O.toks.map(cap)]
print('590-390 objects with an X-060 cap in the first 3 signs:',len(hc),'of',H.object.nunique(),'| corpus',len(allc),'of',N,'=',round(len(allc)/N,4),
      'binomial P(>=)',stats.binom.sf(len(hc)-1,H.object.nunique(),len(allc)/N))
print(hc[['cisi','site','reading_order_text']].to_string(index=False))
c920=H[H.toks.map(lambda t:has(t,['920','060']))].drop_duplicates('object')
print('590-390 with 920-060:',len(c920),' corpus rate 920-060',O.toks.map(lambda t:has0(t,['920','060'])).mean(),' P',stats.binom.sf(len(c920)-1,H.object.nunique(),O.toks.map(lambda t:has0(t,['920','060'])).mean()))
# 7. 060 anywhere in 590-390 texts
print('590-390 objects with 060 anywhere:',H[H.toks.map(lambda t:'060' in t)].object.nunique(),'corpus rate',O.toks.map(lambda t:'060' in t).mean())
