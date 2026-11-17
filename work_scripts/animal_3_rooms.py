"""Do house-mates (same room, depth within 5 ft) carry the same animal? Null = labels shuffled inside area x 3-ft depth band.
PREDICTION (written before the numbers): clan reading says same-room pairs share coarse animal above chance by a clear margin (ratio >=1.5); the earlier 12.5% vs 11.0% (all labels) is the baseline to beat.
Three label sets: coarse animal group (UNI, SHORT, ...), unicorn stand type (W, J, S, I, L, ...) for unicorn seals, and fine = both.
"""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from animal_common import *
rng=np.random.default_rng(11); NP=3000
d=b[(b.room_key!='')&b.depth_ft.notna()&(b.g!='')&(b.g!='NONE')].copy()
d['sfx']=np.where(d.g=='UNI',d.stand_sfx.replace('','plain'),d.g)
d['fine']=d.sfx
d['uni_only']=np.where(d.g=='UNI',d.stand_sfx.replace('','plain'),'')
d['area_depth']=d.site+'|'+d['area-section']+'|'+(d.depth_ft//3).astype(int).astype(str)
d=d.reset_index(drop=True)
rm=d.room_key.values; dep=d.depth_ft.values
pairs=[(i,j) for k,ix in d.groupby('room_key').groups.items() for a,i in enumerate(ix) for j in ix[a+1:] if abs(dep[i]-dep[j])<=5]
P=np.array(pairs); print('rooms with pairs; pairs:',len(P),'  seals in pairs:',len(set(P.ravel())))
st=strata_idx(d.area_depth.values)
def run(label,col,mask=None):
    lab=pd.Categorical(d[col].where(d[col]!='','~')).codes.copy()
    ok=(d[col]!='').values
    pp=P[ok[P[:,0]]&ok[P[:,1]]]
    obs=(lab[pp[:,0]]==lab[pp[:,1]]).mean()
    # shuffle labels inside strata; the pairs stay put
    null=[]
    for _ in range(NP):
        p=lab.copy()
        for ix in st:
            p[ix]=lab[rng.permutation(ix)]
        null.append((p[pp[:,0]]==p[pp[:,1]]).mean())
    null=np.array(null); pv=(1+(null>=obs).sum())/(NP+1)
    print(f'{label:34s} pairs {len(pp):4d} same {obs*100:5.1f}%  chance {null.mean()*100:5.1f}%  ratio {obs/null.mean():.2f}  P {pv:.4f}')
    return dict(label=label,pairs=len(pp),same=round(obs,4),chance=round(null.mean(),4),ratio=round(obs/null.mean(),3),P=round(pv,4))
d['szb']=pd.qcut(d.face.fillna(d.face.median()),3,labels=False).astype(str)
d['area_depth_size']=d.area_depth+'|'+d.szb
st_save=st
out=[run('coarse animal group','g'),run('unicorn stand type (unicorns only)','uni_only'),run('fine (stand type for unicorns)','fine')]
st=strata_idx(d.area_depth_size.values)
print('-- stricter null: shuffle inside area x 3ft depth x seal-size tercile')
out+= [dict(strict=True,**run('STRICT '+a,c)) for a,c in [('coarse animal group','g'),('unicorn stand type','uni_only')]]
pd.DataFrame(out).to_csv(f'{OUT}/rooms.csv',index=False)
