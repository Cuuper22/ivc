#!/usr/bin/env python3
"""Writes jobs/out/sound_list_v4.md from the tables in work_data/sound_v4/ (run after sound_v4_job1.py,
sound_v4_job2.py, sound_v4_job2b.py, sound_v4_values.py, sound_v4_cands.py, sound_v4_readings.py).
The prose sections are written here by hand from those tables."""
import csv, collections
import pandas as pd
ROOT = '/home/claude/ivc'; O = f'{ROOT}/work_data/sound_v4'
SH = pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv', dtype=str).set_index('lipi_wells_number').shape_description.to_dict()
V = pd.read_csv(f'{O}/values_v4.csv', dtype=str).fillna('')
J1 = pd.read_csv(f'{O}/job1_tests.csv'); G = pd.read_csv(f'{O}/job1_grade.csv')
J2 = pd.concat([pd.read_csv(f'{O}/job2_tests.csv'), pd.read_csv(f'{O}/job2b_tests.csv')])
C = pd.read_csv(f'{O}/coverage_v4.csv')
U = pd.read_csv(f'{O}/job1_uses.csv')
def pic(s): return (str(SH.get(s, '')) or '(shape not described)').split(';')[0][:70]
def cov(lst, g): r = C[(C.list == lst) & (C.group == g)].iloc[0]; return r
L = []
A = L.append
A('# Sound list, fourth version: kalam the measure, and the coverage push')
A('')
A('Scripts (in `work_scripts/`, run in this order): `sound_v4_common.py` (third-pass loader plus the coverage counter and the gain table), `sound_v4_job1.py` (705/706: measure against ship), `sound_v4_job2.py` (the 25 signs, predictions A, B, C), `sound_v4_job2b.py` (rescue tests), `sound_v4_values.py` (the list and the coverage numbers), `sound_v4_cands.py` (texts that became readable), `sound_v4_readings.py` (READINGS 61-80), `sound_v4_report.py` (this file). Tables: `work_data/sound_v4/`.')
A('')
A('Plain words used below:')
A('- **Readable start to finish** (or "reads whole"): every sign on the face is a number, a base value (jar, man, fish, spear, comb, carriers, staff-bearer, tree, elder, cup, load comb) or a value we are **building on**. Counted on the 3,600 complete faces of the first catalogue (Lipi); "distinct texts" counts each different sign string once.')
A('- **Building on / testing / paused**: building on = a prediction made for the word came true and we read with it; testing = no prediction has come true yet, or it could only be checked on data already looked at; paused = three different tries came up empty.')
A('- **New texts**: the 1,183 lines of the second catalogue (Mahadevan 1977) with no partner in the first. They were never used to choose a value, so a prediction that comes true there is a prediction in the full sense.')
A('- **fresh / seen**: fresh = the fact a prediction was checked against had not been printed while the word was chosen. Seen = it had been visible in the sign profiles printed while choosing (top neighbours, object kinds, top sites). A value that came true only on a seen fact is building on in the **wide** list and still testing in the **strict** list; both numbers are given.')
A('- **P** = how often chance alone gives a result at least this strong (P 0.01 = once in a hundred). Small P points to the word being right; P near 1 points the other way. "yes" = right direction with P at or under 0.1.')
A('- **Count after / before**: a number sign (short strokes or tall strokes) right after or before a sign. **Tall strokes** are the container count series, **short strokes** the series for other things.')
A('- **Gain** of a sign: how many complete faces would become readable start to finish if that sign alone got a built-on value (counted, not guessed: faces whose only unvalued sign is this one).')
A('- **DEDR** = Burrow and Emeneau, Dravidian Etymological Dictionary (local copy `work_data/lexicons/dedr/`), entry number. **Tamil Lexicon** = University of Madras Tamil Lexicon (1924-36), read online at dsal.uchicago.edu.')
A('')
t3, ws, st = cov('third list', 'all'), cov('fourth list, wide', 'all'), cov('fourth list, strict (fresh-based only)', 'all')
A('## 1. What was found')
A('')
A(f'1. **705 is *kalam*, the grain measure. One word carries both readings.** Tamil *kalam* is "vessel, ship" (DEDR 1305) and also "a measure of capacity" (Tamil Lexicon p. 778, sense 10, cited from the Tolkāppiyam, the oldest Tamil grammar); the Lexicon also gives *marakkāl* = 8 *paṭi* = 1/12 *kalam* (p. 3082). DEDR 1305 itself lists only vessel, pot, ship; the measure sense is in the Tamil Lexicon. The picture fits the measure exactly: a U-shaped vessel with a stick standing in it is a measuring vessel with its levelling stick. The measure predictions came true hardest on new texts: a count follows 705 in 28 of 64 uses against 14.1% for all signs (P 8e-9), and all 28 of those counts are tall strokes, the container series, against 35% for counts overall (P 1e-13). That points straight at the measure: 705 is counted the way containers are, on texts nobody used to choose it.')
A('2. **Where each use falls.** Every face with 705 or 706 in both catalogues (384 faces) went into a box by its own clues. Measure clues (a count after it, a grain or measure word on the face, a tablet or pot): 243 faces. Ship clues only (the sail 500 after it, a coast or foreign findspot, a trade tag): 30 faces, 14 of them the Lothal tag `705-500-...` (11 copies in the first catalogue, 3 new-text tags). Both: 16. Neither: 95 (mostly seals where 705 stands without a count). Measure wins the corpus about 8 to 1.')
A('3. **The ship stands where it works: Lothal, uncounted, before the sail.** The ship predictions that came true are the ones about the sail and trade: sail 500 after it on new texts 3 of 64 against 0.4% (P 0.002), trade-tag words (dozen, given, sale, fish) on the same new-text face 15 of 66 against 15% (P 0.049), coast and abroad 43 of 384 against 9% (P 0.07). Where 705 is followed by the sail it is never counted. So one word, two uses: counted *kalam* = the measure (everywhere), *kalam pāy* = the ship (the Lothal tags and two Mohenjo-daro seals). The Lothal tag reading 42 stands: "by ship, first ward: one dozen fish; the house\'s agent". And Lothal also writes the measure: `705-320` *kalam paṭi* (two Lothal tags), `705-575` *kalam kōṭṭai* (two Lothal seals), `705-540` *kalam paṟai* (one): measure words stacked at the port.')
A('4. **Why the count is a fixed three: "three kalam" is a grade written into titles.** On goods objects the count after *kalam* varies (pots: 2, 3, 5; other tablets: 3, 4, 5); on seals it is three 115 times out of 118 (8 of 69 not-three on goods against 3 of 118 on seals, P 0.015). On seals the chief sign 520 follows "three kalam" 54 times out of 172, against 2.0% after any sign, and seals carrying "three kalam" are bigger than seals with the same number of signs (x1.11, n 87, P 0.064). So `705-033-520` *kalam mū vēḷ* is "the three-kalam chief": a rank named by its grain allowance, the way the allowance *paṭi* gives *paṭiyāḷ* "a servant paid in grain" (DEDR 3849). The copper tablets copy it as a fixed formula too (three, 35 of 35).')
A(f'5. **The coverage push: {ws.faces} of 3,600 faces now read start to finish, up from {t3.faces}; {ws.distinct} distinct texts, up from {t3.distinct}.** That is with every value whose prediction came true on new texts or on a fresh Lipi fact. Counting only values whose fact was fresh: {st.faces} faces, {st.distinct} distinct texts. Split by object: seals {cov("fourth list, wide","seals").faces} faces of 1,540 (was {cov("third list","seals").faces}; strict {cov("fourth list, strict (fresh-based only)","seals").faces}); goods objects {cov("fourth list, wide","goods").faces} of 2,060 (was {cov("third list","goods").faces}; strict {cov("fourth list, strict (fresh-based only)","goods").faces}). On the new texts themselves: 233 of 627 complete new texts read whole (strict 178), up from 134. More than half the complete faces of the first catalogue now read.')
A('6. **22 of the 25 top blockers got a word whose prediction came true (9 of them on fresh facts), and 705/706 came true on fresh facts in job 1.** The fresh ones: *nel* "grain" (413) lies in the Harappa tablet mound E 22 of 44 against 25% (P 0.0003); *turumpu* "threshed heap" (416) and *kutir* "granary bin" (605) lie in mound F, the granary, 15 of 27 and 6 of 9 against 34%; *vēḷāḷaṉ* "cultivator" (137) in mound E 7 of 12 against 25%; *tiṅkaḷ* "month" (900) is counted with short strokes 61 to 6 (things, not containers; P 3e-11); *kūṭumīn* "crate of fish" (226) sits at the coast and abroad 9 of 52 against 9% and takes tall (container) counts 17 to 8; *kāval* "guard" (527) stands where the possessive jar would be (jar on 7 of 63 faces against 33%, P 6e-5), so `550-527` is *vāy kāval* "gate-guard"; *aṭi* "servant" (717) shares its new-text face with a person or title sign 11 of 23 against 16% (P 0.0004); *aracu* (384) stands in the frames of its sister leaves 388/382.')
A('7. **The web paid twice.** (a) *kalam* the measure was chosen for 705 alone, and with it the sign that follows `705-033` 15 times, 923, reads too: `706-033-923-740` on 7 copper tablets reads "three kalam, crescent-horn: of the house". (b) The Lothal measure stack *kalam paṭi* / *kalam kōṭṭai* uses three values chosen in other jobs (320, 575, 540), and the goldsmith reading of 104 (person with the seed-weight *kuṉṟi* at his foot) predicted the gold weight 645 and the seed-weight 480 on the same face: 7 of 27 against 1% (P 2e-8).')
A('8. **Twenty more inscriptions read whole** (READINGS 61-80), all texts that read for the first time in this pass: a 29-copy Harappa store chit, a 10-copy office chit of the "chief staff" keeper, the three-kalam chief, five-kalam copper tablets, ration issues to a bondsman and a cultivator, the granary heir, the gate-guard, millet for sale.')
A('')
A('## 2. Job 1 in full: 705/706 measure against ship')
A('')
A('Predictions were written into `sound_v4_job1.py` before it ran. "seen in v3" = the same check the third pass already ran.')
A('')
A('| test | reading | prediction | outcome | number | P | fact |')
A('|---|---|---|---|---|---|---|')
for r in pd.concat([J1, G]).itertuples():
    fr = getattr(r, 'fresh', '') if isinstance(getattr(r, 'fresh', ''), str) else ('partly seen' if r.stage == 'G1' else 'fresh')
    A(f'| {r.stage} | {r.word} | {r.prediction} | {r.outcome} | {r.result} | {r.p:.2g} | {fr} |')
