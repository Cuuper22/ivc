"""Goods job step 1: for every sign, where it lives (object type, site, area, material), what it counts, whether it stands alone.
Writes goods_out/sign_world.csv. Run from work_scripts: python3 goods_1_signs.py"""
from goods_common import *
d=load()
N=len(d)
print('faces',N)
sig=collections.defaultdict(set)
for i,t in enumerate(d.toks):
    for s in set(t): sig[s].add(i)
groups={'tag':d.cls=='tag','pot':d.cls=='pot','tool':d.cls.isin(['impl','bngl','rod']),'impl':d.cls=='impl','bngl':d.cls=='bngl','rod':d.cls=='rod',
 'tabC':d.cls=='tabC','tabB':d.cls=='tabB','tabI':d.cls=='tabI','seal':d.cls=='seal',
 'lothal':d.site=='Lothal','chanhu':d.site=='Chanhu-daro','dhola':d.site=='Dholavira','gran':d.gran,'harF':d.harF,'E11':d.E11,'moh':d.site=='Mohenjo-daro','har':d.site=='Harappa',
 'copper':d.mat=='copper','ivory':d.mat.isin(['ivory','bone']),'faience':d.mat=='faience','clay':d.mat.isin(['clay','terracotta']),'steatite':d.mat=='steatite','stoneware':d.mat=='stoneware'}
rows=[]
for s,idx in sig.items():
    if s in CNT or s in('000','ALT'): continue
    ix=np.zeros(N,bool); ix[list(idx)]=True
    n=ix.sum()
    if n<6: continue
    r={'sign':s,'faces':int(n)}
    for g,m in groups.items():
        a=int((ix&m.values).sum()); b=int((~ix&m.values).sum()); c=n-a; dd=(N-m.sum())-c
        er,p=fe(a,int(m.sum())-a,c,dd)
        r[g+'_n']=a; r[g+'_x']=round(er,2) if er==er else None; r[g+'_p']=p
    # alone / counted / carrier
    alone=cnt_before=cnt_after=carr_after=cnt_s_carr=0
    for i in idx:
        t=d.toks[i]
        if len(t)==1: alone+=1
        for j,x in enumerate(t):
            if x!=s: continue
            if j>0 and t[j-1] in CNT: cnt_before+=1
            if j+1<len(t) and t[j+1] in CNT: cnt_after+=1
            if j+1<len(t) and t[j+1] in CARR: carr_after+=1
            if j>0 and t[j-1] in CNT and j+1<len(t) and t[j+1] in CARR: cnt_s_carr+=1
    r.update(alone=alone,cnt_before=cnt_before,cnt_after=cnt_after,carr_after=carr_after,cnt_s_carr=cnt_s_carr)
    rows.append(r)
W=pd.DataFrame(rows).sort_values('faces',ascending=False)
W.to_csv(f'{OUT}/sign_world.csv',index=False)
print(len(W),'signs with >=6 faces')
print(d.cls.value_counts().to_dict())
