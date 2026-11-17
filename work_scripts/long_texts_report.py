#!/usr/bin/env python3
"""Assemble jobs/out/long_texts.md from work_data/long_texts/read.json (long_texts_build.py, long_texts_read.py) and the hand text below.
Numbers quoted in the prose come from long_texts_stats.py, long_texts_stats2.py, long_texts_fix.py, long_texts_fix2.py, long_vessels.py, long_signslots.py."""
import json, collections
from long_common import *
T = json.load(open(f'{OUTDIR}/read.json'))
SH_N = 46
def sg_line(sgs):
    seen = []; out = []
    for s in sgs:
        if s in seen or s == '000': continue
        seen.append(s)
        v = snd(s) if (s in CNT or snd(s) or s == '806') else None
        val = ('(n loads)' if s in CNT and CNT[s][0] == 'comb' else '(crop)' if s == '806' else snd(s)) if (s in CNT or s == '806' or snd(s)) else slot_desc(s).split(' [')[0]
        out.append(f'`{s}` {shape_words(s)[:SH_N]} [{val}]')
    return ' · '.join(out)
COMM = {
1: 'Three-face tablet, eight phrases. Face 1 is a normal owner phrase plus the keeper sign 151 standing straight after the jar (porter signs follow a non-final jar in 12 of 460 corpus cases). Face 3 carries a date-like pair: `904` (two months) twice and `820-032-017-904` = "two quarters, seven (units of) 904". Sister tablet M-495 differs in three places: `255` absent, `221`→`267`, final `921`→`740`; `921` stands in the jar\'s slot, so it is a second spelling of the ending or a second ending word.',
2: 'Sister of M-494 (23 against 24 signs). Its last phrase is the template text `415-100-740` (Branch-Elder house) almost whole; M-494 ends the same frame in `921`. Frames that differ in one place: `221~267`, `921~740`, `255` present or absent: three name-end slots written with varying signs.',
3: 'Seven-face prism: one short phrase per face. Face 1 is a dated owner phrase (`920-060-741` month, first ward, then Bamboo-star-Two-months house); faces 2 and 3 are counted lines (3 `645`; weight `171` 2 1); faces 4 to 7 are bare names (`840-461`, `169`, `511`, `000-111-390`). A roll: a heading, a holder, quantities, then names. 6 of the 19 signs have no value, all of them in faces 2 and 4 to 7.',
4: 'Line 1 alone is a complete seal text (wheel two, Bamboo-star-High-star-First-star, spear = chief). Lines 2 and 3 add what a short seal cannot hold: a count of `706` (written with the load-count A-sign `466`) and a child-of house, then `Hunter-Warrior` (`125-390`, a unit seen on 9 lines) and a closing pair. Shape: [title of X] [what he holds] [names].',
5: 'Kalibangan tag, 8 of 23 sign places lost. The only intact phrase is the agent phrase on face 1 (manager of the Tender-leaf-360-Two-362 house). The other faces keep `705-033`, `390-595-002` (Warrior, Chest, Two): count lines, no names to hang them on.',
6: 'The same five-sign phrase on three faces (a tag stamped three times) and a lost fourth face: one distinct phrase, `817-002-032-760-740`. The second "two" (`032`, tall) before `760-740` is the name element Two; "two shares: the Two-Child-of house".',
7: 'Impression of a seal on clay, two faces. Half the signs are unvalued (`776 825 909 066 835`); face 1 is a string of short name-like pieces with two counts (`016-220` six stars, `005-909`), face 2 ends in an ordinary owner phrase with a lost sign inside it. Reads badly mostly for want of values, not for want of structure.',
8: 'The same seven signs on both faces: the short-seal template exactly (two shares, two arrows, of the Chest-Warrior house), stamped twice. Every sign valued, no avoided word pair. From Harappa mound F granary, like H-180 which names the same Chest-Warrior with the keeper sign.',
9: 'Tablet, two faces. Face 1: three jar phrases in a row (`176-740` Tax house, `335-740`, `491-920-002` Month-Two as a date), face 2: the grain line `413-575-335-740` and two cups. The unvalued `335` stands right before the jar in two phrases (12 jar uses in the corpus), the same slot a house word takes.',
10: 'Tag, three faces: three vessels `705-033`; staff-bearer chief (`095-520`); n crop (A-sign + `806`); Descendant-First-star; Gate-527; twelve Chief-Flash-Bound. A list of people and goods with no jar anywhere.',
11: 'One 13-sign run with one jar at the end. Hand division: name `921-690`; count lines `002-032-220` (two stars), `003-900` (three months), `032-590` (two chests); a name with its crop `235-806`; then the owner word `405-740` (Kindred house). A single "of the X house" carrying an inventory.',
12: 'Face 1 holds a name (First-ward-Proclamation-Warrior) and an owner phrase (two Houses of the Descendant house); face 2 is the Harappa grain line `413-575-335-711` + three cups, the same line as on 5 other tablets.',
13: 'Two lines. Line 1 is two phrases: `920-001-235-220-520` (month one, Bamboo-star-Star, chief) and `692-060-482-740` (X-office, of the Hill-share house). Line 2 `368-192-871-842` is a bare name ending in `842`. M-234 repeats line 1 sign for sign and changes line 2.',
14: 'Thirteen signs, one jar. The run cuts into recurring blocks: `032-632`, `125-390` (9 lines elsewhere), `002-235-240` (5), `032-220` (inside a 22-line unit `002-032-220`), `255-435-690-740` (20 lines). Four name-blocks and one "of the house": read as joint owners or a list of members with one possessive. All 13 signs valued.',
15: 'Line 1 identical to M-23; line 2 `004-099-535-842` again ends in `842`. Two seals share a 9-sign first line and end the second line with the same rare sign: the first line is an office or institution, the second line the person.',
16: 'Four faces, no jar, 9 of 13 signs unvalued; `899` stands at both ends of the face-3 phrase `899-380-484-899` (6 of 1,433 corpus lines of 4+ signs start and end on the same sign). Reads as nothing yet; structure is a list of short pieces with three counts.',
17: 'Three-part text: a title (`140-919-520`, Mother-919 the chief), a second opener inside the line (`861-002`, two shares) that starts a new owner phrase `861-002-235-231 705-033 032-877-740`. Mid-line openers: 13 of 157 long objects, 22 of 1,732 short ones.',
18: 'Two phrases in one formula, `692-060-X-740` twice (X = Chief-Flash-Bound, then House), then a line-2 name `125-374-842` ending in `842`. M-682 has the same first line and a lost second line.',
19: 'Lothal tag. Face 1 is the agent phrase `705-500-741-001-055-220-740-090` (manager of the Twelve-Star house), the same stone as on L-191, L-193 and L-197; face 2 and 3 differ: month two, `880`. The first face is the stamp, the other faces are what was attached to it.',
20: 'Three faces, each a lost-crest name + jar: First-star-Elder, Two-Star-Striped-star-King, High-star-335-Child-of. Three owners on one tag.',
21: 'Thirteen signs, one jar. Goods first (great-measure, chest, two; twelve of `706`, three), then two fish and Pair-Two as the house. Inventory under a house, like H-1657.',
22: 'No jar, no closer: seven short count lines (chest, crop, `231-705-033`, ...) and unvalued `812 845 409`. An open list.',
23: 'The same phrase on both faces: `368-330-741-590-390-151` = Banner-330-First-ward-Chest-Warrior + keeper. Harappa mound F granary, the same Chest-Warrior name as the seal H-597.',
24: 'Tablet: face 1 = High-star + three of `705` + `550-525-400` (Gate-525, junior); face 2 = the grain line + three cups. Four tablets carry this pair (H-774, H-1813, H-1814, H-1816).',
25: 'Count lines (three chests, one arrow, two-one stars) then a name `002-255-435-125`. Avoided pair: the title word `435` before the house-class `125`.',
26: 'Fully valued: opener, name (Descendant-Branch-Star), three of `705`, child-of one, of the Chest-Herd house. The "three of 705" is the fixed unit seen in 15 of the 41.',
27: 'Round seal, name, then a second opener `861-002` in mid-line starting an owner phrase, then a tail name. Five unvalued signs.',
28: 'Face 1 is a template seal text (two shares, [191]-Branch-Elder house). Face 2 is "[350-Three-peaks-Descendant-Two-months] house, junior": the comb ending after the jar names a second house and its junior. Two parties on one tablet.',
29: 'As H-774 with the jar `740` where the cup stands at the end of face 2: `033-740` = three jars (a counted pot), not "three house of".',
30: 'As H-774 with plain fish `220` for whisker fish `240` at the front of face 1; the grain line ends in the cup.',
31: 'Faces in the other order from the three tablets above (grain line first, then the High-star line), with one sign lost in the grain line. The order of faces is not fixed by the reading.',
32: 'Eleven identical tablets in the corpus (H-278 to 284, H-871 to 873, 291; mound F). Four blocks and a jar: House-Branch-Star, 318-Month, Chief-436-Bound, of the Chest-Herd house (`590-407-740`, also the end of M-1954).',
33: 'Seal with two faces, two owner phrases (a Field house and a Chest-Sale house) and a count of the unvalued `893`.',
34: 'Same agent face as L-190; face 2 is `861-002-235` (two shares, Bamboo-star), which is a complete short text.',
35: 'Impression, two faces: Chest, eye/seed-weight one, `821`, then House-keeper and a pair of counts. Weak values (391, 821, 913).',
36: 'Eleven signs, no jar: name, two crops, Bamboo-star three of `706`, two arrows, quarter-kindred. A list of counted items.',
37: 'Eleven signs, one jar at the end (Chest-Kindred house) after a list: Many Threshing-floor ... King, two Houses, Bamboo-star-Star.',
38: 'Opening `920-060-742` (month, second ward), a crop-fish name, and the owner block High-star-Chief-Flash-Bound-jar. 10 of 11 signs have a value.',
39: 'Copper tablet, two lines. Line 2 ends in `142-617` (King, servant), a pair of 14 lines in the corpus: "king\'s servant".',
40: 'Opening (quarter, Proclamation), name, `176-175` (two drawings of the seated person side by side), child-of house.',
41: 'The Dholavira signboard (id 144.1, gypsum, 3,000 x 370 mm, Castle, west chamber of the north gate). The record holds 9 signs; see section 6.',
}
def phr_table(t):
    rows = ['| # | where | signs | kind | sound | English | mark |', '|---|---|---|---|---|---|---|']
    for i, p in enumerate(t['read'], 1):
        rows.append(f"| {i} | f{p['face']}l{p['line']} | `{'-'.join(p['signs'])}` | {p['kind']} | {p['sound']} | {p['english'].replace('|','/')} | {p['mark']}{(' (' + p['reason'] + ')') if p['reason'] else ''} |")
    return '\n'.join(rows)
