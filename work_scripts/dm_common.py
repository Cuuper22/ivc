"""Shared loader for the diamond/measure job. Reading order = stored order reversed."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
import pandas as pd, collections, re, numpy as np
ROOT='/home/antigravity/Cuuper22/ivc'
DATA=f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv'
CNT={}
for i in range(1,8): CNT[f'{i:03d}']=('S',i)
CNT['012']=('T',2)
for i in range(13,19): CNT[f'{i:03d}']=('T',i-10)
for i in range(31,37): CNT[f'{i:03d}']=('F',i-30)
def lab(t):
    c=CNT.get(t)
    return None if not c else f'{c[0]}{c[1]}'
def load():
    d=pd.read_csv(DATA,dtype=str,keep_default_na=False)
    d['broken']=d.text.map(lambda t:('[' in t) or (']' in t))
    d['toks']=d.text.map(lambda t:[('ALT' if '/' in x else x) for x in t.strip('+[]').split('-')[::-1]])
    d['lost']=d.toks.map(lambda t:'000' in t or 'ALT' in t)
    d['area']=pd.to_numeric(d['horizontal(mm)'],errors='coerce')*pd.to_numeric(d['vertical(mm)'],errors='coerce')
    d['isseal']=d.type.str.startswith('SEAL')
    d['istab']=d.type.str.startswith('TAB')
    d['ispot']=d.type.str.startswith('POT')
    return d
