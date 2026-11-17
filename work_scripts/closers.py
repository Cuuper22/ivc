# Do the closing signs of seal texts (jar, spear, person, comb, load-carrier) go with something in the world:
# the animal on the seal, the seal's size, the site?  Reading order = reverse of stored order.
import csv,re,collections,math,random
import numpy as np
random.seed(41)
r=list(csv.DictReader(open('research/data/open_prototype/lipi/metadata_filtered.csv',encoding='utf-8')))
G={'740':'jar','520':'spear','090':'person','400':'comb','151':'carrier','154':'carrier','156':'carrier','158':'carrier','155':'carrier','527':'hatched box','407':'tree','226':'fish+4'}
rows=[]
for x in r:
    if not x['type'].startswith('SEAL'): continue
    t=re.findall(r'\d{3}',x['text'])
    if len(t)<2 or t[0]=='000': continue
    c=G.get(t[0])            # stored-first = reading-last
    if not c: continue
    an=re.sub(r'[:\d].*','',x['symbol']) or 'None'
    try: h=float(x['horizontal(mm)']); v=float(x['vertical(mm)'])
    except: h=v=0
    rows.append((c,an,h*v if h>0 and v>0 else None,x['site'],len(t)))
print('seals with a known closer:',len(rows)); print(collections.Counter(z[0] for z in rows))
def table(idx,name,minn=25):
    cl=[z[0] for z in rows]; val=[z[idx] for z in rows]
    cc=collections.Counter(cl); vc=collections.Counter(val); n=len(rows)
    obs=collections.Counter(zip(cl,val))
    chi=sum((obs[(a,b)]-cc[a]*vc[b]/n)**2/(cc[a]*vc[b]/n) for a in cc for b in vc if cc[a]*vc[b]/n>=3)
    null=[]
    for t in range(2000):
        sv=val[:]; random.shuffle(sv); o=collections.Counter(zip(cl,sv))
        null.append(sum((o[(a,b)]-cc[a]*vc[b]/n)**2/(cc[a]*vc[b]/n) for a in cc for b in vc if cc[a]*vc[b]/n>=3))
    print(f'\ncloser x {name}: association score {chi:.1f}, shuffles average {np.mean(null):.1f}, P {(1+sum(x>=chi for x in null))/2001:.4f}')
    for a in cc:
        if cc[a]<minn: continue
        out=[]
        for b,_ in vc.most_common(8):
            e=cc[a]*vc[b]/n
            if e>=3 and abs(obs[(a,b)]-e)/math.sqrt(e)>=2: out.append(f'{b} {obs[(a,b)]} (expected {e:.1f})')
        print(f'  {a:10s} n={cc[a]:4d}  stands out: '+('; '.join(out) or '-'))
table(1,'animal'); table(3,'site')
print('\nseal face area by closer (mm2, median) and text length:')
for a,_ in collections.Counter(z[0] for z in rows).most_common():
    A=[z[2] for z in rows if z[0]==a and z[2]]; L=[z[4] for z in rows if z[0]==a]
    if len(A)>=10: print(f'  {a:10s} seals with size {len(A):4d}  median area {np.median(A):7.0f}  median signs {np.median(L):.0f}')