def where(t):
    return ', '.join(v for v in [t['site'], t['area'], t['block'], ('depth ' + t['depth']) if t['depth'] not in ('- -', '') else ''] if v and v not in ('--', '-'))
def order_line(t):
    out = []
    for fi, f in enumerate(t['faces'], 1):
        for li, l in enumerate(f['lines'], 1):
            out.append(f"face {fi}" + (f" line {li}" if len(f['lines']) > 1 else '') + ': `' + '-'.join(l) + '`')
    return '; '.join(out)
mk = collections.Counter(p['mark'] for t in T for p in t['read'])
nph = sum(len(t['read']) for t in T)
allsg = [s for t in T for p in t['read'] for s in p['signs'] if s != '000']
valued = sum(1 for s in allsg if s in CNT or s == '806' or snd(s))
reasons = collections.Counter(p['reason'].split(':')[0].split(' where')[0][:40] for t in T for p in t['read'] if p['mark'] == 'nonsense')
L = []
A = L.append
A('# Long texts read whole')
A('')
A('Forty-one inscriptions (the 40 longest distinct texts plus the Dholavira signboard) parsed into phrases, read aloud with the working table (`work_data/sound_v2/values_v2.csv`, 137 signs with a sound, numbers included) and set against the corpus. Scripts: `work_scripts/long_common.py` (loader, reading order, reading), `long_texts_build.py` (pick the texts), `long_manual.py` (phrase division by hand), `long_texts_read.py` (read and mark), `long_texts_stats.py`, `long_texts_stats2.py`, `long_vessels.py`, `long_signslots.py`, `long_texts_fix.py`, `long_texts_fix2.py` (tests), `long_texts_report.py` (this file). Tables in `work_data/long_texts/`.')
A('')
A('## What was found')
A('')
A(f'1. Every one of the 41 long texts breaks into two or more phrases: 186 phrases in all (2 to 8 per text, mean {nph/41:.1f}), and a face of a multi-face object holds one phrase in 29 of 60 faces. Phrase kinds: 60 names, 58 count lines, 34 owner phrases ("of the X house"), 14 title phrases (X the chief / keeper / junior), 9 openings, 3 agent phrases, 2 place phrases, 1 junior, 1 load line, 1 name list, 3 signboard lines.')
A(f'2. {valued} of {len(allsg)} signs ({valued/len(allsg):.0%}) carry a sound. Phrases marked: {mk["reads"]} read as sense, {mk["partial"]} partly (an unvalued sign sits in a slot we can name), {mk["unread"]} unread (one unvalued sign alone), {mk["nonsense"]} read as nonsense. 22 of the 559 sign places are lost.')
A('3. **The nonsense is concentrated in a few sign values, not spread out.** 29 phrases are nonsense: 705 or 706 "threshing floor" with a fixed three after it (15 phrases in 15 texts), 435 "flash" (5 phrases in 5 texts), a counted jar read as "house of" (3), `176-175` "tax tax" (1) and word pairs the corpus avoids (5). Section 5 replaces them: `705/706` = a measure with a fixed "three" after it (paṭi, DEDR 3849, "measure of capacity, fixed daily allowance"), `255-435` = one title "chief of the rod" (taṭi, DEDR 3030), jar after a tall count = a counted pot.')
A('4. **Records are a who-phrase plus a what-phrase, and one of the two repeats.** Four Lothal tags share one 8-sign agent face and differ in the other face; two Mohenjo-daro seals share a 9-sign first line and differ in the second; four Harappa tablets share `617-892-740-400` and differ in a cup count; the grain line `413-575-335-711-033-700` sits on 6 tablets under 3 different first faces.')
A('5. **A long single-jar text is a list of name-blocks and count-lines under one "of the house".** 98 of 157 long objects have exactly one jar; the run before it cuts into blocks that recur elsewhere (`125-390` 9 lines, `002-235-240` 5, `255-435-690-740` 20, `032-220` inside a 22-line unit).')
A('6. **Repetition inside one text is a long-text trait:** 52 of 157 long texts (33%) contain a sign twice against 75 of 1,732 texts of 3 to 5 signs (4%). The repeats are the jar (20 texts), the count strokes (`032`, `033`, `002`) and openers, i.e. repeated phrase frames.')
A('7. Signs found only in long texts: `578` (5 uses) and `799` (4), all on five Harappa TAB:I tablets (`415-578-032-824`, `799-840-760-740`); strongly long-enriched: `711` 5.2x, `525` 5.1x, `335` 3.8x, `070` 2.9x, `413` 2.7x. They are the tablet commodity block (`413-575-335-711`) and `550-525-400`.')
A('8. No verb found. The only sign with a fixed place between two parts is `060` (a joiner inside openers: head sign on its left in 132 of 177, jar on its right in 3 of 177). The transaction words (`892` sale, `176` tax, `550`) sit inside phrases, not between them.')
A('9. **The signboard reads as a gate notice of quarters.** Wheel `820` (text-initial in 187 of 244 uses, "quarter" kāl) opens three phrases of the board: `820-611-388` "quarter of the [611] King", `820-850-645-031`, `821-798` "(quarter) of the Maru- (clan)". No god sign and no welcome sign in the slots; ruler (`388`, 22 of 59 uses straight before the jar) yes.')
A('')
A('## 1. The texts and how they were picked')
A('')
A('Source: Lipi table (`metadata_filtered.csv`), 5,679 faces on 4,694 objects, 3,614 distinct objects once copies are merged. An object is the faces `.1 .2 ...` in id order; a face is split at `/` into lines; each line is reversed into reading order, and the order of lines is reversed too (check: M-314 line 1 maps through the crosswalk to Mahadevan text 1400 line 1, `391-99-65-67-70-211` = `820-002-235-240-231-520`). Texts are ranked by legible signs (`000` lost signs not counted; they are shown). 30 distinct texts have 12 or more legible signs; 17 have exactly 11 and 10 of them are taken (ties broken by total place count including lost signs, then by the order of the table). Copies: objects with exactly the same faces are one text, listed once with a copy count. The Dholavira signboard (id 144.1, 9 signs recorded, rank 104 by length) is added as text 41.')
A('')
A('Reading of the tables below. Sign line: `number` shape in words [sound, or the kind of word the slot says it must be]. Phrase rows: where = face and line; kind = phrase kind from the hand division; sound = the working sounds in order, `‹?›` for no value; English = structural reading, `<...>` marks an unvalued sign by its slot; mark: **reads** = every sign valued and no word pair the corpus avoids (class-bigram table `work_data/long_texts/class_bigrams.csv`, pairs seen at under 0.4 of chance with 10 or more expected); **partial** = a sign without value or a lost sign; **unread** = one unvalued sign alone; **nonsense** = an avoided pair or one of the four repaired values (reason given).')
A('')
A('## 2. The 41 texts')
for t in T:
    cop = f", {t['copies']} copies in the corpus" if t['copies'] > 1 else ''
    A('')
    A(f"### {t['rank']}. {t['cisi'] if t['cisi'] != '-' else 'Dholavira signboard'}: {t['type']}, {where(t)}{cop}")
    A('')
    A(f"{t['legible']} legible signs ({t['total']} places), {len(t['faces'])} face{'s' if len(t['faces'])>1 else ''}, {len(t['read'])} phrases" + (f", animal {t['animal']}" if t['animal'] not in ('', 'None', '-') else '') + '. Reading order: ' + order_line(t))
    A('')
    A('Signs: ' + sg_line([s for p in t['read'] for s in p['signs']]))
    A('')
    A(phr_table(t))
    A('')
    A(COMM[t['rank']])

