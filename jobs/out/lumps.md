# Lumps with two or more seal impressions: does the short stamp go with the name stamp beside it?

Word-free job, 2026-11-17: sign numbers and job classes only. Scripts `work_scripts/lump_common.py`, `lump_1_build.py`, `lump_2_pairs.py`, `lump_3_cups.py` (predictions in each top docstring, written before the numbers). Logs and tables in `work_data/lumps/` (`impressions.csv`, `log_2_base.txt`, `log_2_nodup.txt`, `log_2_lenient.txt`, `log_2_both.txt`, `log_3.txt`). Each script runs in about 70 seconds. Counting follows FRAME.md "How pairs are counted".

## Findings in plain words

1. **A short stamp does not copy the crest of the name stamp on its lump.** On the 10 lumps where both can be compared, 1 short stamp carries the name's crest-class sign (the fish-type signs of frame v2); chance gives 0.67; P 0.67. Using FRAME's own crest (first non-number sign of the name) it is 0 against 0.75 by chance (P 1.0). Widened to every readable sign of the name it is 1 against 1.24 (P 0.87). With the widest rules (28 lumps, overlap not removed, damaged names allowed) it is still 1 against 1.2. Points: no tie between short stamp and crest.
2. **Against the idea, at class level:** short stamps whose tail is a fish-type crest sign: 2 of 12 against 3.5 by chance (P_ge 0.91). The two that exist are the 235 and 236 tails of `861-002-235` / `861-002-236`, set beside a name whose crest is 220 (L-191, Mah7249): the same family of sign, a different sign. Points: fish-type tails are not favoured; the short stamp and the name carry unrelated fish.
3. **Heading of the name stamp:** only 4 lumps have a name stamp with a heading field and a readable short stamp. 1 shares a sign (the Dholavira lump: `820-002-...-520` name with `820-002-...` short, same front word on both); chance 1.00; P 1.0. Too few lumps to say anything either way.
4. **Recurrence: the pairing is free.** The one name stamp that recurs (agent stamp `705-500-741-001-055-220-740-090`, Lothal, 3 lumps) takes a different short stamp every time (`317-920-002` + `880`; `861-002-235`; `070-125`): 3 of 3 different, chance gives the same 3 (P 1.0). With the overlap with the second catalogue left in, the same name appears on 6 lumps, each with a different set of short stamps. Short stamps: with overlap kept, `861-002-236` is on 3 lumps with 3 different names and `880-002` on 3 lumps with 3 different names. So one short stamp goes with different names, and one name with different short stamps. Nothing is tied.
5. **Order and mixing: nothing regular, and the catalogues disagree.** Name-first in listing order: Lipi lumps 4 of 5, second-catalogue lumps 0 of 7 (the 7 include Harappa heading + name tablets). Pooled 4 of 12 against 6 (P_le 0.19). The listing order is the catalogue's, not known to be the order of stamping. Role mixing: lumps with both a name stamp and a short stamp 14 of 84 against 18.6 by chance (P_le 0.08): if anything fewer than chance, the opposite of pairing. With the widest rules 32 of 97 against 39.3 (P_le 0.04). Points: name stamps and short stamps are not drawn to each other on lumps.
6. **Cup-count objects (a different stratum, kept apart): the pairing is free too, with a clear count profile.** The second catalogue files 119 of its 146 multi-impression Harappa "sealings" with a cup face (cup 700 with 2, 3 or 4 long strokes). The same kind of object in the first catalogue is the two-face clay tablet: 177 objects with a readable name face and a cup-count face. Counts: 2 strokes 54, 3 strokes 73, 4 strokes 49, 1 stroke 1. The most-used cup-count stamp (3 strokes) goes with 60 different names. Names on 2+ tablets: 35, of which 23 take different counts; chance 25.8 (P_le 0.18). The count does not follow the name's ending (comb 400 against none: chi-square 1.15 against 2.94, P 0.91), crest class (2.03 against 3.13, P 0.68) or man ending (P 0.87); the front word on the name gives 21.8 against 22.1 (P 0.15). The count does not follow the trench: 248 same-trench pairs share a count against 249.0 by chance (P 0.49). Points: the cup count goes with the name the way a random draw would.

What went against the idea: every test of "the short stamp is tied to the name beside it" (crest, heading, recurrence, ending, count) came out at chance or below it. What stands: lumps are made of independent stamps, a short stamp is pressed beside whatever name is to hand. Redesign tried once, as AGENTS.md asks (see "Redesign" below): the same null on three wider rule sets.

## What could not be done, and what is missing

- Only 14 lumps of stratum A hold both a name stamp and a short stamp that can be compared (up to 32 with the widest rules). Cause: the first catalogue has 33 lumps with 2+ impressions, the second 207, and most impressions are damaged (the closer or the first signs are lost). There is no restored-text column for the second catalogue; the first catalogue's restored column (`corpus_jobs.csv`, restored_signs) was not used because it fills lost signs with a predicted sign and would put the guess into the match count.
- Position of impressions on the lump (which is on top, where the knot lies) is not in either catalogue; only the order of listing is, and the two catalogues list in opposite order. Finer findspot than trench or locus is not recorded for lumps; the pair-in-same-spot counts use trench (first catalogue) or locus (second catalogue) only. The photo-pair files in `jobs/` are house-mate seal pairs, not lumps, and carry nothing on impressions.
- The overlap between the two catalogues was found by text near-fit (no shared catalogue number exists): 14 second-catalogue lumps are treated as the same lump as a first-catalogue lump and dropped; the doubtful ones are dropped on purpose, so no lump counts twice. `log_2_nodup.txt` keeps them.

## How the data was built

