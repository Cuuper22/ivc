"""Bare-number objects, global count histogram, followers per counted thing, fish group."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from counted_common import *
d=pd.read_csv(f'{ROOT}/work_data/counted/instances_resolved.csv',dtype=str,keep_default_na=False)
rows=load()
# 1) objects whose whole text is one count sign
bare=collections.defaultdict(collections.Counter)
for r,toks,b in rows:
    if len(toks)==1 and toks[0] in CNT: bare[r['type'].split(':')[0]][label(toks[0])]+=1
print('BARE-NUMBER OBJECTS by type x count label')
for t,c in sorted(bare.items(),key=lambda x:-sum(x[1].values())):
    if sum(c.values())>=4: print(t,sum(c.values()),dict(sorted(c.items())))
# 2) global value histogram of counts before any non-count sign (B), by series
B=d[d.frame=='B'].drop_duplicates(['id','sign','cs'])
print('\nGLOBAL count label histogram (B frame, one per object-sign):'); print(B['count'].value_counts().to_dict())
# 3) followers
def nclass(x):
    if x=='END': return 'END'
    if x in CARR: return 'carrier'
    if x in('740','741'): return 'jar'
    if x=='400': return 'comb'
    if x in CNT: return 'count'
    return 'other'
B=B.assign(nc=B.nxt.map(nclass))
ct=pd.crosstab(B.sign,B.nc); ct['n']=ct.sum(axis=1)
ct=ct[ct.n>=15].sort_values('n',ascending=False)
print('\nFOLLOWERS of counted things (B frame, n>=15)'); print(ct.to_string())
ct.to_csv(f'{ROOT}/work_data/counted/followers.csv')
# 4) fish family (resolved ownership)
FISH=['220','222','226','227','228','231','232','233','234','235','236','240','241','242','243','244']
fo=collections.Counter(s for r,t,b in rows for s in t if s in FISH)
Bf=d[(d.frame=='B')&d.sign.isin(FISH)].drop_duplicates(['id','sign','cs'])
print('\nFISH family (resolved): occurrences, counted-before, share, count labels')
for s in FISH:
    g=Bf[Bf.sign==s]
    if fo[s]: print(s,fo[s],len(g),round(len(g)/fo[s],2),dict(g['count'].value_counts().head(6)))
print('all fish',sum(fo.values()),len(Bf),round(len(Bf)/sum(fo.values()),3)); print('pooled',dict(Bf['count'].value_counts()))
print('pooled by series',dict(Bf.series.value_counts()))
print('fish counted after (X n)',len(d[(d.frame=='A')&d.sign.isin(FISH)]))
print('fish by type',dict(Bf.type.str.split(':').str[0].value_counts()))
