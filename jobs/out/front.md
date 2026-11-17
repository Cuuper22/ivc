# The front of a text

Word-free job, 2026-11-17. Sign numbers, pictures, jobs, counts and findspots only. Scripts `work_scripts/front_common.py` and `front_1_inventory.py` to `front_10_families.py`. Each script has its predictions in the top docstring, written before its numbers. Tables and logs are in `work_data/front/` (`f1_*` to `f10_*`, `log_*.txt`, 0.3 MB). Every script runs in under 4 minutes. Counting follows FRAME.md, "How pairs are counted": one row per stone; identical texts at one site and findspot counted once (a **copy event**); chance drawn by dealing labels only among objects that can carry them, inside the stated group.

## Plain words

- **Front word**: a sign that opens a text. It is fixed by a rule written before any count: frame v2's front class (820 861 817 920 692 880 824 545 091 550 360 556), plus any sign that stands first in 60%+ of its uses and is followed by a slot sign in at least 4 cases and half of its first-position uses. The rule added three: 347, 201, 263. A text **begins with a front** when its first sign is a front word.
- **Slot sign**: the sign right after a front word. Frame v2's slot class is 002 (two short strokes), 060 (a short and a tall stroke), 741 / 742 (jar-like variants), 368 and 365. 745, the third jar-like variant, is checked beside them.
- **Front unit**: the front word plus up to two slot signs, so 920-060-741 is one unit.
- **Name**: the signs between the front unit and the ending. **Ending**: the run of closers (jar 740, spear 520, porters 151-158) and after-jar titles (comb 400, man 090, 527, 621, 679, ...) at the end of a text.
- **Field**: everything before the first slot sign (defined in finding 2).
- **Count line**: numbers followed by one counted thing (`003-390`).
- **Impression**: a clay tag or sealing, or a stamped pot. These are the marks seals left on goods.
- **Dealt / dealing**: a control that shuffles a label (which front, front or none, which slot) at random among the texts of the stated group, thousands of times. **P** is the share of deals at least as extreme as the real count. **Decoy**: a sign of the same frequency put in a real sign's place.
- **Size residual**: a seal's log face area minus the median for seals of the same site group, text length and format. A residual of +0.10 means about 10% bigger than matched seals.

## What was found

**1. The slot sign, not the front word, marks the front. It closes a field that sits before a short name.** After a slot sign, names are short whether a front word or some other sign stands before it:

- On seals, the name after a front word + slot averages 2.52 signs.
- After a field with no front word (`705-500-741`, `851-741`, `260-368`, `634-368`, `891-060`; 144 seal texts) it averages 2.42 signs. The difference is 0.11 (P 0.20).
- Seals with no field average 3.24 signs (difference 0.82, P 0.0003).
- After both kinds of field the name starts with a crest about a third of the time (0.36 and 0.33, against 0.23 with no field). A **crest** is the house emblem at the front of a name, such as the fish signs.

A front word with no slot after it (820-001-..., 820-013-..., 091-056-...; 77 seal texts) behaves like no field at all: names of 3.76 signs, crest first 3%.

Decoy control: 20 sets of signs of the same frequency were cut at in place of the slot signs. The rest of the text came out shorter (1.65 signs against 2.36, decoy maximum 1.98) and opened with a crest far less often (0.114 against 0.326). It was a whole attested text less often too (14.2% against 24.0%). The rival reading is that names are short because a field uses up room on the stone. It fails: on stones in the smaller half for their site and format the gap is 0.16 sign (P 0.095); on the bigger half it is 1.51 signs (P 0.0003).

- **What it means:** a seal text has two shapes. One is `[field][slot][short name][ending]`. The other is `[long name][ending]`. The slot is the boundary that closes the field. The front words are only the commonest fillers of that field.
- **What it opens:** the 175 texts with fields that hold no front word, and the 36 with a sign before the front word (`603-861-002`, `317-920-002`, `491-920-002`, `741-820-002`, `416-861-002`), are new front material (`f9_field_strings.csv`). Long frontless names hold a slot-class sign in second place 9% of the time, so part of them is an unmarked field.

