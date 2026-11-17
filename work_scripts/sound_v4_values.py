#!/usr/bin/env python3
"""Fourth sound list: the third list plus job 1 (705/706) and job 2 (the 25 coverage signs).
A value moves to 'building' when one of its predictions came true (P at or under 0.1) on new texts or on a Lipi
fact not looked at while choosing.  BASIS says which: 'fresh' = the fact that came true was not printed while
choosing; 'seen' = it was visible in the profiles printed while choosing (top neighbours, kinds, top sites).
STRICT coverage counts only fresh-based new values; WIDE counts both.
Writes work_data/sound_v4/values_v4.csv and coverage_v4.csv.  Import: from sound_v4_values import V4, TIER4, STRICT4"""
import os, sys, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_v3_values import V3, TIER3, NOTE
V4 = dict(V3); TIER4 = dict(TIER3); NOTE4 = dict(NOTE); BASIS = {}
UPD = {  # sign: (sound, English, tier, basis, note)
 '705': ('kalam', 'grain measure (a kalam); ship where it stands uncounted before the sail 500', 'building', 'fresh', 'JOB 1. measure: count after it on new texts 28/64 against 14.1% (P 8e-9), tall 28 of 28 (P 1e-13); count varies on goods, fixed three on seals (P 0.015). ship: sail after it 3/64 (P 0.002); coast and abroad 43/384 against 9% (P 0.07)'),
 '706': ('kalam', 'grain measure (variant of 705)', 'building', 'fresh', 'JOB 1, with 705 (the second catalogue merges 706 into 705); 706 takes three after it 45 of 46'),
 '240': ('mīmīn', 'High-star (house crest)', 'building', 'seen', 'A house ending on new-text seals 7/9 against 77% (direction); B another fish crest follows on new texts 15/58 against 6.5%'),
 '233': ('vāḷai', 'scabbard-fish (a counted fish good; also a crest "Bright-star" vāḷmīn)', 'building', 'seen', 'A vāḷmīn house ending 6/9 against 77% (against); B seal size x1.07 (direction); C vāḷai: a measure word follows on new texts 9/39 against 3.4%'),
 '060': ('-iṉ', 'of (joiner after an opener)', 'building', 'seen', 'A sites 17 against 14 (direction); B an opener stands before it on new texts 35/48 against 4.6%'),
 '435': ('kōl', 'rod, sceptre: mutal kōl "chief staff", an office', 'building', 'seen', 'taṭi: size x1.00, sites 6 against 8, land words 6/91 against 5% (all against or direction); kōl: carrier or 690 follows on new texts 9/16 against 1.1%'),
 '407': ('kiḷai', 'herd, lot (the tally word)', 'testing', 'seen', 'A herd-beast reverse 5/43 against 11% (direction); B house share 10 against 9.6 (direction); B2 last sign on copper tablets 45/77 against 21% (Lipi, seen). Not on new texts at all'),
 '900': ('tiṅkaḷ', 'month (counted)', 'building', 'fresh', 'A count before it on new texts 10/20 against 15.8%; B short strokes 61 to tall 6 (both catalogues)'),
 '416': ('turumpu', 'heap of threshed grain', 'building', 'fresh', 'A Harappa mound F 15/27 against 34%; B opens the text on new texts 4/5; C tall counts 1 of 15 (against)'),
 '413': ('nel', 'paddy, grain', 'building', 'fresh', 'A Harappa mound E 22/44 against 25%; B a measure word follows on new texts 3/3'),
 '388': ('aracu', 'pipal; royal (house name)', 'building', 'seen', 'A house share 2 against 1.8 (direction); B jar follows on new texts 5/13 against 10.2%'),
 '384': ('aracu', 'pipal; royal (house name)', 'building', 'fresh', 'A house share 0 against 0.1 (against); C frames of 388/382: 7 against 3 (P 0.054)'),
 '382': ('aracu', 'pipal; royal (lineage head)', 'building', 'seen', 'A frames 3 against 3 (against); B jar after 2/20 (against); B2 maka follows 5/20 against 0.9% (both catalogues)'),
 '226': ('kūṭumīn', 'crate of fish', 'building', 'fresh', 'A coast and abroad 9/52 against 9% (P 0.035); B tall counts 17 to short 8'),
 '048': ('er̤uvar', 'the Seven (a body of seven)', 'testing', 'seen', 'mūṭai earlier; er̤uvar A frames of 585: 0 (against); B jar after 17/17 (Lipi only; 048 is not on new texts)'),
 '097': ('aṭimai', 'bondsman, servant (a ration receiver)', 'building', 'seen', 'A Harappa mound E 2/7 (direction); B a count or cup before it on new texts 4/9 against 16.5%'),
 '717': ('aṭi', 'foot; servant (aṭiyāṉ)', 'building', 'fresh', 'tāḷ earlier. aṭi A: a person or title sign on the same face on new texts 11/23 against 16%; B seal smaller x1.06 (against)'),
 '832': ('kaṇ', 'eye; at, in (place word)', 'testing', 'fresh', 'A sites 6 against 8 (against); B clean: a time/place word before it on new texts 3/25 against 7.2% (direction)'),
 '790': ('maṇi', 'bead, gem', 'building', 'seen', 'kaṉ copper went against in v3. maṇi A bead towns 9/69 against 9% (direction); B tags on new texts 9/20 against 22%'),
 '605': ('kutir', 'grain bin, granary', 'building', 'fresh', 'A Harappa mound F 6/9 against 34%; B maka follows on new texts 2/3'),
 '137': ('vēḷāḷaṉ', 'cultivator', 'building', 'fresh', 'A Harappa mound E 7/12 against 25%; B grain/cup on the face 2/19 (against)'),
 '550': ('vāy', 'gate', 'building', 'seen', 'A a ward jar on the face on new texts 3/27 against 7% (direction); B 060/527/555/525 follows on new texts 6/23 against 2.0%'),
 '923': ('maruppu', 'horn of the crescent (a counted thing before the jar)', 'building', 'seen', 'A a count before it 17/42 against 19% (both catalogues); B month signs on the face 0/48 (against)'),
 '877': ('nālkāṇi', 'four shares', 'building', 'seen', 'A house share 1 against 0.3 (direction); B a count follows on new texts 5/12 against 14.1%'),
 '104': ('taṭṭāṉ', 'goldsmith (person with the seed-weight at his foot)', 'building', 'seen', 'kuṉṟavaṉ: frames 4 against 3, no-jar 10/26 against 33% (against); taṭṭāṉ: frames of 391 1 against 1 (against), gold/seed weight on the face 7/27 against 1% (both catalogues)'),
 '527': ('kāval', 'guard (vāy kāval "gate-guard")', 'building', 'fresh', 'A carries the jar 7/63 against 33%; B ends the text on new texts 3/3'),
 '831': ('tiṉai', 'Italian millet', 'building', 'seen', 'A Harappa mound E 1/6 (against); B sale/price/field/grain words on the face 9/23 against 8% (both catalogues)'),
}
for s, (snd, en, t, b, note) in UPD.items():
    V4[s] = (snd, en); TIER4[s] = t; NOTE4[s] = note; BASIS[s] = b
