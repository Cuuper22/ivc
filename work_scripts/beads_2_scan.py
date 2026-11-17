"""beads_2: one feature table for every sign with >=8 faces, to rank bead and cloth candidates.
PREDICTIONS (fixed before the table was built):
 B-rule: a BEAD sign has >=4 of these 6 features: (f1) ratio>=1.5 at Chanhu-daro; (f2) ratio>=1.5 at Lothal;
   (f3) ratio>=1.5 on Harappa Mound E (bead/faience/shell dump); (f4) present on >=2 faces at the foreign sites
   (Ur, Susa, Kish, Bahrain, Failaka, Oman, Iran, Central Asia: carnelian went there); (f5) ratio>=1.5 on valuable-stone/metal/shell/paste
   objects (agate, shell, paste, silver, gold, BEAD type); (f6) counted by a count sign of 4+ in front of it in >=15% of its faces (big lots).
   Prediction: 0 to 3 signs pass; if the pass count is >=4 for a sign, it is a bead-word candidate. Chance: the product of the 6 pass rates times n signs.
 C-rule: a CLOTH sign has >=4 of: (g1) ratio>=1.5 in the Mohenjo-daro dyers' block (VSA, VS-); (g2) Mohenjo-daro share above 1.3 x its Harappa share;
   (g3) on Lothal tags (>=2); (g4) present on foreign sites (>=2 faces); (g5) counted by 1-4 tall strokes in >=20% of faces (lengths/bolts);
   (g6) on faience/clay tablets of type TAB:B at Mohenjo-daro or Harappa ratio>=1.5 (cloth sealings were moulded tags). 
 Output beads_out/scan.csv"""
from goods_common import *
d=load(); d['set']=d.toks.apply(set)
FOREIGN=['Ur','Susa','Kish','Qala\'at al-Bahrain','Failaka','Ra\'s al-Junayz','Hajar','Luristan','Nippur','Tell Umma','Tello','Tepe Yahya','Gonur Depe','Girsu','Saar','Janabiyah','Kalba','Altyn Depe','Shortughai','Tello','Salut','Karzakan','Sibri','Murda Sang']
d['foreign']=d.site.isin(FOREIGN)
valuable=d.mat.isin(['agate','shell','paste','silver','gold'])|(d.type=='BEAD')
masks={'chanhu':d.site=='Chanhu-daro','lothal':d.site=='Lothal','harE':(d.site=='Harappa')&d['area-section'].str.startswith('E'),
       'valu':valuable,'dyer':(d.site=='Mohenjo-daro')&d['area-section'].isin(['VSA','VS-']),'tabB':(d.cls=='tabB')}
big={k for k,v in CNT.items() if (v[0]=='S' and v[1]>=4) or (v[0]=='T' and v[1]>=4) or (v[0]=='F' and v[1]>=4)}
tall={k for k,v in CNT.items() if v[0] in('F','T') and v[1]<=4}
cnt=collections.Counter(s for x in d.set for s in x)
rows=[]
for s,n in cnt.items():
    if n<8 or s in CNT or s=='ALT' or s=='000': continue
    r={'sign':s,'n':n}
    has=d.set.apply(lambda x:s in x)
    for k,m in masks.items():
        a=(has&m).sum(); b=m.sum()-a; c=(has&~m).sum(); dd=(~m).sum()-c
        r[k+'_n']=a; r[k+'_x'],r[k+'_p']=fe(a,b,c,dd)
    r['foreign_n']=(has&d.foreign).sum()
    r['moh']=(has&(d.site=='Mohenjo-daro')).sum()/(d.site=='Mohenjo-daro').sum()
    r['har']=(has&(d.site=='Harappa')).sum()/(d.site=='Harappa').sum()
    r['lothal_tag_n']=(has&(d.site=='Lothal')&(d.cls=='tag')).sum()
    nb=nt=0
    for t in d.toks[has]:
        for i,u in enumerate(t):
            if u==s and i>0:
                if t[i-1] in big: nb+=1
                if t[i-1] in tall: nt+=1
    r['bigfrac']=nb/n; r['tallfrac']=nt/n
    rows.append(r)
df=pd.DataFrame(rows)
df['f1']=df.chanhu_x>=1.5; df['f2']=df.lothal_x>=1.5; df['f3']=df.harE_x>=1.5; df['f4']=df.foreign_n>=2
df['f5']=(df.valu_x>=1.5)&(df.valu_n>=1); df['f6']=df.bigfrac>=0.15
df['bead_score']=df[['f1','f2','f3','f4','f5','f6']].sum(axis=1)
df['g1']=(df.dyer_x>=1.5)&(df.dyer_n>=2); df['g2']=df.moh>=1.3*df.har; df['g3']=df.lothal_tag_n>=2; df['g4']=df.foreign_n>=2
df['g5']=df.tallfrac>=0.2; df['g6']=(df.tabB_x>=1.5)
df['cloth_score']=df[['g1','g2','g3','g4','g5','g6']].sum(axis=1)
df.to_csv('beads_out/scan.csv',index=False)
print('signs',len(df))
for k in ['f1','f2','f3','f4','f5','f6','g1','g2','g3','g4','g5','g6']: print(k,int(df[k].sum()),end=' | ')
print()
print(df.bead_score.value_counts().sort_index().to_dict()); print(df.cloth_score.value_counts().sort_index().to_dict())
pd.set_option('display.width',250)
print(df.sort_values(['bead_score','n'],ascending=False).head(12)[['sign','n','bead_score','f1','f2','f3','f4','f5','f6','chanhu_x','lothal_x','harE_x','foreign_n','valu_n','bigfrac']].to_string(index=False))
print(df.sort_values(['cloth_score','n'],ascending=False).head(12)[['sign','n','cloth_score','g1','g2','g3','g4','g5','g6','dyer_n','moh','har','lothal_tag_n','foreign_n','tallfrac']].to_string(index=False))
# chance expectation for score>=4 assuming independence
import itertools
pb=[df[k].mean() for k in ['f1','f2','f3','f4','f5','f6']]; pc=[df[k].mean() for k in ['g1','g2','g3','g4','g5','g6']]
def tail(ps,k):
    tot=0
    for sel in itertools.product([0,1],repeat=len(ps)):
        if sum(sel)>=k:
            pr=1
            for p,s_ in zip(ps,sel): pr*=p if s_ else 1-p
            tot+=pr
    return tot
print('expected by independence bead>=4:',round(tail(pb,4)*len(df),2),' observed',int((df.bead_score>=4).sum()))
print('expected by independence cloth>=4:',round(tail(pc,4)*len(df),2),' observed',int((df.cloth_score>=4).sum()))
