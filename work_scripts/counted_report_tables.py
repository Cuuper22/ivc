"""Make the markdown tables used in jobs/out/counted_things.md (all numbers from the CSVs in work_data/counted)."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from counted_common import *
sh=shapes()
raw=pd.read_csv(f'{ROOT}/work_data/counted/sign_by_count.csv',dtype={'sign':str})
rawn=dict(zip(raw.sign,raw.counted))
res=pd.read_csv(f'{ROOT}/work_data/counted/instances_resolved.csv',dtype=str,keep_default_na=False)
rows=load(); occ=collections.Counter(s for r,t,b in rows for s in t)
fol=lambda x:'END' if x=='END' else 'carrier' if x in CARR else 'jar' if x in('740','741') else 'comb' if x=='400' else 'count' if x in CNT else 'other'
order=['S1','S2','S3','S4','S5','S6','S7','T3','T4','T5','T6','T7','T8','F1','F2','F3','F4','F5','F6','A']
def tab(frame,minn):
    X=res[res.frame==frame].drop_duplicates(['id','sign','cs','pos'])
    L=['| sign | shape | occ | raw adj. | owned | counts (value:n) | followed by |','|---|---|---|---|---|---|---|']
    for s,g in sorted(X.groupby('sign'),key=lambda x:-len(x[1])):
        if len(g)<minn: continue
        v=g['count'].value_counts(); cs=' '.join(f'{k}:{v[k]}' for k in order if k in v)
        f=(g.nxt if frame=='B' else g.nxt2).map(fol).value_counts()
        fs=', '.join(f'{k} {x}' for k,x in f.head(3).items())
        L.append(f'| {s} | {sh.get(s,"")[:48]} | {occ[s]} | {rawn.get(s,"") if frame=='B' else ""} | {len(g)} | {cs} | {fs} |')
    return '\n'.join(L)
open('/tmp/tabB.md','w').write(tab('B',8)); open('/tmp/tabA.md','w').write(tab('A',8))
print(open('/tmp/tabB.md').read()[:200])
