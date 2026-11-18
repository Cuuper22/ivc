"""Builds work_data/animal/animal_base.csv : one row per seal face with its animal, its stand, and the template pieces.
Reading order = stored order reversed. Animal coarse classes come from the catalogue `symbol` column (checked on photos, see animal_photocheck.md in jobs/out).
Template pieces: name_rows.csv (tight parse) + masters census (jar and the sign after it)."""
import pandas as pd, numpy as np, re, sys
sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
ROOT='/home/antigravity/Cuuper22/ivc'
M=pd.read_csv(f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv',dtype=str,keep_default_na=False)
G=pd.read_csv(f'{ROOT}/work_data/gloss2_all.csv',dtype=str,keep_default_na=False)
N=pd.read_csv(f'{ROOT}/work_data/name_rows.csv',dtype=str,keep_default_na=False)
C=pd.read_csv(f'{ROOT}/work_data/masters/census.csv',dtype=str,keep_default_na=False)
s=M[M.type.str.startswith('SEAL')].copy()
s=s.merge(G[['id','reading_order_text','tight','ending_kind']],on='id',how='left')
def coarse(sym):
    b=sym.split(':')[0]
    if b=='Bull1': return 'UNICORN'
    if b=='Gaur': return 'SHORTHORN'     # short-horned bull, head low, trough in front
    if b=='Zebu': return 'ZEBU'
    if b in('Bull','Bull2'): return 'BULL_OTHER'
    if b in('Elep',): return 'ELEPHANT'
    if b=='Rhin': return 'RHINO'
    if b=='Tigr': return 'TIGER'
    if b=='Buff': return 'BUFFALO'
    if b.startswith('Goat') or b=='Bull3': return 'GOAT'
    if b in('Comp','CompBull','Mult','T-A-T','T-M-T','Phyt','Htgr'): return 'COMPOSITE'
    if b in('Scene','Othr','Anth','Gavi','Hare','Bird','Ass','Cros','Bult','Unknown','Misc','MISC','?'): return 'OTHER'
    if b=='None': return 'NONE'
    return 'UNKNOWN'    # '-' : catalogue left it blank
s['animal']=s.symbol.map(coarse)
s['stand_sfx']=[x.split(':')[1] if x.startswith('Bull1:') else '' for x in s.symbol]
def cultclass(c,a):
    if c in('Trough',): return 'trough'
    if c.startswith('S'): return 'standard'
    if c.startswith('R') or c.startswith('H'): return 'rack_or_other'
    return 'none_or_blank'
s['stand']=[cultclass(c,a) for c,a in zip(s.cult,s.animal)]
def depth(x):
    m=re.search(r'(-?\d+(\.\d+)?)\s*(ft|cm)',x)
    if not m: return np.nan
    v=float(m.group(1)); return abs(v) if m.group(3)=='ft' else abs(v)/30.48
s['depth_ft']=s.depth.map(depth)
s['face']=pd.to_numeric(s['horizontal(mm)'],errors='coerce')*pd.to_numeric(s['vertical(mm)'],errors='coerce')
s['obj']=s.id.str.split('.').str[0]
# template pieces
nr=N[['id','tight','name','first','last','cls_last','opener','house','seg','seglen','has_class']].rename(columns={'tight':'tight_nr','opener':'opener_nr'})
s=s.merge(nr,on='id',how='left')
cc=C[['id','X','opener','noun','after']].rename(columns={'X':'X_c','opener':'opener_c','noun':'noun_c','after':'after_c'})
s=s.merge(cc,on='id',how='left')
s['toks']=s.reading_order_text.fillna('').str.split('-')
s['has_jar']=s.toks.map(lambda t:'740' in t)
s['ending']=np.select([s.noun_c.eq('090'),s.noun_c.eq('400'),s.noun_c.eq('679'),s.noun_c.eq('621'),s.X_c.notna()&s.noun_c.eq('none'),s.cls_last.eq('520'),s.cls_last.isin(['151','153','154','155','156','158']),s.cls_last.eq('400'),s.cls_last.eq('090')],
  ['jar+man','jar+comb','jar+679','jar+621','jar','spear','porter','comb','man'],'')
s['crest']=s['first'].where(s['first'].isin(['231','233','235','240','226','222']),'')
s['office']=s.reading_order_text.fillna('').str.startswith('920-060-741')
s['opener_type']=np.select([s.opener_c.eq('diamond')|s.opener_nr.isin(['861','817']),s.opener_c.eq('wheel')|s.opener_nr.str.startswith('820'),s.opener_nr.str.contains('060')|s.opener_c.eq('060-920')],['diamond','wheel','060'],'none')
s['room_key']=np.where(s['block-house'].isin(['--','-','']) | s['room-grid'].isin(['--','-','']),'',s.site+'|'+s['area-section']+'|'+s['block-house']+'|'+s['room-grid'])
cols=['id','obj','cisi','site','region','area-section','block-house','room-grid','room_key','depth_ft','period','face','shape','material','symbol','animal','stand_sfx','stand','cult','type','reading_order_text','tight','tight_nr','name','first','last','crest','cls_last','house','seglen','ending','opener_type','office','X_c','noun_c','has_jar']
s[cols].to_csv(f'{ROOT}/work_data/animal/animal_base.csv',index=False)
print(len(s),'seal faces'); print(s.animal.value_counts().to_dict()); print('tight parse',s.tight_nr.eq('True').sum(),'; with ending',s.ending.ne('').sum(),'; room',s.room_key.ne('').sum(),'; office',s.office.sum())
print(s.groupby('animal').agg(n=('id','size'),tight=('tight_nr',lambda x:(x=='True').sum()),jar=('has_jar','sum')))
