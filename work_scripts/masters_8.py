"""Part 4 redesign: opener against X's first sign / last sign / animal / site (mutual information, shuffle p)."""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from masters_common import *
import numpy as np, random
from collections import Counter
C=pd.read_csv('/home/claude/ivc/work_data/masters/census.csv',dtype=str,keep_default_na=False)
S=C[C.grp=='seal'].copy()
S['opn']=S.opener.map(lambda o:'cap' if o=='060-920' else ('count' if o in('diamond','wheel','twin') else 'none'))
S['f']=S.X.str.split('-').str[0]; S['l']=S.X.str.split('-').str[-1]
def mi(a,b):
    n=len(a); ca=Counter(a); cb=Counter(b); cab=Counter(zip(a,b))
    return sum(v/n*np.log((v/n)/((ca[x]/n)*(cb[y]/n))) for (x,y),v in cab.items())
for col in ['f','l','sym','site']:
    d=S.copy()
    if col in('f','l'):
        top=set(k for k,v in Counter(d[col]).items() if v>=8); d=d[d[col].isin(top)]
    if col=='sym': d=d[~d.sym.isin(['','-'])]
    a=list(d[col]); b=list(d.opn); obs=mi(a,b)
    sims=[]
    for _ in range(500):
        bb=b[:]; random.shuffle(bb); sims.append(mi(a,bb))
    print(col,len(d),'MI %.4f'%obs,'shuffle mean %.4f'%np.mean(sims),'p',(np.sum(np.array(sims)>=obs)+1)/501)
# which first signs lean to cap / count
top=[k for k,v in Counter(S.f).items() if v>=10]
for k in top:
    d=S[S.f==k]; print(k,len(d),dict(Counter(d.opn)))
