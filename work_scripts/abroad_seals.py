#!/usr/bin/env python3
"""Round-seal / abroad analysis. Run: python3 abroad_seals.py  (prints everything used in jobs/out/abroad_seals.md)
Reading order = stored text reversed."""
import re, collections, math, itertools
import pandas as pd
ROOT='/home/claude/ivc'
d=pd.read_csv(f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv',dtype=str).fillna('')
sh=pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv',dtype=str).set_index('lipi_wells_number')['shape_description'].to_dict()
st=pd.read_csv(f'{ROOT}/work_data/slot_table.csv',dtype=str)
ABROAD_REG={'Persian Gulf','Mesopotamia','Iranian Plateau','Central Asia'}
isab=d.region.isin(ABROAD_REG)|((d.site=='Unknown')&(d.type=='SEAL:C'))
def sg(t): return re.findall(r'\d{3}',t)
def rd(t):  # reading order
    return sg(t)[::-1]
ab=d[isab].copy()
def cat(r):
    if r.type in('SEAL:C','SEAL:CY'): return 'round'
    if r.type in('SEAL:S','SEAL'): return 'square'
    return 'other'
ab['cat']=ab.apply(cat,axis=1)
ab['rd']=ab.text.apply(rd)
home=d[~isab&(d.region!='Other')]
# class set: signs last (reading) in >=50% of >=15 texts
CLASS={r.sign for r in st.itertuples() if float(r.last)>=0.5 and int(r.texts)>=15}
CLASS|={'090'}
OPEN={'861','817','820','060','920','692'}
MAN={'090','091'}
def short(s):
    return (sh.get(s,'?').split(',')[0])[:28]
def words(toks): return ' | '.join(f'{s} {short(s)}' for s in toks)
def home_fit(t):
    t=[x for x in t if x!='000']; 
    if not t: return 'none'
    return 'class-last' if t[-1] in CLASS else 'no'
def flip_fit(t):
    return 'man-first' if t and t[0] in MAN else 'no'
if __name__=='__main__':
    print('CLASS set',sorted(CLASS))
    for c in ['round','square','other']:
        print('\n=====',c)
        for r in ab[ab.cat==c].itertuples():
            t=r.rd; rev=t[::-1]
            print(f'{r.id:7} {r.site:18} {r.region:15} {r.type:7} dir={r._asdict()["_25"] if False else d.loc[r.Index,"dir."]:4} cmp={r.complete} | reading: {"-".join(t)} | home:{home_fit(t)} flip:{flip_fit(t)} | reversed-text home:{home_fit(rev)}')
    # does dir. L/R change stored orientation at home? jar position by dir.
    hs=home[home.type.str.startswith('SEAL')&(home.complete=='Y')]
    for dr,g in hs.groupby('dir.'):
        tt=[rd(x) for x in g.text if rd(x)]
        if len(tt)>=20: print('home dir',dr,len(tt),'last in CLASS',sum(x[-1] in CLASS for x in tt),'first in CLASS',sum(x[0] in CLASS for x in tt))
    ab_dir=ab.groupby(['cat','dir.']).size()
    print(ab_dir)
