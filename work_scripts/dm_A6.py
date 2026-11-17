"""A6: do opener seals have shorter bodies / fewer name signs / different class than non-opener seals?"""
import warnings; warnings.filterwarnings('ignore')
from dm_common import *
from scipy import stats
s=pd.read_pickle('/tmp/seals_dm.pkl')
g=pd.read_csv(f'{ROOT}/work_data/gloss_all.csv',dtype=str,keep_default_na=False)
s=s.merge(g[['id','role_string']],on='id',how='left')
s['nwho']=s.role_string.map(lambda r:r.split().count('who') if isinstance(r,str) else np.nan)
s['nhouse']=s.role_string.map(lambda r:r.split().count('house') if isinstance(r,str) else np.nan)
s['body']=s.toks.map(len)
s['openlen']=s.grp.map(lambda x:2 if x.startswith(('D2','W2','W1')) else (2 if x.startswith('CAP') else 0))
s['bodylen']=s.body-s.openlen
print(s.groupby('grp').agg(n=('id','count'),len=('body','mean'),bodylen=('bodylen','mean'),who=('nwho','mean'),house=('nhouse','mean')).round(2))
for a in ['D2 (861+2)','D2b (817+2)','W2 (820+2)','CAP (060-920)']:
    x=s[s.grp==a].bodylen;y=s[s.grp=='rest'].body
    print(a,'bodylen vs rest len MWU p %.2g'%stats.mannwhitneyu(x,y).pvalue)
# text-length distribution
print(pd.crosstab(s.grp,s.body.clip(upper=9),normalize='index').round(2))
# opener roles distribution for the sign after opener+2 (what is the first body role)
def firstrole(r,k):
    p=r.split() if isinstance(r,str) else []
    return p[k] if len(p)>k else None
for a in ['D2 (861+2)','D2b (817+2)','W2 (820+2)','CAP (060-920)','rest']:
    x=s[s.grp==a]
    print(a,collections.Counter(firstrole(r,2 if a!='rest' else 0) for r in x.role_string).most_common(5))
# does the rest-of-seal share any 2-sign opening with openers? i.e. do non-opener seals start with 002 or 003 counts?
print('rest starts with count',np.mean([t[0] in CNT for t in s[s.grp=='rest'].toks]))
