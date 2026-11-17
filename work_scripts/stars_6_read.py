#!/usr/bin/env python3
"""Step 5: seals that carry a number + fish star name, read whole with the current sound values (values_v4)
plus the star words of this job. Prints candidates (every sign has a value) for READINGS.md.
"""
from stars_common import *
V = pd.read_csv(f'{ROOT}/work_data/sound_v4/values_v4.csv', dtype=str).fillna('')
VAL4 = {r.sign: (r.sound, r.english) for r in V.itertuples()}
# star words of this job (number form + fish -> sound, English)
STARW = {'tall2+220': ('iru-mīn', 'Dark-star (two-star)'), 'tall2+226': ('iru-mīn', 'Dark-star (caged drawing)'),
         'short2+220': ('iru-mīn', 'Dark-star'), 'short3+220': ('mum-mīn', 'Mrigashira, the Three-star'),
         'tall3+220': ('mum-mīn', 'Three-star'), 'stacked6+220': ('aṟu-mīn', 'Pleiades'), 'short6+220': ('aṟu-mīn', 'Pleiades'),
         'stacked7+220': ('eḻu-mīn', 'Great Bear'), 'short4+220': ('nāṇ-mīn', 'the Asterism'), 'stacked4+220': ('nāṇ-mīn', 'the Asterism'),
         'tall4+220': ('nāṇ-mīn', 'the Asterism'), 'tall1+220': ('or-mīn', 'Lone-star'), 'short1+220': ('or-mīn', 'Lone-star')}
for f in ('231', '233', '235', '236', '240', '241'):
    if f in VAL4: STARW[f'short2+{f}'] = (f'iru {VAL4[f][0]}', f'two {VAL4[f][1]}')
print('marked fish values:', {f: VAL4.get(f) for f in ('231', '233', '235', '236', '240', '241', '226', '220')})
out = []; seen = set()
for cat in ('L', 'Mu'):
    U = all_units(cat); U = U[(U.kind == 'seal') & U.nxt.isin(FISHALL)]
    for _, u in U.iterrows():
        if u.text in seen: continue
        x = u.text.split('-'); comp = f"{u['style']}{u.value}+{u.nxt}"
        if comp not in STARW or '000' in x or 'ALT' in x: continue
        words = []; ok = True; q = 0
        while q < len(x):
            if q == u.i: words.append((x[u.i:u.j + 2], STARW[comp])); q = u.j + 2; continue
            s = x[q]
            if s in VAL4 and VAL4[s][0]: words.append(([s], VAL4[s]))
            elif s in NUMS: words.append(([s], (WORD.get(CNT[s][1], '?'), str(CNT[s][1]))))
            else: ok = False; words.append(([s], ('?', '?')))
            q += 1
        seen.add(u.text)
        out.append(dict(cat=cat, cisi=u.cisi, site=u.site, text=u.text, comp=comp, slot=u.slot, complete=ok,
                        sound=' '.join(w[1][0] for w in words), gloss=' · '.join(f"`{'-'.join(w[0])}` {w[1][0]} \"{w[1][1]}\"" for w in words)))
O = pd.DataFrame(out); O.to_csv(f'{OUTS}/star_seal_readings.csv', index=False)
print(len(O), 'seal texts with a star word;', int(O.complete.sum()), 'read whole')
for _, r in O[O.complete].iterrows(): print(r['cat'], r.cisi, r.site, r.text, r.comp, r.slot, '|', r.sound)
