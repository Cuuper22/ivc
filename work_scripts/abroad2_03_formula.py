"""Follow-up. Predictions first:
 P4 the 10 home texts with 002-004-390 are goods/tag/tablet-type or Lothal/Chanhu-daro craft/bead-town objects, not name seals.
 P5 fibre signs (405,407) sit next to the man sign (090) on foreign round seals (Susa, Ur): 2 of 2. At home fibre signs next to 090 are rarer than on those two.
 P6 a tree sign directly after 004 abroad: 3 of 6 places, home 39 of 90."""
import sys
sys.path.insert(0,'/home/claude/ivc/work_scripts')
from cotton_common import *
from scipy.stats import binomtest
d=faces()
fs={'Altyn Depe','Failaka','Girsu','Gonur Depe','Hajar','Janabiyah','Kalba','Karzakan','Kish','Luristan','Miri Qalat','Murda Sang','Nippur',"Qala'at al-Bahrain","Ra's al-Junayz",'Saar','Salut','Shortughai','Sibri','Susa','Tell Umma','Tello','Tepe Yahya','Ur','Unknown','Ornach area','Nindowari-damb'}
home=d[~d.site.isin(fs)]
print('HOME objects with 002-004 then tree sign:')
for _,r in home.iterrows():
    t=r.toks
    for i in range(len(t)-2):
        if t[i]=='002' and t[i+1]=='004':
            print(r.id,r.site,r.type,r.mat,'|',' '.join(t),'| next:',t[i+2])
# P5
tot=sum(len(t) for t in home.toks)
man=collections.Counter(); n090=0; adj=0; adj_fibre=0; fibre=0
for t in home.toks:
    for i,x in enumerate(t):
        if x in('405','407'):
            fibre+=1
            if (i>0 and t[i-1]=='090') or (i+1<len(t) and t[i+1]=='090'): adj_fibre+=1
n090=sum(t.count('090') for t in home.toks)
print('home: 405/407 places',fibre,'next to 090:',adj_fibre,'; 090 places',n090,'of',tot,'signs; expected adjacent',round(fibre*2*n090/tot,2))
# 004-before-tree abroad vs home
a=39; n=90
print('home 004->tree 39/90; abroad 3/6; binom P(>=3 of 6 | p=.433)=',round(binomtest(3,6,39/90,alternative='greater').pvalue,3),'; vs chance rate 2.8%: P=',binomtest(3,6,556/19522,alternative='greater').pvalue)
# the 002-004-tree: 16 of 20 home, foreign 2 of 2
print('P(2 of 2 foreign 002-004 followed by tree | 16/20)=',0.8**2,' vs chance 2.8%:',round((556/19522)**2,5))
