"""Part 3: match each tag text to seals carrying the same text; which names stamp goods."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from masters_common import *
from collections import Counter
T=pd.read_csv('/home/antigravity/Cuuper22/ivc/work_data/masters/tags.csv',dtype=str,keep_default_na=False)
def informative(t): return [x for x in t.split('-') if x!='000']
rows=[]
for tx,g in T.groupby('reading_order_text'):
    toks=tx.split('-')
    inf=informative(tx)
    if len(inf)<2 or tx.count('000')>0: 
        continue
    # exact seal matches (any non-tag object with the same text)
    m=D[(D.reading_order_text==tx)&~D.type.str.startswith('TAG')]
    # X-level: strip opener, and trailing jar+noun
    op,rest=split_open(toks)
    # seals whose text contains rest as a run
    key=rest[:rest.index('740')] if '740' in rest else rest
    def has(t):
        n=len(key); return n>0 and any(t[i:i+n]==key for i in range(len(t)-n+1))
    m2=D[pd.Series([has(t) for t in D.toks],index=D.index)&~D.type.str.startswith('TAG')] if len(key)>=2 else D.iloc[0:0]
    rows.append(dict(text=tx,tags=len(g),sites=','.join(sorted(set(g.site))),subtype=','.join(f'{k}:{v}' for k,v in Counter(g.type).items()),exact_nontag=len(m),exact_where=','.join(sorted(set(m.cisi))[:5]),run_nontag=len(m2),run_types=dict(Counter(m2.type.map(lambda t:t.split(':')[0]))),run_sites=dict(Counter(m2.site).most_common(4))))
R=pd.DataFrame(rows).sort_values('tags',ascending=False)
R.to_csv('/home/antigravity/Cuuper22/ivc/work_data/masters/tag_matches.csv',index=False)
pd.set_option('display.width',260,'display.max_colwidth',60,'display.max_rows',100)
print(R.head(45).to_string(index=False))
print('tag texts with >=2 informative signs and no lost sign:',len(R),'; with an exact non-tag twin:',(R.exact_nontag>0).sum(),'; with a run twin:',(R.run_nontag>0).sum())
