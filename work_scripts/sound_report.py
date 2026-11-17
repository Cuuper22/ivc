#!/usr/bin/env python3
"""Builds the tables of jobs/out/sound_list.md from work_data/sound/*.csv and sound_values.VALUES.
Prose sections are in this file; tables are filled from the CSVs."""
import pandas as pd, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_values import VALUES
ROOT = '/home/claude/ivc'; S = f'{ROOT}/work_data/sound'
prof = pd.read_csv(f'{S}/profile.csv', dtype=str).fillna('').set_index('sign')
chk = pd.read_csv(f'{S}/checks.csv', dtype=str).fillna('').set_index('sign')
rd = pd.read_csv(f'{S}/readable_names.csv', dtype=str).fillna('')
SEEN = {'798', '407', '892', '850', '845', '790', '335', '630', '095', '645', '540', '636', '711', '824', '167', '820', '061', '920', '742', '745', '055', '838', '615', '500'}
def slot(s):
    if s not in prof.index: return ''
    p = prof.loc[s]; return f"{p.roles}; in names {p.namepos}" + (f"; counts {p.countbefore}" if p.countbefore else '')
def world(s):
    if s not in prof.index: return ''
    p = prof.loc[s]; w = [p.groups.split(';')[0], p.enr_animal.split(';')[0], p.enr_area.split(';')[0]]
    return '; '.join(x for x in w if x) + (f'; seal face {p.seal_face_med} mm2' if p.seal_face_med else '')
rows = ['| sign | picture | slot (measured) | world (measured) | picture word (DEDR) | job word (DEDR) | sound | English | check | result |', '|---|---|---|---|---|---|---|---|---|---|']
for s, pic, pw, jw, snd, gl, kind, t in VALUES:
    c = chk.loc[s] if s in chk.index else None
    res = f"{c.came_true}{' (seen while choosing)' if s in SEEN else ''}: {c.result}" + (f", P {c.p}" if c is not None and c.p else '') if c is not None else ''
    rows.append(f"| {s} | {pic} | {slot(s)} | {world(s)} | {pw} | {jw} | **{snd}** | {gl} | {c.prediction if c is not None else ''} | {res} |")
open(f'{S}/table.md', 'w').write('\n'.join(rows))
nm = ['| name | read | English | objects | sites | example |', '|---|---|---|---|---|---|'] + [f"| {r['name']} | {r.read} | {r.gloss} | {r.objects} | {r.sites} | {r.example} |" for _, r in rd.iterrows()]
open(f'{S}/names_table.md', 'w').write('\n'.join(nm))
ct = chk.came_true.value_counts().to_dict()
fresh = chk[~chk.index.isin(SEEN)]
print('all', ct, '| fresh', fresh.came_true.value_counts().to_dict(), len(fresh))
