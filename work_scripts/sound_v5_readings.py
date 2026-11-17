#!/usr/bin/env python3
"""Twenty more whole readings (101-120; 81-100 belong to the star-names job), all texts that read start to finish
for the first time in the fifth pass.  Appends a section to READINGS.md after whatever is there (reruns replace only
this section).  English written by hand from the word values.  † = word under test; ‡ = word building on a fact seen
while choosing.  Run after sound_v5_values.py."""
from sound_v5_common import *
from sound_v5_values import V5, TIER5, BASIS5
HEAD = '## Twenty more: texts that read whole for the first time in the fifth pass'
R = [
 ('L', '347-741-176-740-090', 'The Stag of the first ward: agent of the Tax house. A tablet in 8 copies.'),
 ('L', '590-705-868', 'Chest: one kalam, half-share. A store chit in 5 copies (5 more write the kalam with 706).'),
 ('L', '491-817-740-400', 'Junior hand of the Horn-share house.'),
 ('L', '371-390', 'Spindle: cotton. Two seals from Farmana.'),
 ('L', '370-390', 'Spindle: cotton (a tablet).'),
 ('L', '231-176-740-565', 'The warrior of the First-star Tax house.'),
 ('L', '235-555-526', 'Bamboo-star, gate-guard. At Harappa and on a Lothal seal.'),
 ('L', '692-060-240-636-740', 'Of the Assembly: of the High-star Many house.'),
 ('L', '519-740', 'Of the Hedge house. Two seals.'),
 ('L', '388-526', 'The royal guard (a Chanhu-daro seal).'),
 ('L', '920-060-740-031-590-390-161', 'In the month: of the house, one boxed-cotton keeper.'),
 ('L', '838-923-740', 'Of the Produce-and-Ivory house.'),
 ('L', '692-060-798-240-220-520', 'Of the Assembly: Descendant of High-star Star, the chief.'),
 ('L', '140-741-097-161', 'The lady of the first ward: her bondsman, the keeper.'),
 ('L', '692-575-595-820', 'Assembly, fort, forge: a quarter. Seal H-1.'),
 ('L', '861-002-240-495-615-740', 'Two shares: of the High-star Horn-Field house.'),
 ('L', '861-002-032-220-740-565-001-416', 'Two shares: of the Dark-star house, the warrior; one threshed heap.'),
 ('Mu', '692-060-255-435-690-740-692-060-803-740', 'Of the Assembly: of the house allied to the Chief Staff; of the Assembly: of the Home house. A new text, on two seals.'),
 ('Mu', '838-798-176-740-151-700-700-700-390', 'Produce of the Descendant-Tax house, the keeper: cup, cup, cup of cotton. A new-text tag, two copies.'),
 ('Mu', '806-415-220-717-740-705-033-520-097-161', 'Produce: of the servant house of Branch-Star; the three-kalam chief; the bondsman keeper. A new-text seal from Harappa.'),
]
if __name__ == '__main__':
    old = open(f'{ROOT}/READINGS.md').read()
    old = old.split('\n' + HEAD)[0].rstrip() + '\n'
    byt = collections.defaultdict(list)
    for r in d.itertuples():
        if r.complete_txt: byt['-'.join(r.tok)].append(r)
    mu = M[~M.partnered & M.complete_b]
    L = ['', HEAD, '',
         'Added by `work_scripts/sound_v5_readings.py` (fifth list: `jobs/out/sound_list_v5.md`). None of these texts read start to finish before this pass. '
         'New words they rest on: kalai "stag" (347), araikkāṇi "half-share" (868), kompu "horn" (491/495), katir "spindle" (370/371), maṟavaṉ "warrior" (565), kāval "guard" (525/526, variants of 527), '
         'kūṭṭam "assembly" (692), vēli "hedge" (519), kā "keeper" (161), viḷai "produce" (838, the second catalogue draws it as 806), maruppu "tusk, ivory" (923), vaḷḷam "grain measure" (711). '
         'Cotton 390 is read *parutti* (cotton house report). A double dagger (‡) marks a word whose prediction came true on a fact seen while choosing; a dagger (†) a word under test. '
         'Reading order = stored order reversed. "New text" = second catalogue (Mahadevan 1977) text with no partner in the first catalogue, never used to choose a value.', '']
    snd = lambda x: ' '.join(V5[a][0] if a in V5 else '?' for a in x)
    mark = lambda a: '†' if TIER5.get(a) == 'testing' else '‡' if BASIS5.get(a) == 'seen' else ''
    for k, (cat, t, en) in enumerate(R, 101):
        x = t.split('-'); ww = ' · '.join(f'`{a}` {V5[a][0]}{mark(a)} "{V5[a][1]}"' for a in x)
        if cat == 'L':
            rs = byt[t]; r0 = rs[0]
            oid = r0.cisi if r0.cisi not in ('-', '') else f'Lipi row {r0.id}'
            kinds = collections.Counter(f'{r.type} {r.material}' for r in rs); sites = collections.Counter(f'{r.site} ({r._5})' for r in rs)
            head = [f'- Object: {oid}; {len(rs)} object{"s" if len(rs) > 1 else ""} carry this exact text ({", ".join(f"{a} {b}" for a, b in kinds.most_common(3))})',
                    f'- Site and findspot: {", ".join(f"{a} x{b}" for a, b in sites.most_common(4))}']
        else:
            rs = mu[mu.tok.apply(lambda y: '-'.join(y)) == t]
            head = [f'- Object: second catalogue text{"s" if len(rs) > 1 else ""} {", ".join(rs.textnum)} ({", ".join(sorted(set(rs.cls)))}; no partner in the first catalogue)',
                    f'- Site: {", ".join(sorted(set(rs.site_l)))}']
        L += [f'## {k}. {en}', ''] + head + [f'- Signs: `{t}`', f'- Sound: *{snd(x)}*', f'- Word by word: {ww}', '']
    open(f'{ROOT}/READINGS.md', 'w').write(old + '\n'.join(L) + '\n')
    print('READINGS.md: 20 readings appended (101-120)')
