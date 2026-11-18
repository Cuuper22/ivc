"""Part 2: tablets headed by X jar [noun]: what is on the other face, where. Part 1 add-on: agent-specific first signs."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from masters_common import *
from collections import Counter
C=pd.read_csv('/home/antigravity/Cuuper22/ivc/work_data/masters/census.csv',dtype=str,keep_default_na=False)
# first-sign enrichment
man=C[(C.noun=='090')&(C.grp=='seal')]; own=C[(C.noun=='none')&(C.grp=='seal')]
fs=lambda df:Counter(x.split('-')[0] for x in df.X)
fm,fo=fs(man),fs(own)
print('man seals',len(man),'owner seals',len(own))
for s in ['692','545','853','683','061','140','031','233','240','235','032']:
    print(s,'man',fm[s],'%.1f%%'%(100*fm[s]/len(man)),'owner',fo[s],'%.1f%%'%(100*fo[s]/len(own)))
S=set(['692','545','853','683'])
print('man with 692/545/853/683 first',sum(fm[s] for s in S),'of',len(man),'owner',sum(fo[s] for s in S),'of',len(own))
# tablets
T=C[(C.grp=='tablet')|(C.grp=='copper')|(C.grp=='tag')|(C.grp=='pot')].copy()
other=D[['id','object','reading_order_text']].copy()
def backs(obj,myid):
    return [r for i,r in zip(D[D.object==obj].id,D[D.object==obj].reading_order_text) if i!=myid]
rows=[]
for r in T.itertuples():
    b=backs(r.object,r.id)
    rows.append(dict(id=r.id,cisi=r.cisi,site=r.site,grp=r.grp,type=r.type,X=r.X,noun=r.noun,area=r._asdict()['_16'] if False else '',back='|'.join(b)))
T2=pd.DataFrame(rows).merge(M[['id','area-section','block-house','period','material']],on='id')
T2.to_csv('/home/antigravity/Cuuper22/ivc/work_data/masters/tablet_heads.csv',index=False)
def cupcount(b):
    for s in b.split('|'):
        t=s.split('-')
        if '700' in t:
            i=t.index('700'); 
            if i>0 and t[i-1] in('032','033','034','031','036','035','037','038'): return int(t[i-1][-1])
            return 0
    return None
T2['cup']=T2.back.map(cupcount)
print(T2[T2.cup.notna()].groupby('X').cup.agg(lambda s:dict(Counter(s))).loc[lambda s:s.map(len)>0].head(0))
for x in ['176','806-235-590-405','605-760','027-032','617-892','440','798-415-220','503-016','347-741-176','104-645-590-235-240','235-240','415-100','240-415-100']:
    s=T2[(T2.X==x)]
    print(x,len(s),'cup counts',dict(Counter(s.cup)),'area',dict(Counter(s['area-section']).most_common(4)),'backs',Counter(s.back).most_common(4))
