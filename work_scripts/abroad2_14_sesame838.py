"""Item 4. Prediction first: sign 838 (eḷ sesame) is rare abroad: fewer than 3 of the foreign objects carry it, and none at Mesopotamian sites. Home rate is compared by count."""
import sys
sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from cotton_common import *
d=faces()
fs={'Altyn Depe','Failaka','Girsu','Gonur Depe','Hajar','Janabiyah','Kalba','Karzakan','Kish','Luristan','Miri Qalat','Murda Sang','Nippur',"Qala'at al-Bahrain","Ra's al-Junayz",'Saar','Salut','Shortughai','Sibri','Susa','Tell Umma','Tello','Tepe Yahya','Ur','Unknown','Ornach area','Nindowari-damb'}
d['foreign']=d.site.isin(fs)
d['has']=[('838' in t) for t in d.toks]
print('objects',len(d),'foreign',int(d.foreign.sum()),'home',int((~d.foreign).sum()))
print('838 foreign',int(d[d.foreign].has.sum()),' home',int(d[~d.foreign].has.sum()))
print(d[d.has].groupby('site').size().sort_values(ascending=False).head(15).to_string())
print(d[d.has&d.foreign][['id','site','type']].to_string())
ports=d[d.site.str.contains('Lothal|Chanhu|Dholavira|Kuntasi|Bet Dwarka|Allahdino|Balakot|Sutkagen',regex=True,na=False)]
print('port-ish objects',len(ports),'with 838',int(ports.has.sum()))
