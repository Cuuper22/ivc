"""Shared loader and helpers for the animal job. Reading order = stored order reversed."""
import pandas as pd, numpy as np
ROOT='/home/claude/ivc'; OUT=f'{ROOT}/work_data/animal'
b=pd.read_csv(f'{OUT}/animal_base.csv',dtype=str,keep_default_na=False)
for c in ['depth_ft','face','seglen']: b[c]=pd.to_numeric(b[c],errors='coerce')
b['office']=b.office.eq('True'); b['has_jar']=b.has_jar.eq('True'); b['tight']=b.tight_nr.eq('True')
GRP={'UNICORN':'UNI','SHORTHORN':'SHORT','RHINO':'WILD3','TIGER':'WILD3','BUFFALO':'WILD3','ELEPHANT':'ELEPH','ZEBU':'ZEBU','GOAT':'GOAT','COMPOSITE':'COMP','NONE':'NONE'}
b['g']=b.animal.map(GRP).fillna('')          # '' = excluded (unknown / other / unspecified bull)
b['site2']=b.site.where(b.site.isin(['Mohenjo-daro','Harappa','Dholavira','Lothal','Chanhu-daro','Kalibangan']),'other')
def cramers(ct):
    from scipy.stats import chi2_contingency
    ct=ct.loc[ct.sum(1)>0, ct.sum(0)>0]
    if ct.shape[0]<2 or ct.shape[1]<2: return np.nan,np.nan
    chi=chi2_contingency(ct,correction=False)[0]; n=ct.values.sum()
    return chi, np.sqrt(chi/(n*(min(ct.shape)-1)))
def perm_within(labels,strata,rng):
    """shuffle labels inside each stratum"""
    out=labels.copy()
    for ix in strata:
        out[ix]=labels[rng.permutation(ix)]
    return out
def strata_idx(keys):
    d={}
    for i,k in enumerate(keys): d.setdefault(k,[]).append(i)
    return [np.array(v) for v in d.values() if len(v)>1]
