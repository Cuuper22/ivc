"""Shared loader for the counted-things job. Reading order = stored order reversed."""
import pandas as pd, re, collections
ROOT='/home/antigravity/Cuuper22/ivc'
DATA=f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv'
SHAPES=f'{ROOT}/work_data/sign_shapes.csv'
# count signs -> (series, value)
CNT={}
for i in range(1,8): CNT[f'{i:03d}']=('S',i)            # short strokes 1-7
CNT['012']=('T',2)
for i in range(13,19): CNT[f'{i:03d}']=('T',i-10)           # stacked short strokes 013-018 (013=3 ... 018=8)
for i in range(31,37): CNT[f'{i:03d}']=('F',i-30)        # full-height strokes 1-6
for i in range(465,476): CNT[str(i)]=('A',0)             # A with comb of ticks (value = tick count, not coded)
CARR={'151','153','154','155','156','158'}
def shapes():
    s=pd.read_csv(SHAPES,dtype=str); return dict(zip(s.lipi_wells_number,s.shape_description))
def load():
    d=pd.read_csv(DATA,dtype=str,keep_default_na=False)
    rows=[]
    for _,r in d.iterrows():
        t=r['text']; broken=('[' in t or ']' in t)
        toks=t.strip('+[]').split('-')[::-1]
        toks=['ALT' if '/' in x else x for x in toks]
        rows.append((r,toks,broken))
    return rows
def cl(tok):
    return CNT.get(tok)
def label(tok):
    c=CNT.get(tok)
    if not c: return None
    return {'S':f'S{c[1]}','T':f'T{c[1]}','F':f'F{c[1]}','A':'A'}[c[0]]
