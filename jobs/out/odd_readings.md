# Making the odd readings read: slot words, count attachment, whole-object records

Scripts (in `work_scripts/`): `odd_common.py` (loader), `odd_1_slots.py` (every use of each blamed sign by slot), `odd_2_names.py` (name-sense tests, predictions in its header), `odd_3_counts.py` + `odd_3b_attach.py` (count attachment), `odd_3c_rescue.py`, `odd_3d_861.py` (second tries), `odd_4_values.py` (writes `work_data/values_master2.csv`), `corpus_build2.py` (the new reader), `odd_5_book.py` (writes `CORPUS.md`), `odd_6_draw.py` (new draw of 60; seed 20261119 is the graded one). Tables and printouts: `work_data/odd/` (`slots_census.csv`, `names_tests.csv`, `count_sides.csv`, `rescue_print.txt`, `object_records.csv`, `corpus_draw60.csv`, `build2_log.txt`). Output: `work_data/corpus_english2.csv`, `CORPUS.md`.

Plain words. **Face** = one inscribed side of an object. **Slot** = the job a sign does in its text: inside a **name** (the house or person on a seal), in a **count line** (amount on a tablet, tag or pot), **text-final** (last sign), **opener** (the formula at the front). **First catalogue** = Lipi (5,679 faces). **New texts** = the 1,183 second-catalogue lines with no partner in the first, never used to choose a value. **Short / stacked / tall strokes** = the three ways numbers are written (half-height in a row; half-height in two rows; full height). **P** = how often chance alone gives a result at least this strong; small P points to the stated direction. **Whole** = every sign on the face has a value we are building on. **Sense / odd / nonsense** = my read by eye: sense is something a seal, tag, tablet or pot would say; odd is awkward or hard to believe; nonsense is garbage.

## 1. What was found

1. **On a fresh seeded draw of 60 whole faces, 44 read as sense, 15 as odd, 1 as nonsense (73% / 25% / 2%). The first draw of 40 was 25 / 13 / 2 (62% / 32% / 5%).** Seed 20261119, drawn after the last rule change; the rules (`corpus_build2.py`, `values_master2.csv`) were frozen before the draw was run and nothing was changed after reading it. An earlier draw (seed 20261118) was read on the rules before the sign 390 cotton fix and the fifth-pass values: 44 / 16 / 0; it is superseded and not used below. The odd share fell 7 points; the 15 odd and 1 nonsense lines fall into six repeatable causes (section 5). No face of the 60 is in the first draw.
2. **Whole faces rise from 2,190 to 2,201 and the readings of most signs are reworded.** The 11 extra whole faces come from adding keeper 152 and the fifth-pass values (jobs/out/sound_list_v5.md: 923 ivory, 692 assembly, 711 grain measure, 370/371 spindle, 161, 347, 491/495 horn, 519, 565, 868; 8 wide values made strict); sign 390 is cotton, and 590-390 inside a name is the house "Boxed-cotton". All the signs blamed in the first draw now have a slot rule (section 3), and all 16 lines of the first draw that changed read at least as well (13 sense, 3 still odd: 1327.1, 145.1, 5576.1; the old per-line grades were not stored, so which lines were odd before is my re-reading of that file).
3. **A number or measure word inside a name is a spelled word, not a count, for the signs below; the evidence is mixed and I say which tests came true and which went against in section 2.** The strongest single result: the pair `840-032` (iṇai + tall two) ends a name, jar after it 35 of 42 in the first catalogue against 25 of 217 (12%) for any other sign + tall two, and 4 of 7 on new texts against 0 of 33. That is the name-use of 840 ("Peer-Two") behaving like a name unit and not like "two pairs".
4. **The stroke-style rule for counts is in** (short and stacked strokes precede the counted thing; tall strokes follow a measure sign and precede a counted container such as the cup 700). It changes where the count lands on 122 of 1,635 goods faces with a count (7.5%). On the 29-copy tablet `501-405-002-240-520` the two strokes now go with the high-star fish 240 (the star-names finding that short two + crest fish is one word) instead of the kindred sign 405.
5. **Multi-face objects are read as one record**: 902 objects have two or more faces; 306 have every face whole, 233 part, 359 damaged, 4 none (`work_data/object_records.csv`, `CORPUS.md` part 3). Example: object 1336 `176-740-400 / 034-700` reads "Four cups, for the junior of the Tax house."

