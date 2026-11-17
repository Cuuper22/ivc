#!/usr/bin/env python3
"""Twenty whole readings 141-160 (seventh list, work_data/values_master4.csv): texts that read whole for the first time in
this pass. Appends a section to READINGS.md (reruns replace only this section). † = word under test; ‡ = wide word (its
came-true fact had been seen while choosing). Run after sound_v7_master.py."""
from sound_v7_common import *
_V, _S, _W = load_values()
V6 = {s: (a, (e or b)) for s, a, b, e in zip(_V.sign, _V.sound, _V.english, _V.english_long)}
_st = dict(zip(_V.sign, _V.status))
TIER6 = {s: ('testing' if st == 'testing' else 'building') for s, st in _st.items()}
BASIS6 = {s: ('seen' if st == 'wide' else 'fresh') for s, st in _st.items()}
HEAD = '## Twenty more: texts opened by the seventh pass'
R = [
 ('L', '104-645-590-235-240-740-090', 'Agent of the Bamboo-star High-star house of the goldsmith\'s gold-weight chest.', ''),
 ('C', '235-233-222-740', 'Of the Bamboo-star Scabbard-fish Shut-in-fish house.', 'a rhinoceros'),
 ('L', '817-002-048-740', 'Two shares: of the house of the Seven.', ''),
 ('L', '705-167', 'Kalam as wages.', ''),
 ('L', '027-032-740-400', 'Junior of the Nine-Two house.', ''),
 ('L', '098-400', 'The junior attendant.', ''),
 ('L', '003-700-900-165', 'Three cups; month and day.', ''),
 ('L', '692-060-240-603-740', 'Of the Assembly: of the High-star Store house.', ''),
 ('L', '792-740-090', 'Agent of the Royal house.', ''),
 ('L', '820-002-554-526', 'Two quarters: the threshing-floor guard.', ''),
 ('L', '240-921-070-520', 'High-star, chief of bow and arrow.', ''),
 ('L', '495-460-520', 'Horn of Three-peaks, chief.', ''),
 ('L', '692-060-798-415-220-554-740', 'Of the Assembly: of the Threshing-floor house of the Descendant of Branch-Star.', ''),
 ('L', '838-798-176-740-151-697-390', 'Keeper of the Produce-Descendant Tax house: woven cotton.', ''),
 ('L', '817-002-220-520-621', 'Two shares: the Star chief; stored.', ''),
 ('L', '820-002-844-390-621', 'Two quarters: sheaves of cotton, stored.', ''),
 ('L', '201-060-032-590-390-740', 'In the rain season: of the Two-Boxed-cotton house.', ''),
 ('L', '003-645-032-590', 'Three lots of two gold weights; the chest.', ''),
 ('L', '595-706-243-617', 'Forge, Ship, Carp: the king\'s servant.', ''),
 ('L', '920-060-741-005-368-705-167', 'In the month, first ward: five banners; kalam as wages.', ''),
]
if __name__ == '__main__':
    old = open(f'{ROOT}/READINGS.md').read()
    old = old.split('\n' + HEAD)[0].rstrip() + '\n'
    byt = collections.defaultdict(list)
    for r in d.itertuples():
        if r.complete_txt: byt['-'.join(r.tok)].append(r)
    mu = M[~M.partnered & M.complete_b]
    L = ['', HEAD, '',
         'Added by `work_scripts/sound_v7_readings.py` (seventh list: `jobs/out/sound_list_v7.md`, `work_data/values_master4.csv`). Every text below read whole for the first time in this pass. '
         'New words they rest on: kar̤añcu "gold weight" (645), aṭaimīn "Shut-in-fish" (222), er̤uvar "the Seven" (048), kūli "wages" (167), toṇṭu "nine" (027), ēvalaṉ "attendant" (098), nāḷ "day" (165), '
         'kūṭu "store" (603), aracu "royal" (792), kaḷam "threshing floor" (554), vil "bow" (921), mukkōṭu "Three-peaks" (460), ney "woven" (697), aṭai "stored" (621), kār "rain season" (201), kayal "carp" (243); '
         'and the measure rule of this pass: an uncounted kalam inside a name is "Ship" (706 in reading 159). '
         'A dagger (†) marks a word under test, a double dagger (‡) a word whose fact was seen while choosing. Reading order = stored order reversed. '
         '"New text" = second-catalogue (Mahadevan 1977) text with no partner in the first catalogue.', '']
    snd = lambda x: ' '.join(V6[a][0] if a in V6 else '?' for a in x)
    mark = lambda a: '†' if TIER6.get(a) in ('testing', 'paused') else '‡' if BASIS6.get(a) == 'seen' else ''
    for k, (cat, t, en, pic) in enumerate(R, 141):
        x = t.split('-'); ww = ' · '.join(f'`{a}` {V6[a][0]}{mark(a)} "{V6[a][1]}"' for a in x)
        if cat in ('L', 'C'):
            rs = byt[t]; ids = [r.cisi for r in rs if r.cisi not in ('-', '')]
            kinds = collections.Counter(f'{r.type} {r.material}' for r in rs); sites = collections.Counter(f'{r.site} ({r._5})' for r in rs)
            head = [f'- Object{"s" if len(rs) > 1 else ""}: {", ".join(ids[:8]) or "Lipi row " + rs[0].id}{" ..." if len(ids) > 8 else ""}; {len(rs)} object{"s" if len(rs) > 1 else ""} carry this exact text ({", ".join(f"{a} {b}" for a, b in kinds.most_common(3))})',
                    f'- Site and findspot: {", ".join(f"{a} x{b}" for a, b in sites.most_common(4))}']
            if cat == 'C': head.append(f'- Picture: {pic}')
        else:
            rs = mu[mu.tok.apply(lambda y: '-'.join(y)) == t]
            head = [f'- Object: second catalogue text{"s" if len(rs) > 1 else ""} {", ".join(rs.textnum)} ({", ".join(sorted(set(rs.cls)))}; no partner in the first catalogue)',
                    f'- Site: {", ".join(sorted(set(rs.site_l)))}']
        L += [f'## {k}. {en}', ''] + head + [f'- Signs: `{t}`', f'- Sound: *{snd(x)}*', f'- Word by word: {ww}', '']
    open(f'{ROOT}/READINGS.md', 'w').write(old + '\n'.join(L) + '\n')
    print('READINGS.md: 20 readings appended (141-160)')