A('')
A('G1 and G2 test the fixed three. G1 was partly visible while exploring (the spear after 705-033 showed in a neighbour count). G2 (size) was not.')
A('')
A('Where every use falls (faces; L = first catalogue, Mu = new texts):')
A('')
A('| | measure only | both | ship only | neither |')
A('|---|---|---|---|---|')
for cat in ['L', 'Mu']:
    c = U[U.cat == cat].box.value_counts()
    A(f'| {cat} | {c.get("measure",0)} | {c.get("both",0)} | {c.get("ship",0)} | {c.get("neither",0)} |')
A('')
A('The 30 ship-only faces: 11 copies of the Lothal tag `705-500-741-001-055-220-740-090` and 3 new-text Lothal tags `705-500-...`, two Mohenjo-daro seals with 705/706 before the sail (`705-500-741-803-923-740`, `706-500-820-062-151`), and Dholavira and Lothal faces whose only ship clue is the findspot. The "neither" faces are mostly seals where *kalam* stands in a name without a count (`091-705-798`, `615-705-595`, `705-140`).')
A('')
A('**The 15 long phrases, read again with *kalam* the measure** (they were nonsense under *kaḷam* "threshing floor"):')
A('')
LP = [
 ('M-314', '466-706-760-740', '(n) kalam maka kuṭi', 'n kalam: of the house of the child', 'the count comes before here, written with the load comb: n kalam-loads'),
 ('K-89', '…-002-…-705-033-…', '… iru … kalam mū …', '… two … three kalam …', 'tag, broken'),
 ('H-2584', '705-033-095-520', 'kalam mū kōlaṉ vēḷ', 'three kalam: the staff-bearer, the chief', 'the three-kalam grade of a staff-bearer chief'),
 ('M-355', '360-861-002-235-231-705-033-032-877-740', '[360] kāṇi iru vēymīn orumīn kalam mū · iru nālkāṇi kuṭi', 'holder of two shares, Bamboo-star First-star: three kalam; of the two-four-shares house', ''),
 ('L-190', '705-500-741-001-055-220-740-090', 'kalam pāy orukuṭi oru paṉṉiru mīn kuṭi āḷ', 'by ship, first ward: one dozen fish; the house\'s agent', 'uncounted kalam before the sail: the ship'),
 ('H-131', '…-794-575-595-002-055-706-033-240-233-840-032-740', '… [794] kōṭṭai paṭṭaṟai iru paṉṉiru kalam mū mīmīn vāḷai iṇai iru kuṭi', '…: great-measure, forge, two; a dozen, three kalam; of the High-star, fish, pair-two house', 'an inventory under a house'),
 ('H-130', '717-125-812-595-002-806-231-705-033-845-032-409', 'aṭi vēṭṭuvaṉ [812] paṭṭaṟai iru viḷai orumīn kalam mū cūṭu iru [409]', 'the Hunter\'s servant: [812], forge, two; produce, First-star, three kalam; sheaf-bundles, two; [409]', 'an open list, no jar'),
 ('H-774, H-1814, H-1816', '240-705-033-550-525-400', 'mīmīn kalam mū vāy [525] ciṟ', 'High-star: three kalam; Gate-[525], junior hand', 'face 2 is the grain line *nel kōṭṭai ūr vaḷḷam mū nāḻi*: two faces, one grain issue'),
 ('H-1813', '220-705-033-550-525-400', 'mīn kalam mū vāy [525] ciṟ', 'Star: three kalam; Gate-[525], junior hand', ''),
 ('M-1954', '861-002-798-415-220-705-033-752-031-590-407-740', 'kāṇi iru maru kavar mīn kalam mū maka oru peṭṭi kiḷai kuṭi', 'holder of two shares, Descendant of Branch-Star: three kalam; child-of, one; of the Chest-Kindred house', ''),
 ('L-191', '705-500-741-001-055-220-740-090', 'as L-190', 'by ship, first ward: one dozen fish; the house\'s agent', ''),
 ('M-10', '455-267-002-806-235-706-033-032-070-061-405', '[455] [267] iru viḷai vēymīn kalam mū iru ampu kāl kiḷai', '…two; produce, Bamboo-star, three kalam; two arrows, a quarter of the kindred', ''),
 ('M-359', '632-705-385-388-002-803-235-220-590-405-740', 'pal kalam [385] aracu iru il vēymīn mīn peṭṭi kiḷai kuṭi', 'many kalam: [385]-Royal, two; of the house of the Bamboo-star-Star Chest-Kindred house', '*pal kalam* "many kalam" with no count: an amount word in the count place'),
]
A('| object | signs (reading order) | sound | English | note |')
A('|---|---|---|---|---|')
for o, s, snd, en, nt in LP: A(f'| {o} | `{s}` | *{snd}* | {en} | {nt} |')
A('')
A('All 15 phrases now make sense as amounts: "three kalam" after a name is the holder\'s grade or issue; "n kalam" with the count in front (M-314, written with the load comb) is a real amount. Square brackets = a sign still without a value.')
A('')
A('**The 11 Lothal tags** read the same as before: *kalam pāy orukuṭi oru paṉṉiru mīn kuṭi āḷ*, "by ship, first ward: one dozen fish; the house\'s agent". The ship is the uncounted *kalam* before the sail; nothing on those tags counts it.')
A('')
A('## 3. Job 2: the 25 signs that blocked the most faces')
A('')
A('Gain = complete Lipi faces that only this sign kept from reading start to finish under the third list (705 blocked 46 faces and 706 blocked 23; they are settled in job 1).')
A('')
gain = {'240': 131, '233': 35, '060': 29, '435': 28, '407': 27, '900': 24, '416': 23, '413': 17, '388': 14, '226': 12, '384': 12, '048': 12, '097': 11, '717': 10, '832': 10, '790': 10, '382': 9, '605': 9, '137': 9, '550': 9, '923': 9, '877': 9, '104': 8, '527': 8, '831': 8}
VV = V.set_index('sign')
A('| sign | picture | faces blocked | word | English | what came true (or not) | status now |')
A('|---|---|---|---|---|---|---|')
for s, g in gain.items():
    r = VV.loc[s]
    st_ = r.tier_v4 + (f' ({r.basis})' if r.basis else '')
    A(f'| {s} | {pic(s)} | {g} | *{r["sound"]}* | {r.english} | {r.note} | {st_} |')
