#!/usr/bin/env python3
"""SPOTS lead 1, rescue for (d): the manager's own stand-letter profile, and stand letter by master within trench.
Plain words: STAND LETTER = W/J/S/I/L after the colon on unicorn seals. Idea 1 (redesign): compare the share of each
letter among managers with the share among all unicorn seals of the same city (is a manager's stand a special set?).
Idea 2 (new): do two managers of the SAME master share the stand letter, and does a manager's letter equal the letter
of the master's seal with the same full name (exact master name, not just crest)?
PREDICTION: W (the large-format stand) is over-represented among managers because managers' seals are big.
Writes work_data/spots/s1b_log.txt.
"""
import pandas as pd, numpy as np, collections
ROOT='/home/antigravity/Cuuper22/ivc'; OUT=f'{ROOT}/work_data/spots'
LOG=open(f'{OUT}/s1b_log.txt','w')
def say(*a):
    s=' '.join(str(x) for x in a); print(s,flush=True); LOG.write(s+'\n')
A=pd.read_csv(f'{ROOT}/work_data/registry/names_all.csv',dtype=str).fillna('')
A=A[(A.damaged=='False')&(A.goods_line=='False')&(A.kind=='seal')].drop_duplicates('object_id')
A['mm2']=pd.to_numeric(A.hmm,errors='coerce')*pd.to_numeric(A.vmm,errors='coerce')
A['ag']=A.ending.str.startswith("X's man")
U=A[A.stand.isin(list('WJSIL'))]
for city in ('Mohenjo-daro','Harappa'):
    u=U[U.site==city]; m=u[u.ag]
    say(f'{city}: unicorn seals with a stand letter {len(u)}, managers among them {len(m)}')
    say('   managers:',dict(m.stand.value_counts()),' all:',{k:f'{v/len(u):.0%}' for k,v in u.stand.value_counts().items()})
# managers of the same master: same stand letter?
m=U[U.ag]; same=diff=0
for k,g in m.groupby('name_core'):
    s=list(g.stand)
    for i in range(len(s)):
        for j in range(i+1,len(s)): same+=s[i]==s[j]; diff+=s[i]!=s[j]
say(f'pairs of managers with the same master name: same letter {same}, different {diff}')
# exact master name: master's own seal with same name_core
own=A[~A.ag]
for _,r in m.iterrows():
    mt=own[(own.name_core==r.name_core)]
    if len(mt): say('  ',r.cisi,r.stand,'| master-name seals:',', '.join(f'{x.cisi}:{x.stand or "-"}' for _,x in mt.iterrows()))
# size explains letter?
say('median face mm2 by stand letter (all unicorn seals, Mohenjo-daro):',{k:int(v) for k,v in U[U.site=='Mohenjo-daro'].groupby('stand').mm2.median().items()})
LOG.close()
