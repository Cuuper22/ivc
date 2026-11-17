"""Which text relationships make two seals share an animal or a stand letter?
PREDICTIONS (written before the numbers): the stand letter is a mark of the house or workshop, not of the person:
 Q1 same room: shown already (ratio 2.2). Q2 gradient: same-letter rate falls from same room > same house other room > same area other house > same site.
 Q3 same full name text (the same person on two stones): shares the letter above chance (ratio >=1.5); shares species above chance too.
 Q4 same first sign (the crest-slot sign): letter ratio ~1 (crest and letter are two separate marks).
 Q5 same ending sign: ratio ~1.
Null: labels shuffled inside site x seal-shape x seal-size tercile. Pairs counted once.
"""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from animal_common import *
rng=np.random.default_rng(5); NP=2000
d=b[(b.g!='')&(b.g!='NONE')].copy().reset_index(drop=True)
d['L']=np.where((d.g=='UNI')&(d.stand_sfx!=''),d.stand_sfx,'')
d['szb']=pd.qcut(d.face.fillna(d.face.median()),3,labels=False).astype(str)
d['stk']=d.site2+'|'+d['shape']+'|'+d.szb
st=strata_idx(d.stk.values)
def pairs_by(key,mask=None,drop=('',)):
    k=d[key].copy()
    if mask is not None: k=k.where(mask,'')
    P=[]
    for v,ix in k.groupby(k).groups.items():
        if v in drop or len(ix)>40: continue
        ix=list(ix); P+= [(i,j) for a,i in enumerate(ix) for j in ix[a+1:]]
    return np.array(P) if P else np.zeros((0,2),int)
def test(label,P,col):
    lab=pd.Categorical(d[col].where(d[col]!='','~')).codes.copy(); ok=(d[col]!='').values
    if len(P)==0: print(label,'no pairs'); return None
    P=P[ok[P[:,0]]&ok[P[:,1]]]
    if len(P)<10: print(f'{label:46s} {col:3s} pairs {len(P)} (too few)'); return None
    obs=(lab[P[:,0]]==lab[P[:,1]]).mean(); null=[]
    for _ in range(NP):
        p=lab.copy()
        for ix in st: p[ix]=lab[rng.permutation(ix)]
        null.append((p[P[:,0]]==p[P[:,1]]).mean())
    null=np.array(null); pv=(1+(null>=obs).sum())/(NP+1)
    r=dict(pairs_of=label,label=col,pairs=len(P),same=round(obs,3),chance=round(null.mean(),3),ratio=round(obs/null.mean(),2),P=round(pv,4))
    print(f"{label:46s} {col:3s} pairs {len(P):5d} same {obs*100:5.1f}% chance {null.mean()*100:5.1f}% ratio {r['ratio']:.2f} P {pv:.4f}"); return r
res=[]
tight=d.tight.values
d['name2']=np.where(tight&(d.name.str.count('-')>=1),d.name,'')           # names with 2+ signs
d['name1']=np.where(tight&(d.name!=''),d.name,'')
d['text']=np.where(d.reading_order_text.str.count('-')>=3,d.reading_order_text,'')
d['firstk']=np.where(tight,d['first'],''); d['lastk']=np.where(tight,d['last'],''); d['clsk']=np.where(tight,d.cls_last,'')
d['room']=d.room_key
d['house']=np.where((d['block-house'].isin(['--','-',''])),'',d.site+'|'+d['area-section']+'|'+d['block-house'])
d['area']=np.where((d['area-section'].isin(['--','-',''])),'',d.site+'|'+d['area-section'])
for lab,key in [('same room (any depth)','room'),('same house block (any room)','house'),('same area','area'),('same 2+ sign name','name2'),('same full name (1+ signs)','name1'),('same text (4+ signs)','text'),('same first name sign','firstk'),('same last name sign','lastk'),('same ending sign','clsk')]:
    P=pairs_by(key)
    for col in ['g','L']:
        r=test(lab,P,col); 
        if r: res.append(r)
pd.DataFrame(res).to_csv(f'{OUT}/pairs.csv',index=False)
