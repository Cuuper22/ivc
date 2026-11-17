"""beads_5: sign 838 (leaf with branching stalk): sesame (eḷ, DEDR 854) or bone/ivory (eḷumpu, DEDR 839)?
PREDICTIONS written before the numbers:
 D1 If 838 is a contents label (sesame) it should sit in the commodity slot of tags/pots with counts, like fish 220; if it is a material label (bone) it should sit
    apart from the name. Prediction: 838 is inside the parsed NAME in >=70% of its faces (it is a name element) against <=35% for fish 220.
 D2 Rod enrichment (28x) shrinks a lot once identical copies are collapsed: distinct rod texts with 838 = 2 of N distinct rod texts; prediction: ratio <10x, P>0.001.
 D3 Identical rod text on bone and on ivory rods (bone rod bearing the same text as an ivory rod) => 838 cannot be the material label; prediction: >=1 such pair.
 D4 jar-dot 741 stands right before 838 (741-838) more than chance (>=3 faces, P<0.01): 'jar of 838' = a packaged good.
 D5 the other signs that sit in the 838 slot on rods (013-840 'three pairs', 482 'tusk-peak') behave as name elements, not material words: 838 and 013-840 share the slot after 240 on rods.
"""
from goods_common import *
d=load(); g=pd.read_csv('../work_data/gloss2_all.csv',dtype=str,keep_default_na=False)
g['key']=g.id; d=d.merge(g[['id','template','name_signs']],on='id',how='left')
h=d.toks.apply(lambda t:'838' in t)
def in_name(sign):
    x=d[d.toks.apply(lambda t:sign in t)]
    k=sum(1 for _,r in x.iterrows() if isinstance(r.name_signs,str) and sign in r.name_signs.split('-'))
    return k,len(x)
for s in ['838','220','806','390']: k,n=in_name(s); print('D1',s,'in parsed name',k,'of',n,'= %.0f%%'%(100*k/n))
rod=d[d.cls=='rod']; rd=rod.drop_duplicates(subset='text'); a=int(rd.toks.apply(lambda t:'838' in t).sum())
alld=d.drop_duplicates(subset='text'); b=int(alld.toks.apply(lambda t:'838' in t).sum())
r,p=fe(a,len(rd)-a,b-a,len(alld)-len(rd)-(b-a)); print('D2 distinct rod texts',len(rd),'with 838',a,' distinct texts with 838 overall',b,' ratio %.1f P %.3g'%(r,p))
x=rod[rod.toks.apply(lambda t:'838' in t)]
for tx,grp in x.groupby('text'): print('D3',tx,list(zip(grp.id,grp.mat)))
tx_mats=rod.groupby('text').mat.nunique(); print('D3 rod texts shared across >1 material:',int((tx_mats>1).sum()),'of',len(tx_mats))
pre=d.toks.apply(lambda t:any(x=='741' and y=='838' for x,y in zip(t,t[1:]))); a=int(pre.sum())
has741=d.toks.apply(lambda t:'741' in t); print('D4 741-838 faces',a,'  741 in %.1f%% of faces, 838 faces %d'%(100*has741.mean(),h.sum()))
# chance: among 838 faces, P(preceded by 741)
n838=0;pr=0
for t in d.toks:
    for i,u in enumerate(t):
        if u=='838':
            n838+=1; pr+= (i>0 and t[i-1]=='741')
from scipy.stats import binom
prev741=sum(1 for t in d.toks for i,u in enumerate(t) if i>0 and u=='741')/sum(len(t) for t in d.toks)
print('   838 occurrences',n838,' preceded by 741:',pr,' chance rate per slot %.3f  P(>=%d)=%.4f'%(prev741,pr,1-binom.cdf(pr-1,n838,prev741)))
# D5
for t in rod.toks:
    if '240' in t: print('D5 rod',t)