# ------------------------------------------------------------------ 3. phrase table
A('')
A('## 3. Phrases per text, kinds, and what reads')
A('')
A('| # | text | signs | phrases | kinds | sense | partial | unread | nonsense | signs valued |')
A('|---|---|---|---|---|---|---|---|---|---|')
for t in T:
    k = collections.Counter(p['kind'] for p in t['read']); m = collections.Counter(p['mark'] for p in t['read'])
    sg = [s for p in t['read'] for s in p['signs'] if s != '000']; v = sum(1 for s in sg if s in CNT or s == '806' or snd(s))
    A(f"| {t['rank']} | {t['cisi'] if t['cisi'] != '-' else 'signboard'} | {t['legible']} | {len(t['read'])} | {', '.join(f'{n} {a}' for a, n in k.most_common())} | {m['reads']} | {m['partial']} | {m['unread']} | {m['nonsense']} | {v}/{len(sg)} |")
A('')
A('Phrase boundaries were set by hand (`long_manual.py`) from five cues, in this order of strength: (1) a closer, i.e. the jar with its relation sign, the spear, the keeper, the junior; (2) a face or line break (a face holds one phrase in 29 of 60 faces of multi-face objects); (3) a second opener (`861-002`, `692-060`, `920-060`) inside a line; (4) a unit that recurs on other objects, found with `long_cohesion.py` (blocks of 3 or more signs seen in 3 or more corpus lines); (5) a count run that starts its own counted thing. Where only cue 4 or 5 applies the phrase is a block inside a name list rather than a sentence.')

