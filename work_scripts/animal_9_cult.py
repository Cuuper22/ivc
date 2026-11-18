"""Second stand code: the catalogue's `cult` column (S/R/H + A/B/C + N/F) on unicorn seals, as a room-mate mark, and its link to the letter W/J/S/I/L.
PREDICTION written before numbers: the 3-letter code behaves like the letter (room-mates share it, ratio ~1.5-2) since both describe the object in front of the unicorn; the third letter (N vs F) is a finer carving detail and shares the least.
Null: labels shuffled inside area x 3-ft depth x size tercile."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from animal_common import *
from scipy.stats import chi2_contingency
rng=np.random.default_rng(12); NP=3000
d=b[(b.g=='UNI')&b.cult.str.match(r'^[SRH][ABC][NF]$')&(b.room_key!='')&b.depth_ft.notna()].copy().reset_index(drop=True)
d['c1']=d.cult.str[0]; d['c2']=d.cult.str[1]; d['c3']=d.cult.str[2]; d['c12']=d.cult.str[:2]
d['szb']=pd.qcut(d.face.fillna(d.face.median()),3,labels=False).astype(str)
d['ad']=d.site+'|'+d['area-section']+'|'+(d.depth_ft//3).astype(int).astype(str)+'|'+d.szb
dep=d.depth_ft.values
P=np.array([(i,j) for k,ix in d.groupby('room_key').groups.items() for a,i in enumerate(ix) for j in ix[a+1:] if abs(dep[i]-dep[j])<=5])
print('unicorn seals with 3-letter code and room:',len(d),' same-room pairs:',len(P))
st=strata_idx(d.ad.values)
for col in ['cult','c1','c2','c3','c12','stand_sfx']:
    lab=pd.Categorical(d[col]).codes; obs=(lab[P[:,0]]==lab[P[:,1]]).mean(); null=[]
    for _ in range(NP): null.append((perm_within(lab,st,rng)[P[:,0]]==perm_within(lab,st,rng)[P[:,1]]).mean() if False else None) if False else None
    nn=[]
    for _ in range(NP):
        p=perm_within(lab,st,rng); nn.append((p[P[:,0]]==p[P[:,1]]).mean())
    nn=np.array(nn); print(f'{col:10s} same-room pairs same {obs*100:5.1f}%  chance {nn.mean()*100:5.1f}%  ratio {obs/nn.mean():.2f}  P {(1+(nn>=obs).sum())/(NP+1):.4f}')
ct=pd.crosstab(d.stand_sfx.where(d.stand_sfx.isin(['W','J','S','I','L']),'rest'),d.c12); print(ct)
print('letter vs 2-letter code: chi2',round(chi2_contingency(ct)[0],1),'p',chi2_contingency(ct)[1])
