"""Part 1 on seals only + Part 4 openers. Agent seals = SEAL* objects, X jar {man,comb,679,621}."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from masters_common import *
from collections import Counter
import random
C=pd.read_csv('/home/antigravity/Cuuper22/ivc/work_data/masters/census.csv',dtype=str,keep_default_na=False); C['face']=C.face.astype(float)
NOUN={'090':'man','400':'comb','679':'679','621':'621'}
ag=C[C.noun.isin(NOUN)&(C.grp=='seal')].copy(); ag['n']=ag.noun.map(NOUN)
own=C[(C.noun=='none')&(C.grp=='seal')]
print('SEAL agent texts',len(ag),ag.n.value_counts().to_dict())
for n in NOUN.values():
    a=ag[ag.n==n]; c=a.X.value_counts()
    print('--',n,'seals',len(a),'distinct X',a.X.nunique(),'X with >=2 seals',(c>=2).sum(),'sites',dict(Counter(a.site)))
    print('  animals',dict(Counter(a.sym)),'median face',a.face[a.face>0].median())
    print('  X with >=2:',[(x,k) for x,k in c.items() if k>=2])
    print('  X also an owner seal (X jar alone, seal):',sum(1 for x in a.X.unique() if x in set(own.X)),'of',a.X.nunique())
    print('  opener',dict(Counter(a.opener)))
# man seals list
print(ag[ag.n=='man'][['cisi','site','area-section','block-house','X','sym','face','opener','text']].to_string())
# first-sign share among agent X's vs among owner X's
def first(x): return x.split('-')[0]
fa=Counter(first(x) for x in ag[ag.n=='man'].X); fo=Counter(first(x) for x in own.X)
print('man first signs',fa.most_common(8)); print('owner first signs',fo.most_common(8))
tags=lambda s: set(x.split('-')[-1] for x in s)
# does X match crest of seal's own house? skipping, earlier job did (4/20)
