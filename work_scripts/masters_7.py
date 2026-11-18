"""Part 4: openers by role, city, era; do seals of one X share the opener?"""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from masters_common import *
from collections import Counter
import random, itertools
C=pd.read_csv('/home/antigravity/Cuuper22/ivc/work_data/masters/census.csv',dtype=str,keep_default_na=False)
S=C[C.grp=='seal'].copy()
S['role']=S.noun.map(lambda n:{'none':'owner','090':'man','400':'comb'}.get(n,'other-noun'))
print(pd.crosstab(S.role,S.opener).to_string()); 
ct=pd.crosstab(S.role,S.opener,normalize='index').round(3); print(ct.to_string())
# chi-square owner vs man (opener yes/no)
from math import erf
import numpy as np
def fisher(a,b,c,d):
    from scipy.stats import fisher_exact; return fisher_exact([[a,b],[c,d]])
for r in ['man','comb','other-noun']:
    a=S[S.role==r]; o=S[S.role=='owner']
    print(r,'with opener',(a.opener!='none').sum(),'/',len(a),' owners',(o.opener!='none').sum(),'/',len(o),'fisher p',fisher((a.opener!='none').sum(),(a.opener=='none').sum(),(o.opener!='none').sum(),(o.opener=='none').sum())[1])
# by site (owner seals)
big=['Mohenjo-daro','Harappa','Lothal','Dholavira','Kalibangan']
print(pd.crosstab(S[S.site.isin(big)].site,S[S.site.isin(big)].opener,normalize='index').round(2).to_string())
print(pd.crosstab(S[S.site.isin(big)].site,S[S.site.isin(big)].role).to_string())
# by period at Harappa and Mohenjo
for st in ['Harappa','Mohenjo-daro']:
    h=S[S.site==st]; print(st,pd.crosstab(h.period,h.opener).to_string())
# X-sharing agreement for owner seals: pairs of seals with identical X: same opener?
def agree(df):
    g=df.groupby('X'); pairs=same=0; ops=[]
    for x,d in g:
        l=list(d.opener)
        for a,b in itertools.combinations(l,2): pairs+=1; same+=(a==b)
        ops+=l
    # chance: shuffle openers over all seals
    return pairs,same,ops
for name,df in [('owner',S[S.role=='owner']),('all-with-jar',S)]:
    pairs,same,ops=agree(df); 
    sims=[]
    for _ in range(300):
        sh=df.copy(); sh['opener']=random.sample(list(df.opener),len(df)); sims.append(agree(sh)[1])
    print(name,'pairs of seals with same X',pairs,'same opener',same,'chance',np.mean(sims),'max',max(sims))
# opener type counts of the 060-920 cap by role
print(S[S.opener=='060-920'].groupby('role').size())
print(S[S.opener=='060-920'].site.value_counts().head())