**2. Two front families, set by the slot, and the pairing is rigid.** Front word against the sign after it (copy events, front words with 5+ texts): chi-square 1352, against a mean of 125 and a maximum of 270 when the after-sign is dealt within site 5,000 times (P 0.0002). Chi-square measures how far a count table is from what free pairing gives.

- **The 002 family:** 817-002 (145 times, against 93.6 dealt), 861-002 (138 against 85.5), 824-002 (9), 880-002 (5).
- **The 060 family:** 920-060 (64 against 19.3), 692-060 (39 against 12.1), 550-060 (26 against 9.1), 201-060 (5).
- 817, 861 and 692 are never followed by 060 or 002 across the line (0 against 37.6, 33.4 and 26.5 dealt). 920 takes 002 once against 44 dealt.
- 820 alone takes both slots (002 93 times, 060 24) and also 001 (15).
- 741 as a slot follows 920-060 (38) and 347 (9 moulded copies of one tablet text). 368 follows 817 (19, against 7.9 dealt).

The two families differ in nothing else measured: impression share P 0.13, endings P 0.17 to 0.88, unicorn P 0.62, Harappa share P 0.48, early time bin P 0.29. The one lean is size: seals of the 060 family are about 8% larger than seals of the 002 family (P 0.052).

- **What it means:** front word and slot form one fixed two-part unit, in two spellings. Which family a text uses carries no information about the person, the place or the object.

**3. On seals the front is free of the name.** Take the same name (the same signs between front and closer) with a front and without one, and deal the front unit within site and name length:

| test | real | dealt | P |
|---|---|---|---|
| seals: names found both with and without a front | 49 | 49.3 | 0.52 / 0.60 |
| seals, names of 2+ signs | 30 | 27.9 | 0.29 (high) |
| seals: names under two different front words | 21 | 22.7 | 0.35 |
| all objects, dealt within length + site + kind | 73 | 89.0 | 0.0025 (low) |
| all objects, two different front words | 22 | 33.3 | 0.0015 (low) |

On seals a front is put on or left off a name exactly as often as chance gives, and one name takes different front words as often as chance gives. Examples:

- `415-100-740` stands bare on a Mohenjo-daro seal and a Harappa tablet, and on seals behind 820-002, 817-002 and 861-002 (twice). Behind 920-060-741 it stands on a tag.
- `255-435-690-740` stands bare on 3 seals and 3 tablets, and on seals behind 817-002 and 861-002.
- `061-142` stands bare on 3 Harappa objects and behind 817-002 and 861-002 at Mohenjo-daro.

The with/without pairs are never in the same building (0 of 862 pairs) and are in the same city half the time. The test file is `f2_tests.csv`; the cases are in `f2_cases.csv` (77 names, 377 texts).

Seal pairs with sizes (190): the fronted stone is larger than its frontless partner in 111. The mean size residual gap is +0.129 (sign-flip P 0.003), but the pairs share names, so this is a lean. A sign-flip test swaps each pair's two members at random to see how often a gap this large comes up by chance.

Across all objects with object kind held fixed, names do keep their front a little (0.82 times chance; two different front words 0.66 times chance). That comes from tablets, where a name keeps its heading (`heads.md`).

- **What it means:** the front is not part of the name (that would give 0 cases), and on seals it is not a fixed personal title either (that would make two different front words rarer than chance).

**4. The front words are free variants of each other.** Front-word labels were dealt within site and object kind (3,000 deals) and set against each property:

| property | P |
|---|---|
| ending class | 0.071 |
| count line or name | 0.80 |
| crest class | 0.57 |
| found as impression | 0.38 |
| Harappa against Mohenjo-daro | 0.095 |
| time bin | 0.20 |
| object kind | 0.035 |
| animal | 0.043 |

The two leans are 692, which sits on tablets more often (30% of its texts against 13-18% for 817, 861 and 820), and 091, which is rarely on a seal with an animal.

