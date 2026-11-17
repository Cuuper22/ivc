# Hands: the seal cutters

Word-free job, 2026-11-17. Photos, sign numbers and findspots only. Scripts: `work_scripts/hands_common.py` (loader and sheet maker), `hands_1_candidates.py`, `hands_1b_tally.py`, `hands_2_pairs.py`, `hands_3_xc_score.py`, `hands_4_md_score.py`, `hands_5_order.py`, `hands_6_relook.py`. Each has its rules, seeds and predictions in its top docstring, written before the numbers. Row-by-row judgements and keys are in `work_data/hands/` (`unfinished_judged.csv`, `twin_relook.csv`, `cross_city_judged.csv`, `md_judged.csv`, `order_judged.csv`, the `*_key.csv` files, the raw judgement text files, and the contact sheets, 7.7 MB in all).

## Plain words

- **Seal photo naming rule**: a file is `<catalogue id>_<face letter>[_<note>].jpg`, for example `M-224_a.jpg`. The catalogue id (M = Mohenjo-daro, H = Harappa, K = Kalibangan, L = Lothal, C = Chanhu-daro, B = Banawali, and so on) is the "cisi" id. Face letter A/a is the front face; other letters are other faces. Of 2,290 seal faces on 2,238 seals, **1,600 faces have a photo on disk** (Mohenjo-daro 1,020, Harappa 358, Lothal 92, Kalibangan 53, Chanhu-daro 28, Banawali 14). Dholavira has 136 seals and one photo. The photos are small scans from the old catalogues (230 to 480 px tall), so fine features are readable only on clean stones. About 754 photo panels were opened in this job (a stone that sits in several pairs was opened once for each pair).
- **Hand**: the habit of one cutter in drawing the same things. Judged from seven features fixed before judging: bull's eye, horn, collar and shoulder mark, the stand in front of the animal, stroke depth and sign proportions, spacing, frame line. Calls: **same** (4 or more features agree, none clashes), **near** (3 agree, none clashes), **different** (2 or more clash), **cannot tell** (a stone is worn, broken, a bar, or has no animal). **Alike** = same plus near.
- **Control pair**: two stones from the same two cities as a text-sharing pair, same "both unicorn or not" status, sharing no run of 2 signs. Pair labels were random numbers; the kind of each pair was looked up only after all 120 were judged.
- **Making order**: which of the two fields was laid out first. I read "text cramped" (signs squeezed into what the animal left, last sign tucked against the horn, text pushed into a corner) as the animal being planned first; "animal cramped" (animal small and low under big signs) as the text being planned first. This is a layout reading, not proof of which line was cut first.

## What was found

