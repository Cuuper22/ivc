#!/usr/bin/env python3
"""Third sound list: the 89 values of the second list plus the third pass (stage A/B/C), sorted into building on,
testing, paused.  Writes work_data/sound_v3/values_v3.csv.  Import: from sound_v3_values import V3, TIER3"""
import os, sys, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OUT3 = '/home/claude/ivc/work_data/sound_v3'
rows = list(csv.DictReader(open('/home/claude/ivc/work_data/sound_v2/values_v2.csv')))
V3 = {r['sign']: (r['sound'], r['english']) for r in rows}
TIER3 = {r['sign']: r['tier'] for r in rows}
OLDTIER = dict(TIER3)
NOTE = {}
# sign: (sound, English, new tier, note)
UPD = {
 '055': ('paṉṉiru', 'dozen', 'building', 'A: on sealings/tags on new texts 14/31 against 22%; the fish follows it 4/40 against 3.1%'),
 '061': ('kāl', 'quarter', 'building', 'A: copper tablets on new texts 1/10 (direction); B: a count before it on new texts 4/10 against 15.8%'),
 '140': ('ammai', 'lady', 'building', 'A: opens the text on new texts 11/17 against 29%'),
 '171': ('niṟai', 'weight, full measure', 'building', 'A: a count after it on new texts 3/7 against 14.1%'),
 '175': ('iṟai', 'tax', 'building', 'A: miniature tablets on new texts 2/4 against 10%'),
 '320': ('paṭi', 'ration measure, daily allowance', 'building', 'NEW WORD. A: the month sign 920 follows it on new texts 5/7 against 0.7%'),
 '335': ('ūr', 'town', 'building', 'NEW WORD (C). puṭṭi failed (A 1/6 tablets, B 2/6 with a number); ūr: jar or maka follows it on new texts 3/6 against 11.2%'),
 '440': ('koḷ', 'received, bought', 'building', 'A against: pots on new texts 1/19 against 7%; B: Harappa on new texts 10/19 against 34%'),
 '503': ('malai', 'hill', 'building', 'A: copper tablets on new texts 3/19 against 4%'),
 '540': ('paṟai', 'drum; a rice measure', 'building', 'MEANING CHANGED to the measure (DEDR 4032). A: pots on new texts 2/7 against 7%'),
 '575': ('kōṭṭai', 'great grain measure', 'building', 'A: a count before it on new texts 6/14 against 15.8%'),
 '595': ('paṭṭaṟai', 'forge, smithy', 'building', 'NEW WORD (C). peṭṭi: A against (counts short 19, tall 1), B copper on new texts 12/27 against 4%; paṭṭaṟai: with smith/copper/weight signs on new texts 4 against 1.4'),
 '615': ('vayal', 'field', 'building', 'A: copper tablets on new texts 16/86 against 4%'),
 '617': ('ūḻiyaṉ', "(king's) servant", 'building', 'A: carries the jar 13/75 against 33% (a title in the possessive place)'),
 '630': ('pal', 'many', 'building', 'A against: a number on the same object 13 against 20.2; B: frames of 632, 6 against 2'),
 '636': ('pal', 'many', 'building', 'A: frames of 630, 4 against 0'),
 '690': ('piṇai', 'bound, allied', 'building', 'A: jar follows it on new texts 10/20 against 10.2%'),
 '760': ('maka', 'child of', 'building', 'A: jar follows it on new texts 25/29 against 10.2%'),
 '803': ('il', 'house', 'building', 'A: a fish crest follows it on new texts 6/22 against 7.8%'),
 '824': ('vilai', 'price', 'building', 'NEW WORD. A: Harappa objects from mound E 11/23 against 25%'),
 '840': ('iṇai', 'pair', 'building', 'A: two tall strokes follow it on new texts 7/16 against 1.7%. Second reading vaḷai "bangle" (Lipi bangles x7.9, seen)'),
 '845': ('cūṭu', 'bundle of sheaves', 'building', 'NEW WORD. A: copper tablets on new texts 3/9 against 4%'),
 '104': ('kuṉṟavaṉ', 'hillman', 'testing', 'NEW WORD. A frames of 480: 3 against 2 (P 0.29); B house share 1 against 0.19 (P 0.18)'),
 '165': ('poḻutu', 'sun, day', 'testing', 'A: with the crescent 900 on one face 10 of 33 against 0.6 (fact seen in Lipi while choosing)'),
 '240': ('mīmīn', 'High-star', 'testing', 'A against: Harappa on new texts 18/60 against 34%; B: spear ending 2/9 against 10% (direction)'),
 '407': ('kiḷai', 'herd, lot', 'testing', 'A: copper tablets with an animal reverse 31/63 against 33% (icon table seen while choosing)'),
 '460': ('mukkōṭu', 'Three-peaks', 'testing', 'A: jar after it 2/11 against 10.2%; B jar or spear 2/11 (direction)'),
 '645': ('kar̤añcu', 'a gold weight', 'testing', 'kaṭṭu: A count before 1/4 (direction), B with a number 2/6 against 35% (against); kar̤añcu: too few new texts with a sign after it'),
 '711': ('vaḷḷam', 'grain measure', 'testing', 'NEW WORD. A against: E trench 11 2/21 against 10%; B: cup on the same object 12 of 21 against 2.5 (seen)'),
 '717': ('tāḷ', 'stem (of a line)', 'testing', 'A jar after it 3/21 against 10.2%; B house share 1 against 0.41 (direction)'),
 '790': ('kaṇ ~ kaṉ', 'eye ~ copper', 'testing', 'A against: copper on new texts 0/20 against 4%; B off seals 8/20 against 55% (direction). The Lipi copper excess stands'),
 '838': ('eḷumpu ~ eḷ', 'bone ~ sesame', 'testing', 'A against: rods on new texts 0/5; B rods both catalogues 4/24 x22 (Lipi seen)'),
 '850': ('kaṇ ~ kaṉ', 'eye ~ copper', 'testing', 'A copper on new texts 2/13 against 4% (P 0.11); B both catalogues 20/69 x6.5 (Lipi seen)'),
 '877': ('nālkāṇi', 'four shares', 'testing', 'A against: seal size x0.93; B opens the text 12/26 against 29% (Lipi seen)'),
 '167': ('?', 'tablet word', 'paused', 'poli: mound F 3/9 against 34%, copies 10/15 against 69%; kā: carrier frames 1 against 2. Lead: closes kaḷam (705/706) tablets only'),
 '233': ('varimīn', 'Striped-star', 'paused', 'spear after it 1/39, jar or spear 3/39 against 11.4%; kavar-mīn on copper tablets 0/39'),
 '832': ('?', 'eye with pupil', 'paused', 'copper 1/23, off seals 14/23 on seals, bead towns 0/23; lead: after the two-crescent sign 904 and before chief 255'),
 # signs entering the list
 '806': ('viḷai', 'produce, ripened crop', 'building', 'NEW WORD for the crop. A: a load-carrier follows it on new texts 5/25 against 1.4%'),
 '500': ('pāy', 'sail (ship)', 'building', 'NEW WORD for a building value. A: Lothal on new texts 8/12 against 8%'),
 '890': ('koṭu', 'given', 'building', 'NEW SIGN. A: sealings/tags on new texts 7/9 against 22%'),
 '413': ('nel', 'paddy, grain', 'testing', 'NEW WORD (katir paused). A cup on the face 1/6 against 0.1 expected (P 0.12); B opens the text 3/5 against 29% (P 0.15)'),
 '048': ('mūṭai', 'sack-load', 'testing', 'NEW SIGN. A against: no-animal objects 5/18 against 51%; B frames of the dozen 055, 2 against 0 (P 0.12)'),
 '391': ('kollaṉ', 'smith', 'testing', 'NEW SIGN. A copper on new texts 1/3 (P 0.13); B both catalogues 4/13 x6.9 (Lipi tools seen)'),
 '705': ('kalam', 'vessel, ship (hull with a mast)', 'testing', 'NEW WORD (kaḷam paused in the second list). D: 500 sail follows it on new texts 3/64 against 0.4%; Lothal 8/66 against 8% and sealings 17/66 against 22% (direction)'),
 '417': ('kā', 'carrying pole (pole-load)', 'testing', 'NEW SIGN. too few for a frame test; a count before it 8/8 (seen)'),
}
for s, (snd, en, t, note) in UPD.items():
    V3[s] = (snd, en); TIER3[s] = t; NOTE[s] = note
NEWW = {'705', '320', '335', '595', '824', '845', '806', '500', '890', '413', '048', '391', '417', '104', '645', '711', '540'}
if __name__ == '__main__':
    with open(f'{OUT3}/values_v3.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['sign', 'sound', 'english', 'tier_v3', 'tier_v2', 'note'])
        for s in sorted(V3):
            w.writerow([s, V3[s][0], V3[s][1], TIER3[s], OLDTIER.get(s, 'new'), NOTE.get(s, '')])
    from collections import Counter
    nb = {s: t for s, t in TIER3.items() if t != 'base'}
    print('tiers (non-base):', Counter(nb.values()), 'total', len(nb))