# ------------------------------------------------------------------ 4. what long texts teach
A('')
A('## 4. What the long texts teach that short ones cannot')
A('')
A('Corpus: 3,614 distinct objects; long = 9 or more legible signs (157), middle 6 to 8 (744), short 1 to 5 (2,705). Scripts `long_texts_stats.py`, `long_texts_stats2.py`. Measured facts first, then the reading they point to.')
A('')
A('Measured slot facts')
A('')
A('- S1. Jars per long object: 0 in 39, 1 in 98, 2 in 16, 3 in 4. Two or more jars: 20 of 157 long objects against 14 of 1,732 texts of 3 to 5 signs.')
A('- S2. A jar that is not line-final: 49 of 142 jar uses in long texts (35%) against 237 of 873 in short texts (27%). After such a jar in the whole corpus (460 cases): a relation sign `090/400/679/621` 286 (62%), a porter sign 12, a new opener `692/820/861/817/920` 6 (1%), anything else 156 (34%, a second name or a count). Openers do not restart a phrase after a jar; a name does.')
A('- S3. An opener-plus-count (`861/817/820` + `001/002/003/031/032`) in mid-line: 13 of 157 long objects (8.3%) against 22 of 1,732 short ones (1.3%). Examples: M-355, M-391.')
A('- S4. Kind pairs in order over all 157 long objects (hand-free cut by closers): owner phrase then bare name 21, owner then owner 20, owner then count-line-with-name 12, count-line-with-name then owner 10, name then name 8, title then owner 7, name then owner 6, owner then title 4, agent phrase then name 4. A bare name follows an owner phrase 3.5 times as often as it precedes one.')
A('- S5. Repetition inside one text: 52 of 157 long texts (33%) against 75 of 1,732 texts of 3 to 5 signs (4%). Texts with the sign twice or more: `740` 20, `032` 10, `033` 9, `002` 5, `741` 4, `368` 2, `590` 2, `390` 2, `820` 2, `692` 2, `060` 2. The same 3-sign-or-longer phrase on two or more faces of one object: M-1385 (3 faces), H-597 (2), H-180 (2).')
A('- S6. Shared first face, different rest: the 8-sign agent face `705-500-741-001-055-220-740-090` on 4 Lothal tags (L-190 L-191 L-193 L-197) with 4 different second faces; the 9-sign first line `920-001-235-220-520-692-060-482-740` on M-23 and M-234 (second lines `368-192-871-842`, `004-099-535-842`); `617-892-740-400` on 4 Harappa tablets (H-229 H-849 H-2090 H-2089) followed by `033-700`, `700-032`, `820-060-869`, `820-001-060-869`; `255-435-156-400` on 4 tablets (H-358 H-761 H-897 H-2062).')
A('- S7. Shared last face, different first: the grain line `413-575-335-711-033-700` on 6 objects under first faces `851-741-048-740` (3), `240-705-033-550-525-400` (2) and others; `027-032-740-400` on 4.')
A('- S8. The ending sign `842` is line-final in 5 of 5 uses; 3 of the 5 are the second line of a seal whose first line is the office formula (`692-060` or `920-060`: M-23, M-234, M-626) and a 4th is C-54, which starts `920-060`.')
A('- S9. `060` is a joiner: head sign on its left in 132 of 177 uses (`920` 65, `692` 45, `550` 28, `820` 26); after `920-060` a ward-number jar (`741/742/745`) follows 41 of 54 times, after `692`, `550`, `820` with `060` a ward jar follows 1 of 75 (a fish or other name sign follows); `060` before the jar directly: 3 of 177.')
A('- S10. Counts: count before the counted thing holds across the 41 (cup `700`: count in front in 24 of 34, values 2 to 6), with one regular exception: `705` and `706` take their count after them, tall strokes, and the count is three in 65 of 69 (`705`) and 30 of 30 (`706`). `711` the same: followed by `033` in 15 of 21.')
A('- S11. Signs found only in long texts (3+ uses, none in short): `578` (5, all five Harappa TAB:I tablets, `415-578-032-824`) and `799` (4, `799-840-760-740` and one variant, same tablets). Long-enriched against all signs with 8+ uses: `711` 5.2x, `525` 5.1x, `335` 3.8x, `070` 2.9x, `413` 2.7x, `575` 2.1x, `125` 2.1x, `850` 2.1x (`work_data/long_texts/sign_long_vs_short.csv`).')
A('- S12. A sign opening and closing one phrase: `899-380-484-899` (M-331) is one of 6 of 1,433 corpus lines of 4+ signs that start and end on the same sign.')
A('')
A('What these say')
A('')
A('1. A long text is a short text with parts added, not a new kind of sentence. Of the 41, 28 contain at least one jar phrase (owner, agent or junior: name + jar + relation, the short-seal template) and 30 contain at least one count line.')
A('2. Order between phrases. Owner phrase first, then a name (S4), and a second line that is a personal name after a first line that is an office or a house (S6, S8). The second phrase does not describe the first as "X\'s man, keeper of Y" in general: owner-then-title is 4 cases of 157. The pattern does occur once in full: M-494 face 1, `of the Sesame-Descendant-Tax house` + keeper `151` straight after the jar + a name. Reading on the table: second part = who handles it, name of the person handling the first.')
A('3. A record is who + what (S6, S7). Tablets: face A = the person or house (with the junior or keeper ending), face B = the commodity and a cup count (`413-575-335-711-033-700`, `033-700`, `700-032`). Faces swap order between copies (H-1816 against H-774, H-1813, H-1814), so face order carries no meaning and the two faces are a pair, not a sequence.')
A('4. Repeated frames inside one text (S5, S3) are list items: `692-060-X-740` twice (M-626), `817-002-032-760-740` three times (M-1385) = the same stamp on several faces; `861-002` mid-line (M-355, M-391) = a second sealed statement joined to the first.')
A('5. Verbs and linking words. None. A linker exists, `060` (S9), and it joins an office head to the thing it governs ("month-060-first ward"). The transaction words (`892` sale, 46 uses, 22 mid-line; `176` tax; `550`) sit inside phrases next to a count, not between phrases. A verb in an account text may simply be missing, as in Linear B tablets, where the entry is name + commodity + number.')
A('6. Counts show a second construction. Counted container words (`705`, `706`, `711`) put the number after (S10); with the number nearly always three. That is a lexical unit, "X-three", not a counting of three things.')