1. **Stones with the text cut and the animal field left empty exist: 6 of 60 square blank-animal seals, and 3 of the 6 are at Lothal.** L-55, L-58, L-97 (Lothal) and M-315, M-1195, M-1232 (Mohenjo-daro): text in the upper band or half, the lower field smooth. Of 13 animal seals whose catalogue text is lost, 1 (K-35 at Kalibangan) has the animal cut and the text field blank (a small triangle only); 10 have the text broken or worn away; 2 cannot be told. Text cut and animal empty (6) against animal cut and text empty (1): text-first is the rule where the order shows. Lothal holds 3 of the 6 against 9 of the 60 in the pool (P 0.038 that Lothal would hold 3 or more by chance: Lothal has more unfinished stones than its share). Means: the town where the known unfinished copy L-55 was found (twin L-35, finished) made more unfinished stones than others; stones were being made there. Opens: the L-55 case is one of a Lothal habit, and the 4 Lothal sector codes (SRG 2B 10, SRG 2GX 9) can be set against the excavation plan.
2. **The same text on two stones in two cities does not predict the same hand beyond what any two stones from the same two cities show.** Text-sharing pairs: 7 alike (all near, no same) of 37 judged (19%), 23 of 60 cannot tell. Control pairs (no shared run): 4 alike of 32 judged (12.5%), 28 of 60 cannot tell. The gap is 6.5 points (permutation P 0.35, Fisher P 0.26). On all 60 pairs each: 12% against 7%. The 8 twin pairs from the earlier job, looked at again: 1 same (L-35 and its unfinished copy L-55, one city) and 7 near, 5 of the 8 between two cities (H-62/M-1108, H-451/M-879, H-49/M-401, K-19/M-224, K-19/M-404): the earlier reading stands as "same or near" and none was downgraded. What opens: **hand similarity here is a style that crosses cities, not a text that carries its cutter.** Lh-1 (Lohumjo-daro) is judged near to H-450 (a control pair, no shared text) and near to H-13 (a text pair); both partners are Harappa unicorn stones with collar bands, a long upswept horn and a tall hatched-box stand. 9 of the 11 alike cross-city pairs share that tall hatched-box stand on a pole (the stand is one of my seven features, so this is partly built in).
3. **A Mohenjo-daro building does not get its seals from one cutter.** Alike rates among judged pairs: same building 8 of 35 (23%), different buildings in the same area 7 of 31 (23%), different areas 4 of 19 (21%). Fisher P between same building and either other group: 0.61 and 0.58. Cannot-tell counts: 25, 29, 41 of 60 each. One pair was judged same (M-13 and M-22, both in house HRB 2V, a clean pair with matching horn, collar bands, stand and text strokes); the other 18 alike pairs are near. None of the 180 pairs carries one text on both stones. All Mohenjo-daro pairs together are 19 alike of 85 judged (22%), against the cross-city control 4 of 32 (12.5%): P 0.18, the direction one would expect if one city has a more shared style but the numbers cannot carry it.
4. **Making order: the text is cramped more often than the animal, and which one is cramped follows the length of the text.** 40 seals drawn by seed (18 Mohenjo-daro, 8 Harappa, 6 Lothal, 4 Kalibangan, 4 Chanhu-daro): text cramped by the animal 13, animal cramped under big signs 7, even 19, cannot tell 1. Mean text length: 6.0 signs where the text is cramped, 5.6 even, 3.6 where the animal is cramped. Long texts shrink into a thin band or a corner (K-10 at 10 signs, H-20 at 10, M-119 at 10); short texts are cut large and the animal shrinks (M-1088, M-87, M-1202, K-1). Means: the cutter laid both fields out before cutting either, then sized the signs to the text. Ruled guide lines: 0 of 40. Erased or ghost signs: 0 of 40.
5. **Hairline sketches: 4 stones carry sign shapes drawn in thin scratches, with at most a few signs cut deep.** C-31 (Chanhu-daro), H-613 (Harappa), L-62 (Lothal), M-1228 (Mohenjo-daro). M-1228 has two signs (a diamond and a stroke) cut deep with the rest still hairline; C-31 has hairline signs only on a smooth dark face. These are the guide line stage the 40 finished seals no longer show: the text is drawn thin first, then cut. They were found among the blank-animal candidates and were first sorted as "cannot tell"; counted with the unfinished stones, text drawn or cut with no animal is 10 of 60.
6. **What the photos say about who cut seals.** City workshops working to shared styles, with some cutters or stones travelling: (a) unfinished stones sit scattered, one per house, and 3 of 6 at one city (no household pile); (b) no building signal in 180 Mohenjo-daro pairs (23% against 23% against 21%); (c) near-identical stones sit in two cities (K-19 at Kalibangan with M-224 at Mohenjo-daro share pose, horn ornament and stand; the text cut of K-19 also matches the bar M-404); (d) the style that links Harappa and Lohumjo-daro stones holds without shared text, so a cutter's style moved with or without a text. How a seal was made: layout of the two fields first, thin sketch of the signs, text cut deep, animal added or left for later (6 stones show text cut and the animal field smooth).

## Tables

### 1. Blank-animal candidates, sorted from photos (`unfinished_judged.csv`)

Rule fixed first: seal faces with a photo, catalogue animal field empty, type SEAL:S or both sides 15 mm or more with long side at most 1.35 times the short side. This gave 69 faces on 60 stones (all kept, fewer than 80). The catalogue has no note field and no unfinished/blank/recut/worn code (type codes are only SEAL:S, R, C, CY, L), so shape and size are the only rule. Control pool: 13 animal seals with photo whose catalogue text is entirely lost.

