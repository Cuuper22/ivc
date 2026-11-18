import re,sys,collections as C
sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from carrier_load import load
rows=load()
pat=re.compile(r'(?<!\d)4(6[5-9]|7[0-5])(?!\d)')
allA=[r for r in rows if pat.search(r['text'])]
print(len(allA),[ (r['id'],r['cisi'],r['text']) for r in allA if not any(t in {f'{i}' for i in range(465,476)} for t in r['toks'])])
A={str(i) for i in range(465,476)}
LC={'151','154','155','156','158'}
ph=[]
for r in rows:
    t=r['toks'][::-1]
    for i in range(len(t)-2):
        if t[i] in A and t[i+1]=='806' and t[i+2] in LC: ph.append((r,t[i],t[i+2],i,len(t)));break
print('phrase',len(ph))
print('variant x type'); c=C.Counter((v,r['type'].split(':')[0]) for r,v,l,i,n in ph)
for v in sorted(A): print(v,{k[1]:x for k,x in c.items() if k[0]==v}, 'LC',dict(C.Counter(l for r,vv,l,i,n in ph if vv==v)),'site',dict(C.Counter(r['site'][:3] for r,vv,l,i,n in ph if vv==v)))
print('alone (len3 or 4 with 400):',sum(1 for r,v,l,i,n in ph if n<=4), ' as ending of longer:',sum(1 for r,v,l,i,n in ph if n>4), 'phrase at text end in reading order:',sum(1 for r,v,l,i,n in ph if i+3==n))
print('phrase starts text:',sum(1 for r,v,l,i,n in ph if i==0))
# position of phrase for longer seals: what precedes (reading order)
for r,v,l,i,n in ph:
    t=r['toks'][::-1]
    if i>0: print('prefix',r['cisi'],' '.join(t[:i]),'|',' '.join(t[i:]))
# tablet 400 tail
tb=[(r,v,l) for r,v,l,i,n in ph if r['type'].startswith('TAB')]
print('tablets',len(tb),'with 400 tail',sum(1 for r,v,l in tb if r['toks'][0]=='400'))
# 158 vs 154 by type
print(C.Counter((l,r['type'].split(':')[0]) for r,v,l,i,n in ph))
# base rates of tablet phrases among all TAB:B
tbs=[r for r in rows if r['type']=='TAB:B'];print('TAB:B total',len(tbs),'with 806',sum('806' in r['toks'] for r in tbs),'with phrase',sum(1 for r in tbs if any(r is p[0] for p in ph)))
# Harappa tablets period field
for r in ph:
    pass
print('Harappa period values among phrase:',C.Counter(r[0]['period'] for r in ph if r[0]['site']=='Harappa'))
print('site totals for phrase',C.Counter(r[0]['site'] for r in ph))
print('Harappa share of all rows with 806:',C.Counter(r['site'] for r in rows if '806' in r['toks']).most_common(5))
print('Harappa share all rows:',C.Counter(r['site'] for r in rows).most_common(4))
print('Harappa area:',C.Counter(r[0]['area-section'] for r in ph if r[0]['site']=='Harappa'))
print('Harappa area ALL:',C.Counter(r['area-section'] for r in rows if r['site']=='Harappa').most_common(8))
print('round seals abroad A?',[(r['id'],r['text']) for r in allA if r['shape'] in('circular','round')])
