from abroad_orient import *
call=prof(full.rd) if False else None
import pandas as pd
hs2=hs.copy(); hs2['rd']=hs2.text.apply(rd); call=prof(hs2.rd)
def strip(t): return [x for x in t if x not in MAN]
print('== LLR excluding 090/091, summed by category (positive = home order)')
for catg in ['square','round','other']:
    ls=[]
    for r in ab[ab.cat==catg].itertuples():
        t=strip(r.rd); 
        if len([x for x in t if x!='000'])>=2: ls.append(llr(t,call))
    print(catg,len(ls),'sum',round(sum(ls),2),'home-order',sum(l>0 for l in ls),'mirrored',sum(l<0 for l in ls))
# man sign position home vs abroad (reading order, complete texts of length>=2)
def pos(t,s):
    t=[x for x in t if x!='000']; return [i for i,x in enumerate(t) if x==s],len(t)
for s in ['090','091']:
    print('\n== sign',s)
    for name,df in [('home seals',hs2[hs2.complete=='Y']),('abroad all',ab)]:
        c=collections.Counter()
        for t in df.rd:
            ps,n=pos(t,s)
            if n<2: continue
            for p in ps: c['first' if p==0 else 'last' if p==n-1 else 'mid']+=1
        print(name,dict(c))
    for r in ab.itertuples():
        if s in r.rd: print('  ',r.id,r.site,r.cat,'reading','-'.join(r.rd),' stored',r.text)
# home texts with 091
print('\nhome 091 texts:')
for r in hs2[hs2.rd.apply(lambda t:'091' in t)].itertuples(): print(r.id,r.site,'-'.join(r.rd),r.complete)
