"""Which signs sit under which animal, slot by slot? Null = animal labels shuffled inside site x seal shape x size tercile.
Slots: ANY (sign anywhere in the text), FIRST (first sign read), LAST (last sign read), NAME1 (first name sign), NAMEL (last name sign), CLS (ending class sign), AFTER (sign after the jar).
PREDICTIONS (written before the numbers):
 S1 Animal species is a weak text-mark, so few sign-animal links survive false-discovery control: at most 5 of the ~several thousand cells at q<0.10.
 S2 If any survive, they sit in ANY/FIRST (opener region), not in the ending slot (ending belongs to the person).
 S3 Elephant seals over-use fish crests and the 7-city office opening (great-house beasts): NAME1 in {231,233,235,240} ratio >1.5 for ELEPH vs chance (small n).
 S4 Goat seals are short texts with 1-2 sign names (n<=3 in 88% of MD goats): FIRST=LAST sign repeats; goat over-uses a small set of signs.
 S5 Stand-type letters (W,J,S,I,L) show no over-used signs beyond W's tie to seal size (big seals take longer, rarer signs).
Reporting: ratio=obs/chance, P one-sided (over or under), Benjamini-Hochberg q over all cells.
"""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from animal_common import *
rng=np.random.default_rng(3); NP=4000
mode=sys.argv[1] if len(sys.argv)>1 else 'SPECIES'
d=b[(b.g!='')&(b.g!='NONE')].copy().reset_index(drop=True)
if mode=='LETTER':
    d=d[(d.g=='UNI')&(d.stand_sfx!='')].reset_index(drop=True); d['g']=d.stand_sfx.where(d.stand_sfx.isin(['W','J','S','I','L']),'rest')
d['szb']=pd.qcut(d.face.fillna(d.face.median()),3,labels=False).astype(str)
st=strata_idx((d.site2+'|'+d['shape']+'|'+d.szb).values)
toks=d.reading_order_text.str.split('-')
cells={}
def add(slot,i,sign):
    if sign and sign not in('000','ALT') : cells.setdefault((slot,sign),set()).add(i)
for i,t in enumerate(toks):
    for s in set(t): add('ANY',i,s)
    add('FIRST',i,t[0]); add('LAST',i,t[-1])
    if d.tight[i]:
        add('NAME1',i,d['first'][i]); add('NAMEL',i,d['last'][i]); add('CLS',i,d.cls_last[i])
    add('AFTER',i,d.noun_c[i] if d.noun_c[i] not in('none','') else '')
keys=[k for k,v in cells.items() if len(v)>=8]
X=np.zeros((len(d),len(keys)),dtype=np.float32)
for j,k in enumerate(keys): X[list(cells[k]),j]=1
gl=sorted(d.g.unique()); gi=pd.Categorical(d.g,categories=gl).codes
def counts(gv):
    G=np.zeros((len(gl),len(d)),dtype=np.float32); G[gv,np.arange(len(d))]=1; return G@X
obs=counts(gi); null=np.zeros((NP,)+obs.shape,dtype=np.float32)
for r in range(NP): null[r]=counts(perm_within(gi,st,rng))
mu=null.mean(0); over=((null>=obs[None]-1e-6).sum(0)+1)/(NP+1); under=((null<=obs[None]+1e-6).sum(0)+1)/(NP+1)
rows=[]
for j,(sl,sg) in enumerate(keys):
    for a,g in enumerate(gl):
        rows.append(dict(group=g,slot=sl,sign=sg,obs=int(obs[a,j]),chance=round(float(mu[a,j]),2),ratio=round(float(obs[a,j]/mu[a,j]),2) if mu[a,j]>0 else np.nan,P_over=round(float(over[a,j]),5),P_under=round(float(under[a,j]),5),n_group=int((gi==a).sum()),n_sign_total=int(X[:,j].sum())))
R=pd.DataFrame(rows)
R['P']=R[['P_over','P_under']].min(axis=1); R['dir']=np.where(R.P_over<=R.P_under,'over','under')
def bh(p):
    o=np.argsort(p); q=np.empty(len(p)); r=p[o]*len(p)/(np.arange(len(p))+1); q[o]=np.minimum.accumulate(r[::-1])[::-1]; return np.minimum(q,1)
R['q']=bh(R.P.values); R=R.sort_values('P'); R.to_csv(f'{OUT}/slots_{mode}.csv',index=False)
print('cells tested',len(R),' q<0.10:',(R.q<0.10).sum(),' q<0.25:',(R.q<0.25).sum(),'  P<0.001:',(R.P<0.001).sum(),'(expected by chance ~',round(len(R)*0.001,1),')')
print(R[R.obs>=4].head(30).to_string(index=False))
