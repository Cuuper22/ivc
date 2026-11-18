"""Crest-level institutions: sign in the name slot (X before jar), counted over all object groups. 705/706 merged (variant drawings)."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from masters_common import *
from collections import Counter, defaultdict
C=pd.read_csv('/home/antigravity/Cuuper22/ivc/work_data/masters/census.csv',dtype=str,keep_default_na=False)
MERGE={'706':'705'}
rows=[]
for r in C.itertuples():
    for s in set(MERGE.get(x,x) for x in r.X.split('-')):
        rows.append((s,r.id,r.object,r.site,r.grp,r.noun,r.X,r.type))
S=pd.DataFrame(rows,columns=['sign','id','object','site','grp','noun','X','type'])
agg=S.groupby('sign').agg(n=('id','size'),sites=('site','nunique'),
  seal=('grp',lambda s:(s=='seal').sum()),tablet=('grp',lambda s:(s=='tablet').sum()),copper=('grp',lambda s:(s=='copper').sum()),tag=('grp',lambda s:(s=='tag').sum()),pot=('grp',lambda s:(s=='pot').sum()),
  man=('noun',lambda s:(s=='090').sum()),comb=('noun',lambda s:(s=='400').sum()),
  Xn=('X','nunique'))
agg=agg.sort_values('n',ascending=False)
agg.to_csv('/home/antigravity/Cuuper22/ivc/work_data/masters/crest_summary.csv')
print(agg.head(30).to_string())
# signs with seal, tablet and tag all present, >=4 sites
print(agg[(agg.seal>0)&(agg.tablet>0)&(agg.tag>0)].head(20).to_string())
