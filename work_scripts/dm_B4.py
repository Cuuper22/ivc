"""B4: additive count groups (two count signs in a row) before/after a sign; what takes them; cup especially."""
import warnings; warnings.filterwarnings('ignore')
from dm_common import *
d=load()
grp=collections.defaultdict(list)
for r in d.itertuples():
    t=r.toks
    i=0
    while i<len(t):
        if t[i] in CNT:
            j=i
            while j<len(t) and t[j] in CNT: j+=1
            run=t[i:j]
            if len(run)>=2:
                before=t[i-1] if i>0 else 'START'; after=t[j] if j<len(t) else 'END'
                grp[tuple(run)].append((r.cisi,r.type,r.site,before,after,' '.join(t)))
            i=j
        else: i+=1
rows=sorted(grp.items(),key=lambda kv:-len(kv[1]))
print('runs of >=2 count signs:',sum(len(v) for v in grp.values()))
for run,v in rows[:30]:
    labs='+'.join(lab(x) for x in run)
    nb=collections.Counter(x[3] for x in v).most_common(3); na=collections.Counter(x[4] for x in v).most_common(3)
    print(labs,len(v),'before',nb,'after',na)
print('\nruns touching the cup (700):')
for run,v in rows:
    for x in v:
        if x[3]=='700' or x[4]=='700': print(' ','+'.join(lab(y) for y in run),x[0],x[1],x[5])