# ------------------------------------------------------------------ 5. repairs
A('')
A('## 5. The sign that does the damage, and a better value')
A('')
A('The 29 nonsense phrases and the signs behind them:')
A('')
A('| text | phrase | reason | damaging sign |')
A('|---|---|---|---|')
for t in T:
    for p in t['read']:
        if p['mark'] == 'nonsense':
            dm = [s for s in p['signs'] if s in ('705', '706', '435')] or ([b[0] for b in p['breaks']] if p['breaks'] else (['740'] if p['potjar'] else p['signs']))
            A(f"| {t['cisi'] if t['cisi'] != '-' else 'signboard'} | `{'-'.join(p['signs'])}` | {p['reason']} | `{'`, `'.join(dict.fromkeys(dm))}` |")
A('')
A('Unvalued signs that spoil the most texts (number of the 41 that carry them): `335` 7, `060` 5, `711` 4, `525` 4, `692` 3, `842` 3. Values already marked paused that sit in the bad texts: `705` 12 texts, `413` 6, `435` 5, `550` 5, `706` 3, `692` 3, `388` 3.')
A('')
A('### R1. `705`, `706` (and `711`): a measure with a fixed three, not a threshing floor')
A('')
A('Old value: kaḷam "threshing floor" (DEDR 1376), picture word kalam "vessel" (DEDR 1305) dropped. Its own check went against (not more on records than seals: 51% against 52%). Why it reads as nonsense: "High-star, threshing floor, three" and "Bamboo-star, assembly place, three" name nothing, and the three never changes.')
A('')
A('Measured: the two drawings are one word: `705` and `706` replace each other in 6 frames (the rest of the line identical) against 0.03 expected from their frame counts. Both take the count after them (69 of 124 uses and 30 of 67) and the count is tall-stroke (container series) in 86% of adjacent counts for `705` (73 of 85) and 82% for `706` (33 of 40), against 35% for all signs (890 of 2,511 adjacent counts), 81% for the cup `700`, 61% for the box `590`, 49% for the plain fish. The number is three in 65 of 69 (`705`) and 30 of 30 (`706`). A sign the old value could not predict.')
A('')
A('New value from picture, slot and dictionary: the U-vessel with a stick standing in it is a measure with its striking stick, and the slot is "name, measure, three": `705/706` = *paṭi* "a weight, the ordinary measure of capacity; fixed daily allowance for food" (DEDR 3849; paṭiy-āḷ "one whose wages are paid in grain"; same word 3850 "grade, rank"). "X, mūṉṟu paṭi" = X: three paṭi, a ration. Rival kept alive: *pāṉai* "large earthen pot; a measure of capacity" (DEDR 4124), or kalam (1305). `711` (U with a cross) the same class: *pāṉai*; `711` is followed by `033` in 15 of 21 uses, tablets only.')
A('')
A('Check on texts of 5 signs or fewer (1,879 lines, none of the 41): `705` has a tall adjacent count in 27 of 33 (82%), the count after it is three in 20 of 24; `706` tall in 12 of 16 (75%), three in 11 of 11. The value predicts both, the old one neither. Effect on the 41: of the 15 nonsense phrases, 11 are `705/706-033` count lines that now read "[X]: three paṭi" (`240-705-033` = "High-star: three paṭi", `231-705-033`, `235-706-033`, `055-706-033`, `705-033`); `466-706` in M-314 (the A-count with `706`) = "n paṭi", which the old value read as "n assembly place"; 3 (L-190, L-191, M-359) keep `705` inside a name and stay partial.')
A('')
A('### R2. `435`: a rod, and `255-435` is one title')
A('')
A('Old value miṉ "flash". It makes "Chief-Flash-Bound" (`255-435-690`) in M-38, M-626, M-369, M-1688 and H-2584. Measured: `435` has `255` on its left in 61 of 75 uses and `690` on its right in 38 (a porter `156` in 14); the block `255-435-690` is on 23 lines and a jar follows it in 20; `255-435-156` 2 lines. The nearest sign to `435` by neighbours is the arrow `070` (cosine 0.37, first of 77 signs), but the two never replace each other (0 frames), so `435` is a different word of the same kind, not an arrow variant.')
A('')
A('The size test: seals with `255-435` have a median face of 838 mm2 (24 seals), with `255-435-690` 930 (18), all seals 605 (1,775). Seals with `255` and no `435`: 556 (28). The earlier result "chief seals are bigger" (684 against 600) is carried entirely by the pair.')
A('')
A('New value: `435` = *taṭi* "stick, staff, rod, cane, measuring rod" (DEDR 3030); `255-435` = *mutal-taṭi* "head of the rod", an office (the measuring-rod holder, a surveyor-chief); `255-435-690-740` = "of the house of the head of the rod, [690]". The sound of `690` stays piṇai (bound, allied) for now. Check: the pair marks the biggest seals (838 against 605), and a title is predicted to stand in front of the jar, which it does in 20 of 23.')
A('')
A('### R3. A jar after a tall count is a counted pot')
A('')
A('`033-740` ends H-1814 and H-1816, read "three house of". A tall count right before the jar occurs 48 times in 1,062 jar uses (37 of them `032`); the avoided pair NUM then POSS is seen at 0.29 of chance (60 against 207). The jar is a container (kuṭam "waterpot", DEDR 1651) counted with the tall series like the cup. In H-1814 it stands where the cup stands at the end of the same line in H-774 and H-1813 (`413-575-335-711-033-[700|740]`): two writings of the counted vessel, "three cups / three jars". Check on short lines: `tall count + 740` closes 19 of 496 short lines ending in a jar (3.8%), 33 of 765 over all lines.')
A('')
A('### R4. `413` is the commodity header, not a granary sign')
A('')
A('The old check (granary mound F share, 20% against 34%) was the wrong place to look. Measured slot: line-first in 44 of 57 uses (77%), Harappa 44 of 57, tablets 40; next sign `575` 22, `892` 14 (sale/price), end of line 10. Reading kept (*katir* ear of grain, DEDR 1194, by the picture) but the role is a header: "grain: [575 335 711] three cups", and `413-892` = "grain, sale". Short-line check: `413` is first in 7 of 15 short lines it occurs in. The three unvalued signs after it (`575` great-measure/fort, `335`, `711`) are one block (`575-335` 21, `335-711` 18, `711-033` 15) = commodity or grade name, then the count.')
A('')
A('### R5. `060`: a particle, sound for the slot')
A('')
A('Not a damaging value but the commonest hole (5 of the 41, 222 uses in the corpus). Slot (S9): sits between a head sign and what it governs, never next to the jar. Proposal from the dictionary: the oblique/genitive linker *-iṉ* (the Dravidian genitive, written between head and noun), so `920-060-741` = "of the month, first ward" and `692-060-482-740` = "of the office, of the hill-share house". Check on short lines: 101 uses in lines of 2 to 5 signs, head sign on its left in 78 (77%), the ward jar to its right in 19; a particle that takes a head and a noun predicts exactly this pattern, no free-standing uses (first or last in 10 of 222 uses).')
A('')
A('### R6. Class slips, no new value')
A('')
A('Pair flags left over: `070-741` Arrow before First-ward (M-494, M-495): `070` stands as a name word here (arrow, a clan emblem as `455`), not a title; `095-390` staff-bearer + warrior (C-40) the same; `061-405` quarter-kindred (M-10) = `061` read as part of the name; `176-175` (M-623) two drawings of the seated person: iṟai written twice, one word.')

