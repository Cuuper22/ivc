"""beads_1: signs and sign pairs concentrated at bead-making towns and workshop areas.
PREDICTIONS (written before any number):
 P1 A bead sign is enriched (ratio>=2, one-sided Fisher P<0.01) at BOTH Chanhu-daro and Lothal, counting faces that hold it anywhere in the text. Expect 1 to 3 signs; the diamond 817 is not new.
 P2 In Harappa Mound E/ET trenches (faience, shell, bead dumps) some sign is enriched >=2x with P<0.01 against the rest of Harappa; expect a different sign from P1 if workshops differ.
 P3 Sign pairs (bigrams) enriched at the bead towns give a noun+count or noun+noun phrase not found at inland sites.
Unit: text faces from goods_common.load(); presence of sign in a face counts once."""
from goods_common import *
d=load()
d['set']=d.toks.apply(set)
def pairs(t): return {a+'_'+b for a,b in zip(t,t[1:])}
d['pset']=d.toks.apply(pairs)
def enrich(mask, label, col='set', minn=4):
    inn=d[mask]; out=d[~mask]
    cn=collections.Counter(s for x in inn[col] for s in x); co=collections.Counter(s for x in out[col] for s in x)
    rows=[]
    for s,a in cn.items():
        if a<minn: continue
        c=co.get(s,0); r,p=fe(a,len(inn)-a,c,len(out)-c); rows.append((s,a,c,len(inn),r,p))
    return pd.DataFrame(rows,columns=['sign','in','out','n_in','ratio','p']).sort_values('p')
res={}
for name,m in [('Chanhu',d.site=='Chanhu-daro'),('Lothal',d.site=='Lothal'),('Dholavira',d.site=='Dholavira'),
               ('HarE',(d.site=='Harappa')&d['area-section'].str.startswith('E')),
               ('HarEoutsideHarappa',None)]:
    if m is None: continue
    res[name]=enrich(m,name)
    print(name,'faces',m.sum()); print(res[name].head(12).to_string(index=False))
# P1
a=res['Chanhu'].set_index('sign'); b=res['Lothal'].set_index('sign')
both=a.join(b,lsuffix='_C',rsuffix='_L',how='inner')
both['pc']=both.p_C*both.p_L
print('P1 both-town signs'); print(both.sort_values('pc').head(12)[['in_C','ratio_C','p_C','in_L','ratio_L','p_L','pc']])
# pairs at the two towns together
m=d.site.isin(['Chanhu-daro','Lothal'])
pr=enrich(m,'CL',col='pset',minn=3); print('P3 pairs at Chanhu+Lothal'); print(pr.head(15).to_string(index=False))
for k,v in res.items(): v.to_csv(f'beads_out/site_{k}.csv',index=False)
pr.to_csv('beads_out/pairs_CL.csv',index=False)
