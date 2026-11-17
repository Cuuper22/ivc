"""A5: tablets carrying 'n diamond' faces: where, which count, equality with load count; batch test."""
import warnings; warnings.filterwarnings('ignore')
from dm_common import *
d=load()
t=d[d.istab|d.type.isin(['TAG','TAG:P','TAG:L'])]
rows=[]
for cisi,g in d[d.istab&(d.cisi!='-')].groupby('cisi'):
    faces=[' '.join(x) for x in g.toks]
    has=lambda pat:any(f==pat for f in faces)
    rows.append(dict(cisi=cisi,site=g.site.iloc[0],area=g['area-section'].iloc[0],mat=g.material.iloc[0],depth=g.depth.iloc[0],time=g.time.iloc[0],n=len(g),faces=' | '.join(faces)))
R=pd.DataFrame(rows)
D=R[R.faces.str.contains('861')]
print('tablet records with 861 anywhere',len(D))
X=R[R.faces.str.contains(r'(^| )003 861( |$)')]
print('003 861 faces: records',len(X)); print(X.area.value_counts().to_dict(), X.mat.value_counts().to_dict(), X.time.value_counts().to_dict())
# all tablet faces (single face too) with 861 preceded by count: counts by area
f=d[d.istab&d.toks.map(lambda t:any(t[i]=='861' and i>0 and t[i-1] in CNT for i in range(len(t))))]
print('faces n X861',len(f)); 
f['c']=f.toks.map(lambda t:[lab(t[i-1]) for i in range(1,len(t)) if t[i]=='861' and t[i-1] in CNT][0])
print(pd.crosstab(f['area-section'],f.c))
# equality with carrier count across all multi-face tablets
eq=[];
for cisi,g in d[d.istab&(d.cisi!='-')].groupby('cisi'):
    dc=[];cc=[]
    for x in g.toks:
        for i in range(1,len(x)):
            if x[i]=='861' and x[i-1] in CNT: dc.append(lab(x[i-1]))
            if x[i] in('156','154','158','151') and x[i-1] in CNT: cc.append(lab(x[i-1]))
    if dc and cc: eq.append((cisi,dc,cc))
print('tablets with both diamond-count and carrier-count:',len(eq),'equal',sum(a==b for _,a,b in eq),[e for e in eq if e[1]!=e[2]])
# wheel / 817 faces on tablets with counts by area
for s in['817','820']:
    f=d[d.istab&d.toks.map(lambda t:s in t)]
    print(s,'tablet faces',len(f),f['area-section'].value_counts().head(5).to_dict(), 'material',f.material.value_counts().to_dict())
# opener on tablets by area: 861 vs 817 vs 820 composition per trench (batch test)
tt=d[d.istab&~d.broken]
tt['op']=tt.toks.map(lambda t:next((x for x in t[:1] if x in('861','817','820')),None))
tt=tt[tt.op.notna()]
print(pd.crosstab(tt['area-section'],tt.op).sort_values('861',ascending=False).head(10))