| step | count |
|---|---|
| first-catalogue lumps with 2+ impression rows (clay sealings, TAG types) | 33 |
| second-catalogue sealings with 2+ text surfaces | 207 |
| lumps after removing second-catalogue duplicates of first-catalogue lumps | 226 |
| after counting identical batches (same site, locus, set of texts) once | 213 |
| with 2+ different impression texts (a stone pressed twice is one stamp) | 199 |
| stratum A, lumps proper (no cup-count impression) | 84 (30 first catalogue, 54 second) |
| stratum B, name + cup-count objects | 115 |

Roles, fixed before counting: name stamp = a closer sign (740, 520, 151, 154, 155, 158 or after-jar title) in its ending and 3+ signs; short stamp = no closer and (front word at the start, front word + slot sign one sign in, count line, or 3 signs or fewer); crest = frame v2 CREST class (140 220 222 226 231 233 235 240 243 803 806) or the first non-number sign of the name body; heading = signs up to and including the first slot sign when that sits in the first three places; tail of a short stamp = its signs minus front words, slot signs and numbers. Stratum A: 51 lumps have a name stamp, 40 a short stamp, 14 both.

The 14 comparable lumps: H-1722, L-190, L-191, L-193, L-198, the Rupar lump (its second-catalogue twin Mah9022 dropped), the Dholavira lump, Mah1616, Mah2810, Mah2835, Mah4658, Mah5296, Mah5320, Mah5324.

## Tables (stratum A, base rule set; chance = short-stamp sets dealt among eligible lumps of the same site, 20,000 deals; P_ge = share of deals at least as large as real)

| test | eligible lumps | real | chance | P_ge | what it means |
|---|---|---|---|---|---|
| 1a short tail sign = crest-class sign of the name | 10 | 1 | 0.67 | 0.668 | at chance |
| 1b short tail sign = first non-number sign of name | 11 | 0 | 0.75 | 1.000 (P_le 0.25) | at chance, none |
| 1c short tail sign = any sign of the name body | 12 | 1 | 1.24 | 0.872 | at chance |
| 1d short tail is a crest-class sign of any kind | 12 stamps | 2 | 3.51 | 0.912 | fewer than chance |
| 2a short stamp shares a sign with name heading | 4 | 1 | 1.00 | 1.000 | at chance |
| 2b same front word on both | 1 | 1 | 1.00 | 1.000 | one case, nothing to test |
| 3 names on 2+ lumps with 2+ different shorts | 1 name | 1 | 1.00 | 1.000 | free pairing |
| 3 distinct (name, short) pairs | 14 lumps | 16 | 16.00 | 1.000 | every pair different |
| 4a name listed first (lumps with one of each) | 12 | 4 | 6.0 | 0.928 (P_le 0.19) | no order |
| 4b lumps with both name and short stamp | 84 | 14 | 18.62 | 0.960 (P_le 0.081) | fewer than chance |
| 4b lumps with 2+ name stamps | 84 | 10 | 12.53 | 0.930 | at chance |
| 4b lumps with 2+ short stamps | 84 | 8 | 6.91 | 0.364 | at chance |
| 4c second-catalogue name stamps with a picture field | 34 | 14 | 15.36 | 0.827 | at chance |
| 4c second-catalogue short stamps with a picture field | 31 | 16 | 14.63 | 0.327 | at chance |
| 4d lump pairs with the same short stamp in the same spot | 3 pairs | 1 | 0.39 | 0.345 | at chance |
| 4d lump pairs with the same name stamp in the same spot | 4 pairs | 1 | 0.79 | 0.600 | at chance |
| 4e name ending class against short front word (chi-square) | 14 | 9.85 | 9.98 | 0.774 | at chance |

## Redesign (the null tried again in a different shape)

Same tests on wider rule sets (`LUMP_VARIANT` in `lump_common.py`):

| rule set | lumps A | eligible 1a | 1a real / chance | 1b real / chance | 1c real / chance | 4b both-role lumps real / chance (P_le) |
|---|---|---|---|---|---|---|
| base | 84 | 10 | 1 / 0.67 | 0 / 0.75 | 1 / 1.24 | 14 / 18.6 (0.081) |
| overlap kept (nodup) | 97 | 15 | 1 / 0.67 | 0 / 0.75 | 1 / 1.25 | 20 / 25.4 (0.075) |
| damaged 3+ sign texts may be names (lenient) | 84 | 15 | 1 / 0.50 | 0 / 0.50 | 1 / 1.09 | 26 / 31.3 (0.080) |
| both | 97 | 20 | 1 / 0.50 | 0 / 0.60 | 1 / 1.22 | 32 / 39.3 (0.040) |

Widening from 10 to 20 comparable lumps changes nothing: the one match is H-1722 (`000-415-220-520` with `220-000`, fish 220), a name stamp and a stamp that is only the fish sign. Also tried at class level (item 1d) rather than identity: fewer than chance. The idea gets a fair test only with more lumps; the repeat-stamp design of item 4 (one agent stamp with three short stamps at Lothal) says the short stamps are chosen per transaction, not per name.

## Items for the map

- `measured` Short stamps and name stamps on one lump are paired freely: crest 1 against 0.67, heading 1 against 1.00, same short with different names and same name with different short stamps (agent stamp `705-500-741-001-055-220-740-090`: 3 lumps, 3 different short stamps).
- `measured` Cup-count tablets: counts 2 / 3 / 4 strokes = 54 / 73 / 49 on 177 objects, independent of the name's ending, crest, front word and trench (P 0.91, 0.68, 0.15, 0.49).
- `guess` A short stamp on a lump is the transaction's own stamp (which office or share), pressed beside whichever sender's stamp is present; this fits free pairing and fits the agent stamp reused with four different short stamps.
