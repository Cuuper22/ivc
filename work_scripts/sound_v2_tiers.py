#!/usr/bin/env python3
"""Second sound list: every value after the rescue tries, in three tiers, with a word class used by the
consistency pass.  Writes work_data/sound_v2/values_v2.csv.  Import: from sound_v2_tiers import V2, CLASS, TIER"""
import os, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_values import VALUES, OLD
OUT = '/home/antigravity/Cuuper22/ivc/work_data/sound_v2'

# sign -> (sound, English)
V2 = {s: (snd, gl) for (s, pic, pw, jw, snd, gl, kind, t) in VALUES}
for s, (snd, gl) in OLD.items(): V2.setdefault(s, (snd, gl))
CHANGED = {
 '231': ('orumīn', 'First-star', 'oru one (DEDR 990, inside the 1025 block) + mīṉ star (4885); the mark is one stroke'),
 '480': ('kuṉṟi', 'seed-weight', 'kuṉṟi Abrus seed (1865), a goldsmith\'s weight unit (4636)'),
 '482': ('kōṭukāṇi', 'hill share', 'kōṭu summit (2049) + kāṇi share (1444): the outlined peak with the diamond inside'),
 '590': ('peṭṭi', 'chest', 'peṭṭi box, chest (4388), the picture word itself; counted with tall strokes like containers'),
 '595': ('peṭṭi', 'chest', 'as 590'),
 '617': ('ūḻiyaṉ', "(king's) servant", 'ūr̤iyaṉ slave, servant; Ma. ūr̤an servant of kings (758)'),
 '717': ('tāḷ', 'stem (of a line)', 'tāḷ foot, foot of a tree, stem (3185)'),
 '832': ('kaṇṇi', 'tender leaf', 'kaṇṇi sprout, shoot, tender leaf (1185)'),
 '165': ('poḻutu', 'time, day', 'por̤utu, pōtu time, sun, day (4559)'),
}
for s, (snd, gl, src) in CHANGED.items(): V2[s] = (snd, gl)

FRESH_YES = ['861', '817', '176', '415', '255', '405', '368', '455', '555', '679']
NEWTEXT_YES = ['798', '892', '095', '820', '920', '742', '745', '500']
SHARP_YES = ['235', '741', '752', '632']
TRY1_YES = ['904', '585', '125', '070', '091', '501']
TRY2_YES = ['231', '480', '463', '530', '482', '590']
BUILD = FRESH_YES + NEWTEXT_YES + SHARP_YES + TRY1_YES + TRY2_YES
PAUSED = ['226', '236', '705', '706', '550', '900', '692', '435', '527', '416', '413', '350', '923', '495', '097', '388', '384', '382']
TIER = {}
for s, _ in V2.items(): TIER[s] = 'base' if s in OLD else 'testing'
for s in BUILD: TIER[s] = 'building'
for s in PAUSED: TIER[s] = 'paused'

# word classes for the consistency pass (guess, from slot + meaning)
CLASS = {}
for s in OLD:
    CLASS[s] = 'NUM' if OLD[s][1] in ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'n loads') else 'X'
CLASS.update({'740': 'POSS', '090': 'REL', '520': 'END', '400': 'END', '220': 'HOUSE', '142': 'TITLE', '390': 'SELF', '100': 'TITLE',
              '700': 'GOODS', '806': 'GOODS'})
for p in ('151', '153', '154', '155', '156', '157', '158'): CLASS[p] = 'END'
HOUSE = '235 240 233 231 236 415 803 140 125 368 503 741 742 745 482 460 463 615 495 416'.split()
KIN = '760 752 798 405 690 923 840 717'.split()
TITLE = '255 617 679 388 384 382 091 097 095 070 435'.split()
GOODS = '705 706 575 480 590 595 501 226 838 055 171 530 540 700 806 407 645 711 335 845 824 167 500 630 632 636 350'.split()
TIME = '904 165 900'.split()
TRANS = '892 440 176 175 550 527 850 790 832'.split()
OPEN = '861 817 820 920 692 877 061'.split()
for grp, lab in ((HOUSE, 'HOUSE'), (KIN, 'KIN'), (TITLE, 'TITLE'), (GOODS, 'GOODS'), (TIME, 'TIME'), (TRANS, 'TRANS'), (OPEN, 'OPEN')):
    for s in grp: CLASS[s] = lab
for s in V2: CLASS.setdefault(s, 'SELF')

if __name__ == '__main__':
    rows = [dict(sign=s, sound=V2[s][0], english=V2[s][1], tier=TIER[s], word_class=CLASS[s], changed=CHANGED.get(s, ('', '', ''))[2]) for s in sorted(V2)]
    pd.DataFrame(rows).to_csv(f'{OUT}/values_v2.csv', index=False)
    t = pd.DataFrame(rows); print(t[~t.sign.isin(OLD)].tier.value_counts().to_dict(), 'base', (t.tier == 'base').sum())
