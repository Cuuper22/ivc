"""Build one row per (count sign, counted sign) adjacency, both frames, with metadata.
frame=B: count right before the sign (n X); frame=A: count right after (X n).
Output work_data/counted/instances.csv (rows) and rows.csv (one per object with token list)."""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from counted_common import *
rows=load(); inst=[]; objs=[]
seen=set()
meta=['id','cisi','site','area-section','block-house','material','type','symbol','period','shape','horizontal(mm)','vertical(mm)','sides','class','text']
for r,toks,broken in rows:
    first=r['text'] not in seen; seen.add(r['text'])
    objs.append(dict(id=r['id'],read=' '.join(toks),n=len(toks),first=first))
    for i,s in enumerate(toks):
        if s in CNT or s in('ALT','000'): continue
        for frame,j in(('B',i-1),('A',i+1)):
            if 0<=j<len(toks) and label(toks[j]):
                d={m:r[m] for m in meta}
                try: area=float(r['horizontal(mm)'])*float(r['vertical(mm)'])
                except: area=0
                d.update(sign=s,frame=frame,count=label(toks[j]),series=CNT[toks[j]][0],value=CNT[toks[j]][1],cs=toks[j],
                  pos=i,n=len(toks),atstart=(j==0 if frame=='B' else False),
                  nxt=toks[i+1] if i+1<len(toks) else 'END',prv=toks[i-2] if frame=='B' and i>=2 else ('START' if frame=='B' else toks[i-1] if i>=1 else 'START'),
                  nxt2=toks[i+2] if i+2<len(toks) else 'END',first=first,broken=broken,area=area)
                inst.append(d)
pd.DataFrame(inst).to_csv(f'{ROOT}/work_data/counted/instances.csv',index=False)
pd.DataFrame(objs).to_csv(f'{ROOT}/work_data/counted/objs.csv',index=False)
print(len(inst))