# ------------------------------------------------------------------ 6. signboard
A('')
A('## 6. The Dholavira signboard: what the gate said')
A('')
A('Object: gypsum letters on a board 3,000 x 370 mm, found lying in the west guard chamber of the north gate of the Castle, fallen from above the lintel of the central passage (excavation report quoted in `evidence/tmp/source_route_hunt_20260530/Dholavira-Bisht2015.txt`). Lipi id 144.1 stores 9 signs; the published count is 10. Reading order (stored order reversed): `820-611-388-820-850-645-031-821-798`. A published Mahadevan-number string for the ten (a reader\'s transcription, one source) is `391 256 327 391 261 134 98 391 391 53`; the crosswalk maps 391 to 820, 256 to 611, 327 to 388, 261 to 850, 53 to 798, so five of its ten signs and the last one agree with Lipi, and the extra signs are wheels: the board has 4 wheels in 10, and Lipi\'s `821` is one of them.')
A('')
A('| # | sign | picture | uses in corpus | slot elsewhere (measured) | value |')
A('|---|---|---|---|---|---|')
A('| 1 | `820` | six-spoke wheel | 244 | first in 187 (77%); a count of 1 to 3 follows in 138 of 139 counted cases; on the board it never has one | kāl, wheel, quarter |')
A('| 2 | `611` | vertical line with two small boxes on top | 6 | name-end slot (last 4 of 6); on 4 seals and 2 plaques; left neighbour `820` twice, right neighbour `388` once (this board) | a proper name (word unvalued) |')
A('| 3 | `388` | upside-down heart with bars | 59 | straight before the jar in 22 (37%), first in 17; paused value *aracu* "king, royal" | aracu, king |')
A('| 4 | `820` | wheel | | as 1 | kāl |')
A('| 5 | `850` | leaf or diamond on its point | 57 | right neighbour `900` month 15; left neighbour `407` herd 15; tablets 21, seals 20; Dholavira 3 | kaṇ, place, region |')
A('| 6 | `645` | plain X | 28 | counted thing (count before it in 13 of 28); right neighbour `590` box 7 | unvalued, a counted thing |')
A('| 7 | `031` | one tall stroke | 258 | container-series "one"; first in 99 | oru, one |')
A('| 8 | `821` | wheel variant | 14 | first in 6; right neighbour the jar 4; left neighbour `001` 5 | kāl-type opener |')
A('| 9 | `798` | leaf with pincers | 151 | straight before the jar 50, before `415` 23, before `240` 20; mid-name 108 | maru-, descendant, clan |')
A('')
A('Phrase structure: the wheel is text-initial in 77% of its corpus uses and the board repeats it every three or four signs, so the wheel starts a phrase: `[820 611 388] [820 850 645 031] [(820) 821 798]`, three phrases of 3, 4 and 3 signs (Mahadevan string: `391 256 327 | 391 261 134 98 | 391 391 53`). A wheel followed by a count is the seal opener "two quarters"; none of the board\'s wheels has a count behind it, so here the wheel is the head word of each phrase, not an opener of a seal text.')
A('')
A('Reading aloud: *kāl [611] aracu · kāl kaṇ [645] oru · kāl maru-*')
A('')
A('**Commitment.** The board names a ruler and a people and divides the city in quarters: "The quarters (kāl) of King [611]; the quarter-place [645], one; the quarter of the Maru (the descendants, the clan)". The city\'s name is the unvalued word `611` (a rare sign, 6 uses, name slot, standing before the title `388` in the only place it meets it): "King [611]" is both the ruler and the name the gate gave the town. No god (none of its nine signs sits in a slot we have tied to a god) and no welcome (no verb, nothing between phrases). It is a statement of ownership and subdivision, put where visitors read it from outside: this city, its king, its four quarters, its clan. The plan fits: the Lipi findspot column splits Dholavira into Castle, Bailey, Middle Town and Lower Town (four parts), and four wheels stand in the ten-sign board. Evidence list: the wheel as quarter (counts of one to three, 138 of 139; seals with it smaller, 525 against 645 mm2), `388` straight before the jar in 37% of its uses (the royal house), `798` straight before the jar in 33% (the clan word), `850` right before month `900` in 15 uses.')
A('')
A('What would move it: a transcription of the tenth sign; `611` and `645` values; a second reading of `850` (kaṇ "eye" or "place"). No image named for id 144 was found in the seal-image folder.')

# ------------------------------------------------------------------ files
A('')
A('## Files')
A('')
A('`work_scripts/long_common.py`, `long_cohesion.py`, `long_classgrid.py`, `long_manual.py`, `long_texts_build.py`, `long_texts_read.py`, `long_texts_stats.py`, `long_texts_stats2.py`, `long_vessels.py`, `long_signslots.py`, `long_texts_fix.py`, `long_texts_fix2.py`, `long_texts_report.py`. Data in `work_data/long_texts/` (`texts.json`, `read.json`, `class_bigrams.csv`, `sign_long_vs_short.csv`, `long_phrases_all.csv`). Rerun order: build, classgrid, read, stats, stats2, fix, fix2, report.')
open(f'{ROOT}/jobs/out/long_texts.md', 'w').write('\n'.join(L) + '\n')
print('written', len(L), 'lines')
