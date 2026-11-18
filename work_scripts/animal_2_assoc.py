"""What does the animal go with? Cramer V of animal group against each text/object feature, null = animal labels shuffled inside the same site.
PREDICTIONS written before the numbers (committed reading: animal = clan/lineage emblem, a second family-level mark beside the fish crest):
 P1 crest-or-first-sign: animal goes with the first name sign (clan reading) -> p<0.01 beyond site.
 P2 ending class (jar/spear/carrier/comb): animal does NOT go with it (ending belongs to the person) -> p>0.05.
 P3 seal size: animal goes with face size within site only weakly (V small), rank reading mostly wrong.
 P4 area inside Mohenjo-daro: animal goes with area (ward) -> p<0.05.
 P5 opener type (diamond/wheel/060): animal goes with it (opener = kind of owner) -> p<0.05.
 P6 office opening 920-060-741 : animal mix differs from site baseline.
 P7 material, shape: control; expected to go with animal through seal type only.
"""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from animal_common import *
from scipy.stats import chi2_contingency
rng=np.random.default_rng(7); NP=3000
MODE=sys.argv[1] if len(sys.argv)>1 else 'ANIM'   # ANIM = real animals only (square/round seals with a beast); ALL adds the no-animal seals
d=b[(b.g!='')&((b.g!='NONE')|(MODE=='ALL'))&(b.type.isin(['SEAL:S','SEAL:C','SEAL','SEAL:R','SEAL:CY','SEAL:L'])|(MODE=='ALL'))].copy()
if MODE=='STAND':      # label = unicorn stand-type letter (W, J, S, I, L, rest); unicorn seals only
    d=b[(b.g=='UNI')&(b.stand_sfx!='')].copy(); d['g']=d.stand_sfx.where(d.stand_sfx.isin(['W','J','S','I','L']),'rest')
def top(s,k):
    v=s[s!=''].value_counts().head(k).index; return s.where(s.isin(v),'~other').where(s!='','')
d['first_t']=top(d['first'],10); d['last_t']=top(d['last'],10); d['cls_t']=top(d.cls_last,8)
d['end_t']=d.ending
d['crest_bin']=np.where(d.crest!='','marked-fish',np.where(d['first']!='','other',''))
d['office_b']=np.where(d.office,'office','no')
d['size_bin']=''
for s_,ix in d.groupby('site2').groups.items():
    f=d.loc[ix,'face'].dropna(); 
    if len(f)>=30:
        q=f.quantile([1/3,2/3]).values
        d.loc[f.index,'size_bin']=np.where(f<=q[0],'small',np.where(f<=q[1],'mid','large'))
d['depth_bin']=np.where(d.depth_ft.isna(),'',np.where(d.depth_ft<5,'0-5ft',np.where(d.depth_ft<10,'5-10ft','10+ft')))
d['area_t']=''
md=d.site=='Mohenjo-daro'; a=d['area-section']; keep=a[md&(a!='--')].value_counts(); keep=keep[keep>=25].index
d.loc[md&a.isin(keep),'area_t']=a
d['mat_t']=top(d.material,5); d['shape_t']=top(d['shape'],5)
d['len_bin']=np.where(d.reading_order_text.str.count('-')<2,'1-3',np.where(d.reading_order_text.str.count('-')<4,'4-5','6+'))
feats=[('P1 first name sign','first_t',True),('P1b marked-fish crest or not','crest_bin',True),('P1c last name sign','last_t',True),('P2 ending class sign','cls_t',True),('P2b ending form','end_t',False),
 ('P3 seal size within site','size_bin',False),('P4 area (Mohenjo-daro only)','area_t',False),('P4b depth band','depth_bin',False),('P5 opener type','opener_type',False),('P6 office opening','office_b',False),('P7 material','mat_t',False),('P7 shape','shape_t',False),('text length','len_bin',False)]
rows=[]
for name,col,tightonly in feats:
    x=d[(d[col]!='')&((d.tight)|(not tightonly))&(d.g!='')]
    if col=='area_t': x=x[x.site=='Mohenjo-daro']
    if col=='ending' or col=='end_t': x=x[x.end_t!='']
    ct=pd.crosstab(x.g,x[col]); chi,V=cramers(ct)
    lab=x.g.values.copy(); st=strata_idx((x.site2+'|'+x['shape']).values); cols=pd.Index(sorted(x[col].unique())); ci=np.searchsorted(cols,x[col].values); gi=pd.Categorical(x.g).codes
    ng=gi.max()+1; nc=len(cols)
    null=[]
    for _ in range(NP):
        p=perm_within(gi,st,rng); m=np.zeros((ng,nc)); np.add.at(m,(p,ci),1)
        m=m[m.sum(1)>0][:,m.sum(0)>0]
        e=np.outer(m.sum(1),m.sum(0))/m.sum(); null.append(((m-e)**2/e).sum())
    null=np.array(null); P=(1+(null>=chi-1e-9).sum())/(NP+1)
    rows.append(dict(test=name,n=len(x),V=round(V,3),chi=round(chi,1),null_mean=round(null.mean(),1),P_within_site=round(P,4)))
    print(rows[-1])
pd.DataFrame(rows).to_csv(f'{OUT}/assoc_{MODE}.csv',index=False)
