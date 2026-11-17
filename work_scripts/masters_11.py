"""Checks behind the institution table: animals per X, 176, 048, 590-390, copper tablet spread, Lothal tag areas, first-sign tag test."""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from masters_common import *
from collections import Counter
import random, itertools
from scipy.stats import fisher_exact
C=pd.read_csv('/home/claude/ivc/work_data/masters/census.csv',dtype=str,keep_default_na=False); C['face']=C.face.astype(float)
S=C[C.grp=='seal']
man=S[S.noun=='090']; own=S[S.noun=='none']
F=lambda df:df.X.str.split('-').str[0].isin(['692','545','853','683'])
a,b,c,d=F(man).sum(),(~F(man)).sum(),F(own).sum(),(~F(own)).sum()
print('agent first sign in {692,545,853,683}: man seals',a,'of',a+b,'owner seals',c,'of',c+d,'fisher p',fisher_exact([[a,b],[c,d]])[1])
# last sign of agent X vs owner
for L in ['220','100','240','035','101']:
    f=lambda df:(df.X.str.split('-').str[-1]==L)
    print('last',L,'man',f(man).sum(),'owner',f(own).sum(),'of',len(own))
# animals of 176 seals
s176=S[S.X=='176']; print('seal X=176',len(s176),dict(Counter(s176.sym)),dict(Counter(s176.site)),dict(Counter(s176.noun)))
allseals=D[D.type.str.startswith('SEAL')]; print('Bult share among all seals',(allseals.symbol=='Bult').mean(), 'n',(allseals.symbol=='Bult').sum())
t176=C[(C.X=='176')&(C.noun=='400')]; print('176 jar comb by group',dict(Counter(t176.grp)),dict(Counter(t176.site)))
# animal sharing across seals of the same X (any noun)
def pairs_same(df):
    n=s=0
    for x,g in df.groupby('X'):
        l=[a for a in g.sym if a not in('','-')]
        for p,q in itertools.combinations(l,2): n+=1; s+=(p==q)
    return n,s
sd=S[~S.sym.isin(['','-'])].copy(); sd['sym2']=sd.sym.str.split(':').str[0]
sd['sym']=sd['sym2']
n,s=pairs_same(sd); sims=[]
for _ in range(300):
    t=sd.copy(); t['sym']=random.sample(list(sd.sym),len(sd)); sims.append(pairs_same(t)[1])
print('seal pairs sharing exact X',n,'same animal (family-merged)',s,'chance',sum(sims)/300,'max',max(sims))
sa=sd[sd.noun.isin(['090','400','679','621'])]
n,s=pairs_same(sa); print('agent seals sharing X: pairs',n,'same animal',s)
# 048
x=D[D.toks.map(lambda t:'048' in t)]
print(x[['cisi','site','type','symbol','reading_order_text']].to_string())
# 590-390 text
x=D[D.toks.map(lambda t:t[:0]==[] and any(t[i:i+2]==['590','390'] for i in range(len(t)-1)))]
print('590-390 by region',dict(Counter(x.region)),'abroad',x[x.region.isin(['Persian Gulf','Mesopotamia','Iranian Plateau','Central Asia'])][['cisi','site','type','reading_order_text']].to_string())
print('590-390 as full X before jar: ',dict(Counter(C[C.X=='590-390'].site)), dict(Counter(C[C.X=='590-390'].noun)))
# copper
for X in ['503-615-752','806-845-061-407-850-900','706-033-923']:
    cc=D[D.type=='TAB:C'][D[D.type=='TAB:C'].toks.map(lambda t:'-'.join(t).startswith(X))].merge(M[['id','area-section','block-house','horizontal(mm)','vertical(mm)','symbol']],on='id',suffixes=('','_m'))
    print(X,len(cc),'blocks',cc['area-section'].nunique(),dict(Counter(cc['area-section']).most_common(8)),'houses',cc['block-house'].nunique(),'size',cc['horizontal(mm)_m'].astype(float).median(),cc['vertical(mm)_m'].astype(float).median(),dict(Counter(cc['symbol_m'])))
# Lothal tag areas
T=pd.read_csv('/home/claude/ivc/work_data/masters/tags.csv',dtype=str,keep_default_na=False)
L=T[T.site=='Lothal']; print('Lothal tag rows',len(L),'objects',L.object.nunique(),dict(Counter(L['area-section'])))
print('Lothal by kind',dict(Counter(L.kind)))
print('Lothal 3GX 10 by text', L[L['area-section']=='SRG 3GX 10'].reading_order_text.value_counts().to_dict())
