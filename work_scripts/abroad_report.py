#!/usr/bin/env python3
"""Writes jobs/out/abroad_seals.md: tables from data + prose block in abroad_seals_prose.md (same folder as this script)."""
from abroad_orient import *
import os
hs2=hs.copy(); hs2['rd']=hs2.text.apply(rd); call=prof(hs2.rd)
def row(r):
    t=r.rd; n=len([x for x in t if x!='000'])
    core=[x for x in t if x not in MAN]
    l=llr(core,call) if len([x for x in core if x!='000'])>=2 else 0
    ori='home' if l>=1 else 'mirror' if l<=-1 else 'open'
    parts=[]
    # parse
    hf='fits' if (t and t[-1] in CLASS) else ('class-before-lost' if '000' in t and any(x in CLASS for x in t) else 'no')
    ff='fits' if (t and t[0] in MAN) else 'no'
    words=' / '.join(f'{s} {short(s)}' for s in t if s!='000') + (' (+lost)' if '000' in t else '')
    return f'| {r.id} | {r.site} | {d.loc[r.Index,"dir."]} | {r.complete} | `{"-".join(t)}` | {words} | {hf} | {ff} | {ori} ({l:+.1f}) |'
out=[]
for title,c in [('Round seals and cylinders','round'),('Square seals','square'),('Other objects','other')]:
    out.append(f'\n### {title} ({len(ab[ab.cat==c])})\n')
    out.append('| id | site | dir. | complete | reading order | in words | home template (class last) | flipped (man first) | orientation from non-man signs |')
    out.append('|---|---|---|---|---|---|---|---|---|')
    for r in ab[ab.cat==c].itertuples(): out.append(row(r))
tab='\n'.join(out)
prose=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'abroad_seals_prose.md')).read()
open(f'{ROOT}/jobs/out/abroad_seals.md','w').write(prose.replace('@@TABLES@@',tab))
print('written')
