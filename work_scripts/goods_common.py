"""Shared loader for the goods job. Reading order = stored order reversed. One row per text face."""
import pandas as pd, numpy as np, re, collections
from scipy.stats import fisher_exact, hypergeom
ROOT='/home/claude/ivc'
DATA=f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv'
OUT=f'{ROOT}/work_scripts/goods_out'
CNT={}
for i in range(1,8): CNT[f'{i:03d}']=('S',i)
CNT['012']=('T',2)
for i in range(13,19): CNT[f'{i:03d}']=('T',i-10)
for i in range(31,37): CNT[f'{i:03d}']=('F',i-30)
for i in range(465,476): CNT[str(i)]=('A',0)
CARR={'151','153','154','155','156','158'}
def load():
    d=pd.read_csv(DATA,dtype=str,keep_default_na=False)
    d['toks']=[['ALT' if '/' in x else x for x in t.strip('+[]').split('-')[::-1]] for t in d.text]
    d['broken']=d.text.str.contains(r'\[|\]')
    ty=d.type
    d['cls']=np.select([ty.str.startswith('SEAL'),ty=='TAB:B',ty=='TAB:I',ty=='TAB:C',ty.str.startswith('POT'),ty.str.startswith('TAG'),ty=='IMPL',ty=='BNGL',ty=='ROD'],
                       ['seal','tabB','tabI','tabC','pot','tag','impl','bngl','rod'],'other')
    d['mat']=d.material.str.lower()
    d['gran']=(d.site=='Harappa')&(d['area-section'].isin(['FGranery','FGranary']))
    d['harF']=(d.site=='Harappa')&d['area-section'].str.startswith('F')
    d['E11']=(d.site=='Harappa')&d['area-section'].isin(['ETrench 11','ETrench 10W/11','ETrench 11W'])
    return d
def fe(a,b,c,dd):
    """a hit in group, b miss in group, c hit outside, dd miss outside: enrichment ratio and one-sided P (more than chance)"""
    n1=a+b; n2=c+dd
    base=(a+c)/(n1+n2) if n1+n2 else 0
    r=(a/n1)/base if n1 and base else np.nan
    p=fisher_exact([[a,b],[c,dd]],alternative='greater')[1] if n1 and n2 else np.nan
    return r,p
