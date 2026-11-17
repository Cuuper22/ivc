#!/usr/bin/env python3
"""Twenty more whole readings (61-80), all texts that became readable start to finish only in the fourth pass;
appends a section to READINGS.md (entries 1-60 are left as they are).  English written here by hand from the word
values (guesses built on measured slots).  A dagger (†) marks a word under test; a double dagger (‡) marks a word
building on a prediction whose fact had been visible while choosing.  Run after sound_v4_values.py."""
import collections
from sound_v4_common import *
from sound_v4_values import V4, TIER4, BASIS
HEAD = '## Twenty more: texts that became readable in the fourth pass'
R = [
 ('501-405-002-240-520', 'Stock of the kindred, two: High-star the chief. A store chit in 29 copies.'),
 ('255-435-156-400', 'Junior keeper of the chief staff (mutal kōl kā): an office chit in 10 copies.'),
 ('706-033-923-740', 'Three kalam, the crescent-horn: of the house. Seven copper tablets.'),
 ('137-400', 'The cultivator, junior hand: a ration chit in 7 copies.'),
 ('605-760-740-400', 'Junior hand of the house of the heir of the Granary (kutir maka kuṭi).'),
 ('416-861-002', 'Threshed heap: two shares.'),
 ('550-060-690-740', 'Of the allied house of the Gate (vāy-iṉ piṇai kuṭi).'),
 ('005-900-740', 'Five months: of the house.'),
 ('384-740', 'Of the Royal (Pipal) house.'),
 ('004-700-097-400', 'Four cups: the bondsman, junior hand. A ration issue in 4 copies.'),
 ('017-585-388-740', 'Of the Royal house of the Seven Maidens (on copper tablets).'),
 ('717-740-400', 'Junior hand of the Servant house.'),
 ('705-033-520', 'The three-kalam chief.'),
 ('005-706', 'Five kalam (on copper tablets).'),
 ('550-527', 'Gate-guard (vāy kāval).'),
 ('806-233-384-740', 'Produce, scabbard-fish: of the Royal house (on copper tablets).'),
 ('831-892-400', 'Millet: sale. Junior hand.'),
 ('798-231-705-033-904-100-740', 'Descendant of First-star: three kalam, two months; of the Elder house (on copper tablets).'),
 ('798-240-233-320-920-740-400', 'Descendant of the High-star house, fish: monthly allowance; of the house, junior hand.'),
 ('033-590-416', 'Three chests: threshed heap.'),
]
if __name__ == '__main__':
    old = open(f'{ROOT}/READINGS.md').read()
    old = old.split('\n' + HEAD)[0].rstrip() + '\n'
    byt = collections.defaultdict(list)
    for r in d.itertuples():
        if r.complete_txt: byt['-'.join(r.tok)].append(r)
    L = ['', HEAD, '',
         'Added by `work_scripts/sound_v4_readings.py` (fourth list: `jobs/out/sound_list_v4.md`). None of these texts read start to finish before this pass. '
         'New words they rest on: kalam "grain measure" (705/706), kōl "staff" (435), maruppu "crescent horn" (923), vēḷāḷaṉ "cultivator" (137), kutir "granary" (605), turumpu "threshed heap" (416), '
         'vāy "gate" (550), -iṉ "of" (060), tiṅkaḷ "month" (900), aracu "pipal, royal" (384/388), aṭimai "bondsman" (097), aṭi "servant" (717), kāval "guard" (527), vāḷai "scabbard-fish" (233), tiṉai "millet" (831), mīmīn "High-star" (240). '
         'A double dagger (‡) marks a word whose prediction came true on a fact that had been visible while the word was chosen. Reading order = stored order reversed. Object id, site and findspot are from the first catalogue (Lipi).', '']
    for k, (t, en) in enumerate(R, 61):
        rs = byt[t]; x = t.split('-'); r0 = rs[0]
        oid = r0.cisi if r0.cisi not in ('-', '') else f'Lipi row {r0.id}'
        kinds = collections.Counter(f'{r.type} {r.material}' for r in rs)
        sites = collections.Counter(f'{r.site} ({r._5})' for r in rs)
        snd = ' '.join(V4[a][0] if a in V4 else '?' for a in x)
        mark = lambda a: '†' if TIER4.get(a) == 'testing' else '‡' if BASIS.get(a) == 'seen' else ''
        ww = ' · '.join(f'`{a}` {V4[a][0]}{mark(a)} "{V4[a][1]}"' for a in x)
        L += [f'## {k}. {en}', '', f'- Object: {oid}; {len(rs)} object{"s" if len(rs) > 1 else ""} carry this exact text ({", ".join(f"{a} {b}" for a, b in kinds.most_common(3))})',
              f'- Site and findspot: {", ".join(f"{a} x{b}" for a, b in sites.most_common(4))}',
              f'- Signs: `{t}`', f'- Sound: *{snd}*', f'- Word by word: {ww}', '']
    open(f'{ROOT}/READINGS.md', 'w').write(old + '\n'.join(L) + '\n')
    print('READINGS.md: 20 readings appended (61-80)')
