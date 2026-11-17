"""beads_4: signs on seals found abroad (Ur, Susa, Kish, Bahrain, Failaka, Oman, Central Asia ...) where carnelian beads were landed,
crossed with the bead towns.
PREDICTION (before the table): a bead/carnelian word is among signs with >=3 foreign faces and ratio>=3 (one-sided Fisher P<0.01) AND ratio>=1.3 at Lothal or Chanhu-daro.
Expect 0 to 2 signs pass. Also test 055 (dozen) abroad and 048 on silver."""
from goods_common import *
d=load(); d['set']=d.toks.apply(set)
FOREIGN=['Ur','Susa','Kish',"Qala'at al-Bahrain",'Failaka',"Ra's al-Junayz",'Hajar','Luristan','Nippur','Tell Umma','Tello','Tepe Yahya','Gonur Depe','Girsu','Saar','Janabiyah','Kalba','Altyn Depe','Shortughai','Salut','Karzakan','Sibri','Murda Sang']
fo=d.site.isin(FOREIGN); print('foreign faces',fo.sum())
cn=collections.Counter(s for x in d[fo].set for s in x); co=collections.Counter(s for x in d[~fo].set for s in x)
bt=d.site.isin(['Lothal','Chanhu-daro']); cb=collections.Counter(s for x in d[bt].set for s in x); cr=collections.Counter(s for x in d[~bt].set for s in x)
rows=[]
for s,a in cn.items():
    if a<3 or s in('ALT','000'): continue
    r,p=fe(a,fo.sum()-a,co.get(s,0),(~fo).sum()-co.get(s,0))
    rb,pb=fe(cb.get(s,0),bt.sum()-cb.get(s,0),cr.get(s,0),(~bt).sum()-cr.get(s,0))
    rows.append((s,a,round(r,2),'%.2g'%p,cb.get(s,0),round(rb,2),'%.2g'%pb))
df=pd.DataFrame(rows,columns=['sign','foreign_n','foreign_x','foreign_p','bt_n','bt_x','bt_p']).sort_values('foreign_p',key=lambda c:c.astype(float))
print(df.head(14).to_string(index=False)); df.to_csv('beads_out/foreign.csv',index=False)
print('passing prediction:',df[(df.foreign_x>=3)&(df.foreign_p.astype(float)<0.01)&(df.bt_x>=1.3)].sign.tolist())
# 055 abroad
for _,r in d[fo&d.toks.apply(lambda t:'055' in t)].iterrows(): print(r.id,r.site,r.type,'-'.join(r.toks))
# 048 on silver
sil=d[d.mat=='silver']; print('silver objects',len(sil),'with 048:',int(sil.toks.apply(lambda t:'048' in t).sum()),' base rate of 048 per face %.4f'%(d.toks.apply(lambda t:'048' in t).mean()))
from scipy.stats import binom
print('P(>=1 of 3 silver by chance)=%.4f'%(1-(1-d.toks.apply(lambda t:'048' in t).mean())**len(sil)))
