"""Does the Umma sealing's frame 705 + count + 390 repeat at home on goods-type objects?
Prediction first: 705 (ship / measure) followed within 4 signs by a count then tree-family 390 is enriched on tags/tablets/sealings against seals.
Reading order = stored reversed."""
import sys
sys.path.insert(0,'/home/claude/ivc/work_scripts')
from cotton_common import *
d=faces()
rows=[]
for _,r in d.iterrows():
    t=r.toks
    for i,x in enumerate(t):
        if x=='705':
            win=t[i+1:i+5]
            found=[s for s in win if s in('390','405','407','392')]
            rows.append((r.id,r.site,r.type,r.cls,' '.join(t),bool(found),found[:1]))
x=pd.DataFrame(rows,columns=['id','site','type','cls','text','tree_within4','tree'])
print('705 places',len(x),'with tree within next 4 signs',x.tree_within4.sum())
print(x[x.tree_within4].drop_duplicates('text').to_string())
base=sum(1 for t in d.toks for s in t if s in('390','405','407','392'))/sum(len(t) for t in d.toks)
print('tree-family share of all signs',round(base,4),'; expected within next 4 signs ~',round(4*base,3),'-> expected hits',round(len(x)*4*base,1))
print(x.groupby('cls').tree_within4.agg(['sum','count']))
