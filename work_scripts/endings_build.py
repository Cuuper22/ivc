#!/usr/bin/env python3
"""Build the ending table: one row per text face with its ending (jar / spear / porter / comb / none), name, object, findspot.
Reading order = stored order reversed. Output work_data/endings/faces.csv"""
import pandas as pd, numpy as np, re
R='/home/antigravity/Cuuper22/ivc'
m=pd.read_csv(f'{R}/research/data/open_prototype/lipi/metadata_filtered.csv',dtype=str)
g=pd.read_csv(f'{R}/work_data/gloss2_all.csv',dtype=str)
g=g[['id','reading_order_text','template','name_signs','ending_kind','relation_sign','tight']]
d=m.merge(g,on='id',how='inner')
d['toks']=d.reading_order_text.fillna('').str.split('-')
PORT={'151','154','155','156','158'}
def ending(t,k,rel):
    if '740' in t:
        i=max(j for j,s in enumerate(t) if s=='740')
        after=t[i+1:]
        return 'jar', (after[0] if after else '')
    if t and t[-1]=='520': return 'spear',''
    if t and t[-1] in PORT: return 'porter',t[-1]
    if t and t[-1]=='400': return 'comb',''
    return 'none',''
r=[ending(t,k,x) for t,k,x in zip(d.toks,d.ending_kind,d.relation_sign)]
d['end']=[a for a,b in r]; d['endsub']=[b for a,b in r]
d['jarman']=(d.end=='jar')&(d.endsub=='090')
d['name']=d.name_signs.fillna('')
def f(x):
    try: return float(x)
    except: return np.nan
d['h']=d['h'].map(f) if 'h' in d else np.nan
d['hmm']=d['horizontal(mm)'].map(f); d['vmm']=d['vertical(mm)'].map(f)
d['face']=d.hmm*d.vmm
d.loc[(d.hmm<=0)|(d.vmm<=0),'face']=np.nan
d['obj']=d.id.str.split('.').str[0]
d['isseal']=d.type.isin(['SEAL:S','SEAL:R','SEAL'])
d['nlen']=d.name.map(lambda s: len(s.split('-')) if s else 0)
d['crest']=[s.split('-')[0] if s and '-' in s else '' for s in d.name]
d['house']=np.where((d.site=='Mohenjo-daro')&(d['block-house']!='--'),d['area-section']+'|'+d['block-house'],'')
d.to_csv(f'{R}/work_data/endings/faces.csv',index=False)
print(len(d)); print(d.groupby(['isseal','end']).size())
print(d[d.isseal].groupby('end').face.median())
print(d[d.isseal&(d.end=='jar')].endsub.value_counts().head(8))
