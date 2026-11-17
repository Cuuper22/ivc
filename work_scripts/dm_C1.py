"""C1: cups vs loads vs diamonds on every multi-face tablet; per-head / per-trench / conversion tests."""
import warnings; warnings.filterwarnings('ignore')
from dm_common import *
from scipy import stats
d=load()
T=d[d.istab&(d.cisi!='-')]
CAR=('151','153','154','155','156','158')
recs=[]
for cisi,g in T.groupby('cisi'):
    cup=[];car=[];dia=[];faces=[]
    for toks in g.toks:
        faces.append(' '.join(toks))
        for i,x in enumerate(toks):
            if x=='700':
                if i>0 and toks[i-1] in CNT: cup.append(lab(toks[i-1]))
                elif i+1<len(toks) and toks[i+1] in CNT: cup.append('x'+lab(toks[i+1]))
                else: cup.append('bare')
            if x in CAR:
                if i>0 and toks[i-1] in CNT: car.append(lab(toks[i-1]))
                else: car.append('bare')
            if x=='861':
                if i>0 and toks[i-1] in CNT: dia.append(lab(toks[i-1]))
                elif i+1<len(toks) and toks[i+1] in CNT: dia.append('x'+lab(toks[i+1]))
                else: dia.append('bare')
    r=g.iloc[0]
    recs.append(dict(cisi=cisi,n=len(g),site=r.site,area=r['area-section'],mat=r.material,depth=r.depth,time=r.time,cup=','.join(cup),car=','.join(car),dia=','.join(dia),faces=' | '.join(faces),broken=g.broken.any(),lost=g.lost.any()))
R=pd.DataFrame(recs); R.to_csv(f'{ROOT}/work_data/tablet_records_cup_load.csv',index=False)
M=R[R.n>=2]
print('multi-face tablets',len(M))
both=M[(M.cup!='')&(M.car!='')]
print('with cup and carrier faces',len(both)); print(pd.crosstab(both.cup,both.car))
print('with cup and diamond',len(M[(M.cup!='')&(M.dia!='')])); print(pd.crosstab(M[(M.cup!='')&(M.dia!='')].cup,M[(M.cup!='')&(M.dia!='')].dia))
print('with carrier and diamond (any cup)',len(M[(M.car!='')&(M.dia!='')])); print(pd.crosstab(M[(M.car!='')&(M.dia!='')].car,M[(M.car!='')&(M.dia!='')].dia))
# carrier faces across ALL tablets (single face too)
print('\nall tablet faces with carrier: count dist'); 
c=collections.Counter()
for r in d[d.istab].itertuples():
    for i,x in enumerate(r.toks):
        if x in CAR: c[(x,lab(r.toks[i-1]) if i>0 and r.toks[i-1] in CNT else 'bare')]+=1
print(sorted(c.items(),key=lambda z:-z[1])[:14])
# Per-head: cups per carrier among 22
std=both[both.car.isin(['S3','S3,S3'])|both.car.str.contains('S3')]
print('\nboth-with-S3-carrier tablets',len(std),std.cup.value_counts().to_dict())
# conversion test: for carrier != S3
oth=both[~both.car.str.contains('S3')]
print('carrier not S3:',oth[['cisi','cup','car','dia','faces']].to_string())