| site | a: text cut, animal field empty | b: text only by design | c: animal worn or broken | d: animal cut, text empty | e: cannot tell | f: hairline sketch |
|---|---|---|---|---|---|---|
| Mohenjo-daro | 3 | 16 | 1 | 0 | 7 | 1 |
| Harappa | 0 | 6 | 1 | 0 | 5 | 1 |
| Lothal | 3 | 2 | 1 | 0 | 2 | 1 |
| Chanhu-daro | 0 | 2 | 0 | 0 | 0 | 1 |
| Kalibangan | 0 | 0 | 0 | 0 | 4 | 0 |
| other (Allahdino, Banawali, Surkotada) | 0 | 1 | 0 | 0 | 2 | 0 |
| all 60 stones | 6 | 27 | 3 | 0 | 20 | 4 |
| control pool, 13 animal seals with lost text | 0 | 0 | 10 | 1 | 2 | 0 |

The six "a" stones: L-55 (no findspot recorded), L-58 (SRG 2B 10, layer 13), L-97 (SRG 2GX 9, layer 2), M-315 (VSA, house 2VIII), M-1195 (DKG, Central Street), M-1232 (DKG(S), house 7III room 43). Same house: none. Same area family: 2 pairs (the two Lothal SRG stones, the two DKG stones) against 1.95 when the "a" label is dealt at random among stones of the same site 5,000 times (P 0.54). No excavation report with stone debris or workshop locations could be read in this job (one web page read gave a bead-factory plan but no position and no seal debris), so the workshop-against-house question is open on the debris side; on the findspot side the unfinished stones are scattered.

### 2. Twin pairs looked at again (`twin_relook.csv`)

| pair | stones | cities | call | why |
|---|---|---|---|---|
| T3 | H-62 / M-1108 | Harappa / Mohenjo-daro | near | text signs same forms and spacing; animals differ |
| T4 | H-451 / M-879 | Harappa / Mohenjo-daro | near | text strokes and layout alike |
| T10 | H-49 / M-401 | Harappa / Mohenjo-daro | near | text compared only (M-401 a bar) |
| T14 | L-35 / L-55 | Lothal / Lothal | same | same signs, sizes, spacing; L-55 has no animal |
| T21 | M-874 / M-1305 | Mohenjo-daro | near | text compared only (M-1305 a bar) |
| T27 | M-187 / M-193 | Mohenjo-daro | near | text alike; unicorn with face-like stand both |
| T28 | K-19 / M-224 | Kalibangan / Mohenjo-daro | near | pose, horn ornament, cup stand, five strokes match; tree top fuller on K-19 |
| T29 | K-19 / M-404 | Kalibangan / Mohenjo-daro | near | five strokes and spacing match; M-404 a bar |

### 3. Text-sharing against control (`cross_city_judged.csv`, `hands_pairs_key.csv`)

120 pairs, seed 2101 to 2103. Text pairs: two stones in different cities, both with photo and animal, sharing a run of 3 or more signs, the 29 earlier pairs left out, round-robin over city pairs (27 city pairs); 684 such pairs exist.

| kind | same | near | different | cannot tell | alike of judged | share |
|---|---|---|---|---|---|---|
| text-sharing (60) | 0 | 7 | 30 | 23 | 7 of 37 | 19% |
| control (60) | 0 | 4 | 28 | 28 | 4 of 32 | 12.5% |

Alike text pairs: H-13/Lh-1, H-268/M-50, H-17/K-5, H-3/K-13, B-1/M-725, K-2/M-776, C-10/H-444. Alike controls: H-388/L-9, H-450/Lh-1, L-22/M-69, K-22/M-875. Both-unicorn pairs only (the redesign): text 7 of 23 (30%), control 4 of 20 (20%), Fisher P 0.33. Stand letter of the catalogue agrees in 4 of 9 alike pairs and 5 of 19 different pairs with a letter on both (too few to tell).

### 4. Mohenjo-daro (`md_judged.csv`, `hands_md_key.csv`)

180 pairs of square animal seals, seed 2104 and 2105. Building = catalogue house (streets and trenches left out); area = first word of the catalogue area.

