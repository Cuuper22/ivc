"""Remaining numbers: agent-name last signs, 176 comb tablets, 415-100 chain counts, Lothal tag who-list, 920-060-741 office prefix."""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from masters_common import *
from collections import Counter
from scipy.stats import fisher_exact
C=pd.read_csv('/home/claude/ivc/work_data/masters/census.csv',dtype=str,keep_default_na=False)
S=C[C.grp=='seal']; man=S[S.noun=='090']; own=S[S.noun=='none']
for L in ['220','240','035','101']:
    a=(man.X.str.split('-').str[-1]==L).sum(); c=(own.X.str.split('-').str[-1]==L).sum()
    print('last sign',L,'man',a,'/',len(man),'owner',c,'/',len(own),'p',fisher_exact([[a,len(man)-a],[c,len(own)-c]])[1])
fish=lambda df:df.X.str.split('-').str[-1].isin(['220','240','235','231','233'])
a,c=fish(man).sum(),fish(own).sum(); print('any fish last: man',a,'owner',c,'p',fisher_exact([[a,len(man)-a],[c,len(own)-c]])[1])
# 176 jar comb
t=C[(C.X=='176')&(C.noun=='400')]
print('176 jar comb objects',len(t),dict(Counter(t.grp)),dict(Counter(t['area-section'])),dict(Counter(t.sym)))
sy=D[D.symbol=='Bult']; print('Bult objects total',len(sy),'with 176-740-400',(sy.reading_order_text=='176-740-400').sum())
# 920-060-741 prefix
D['pre']=D.toks.map(lambda t:t[:3]==['920','060','741'])
p=D[D.pre]; print('920-060-741 prefix: objects',len(p),'sites',p.site.nunique(),dict(Counter(p.type.str.split(':').str[0])))
print('  with jar close',sum('740' in t for t in p.toks))
# 415-100 contiguous
x=D[D.toks.map(lambda t:any(t[i:i+2]==['415','100'] for i in range(len(t)-1)))]
print('415-100 objects',len(x),x.object.nunique(),'sites',dict(Counter(x.site)),dict(Counter(x.type.str.split(':').str[0])))
# Lothal tags who
T=pd.read_csv('/home/claude/ivc/work_data/masters/tags.csv',dtype=str,keep_default_na=False)
L=T[T.site=='Lothal']
print('Lothal tag rows',len(L),'objects',L.object.nunique())
def lothal_kind(tx):
    k=T[T.reading_order_text==tx].kind.iloc[0]; return k
print(L.kind.value_counts().to_dict())
print('distinct whole-name tag texts (no lost sign, has jar or spear):',L[(~L.reading_order_text.str.contains('000'))&L.reading_order_text.str.contains('740|520')].reading_order_text.nunique())
print('tags by Lothal rows in 3GX 10:',(L['area-section']=='SRG 3GX 10').sum())
# tags overall kinds
print('all tags', T.kind.value_counts().to_dict())
# total tag rows with whole-name+ending
ok=T[T.kind.isin(['owner (X jar)','agent (X jar man)','spearman (X spear)','carrier (X porter)','jar + other (151)'])]
print('tag rows with a whole ending',len(ok))
print('tags: owner-type share',(T.kind=='owner (X jar)').sum(),'agent',(T.kind=='agent (X jar man)').sum(),'spear',(T.kind=='spearman (X spear)').sum(),'carrier',(T.kind=='carrier (X porter)').sum())
# in the seals corpus the ratio
Sa=D[D.type.str.startswith('SEAL')]
print('seals: spear-final',(Sa.toks.map(lambda t:t[-1]=='520')).mean(),'tags spear-final',(T.reading_order_text.str.endswith('520')).mean())
# 590-390: Kish & Gonur seals
print(D[D.toks.map(lambda t:any(t[i:i+2]==['590','390'] for i in range(len(t)-1)))].groupby('site').size().to_dict())