There are not two kinds of front, one for names and one for counts. Count lines are 28 of 301 complete texts in the 002 family and 8 of 131 in the 060 family; with the family label dealt, P 0.19. Every main front word heads both names and count lines (817: 14 count lines and 64 jar names; 861: 13 and 47; 820: 8 and 55; 920: 3 and 29). The table by front word is `f3_by_front.csv`.

**5. The slot is a marker, not a number series.**

- After the diamond fronts the stroke count does not run. After 861, 002 is 98% of all stroke signs (138 of 141; 003 once, 013 twice). After 817 it is 94% (145 of 154).
- The wheel 820 takes 001 (15), 002 (93) and 060 (24). This split goes with nothing: ending P 0.40, kind 0.69, city 0.079, time 0.72, crest 0.64, length 0.95.
- After 920-060 the third sign is 741 (38), 742 (9), 745 (3) or something else (14). This goes with nothing either: P 0.31 to 0.89 for ending, kind, city, time, crest and length.
- Five names stand after both 741 and 742 (or 741 and 745) somewhere in the corpus: `590-390`, `350-463-798`, `220`, `415-100`, `233-798`. So the jar variants are interchangeable spellings, not first, second and third of a series.
- **The one slot that carries information is 368 after 817.** 817-368 is on 12 of 28 tablet texts of 817 against 7 of 121 seal texts (object kind P 0.002; ending P 0.011; length P 0.007). It is the Harappa tablet heading `817-368-690`.
- The same front and the same name with a different slot: 5 cases, against 9.06 when slots are dealt within front word and site (P 0.011, low). The cases are 817-002/368 + `003-390`, `220`, `233`, 817-368/365 + `690`, and 817-002 against bare 817 + `004-390` (`f4_same_front_name_diff_slot.csv`).

**6. Tablets and seals open from two different sets.**

- 413 opens 2 of 1,535 complete seal texts (0.13%) against 28 of 1,293 tablet texts (2.2%).
- 415 opens 0.8% of seal texts against 2.2% of tablet texts.
- 501 opens 29 tablet texts and 0 seal texts.
- Of the signs that mostly stand first on each kind, the shared ones are 817, 820, 692 and 491.
- Seal front words on tablets (109 complete texts, 96 at Harappa, 82 moulded) are seal texts written on clay: front + name + closer. 861-002 does this 13 times, 692-060 and 347-741 8 times each. The exception is 817-368, which heads an amount or measure 8 times (the heading line).
- Count-line seals use the seal set: 36 of 84 copy events carry a front (817-002 8, 861-002 8, 820-002 6, then single cases).
- On the multi-stamp lumps, 16 of 82 stamps open with a front word. All are seal-set: 861-002 5, 820-002 4, 817-002 3, 820-032 2, 880, 550. The short stamps are `861-002-235`, `861-002-236`, `820-002-220-234`, `820-032-130` (twice), `820-002-000-520`.
- A seal front word directly followed by 413 or 415: 1 text.
- Front share by object kind (stones): seals 28.8%, tags 40.1%, tablets 12.8%, other 13.5%, pots 6.7%, copper 1.1%.

- **What it means:** the tablet headings (413-575, 413-892) are a separate system. The seal front belongs to seals and to the clay impressions they made.

**7. One front per object, and almost never a second front in a text.**

- On 703 objects with 2 or more readable faces, a front on 2 or more faces happens 7 times, against 7.45 when faces are dealt among such objects of the same site and kind (P 0.67). Those 7 are mostly the same text repeated (the triple impression M-1385, the duplicate faces of H-597).
- A text that opens with a front and starts again with a front + slot inside: 1 of 603 (M-317, `920-401-692-060-255`).
- Front words standing inside a text are mostly other jobs:
  - 861 after a number (34 texts, 30 of them tablets: `003-861`, the counted diamond);
  - 920 after 320, 318 or 140 (a name part, `320-920-740`);
  - 824 after 892 (`413-892-824`, the Harappa heading).

The catalogue has no line breaks inside a face, so faces stand in for lines.

**8. Seals without a front are the default (71.5%).** The front changes the text, not the stone.