STRICT4 = dict(TIER4)
for s, b in BASIS.items():
    if b == 'seen' and TIER4[s] == 'building': STRICT4[s] = 'testing'
if __name__ == '__main__':
    from sound_v4_common import coverage, OUT4
    import pandas as pd
    with open(f'{OUT4}/values_v4.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['sign', 'sound', 'english', 'tier_v4', 'basis', 'tier_v3', 'note'])
        for s in sorted(V4): w.writerow([s, V4[s][0], V4[s][1], TIER4[s], BASIS.get(s, ''), TIER3.get(s, 'new'), NOTE4.get(s, '')])
    from collections import Counter
    print('tiers v4 (non-base):', Counter(t for t in TIER4.values() if t != 'base'), 'strict:', Counter(t for t in STRICT4.values() if t != 'base'))
    rows = []
    for name, T, allow in [('third list', TIER3, ('base', 'building')), ('fourth list, strict (fresh-based only)', STRICT4, ('base', 'building')),
                           ('fourth list, wide', TIER4, ('base', 'building')), ('fourth list incl. testing', TIER4, ('base', 'building', 'testing'))]:
        c = coverage(T, allow)
        for g, v in c.items(): rows.append(dict(list=name, group=g, **v))
    df = pd.DataFrame(rows); print(df.to_string(index=False)); df.to_csv(f'{OUT4}/coverage_v4.csv', index=False)
