"""A count sitting between two signs may belong to the left sign (X n) or the right sign (n Y).
Estimate each sign's attraction to a count on either side from the data (EM, fractional ownership), then give each
count to the side with more ownership. Output: work_data/counted/instances_resolved.csv (same format as instances.csv,
only owned adjacencies) and owner_rates.csv."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from counted_common import *
inst=pd.read_csv(f'{ROOT}/work_data/counted/instances.csv',dtype=str,keep_default_na=False)
rows=load()
occ=collections.Counter(s for r,t,b in rows for s in t)
# collect count-run slots: (row idx, run start, run end, left sign idx, right sign idx)
slots=[]
for ri,(r,t,b) in enumerate(rows):
    i=0
    while i<len(t):
        if t[i] in CNT:
            j=i
            while j+1<len(t) and t[j+1] in CNT: j+=1
            L=i-1 if i>=1 and t[i-1] not in CNT and t[i-1] not in('ALT','000') else None
            R=j+1 if j+1<len(t) and t[j+1] not in CNT and t[j+1] not in('ALT','000') else None
            slots.append((ri,i,j,L,R)); i=j+1
        else: i+=1
ownA=collections.defaultdict(float); ownB=collections.defaultdict(float)   # ownA[s]: counts owned as "s n"; ownB[s]: "n s"
# init: unambiguous slots owned fully, ambiguous split 50/50
w=[]
for (ri,i,j,L,R) in slots:
    if L is not None and R is not None: w.append(0.5)
    elif R is not None: w.append(0.0)
    else: w.append(1.0)
def tally():
    A=collections.defaultdict(float);B=collections.defaultdict(float)
    for (ri,i,j,L,R),x in zip(slots,w):
        t=rows[ri][1]
        if L is not None: A[t[L]]+=x
        if R is not None: B[t[R]]+=(1-x)
    return A,B
for it in range(30):
    A,B=tally()
    for k,(ri,i,j,L,R) in enumerate(slots):
        if L is not None and R is not None:
            t=rows[ri][1]
            a=(A[t[L]]+0.05)/(occ[t[L]]+1); b=(B[t[R]]+0.05)/(occ[t[R]]+1)
            w[k]=a/(a+b)
A,B=tally()
pd.DataFrame([dict(sign=s,occ=occ[s],owned_after=round(A.get(s,0),1),owned_before=round(B.get(s,0),1)) for s in occ if A.get(s,0)+B.get(s,0)>=5]).sort_values('owned_before',ascending=False).to_csv(f'{ROOT}/work_data/counted/owner_rates.csv',index=False)
keep=set()
for k,(ri,i,j,L,R) in enumerate(slots):
    t=rows[ri][1]; x=w[k]
    if L is not None and R is not None:
        if x>=0.5: keep.add((ri,L,'A'))
        else: keep.add((ri,R,'B'))
    elif L is not None: keep.add((ri,L,'A'))
    elif R is not None: keep.add((ri,R,'B'))
rid={r['id']:ri for ri,(r,t,b) in enumerate(rows)}
m=[(rid[x.id],int(x.pos),x.frame) in keep for x in inst.itertuples()]
res=inst[m]
res.to_csv(f'{ROOT}/work_data/counted/instances_resolved.csv',index=False)
print('raw adjacencies',len(inst),'owned',len(res)); print(res.frame.value_counts().to_dict())
