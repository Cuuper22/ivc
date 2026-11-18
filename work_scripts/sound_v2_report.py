#!/usr/bin/env python3
"""Writes jobs/out/sound_list_v2.md from the result tables in work_data/sound_v2/ (run the other sound_v2_*.py first)."""
import os, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_values import VALUES, OLD
from sound_v2_tiers import V2, TIER, CLASS, CHANGED
R = '/home/antigravity/Cuuper22/ivc/work_data/sound_v2'
PIC = {s: pic for (s, pic, *_ ) in VALUES}
ck = pd.read_csv('/home/antigravity/Cuuper22/ivc/work_data/sound/checks.csv', dtype=str).set_index('sign')
t1 = pd.read_csv(f'{R}/try1.csv', dtype=str).fillna('').set_index('sign')
t2 = pd.read_csv(f'{R}/try2.csv', dtype=str).fillna('').set_index('sign')
sh = pd.read_csv(f'{R}/sharpen.csv', dtype=str).fillna('').set_index('sign')
sr = pd.read_csv(f'{R}/seen_rerun.csv', dtype=str).fillna('').set_index('sign')
ex = pd.read_csv(f'{R}/extra.csv', dtype=str).fillna('').set_index('run')


def p(x): return f', P {x}' if x not in ('', 'nan') else ''


def evidence(s):
    e = []
    if s in ck.index: e.append(f'first check ({ck.loc[s, "prediction"]}): {ck.loc[s, "came_true"]}, {ck.loc[s, "result"]}{p(ck.loc[s, "p"])}')
    if s in sr.index: e.append(f'same check on new second-catalogue texts: {sr.loc[s, "outcome"]}, {sr.loc[s, "result"]}{p(sr.loc[s, "p"])}')
    if s in sh.index: e.append(f'sharpened ({sh.loc[s, "test"]}): {sh.loc[s, "outcome"]}, {sh.loc[s, "result"]}{p(sh.loc[s, "p"])}')
    if s in t1.index: e.append(f'try 1, same word, better test ({t1.loc[s, "test"]}): {t1.loc[s, "outcome"] or "too few cases"}, {t1.loc[s, "result"]}{p(t1.loc[s, "p"])}')
    if s in t2.index: e.append(f'try 2, new word {t2.loc[s, "new_word"]}; prediction: {t2.loc[s, "prediction"]}: {t2.loc[s, "outcome"]}, {t2.loc[s, "result"]}{p(t2.loc[s, "p"])}')
    for k in ex.index:
        if k.split()[0] == s: e.append(f'{k}: {ex.loc[k, "test"]}: {ex.loc[k, "outcome"]}, {ex.loc[k, "result"]}{p(ex.loc[k, "p"])}')
    return ' / '.join(e)


def table(signs):
    L = ['| sign | picture | sound | English | evidence |', '|---|---|---|---|---|']
    for s in signs:
        L.append(f'| {s} | {PIC.get(s, "")} | *{V2[s][0]}* | {V2[s][1]} | {evidence(s)} |')
    return '\n'.join(L)


new = [s for s in V2 if s not in OLD]
B = sorted([s for s in new if TIER[s] == 'building']); T = sorted([s for s in new if TIER[s] == 'testing']); P_ = sorted([s for s in new if TIER[s] == 'paused'])
LEARN = {
 '226': 'seal-heavy (25 of 38), counted with two tall strokes 11 times, texts end with no owner ending; neither a star name nor a no-animal goods sign. Lead: a container named on seals.',
 '236': 'only 26 uses, ends texts, comb follows 7 times; not in houses, not in the granary mound (2 of 8).',
 '705': 'counted with three tall strokes (114 tall against 14 short) and 705-033 is a fixed pair, yet not a granary sign (34% against 34%) and not with the cup on one object (25 against 25.8). Lead: 705-033 is a name ("three vessels") rather than a quantity.',
 '706': 'same as 705; with the cup 3 times against 12 expected: it keeps away from cups.',
 '550': 'average spread over cities; faces with it carry a number less than chance (57 against 66.4). It heads the 550-060 cap and the 550-527 pair: an office, wordless for now.',
 '900': 'counts beside it stop at five (1 of 67 above five, a month would put about 3 in 8 there); not shared before the jar in houses. Learned: a small-count unit (1 to 5) that closes names before the jar.',
 '692': 'fewer cities than its peers (6 against 8) and not on sealings (3 of 16); big seals, cap head, opens agents\' masters\' names. An outside office, wordless for now.',
 '435': 'always inside 255-435-(690|156); fewer cities (6 against 8); names with it rarely take spear or porter (1 of 23). It is the fixed middle of one long name; the name, not the sign, is the unit.',
 '527': 'never shared in houses; faces with it carry fewer numbers than chance (26 against 32.3); always after 550/555 at the text end. Read with 550 as one title.',
 '416': 'no house sharing, not local (top city 48% against 57%).',
 '413': 'not in mound F even among tablets (9 of 40 against 35%); never on an object with a crescent (0 against 2.0). It sits in the tablet phrase 413-575-335-711: a tablet formula word.',
 '350': 'not in houses; carries an animal more than objects overall (37 of 47 with an animal): an owner word, not a goods word.',
 '923': 'not before the jar in houses (0 against 0.94); does not share frames with the crescent 900 (4 against 4). Copper-tablet and elephant sign at Mohenjo-daro.',
 '495': 'names with it take the jar less than names overall (5 of 9 against 71%).',
 '097': 'seals not smaller at equal sign count (x1.06); its names take the carrier ending (5 of 6 in Lipi). Lead: the person between two bars is a carrier title.',
 '388': 'pointed the right way on raw size (638 against 604) but not at equal sign count (x0.94); no opener excess (7 of 61); never "X\'s man" (0 of 19). The three pipal signs do not share slots (homophone test P 0.35 to 0.60): they are not one word.',
 '384': 'x0.95 at equal sign count; opener 1 of 31; never jar+man.',
 '382': 'frames shared with 388/384 3 against 3; opener 1 of 16.',
}