## 2. Do number and measure words inside names have a name-like second meaning?

Predictions were written at the top of `odd_2_names.py` before it ran. If sign S is a name word when it stands in a name: P1 the strokes beside it are locked to one form inside names (as with the fish); P2 house-mates (Mohenjo-daro seals of one room within 3 ft) share S in names; P3 a name use of S ends the name (jar or closer follows) more than a count use does; P4 S in names goes with a fish crest (sky vocabulary) more than name faces in general do (29.5% of first-catalogue name faces carry a fish; 27.1% on new texts).

| sign | name word / count word | first catalogue | new texts | verdict |
|---|---|---|---|---|
| 904 | Dark-moon (*iru-tiṅkaḷ*, *iru* = two and black, built like *iru-mīn*) / "two months" | P4: fish on 23 of 46 name faces, P 0.003; P3 27/46 against 9/15 (no gap) | P4 5/14 (P 0.32) | name-sense true on P4, nothing else tested true; kept |
| 900 | Moon / month | P4 7/71 (against); P2 1 pair against 1.32 | too few | no support for the moon sense; kept as the plain word of the same sound |
| 840 | Peer (*iṇai* "equal") / pair | `840-032` ends the name 35 of 42 against 12%; P4 10/57 (against); P2 0 against 0.55 | `840-032` jar after 4 of 7 against 0 of 33 | true on the compound; against on fish and house-mates |
| 055 | the Twelve (*paṉṉiru*) / dozen | P3: ends the name 21/45 in names, 0/17 in count uses; P4 18/45 (P 0.085) | P1: two-stroke form in 7 of 9 name uses against one-stroke in 6 of 9 count uses | true on P3 and the new-text form lock |
| 690 | Ally (*piṇai* "union") / bound | P3: ends the name 85/113 (75%); P2 3 pairs against 0.93 (P 0.07) | 15/23 end the name | true on endings; house-mates borderline |
| 806 | Bounty (*viḷai* "yield") / produce | P4: fish on 48 of 80 name faces (60%), P 1e-5 | 10/19, P 0.016 | true on both catalogues |
| 501 | Throng (*kumi* "multitude") / heap | fish on 29 of 30 uses | none | one text (29 moulded copies); stands on that alone |
| 368 | Banner / banner, and text-final title (see below) | P4 14/89 (against); P2 5 pairs against 4.4 | too few | name-sense against; moved to the closer rule |
| 861 | Tribute (see below) / share | beside a transaction word 2/99 (against) | 5/21 against 4.0%, P 0.0012 | first word Holding went against; second word true on new texts only |
| 824 | Worth / price | P4 1/27 (against) | none | name-sense against; opener rule below |

Pooled test P1 (the number form beside these signs is locked inside names, loose in counts, with slot labels shuffled within each sign 3,000 times): first catalogue the top form covers 26 of 67 name uses against 165 of 362 count uses (difference −0.07, P 0.54, **goes against**); new texts 11 of 15 against 37 of 64 (+0.16, P 0.036, comes true). So the form lock found for fish does not generalise across all these signs in the first catalogue; it appears on new texts. P2 (house-mates) is weak everywhere (best P 0.07).