| measure | front | no front | dealt | P |
|---|---|---|---|---|
| size residual, median | +0.007 | 0.000 | +0.003 | 0.37 |
| raw log area, median | 6.469 | 6.338 | | 0.0003 (the longer text) |
| text length, mean | 5.31 | 4.23 | | 0.0003 |
| name length, mean | 2.71 | 3.63 | | 0.0003 (low) |

Format P 0.56, time bin P 0.34, city P 0.12, animal P 0.065 (unicorn 66% against 60%).

The ending differs (chi-square 35.6 against 7.1, P 0.0005):

| ending | front | no front |
|---|---|---|
| plain jar | 42.1% | 33.4% |
| count line | 8.2% | 4.4% |
| porter | 2.5% | 5.6% |
| comb | 1.4% | 2.4% |
| no closer | 30.4% | 41.5% |

The front as an addition: the rest of a fronted text, once the front unit is removed, is itself a whole frontless text somewhere in 152 of 578 cases (26.3%). Frontless texts with the same number of signs cut off give 17.7% (20 rounds, maximum 19.7%), a ratio of 1.49. 125 of 1,182 frontless name + closer texts also appear whole behind a front.

## What the front is

Plain claim: **the front is a heading field placed before a short personal name on a seal. The field says in what capacity the stone seals, not who holds it.** The numbers that pin it down:

- **Not part of the name.** On seals the same name appears with and without it at chance (49 against 49.3).
- **Not a fixed personal title.** One name takes two different front words at chance (21 against 22.7). A title would stay with its holder.
- **Not a place.** No front word or family splits by city (P 0.095 and 0.48) or by building (0 of 862 with/without pairs in one building).
- **Not a number or series.** The slot does not run 1, 2, 3 (002 is 98% after 861), the jar variants are interchangeable on the same names, and the 820 001/002/060 split goes with nothing.
- **A kind-of-seal marker, the reading that fits.** The fielded seal is a separate text shape. Its name is a crest plus about one sign (2.5 against 3.6, with the gap biggest on big stones). It ends more often in the plain jar and in count lines, and less in porter and comb. It is pressed on goods: 40% of tags open with a front against 29% of seals, and the short front stamps sit beside name stamps on multi-stamp lumps. The front words inside the field are interchangeable spellings in two families (002, 060).

Building on: `[field][slot]` = an office or capacity heading, "sealing for the X office". The holder's short name follows, and the same person can seal with or without it. The long frontless name is the private seal, with the house and person spelled out in full.

Per front word:

- **817, 861, 824, 880 (diamond family + 002) and 920, 692, 550, 201 (bracket / X / pincers family + 060):** the office heading. These are free variants on every measure except the leans above (692 more on tablets, 060 seals about 8% larger, P 0.052). 861 is also the counted head on Harappa tablets (`003-861`, 30 tablets), which fits the MAP guess that it is a head-count word.
- **820 (wheel):** the same heading, with a stroke count (001 / 002) that goes with nothing yet. It is the one front word where a number may live.
- **817-368:** a tablet form of the heading at Harappa (`817-368-690` + cups).
- **091:** a tag and tablet front (091-056-002-417-890-892, seven copies of one stamp at Kalibangan; 091-368 + cups on Harappa tablets), rarely on seals with an animal.
- **347-741:** one moulded tablet text (`347-741-176-740-090`, 9 copies).
- **'Other' fields (705-500-741 ×12, 851-741, 260-368, 634-368, ...):** the same field filled with rarer signs.

Tests that would settle what is still open:

1. Does the field's filler match the holder's crest on the same multi-stamp lump (`861-002-235` beside a 235 name)?
2. Do the 'other' field strings repeat across cities the way the classic front words do, or are they one-city offices?
3. Does 820-001 against 820-002 match tablet counts in the same findspots?
4. Do the long frontless names hold an unmarked field (the slot-class sign in second place in 9% of them), and is it the same field?

## Tables

### Front words (`f1_front_words.csv`; faces where the sign stands first, stones by kind)

