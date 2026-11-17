"""Targeted follow-up from the slot scan: do short-horned-bull seals (animal with feeding trough) carry marked-fish signs (231,233,235,240) more than chance?
PREDICTION written before the number: yes, ratio > 1.5 (scan gave 235: 2.1x, 233 at name start 4.7x). Splits: Mohenjo-daro vs all other sites (the second half is out-of-sample for the first).
Null: animal labels shuffled inside site x shape x size tercile."""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from animal_common import *
rng=np.random.default_rng(1); NP=5000
d=b[(b.g!='')&(b.g!='NONE')].copy().reset_index(drop=True)
d['szb']=pd.qcut(d.face.fillna(d.face.median()),3,labels=False).astype(str)
FISH={'231','233','235','240'}
d['fish']=d.reading_order_text.map(lambda t:any(x in FISH for x in t.split('-')))
d['fish_name_first']=d['first'].isin(FISH)
for lab,sub in [('all sites',d),('Mohenjo-daro',d[d.site=='Mohenjo-daro']),('all other sites',d[d.site!='Mohenjo-daro'])]:
    sub=sub.reset_index(drop=True); st=strata_idx((sub.site2+'|'+sub['shape']+'|'+sub.szb).values)
    for grp in ['SHORT','ELEPH','WILD3','ZEBU','COMP','GOAT','UNI']:
        m=(sub.g==grp).values
        if m.sum()<8: continue
        x=sub.fish.values.astype(int); obs=x[m].mean(); gi=m.astype(int); null=[]
        for _ in range(NP): null.append(x[perm_within(gi,st,rng).astype(bool)].mean())
        null=np.array(null); po=(1+(null>=obs-1e-9).sum())/(NP+1); pu=(1+(null<=obs+1e-9).sum())/(NP+1)
        print(f'{lab:15s} {grp:6s} n={m.sum():4d} with marked fish {x[m].sum():3d} ({obs*100:4.1f}%) chance {null.mean()*100:4.1f}% ratio {obs/null.mean():.2f}  P_over {po:.4f}  P_under {pu:.4f}')
