"""Do agent seals (`X jar man`) favour particular animals compared with owner seals (`X jar`)?
PREDICTION written before the numbers: if animal were rank/office, agents (junior to the master) would use common beasts (unicorn) more and rare beasts less; ratio for rare beasts (not unicorn) <0.8.
Null: labels shuffled inside site x shape."""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from animal_common import *
rng=np.random.default_rng(9); NP=5000
d=b[(b.g!='')&(b.g!='NONE')&b.noun_c.isin(['090','none'])&(b.X_c!='')].copy().reset_index(drop=True)
d['agent']=(d.noun_c=='090').astype(int); st=strata_idx((d.site2+'|'+d['shape']).values)
print('agents',d.agent.sum(),'owners',(1-d.agent).sum()); print(pd.crosstab(d.g,d.agent))
for grp in ['UNI','ZEBU','ELEPH','SHORT','WILD3','COMP','GOAT']:
    x=(d.g==grp).values.astype(int); obs=x[d.agent==1].mean(); null=[]
    for _ in range(NP): null.append(x[perm_within(d.agent.values,st,rng)==1].mean())
    null=np.array(null)
    print(f'{grp:6s} agents with this animal {obs*100:5.1f}%  chance {null.mean()*100:5.1f}%  ratio {obs/null.mean() if null.mean() else float("nan"):.2f} P_over {(1+(null>=obs-1e-9).sum())/(NP+1):.4f} P_under {(1+(null<=obs+1e-9).sum())/(NP+1):.4f}')
