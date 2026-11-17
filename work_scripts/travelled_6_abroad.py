"""Job: the travelled name. Step 6: every object found abroad: its text, and which adjacent sign pairs (2-grams, no lost/count/jar signs) also stand on home objects, with home counts and sites. Run: python3 travelled_6_abroad.py"""
import pandas as pd, collections, re
R='/home/claude/ivc/'
G=pd.read_csv(R+'work_data/gloss2_all.csv',dtype=str)
M=pd.read_csv(R+'research/data/open_prototype/lipi/metadata_filtered.csv',dtype=str)
D=G.merge(M[['id','region']],on='id'); D['toks']=D.reading_order_text.str.split('-')
AB={'Persian Gulf','Mesopotamia','Iranian Plateau','Central Asia'}
SKIP={'000','740','001','002','003','004','005','031','032','033','034','ALT'}
home=D[~D.region.isin(AB)]
idx=collections.defaultdict(lambda:(set(),collections.Counter()))
for o,s,t in zip(home.object,home.site,home.toks):
    seen=set()
    for i in range(len(t)-1):
        p=(t[i],t[i+1])
        if set(p)&SKIP or p in seen: continue
        seen.add(p); idx[p][0].add(o); idx[p][1][s]+=1
rows=[]
for r in D[D.region.isin(AB)].drop_duplicates('object').itertuples():
    t=r.toks
    for i in range(len(t)-1):
        p=(t[i],t[i+1])
        if set(p)&SKIP: continue
        n=len(idx[p][0])
        if n>=5: rows.append((r.site,r.cisi,r.type,r.reading_order_text,'-'.join(p),n,len(idx[p][1]),dict(idx[p][1].most_common(3))))
out=pd.DataFrame(rows,columns=['site','cisi','type','text','pair','home_objects','home_sites','top_sites'])
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',60)
print(out.sort_values('home_objects',ascending=False).to_string(index=False))
out.to_csv(R+'work_scripts/travelled_out/abroad_pairs.csv',index=False)
print('abroad objects',D[D.region.isin(AB)].object.nunique())
# tree sign 390 (and variant 392) on square seals abroad vs home
from scipy import stats
sq=D[(D.type=='SEAL:S')].drop_duplicates('object')
ab=sq[sq.region.isin(AB)]; hm=sq[~sq.region.isin(AB)]
f=lambda df,S:df.toks.map(lambda t:bool(set(t)&S)).sum()
for S,name in [({'390'},'390'),({'390','392'},'390 or 392'),({'590'},'590')]:
    a=f(ab,S);h=f(hm,S)
    print(name,'abroad square seals',a,'of',len(ab),'| home',h,'of',len(hm),f'({h/len(hm):.3f})','binomial P(>=a)=',round(stats.binom.sf(a-1,len(ab),h/len(hm)),4))
print(ab[['site','cisi','reading_order_text']].to_string(index=False))
