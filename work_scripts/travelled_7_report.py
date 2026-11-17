"""Job: the travelled name. Step 7: markdown table of all 71 objects with 590-390 + summary counts for opener/ending. Output: travelled_out/table.md"""
import pandas as pd, collections, os
R='/home/claude/ivc/'
d=pd.read_csv(R+'work_scripts/travelled_out/t590_390.csv',dtype=str,keep_default_na=False)
S=R+'evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images/'
files=os.listdir(S)
def photo(c): return 'yes' if c!='-' and any(f.startswith(c+'_') for f in files) else 'no'
def opener(t):
    s=t.split('-')
    if s[:2]==['920','060'] or s[:2]==['550','060']: return s[0]+'-060 cap'
    if s[0] in('861','817'): return 'diamond'
    if s[0]=='820': return 'wheel'
    if s[0]=='060': return '060-'+s[1]
    return 'none'
def ending(a):
    s=a.split('-') if a else []
    if not s or s==['']: return 'ends on the name'
    return a
rows=[]
d=d.drop_duplicates('object')
lines=['| id | site | type | animal | face mm2 | period / stratum | findspot | reading-order text | opener | after 590-390 | photo |','|---|---|---|---|---|---|---|---|---|---|---|']
for r in d.itertuples():
    fs=' '.join(x for x in [r._asdict()['_28'] if False else '',] if x)
    row=r._asdict()
    area=d.loc[r.Index,'area-section'];bh=d.loc[r.Index,'block-house'];rg=d.loc[r.Index,'room-grid'];dp=d.loc[r.Index,'depth']
    fs=' '.join(x for x in [area,bh,rg,dp] if x not in('--','-','- -',''))
    per=' '.join(x for x in [r.period,r.phase] if x not in('-',''))
    face=f'{float(r.face_mm2):.0f}' if r.face_mm2 not in('',) else ''
    lines.append(f'| {r.cisi if r.cisi!="-" else r.id} | {r.site} | {r.type} | {r.symbol if r.symbol not in ("-","nan","") else ""} | {face} | {per} | {fs} | `{r.reading_order_text}` | {opener(r.reading_order_text)} | `{r.after}` | {photo(r.cisi)} |')
open(R+'work_scripts/travelled_out/table.md','w').write('\n'.join(lines))
print(len(lines)-2,'rows')
op=collections.Counter(opener(t) for t in d.reading_order_text)
print('openers',dict(op))
print('after 590-390',collections.Counter(d.after).most_common(12))
print('animals',collections.Counter(d.symbol).most_common(12))
print('median face',pd.to_numeric(d.face_mm2,errors='coerce').median(), 'n',pd.to_numeric(d.face_mm2,errors='coerce').notna().sum())
sd=d[d.type=='SEAL:S']; print('SEAL:S',len(sd),'median face',pd.to_numeric(sd.face_mm2,errors='coerce').median())