A('')
A('Every check run in job 2, in the order run (A = the bold prediction, B = a better test of the same word, B2 = one more better test, C/C2 = a new word):')
A('')
A('| stage | sign | word | prediction | outcome | number | P | fact |')
A('|---|---|---|---|---|---|---|---|')
for r in J2.itertuples():
    A(f'| {r.stage} | {r.sign:0>3} | {r.word} | {r.prediction} | {r.outcome} | {r.result} | {r.p:.2g} | {r.fresh} |')
A('')
A('## 4. How much reads now')
A('')
A('| list | object group | faces read whole | of | distinct texts | of | objects |')
A('|---|---|---|---|---|---|---|')
for r in C.itertuples(): A(f'| {r.list} | {r.group} | {r.faces} | {r.of_faces} | {r.distinct} | {r.of_distinct} | {r.objects} |')
A('')
A('New texts (second catalogue, no Lipi partner, complete lines): 134 of 627 read whole under the third list; 178 under the fourth strict list; 233 under the fourth wide list (seals 71 / 94 / 125 of 346; goods 63 / 84 / 108 of 281). 454 distinct Lipi texts read whole for the first time in this pass (131 under the strict list); `work_data/sound_v4/reading_candidates.csv`.')
A('')
A('## 5. The whole list (98 values)')
A('')
n = V[V.tier_v4 != 'base'].tier_v4.value_counts()
A(f'{n.get("building",0)} building on, {n.get("testing",0)} testing, {n.get("paused",0)} paused (third list: 58 / 17 / 19 of 94). Strict list (only fresh facts promote): 69 building on, 24 testing, 5 paused. "basis" = fresh or seen for values decided in this pass. Base values (numbers, jar, man, fish, spear, comb, carriers, staff-bearer, tree, elder, cup, load comb) are not listed.')
A('')
for tier in ['building', 'testing', 'paused']:
    A(f'### {tier.capitalize() if tier != "building" else "Building on"}')
    A('')
    A('| sign | picture | sound | English | before (v3) | basis | evidence |')
    A('|---|---|---|---|---|---|---|')
    for r in V[V.tier_v4 == tier].itertuples():
        A(f'| {r.sign} | {pic(r.sign)} | *{r.sound}* | {r.english} | {r.tier_v3} | {r.basis} | {r.note[:260]} |')
    A('')
