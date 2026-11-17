"""The short-horned bull with trough and the seals found abroad.
Found by the scan: abroad seals (Gulf, Mesopotamia, Iran, Central Asia) are short-horned bull 14 of 26 (54%) against 92 of 1575 at home (5.8%).
PREDICTIONS written before these numbers: if the short-horned bull marks the overseas-trade circuit, then at HOME its seals (a) use the 'abroad' signs man 090 / twin-men 091 / single stroke 001 more than chance, (b) end with the jar 740 less than chance, (c) sit more at the port/coast towns (Lothal, Chanhu-daro, Gola Dhoro, Kalibangan?) - no: predicted at coast sites: Lothal, Chanhu-daro, Gola Dhoro, Nausharo, Allahdino.
Null: animal labels shuffled inside site x shape x size tercile (a)(b); for (c) Fisher against the other animals.
"""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from animal_common import *
from scipy.stats import fisher_exact
rng=np.random.default_rng(4); NP=5000
ABR=['Persian Gulf','Mesopotamia','Iranian Plateau','Central Asia']
d=b[(b.g!='')&(b.g!='NONE')&(~b.region.isin(ABR))].copy().reset_index(drop=True)
d['szb']=pd.qcut(d.face.fillna(d.face.median()),3,labels=False).astype(str)
st=strata_idx((d.site2+'|'+d['shape']+'|'+d.szb).values)
tk=d.reading_order_text.str.split('-')
feat={'man 090 or 091 anywhere':tk.map(lambda t:('090' in t) or ('091' in t)),'single stroke 001 anywhere':tk.map(lambda t:'001' in t),'ends in jar 740':tk.map(lambda t:t[-1]=='740'),'has jar 740':tk.map(lambda t:'740' in t),'text length<=3':tk.map(lambda t:len(t)<=3)}
m=(d.g=='SHORT').values.astype(int)
for k,v in feat.items():
    x=v.values.astype(int); obs=x[m==1].mean(); null=[]
    for _ in range(NP): null.append(x[perm_within(m,st,rng).astype(bool)].mean())
    null=np.array(null); po=(1+(null>=obs-1e-9).sum())/(NP+1); pu=(1+(null<=obs+1e-9).sum())/(NP+1)
    print(f'{k:28s} short-horned home seals {obs*100:5.1f}% ({x[m==1].sum()}/{m.sum()})  chance {null.mean()*100:5.1f}%  ratio {obs/null.mean():.2f}  P_over {po:.4f}  P_under {pu:.4f}')
print('\nWhere are the home short-horned seals (share of the site animal seals):')
t=d.groupby('site').agg(n=('id','size'),short=('g',lambda x:(x=='SHORT').sum())); t['pct']=(t.short/t.n*100).round(1); print(t[t.n>=15].sort_values('pct',ascending=False))
coast=['Lothal','Chanhu-daro','Gola Dhoro (Bagasra)','Allahdino','Nausharo','Bala-kot']
c=d.site.isin(coast); tab=[[ (c&(d.g=='SHORT')).sum(),(c&(d.g!='SHORT')).sum()],[(~c&(d.g=='SHORT')).sum(),(~c&(d.g!='SHORT')).sum()]]
print('coast/port sites',coast,tab,fisher_exact(tab,alternative='greater'))
