"""C2: per-head vs per-trench vs conversion, on all multi-face tablets with a cup count."""
import warnings; warnings.filterwarnings('ignore')
from dm_common import *
from scipy import stats
R=pd.read_csv(f'{ROOT}/work_data/tablet_records_cup_load.csv',keep_default_na=False)
M=R[R.n>=2].copy()
def cupval(c):
    v=[x for x in c.split(',') if x]
    nv=[int(x[-1]) for x in v if x[-1].isdigit() and (x.startswith('F') or x.startswith('xF'))]
    return nv[0] if nv else np.nan
M['cupn']=M.cup.map(cupval)
M=M[M.cupn.notna()]
M['area2']=M.area.str.replace('ETrench 10W/11','E10W/11').str.strip()
print('multi-face tablets with a numbered cup',len(M),M.cupn.value_counts().sort_index().to_dict())
M['loads']=M.car.map(lambda c:'3' if 'S3' in c else ('bare' if c else 'none'))
print(pd.crosstab(M.loads,M.cupn))
# per-trench: cup distribution by area
big=M.area2.value_counts(); keep=big[big>=8].index
ct=pd.crosstab(M[M.area2.isin(keep)].area2,M.cupn); print(ct)
chi,p,dof,_=stats.chi2_contingency(ct); print('cup by trench chi2 %.1f dof %d p %.2g'%(chi,dof,p))
# per-head within E-11: loads 3 vs bare/none
E=M[M.area2=='ETrench 11']
print('E-11 only: cup by load status');print(pd.crosstab(E.loads,E.cupn))
# within-trench share of mode
for a in keep:
    x=M[M.area2==a].cupn; print(a,len(x),'mode',x.mode().iloc[0],'share %.2f'%(x.value_counts(normalize=True).iloc[0]))
# per-head predicted: cups per carrier constant?  3 loads -> cups; lone carrier -> cups
x=M[M.loads=='3'].cupn; y=M[M.loads=='bare'].cupn
print('cups | 3 loads: mean %.2f (n=%d)  cups | bare carrier: mean %.2f (n=%d)  MWU p %.3g'%(x.mean(),len(x),y.mean(),len(y),stats.mannwhitneyu(x,y).pvalue))
print('per-head prediction: cups(3 loads)/cups(1 load)=3; observed %.2f'%(x.mean()/y.mean()))
# same, carrier faces with bare carrier in E-11 vs 3 loads in E-11
print('E-11 bare-carrier tablets cup dist',E[E.loads=='bare'].cupn.value_counts().to_dict(),' E-11 3-load',E[E.loads=='3'].cupn.value_counts().to_dict())
# depth / time within E-11 (batch)
print(E[['cisi','cupn','loads','depth','time']].sort_values('cisi').to_string())
