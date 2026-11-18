"""Job: the travelled name 590-390. Step 1: list every text face that carries 590-390 (adjacent, reading order) with full metadata.
Reading order = stored order reversed (work_data/gloss2_all.csv is already in reading order). Output: travelled_out/t590_390.csv and a printout."""
import pandas as pd, os
R='/home/antigravity/Cuuper22/ivc/'
G=pd.read_csv(R+'work_data/gloss2_all.csv',dtype=str)
M=pd.read_csv(R+'research/data/open_prototype/lipi/metadata_filtered.csv',dtype=str)
D=G.merge(M[['id','region','area-section','block-house','room-grid','excavation-idno','time','period','phase','depth','material','shape','symbol','cult','sides','complete','class','horizontal(mm)','vertical(mm)','thickness(mm)','text']],on='id',how='left')
D['toks']=D.reading_order_text.str.split('-')
def has(t,pat):
    n=len(pat); return any(t[i:i+n]==pat for i in range(len(t)-n+1))
def pos(t,pat):
    n=len(pat)
    for i in range(len(t)-n+1):
        if t[i:i+n]==pat: return i
X=D[D.toks.map(lambda t:has(t,['590','390']))].copy()
def f(x):
    try: return float(x)
    except: return None
X['face_mm2']=[ (f(a) or 0)*(f(b) or 0) or None for a,b in zip(X['horizontal(mm)'],X['vertical(mm)'])]
X['before']=X.toks.map(lambda t:'-'.join(t[:pos(t,['590','390'])]))
X['after']=X.toks.map(lambda t:'-'.join(t[pos(t,['590','390'])+2:]))
os.makedirs(R+'work_scripts/travelled_out',exist_ok=True)
X.drop(columns=['toks']).to_csv(R+'work_scripts/travelled_out/t590_390.csv',index=False)
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',60)
print(len(X),'faces',X.object.nunique(),'objects')
print(X[['id','cisi','site','type','symbol','period','phase','area-section','block-house','room-grid','depth','excavation-idno','face_mm2','reading_order_text']].to_string())
