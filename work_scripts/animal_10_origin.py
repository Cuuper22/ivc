"""Does a non-unicorn animal bring a home community's sign vocabulary with it?
Idea (from the abroad finding and Banawali goats): species marks a community of origin or circuit. If so, SHORT-horned seals at Mohenjo-daro should use the signs found on SHORT seals abroad
more than other Mohenjo-daro seals do; GOAT seals at Mohenjo-daro should use the signs of Banawali goat seals more than other Mohenjo-daro seals.
PREDICTION written before numbers: ratio >1.3 for both. Score = share of a seal's signs that occur on the reference seals (excluding common signs seen on >150 faces: 032, 060, 740 etc.).
Null: Mohenjo-daro labels shuffled inside shape x size tercile."""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from animal_common import *
rng=np.random.default_rng(6); NP=5000
ABR=['Persian Gulf','Mesopotamia','Iranian Plateau','Central Asia']
allt=b.reading_order_text.str.split('-')
freq=pd.Series([s for t in allt for s in set(t)]).value_counts(); rare={s for s,c in freq.items() if c<=150 and s not in('000','ALT')}
def signs(t): return {s for s in t.split('-') if s in rare}
def ref(mask): 
    S=set()
    for t in b.loc[mask,'reading_order_text']: S|=signs(t)
    return S
md=b[(b.site=='Mohenjo-daro')&(b.g!='')&(b.g!='NONE')].copy().reset_index(drop=True)
md['szb']=pd.qcut(md.face.fillna(md.face.median()),3,labels=False).astype(str); st=strata_idx((md['shape']+'|'+md.szb).values)
for nm,grp,refmask in [('SHORT at MD vs abroad SHORT seals','SHORT',(b.g=='SHORT')&b.region.isin(ABR)),('GOAT at MD vs Banawali GOAT seals','GOAT',(b.g=='GOAT')&(b.site=='Banawali')),('SHORT at MD vs abroad ANY animal seals','SHORT',b.region.isin(ABR)&(b.g!='')&(b.g!='NONE'))]:
    R=ref(refmask); sc=[]
    for t in md.reading_order_text:
        S=signs(t); sc.append(len(S&R)/len(S) if S else np.nan)
    sc=np.array(sc); m=(md.g==grp).values&~np.isnan(sc); obs=np.nanmean(sc[m])
    gi=(md.g==grp).values.astype(int); null=[]
    for _ in range(NP):
        p=perm_within(gi,st,rng).astype(bool)&~np.isnan(sc); null.append(np.nanmean(sc[p]))
    null=np.array(null); print(f'{nm:42s} ref signs {len(R):3d} seals {m.sum():3d} score {obs:.3f} chance {null.mean():.3f} ratio {obs/null.mean():.2f} P_over {(1+(null>=obs).sum())/(NP+1):.4f}')