Rescues tried, and results:
- **368 banner** (name-sense against). Second reading: a title that closes a name, standing where the jar would. Text-final 34% against 26.7% (P 0.08, weak), but the jar is on the face in only 1 of 32 seals ending in 368 against 39.5% of all seals (P 2e-6; new texts 0 of 5). Rule: 368 last after a name on a seal = "standard-bearer" (comes true).
- **861 holding** (first word, *kāṇi* landholder, went against: a land word on the face 8 of 120 against 6.1%, none on copper tablets 0 of 120 against 4%). One new word, *kāṇikkai* "due, tribute": beside a transaction word (received 440, sale 892, given 890, tax 176/175) in the first catalogue 2 of 99 against 3.6% (**against**), on new texts 5 of 21 against 4.0% (P 0.0012, comes true). Kept as "Tribute" in names on the strength of the new texts, with the first-catalogue miss stated.
- **824 price**: at the front of a seal before a stroke it works like the share openers: the sign after the stroke is one that follows the share openers 9 of 9 against 49% of seals (new texts: no such use). Rule: opener "worth two".
- **060** away from the openers: the next sign is a fish or a number 28 of 51 against 22.9% (P 8e-7), new texts 5 of 11 against 22.1% (P 0.07). Rule: "Inner-" as a name prefix; between two numbers it reads "within".
- **Keepers 151-158 with a count**: 73 of 78 first-catalogue uses are text-final, 38 on seals, 40 on goods. Rule: counted on a seal it is a title spelled with the number (Three-keeper); counted on goods it is porters (three porters).

## 3. The fix for each blamed sign (slot rule in `values_master2.csv`, columns `short_name`, `short_count`, `short_final`, `short_open`)

| sign | in a name | in a count line (goods) | other slot |
|---|---|---|---|
| 904 | Dark-moon | two months | |
| 900 | Moon | month | |
| 824 | Worth | price (after sale 892 on tablets: "grain sale price") | opener "worth two" |
| 840 | Peer (`840-032` = Peer-Two) | pair (a lone 840 on a bangle) | |
| 055 | Twelve | dozen | |
| 690 | Ally | bound | |
| 806 | Bounty | produce (in the load tag) | |
| 501 | Throng | heap | |
| 368 | Banner | banner | text-final after a name: standard-bearer |
| 861 | Tribute | share | opener "share" |
| 060 | Inner (before a fish or name word) | | between two numbers: within; near an opener: in (unchanged) |
| 151-158 | Keeper | porter | text-final: keeper; counted on a seal: Three-keeper |
| 741 / 742 / 745 | First- / Second- / Third-ward (no "house") | | |

Count attachment (`reattach` in `corpus_build2.py`). For each run of strokes between two signs, each neighbour gets a score from how often its own neighbouring runs of that stroke style stand after it (a measure taking its count) or before it (a counted thing); counts come from all runs of both catalogues. The run goes to the higher score. Added rules: the ward signs 741/742/745 never take a count (they are already number words); when both neighbours score 0.8 or more with 6 or more cases each, the cup 700 wins (three cups) and any other pair goes to the measure; the jar 740 is never counted (the old parser sometimes counted it, which turned "peer, two, house" into "two houses").

Test on batches of near-identical objects (`odd_3b_attach.py`). Prediction written first: the right attachment gives the same counted signs in every variant of a batch. Copies of one tablet are the same string and a fixed rule reads them the same, so the test used batches: faces with the same non-count signs but different count patterns. Of 51 such batches (both catalogues), all variants agree in 35 (68.6%) under the old parser and 37 (72.5%) under the new rule; two batches only the new rule makes consistent, none only the old, sign test P 0.25. This is a small lead in the right direction, not a separation.

## 4. Grade totals (Lipi, 5,679 faces) and object records

| grade | old | new |
|---|---|---|
| whole | 2,190 | 2,201 |
| part | 1,276 | 1,268 |
| damaged | 2,079 | 2,079 |
| none | 134 | 131 |

Object records, 902 multi-face objects: 306 whole, 233 part, 359 damaged, 4 none.

## 5. The new draw of 60 whole faces (seed 20261119), read by eye

**44 sense, 15 odd, 1 nonsense.** File: `work_data/odd/corpus_draw60b.csv`. Every odd or nonsense line and the sign to blame:

