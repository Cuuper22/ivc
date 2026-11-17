"""Part 3: every TAG row: parse, kind of seal that made it, subtype, site. Output work_data/masters/tags.csv"""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from masters_common import *
from collections import Counter
T=D[D.type.str.startswith('TAG')].copy()
def kind(t):
    toks=t.split('-')
    if toks==['000'] or all(x=='000' for x in toks): return 'blank'
    j=toks.index('740') if '740' in toks else None
    if j is not None:
        nxt=toks[j+1] if j+1<len(toks) else ''
        pre=[x for x in toks[:j] if x!='000']
        if nxt=='090': return 'agent (X jar man)'
        if nxt=='400': return 'agent-comb (X jar comb)'
        if nxt in('679','621','565'): return 'agent-other (X jar %s)'%nxt
        if nxt=='': return 'owner (X jar)' if pre else 'jar only (name lost)'
        return 'jar + other (%s)'%nxt
    last=toks[-1]
    if last=='520': return 'spearman (X spear)'
    if last in('151','154','156','158'): return 'carrier (X porter)'
    if last=='400': return 'comb (X comb)'
    if last in('090',): return 'man (X man)'
    return 'name/other, no ending'
T['kind']=T.reading_order_text.map(kind)
T=T.merge(M[['id','material','shape','symbol','area-section']],on='id',suffixes=('','_m'))
T.to_csv('/home/claude/ivc/work_data/masters/tags.csv',index=False)
print(len(T),'tag rows,',T.object.nunique(),'objects')
print(T.kind.value_counts().to_string())
print(pd.crosstab(T.kind,T.type).to_string())
print(pd.crosstab(T.site,T.kind).to_string())
vc=T.reading_order_text.value_counts(); print(vc.head(25).to_string())
print('distinct texts',T.reading_order_text.nunique())
for s in ['Lothal','Dholavira','Kalibangan']:
    print('==',s); print(T[T.site==s].reading_order_text.value_counts().head(14).to_string())
