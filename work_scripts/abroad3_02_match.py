"""Third way in, item 2. Corrected string from the photograph vs every Lipi catalogue text.
Prediction first: (a) if the photograph's five signs are right, at least one home text carries the 4-sign tail 705 002 004 390 or 002 004 390 with 127 or 705 before it;
(b) objects sharing 3+ signs in order are goods tags / craft-town objects, with unicorn or bull as animal on most.
Query is in reading order (toks column is reading order)."""
import sys
sys.path.insert(0,'/home/claude/ivc/work_scripts')
from cotton_common import *
import itertools, csv
Q=['127','705','002','004','390']
d=faces()
u=d[d.id=='3884.1'].iloc[0]; print('catalogue Umma toks:',u.toks, u.symbol, u.type, u.site)
def lcs_sub(t,q):
    # longest common subsequence length and the matched signs
    n,m=len(t),len(q); L=[[0]*(m+1) for _ in range(n+1)]
    for i in range(n-1,-1,-1):
        for j in range(m-1,-1,-1):
            L[i][j]=L[i+1][j+1]+1 if t[i]==q[j] else max(L[i+1][j],L[i][j+1])
    i=j=0; out=[]
    while i<n and j<m:
        if t[i]==q[j]: out.append(t[i]); i+=1; j+=1
        elif L[i+1][j]>=L[i][j+1]: i+=1
        else: j+=1
    return out
def contig(t,q):
    best=[]
    for i in range(len(t)):
        for j in range(len(q)):
            k=0
            while i+k<len(t) and j+k<len(q) and t[i+k]==q[j+k]: k+=1
            if k>len(best): best=t[i:i+k]
    return best
rows=[]
for _,r in d.iterrows():
    if r.id=='3884.1': continue
    t=[x for x in r.toks]
    s=lcs_sub(t,Q); c=contig(t,Q)
    if len(s)>=3 or len(c)>=3:
        rows.append(dict(id=r.id,cisi=r.cisi,site=r.site,type=r.type,material=r.material,animal=r.symbol,text=' '.join(t),shared_in_order=' '.join(s),n_shared=len(s),contig=' '.join(c),n_contig=len(c)))
out=pd.DataFrame(rows).sort_values(['n_contig','n_shared'],ascending=False)
out.to_csv('/home/claude/ivc/work_data/abroad3/home_matches_3plus.csv',index=False)
print(len(out),'home faces share >=3 signs in order (subsequence) or contiguous')
print(out.n_shared.value_counts().to_dict(), out.n_contig.value_counts().to_dict())
pd.set_option('display.width',250,'display.max_colwidth',60,'display.max_rows',200)
print(out[(out.n_shared>=4)|(out.n_contig>=3)][['id','site','type','animal','text','shared_in_order','n_contig']].to_string())
# the 2-4-tree tail and 705 before 002/004
print('\ncontaining contiguous 002 004 390 :',[ (r.id,r.site,r.symbol,' '.join(r.toks)) for _,r in d.iterrows() if ' '.join(['002','004','390']) in ' '.join(r.toks)])
print('containing 705 ... 002 004 :',[ (r.id,r.site,r.symbol,' '.join(r.toks)) for _,r in d.iterrows() if '705' in r.toks and ' '.join(['002','004']) in ' '.join(r.toks)])
print('containing 127 ... 705 :',[ (r.id,r.site,r.symbol,' '.join(r.toks)) for _,r in d.iterrows() if ' '.join(['127','705']) in ' '.join(r.toks)])
# pair statistics for the two signs that make the Umma line unique
import collections
home=d[d.id!='3884.1']
def nxt(a):
    c=collections.Counter()
    for t in home.toks:
        for i in range(len(t)-1):
            if t[i]==a: c[t[i+1]]+=1
    return c
for a in ['127','705']:
    c=nxt(a); print(f'\nhome: {a} occurs {sum(1 for t in home.toks for x in t if x==a)} times; followed by:',c.most_common(8))
prev=collections.Counter(t[i-1] for t in home.toks for i in range(1,len(t)) if t[i]=='127'); print('before 127:',prev.most_common(6))
print('127 position: first sign in',sum(1 for t in home.toks if t and t[0]=='127'),'of',sum(1 for t in home.toks if '127' in t))
print('705 then 002/003/004 count:',sum(1 for t in home.toks for i in range(len(t)-1) if t[i]=='705' and t[i+1] in {'002','003','004','005','006','007','031','032','033','034'}))
for _,r in home[home.toks.apply(lambda t:'127' in t)].iterrows(): print('127 text',r.id,r.site,r.symbol,' '.join(r.toks))
