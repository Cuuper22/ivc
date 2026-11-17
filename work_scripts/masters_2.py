"""Part 1/2: census of X (signs before the jar, opener removed) over ALL object types, and what tablet-headed X's issue.
Writes work_data/masters/census.csv, x_summary.csv"""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from masters_common import *
from collections import Counter
def grp(t):
    if t.startswith('SEAL'): return 'seal'
    if t.startswith('TAB:C'): return 'copper'
    if t.startswith('TAB'): return 'tablet'
    if t.startswith('TAG'): return 'tag'
    if t.startswith('POT'): return 'pot'
    return 'other'
rows=[]
for r in D.itertuples():
    t=r.toks
    if t.count('740')!=1: continue
    j=t.index('740'); op,pre=split_open(t[:j])
    if not pre or '000' in pre: continue
    rows.append(dict(id=r.id,object=r.object,cisi=r.cisi,site=r.site,region=r.region,type=r.type,grp=grp(r.type),X='-'.join(pre),opener=opener_type(op),noun=(t[j+1] if j+1<len(t) else 'none'),after='-'.join(t[j+1:]),sym=r.symbol if isinstance(r.symbol,str) else '',face=r.face,area=r._asdict().get('_18',''),text=r.reading_order_text))
C=pd.DataFrame(rows)
# attach area & other columns by merge
C=C.merge(M[['id','area-section','block-house','period']],on='id')
C.to_csv('/home/claude/ivc/work_data/masters/census.csv',index=False)
# per object (collapse faces): keep first face per object
S=C.groupby('X').agg(n=('id','size'),objs=('object','nunique'),sites=('site',lambda s:len(set(s))),site_list=('site',lambda s:dict(Counter(s))),
   grps=('grp',lambda s:dict(Counter(s))),nouns=('noun',lambda s:dict(Counter(s))),animals=('sym',lambda s:dict(Counter(x for x in s if x not in('','-')))),
   med_face=('face',lambda s:s[s>0].median())).sort_values('n',ascending=False)
S.to_csv('/home/claude/ivc/work_data/masters/x_summary.csv')
pd.set_option('display.width',250,'display.max_colwidth',120)
print(len(C),'texts with X;',C.X.nunique(),'distinct X')
print(S.head(40)[['n','sites','grps','nouns','animals']].to_string())
