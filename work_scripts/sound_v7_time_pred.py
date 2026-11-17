#!/usr/bin/env python3
"""JOB 2, PREDICTIONS (written in one go on 2026-11-17, before sound_v7_time.py computed any number by time bin).

Every strict and wide value was chosen without looking at dates. If the word is real, the sign does the job the word
says in early, middle and late objects alike. Each value gets ONE CLASS from what its word means (not from data by bin);
the class names the behaviour (the "signature") the sign must show in every time bin:

  NAME     a house / person / crest word: a jar 740 or a closing title stands LATER in the same text
  TITLE    a closing title (manager, junior, chief, keeper, guard, deputy, servant, throne): it is the LAST sign of the text
  ENDING   the jar 740: last sign, or followed directly by a title
  KIN      "child of": the jar 740 follows directly
  MEASURE  a measure / share word that takes its count after it: a number sign directly AFTER it
  THING    a counted thing: a number sign directly BEFORE it
  OPENER   a front word (month head, assembly, quarter, share opener, grain header): the FIRST sign of the text
  GOODS    a goods / transaction word: the object is not a seal (tablet, tag, pot, tool, rod, bangle, copper tablet)
  KINDRED  kindred 406/407: a fish crest (220 226 231 233 235 236 240) on the same face
  JOINER   060 "of": its left neighbour is a head word (month 920/900, gate 550/555, quarter 820, assembly 692)
  LOAD     the A-comb load counts 465-475: produce 806 directly after it

RULE for one bin (written before computing): take every use of the sign on dated Lipi faces of that bin. With 3 or more
uses the value HOLDS in that bin if the share of uses showing the signature is above the same share for all
non-number sign uses of that bin (the bin's base), and FAILS if it is at or under it. Under 3 uses the bin has no data.
A real word holds in every bin it has data for; a word fitted to noise holds in the middle bin (which holds most of the
dated data) and fails in early or late.

SAMENESS (the four facets the brief names): for each value with 3+ uses in at least two bins, slot (first / middle / last),
object kind (seal / moulded tablet / other goods), left neighbour class and right neighbour class are compared across
bins (chi-square), with bins shuffled among the sign's own uses within site 2,000 times. Prediction: a real word's
facets do not change with time; at P 0.05 about 5% of values would show a change by chance alone.

RIVAL (the strongest other explanation: the grammar positions are so stable that ANY class would hold in every bin):
the classes are shuffled among the values 1,000 times and the number holding in all bins with data is counted again.
Prediction: the real classes hold in all bins far more often than shuffled classes.

TESTING VALUES (26): each gets two rival words with their classes (RIVALS). Prediction: the word whose signature is
stronger (share over base) in the EARLY bin alone is the right one, and it stays the stronger in middle and late.
"""
CLASS = {}
for s in ['070', '091', '095', '100', '101', '104', '125', '140', '142', '175', '176', '220', '231', '233', '235', '240', '255', '335', '336',
          '347', '382', '384', '388', '415', '435', '455', '463', '491', '495', '503', '519', '550', '555', '565', '585', '590', '605', '611',
          '615', '630', '632', '636', '642', '690', '741', '742', '745', '798', '803', '806', '838', '840', '904', '927', '055']:
    CLASS[s] = 'NAME'
for s in ['090', '151', '152', '153', '154', '155', '156', '157', '158', '161', '368', '400', '520', '525', '526', '527', '617', '679', '717', '842']:
    CLASS[s] = 'TITLE'
CLASS['740'] = 'ENDING'
for s in ['752', '760', '772', '773']: CLASS[s] = 'KIN'
for s in ['705', '706', '711', '575', '540', '171', '850', '861', '877', '320', '321', '323', '480', '482']: CLASS[s] = 'MEASURE'
for s in ['700', '390', '405', '421', '422', '423', '424', '845', '844', '097', '137', '226', '061', '868', '900']: CLASS[s] = 'THING'
for s in ['920', '692', '820', '824', '817', '413', '530']: CLASS[s] = 'OPENER'
for s in ['416', '440', '500', '501', '890', '892', '923', '831', '790', '595', '370', '371']: CLASS[s] = 'GOODS'
for s in ['406', '407']: CLASS[s] = 'KINDRED'
CLASS['060'] = 'JOINER'
for s in [f'{i}' for i in range(465, 476)]: CLASS[s] = 'LOAD'

# testing values: (word A, class A, word B, class B); A = the sixth-pass word
RIVALS = {
 '048': ('er̤uvar "the Seven"', 'NAME', 'kōvai "string of seven beads"', 'GOODS'),
 '064': ('kavar "fork"', 'NAME', 'parutti "cotton"', 'THING'),
 '098': ('ammai "lady"', 'NAME', 'kōṉ "lord"', 'TITLE'),
 '130': ('aṭiyāṉ "servant"', 'TITLE', 'ur̤avaṉ "ploughman" (counted worker)', 'THING'),
 '136': ('aṭimai "bondsman" (counted)', 'THING', 'āḷ "man"', 'TITLE'),
 '165': ('poḻutu "day" (counted)', 'THING', 'nāḷ "date" (head of a date phrase)', 'OPENER'),
 '222': ('aṭaimīn "shut-in fish" (crest)', 'NAME', 'kuḷamīn "pond fish" (a good)', 'THING'),
 '236': ('vēymīn (crest)', 'NAME', 'vēy-kūṭu "bamboo cage" (container)', 'THING'),
 '243': ('vāḷai "scabbard-fish" (a counted good)', 'THING', 'vēymīn (crest)', 'NAME'),
 '341': ('kalai "stag" (record mark on goods)', 'GOODS', 'kalai "Stag" (name word)', 'NAME'),
 '391': ('kollaṉ "smith" (title)', 'TITLE', 'kollaṉ (maker\'s mark on goods)', 'GOODS'),
 '408': ('kiḷai "herd, lot" (counted)', 'THING', 'kiḷai "kindred"', 'KINDRED'),
 '417': ('kā "pole-load" (counted)', 'THING', 'kā "keeper"', 'TITLE'),
 '460': ('mukkōṭu "Three-peaks" (name)', 'NAME', 'mukkōṭṭai "three stores" (goods)', 'GOODS'),
 '554': ('paṟai "grain measure"', 'MEASURE', 'paṟai "proclamation"', 'OPENER'),
 '592': ('paṭṭi "hamlet"', 'NAME', 'kūṭu "crate"', 'GOODS'),
 '603': ('katavu "door" (door-keeper title)', 'TITLE', 'kutir "grain bin"', 'GOODS'),
 '621': ('kōṭṭai "store" (a measure)', 'MEASURE', 'katavu "door" (title)', 'TITLE'),
 '645': ('kar̤añcu "gold weight"', 'MEASURE', 'kuṟi "mark, tally" (counted)', 'THING'),
 '697': ('kaṭṭu "bundle" (counted)', 'THING', 'valai "net" (goods)', 'GOODS'),
 '703': ('nāḻi "cup" (counted)', 'THING', 'aḷavu "measure"', 'MEASURE'),
 '776': ('pū "Flower" (name)', 'NAME', 'pū "flowers" (goods)', 'GOODS'),
 '792': ('maṇi "gem"', 'GOODS', 'aracu "royal"', 'NAME'),
 '804': ('kūṭu "crate"', 'GOODS', 'il "house"', 'NAME'),
 '821': ('veṟṟilai "betel"', 'GOODS', 'kāl "quarter" (opener)', 'OPENER'),
 '832': ('kaṇ "eye" (name word)', 'NAME', 'maṇi "gem"', 'GOODS'),
}
