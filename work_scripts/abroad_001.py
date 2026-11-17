from abroad_seals import *
import random
hs=home[home.type.str.startswith('SEAL')].copy(); hs['rd']=hs.text.apply(rd)
def near(t,i,S,k=2): return any(t[j] in S for j in range(max(0,i-k),min(len(t),i+k+1)) if j!=i)
def stat(rows,label):
    n=m=0
    for t in rows:
        for i,s in enumerate(t):
            if s=='001': 
                n+=1; m+=near(t,i,MAN)
    print(label,'001 occurrences',n,'with a man sign within 2:',m)
stat(ab[ab.cat=='round'].rd,'round')
stat(hs.rd,'home')
# base rate: for round seals, fraction of non-001 positions with man within 2
b=[];
for t in ab[ab.cat=='round'].rd:
    for i,s in enumerate(t):
        if s not in('001','000'): b.append(near(t,i,MAN))
print('round base rate man-within-2 for other positions',sum(b),len(b),round(sum(b)/len(b),3))
# permutation: shuffle sign order within each round seal
R=list(ab[ab.cat=='round'].rd); random.seed(1); hits=[]
obs=sum(near(t,i,MAN) for t in R for i,s in enumerate(t) if s=='001')
for _ in range(5000):
    h=0
    for t in R:
        u=t[:]; random.shuffle(u)
        h+=sum(near(u,i,MAN) for i,s in enumerate(u) if s=='001')
    hits.append(h)
print('perm: observed',obs,'mean shuffled',sum(hits)/5000,'P(>=obs)',sum(h>=obs for h in hits)/5000)
# 001 not at edge on round seals?
print('001 at edge (first/last, lost ignored):',sum(1 for t in R for i,s in enumerate([x for x in t if x!='000']) if s=='001' and i in (0,len([x for x in t if x!='000'])-1)))
# segments left/right of 001
for r in ab[ab.cat=='round'].itertuples():
    t=r.rd
    if '001' in t:
        i=t.index('001'); print(r.id,'left',t[:i],'right',t[i+1:])
# man sign + 740 co-occurrence in round
print('round seals with 740:',[r.id for r in ab[ab.cat=='round'].itertuples() if '740' in r.rd],' 740 anywhere abroad:',sum('740' in t for t in ab.rd),'of',len(ab))
print('round seals with man and with 740 in same seal:',sum(1 for t in R if '740' in t and (set(t)&MAN)))
# 090 preceded by 740 at home in complete seals
c=collections.Counter(); 
for t in hs.rd:
    for i,s in enumerate(t):
        if s=='090': c['prev740' if i and t[i-1]=='740' else 'other']+=1
print('home 090',c)