| kind | same | near | different | cannot tell | alike of judged |
|---|---|---|---|---|---|
| same building (60) | 1 | 7 | 27 | 25 | 8 of 35 (23%) |
| different building, same area (60) | 0 | 7 | 24 | 29 | 7 of 31 (23%) |
| different area (60) | 0 | 4 | 15 | 41 | 4 of 19 (21%) |

Both-unicorn pairs only: 8 of 22, 7 of 17, 4 of 10. The alike pairs per building: HRB 5XXIII 1 of 2, DKG(S) 12V 1 of 2, and every other building 0 or 1 of 1.

### 5. Making order of 40 seals (`order_judged.csv`)

| site | text cramped | animal cramped | even | cannot tell |
|---|---|---|---|---|
| Mohenjo-daro (18) | 4 | 5 | 8 | 1 |
| Harappa (8) | 3 | 0 | 5 | 0 |
| Lothal (6) | 2 | 1 | 3 | 0 |
| Kalibangan (4) | 2 | 1 | 1 | 0 |
| Chanhu-daro (4) | 2 | 0 | 2 | 0 |
| all 40 | 13 | 7 | 19 | 1 |

Text length (signs) by class: text cramped 6.0, even 5.6, animal cramped 3.6. Ruled guide lines 0, ghost signs 0. Text cramped against animal cramped, 13 to 7: binomial P 0.26 against an even split.

### 6. Recut and reused stones

I found no stone where an older text or an older animal shows under the present one clearly enough to list as certain. Candidates, all from the photos:

| stone | what shows |
|---|---|
| M-1233 (Mohenjo-daro) | thin crossing strokes and an X shape among the deep signs, lower left: a second, finer set of cuts, under or over the main text |
| Sktd-2 (Surkotada) | text cut deep in the top band; the animal field below is a scraped rough patch with one trial incised leaf-like mark |
| L-58, M-1195 (the "a" stones) | lower field unworked or roughened, no animal, no trace of a cut one |
| H-99 (Harappa) | a ship-like drawing scratched across the whole face, fine grid lines over it: a scratched drawing, not a stamped text; no under-text |

Photos of 40 finished seals show no ghost sign. Most of the 1,600 photos were not opened (only stones in the candidate list, the 300 pairs and the 40-seal draw were), so a recut among the unopened ones is not excluded.

## What went against

- Text-sharing pairs do not look alike more often than controls: 19% against 12.5% (P 0.26 to 0.35), inside the 10 to 18% I wrote down for controls and under the 25 to 35% I wrote down for text pairs. Redesign: restrict to both-unicorn pairs, 30% against 20% (P 0.33), no change in the picture. New idea, now the live lead: hand similarity is a style family that crosses cities (Lh-1 with H-450 and H-13, the collar-bands plus tall hatched-box stand family), and a text-only hand call (sign cut, ignoring animal and stand) is the next test, using the bar and animal-blank stones as the text-only witnesses (T10, T14, T21, T29 were the clean text-only calls).
- No building effect at Mohenjo-daro: 23% against 23% against 21%, where I wrote 25, 18 and 15. Redesign: both-unicorn pairs only, same flat result (8 of 22, 7 of 17, 4 of 10). New idea: the cannot-tell share is 40% to 70% and rises with distance (25, 29, 41 of 60), so the three groups were judged on different numbers of readable stones; a test on the readable stones only, with the hand call made on text signs, is the next test.
- Making order: I wrote 15 to 25 text-first and at most 5 animal-first, and got 7 text-first (animal cramped) and 13 animal-first (text cramped). Redesign: sort by text length, which removes most of it (long text cramped, short text large). New idea: the blank stones (6) with the text laid in the upper band and no animal show a text-first cut, so the layout was planned for both fields and the cut order was text first; this holds with the cramped-text count because both fields were set out before either was cut.
- Workshop debris: no excavation report with stone debris could be read; the workshop-against-house question is answered only on findspots (scattered).
- Guide lines and ghost signs: none seen on 40 finished seals, against my 4 and 3.
- The unfinished count is 6 of 60 (inside my 6 to 12); 20 of 60 are cannot-tell and 4 more are sketches, so the count of text-first stones is 6 to 10.
