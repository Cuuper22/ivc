"""Shared loader for the masters job. Reading order = stored order reversed (gloss2 file already in reading order)."""
import pandas as pd, re
G=pd.read_csv('/home/claude/ivc/work_data/gloss2_all.csv',dtype=str)
M=pd.read_csv('/home/claude/ivc/research/data/open_prototype/lipi/metadata_filtered.csv',dtype=str)
D=G.merge(M[['id','region','area-section','block-house','room-grid','period','symbol','material','class','horizontal(mm)','vertical(mm)','depth','excavation-idno','shape']],on='id',how='left')
def num(x):
    try: return float(x)
    except: return None
D['face']=[ (num(a) or 0)*(num(b) or 0) for a,b in zip(D['horizontal(mm)'],D['vertical(mm)'])]
D['toks']=D.reading_order_text.str.split('-')
OPENERS={'861','817','820','091'}
def split_open(t):
    """strip opener from token list; returns (opener_str, rest)"""
    i=0
    if t[:2]==['060','920'] or t[:1]==['060']:
        i=1
        if len(t)>1 and t[1]=='920': i=2
        # 060-920 is cap; some texts 920-060
    elif t[:1]==['920'] and len(t)>1 and t[1]=='060': i=2
    elif t and t[0] in OPENERS:
        i=1
        while i<len(t) and t[i] in ('001','002','003') : i+=1
    return '-'.join(t[:i]), t[i:]
def opener_type(o):
    if not o: return 'none'
    s=o.split('-')[0]
    if s in('861','817'): return 'diamond'
    if s=='820': return 'wheel'
    if s in ('060','920'): return '060-920'
    if s=='091': return 'twin'
    return 'other'
