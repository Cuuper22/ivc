#!/usr/bin/env python3
"""Twenty whole readings 121-140 (sixth list), favouring Mohenjo-daro copper tablets with their picture named.
Appends a section to READINGS.md (reruns replace only this section). † = word under test; ‡ = word whose fact was seen
while choosing. Run after sound_v6_values.py."""
from sound_v6_common import *
from sound_v6_values import V6, TIER6, BASIS6
HEAD = '## Twenty more: copper tablets with their pictures, and texts opened by the sixth pass'
R = [
 ('C', '235-705-033-845-407-321-407', 'Bamboo-star: three kalam; sheaves of the kindred, the kindred\'s ration.', 'a hare among plants (on two copies the sign 753 is written on that side instead)'),
 ('C', '806-845-061-407-850-900-740', 'Produce: sheaves, a quarter; the kindred\'s share; of the Month house.', 'a horned figure with a bow (on four copies a flowering-plant sign, 777 / 780 / 781 / 782, is written on that side instead)'),
 ('C', '231-017-585-095-520-032-407', 'First-star, the Seven Maidens; the staff-bearer chief; two kindreds.', 'a goat with a marked body and a trough (on four copies sign 777 instead)'),
 ('C', '798-240-845-061-407', 'Descendant of High-star: sheaves, a quarter, the kindred.', 'a tiger'),
 ('C', '415-220-845-407', 'Branch-Star: sheaves of the kindred.', 'an endless knot'),
 ('C', '255-435-690-740-900-003-422', 'Of the house allied to the Chief Staff; month: three fields.', 'a water buffalo; copies write the field sign as 422, 423 or 424'),
 ('C', '003-422-176-100-740', 'Three fields: of the Tax-Elder house.', 'a goat with a marked body (the sister set 003-421-176-100-740-790 writes the field sign 421)'),
 ('C', '806-235-233-705-033-585-407', 'Produce of the Bamboo-star Scabbard house: three kalam; the Maiden kindred.', 'a spotted composite beast'),
 ('C', '233-585-407', 'Scabbard-fish, the Maiden kindred: five kalam.', 'no picture: the other face carries the amount 706-005 "kalam five"'),
 ('C', '798-231-705-033-904-100-740', 'Descendant of First-star: three kalam, two months: of the Elder house.', 'sign 957 on the picture side'),
 ('C', '503-615-752-740', 'Of the house of the heir of Hill-Field.', 'a branch-horned beast with a trough (stag); on two copies of the short form 503-615-740 the deer sign 341 is written in its place'),
 ('C', '706-033-923-740-001', 'Three kalam of ivory: of the house; one.', 'an elephant'),
 ('C', '017-585-388-740', 'Of the royal house of the Seven Maidens.', 'a spotted, long-necked composite beast'),
 ('C', '231-255-435-690-740', 'First-star: of the house allied to the Chief Staff.', 'signs 479-749 on the picture side'),
 ('L', '371-031-741-844-390', 'Spindle, one; first ward: a bundle of cotton.', ''),
 ('L', '692-060-806-233-923-740-061-407', 'Of the Assembly: of the Produce-Scabbard-Ivory house; a quarter for the kindred.', ''),
 ('L', '820-002-101-740-090', 'Two quarters: agent of the Elder house.', ''),
 ('L', '817-033-927-740', 'Three shares: of the Two-Months house.', ''),
 ('Mu', '495-615-176-100-001-033-422', 'Horn-Field, the Tax-Elder: one; three fields. A new text.', ''),
 ('Mu', '055-055-415-060-240-773-740', 'Twelve, twelve; of Branch: the house of the child of High-star. A new text.', ''),
]
if __name__ == '__main__':
    old = open(f'{ROOT}/READINGS.md').read()
    old = old.split('\n' + HEAD)[0].rstrip() + '\n'
    byt = collections.defaultdict(list)
    for r in d.itertuples():
        if r.complete_txt: byt['-'.join(r.tok)].append(r)
    mu = M[~M.partnered & M.complete_b]
    L = ['', HEAD, '',
         'Added by `work_scripts/sound_v6_readings.py` (sixth list: `jobs/out/sound_list_v6.md`). Readings 121-134 are Mohenjo-daro copper tablets: one face carries the text, the other a picture; '
         'all copies of one text carry the same picture (a "set"). The picture is named as read from the photographs. New words they rest on: kiḷai "kindred" (407/406/408), par̤aṉam "paddy field" (421-424), '
         'paṭi "ration" (321, 323, variants of 320), maka "child of" (772/773), irutiṅkaḷ "two months" (927), mutu "elder" (101), pal "many" (642), cūṭu "sheaves" (844), ūr "town" (336), vaḷḷam "grain measure" (711). '
         'A dagger (†) marks a word under test, a double dagger (‡) a word whose fact was seen while choosing. Reading order = stored order reversed. '
         '"New text" = second-catalogue (Mahadevan 1977) text with no partner in the first catalogue.', '']
    snd = lambda x: ' '.join(V6[a][0] if a in V6 else '?' for a in x)
    mark = lambda a: '†' if TIER6.get(a) in ('testing', 'paused') else '‡' if BASIS6.get(a) == 'seen' else ''
    for k, (cat, t, en, pic) in enumerate(R, 121):
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
    print('READINGS.md: 20 readings appended (121-140)')
