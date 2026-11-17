"""How over-represented are the box/tree-family signs among objects found abroad? (objects, not faces; identical-text copies collapsed within the foreign set only because the foreign set has none.)
Prediction first: box 590 and tree signs (390,392,405,406,407) appear on a larger share of foreign objects than of home objects (earlier job: tree 5 of 14 foreign square seals vs 9.8%)."""
import sys
sys.path.insert(0,'/home/claude/ivc/work_scripts')
from cotton_common import *
d=faces()
fs={'Altyn Depe','Failaka','Girsu','Gonur Depe','Hajar','Janabiyah','Kalba','Karzakan','Kish','Luristan','Miri Qalat','Murda Sang','Nippur',"Qala'at al-Bahrain","Ra's al-Junayz",'Saar','Salut','Shortughai','Sibri','Susa','Tell Umma','Tello','Tepe Yahya','Ur','Unknown','Ornach area','Nindowari-damb'}
d['obj']=d.id.str.split('.').str[0]
def anyset(t,S): return bool(S&set(t))
for name,S in [('tree family (390,392,405,406,407)',{'390','392','405','406','407'}),('box 590',{'590'}),('either',{'390','392','405','406','407','590'}),('390 only',{'390'})]:
    d['hit']=[anyset(t,S) for t in d.toks]
    f=d[d.site.isin(fs)]; h=d[~d.site.isin(fs)]
    # collapse home faces to distinct texts to avoid moulded copies inflating
    hh=h.drop_duplicates('text')
    a,b=f.hit.sum(),(~f.hit).sum(); c,dd=hh.hit.sum(),(~hh.hit).sum()
    r,p=fe(a,b,c,dd)
    print(f'{name}: foreign {a}/{a+b} ({a/(a+b):.1%}) vs home distinct texts {c}/{c+dd} ({c/(c+dd):.1%}); x{r:.2f}  P={p:.4f}')
# restrict foreign set to Mesopotamia+Gulf+Iran+Central Asia named sites only (drop 'Unknown')
fs2=fs-{'Unknown'}
for name,S in [('either (named foreign sites only)',{'390','392','405','406','407','590'})]:
    d['hit']=[anyset(t,S) for t in d.toks]
    f=d[d.site.isin(fs2)]; hh=d[~d.site.isin(fs)].drop_duplicates('text')
    a,b=f.hit.sum(),(~f.hit).sum(); c,dd=hh.hit.sum(),(~hh.hit).sum()
    r,p=fe(a,b,c,dd); print(f'{name}: foreign {a}/{a+b} vs home {c}/{c+dd}; x{r:.2f} P={p:.4f}')
