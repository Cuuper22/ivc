"""A2: 2-diamond vs 2-wheel vs 2-817 vs 060-920-opener seals: animal, class, size, zone, period, site."""
from dm_common import *
from scipy import stats
d=load()
s=d[d.isseal&~d.broken&~d.lost&(d.toks.map(len)>=3)].copy()
def grp(t):
    if t[:2]==['861','002']: return 'D2 (861+2)'
    if t[:2]==['817','002']: return 'D2b (817+2)'
    if t[:2]==['820','002']: return 'W2 (820+2)'
    if t[:2]==['820','001']: return 'W1 (820+1)'
    if t[0]=='060' or t[:2]==['920','060'] or (t[0] in('692','550','820') and len(t)>1 and t[1]=='060'): return 'CAP (060-920)'
    return 'rest'
s['grp']=s.toks.map(grp)
CL={'740':'jar','520':'spear','090':'person','400':'comb','151':'carrier','154':'carrier','156':'carrier','158':'carrier'}
s['cls']=s.toks.map(lambda t:CL.get(t[-1],'other'))
s['animal']=s.symbol.replace({'-':'unk','None':'none'}).map(lambda x:'bull' if x.startswith('Bull') else x)
def zone(r):
    a=r['area-section']
    if r.site=='Harappa':
        a2=a.strip('-').strip()
        return 'H:'+(a2[:2] if a2 else '?')
    if r.site=='Mohenjo-daro':
        return 'M:'+a.strip('-').strip().split('.')[0].replace(' ','')[:4]
    return r.site[:5]
s['zone']=s.apply(zone,axis=1)
def per(r):
    p=r.time
    if p in('-',''):
        p=r.period
    return p
s['per']=s.apply(per,axis=1)
s['sz']=s.area
print(s.grp.value_counts())
G=['D2 (861+2)','D2b (817+2)','W2 (820+2)','W1 (820+1)','CAP (060-920)','rest']
def cram(a,b,sub):
    ct=pd.crosstab(a[sub],a['grp']); ct=ct[[c for c in ct.columns if c in b]]
    ct=ct.loc[ct.sum(1)>=3]
    chi,p,dof,_=stats.chi2_contingency(ct); n=ct.values.sum(); v=(chi/(n*(min(ct.shape)-1)))**.5
    return ct,chi,p,dof,v
for col in ['cls','animal','site','zone','per','material','shape']:
    ss=s.copy()
    for pair in [('D2 (861+2)','W2 (820+2)'),('D2 (861+2)','D2b (817+2)'),('D2 (861+2)','CAP (060-920)'),('W2 (820+2)','CAP (060-920)'),('D2 (861+2)','rest')]:
        ct,chi,p,dof,v=cram(ss,pair,col)
        print(f'{col:9s} {pair[0][:3]} vs {pair[1][:4]}: chi2 {chi:6.1f} dof {dof} p {p:.3g} V {v:.2f}')
print()
# shares
for col in ['cls','animal','site','material','shape']:
    ct=pd.crosstab(s[col],s.grp,normalize='columns').round(2)
    ct=ct.loc[(pd.crosstab(s[col],s.grp).sum(1)>=25)]
    print(col);print(ct[G]);print()
print('size median mm2');print(s.groupby('grp').sz.agg(['count','median','mean']).round(0))
for a,b in [('D2 (861+2)','W2 (820+2)'),('D2 (861+2)','CAP (060-920)'),('W2 (820+2)','CAP (060-920)'),('D2 (861+2)','D2b (817+2)'),('D2 (861+2)','rest')]:
    x=s[s.grp==a].sz.dropna();y=s[s.grp==b].sz.dropna();print(a,b,'MWU p',round(stats.mannwhitneyu(x,y).pvalue,4))
print('text length');print(s.groupby('grp').toks.apply(lambda x:x.map(len).mean()).round(2))
# co-occurrence of opener signs in same text
for a,b in [('861','817'),('861','820'),('817','820')]:
    n=sum((a in t and b in t) for t in s.toks); print(a,b,'cooccur in seals',n,'of',sum(a in t for t in s.toks),sum(b in t for t in s.toks))
s.to_pickle('/tmp/seals_dm.pkl')