| # | face | signs | new English | blame |
|---|---|---|---|---|
| 2 | 4936.1 | 031 | One | a lone number as the whole text of a seal |
| 7 | 2558.1 | 806-235-240-503-017-752-740 | Of the Bounty-Bamboo-star-High-star-Hill-Seven-Child of house | 017 seven spelled in front of 752 child-of |
| 8 | 434.1 | 001-034-700 | Five cups | 001 + 034: short and tall strokes added (cup counts are never 5) |
| 11 | 1180.1 | 503-861-368 | Hill-Tribute, standard-bearer | 861 as Tribute |
| 15 | 4182.1 | 904-530-705-002-231-590-390-740 | Of the Dark-moon-Proclamation-Kalam-Two-First-star-Boxed-cotton house | 530 and 705 left as plain words inside a name |
| 20 | 1496.1 | 700-741-033-904-740 | Of the Cup-First-ward-Three-Dark-moon house | 700 cup and ward 741 inside a name |
| 22 | 3909.1 | 803-861-002-705-033-482-740 | Of the House two shares three kalam Hill-share house (nonsense) | 861 and 705 counted inside a name; 803 |
| 25 | 2084.1 | 692-031-001-015-140 | Assembly; Seven ladies | 031 + 001 + 015 summed (mixed stroke styles) |
| 29 | 867.2 | 413-575-335-711-033-700 | Grain-Great measure-Town-Grain measure; Three cups | 575, 335, 711 joined as a hyphen name on a goods tablet |
| 30 | 5533.1 | 390-390-390 | Cotton-Cotton-Cotton | 390 repeated joined as a name instead of a count |
| 31 | 2061.1 | 590-540-002-605-760-740 | Of the Chest-Rice measure-Two-Granary-Child of house | 540 rice measure and 002 in a name |
| 35 | 631.2 | 803-233-176-435-690-740 | Of the House-Scabbard-fish-Tax-Rod-Ally house | 803 "House" in a house name |
| 39 | 5359.1 | 032-760-740 | Of the Two-Child of house | 032 spelled in front of 760 child-of |
| 54 | 532.1 | 590-705-868 | Chest-Kalam-Half-share | 705 and 868 hyphened on a goods tablet |
| 56 | 1149.1 | 700-892 | Cup-Sale | 700 cup as a name word on a seal |
| 60 | 1386.1 | 700 | Cup | 700 alone on a seal |

Causes (the next pass, not applied to this draw): measure words (700, 705, 530, 540, 575, 711, 868, 861) left or hyphened inside a name or on a goods line, 10 lines; strokes of two styles added together, 2; a spelled number before child-of (752/760), 2; 803 "House" inside a house name, 2; a repeated sign hyphened (390-390-390), 1; lone number on a seal, 1. Each is one rule: measure words in a name take the spelled or count form; mixed styles stay two numbers; a number before child-of is a count of children; 803 reads "Home" in a name; repeats read as a count.

## 6. What went against, and the rescue tried

- Name-sense for 900 (Moon), 368 (Banner), 861 (Holding) and 824 (Worth) fails every test in the first catalogue (section 2). Rescue for 368 came true (closer, jar absent 1 of 32); for 861 a new word came true on new texts only; for 824 an opener role came true (9 of 9). For 900 and 840 outside the pair `840-032` no rescue was run; they stay as the sound-matching word the slot rule gives.
- The form lock of the star-names job (the number beside a sign is fixed inside names) does not carry across these signs in the first catalogue (P 0.54, wrong way); it comes true on new texts (P 0.036). The slot census suggests the parser's own name/count labels are noisy for these signs, which weakens every pooled test.
- House-mates sharing the sign is not shown for any of these signs except borderline 690 (P 0.07).
- Count attachment: the batches test separates the rules only slightly (37 against 35 of 51). The rule is built on all-run adjacency statistics, so signs seen only a few times fall back to the global stroke-style rates.
- I read the draw myself and designed the rules; no second reader. The first draw's per-line grades were not stored, so the 40-line comparison rests on my re-reading of the 16 changed lines.
- Status changes in `values_master2.csv`: keeper 152 added strict; eight wide values made strict and the fifth-pass words folded in as wide (405, 645 and 236 moved to testing, so they print as [number]).

## 7. Files and next

`MAP.md` and `DIARY.md` were not edited (outside the files named). Next: apply the five single-line rules listed under the odd table and draw a third seed to read; run the slot split on the other number-word signs that sit inside names (048 the Seven, 877, 320); build the `Inner` prefix test on 060 + fish into the star-names table.
