#!/usr/bin/env python3
"""Sixth value list = fifth list (sound_v5_values) + jobs 1-2 of this pass (+ job 3 when sound_v6_job3*.py add theirs
through J3 below). BASIS 'fresh' / 'seen' as before; STRICT6 counts only fresh-based values.
Import: from sound_v6_values import V6, TIER6, STRICT6, BASIS6, NOTE6, ALT6"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_v5_values import V5, TIER5, STRICT5, BASIS5, NOTE5
V6 = dict(V5); TIER6 = dict(TIER5); BASIS6 = dict(BASIS5); NOTE6 = dict(NOTE5); ALT6 = {}
UPD = {  # sign: (sound, English, tier, basis, note, second word or '')
 '711': ('vaḷḷam', 'grain measure (4 marakkāl)', 'building', 'fresh', 'v6 J2: the other face holds a who-word 15/20 against 43% (P 0.004); pāṉai: other face a number/cup 8/20 against 52% (against)', ''),
 '060': ('-iṉ', 'of (joiner after an opener)', 'building', 'fresh', 'v6 J2: new texts with 060 end in the house ending 11/20 against 37% (P 0.08); uḷ: amount within two places after 6/49 against 12.9% (against)', 'uḷ "in"'),
 '692': ('kūṭṭam', 'assembly, council (an office opening)', 'building', 'fresh', 'v6 J2: person words 17/89 against 25% (against); B Mohenjo-daro/Harappa 81/89 against 82% (P 0.014). nāṭu: land words 3/89 against 11% (against), crop words 5/89 against 10% (against)', 'nāṭu "district" (two misses this pass)'),
 '838': ('viḷai', 'produce (variant of 806)', 'building', 'fresh', 'v6 J2: carrier or number after it 1/21 (against); B another crop word on the face 6/24 against 10% (P 0.023; distinct texts 4/19 against 11%, P 0.16). eḷ: coast/abroad 3/24 against 10% (direction), pots 0/24 (against)', 'eḷ "sesame"'),
 '407': ('kiḷai', 'kindred, family (the branching tree: kiḷai "to branch, multiply as families")', 'building', 'fresh', 'v6 J2: house-mates 10 against 9.6 (direction); B a fish crest on the face 65/127 against 20% (P 1e-14; distinct texts 23/69 against 25%, P 0.07). tuṇi: coast/abroad 7/127 (against), trade verbs 1/127 (against)', 'tuṇi "cloth" (four misses)'),
 '842': ('tuṇai', 'deputy, companion (closes an office text)', 'building', 'seen', 'v6 J2 (texts seen): last sign 5/5 against 29% (P 0.002); month/assembly opener on the face 4/5 against 4% (P 1e-5)', ''),
 '611': ('kuṭai', 'umbrella: a ruling house ("the quarter of the Umbrella")', 'building', 'seen', 'v6 J2 (texts seen): wheel kāl right before it 2/6 against 1.5% (P 0.003); jar/aracu/gate within two after it 3/8 against 11% (P 0.046)', ''),
 '341': ('kalai', 'stag, deer (the deer sign stands for the stag picture on copper tablets M-516, M-517)', 'testing', 'fresh', 'v6 J1: hill/field words on the face 1/28 (direction); tablets 12/28 against 36% (direction)', ''),
}
for s, (snd, en, t, b, note, alt) in UPD.items():
    V6[s] = (snd, en); TIER6[s] = t; BASIS6[s] = b; NOTE6[s] = (NOTE6.get(s, '') + ' | ' if s in NOTE6 else '') + note
    if alt: ALT6[s] = alt
NOTE6['255'] = NOTE6.get('255', '') + ' | v6 J1: the gharial (crocodile, mutalai) tablets carry it 11/53 against 3.1 by shuffle (P 0.0002; one text in 11 copies)'
NOTE6['520'] = NOTE6.get('520', '') + ' | v6 J1: elephant (vēḻam) seals on new texts 1/8 against 6% (direction); tags 1/6 (direction)'
NOTE6['923'] = NOTE6.get('923', '') + ' | v6 J1: elephant seals 1/49 against 1.0% (direction); ivory rods 0/48 (against)'
NOTE6['806'] = NOTE6.get('806', '') + ' | v6 J1 (seen in the scan): plant-picture moulded tablets carry it 5 distinct texts against 1.1; with the carrier 158/154 9 of 43 tablets against 2.8 (P 0.0002)'
J3 = {}   # filled by sound_v6_job3_values.py
try:
    from sound_v6_j3vals import J3
except ImportError:
    pass
for s, (snd, en, t, b, note, alt) in J3.items():
    V6[s] = (snd, en); TIER6[s] = t; BASIS6[s] = b; NOTE6[s] = (NOTE6.get(s, '') + ' | ' if s in NOTE6 else '') + note
    if alt: ALT6[s] = alt
STRICT6 = dict(TIER6)
for s, b in BASIS6.items():
    if b == 'seen' and TIER6[s] == 'building': STRICT6[s] = 'testing'
if __name__ == '__main__':
    import csv
    import pandas as pd
    from collections import Counter
    from sound_v6_common import coverage, OUT6, readable, M, d
    with open(f'{OUT6}/values_v6.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['sign', 'sound', 'english', 'tier_v6', 'strict_v6', 'basis', 'tier_v5', 'second_word', 'note'])
        for s in sorted(V6): w.writerow([s, V6[s][0], V6[s][1], TIER6[s], STRICT6[s], BASIS6.get(s, ''), TIER5.get(s, 'new'), ALT6.get(s, ''), NOTE6.get(s, '')])
    print('tiers v6 (non-base):', Counter(t for t in TIER6.values() if t != 'base'), 'strict:', Counter(t for t in STRICT6.values() if t != 'base'), 'values', len(V6))
    rows = []
    m = M[~M.partnered & M.complete_b]
    for name, T in [('fifth list, strict', STRICT5), ('fifth list, wide', TIER5), ('sixth list, strict', STRICT6), ('sixth list, wide', TIER6)]:
        c = coverage(T)
        for g, v in c.items(): rows.append(dict(list=name, group=g, **v))
        h = m.tok.apply(lambda x: readable(x, T))
        for g, mm in [('all', h.index == h.index), ('seals', (m.kind == 'seal').values), ('goods', (m.kind != 'seal').values)]:
            rows.append(dict(list=name, group='new texts ' + g, faces=int(h[mm].sum()), of_faces=int(mm.sum()), distinct=len(set(m.tok[h & mm])), of_distinct=len(set(m.tok[mm])), objects=None))
    C = pd.DataFrame(rows); C.to_csv(f'{OUT6}/coverage_v6.csv', index=False)
    print(C.to_string(index=False))
