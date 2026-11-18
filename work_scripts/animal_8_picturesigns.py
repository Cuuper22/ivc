"""Do animal-picture signs in the text go with the animal on the seal?
Sets (shapes from sign_shapes.csv): DEER 340-348 ; ANIMAL255 = 255,256 ; HORN 490,500,502 ; ANIMALLEG 121.
PREDICTIONS written before numbers: the text sign for an animal is the same word as the seal animal? If the seal animal is the name of the owner's group, the deer signs would sit under the deer-like animals (goat/antelope/composite) and horn signs under bulls (UNI, SHORT, ZEBU). Expect ratio >1.5 in those pairs; otherwise none.
Null: labels shuffled inside site x shape x size tercile."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from animal_common import *
rng=np.random.default_rng(8); NP=5000
d=b[(b.g!='')&(b.g!='NONE')].copy().reset_index(drop=True)
d['szb']=pd.qcut(d.face.fillna(d.face.median()),3,labels=False).astype(str); st=strata_idx((d.site2+'|'+d['shape']+'|'+d.szb).values)
tk=d.reading_order_text.str.split('-')
sets={'DEER 340-348':{str(i) for i in range(340,349)},'ANIMAL 255/256':{'255','256'},'HORN-triangle 490/500/502':{'490','500','502'},'person+animal leg 121':{'121'}}
gl=['UNI','SHORT','ZEBU','ELEPH','WILD3','GOAT','COMP']
for nm,S in sets.items():
    x=tk.map(lambda t:any(s in S for s in t)).values.astype(int)
    for g in gl:
        m=(d.g==g).values
        obs=x[m].sum()
        if x.sum()<6: continue
        null=np.array([x[perm_within(m.astype(int),st,rng).astype(bool)].sum() for _ in range(NP)])
        po=(1+(null>=obs).sum())/(NP+1); pu=(1+(null<=obs).sum())/(NP+1)
        print(f'{nm:26s} {g:6s} n={m.sum():4d} seals with set {obs:3d} chance {null.mean():5.1f} ratio {obs/null.mean() if null.mean() else float("nan"):.2f} P_over {po:.4f} P_under {pu:.4f}')
