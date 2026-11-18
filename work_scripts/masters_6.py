"""Part 2: X elsewhere. For each candidate X, find every object whose text contains X as a contiguous run (not as a longer name's piece), by group/site/abroad."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from masters_common import *
from collections import Counter
C=pd.read_csv('/home/antigravity/Cuuper22/ivc/work_data/masters/census.csv',dtype=str,keep_default_na=False)
def grp(t):
    if t.startswith('SEAL'): return 'seal'
    if t.startswith('TAB:C'): return 'copper'
    if t.startswith('TAB'): return 'tablet'
    if t.startswith('TAG'): return 'tag'
    if t.startswith('POT'): return 'pot'
    return 'other'
D['grp']=D.type.map(grp)
ABROAD={'Persian Gulf','Mesopotamia','Iranian Plateau','Central Asia'}
def has(toks,x):
    n=len(x)
    return any(toks[i:i+n]==x for i in range(len(toks)-n+1))
def profile(X):
    x=X.split('-'); rows=D[[has(t,x) for t in D.toks]]
    # collapse: objects
    out=dict(X=X,rows=len(rows),objects=rows.object.nunique(),sites=len(set(rows.site)),
      grp=dict(Counter(rows.grp)),abroad=int(rows.region.isin(ABROAD).sum()),cities=dict(Counter(rows.site).most_common(6)))
    return out,rows
if __name__=='__main__':
    cands=['176','503-615-752','806-845-061-407-850-900','705-500-741-001-055-220','347-741-176','104-645-590-235-240','235-240','806-235-590-405','048','706-033-923','590-390','013-840','803-415-220-318-920-255-436-690-590-407','840-032','255-435-690','415-100','240-415-100','605-760','061-171-035','705-255','027-032','617-892','792','630','240-482','235-220-176','240-904']
    P=[]
    for x in cands:
        o,r=profile(x); P.append(o); print(o)
    pd.DataFrame(P).to_csv('/home/antigravity/Cuuper22/ivc/work_data/masters/candidate_profiles.csv',index=False)
