"""Multi-face tablets as records: group faces by cisi, pair the cup face with the other faces."""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from counted_common import *
a=pd.read_csv(DATA,dtype=str,keep_default_na=False)
a=a[(a.cisi!='-')&a['type'].str.startswith('TAB')]
rd=lambda t:' '.join(t.strip('+[]').split('-')[::-1])
recs=[]
for c,g in a.groupby('cisi'):
    if len(g)<2: continue
    faces=[rd(t) for t in g.text]
    recs.append(dict(cisi=c,site=g.site.iloc[0],type=g.type.iloc[0],mat=g.material.iloc[0],area=g['area-section'].iloc[0],n=len(g),faces=faces,ids=list(g.id)))
R=pd.DataFrame(recs); print('multi-face tablets',len(R),R.n.value_counts().to_dict())
def cupface(f):
    t=f.split()
    return t[0] if len(t)==2 and t[1]=='700' else None
def cupcount(faces):
    for f in faces:
        t=f.split()
        if len(t)==2 and t[1]=='700' and t[0] in CNT: return CNT[t[0]][1] if CNT[t[0]][0]=='F' else 's'+str(CNT[t[0]][1])
        if len(t)==2 and t[0]=='700' and t[1] in CNT: return 'x'+str(CNT[t[1]][1])
    return None
R['cup']=R.faces.map(cupcount)
print(R.cup.value_counts(dropna=False).to_dict())
# per cup value: which 2-sign count faces accompany
for cv in ['2','3','4']:
    S=R[R.cup==cv]; print('\ncup',cv,'tablets',len(S))
    cnt=collections.Counter()
    for fs in S.faces:
        for f in fs:
            if len(f.split())==2 and f.split()[1]!='700': cnt[f]+=1
    print(cnt.most_common(8))
    print(collections.Counter(len(x) for x in S.faces))
# faces 003 861 and 003 156 vs cup
for pat in ['003 861','003 156']:
    S=R[R.faces.map(lambda fs:pat in fs)]; print(pat,len(S),S.cup.value_counts(dropna=False).to_dict())
# faces cup+4 : share of other faces
S=R[R.cup=='4']; tot=sum(len(f) for f in S.faces)
print('cup4 tablets',len(S),'faces',tot,collections.Counter(f for fs in S.faces for f in fs if '700' not in f).most_common(6))
# fronts opening with 003 / closing with 156 (all tablets, first face)
def first_open(fs): return [f for f in fs if '700' not in f]
R.to_pickle('/tmp/R.pkl')

print('\n=== by cup value (int) ===')
R['cupv']=R.cup.map(lambda x:x if isinstance(x,int) else None)
def fronts(fs): return [f for f in fs if '700' not in f.split()]
rows=[]
for r in R.itertuples():
    if r.cupv is None: continue
    for f in fronts(r.faces):
        t=f.split(); rows.append(dict(cisi=r.cisi,cup=r.cupv,front=f,first=t[0],last=t[-1],n=len(t),site=r.site,area=r.area,mat=r.mat,nfaces=r.n))
F=pd.DataFrame(rows); F.to_csv(f'{ROOT}/work_data/counted/tablet_fronts.csv',index=False)
print('fronts',len(F),F.cup.value_counts().to_dict())
for cv in [2,3,4]:
    X=F[F.cup==cv]; print('\ncup',cv,'fronts',len(X),'tablets',X.cisi.nunique())
    print(' last',X['last'].value_counts().head(8).to_dict()); print(' first',X['first'].value_counts().head(8).to_dict())
    print(' len',X.n.value_counts().sort_index().to_dict(), ' sites',X.site.value_counts().head(3).to_dict(),'areas',X.area.value_counts().head(4).to_dict(),'mats',X.mat.value_counts().to_dict())
# tablets with a front opening 003 -> cup
for lab,cond in [('front starts 003',lambda x:x['first']=='003'),('front ends 156',lambda x:x['last']=='156'),('front ends 861',lambda x:x['last']=='861'),('front ends 740',lambda x:x['last']=='740'),('front starts 032',lambda x:x['first']=='032'),('front has 840',lambda x:'840' in x['front'].split())]:
    X=F[F.apply(cond,axis=1)]; print(lab,len(X),X.cup.value_counts().to_dict())
# does the front's own tail carry a count that tracks the cup?  front ending in count/jar
F['lastcnt']=F['front'].map(lambda f:next((CNT[x][1] for x in f.split()[::-1] if x in CNT and CNT[x][0]=='F'),None))
print(pd.crosstab(F.cup,F.lastcnt.fillna(0)))
