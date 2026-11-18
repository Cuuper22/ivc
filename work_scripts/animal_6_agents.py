"""Do agents carry their master's animal? Agent seal = `X jar man` (X = master). Owner seals = `X jar` with the same X (or the same first sign of X, the house crest).
PREDICTION written before the numbers: clan/house reading predicts agents carry the master's species and stand letter above chance (ratio >=1.5). If animal is a mark of the person and not the house, ratio ~1.
Null: agent labels shuffled among agents of the same site."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from animal_common import *
rng=np.random.default_rng(2); NP=5000
d=b[(b.g!='')&(b.g!='NONE')&(b.X_c!='')].copy().reset_index(drop=True)
d['L']=np.where((d.g=='UNI')&(d.stand_sfx!=''),d.stand_sfx,'')
ag=d[(d.noun_c=='090')]; ow=d[(d.noun_c=='none')&(d.has_jar)]
print('agent seals with animal:',len(ag),' owner seals with animal:',len(ow))
d['Xfirst']=d.X_c.str.split('-').str[0]
def run(label,keyfun,col):
    pairs=[]
    ak=ag.X_c.map(keyfun); ok_=ow.X_c.map(keyfun)
    for i,k in ak.items():
        for j in ok_[ok_==k].index:
            if d.id[i]!=d.id[j]: pairs.append((i,j))
    lab=d[col].values
    pairs=[(i,j) for i,j in pairs if lab[i]!='' and lab[j]!='']
    if len(pairs)<8: print(f'{label:36s}{col:2s} pairs {len(pairs)} (too few)'); return
    pairs=np.array(pairs); obs=np.mean(lab[pairs[:,0]]==lab[pairs[:,1]])
    agi=np.array(sorted(set(pairs[:,0]))); st=strata_idx(d.loc[agi,'site2'].values); null=[]
    for _ in range(NP):
        l2=lab.copy(); p=perm_within(np.arange(len(agi)),st,rng); l2[agi]=lab[agi][p]
        null.append(np.mean(l2[pairs[:,0]]==l2[pairs[:,1]]))
    null=np.array(null); pv=(1+(null>=obs).sum())/(NP+1)
    print(f'{label:36s}{col:2s} pairs {len(pairs):3d} agents {len(agi):3d}  same {obs*100:5.1f}%  chance {null.mean()*100:5.1f}%  ratio {obs/null.mean():.2f}  P {pv:.4f}')
for col in ['g','L']:
    run('same master X (exact)',lambda x:x,col)
    run('same master crest (first sign of X)',lambda x:x.split('-')[0],col)
# agents vs agents of the same master and owner seals of same X (all types incl. no-animal) -> how many masters have animals on both sides
