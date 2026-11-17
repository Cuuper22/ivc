"""Goods job step 5: what each object type is labelled with. Reads every inscription on tools, bangles, rods and pots with the
possessive-model parser output (work_data/gloss2_all.csv). Writes goods_out/object_kinds.txt and goods_out/object_reads.csv"""
from goods_common import *
g=pd.read_csv(f'{ROOT}/work_data/gloss2_all.csv',dtype=str,keep_default_na=False)
d=load(); d=d.merge(g[['id','template','ending_kind','relation_sign','gloss','name_signs']],on='id',how='left')
d['n']=d.toks.apply(len)
def kind(r):
    t=r.toks; s=[x for x in t if x!='000']
    if not s: return 'lost'
    if all(x in CNT for x in s): return 'count only'
    if len(s)==1: return 'one sign'
    cnt=any(x in CNT for x in s)
    if '740' in s and s.index('740')>0 and r.ending_kind in('poss',) : 
        return 'name+jar (owner)' if not cnt else 'name+jar+count'
    if r.ending_kind=='ending': return 'name+ending'
    if cnt: return 'thing+count'
    return 'other signs'
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
d['kind']=d.apply(kind,axis=1)
rows=[]
for cls in ['impl','bngl','rod','pot','tag']:
    x=d[d.cls==cls]; P(f'\n## {cls}  faces {len(x)}  objects {x.cisi.nunique()}  broken {int(x.broken.sum())}')
    P(x.kind.value_counts().to_dict())
    P('with jar 740:',int(x.toks.apply(lambda t:'740' in t).sum()),' ends in jar:',int(x.toks.apply(lambda t:t[-1:]==['740']).sum()),' ends in comb 400:',int(x.toks.apply(lambda t:t[-1:]==['400']).sum()),' has count sign:',int(x.toks.apply(lambda t:any(a in CNT for a in t)).sum()))
    P('mean signs',round(x.n.mean(),2),'median',x.n.median())
    P('top signs:',collections.Counter(a for t in x.toks for a in t if a not in('000',)).most_common(14))
    P('sites:',x.site.value_counts().head(6).to_dict(),' material:',x.mat.value_counts().head(4).to_dict())
base=d[d.cls=='seal']; P('\nseals for comparison: with jar',round(base.toks.apply(lambda t:'740' in t).mean(),3),'ends in jar',round(base.toks.apply(lambda t:t[-1:]==['740']).mean(),3),'has count',round(base.toks.apply(lambda t:any(a in CNT for a in t)).mean(),3),'mean signs',round(base.n.mean(),2))
# pot detail
pt=d[d.cls=='pot']
P('\nPOT single-count pots by series:',collections.Counter(('F' if CNT[t[0]][0]=='F' else CNT[t[0]][0]) for t in pt.toks if len(t)==1 and t[0] in CNT))
P('POT whole-text single non-count signs:',collections.Counter(t[0] for t in pt.toks if len(t)==1 and t[0] not in CNT and t[0]!='000').most_common(14))
P('POT texts with a name-and-jar:',int(pt.kind.isin(['name+jar (owner)','name+jar+count']).sum()),'of',len(pt))
P('POT sites:',pt.groupby('site').size().sort_values(ascending=False).head(8).to_dict())
P('POT type g/s/p:',pt.type.value_counts().to_dict())
for ty in ['POT:T:g','POT:T:s','POT:T:p']:
    z=pt[pt.type==ty]; P(ty,len(z),'count-only',int((z.kind=='count only').sum()),'owner(name+jar)',int(z.kind.isin(['name+jar (owner)','name+jar+count']).sum()),'one sign',int((z.kind=='one sign').sum()))
d[d.cls.isin(['impl','bngl','rod','pot'])][['id','cisi','cls','type','site','material','symbol','area-section','text','kind','gloss']].to_csv(f'{OUT}/object_reads.csv',index=False)
open(f'{OUT}/object_kinds.txt','w').write('\n'.join(out))