| front | faces first | share of its uses first | seal | tablet | tag | pot | other | cities | sign after it |
|---|---|---|---|---|---|---|---|---|---|
| 817 | 188 | 0.85 | 130 | 34 | 14 | 5 | 2 | 12 | 002 147; 368 19; 013 5 |
| 820 | 185 | 0.78 | 133 | 25 | 11 | 9 | 5 | 16 | 002 93; 060 24; 001 15 |
| 861 | 173 | 0.64 | 118 | 22 | 13 | 13 | 3 (+2 copper) | 14 | 002 139; 368 5; 741 3 |
| 920 | 86 | 0.57 | 66 | 10 | 5 | 2 | 3 | 9 | 060 64 |
| 692 | 59 | 0.81 | 38 | 18 | 1 | 2 | 0 | 6 | 060 39; 001 4 |
| 550 | 54 | 0.45 | 31 | 12 | 3 | 3 | 5 | 6 | 060 26; 527 5 |
| 091 | 24 | 0.86 | 11 | 5 | 8 | 0 | 0 | 7 | 056 8; 368 3 |
| 824 | 13 | 0.41 | 10 | 3 | 0 | 0 | 0 | 5 | 002 9 |
| 545 | 10 | 1.00 | 10 | 0 | 0 | 0 | 0 | 2 | mixed |
| 556 | 9 | 0.82 | 4 | 1 | 0 | 1 | 3 | 3 | mixed |
| 347 | 9 | 0.90 | 0 | 9 | 0 | 0 | 0 | 1 | 741 9 |
| 880 | 8 | 0.73 | 6 | 0 | 2 | 0 | 0 | 3 | 002 5 |
| 360 | 6 | 0.50 | 4 | 2 | 0 | 0 | 0 | 2 | mixed |
| 201 | 5 | 1.00 | 4 | 1 | 0 | 0 | 0 | 2 | 060 5 |
| 263 | 5 | 0.83 | 3 | 2 | 0 | 0 | 0 | 3 | 368 2; 741; 365 |

### Slot signs (`f1_slot_signs.csv`)

| slot | uses | right after a front | share | fronts before it |
|---|---|---|---|---|
| 002 | 844 | 457 | 0.54 | 861 173, 817 155, 820 101, 824 9, 920 6, 880 5 |
| 060 | 219 | 170 | 0.78 | 920 65, 692 44, 550 28, 820 24, 201 5 |
| 741 | 224 | 56 | 0.25 | 920+060 38, 347 9, 861 4 |
| 368 | 117 | 41 | 0.35 | 817 20, 861 11, 091 3 |
| 742 | 56 | 12 | 0.21 | 920+060 9, 861 2 |
| 745 | 36 | 3 | 0.08 | 920+060 3 |
| 365 | 18 | 4 | 0.22 | single cases |

741, 742 and 745 also open texts themselves (26, 16 and 19 times) and stand after 500 and 390 (`500-741` 15, `390-741` 13), the 'other' fields of finding 1.

### Share of texts that begin with a front (`f1_share_by_kind.csv`; stones with a readable first sign)

| kind | stones | with a front | share | complete stones | share |
|---|---|---|---|---|---|
| seal | 1,969 | 568 | 0.288 | 1,506 | 0.290 |
| tag (impressions) | 142 | 57 | 0.401 | 75 | 0.440 |
| tablet | 1,120 | 143 | 0.128 | 841 | 0.130 |
| other objects | 156 | 21 | 0.135 | 123 | 0.106 |
| pot | 525 | 35 | 0.067 | 294 | 0.037 |
| copper tablet | 174 | 2 | 0.011 | 160 | 0.006 |

Seal share by city: Mohenjo-daro 0.310, Harappa 0.251, Dholavira 0.253, Lothal 0.324, Chanhu-daro 0.345, Kalibangan 0.122 (49 stones), Nausharo 0.467 (15).

### What each front goes with (`f3_by_front.csv`; complete copy events)

