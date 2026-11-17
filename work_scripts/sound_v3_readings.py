#!/usr/bin/env python3
"""Twenty more whole readings on goods objects under the third sound list; appends a section to READINGS.md
(the first forty are left as they are).  Texts chosen from work_data/sound_v3/reading_candidates.csv; the English
for each text is written here by hand from the word values (guesses built on measured slots).  A dagger marks a
word still under test.  Run after sound_v3_values.py and sound_v3_cands.py."""
import re, collections
from sound_v3_common import *
from sound_v3_values import V3, TIER3
NUMW = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight'}
R = [  # text in reading order, English
 ('503-615-752-740', 'Of the house of the heir of Hill-Field: on 29 copper tablets, all at Mohenjo-daro.'),
 ('705-500-741-001-055-220-740-090', 'By ship (kalam pāy, ship-sail), first ward: one dozen fish; the house\'s agent.'),
 ('798-240-845-061-407', 'Descendant of the High-star house: sheaf-bundles, a quarter, the lot.'),
 ('415-220-845-407', 'Branch-Star: sheaf-bundles, the lot.'),
 ('806-231-176-740', 'Produce: of the First-star Tax house.'),
 ('861-368-001-142-617', "Holder of a share: Banner; one, the king's servant."),
 ('142-617-001-004-407', "The king's servant: one; four lots."),
 ('503-463-740', 'Of the Hill-Three-peaks house (on a copper object).'),
 ('540-540', 'A paṟai measure, a paṟai measure: two drum-measures of grain.'),
 ('920-540-740', "The month's paṟai measure, of the house."),
 ('320-920-740', 'Monthly allowance (paṭi tiṅkaḷ), of the house.'),
 ('001-033-415-175-740', 'One; three: of the Branch-Tax house.'),
 ('171-035', 'Full weight: five.'),
 ('413-220-440', 'Grain, fish: received.'),
 ('140-176-740-400', 'Junior hand of the Lady-Tax house (an ivory rod).'),
 ('413-892-824', 'Grain: sale, price. A sale chit, issued in 11 copies.'),
 ('413-575-335-711-033-700', 'Grain of Fort-town (kōṭṭai ūr): measure (vaḷḷam), three cups.'),
 ('413-575-335-740-032-700', 'Grain, of the Fort-town house: two cups.'),
 ('440-100-740', 'Received: of the Elder house (granary area).'),
 ('220-440-154-400', 'Fish received; the carrier, junior hand.'),
]
if __name__ == '__main__':
    old = open(f'{ROOT}/READINGS.md').read()
    old = old.split('\n## Twenty more')[0].rstrip() + '\n'
    byt = collections.defaultdict(list)
    for r in d.itertuples():
        if r.complete_txt: byt['-'.join(r.tok)].append(r)
    L = ['', '## Twenty more: goods objects read under the third sound list', '',
         'Added by `work_scripts/sound_v3_readings.py` (third list: `jobs/out/sound_list_v3.md`). Each text below became fully sounded in this pass because a value it needs moved to "building on" or got its word: '
         'paṭi "ration, allowance" (320), ūr "town" (335), vilai "price" (824), cūṭu "sheaf-bundle" (845), viḷai "produce" (806), malai "hill" (503), vayal "field" (615), kāl "quarter" (061), ūḻiyaṉ "servant" (617), paṟai "drum-measure" (540), niṟai "full weight" (171), koḷ "received" (440), iṟai "tax" (175), ammai "lady" (140), kōṭṭai "great measure; fort" (575). '
         'A dagger (†) marks a word still under test: kalam "ship" (705), nel "grain" (413), vaḷḷam "measure" (711), mīmīn "High-star" (240), kiḷai "lot" (407). Reading order = stored order reversed. Object id, site and findspot are from the first catalogue (Lipi).', '']
    for k, (t, en) in enumerate(R, 41):
        rs = byt[t]; x = t.split('-')
        r0 = rs[0]
        oid = r0.cisi if r0.cisi not in ('-', '') else f'Lipi row {r0.id}'
        kinds = collections.Counter(f'{r.type} {r.material}' for r in rs)
        sites = collections.Counter(f'{r.site} ({r._5})' for r in rs)
        snd = ' '.join(V3[a][0] if a in V3 else '?' for a in x)
        ww = ' · '.join(f'`{a}` {V3[a][0]}{"†" if TIER3.get(a) == "testing" else ""} "{V3[a][1]}"' for a in x)
        L += [f'## {k}. {en}', '', f'- Object: {oid}; {len(rs)} object{"s" if len(rs) > 1 else ""} carry this exact text ({", ".join(f"{a} {b}" for a, b in kinds.most_common(3))})',
              f'- Site and findspot: {", ".join(f"{a} x{b}" for a, b in sites.most_common(4))}',
              f'- Signs: `{t}`', f'- Sound: *{snd}*', f'- Word by word: {ww}', '']
    open(f'{ROOT}/READINGS.md', 'w').write(old + '\n'.join(L) + '\n')
    print('READINGS.md: 20 readings appended (41-60)')
