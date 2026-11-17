"""Goods job step 4: which signs ride with the cup measure (grain rations) and with the granary area? writes goods_out/cup_gran.csv"""
from goods_common import *
d=load(); d['obj']=d.cisi.where(~d.cisi.isin(['-','']),d.id)
g=d.groupby('obj')
objsigs=g.toks.apply(lambda L:set(x for t in L for x in t))
objgran=g.gran.any(); objE11=g.E11.any()
cup=objsigs.apply(lambda s:'700' in s)
rows=[]
allsigs=collections.Counter(x for s in objsigs for x in s)
for s,n in allsigs.items():
    if n<8 or s in CNT or s in('000','ALT','700'): continue
    h=objsigs.apply(lambda q:s in q)
    a=int((h&cup).sum());r,p=fe(a,int((h&~cup).sum()),int((~h&cup).sum()),int((~h&~cup).sum()))
    ag=int((h&objgran).sum());rg,pg=fe(ag,int((h&~objgran).sum()),int((~h&objgran).sum()),int((~h&~objgran).sum()))
    rows.append((s,n,a,round(r,2),p,ag,round(rg,2),pg))
R=pd.DataFrame(rows,columns=['sign','objs','with_cup','cup_x','cup_p','granary','gran_x','gran_p'])
R.to_csv(f'{OUT}/cup_gran.csv',index=False)
print(R.sort_values('cup_p').head(16).to_string(index=False)); print(R.sort_values('gran_p').head(12).to_string(index=False))
print('objects',len(objsigs),'cup objects',int(cup.sum()))
