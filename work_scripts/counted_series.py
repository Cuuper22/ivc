"""Two counting systems test + count-value distribution shapes per counted thing."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from counted_common import *
from scipy.stats import chi2_contingency, fisher_exact
import numpy as np
d=pd.read_csv(f'{ROOT}/work_data/counted/instances_resolved.csv',dtype=str,keep_default_na=False)
d['t']=d['type'].str.split(':').str[0]
d['value']=d.value.astype(int)
B=d[d.frame=='B'].drop_duplicates(['id','sign','cs'])
B=B[B.series.isin(['S','F','T'])]
def ct(X):
    c=pd.crosstab(X.sign,X.series).reindex(columns=['S','T','F'],fill_value=0)
    c['n']=c['S']+c['T']+c['F']; c['F_frac']=(c['F']/c['n']).round(2); return c
print('ALL objects: type x series'); print(pd.crosstab(B.t,B.series))
for tt in['SEAL','TAB']:
    X=B[B.t==tt]; c=ct(X); c=c[c.n>=12].sort_values('F_frac')
    print('\n',tt,'sign x series (n>=12)'); print(c.to_string())
    # test heterogeneity of F share among signs
    cc=c[['S','T','F']].copy(); cc['SF']=cc['S']+cc['T']
    chi=chi2_contingency(cc[['SF','F']].values); print('chi2 signs differ in F-share within',tt,'chi2=%.1f dof=%d p=%.2g'%(chi[0],chi[2],chi[1]))
# value shape per sign: pooled series-specific distributions
print('\nvalue distributions: sign, series, counts by value 1..8, n, modal share, top2 share')
for s in B.sign.value_counts()[lambda x:x>=15].index:
    X=B[B.sign==s]
    for ser in['S','F','T']:
        Y=X[X.series==ser]
        if len(Y)>=10:
            v=Y.value.value_counts().reindex(range(1,9),fill_value=0)
            print(s,ser,list(v.values),len(Y),round(v.max()/len(Y),2))
