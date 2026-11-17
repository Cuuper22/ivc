#!/usr/bin/env python3
"""Step 1: for each blamed sign, split every use by slot. Output work_data/odd/slots_census.csv and a printout.
Slot = parser role (name = crest/self/tag; counted = the thing a count stands beside; opener; ending; relation; tail; load).
Also: object kind group (seal / goods), text-final, and the neighbours."""
from odd_common import *
BL = ['904','900','824','840','055','690','806','501','368','152','156','861','060']
BL_ALL = BL + ['151','153','154','155','157','158']
F = faces()
rows = []
for f in F:
    x, R = f['x'], f['roles']
    for i, s in enumerate(x):
        if s in BL_ALL:
            role = R[i]; slot = {'crest':'name','self':'name','tag':'name','lost':'name'}.get(role, role)
            rows.append(dict(sign=s, cat=f['cat'], id=f['id'], kind=f['kind'], grp='seal' if f['kind']=='seal' else 'goods', slot=slot, final=i==len(x)-1, first=i==0,
                             prev=x[i-1] if i else '^', nxt=x[i+1] if i+1<len(x) else '$', n=len(x), text='-'.join(x)))
T = pd.DataFrame(rows); T.to_csv(f'{OUT}/slots_census.csv', index=False)
for s in BL_ALL:
    t = T[T.sign==s]
    if not len(t): continue
    print(f'\n=== {s}: {len(t)} uses ({(t.cat=="Mu").sum()} on new texts); distinct texts {t.text.nunique()}')
    print('  slot x group:', dict(t.groupby(['slot','grp']).size()))
    print('  text-final', int(t.final.sum()), ' first', int(t['first'].sum()))
    print('  prev', t.prev.value_counts().head(6).to_dict()); print('  next', t.nxt.value_counts().head(6).to_dict())