head = f'''# Sound list, second version: rescue tries, sharper tests, the whole read together

Scripts (in `work_scripts/`, run in this order): `v2_common.py` (loader and test kit: Lipi objects, Mohenjo-daro houses with 3-ft depth bands, the second catalogue mapped through the crosswalk, with its texts that have no Lipi partner kept apart as new texts), `sound_v2_try1.py`, `sound_v2_try2.py` (try 2 and the sharpened reruns), `sound_v2_extra.py`, `sound_v2_seen.py`, `sound_v2_tiers.py` (this table), `sound_v2_consistency.py`, `sound_v2_readings.py` (`READINGS.md`), `sound_v2_report.py` (this file), `v2_dedr.py` (dictionary look-up). Tables: `work_data/sound_v2/`. Reading order = stored order reversed. "New texts" = second-catalogue texts with no partner in the first catalogue (1,183 lines), never used to choose any value. Word choices are guesses; DEDR numbers are entries in the local copy of the Dravidian Etymological Dictionary.

## Tiers now (89 values of the second list)

- **Building on: {len(B)}** (a prediction came true: fresh, or on new texts)
- **Testing: {len(T)}** (pointing the right way, or a first check whose fact was seen while choosing and has not yet been rerun on enough new texts)
- **Paused: {len(P_)}** (two rescue tries spent)
- Base under all of them: the first values (jar *kuṭi*, man *āḷ*, fish *mīn*, spear *vēḷ*, comb *ciṟ*, carriers *kā*, staff-bearer *kō*, tree *maṟam*, three-headed person *mutu*) and the numbers.

## What moved

1. **590 is *peṭṭi* "chest, strongbox" (DEDR 4388), and the nine-city name reads.** The box-with-pole is counted with tall strokes, the container series, on new texts: tall 8, short 3 (73% against 35% for all counts, P 0.012). The old reading *paṭṭi* "hamlet" went against twice (house sharing 6 against 7.6; not local to one city, 45% against 51%). With the chest, `590-390` on 71 objects in 9 cities (Kish and Gonur included) reads *peṭṭi maṟam*, "Chest-guard": the trading house is named for the strongbox it guards. The 7-city office prefix joins it on one stone: `920-060-741-590-390-151` reads "Office stamp, first ward: Chest-guard the carrier" (READINGS 39). A value fixed by counting strokes on unseen texts explains the travelling name and the office stamp at once.
2. **231 is *oru-mīn* "First-star".** The dotted fish is the plain fish plus one short stroke, the way the marked fish are mark + plain fish. "First" predicts a senior house: names with it carry a holding opener 31 of 106 times against 12% for all names (P 0.0000016).
3. **480 is *kuṉṟi*, the Abrus seed used as a goldsmith\'s weight (DEDR 1865, 4636).** A weight unit takes its number after it: on new texts the next sign is a count 5 of 6 against 14% (P 0.0003); both catalogues 27 of 39 against 15%.
4. **Same word, same slot.** Signs given one word sit in the same slots far more than signs of the same frequency: 13 of 33 same-word pairs at P 0.10 or less, where chance gives 3.3 (carriers 151/154/156/158, *kaḷam* 705/706, *kiḷai* 405/407, *maka* 760/752, *mukkōṭu* 460/463, *kāṇi* 861/817). The ones that fail split words the table had merged: the three pipal signs are not one *aracu*, and 061 is not the wheel's *kāl*.
5. **Head-last order holds inside names:** house and place words before kin and title words 121 times, the other way 59. **Endings agree with the last word of the name:** names ending in a kin word (*maka* child, *kiḷai* kindred, *piṇai* allied) take the "house of" jar 151 of 182 times; texts ending in a goods word carry no owner ending 92 of 154 times; house-crest-final names are where the spear goes (70 of the 87 spear texts whose name ends in a sounded sign).
6. **Sharper tests on the pointing-the-right-way values:** 235 *vēy-mīn* "Bamboo-star" is shared by house-mates at seal level, shuffled within area and 3-ft depth band, 30 pairs against 20.0 (P 0.037); 741 *oru-kuṭi* "first ward" 18 against 10.3 (P 0.038); 752 stands in the frames of 760 (*maka* "child of", 11 shared frames against 1, P 0.02); 632 in the frames of 630 (*pal*, 6 against 2, P 0.024).
7. **Rescued with a better test of the same word:** 585 is counted seven on new texts (27 of 31 counts before it; the "Seven Maidens"); 070 *ampu* "arrow" stands before the spear on new texts 3 of 10 against 1.2%; 091 *iruvar* "the pair" opens the text on new texts 6 of 6 against 29%; 904 *iru-tiṅkaḷ* sits on a face with a number 41 of 76 against 34.1; 125 *vēṭṭuvaṉ* "Hunter (clan)" seals carry one animal 35 of 39 against 75%. 463 is 460 written another way (three peaks, frames 3 against 1); 530 is the drum 540 (*paṟai*, frames 3 against 1); 482 *kōṭu-kāṇi* "hill share" names take the plain jar 16 of 16 against 71%.
8. Eight values whose first check used a fact seen while choosing the word hold on new texts: 798 *maru-* before the jar 7 of 32 against 10%; 892 *vil* "sale" off seals 18 of 27 against 45%; 095 *kōlaṉ* 9 of 10; 500 10 of 12; the wheel 820 counted 3 or less 30 of 30; the cap selector after 060 falls 7 > 2 > 0 (920, 742, 745).

## Against, then what was done

- The month reading of 900 *tiṅkaḷ* is paused: counts beside the crescent stop at five, 1 of 67 above five where a month count would put about 3 in 8; the second word (*maruppu* ~ *marukaṉ* "descendant") found no house pairs before the jar (0 against 0.19). What it is: a small count unit, 1 to 5, closing names right before the jar. The day sign 165 moves to *poḻutu* "time, day" (DEDR 4559) and stays in testing.
- *aracu* "king" for the pipal signs 388/384/382 is paused: not bigger at equal sign count (x0.94, x0.95), no excess of holding openers (7 of 61), never "X\'s man" (0 of 19).
- 18 values paused in all; each keeps what its failed checks taught (table 3).

## Nonsense finder: which values make bad strings

Read over the 1,386 distinct complete texts with a sound on every sign (1,302 of two signs or more; Lipi + new texts):
- **798 *maru-* "descendant"** is the weak one in names: 30 of its 65 uses in sounded names put the kin word before a house crest (`798-415`, `798-240`: "descendant + Branch", "descendant + High-star"), against the head-last order every other kin word keeps. Before the jar it works (new texts 7 of 32). Reading on the table: 798 is two words, a name-front word and the pre-jar kin word.
- **061 *kāl* "quarter"** shares no slots with the wheel 820 *kāl* (homophone test P 0.70), and its count ceiling failed on new texts (3 of 5 counts at three or less). The wheel keeps *kāl*; 061 needs a new word.
- **Measure words take their number after them**: 171 (10 of 11 uses), 480 (8 of 13), 705 and 706 (66 of 174). The cup and the crop take theirs before. Goods words overall: number before 141, number only after 121. Two orders for two kinds of word (measure + number; number + thing counted): this is the pattern the grammar should carry, not a fault in 480.
- 091 *iruvar* breaks name order because it is an opener, not a name word (6 of 6 text-initial on new texts).

## 1. Building on ({len(B)})

{table(B)}

## 2. Testing ({len(T)})

{table(T)}

## 3. Paused ({len(P_)}), with what was learned

| sign | picture | last sound | what the failed checks taught | evidence |
|---|---|---|---|---|
'''
rows = [f'| {s} | {PIC.get(s, "")} | *{V2[s][0]}* | {LEARN.get(s, "")} | {evidence(s)} |' for s in P_]
tail = f'''

## Values that changed word in this pass

| sign | new sound | English | source |
|---|---|---|---|
''' + '\n'.join(f'| {s} | *{a}* | {b} | {c} |' for s, (a, b, c) in CHANGED.items()) + '''

## Next tests (one per testing value is in its row; the strongest leads)

- 798 split: name-front 798 against pre-jar 798 as two signs; check whether the two uses differ in drawing on the photographs.
- Measure order: list every sign that takes its number after it (705, 706, 171, 480 and others); if they are all measures and never names, the measure + number order becomes a grammar rule for the parser.
- 590 *peṭṭi*: chest-guard seals (`590-390`) should sit with goods (tags, sealings) and in warehouse findspots (Lothal SRG 3GX 10, Harappa mound F) more than other names.
- 061 new word: a leg (*tāḷ*, DEDR 3185, is now 717's) or a foot measure; first check its counts on all texts.
'''
open('/home/antigravity/Cuuper22/ivc/jobs/out/sound_list_v2.md', 'w').write(head + '\n'.join(rows) + tail)
print('written', len(B), len(T), len(P_))
