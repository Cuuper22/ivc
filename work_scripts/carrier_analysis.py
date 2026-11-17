import sys,collections as C
sys.path.insert(0,'/home/claude/ivc/work_scripts')
from carrier_load import load
rows=load()
A={f'{i:03d}' for i in range(465,476)}
LC={'151','154','155','156','158'}
def rd(r): return r['toks'][::-1]   # reading order
ph=[r for r in rows if any(rd(r)[i] in A and rd(r)[i+1:i+3][:1]==['806'] and rd(r)[i+2:i+3] and rd(r)[i+2] in LC for i in range(len(rd(r))-2))]
print('phrase objects',len(ph))
print('--- by id family: other rows with same cisi / id prefix')
byc=C.defaultdict(list);byp=C.defaultdict(list)
for r in rows:
    byc[r['cisi']].append(r);byp[r['id'].split('.')[0]].append(r)
for r in ph:
    sibs=[s for s in byp[r['id'].split('.')[0]] if s is not r]
    cs=[s for s in byc[r['cisi']] if s is not r] if r['cisi']!='-' else []
    print(r['id'],r['cisi'],r['type'],r['sides'],'|',r['text'],'| sib:',[(s['id'],s['text']) for s in sibs+cs])
print('--- variants by site/period/size')
for r in ph:
    v=[t for t in rd(r) if t in A][0]
    print(v,r['site'],r['area-section'],r['block-house'],r['room-grid'],r['period'],r['depth'],r['material'],r['type'],r['horizontal(mm)'],r['vertical(mm)'],len(r['toks']))
print('--- before/after 806 (reading order)')
bef=C.Counter();aft=C.Counter();pair=C.Counter();n=0;ends=C.Counter();starts=C.Counter()
for r in rows:
    t=rd(r)
    for i,x in enumerate(t):
        if x=='806':
            n+=1
            bef[t[i-1] if i>0 else '^']+=1; aft[t[i+1] if i+1<len(t) else '$']+=1
            pair[(t[i-1] if i>0 else '^',t[i+1] if i+1<len(t) else '$')]+=1
print('806 total',n);print('before',bef.most_common(25));print('after',aft.most_common(25));print('pairs',pair.most_common(25))
print('--- all sign counts after 806 incl A groups')
ga=sum(v for k,v in aft.items() if k in A);print('A after',ga,'LC after',sum(v for k,v in aft.items() if k in LC))
print('--- what precedes A-variants (reading order), what follows')
b=C.Counter();
for r in rows:
    t=rd(r)
    for i,x in enumerate(t):
        if x in A: b[(t[i-1] if i>0 else '^')]+=1
print('before A',b.most_common())
print('--- other load-carriers: contexts')
for lc in ['151','155','156','154','158']:
    c=C.Counter();c2=C.Counter();m=0
    for r in rows:
        t=rd(r)
        for i,x in enumerate(t):
            if x==lc:
                m+=1;c[t[i-1] if i>0 else '^']+=1;c2[t[i-1] if i>0 else '^']
    print(lc,m,c.most_common(8))
print('--- 845-806 / 235-806 / x-806-LC ')
for r in rows:
    t=rd(r)
    for i,x in enumerate(t):
        if x=='806' and i>0 and t[i-1] not in A and t[i-1]!='-': pass
for r in rows:
    t=rd(r)
    if '806' in t and not (A&set(t)): print(r['id'],r['cisi'],r['site'],r['type'],' '.join(t))
