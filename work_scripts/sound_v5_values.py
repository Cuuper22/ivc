#!/usr/bin/env python3
"""Fifth sound list: the fourth list plus job 1 (wide values turned strict by a fresh prediction) and job 2 (the next
25 blockers and the tree signs).  BASIS 'fresh' = the fact that came true was not printed while the word was chosen;
'seen' = it was.  STRICT counts only fresh-based new values; WIDE counts both.
Writes work_data/sound_v5/values_v5.csv and coverage_v5.csv.  Import: from sound_v5_values import V5, TIER5, STRICT5, BASIS5"""
import os, sys, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_v4_values import V4, TIER4, NOTE4, BASIS, STRICT4
V5 = dict(V4); TIER5 = dict(TIER4); NOTE5 = dict(NOTE4); BASIS5 = dict(BASIS)
# job 1: fresh predictions that came true (round one / round two)
J1 = {
 '233': 'J1 fresh: a number two places after it 27/166 against 9.0% (P 0.002)',
 '060': 'J1 fresh: a fish crest two places after it 30/205 against 5.8% (P 3e-6)',
 '435': 'J1 fresh: a closing class sign or text end two places after it 53/65 against 52% (P 8e-7)',
 '388': 'J1 fresh: man/comb/spear/carrier or text end two places after it 33/50 against 41% (P 0.0004)',
 '240': 'J1 round two fresh: the other face of its tablets carries a number or cup 59/96 against 52% (P 0.036); seal size x0.99 (against)',
 '097': 'J1 round two fresh: a number two places before it 10/14 against 12.9% (P 8e-7); reverse face 3/3 (too few)',
 '923': 'J1 round two fresh: copper tablets with it show the elephant 11/12 against 14% (P 6e-9); horned beasts 0/12 (against)',
 '104': 'J1 round two fresh: Mohenjo-daro objects in the DK area 13/14 against 70% (P 0.048); seals smaller x0.72 (P 0.10)',
}
for s, n in J1.items():
    BASIS5[s] = 'fresh'; NOTE5[s] = NOTE5.get(s, '') + ' | ' + n
V5['923'] = ('maruppu', 'tusk, ivory (horn; the counted thing on elephant copper tablets)')
for s, n in {'382': 'J1: jar two places after 2/15 (direction); seal size x1.15 n 6 (direction)', '790': 'J1: number two places away 2/76 (against); Harappa mound E 4/21 (against)',
             '550': 'J1: closing sign two places after 49/96 against 52% (against); seal size x0.91 (against)', '877': 'J1: fish crest two places after 0/22 (against); seal size x0.93 (against)',
             '831': 'J1: reverse face 2/4 (against); Harappa Period 3C too few dated'}.items():
    NOTE5[s] = NOTE5.get(s, '') + ' | ' + n