| front | texts | count line | jar | jar + man | spear | fish crest | seal size residual (median) | impression share | Harappa share of MD+HP |
|---|---|---|---|---|---|---|---|---|---|
| 817 | 146 | 0.096 | 0.438 | 0.027 | 0.103 | 0.248 | -0.065 | 0.086 | 0.399 |
| 861 | 125 | 0.104 | 0.376 | 0.032 | 0.080 | 0.303 | +0.028 | 0.076 | 0.323 |
| 820 | 125 | 0.064 | 0.440 | 0.032 | 0.072 | 0.222 | -0.056 | 0.065 | 0.329 |
| 920 | 63 | 0.048 | 0.460 | 0.000 | 0.063 | 0.177 | -0.010 | 0.070 | 0.261 |
| 692 | 43 | 0.070 | 0.558 | 0.070 | 0.070 | 0.341 | +0.292 | 0.017 | 0.556 |
| 550 | 36 | 0.056 | 0.389 | 0.028 | 0.028 | 0.179 | +0.020 | 0.056 | 0.415 |
| none (all objects) | 2,915 | 0.135 | 0.224 | 0.023 | 0.059 | 0.112 | 0.000 | 0.039 | 0.609 |

### Field kinds (`f9_fields.csv`; seals)

| field | texts | name + closer texts | name length | crest first | text length |
|---|---|---|---|---|---|
| front word + slot | 356 | 228 | 2.52 | 0.364 | 5.46 |
| sign(s) + front word + slot | 33 | 25 | 2.64 | 0.360 | 7.12 |
| other sign(s) + slot | 144 | 89 | 2.42 | 0.326 | 5.81 |
| front word, no slot | 77 | 34 | 3.76 | 0.029 | 4.56 |
| no field | 921 | 473 | 3.24 | 0.230 | 3.88 |

## What went against

- **Prediction that the front is a title kept by its holder (front_2 P2).** Two different front words on one seal name: 21 against 22.7 (P 0.35). It is not rarer than chance. Redesign run: names of 2+ signs, 12 against 13.5. New idea, followed in finding 1: the front word is one interchangeable filler of a field.
- **Prediction of two kinds of front, one for names and one for counts (front_3 P2).** 002 family 9.3% count lines against 060 family 6.1% (P 0.19); by front word P 0.80. Every front heads both kinds of text.
- **Prediction that fronted seals are bigger (front_3 P3, front_7).** Size residual +0.007 against 0.000 (P 0.37). The raw size gap is the longer text. Only the 060 family leans larger than the 002 family (P 0.052), and with/without seal pairs lean larger for the fronted stone (+0.129, pairs not independent).
- **Prediction that the 002 family is the stamping family (front_3 P4, front_10).** Impression share 8.9% against 3.1% looks like a gap, but with labels dealt within site P is 0.13.
- **Prediction that the front replaces the crest (front_8 P1).** It went the other way: names behind a front open with a crest more often (0.309 against 0.192; P 0.021, high side). The front sits before the crest, not in its place. Redesign: head/tail matching. Fronted names are found as the tail of a longer frontless name 15.2% of the time against 9.9% for frontless names, and the extra first sign is a crest in 38 of 93 matches (41%), about the same as for frontless names (55 of 125, 44%), so no crest substitution. The new idea that came out of this is finding 1 (the field).
- **Prediction that the front is a clean addition (front_7 P2) at 3 times the control.** It came out at 1.49 times (26.3% against 17.7%).
- **Names under the front on all objects** keep their front somewhat (0.82 times chance). This comes from tablets: on tablets a name keeps its heading (see `heads.md`).
- **Slot difference within one front and name** is rarer than chance (5 against 9.1). The cases are the 817-368 tablet heading, so the slot is not completely free there.
- **No line information** inside a face in the catalogue, so 'each line starts with a front' could only be tested as faces.

## Files

Scripts: `work_scripts/front_common.py`, `front_1_inventory.py`, `front_2_withwithout.py`, `front_3_goeswith.py`, `front_4_slots.py`, `front_5_sets.py`, `front_6_doubling.py`, `front_7_nofront.py`, `front_8_replace.py`, `front_9_field.py`, `front_10_families.py`. Tables and logs: `work_data/front/`.
