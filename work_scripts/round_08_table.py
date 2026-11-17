#!/usr/bin/env python3
"""Writes the report table of round seals (one row per object) from work_data/round/round_list.csv. Output: work_data/round/round_table.md"""
import pandas as pd, os
R = '/home/claude/ivc/work_data/round'
L = pd.read_csv(f'{R}/round_list.csv', dtype=str).fillna('')
def clean(x): return '' if x in ('-', '--', '0', '0.0', 'nan') else x
rows = []
for obj, g in L.groupby('obj', sort=False):
    a = g.iloc[0]
    ids = ' / '.join(g.id)
    txt = ' ; '.join(f'`{t}`' for t in g.text)
    find = ' '.join(x for x in [clean(a.area).strip('-'), clean(a.house).strip('-'), clean(a.room).strip('-')] if x) or '-'
    if a.depth not in ('-', '- -', ''): find += f' ({a.depth})'
    tm = a.bin or ' '.join(x for x in [clean(a.period), clean(a.phase)] if x) or '-'
    if a.tier == 'home' and a.period not in ('-', ''): tm = (a.bin + '; ' if a.bin else '') + a.period
    dims = []
    if float(a.horiz_mm) > 0: dims.append(f'{a.horiz_mm} wide')
    if float(a.vert_mm) > 0: dims.append(f'{a.vert_mm} high')
    if clean(a.thick_mm): dims.append(f'thick {a.thick_mm}')
    bp = {'pierced': 'P', 'not pierced': 'N'}.get(a.pierced, 'n/r') + '/' + {'boss': 'B', 'no boss': 'no B'}.get(a.bossed, 'n/r') 
    boss = 'not recorded' if a.boss_code in ('-', '') else bp + f' [{a.boss_code}]'
    note = ' ; '.join(g.photo_note)
    tier = {'home': 'home', 'abroad': 'abroad', 'unknown site': 'unknown site', 'South India': 'S India'}[a.tier]
    rows.append(f"| {ids} | {tier} | {a.site} | {find} | {tm} | {', '.join(dims) or 'not recorded'} | {a.animal.lower() if a.animal else '-'} ({a.symbol if a.symbol not in ('-', '') else 'no symbol'}) | {a.material if a.material != '-' else '-'} | {boss} | {txt} | {note} |")
hdr = '| id | where | site | findspot (area, building, room, depth) | time | size (mm as recorded) | animal (catalogue symbol) | material | pierced / boss | text (reading order) | photo |\n|' + '---|' * 11 + '\n'
open(f'{R}/round_table.md', 'w').write(hdr + '\n'.join(rows) + '\n'); print(len(rows))
