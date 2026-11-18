"""Counted-thing measurement: for each sign, how often a count sign is right before it (reading order).
Writes work_data/counted/sign_by_count.csv, sign_summary.csv"""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from counted_common import *
rows=load(); sh=shapes()
occ=collections.Counter(); occ1=collections.Counter()   # occurrences, occurrences at pos>=1
tab=collections.defaultdict(collections.Counter)         # sign -> count label -> n
tabD=collections.defaultdict(collections.Counter)        # distinct-text version
after=collections.defaultdict(collections.Counter)       # sign counted -> next sign
seen=set(); aft_cnt=collections.defaultdict(collections.Counter)
for r,toks,broken in rows:
    key=r['text']; first=key not in seen; seen.add(key)
    for i,s in enumerate(toks):
        occ[s]+=1
        if i>=1:
            occ1[s]+=1
            L=label(toks[i-1])
            if L and s not in CNT and s not in('ALT','000'):
                tab[s][L]+=1
                if first: tabD[s][L]+=1
                nxt=toks[i+1] if i+1<len(toks) else 'END'
                after[s][nxt]+=1
        # count AFTER the sign (postposed)
        if i+1<len(toks):
            L=label(toks[i+1])
            if L and s not in CNT: aft_cnt[s][L]+=1
labs=['S1','S2','S3','S4','S5','S6','S7','T2','T3','T4','T5','T6','T7','T8','F1','F2','F3','F4','F5','F6','A']
out=[]
for s in tab:
    n=sum(tab[s].values()); nd=sum(tabD[s].values())
    row=dict(sign=s,shape=sh.get(s,''),occ=occ[s],occ_pos1=occ1[s],counted=n,counted_distinct=nd,rate=round(n/max(occ1[s],1),3),
      after_count=sum(aft_cnt[s].values()))
    for l in labs: row[l]=tab[s].get(l,0)
    row['next']='; '.join(f'{k}:{v}' for k,v in after[s].most_common(4))
    out.append(row)
df=pd.DataFrame(out).sort_values('counted',ascending=False)
df.to_csv(f'{ROOT}/work_data/counted/sign_by_count.csv',index=False)
print(df.head(60)[['sign','shape','occ','counted','counted_distinct','rate','after_count','next']].to_string())
tot=sum(occ1[s] for s in occ1 if s not in CNT); c=df.counted.sum()
print('baseline rate (non-count sign after a count)',c,tot,c/tot)
