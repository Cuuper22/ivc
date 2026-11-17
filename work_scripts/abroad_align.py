#!/usr/bin/env python3
"""Round-seal alignment: positions, pairs, abroad-only signs, home name signs missing abroad, 001 context. Reading order."""
from abroad_seals import *
from scipy.stats import fisher_exact
rnd=ab[ab.cat=='round']; sq=ab[ab.cat=='square']
hs=home[home.type.str.startswith('SEAL')].copy(); hs['rd']=hs.text.apply(rd)
R=[t for t in rnd.rd]; 
print('round seals',len(R),'signs',sum(len(t) for t in R))
cnt=collections.Counter(s for t in R for s in t if s!='000')
hc=collections.Counter(s for t in hs.rd for s in t if s!='000'); H=sum(hc.values()); N=sum(cnt.values())
print('\n== signs on round seals (count, seals, home share, round share, ratio, Fisher p)')
rows=[]
for s,n in cnt.most_common():
    ns=sum(s in t for t in R)
    a=n; b=N-n; c=hc[s]; dd=H-c
    p=fisher_exact([[a,b],[c,dd]])[1]
    rows.append((s,n,ns,c/H*100,n/N*100,(n/N)/(max(c,0.5)/H),p))
for r in rows[:40]: print(f'{r[0]} {short(r[0]):28} n={r[1]} seals={r[2]} home%={r[3]:.2f} round%={r[4]:.2f} x{r[5]:.1f} p={r[6]:.1e} home_n={hc[r[0]]}')
print('\nsigns on round seals never or <=3 at home:',[(s,cnt[s],hc[s]) for s in cnt if hc[s]<=3])
# all abroad
allc=collections.Counter(s for t in ab.rd for s in t if s!='000')
print('abroad-all signs with home n<=3:',[(s,allc[s],hc[s]) for s in allc if hc[s]<=3])
# position profile: first / last / pos
print('\n== first sign / last sign (reading order) on round seals, ignoring lost')
fs=collections.Counter(t[0] for t in R if t and t[0]!='000'); ls=collections.Counter(t[-1] for t in R if t and t[-1]!='000')
print('first',fs.most_common(10)); print('last',ls.most_common(10))
# in stored (mirrored) order
fs2=collections.Counter(t[-1] for t in R if t and t[-1]!='000'); 
print('\n== pairs (adjacent, reading order) appearing on >=2 round seals')
pc=collections.Counter(); 
for t in R:
    for a,b in set(zip(t,t[1:])):
        if '000' not in (a,b): pc[(a,b)]+=1
for k,v in pc.most_common():
    if v>=2: print(k,v)
print('\n== sign pairs (any distance, order kept) on >=2 round seals')
pc2=collections.Counter()
for t in R:
    tt=[x for x in t if x!='000']
    for i,j in set(itertools.combinations(range(len(tt)),2)): pc2[(tt[i],tt[j])]+=1
for k,v in pc2.most_common(40):
    if v>=2: print(k,v)
# 001 context
print('\n== 001 on round seals: neighbours (reading order)')
for r in rnd.itertuples():
    t=r.rd
    for i,s in enumerate(t):
        if s=='001': print(r.id,r.site,'-'.join(t),' prev',t[i-1] if i else '^',' next',t[i+1] if i+1<len(t) else '$')
n001=sum('001' in t for t in R); print('round seals with 001:',n001,'of',len(R),' square:',sum('001' in t for t in sq.rd),'of',len(sq),' home seals:',sum('001' in t for t in hs.rd),'of',len(hs))
# home context of 001: prev/next signs
pc_prev=collections.Counter(); pc_next=collections.Counter()
for t in hs.rd:
    for i,s in enumerate(t):
        if s=='001':
            pc_prev[t[i-1] if i else '^']+=1; pc_next[t[i+1] if i+1<len(t) else '$']+=1
print('home 001 prev',pc_prev.most_common(8),'next',pc_next.most_common(8))
# home name signs never abroad
nr=pd.read_csv(f'{ROOT}/work_data/name_rows.csv',dtype=str)
print(nr.columns.tolist())