A('## 6. What went against, and the rescue tried')
A('')
A('- **705 as a record-object word**: on new texts 705 sits on tablets and pots 5 of 66 against 21% (P 0.999), and Harappa objects with it are not in the granary mound F (30 of 90 against 34%). Grain words on the same new-text face: 8 of 66 against 9% (direction only). The measure is read off the counts, not the object kind: on the new texts it lives on seals and tags. Rescue: the fixed-three grade (G1, G2) explains why a measure word sits on seals.')
A('- **705 abroad**: 1 face of 384 at a foreign site (against 1%). The ship reading gets no foreign support; it stands at Lothal.')
A('- **240 *mīmīn***: house ending on new-text seals 7 of 9 against 77% (no excess). Rescued by B on new texts (another fish crest follows, 15 of 58 against 6.5%), a fact visible while choosing: building on in the wide list only.')
A('- **233**: *vāḷmīn* "Bright-star" as a crest went against (house ending 6 of 9 against 77%; size x1.07). New word *vāḷai* "scabbard-fish", a counted fish good: a measure word follows it on new texts 9 of 39 against 3.4% (seen). It now reads as goods in `806-233-384-740` and `798-240-233-320-920-740-400`.')
A('- **435 *taṭi* "staff"**: bigger seals x1.00, sites 6 against 8, land words 6 of 91 against 5%: three misses. New word *kōl* "rod, sceptre": the carrier or 690 follows on new texts 9 of 16 against 1.1% (seen). `255-435` *mutal kōl* "chief staff" is an office.')
A('- **407 *kiḷai***: herd-beast reverse 5 of 43 against 11%, house share 10 against 9.6: direction only. Better test: last sign on copper tablets 45 of 77 against 21% (Lipi, seen). 407 has no new texts at all (the crosswalk does not carry it), so it stays testing; it blocks 27 faces.')
A('- **388/384/382 *aracu***: house sharing went against for 384 and 382 (0 against 0.1; frames 3 against 3; jar after 382 2 of 20). Rescue: 384 stands in the frames of its sisters (7 against 3, fresh); 382 takes *maka* after it 5 of 20 against 0.9% (seen). All three building on as one word.')
A('- **048 *er̤uvar* "the Seven"**: no shared frames with the Seven Maidens 585 (0). The jar follows it 17 of 17, but only in the first catalogue; 048 is not on new texts. Testing.')
A('- **832 *kaṇ* "at, in"**: sites 6 against 8 (against); a time or place word before it on new texts 3 of 25 against 7.2% (direction). The first run counted 832 standing after 832 as a hit (11 of 25); the clean rerun is the number given. Testing.')
A('- **104**: *kuṉṟavaṉ* "hillman" went against (frames 4 against 3; jar 10 of 26 against 33%), the goldsmith *taṭṭāṉ* did not stand in the smith\'s frames (1 against 1) but predicted the weights on its face (7 of 27 against 1%, seen). Building on in the wide list.')
A('- **Smaller misses inside a sign that came true elsewhere**: 416 counted with tall strokes 1 of 15 (a heap is counted as a thing, not a container); 137 with grain/cup on its face 2 of 19; 717 servant seal smaller x1.06 (it is not smaller); 923 with month signs 0 of 48 (so *maruppu* is the crescent horn as a counted thing, not a date); 550 with a ward jar 3 of 27 (direction); 790 at bead towns 9 of 69 against 9% (direction); 831 in mound E 1 of 6; 060 sites 17 against 14 (direction).')
A('')
A('## 7. What it opens next')
A('')
A('- **The grade system.** "Three kalam" before the chief is a grain grade. Next: every count after a measure word on seals (705, 711, 320) as a grade, against seal size and closing title; and whether *kalam* grades sit with the fish-star houses (the great houses).')
A('- **167**, an arch with a ring at each foot, closes only *kalam* tablets (`705-167`, `167-705-031` at Chanhu-daro) and is still paused: with *kalam* now a measure it should be a measuring or issuing word. It is the next sign to give a word.')
A('- **407** blocks 27 faces and cannot be tested on new texts: build its crosswalk entry from the second catalogue\'s tree signs and rerun.')
A('- **The Harappa mounds now sort words**: grain *nel*, cultivator, ration chits in mound E; threshed heap, granary bin in mound F. A findspot map of every built-on value at Harappa is the next cheap test bed.')
open(f'{ROOT}/jobs/out/sound_list_v4.md', 'w').write('\n'.join(L) + '\n')
print('wrote jobs/out/sound_list_v4.md', len(L), 'lines')