# job 2
UPD = {  # sign: (sound, English, tier, basis, note)
 '405': ('nūl', 'thread, yarn (counted in lots)', 'building', 'seen', 'J2 A: a count of 3+ before the tree family on new texts 6/48 against 3.2% (P 0.004); B reverse face 2/7 (against)'),
 '407': ('kiḷai', 'kindred; lot (cloth tuṇi went against)', 'testing', 'seen', 'J2 tuṇi: reverse face 5/20 against 52% (against); tree family on goods objects 16/46 against 45% (against); C kiḷai: names with the tree family end in the house ending 4/4 against 77% (direction)'),
 '692': ('kūṭṭam', 'assembly, council (an office opening)', 'building', 'fresh', 'J2 A: sites 6 against 8 (against); B seals x1.45 bigger at equal length (n 42, P 8e-6)'),
 '711': ('vaḷḷam', 'grain measure (vessel)', 'building', 'fresh', 'J2 A: counts after it tall 15, short 0 (P 1e-5); B the cup two places after 10/13 against 0.4% (seen)'),
 '526': ('kāval', 'guard (variant of 527)', 'building', 'fresh', 'J2 A: frames of 527/525 4 against 0 (P 0.017); B jar 0/13 against 33% (P 0.006)'),
 '525': ('kāval', 'guard (variant of 527)', 'building', 'fresh', 'J2 A: frames of 527/526 1 against 0 (P 0.035); B jar 0/11 against 33% (P 0.012)'),
 '161': ('kā', 'keeper, load-carrier (variant)', 'building', 'fresh', 'J2 A: jar 4/15 against 32% (direction); B frames of the carriers 7 against 2 (P 0.029)'),
 '495': ('kompu', 'horn (horn-blower; a name word)', 'building', 'fresh', 'J2 A: horned non-unicorn beasts 2/19 against 14% (against); B frames of 491 3 against 1 (P 0.069)'),
 '491': ('kompu', 'horn (variant of 495)', 'building', 'fresh', 'J2 A: frames of 495 3 against 1 (P 0.053); B house share 0 against 0.15 (against)'),
 '838': ('viḷai', 'produce (variant of 806, as the second catalogue draws it)', 'building', 'fresh', 'J2 A: frames of 806 11 against 2 (P 0.041); B number two places before 0/9 (against)'),
 '370': ('katir', 'spindle (also ear of grain, ray)', 'building', 'fresh', 'J2 A: faces with 370/371 carry a fibre sign 12/24 against 9% (P 3e-7); B frames of 371 3 against 0 (P 0.008)'),
 '371': ('katir', 'spindle (same drawing code as 370)', 'building', 'fresh', 'with 370 (one sign in the second catalogue, M397; one drawing code P108)'),
 '565': ('maṟavaṉ', 'warrior (crossed arrows)', 'building', 'fresh', 'J2 A: jar 10/18 against 32% (against); B frames of the chief 520 4 against 2 (P 0.067)'),
 '850': ('kāṇi', 'share (the bare diamond)', 'building', 'fresh', 'J2 A: a count follows it on new texts 4/12 against 14.1% (P 0.076); B frames of 861/817 7 against 5 (direction)'),
 '868': ('araikkāṇi', 'half-share (a fraction ending)', 'building', 'fresh', 'J2 kāṇi: frames 1 against 1 (against), new-text count too few; C araikkāṇi: jar 0/13 against 33% (P 0.006)'),
 '519': ('vēli', 'fence, hedged plot (a name element)', 'building', 'fresh', 'J2 tōṭṭam: land words 0/17 (against), frames of 910 too few; C vēli: jar one or two places after 8/26 against 10% (P 0.003)'),
 '347': ('kalai', 'stag', 'building', 'fresh', 'J2 māṉ: reverse too few; number on the face 0/10 (against); C kalai: Harappa mound E 9/9 against 25% (P 4e-6; one text in copies)'),
 '165': ('poḻutu', 'sun, day', 'testing', 'fresh', 'J2: short counts 2 to tall 3 (against); reverse 6/10 against 52% (direction); C kātu: mound E 0/9 (against)'),
 '645': ('kar̤añcu', 'a gold weight', 'testing', 'fresh', 'J2: DK 10/13 against 70% (direction); number two away 5/43 (direction); C pāti: frames 4 against 8 (against)'),
 '167': ('?', 'closes kalam tablets', 'paused', 'fresh', 'J2 tūkku: number two before 0/14 (against); reverse 2/3 (direction); C kā: carrier frames 1 against 2 (against). Third word to fail (poli, kā, tūkku)'),
 '236': ('vēymīn', 'Bamboo-star (caged; crest variant)', 'testing', 'fresh', 'J2 vēy-kūṭu: tall counts 0 of 7 (against); new-text counts too few; C vēymīn: frames of 235 5 against 3 (direction)'),
 '048': ('er̤uvar', 'the Seven', 'testing', 'fresh', 'J2: man two places after 0/17 (against); trade words 0/18 (against); C kōvai: frames of 790/792 1 against 0 (direction). Bracketed seven absent from new texts'),
 '832': ('kaṇ', 'eye; at, in', 'testing', 'fresh', 'J2 kaṇkāṇi: seals x0.82 (against), jar 13/43 against 33% (direction); C maṇi: frames of 790 4 against 3 (direction)'),
 '222': ('aṭaimīn', 'shut-in fish (crest?)', 'testing', 'fresh', 'J2 kuḷa-mīn: jar on new texts 2/3 (direction), house share 0 (against); C aṭaimīn: crest frames 7 against 4 (direction)'),
 '460': ('mukkōṭu', 'Three-peaks', 'testing', 'fresh', 'J2: hill frames 1 against 1; house share 1 against 0.66 (direction); C mukkōṭṭai: fort/town frames 2 against 1 (direction)'),
 '821': ('veṟṟilai', 'betel leaf?', 'testing', 'fresh', 'J2 kāl: wheel frames 2 against 2, 002 after 0/10 (against); C veṟṟilai: a number within two places 8/43 against 12% (direction)'),
 '792': ('maṇi ~ aracu', 'gem ~ pipal', 'testing', 'fresh', 'J2 maṇi: frames of 790 2 against 1 (direction), house share 0 (against); C aracu: pipal frames 3 against 2 (P 0.11, direction)'),
}
for s, (snd, en, t, b, note) in UPD.items():
    V5[s] = (snd, en); TIER5[s] = t; NOTE5[s] = (NOTE5.get(s, '') + ' | ' if s in NOTE4 else '') + note; BASIS5[s] = b
STRICT5 = dict(TIER5)
for s, b in BASIS5.items():
    if b == 'seen' and TIER5[s] == 'building': STRICT5[s] = 'testing'
if __name__ == '__main__':
    from sound_v5_common import coverage, OUT5, readable, M, d
    from sound_v3_values import TIER3
    import pandas as pd
    from collections import Counter
    with open(f'{OUT5}/values_v5.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['sign', 'sound', 'english', 'tier_v5', 'strict_v5', 'basis', 'tier_v4', 'note'])
        for s in sorted(V5): w.writerow([s, V5[s][0], V5[s][1], TIER5[s], STRICT5[s], BASIS5.get(s, ''), TIER4.get(s, 'new'), NOTE5.get(s, '')])
    print('tiers v5 (non-base):', Counter(t for t in TIER5.values() if t != 'base'), 'strict:', Counter(t for t in STRICT5.values() if t != 'base'), 'values', len(V5))
    rows = []
    m = M[~M.partnered & M.complete_b]
    for name, T in [('fourth list, strict', STRICT4), ('fourth list, wide', TIER4), ('fifth list, strict', STRICT5), ('fifth list, wide', TIER5)]:
        c = coverage(T)
        for g, v in c.items(): rows.append(dict(list=name, group=g, **v))
        h = m.tok.apply(lambda x: readable(x, T))
        for g, mm in [('all', h.index == h.index), ('seals', (m.kind == 'seal').values), ('goods', (m.kind != 'seal').values)]:
            rows.append(dict(list=name, group='new texts ' + g, faces=int(h[mm].sum()), of_faces=int(mm.sum()), distinct=len(set(m.tok[h & mm])), of_distinct=len(set(m.tok[mm])), objects=None))
    df = pd.DataFrame(rows); print(df.to_string(index=False)); df.to_csv(f'{OUT5}/coverage_v5.csv', index=False)
