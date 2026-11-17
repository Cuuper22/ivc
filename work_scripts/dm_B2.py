"""B2: counts on pots vs on tablet cups vs jars; bands; the 6-cup objects; count-value spectrum vs binary/decimal series."""
import warnings; warnings.filterwarnings('ignore')
from dm_common import *
from scipy import stats
d=load()
pot=d[d.ispot]
# every count token on pots, with owner = neighbour sign
c=collections.Counter(); ex=collections.defaultdict(list)
for r in pot.itertuples():
    for i,x in enumerate(r.toks):
        if x in CNT:
            c[lab(x)]+=1
print('all count tokens on pots',sum(c.values()),dict(sorted(c.items())))
# whole-pot text is a single count
single=[r for r in pot.itertuples() if len(r.toks)==1 and r.toks[0] in CNT and not r.broken]
cc=collections.Counter(lab(r.toks[0]) for r in single); print('single-count pots',len(single),dict(sorted(cc.items())))
tall=[v for k,v in cc.items() if k.startswith('F')]
print('single tall-count pots in 1-4: %d of %d; F5+ : %d'%(sum(cc[k] for k in['F1','F2','F3','F4']),sum(tall),sum(cc[k] for k in cc if k.startswith('F') and int(k[1])>=5)))
# pot count + 700, or other signs
for r in pot.itertuples():
    t=r.toks
    if '700' in t: print(' pot with cup:',r.cisi,r.site,' '.join(t))
# cup tablets F-count distribution
cup=collections.Counter()
for r in d[d.istab].itertuples():
    t=r.toks
    for i,x in enumerate(t):
        if x=='700' and i>0 and t[i-1] in CNT: cup[lab(t[i-1])]+=1
print('tablet cup counts',dict(sorted(cup.items())))
# homogeneity: pot singles F1-4 vs tablet cup F1-4
a=[cc.get(k,0) for k in['F1','F2','F3','F4']]; b=[cup.get(k,0) for k in['F1','F2','F3','F4']]
chi,p,_,_=stats.chi2_contingency([a,b]); print('pot single tall counts',a,'tablet cup counts',b,'chi2 %.1f p %.3g'%(chi,p))
# pot counts by site
ps=collections.defaultdict(collections.Counter)
for r in single: ps[r.site][lab(r.toks[0])]+=1
print({k:dict(v) for k,v in ps.items()})
# count value spectrum across corpus (all count tokens, any owner), by numeric value
val=collections.Counter()
for r in d.itertuples():
    for x in r.toks:
        if x in CNT: val[CNT[x][1]]+=1
print('count tokens by value (all series, any owner)',dict(sorted(val.items())))
bin_=[1,2,4,8]; 
tot=sum(val.values()); print('share at 1,2,4,8: %.2f; at 3,5,6,7: %.2f'%(sum(val[k] for k in bin_)/tot,sum(val[k] for k in [3,5,6,7])/tot))
# big-number signs frequency
sh=pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv',dtype=str).set_index('lipi_wells_number').shape_description
cn=collections.Counter(x for t in d.toks for x in t)
for s in ['019','020','025','026','027','028','029','044','048','049','051','055','057','058']: print(s,cn[s],sh.get(s)[:60])
