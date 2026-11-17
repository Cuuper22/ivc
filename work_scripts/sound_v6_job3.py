#!/usr/bin/env python3
"""Job 3: the next 25 signs (ranked by sound_v6_job3_rank.py, which printed only picture and slot).
Word chosen from the picture (shape + second-catalogue glyph) and the slot; where the second catalogue draws the sign
as one with a valued sign, the variant takes the main sign's word (the fifth-pass merge trick) and prediction A is the
frame test. ALL predictions below were written before any was computed. Writes work_data/sound_v6/job3_tests.csv."""
from sound_v6_common import *
from sound_v6_job2 import frac_with, sites
CREST = {'231', '233', '235', '240', '220', '236', '243'}
CROP = {'806', '838', '413', '416', '845', '390', '831', '615'}
GOODS = {'220', '226', '390', '413', '806', '590', '595', '700', '705'}
TALLN = TALL
def tabs(s): return on_kind(s, {'ctab', 'mtab'}, 'LM')
W = {  # sign: (word, English, DEDR, why)
 '321': ('paṭi', 'rung; ration measure (drawn like 320 with a stroke more)', '3849/3850', 'picture: ladder like 320; slot: middle of copper-tablet text; second word muyal "hare" (the picture beside it)'),
 '592': ('kūṭu', 'crate, cage, coop (the chest 590 caged by four strokes)', '1883', 'picture: box 590 inside the four-stroke cage (as 226 is the fish in a cage)'),
 '703': ('aḷavu', 'measure, a measured amount (cup with strokes inside)', '295', 'picture: the cup 700 with marks inside; slot: opens or stands mid-text'),
 '773': ('maka', 'child of (variant of 752/760, the branched U)', '4630?', 'picture: U with branching arms like 752/760; slot: right before the jar 12 of 14 (as maka)'),
 '772': ('maka', 'child of (same sign as 773 in the second catalogue, M348)', '', 'merge: M348 = 772 + 773'),
 '927': ('irutiṅkaḷ', 'two months (variant of 904)', '', 'merge: the second catalogue draws 927 as 904 (M294)'),
 '554': ('paṟai', 'a grain measure (variant of the bowtie 540)', '4032', 'picture: bowtie like 530/540; slot: counted 7 of 19'),
 '064': ('parutti', 'cotton (variant of the tree 390)', '3976', 'merge: the second catalogue draws 064 as 390 (M162) or M161'),
 '422': ('par̤aṉam', 'paddy field, agricultural land (a grid with growing plants on top)', '4112', 'picture: field grid (like 615 vayal) with plant heads; slot: counted, last on copper tablets'),
 '136': ('āḷ', 'man, worker (a person sign; counted)', '399', 'picture: person (M38); slot: last or counted'),
 '844': ('cūṭu', 'bundle of sheaves (two overlapping leaves, variant of 845)', '', 'picture: two overlapping leaves like 845'),
 '603': ('kutir', 'grain bin (tall hatched box, variant of 605)', '1716?', 'picture: tall box with bars like 605'),
 '098': ('kōṉ', 'lord, king (person with a raised arm)', '2177', 'picture: person with an arm raised; slot: text-first 7 of 10'),
 '408': ('kiḷai', 'kindred, family (tree; stands for 407 in the goat copper set variant)', '2018', 'picture: the branched tree; the copper text 220-017-585-095-520-032-408 is the goat set with 408 for 407'),
 '406': ('kiḷai', 'kindred, family (variant of 407: one sign M169 in the second catalogue)', '2018', 'merge: M169 = 405 + 406 + 407; main sign 407'),
 '336': ('ūr', 'town (variant of 335)', '', 'picture: 335 with extra strokes; second catalogue M193 holds 336/337'),
 '621': ('katavu', 'door, gate (a frame with a dividing bar)', '1187', 'picture: double-leaf door (M242); slot: first or last'),
 '323': ('paṭi', 'ration measure (variant of 320)', '3849', 'merge: the second catalogue draws 323 as 320 (M182)'),
 '243': ('vēymīn', 'Bamboo-star (hatched caret-hat fish, variant of 235)', '', 'picture: the caret-hat fish 235 with hatching'),
 '130': ('ur̤avaṉ', 'ploughman, cultivator (person with a rake)', '688', 'picture: person holding a rake/pitchfork (M19); slot: counted 10 of 17'),
 '697': ('valai', 'net (crossed diamond)', '5288', 'picture: a diamond with crossing sticks (M276), a net'),
 '776': ('pū', 'flower, bloom (three-stemmed plant)', '4345', 'picture: flowering plant like 777/782'),
 '642': ('pal', 'many (variant of 630/632/636)', '', 'merge: the second catalogue draws 642 as 630 (M244)'),
 '101': ('mutu', 'elder (bracketed three-headed person, variant of 100)', '', 'picture: 100 inside brackets (M9)'),
 '804': ('il', 'house (caged leaf-on-tree, variant of 803)', '494', 'picture: 803/806 inside the four-stroke cage'),
}
TESTS = [
 ('321', 'A', 'one word with the ration rung: 321 stands in the frames of 320/323', lambda: frame_swap('321', {'320', '323'})),
 ('321', 'B', 'a ration word lives on records: faces with 321 sit on copper/moulded tablets more than all faces', lambda: tabs('321')),
 ('592', 'A', 'a container: faces with 592 carry a goods word (fish, crate of fish, cotton, grain, produce, chest, forge, cup, kalam)', lambda: frac_with('592', GOODS)),
 ('592', 'B', 'one word family with the chest: 592 stands in the frames of 590', lambda: frame_swap('592', '590')),
 ('703', 'A', 'a measured amount: a number stands two places before or after 703', lambda: two_away('703', set(VAL), offs=(-2, 2))),
 ('703', 'B', 'a record word: faces with 703 sit on copper/moulded tablets more than all faces', lambda: tabs('703')),
 ('773', 'A', 'maka: 773 stands in the frames of 752/760', lambda: frame_swap('773', {'752', '760'})),
 ('773', 'B', '"child of [Star] house": faces with 773 carry a fish crest more than faces overall', lambda: frac_with('773', CREST)),
 ('772', 'A', 'one sign with 773: 772 stands in the frames of 773', lambda: frame_swap('772', '773')),
 ('772', 'B', 'maka: 772 stands in the frames of 752/760', lambda: frame_swap('772', {'752', '760'})),
 ('927', 'A', 'one word with 904: 927 stands in the frames of 904', lambda: frame_swap('927', '904')),
 ('927', 'B', 'a date word: faces with 927 carry month/day words or the joiner (900, 920, 165, 060)', lambda: frac_with('927', {'900', '920', '165', '060'})),
 ('554', 'A', 'one word with the bowtie measure: 554 stands in the frames of 540/530', lambda: frame_swap('554', {'540', '530'})),
 ('554', 'B', 'a measure takes tall counts: a tall-stroke number stands within two places of 554', lambda: two_away('554', TALLN, offs=(-2, -1, 1, 2))),
 ('064', 'A', 'one word with cotton: 064 stands in the frames of 390', lambda: frame_swap('064', '390')),
 ('064', 'B', 'cotton goes with the spindle and the chest: faces with 064 carry 370/371/590/405 more than faces overall', lambda: frac_with('064', {'370', '371', '590', '405'})),
 ('422', 'A', 'one word with 421/423/424: 422 stands in their frames', lambda: frame_swap('422', {'421', '423', '424'})),
 ('422', 'B', 'land goes with crops: faces with 421-424 carry a crop or land word more than faces overall', lambda: frac_with('422', CROP | {'503'})),
 ('136', 'A', 'a man word: 136 stands in the frames of the man 090', lambda: frame_swap('136', '090')),
 ('136', 'B', 'workers get rations: faces with 136 carry the cup, grain or a measure (700, 413, 705, 706, 711, 575)', lambda: frac_with('136', {'700', '413', '705', '706', '711', '575'})),
 ('844', 'A', 'one word with the sheaves: 844 stands in the frames of 845', lambda: frame_swap('844', '845')),
 ('844', 'B', 'sheaves go with crops: faces with 844 carry another crop word', lambda: frac_with('844', CROP - {'845'})),
 ('603', 'A', 'one word with the grain bin: 603 stands in the frames of 605', lambda: frame_swap('603', '605')),
 ('603', 'B', 'grain bins are in the granary mound: Harappa objects with 603 lie in mound F', lambda: harappa_area('603', 'F')),
 ('098', 'A', 'a person title: 098 stands in the frames of the person signs 090/095/140/142', lambda: frame_swap('098', {'090', '095', '140', '142'})),
 ('098', 'B', 'a lord: seals with 098 are bigger than seals with the same number of signs', lambda: seal_size('098')),
 ('408', 'A', 'one word with 407: 408 stands in the frames of 407', lambda: frame_swap('408', '407')),
 ('408', 'B', 'kindred in names: faces with 408 carry a fish crest', lambda: frac_with('408', CREST)),
 ('406', 'A', 'one word with 407: 406 stands in the frames of 407', lambda: frame_swap('406', '407')),
 ('406', 'B', 'kindred in names: faces with 406 carry a fish crest', lambda: frac_with('406', CREST)),
 ('336', 'A', 'one word with the town: 336 stands in the frames of 335', lambda: frame_swap('336', '335')),
 ('336', 'B', 'a town of the grain records: faces with 336 sit on tablets more than all faces', lambda: tabs('336')),
 ('621', 'A', 'a door word: 621 stands in the frames of the gate 550/555 or the guard 525/526/527', lambda: frame_swap('621', {'550', '555', '525', '526', '527'})),
 ('621', 'B', 'a door belongs to a house: Mohenjo-daro house-mates both carry 621', lambda: house_share('621', where='any', seals=False)),
 ('323', 'A', 'one word with 320: 323 stands in the frames of 320', lambda: frame_swap('323', '320')),
 ('323', 'B', 'the monthly allowance: faces with 323 carry the month 920/900', lambda: frac_with('323', {'920', '900'})),
 ('243', 'A', 'one word with the Bamboo-star: 243 stands in the frames of 235', lambda: frame_swap('243', '235')),
 ('243', 'B', 'a crest in a chain of crests: faces with 243 carry another fish crest', lambda: frac_with('243', CREST - {'243'})),
 ('130', 'A', 'a threshing-floor worker: Harappa objects with 130 lie in mound F (granary and threshing floors)', lambda: harappa_area('130', 'F')),
 ('130', 'B', 'a cultivator goes with crops: faces with 130 carry a crop word', lambda: frac_with('130', CROP)),
 ('697', 'A', 'a net catches fish: faces with 697 carry a fish sign (plain, crate, scabbard-fish)', lambda: frac_with('697', {'220', '226', '233'})),
 ('697', 'B', 'nets at the coast: faces with 697 lie at Lothal, Chanhu-daro, the Gujarat sites or abroad', lambda: sites('697', {'Lothal', 'Chanhu-daro', 'abroad', 'Dholavira', 'Kanmer', 'Desalpur', 'Surkotada', 'Gola Dhoro (Bagasra)', 'Bala-kot'})),
 ('776', 'A', 'one word family with the flowering plants: 776 stands in the frames of 777/782', lambda: frame_swap('776', {'777', '782', '780', '781'})),
 ('776', 'B', 'flowers go with crops: faces with 776 carry a crop word', lambda: frac_with('776', CROP)),
 ('642', 'A', 'one word with "many": 642 stands in the frames of 630/632/636', lambda: frame_swap('642', {'630', '632', '636'})),
 ('642', 'B', '"many" takes no number: faces with 642 carry a number less than faces overall', lambda: share_less(np.array([any(a in VAL for a in x) for x, P, s_, g_ in faces_all('LM')]), np.array([any(a in VAL for a in x) for x, P, s_, g_ in faces_all('LM') if '642' in x]), 'faces with 642 that carry a number (LM)')),
 ('101', 'A', 'one word with the elder: 101 stands in the frames of 100', lambda: frame_swap('101', '100')),
 ('101', 'B', 'elders outrank: seals with 101 are bigger than seals with the same number of signs', lambda: seal_size('101')),
 ('804', 'A', 'one word with the house: 804 stands in the frames of 803', lambda: frame_swap('804', '803')),
 ('804', 'B', '"house" before a star name: a fish crest follows 804', lambda: adjacent('804', CREST, 'next', 'LM')),
]
if __name__ == '__main__':
    for s, st, p, f in TESTS: print(f'[{st}] {s} {W[s][0]}: {p}', flush=True)
    print('---- computing ----', flush=True)
    out = [run(st, s, W[s][0], p, f) for s, st, p, f in TESTS]
    pd.DataFrame(out).to_csv(f'{OUT6}/job3_tests.csv', index=False)
