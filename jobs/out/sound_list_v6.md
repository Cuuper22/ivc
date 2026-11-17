# Sound list, sixth version: the picture bilingual, the rivals split, 25 more signs

Scripts (in `work_scripts/`, run in this order): `sound_v6_sets.py` (copper-tablet sets), `sound_v6_sheet.py` (photo contact sheets for looking by eye), `sound_v6_common.py` (fifth-pass kit plus the picture table), `sound_v6_job1_scan.py` (which signs go with which picture), `sound_v6_job1_tests.py` and `sound_v6_job1b.py` (picture words, two rounds), `sound_v6_job2.py` and `sound_v6_job2b.py` (rivals, two rounds), `sound_v6_values.py` (the list and the counts; job-3 values come from `sound_v6_j3vals.py`), `sound_v6_job3_rank.py`, `sound_v6_job3.py`, `sound_v6_job3b.py` (job 3), `sound_v6_settable.py` (copper sets read), `sound_v6_master.py` (`work_data/values_master3.csv`), `sound_v6_readings.py` (READINGS 121-140). Tables: `work_data/sound_v6/`.

Plain words used below:
- **Picture side**: the face of an object that carries a drawing (animal, plant, figure, motif) instead of, or beside, the writing. Copper tablets have the text on one face and the picture on the other.
- **Set**: all copper tablets that carry the same text. A set is a batch of copies of one record.
- **Unit**: one distinct text with its picture (copies of the same text with the same picture count once). Used so that a set of 29 copies does not count 29 times.
- **Shuffle within site and object kind**: the picture labels are mixed at random among units (or objects) of the same site and the same object kind, thousands of times; **P** is the share of shuffles that look at least as strong as the real data. Small P points to a real tie between sign and picture; P near 1 points the other way.
- **Reads whole**: every sign on the face is a number, a base value, or a value we are building on. Counted on the 3,600 complete faces of the first catalogue (Lipi). **Strict** counts only values whose came-true fact had not been seen while the word was chosen; **wide** also counts values whose fact had been seen.
- **New texts**: the 1,183 second-catalogue (Mahadevan 1977) texts with no partner in the first catalogue.
- **Frames**: the pair (sign on the left, sign on the right) around a sign in a distinct text. Two signs that share frames more than signs of the same frequency are standing in for each other.
- **Merge trick**: where the second catalogue draws two first-catalogue signs as one, the variant takes the main sign's word, tested by frames.
- **yes** = right direction with P at or under 0.1; **direction only** = right direction, P above 0.1; **no** = wrong direction.
- **DEDR** = Burrow and Emeneau, Dravidian Etymological Dictionary (local copy), entry number. **Tamil Lexicon** = University of Madras Tamil Lexicon, read on dsal.uchicago.edu.

## 1. What was found

1. **Fully read faces: strict 1,970 of 3,600 (was 1,825), wide 2,160 (was 2,004).** Distinct texts strict 997 of 2,162 (was 909), wide 1,126 (was 1,029). Seals strict 738 of 1,540 (was 682), wide 820 (was 758). Goods objects strict 1,232 of 2,060 (was 1,143), wide 1,340 (was 1,246). New texts strict 215 of 627 complete lines (was 213), wide 254 (was 250): new-text seals 121 / 142 of 346, new-text goods 94 / 112 of 281. Of the 145 new strict faces, 62 come from 407 *kiḷai* "kindred" turning strict (rivals job) and 83 from the 25 new signs and their variants. The new texts barely move: the signs opened here are mostly first-catalogue variants.
2. **The copper tablets now read.** Complete copper-tablet faces reading whole: strict 135 of 196 (was 69), wide 142. Of the 27 copper sets with 2 or more copies, 18 read whole strict and 19 wide. Every big set reads: the stag set (29 copies), hare (14), horned archer (14), goat (8), elephant (7 + 4), tiger (6), knot, buffalo. Section 2 gives each set with its picture and its reading.
3. **A second picture pun: the crocodile tablets carry the sign read "chief", *mutal*, and crocodile is *mutalai*.** Prediction written before computing: tablets showing the gharial (the long-snouted river crocodile) carry 255. Result: 11 of 53 gharial tablets against 3.1 by shuffle within site (P 0.0002). DEDR 4952 *mutalai* "crocodile"; 255 *mutal* "chief, first" was chosen in an earlier pass from the drawing ("asymmetric animal"). The 11 are copies of one 11-sign Harappa text (`803-415-220-318-920-255-436-690-590-407-740`, H-278 to H-284 and more), so it is one record in copies, the same footing as the elephant (11 of 12 copper tablets, copies of two texts). This means the picture side names a word that is written in the text, a second time after the tusk. It opens the hunt for the picture word in every pictured record.
4. **Plant pictures go with produce, carried.** Harappa moulded tablets with a plant picture carry produce 806 *viḷai* in 5 distinct texts against 1.1 by shuffle (P 0.001) and the load-carrier 158/154 on 9 of 43 tablets against 2.8 (P 0.0002). The load tag "produce, carried" sits under a picture of the crop. This fact was seen in the scan before the word test, so it counts wide.
5. **The picture side can be written.** On copper-tablet copies the picture is sometimes replaced by one sign: the deer sign 341 replaces the stag on 2 of the 3 copies of `503-615-740`; sign 753 replaces the hare on 2 of 14; flowering-plant signs 777 / 780 / 781 / 782 replace the horned archer on 4 of 14; 777 replaces the goat on 4 of 8. A record's picture is a word the scribe could also write. The deer sign standing for the stag is the plainest case: the picture is read, not decorative.
6. **Copies of one copper text swap signs, and the swaps are word links.** Within one set the catalogue shows 421 / 422 (two goat sets), 422 / 423 / 424 (buffalo set), 904 / 905 (M-1529 against the other four), 407 / 408 and 231 / 220 (M-599 against the goat set), 705 / 706 (elephant). These pairs were drawn by scribes as the same word. Job 3 found 422 standing in the frames of 421 / 423 / 424 (P 0.008) independently; the four now read *par̤aṉam* "paddy field".
7. **Rivals split.** 711 is *vaḷḷam* "grain measure" (its tablets' other face holds a who-word 15 of 20 against 43%, P 0.004; *pāṉai* "pot" no). 060 is *-iṉ* "of" (new texts with 060 end in the house ending 11 of 20 against 37%, P 0.08; *uḷ* "in" no). 407 is *kiḷai* "kindred" (a fish crest on the face 65 of 127 against 20%, P 1e-14; 23 of 69 distinct texts against 25%, P 0.07; "cloth" missed twice more, four misses in all). 838 *viḷai* "produce" is ahead of *eḷ* "sesame". 692 *kūṭṭam* "assembly" is ahead of *nāṭu* "district" (district missed twice). 842 *tuṇai* "deputy" closes the text 5 of 5 times and stands with an office opening 4 of 5; 611 *kuṭai* "Umbrella" takes the quarter word before it; both rest on texts that were printed, so they count wide.
8. **Job 3: 11 of 25 signs came true; the merge trick came true 5 of 6 times** (927 as "two months", 642 as "many", 406 as "kindred", 323 as "ration", 772 as "child of"; 064 pointed the right way).

What it opens: (a) the picture as a second text: every pictured object becomes a bilingual where the picture word should be findable in the text or be its product; (b) the copper sets as a ledger of crop and field records (sheaves, fields, kalam, shares) under a house name and an animal, so the animal may be the account or the district, not the owner; (c) the copy swaps as a free source of sign equivalences.

## 2. The picture and text table (job 1)

### 2a. The photo check

Picture sides looked at by eye (`sound_v6_sheet.py` sheets): 51 copper-tablet picture sides, 12 Harappa tablet picture sides, 13 text sides for the tree signs.
- Copper tablets, 51: catalogue code names what the photo shows 16 (hare 2, horned figure 3, tiger 2, goat 2, rhinoceros 1, buffalo 1, knot 2, unicorn 1, composite 2); code is "Othr" or blank but an animal is plain 13 (branch-horned stag 5, marked goat 1, tiger 1, horned striped beast 2, rhinoceros-like 3, spotted long-necked beast 1); doubtful 1 (M-567 coded gaur, striped like its tiger set); too worn or dark 20; the picture side is a sign 1 (M-516, the deer sign). No code named a clearly wrong animal.
- Copies of one set carry one picture wherever the photo is readable. Because of this, each set's picture (read by eye) is given to all its copies (`CTAB_SET` in `sound_v6_common.py`); the catalogue codes inside sets were often mixed (the tiger set is coded gaur, tiger, Othr and blank).
- Harappa tablets, 12: gharial 2 (long reptile body), plant 2, fish 2 (fish; strokes), "Bult" 2 (a fish-shaped tablet with dotted circles; a lozenge with dotted circles), "several figures" 2 (unclear), scene 1, human figure 1.

### 2b. Which signs go with which picture

`sound_v6_job1_scan.py`: 1,942 units (1,563 seals, 266 moulded/incised tablets, 68 tags, 34 copper texts), 654 sign-picture cells with 2+ units. At P 0.01 or less: 28 cells (6.5 expected by chance); at P 0.002 or less: 9 (1.3 expected). The cells at P 0.01 or less:

| picture | sign | units with both | expected | ratio | P |
|---|---|---|---|---|---|
| scene with figures | 534 | 2 | 0.02 | 105 | 0.001 |
| rhinoceros | 942 | 2 | 0.05 | 41 | 0.001 |
| plant | 158 load-carrier *kā* | 5 | 0.92 | 5.4 | 0.001 |
| plant | 806 produce *viḷai* | 5 | 1.08 | 4.6 | 0.001 |
| dotted circles (code Bult) | 700 cup | 25 | 14.2 | 1.8 | 0.001 |
| stag (branch-horned beast) | 503 hill *malai* | 2 | 0.12 | 17 | 0.002 |
| plant | 463 Three-peaks | 4 | 0.63 | 6.3 | 0.002 |
| water buffalo | 690 allied *piṇai* | 5 | 1.0 | 5.0 | 0.002 |
| rhinoceros | 820 quarter *kāl* | 7 | 1.65 | 4.2 | 0.002 |
| water buffalo | 900 month | 5 | 1.18 | 4.2 | 0.003 |
| dotted circles (code Bult) | 413 grain *nel* | 4 | 0.96 | 4.2 | 0.003 |
| unicorn | 405 | 28 | 23.0 | 1.2 | 0.003 |
| unicorn | 747 | 2 | 0.16 | 12 | 0.004 |
| plant | 752 child of | 3 | 0.46 | 6.6 | 0.004 |
| gaur | 150 | 3 | 1.12 | 2.7 | 0.004 |
| several figures | 347 stag *kalai* | 2 | 0.17 | 12 | 0.005 |
| human figure | 060 | 3 | 0.35 | 8.5 | 0.005 |
| stag | 615 field *vayal* | 2 | 0.17 | 12 | 0.006 |
| gaur | 233 | 13 | 6.18 | 2.1 | 0.006 |
| water buffalo | 269 | 2 | 0.10 | 20 | 0.008 |
| dotted circles (code Bult) | 824 price | 4 | 0.94 | 4.3 | 0.008 |
| gharial | 503 hill | 3 | 0.43 | 7.0 | 0.009 |
| box sign as picture | 090 | 2 | 0.18 | 11 | 0.010 |
| box sign as picture | 240 | 2 | 0.22 | 9.3 | 0.010 |
| composite beast | 597 | 3 | 0.61 | 4.9 | 0.010 |
| water buffalo | 435 staff *kōl* | 4 | 0.84 | 4.8 | 0.010 |
| plant | 798 | 4 | 1.04 | 3.8 | 0.010 |
| elephant | 520 chief *vēḷ* | 10 | 4.37 | 2.3 | 0.010 |

What it means: the commodity pictures (plant, dotted circles on the incised Harappa tablets) carry commodity and account words (produce, carrier, grain, cup, price); the animal pictures carry name words. The elephant goes with the chief sign 520 on seals (10 against 4.4), which the pun test below took up.

### 2c. Picture words: predictions written before computing (`sound_v6_job1_tests.py`, redesigns in `sound_v6_job1b.py`)

| test | sign | word and pun | prediction | outcome | number | P |
|---|---|---|---|---|---|---|
| T1 | 520 | *vēḷ* "chief"; *vēḻam* "elephant" (Tamil Lexicon p. 3841 sense 8) | new-text elephant seals carry 520 | direction only | 1 of 8 against 19 of 328 (6%) | 0.39 |
| T2 | 923 | *maruppu* "tusk, ivory" (DEDR 4720) | elephant seals carry 923 | direction only | 1 of 49 against 1.0% | 0.41 |
| T3 | 255 | *mutal* "chief"; *mutalai* "crocodile" (DEDR 4952) | gharial tablets carry 255 | **yes** | 11 of 53 against 3.1 by shuffle (one text in 11 copies) | 0.0002 |
| T4 | set words | the copper set's words | seals with animal A carry a word of A's copper text | no | 145 against 159 by shuffle | 0.99 |
| T5 | 341 | *kalai* / *māṉ* "deer" (DEDR 4780) | deer signs stand with hill/field words | direction only | 1 of 28 against 3% | 0.59 |
| T6 | 806 | *viḷai* "produce" (DEDR 5437) | plant tablets carry the carrier 158/154 | yes (seen in the scan) | 9 of 43 against 2.8 | 0.0002 |
| T1b | 520 | as T1 | pictured tags with 520 show the elephant | direction only | 1 of 6 against 13% | 0.57 |
| T2b | 923 | as T2 | 923 on ivory/bone rods | no | 0 of 48 | 1 |
| T4b | set words | as T4, unicorn left out | special-beast seals carry their copper set's words | no | 17 of 229 against 24.7 | 0.99 |
| T5b | 341 | as T5 | deer signs on tablets | direction only | 12 of 28 against 36% | 0.27 |

Two words to note for the stag set: DEDR 4720 *maruppu* is also "branch of a tree", and its Kurux and Malto cognates are "antler" and "male deer"; the branch-horned beast on the 29 stag tablets is the antlered animal of that same word. The stag set's text does not contain 923, so this stays a note.

### 2d. The copper-tablet sets of Mohenjo-daro

Picture = set picture read from the photos. "Picture-side sign" = the copies where one sign stands on the picture face. Reading order; sounds from the sixth list; [n] = sign without a value.

| text | copies | picture | picture-side sign | sounds | English | reads whole |
|---|---|---|---|---|---|---|
| 503-615-752-740 | 29 | branch-horned beast with trough (stag) | | *malai vayal maka kuṭi* | Of the house of the heir of Hill-Field. | strict |
| 503-615-740 | 3 | stag | deer sign 341 on 2 | *malai vayal kuṭi* | Of the Hill-Field house. | strict |
| 235-705-033-845-407-321-407 | 14 | hare among plants | 753 on 2 | *vēymīn kalam mū cūṭu kiḷai paṭi kiḷai* | Bamboo-star: three kalam; sheaves of the kindred, the kindred's ration. | strict |
| 806-845-061-407-850-900-740 | 14 | horned figure with a bow | 777, 780, 781, 782 (one each) | *viḷai cūṭu kāl kiḷai kāṇi tiṅkaḷ kuṭi* | Produce: sheaves, a quarter; the kindred's share; of the Month house. | strict |
| 231-017-585-095-520-032-407 | 8 | goat with marked body and trough | 777 on 4 | *orumīn ēḻu kaṉṉi kōlaṉ vēḷ iru kiḷai* | First-star, the Seven Maidens; the staff-bearer chief; two kindreds. | strict |
| 706-033-923-740 | 7 | elephant | | *kalam mū maruppu kuṭi* | Three kalam of ivory: of the house. | strict |
| 706-033-923-740-001 | 4 | elephant | | *kalam mū maruppu kuṭi oru* | Three kalam of ivory: of the house; one. | strict |
| 798-240-845-061-407 | 6 | tiger | | *maru- mīmīn cūṭu kāl kiḷai* | Descendant of High-star: sheaves, a quarter, the kindred. | strict |
| 905-032-597-142-617 | 5 | spotted long-necked composite beast | | *[905] iru [597] kō ūḻiyaṉ* | [905 = 904 "two months" on copy M-1529] two, [597], the king's servant. | no (905, 597) |
| 017-585-388-740 | 4 | spotted long-necked composite beast | | *ēḻu kaṉṉi aracu kuṭi* | Of the royal house of the Seven Maidens. | strict |
| 003-421-176-100-740-790 | 3 | goat with marked body and trough | | *mū par̤aṉam iṟai mutu kuṭi maṇi* | Three fields: of the Tax-Elder house; gem. | wide (790 testing) |
| 003-422-176-100-740 | 2 | goat | | *mū par̤aṉam iṟai mutu kuṭi* | Three fields: of the Tax-Elder house. | strict |
| 235-233-222-740 | 3 | rhinoceros | | *vēymīn vāḷai aṭaimīn kuṭi* | Of the Bamboo-star Scabbard Shut-in-fish house. | no (222 testing) |
| 255-435-690-740-900-003-422 | 3 | water buffalo (copies 423, 424) | | *mutal kōl piṇai kuṭi tiṅkaḷ mū par̤aṉam* | Of the house allied to the Chief Staff; month: three fields. | strict |
| 415-220-845-407 | 3 | endless knot | | *kavar mīn cūṭu kiḷai* | Branch-Star: sheaves of the kindred. | strict |
| 806-235-233-705-033-585-407 | 3 | spotted composite beast | | *viḷai vēymīn vāḷai kalam mū kaṉṉi kiḷai* | Produce of the Bamboo-star Scabbard house: three kalam; the Maiden kindred. | strict |
| 233-585-407 | 3 | none: other face `706-005` | | *vāḷai kaṉṉi kiḷai* / *kalam ai* | Scabbard-fish, the Maiden kindred / five kalam. | strict |
| 806-233-384-740 | 3 | (catalogue Othr, unclear) | 749 on 2 | *viḷai vāḷai aracu kuṭi* | Produce: of the royal Scabbard house. | strict |
| 032-071-407 | 2 | gaur | | *iru [071] kiḷai* | Two [071], kindred. | no (071) |
| 744-760-095-595-001-142-617 | 2 | unicorn | | *[744] maka kōlaṉ paṭṭaṟai oru kō ūḻiyaṉ* | [744]'s child, staff-bearer, forge one, the king's servant. | no (744) |
| 798-231-705-033-904-100-740 | 2 | none: sign 957 | | *maru- orumīn kalam mū irutiṅkaḷ mutu kuṭi* | Descendant of First-star: three kalam, two months: of the Elder house. | strict |
| 231-255-435-690-740 | 2 | none: signs 479-749 | | *orumīn mutal kōl piṇai kuṭi* | First-star: of the house allied to the Chief Staff. | strict |
| 806-233-176-740 | 2 | (Othr, unclear) | | *viḷai vāḷai iṟai kuṭi* | Produce: of the Scabbard Tax house. | strict |
| 326-002-176-740-240-405 | 2 | none: other face `900-165` | | *[326] iru iṟai kuṭi mīmīn nūl* / *tiṅkaḷ poḻutu* | [326] two, of the Tax house, High-star thread / month, day. | no (326) |
| 003-700-900-165 | 2 | none: other face `032-220-176-740` | | *mū nāḻi tiṅkaḷ poḻutu* / *iru mīn iṟai kuṭi* | Three cups, month, day / of the Dark-star Tax house. | no (165 testing) |

How the sets read as a whole: a copper tablet is a crop or allowance record (sheaves, fields, kalam, shares, ration, month) for a named house, with one animal or motif per record. The animal does not follow the house: the same house words (Bamboo-star 235, First-star 231, Scabbard 233) sit under hare, goat, rhinoceros and composite beast, and the set words do not carry over to seals of the same animal (T4, T4b). The animal belongs to the record. Where its word is in the text it is the commodity (elephant: ivory) or a pun (crocodile: *mutal*); where it is not, it is the record's own mark, which a scribe could also write as a sign (deer 341 for the stag, 753 for the hare, the flowering plants for the archer and the goat).

## 3. The rivals (job 2)

All predictions for both words of each pair were written into `sound_v6_job2.py` before any number; one redesign for each miss in `sound_v6_job2b.py`, also written before running.

| sign | word | prediction | outcome | number | P |
|---|---|---|---|---|---|
| 692 | *kūṭṭam* "assembly" (DEDR 1882) | person/title words on the face | no | 17 of 89 against 25% | 0.93 |
| 692 | *nāṭu* "district" (DEDR 3638) | place/land words on the face | no | 3 of 89 against 11% | 1.0 |
| 692 | *kūṭṭam*, redesign | at Mohenjo-daro or Harappa | **yes** | 81 of 89 against 82% | 0.014 |
| 692 | *nāṭu*, redesign | crop words on the face | no | 5 of 89 against 10% | 0.95 |
| 711 | *vaḷḷam* "grain measure, 4 marakkāl" (DEDR 5315) | the other face of its tablets holds a who-word | **yes** | 15 of 20 against 43% | 0.004 |
| 711 | *pāṉai* "large pot" (DEDR 4124) | the other face holds a number or cup | no | 8 of 20 against 52% | 0.90 |
| 060 | *-iṉ* "of" | new texts with 060 end in the house ending | **yes** | 11 of 20 against 37% | 0.08 |
| 060 | *uḷ* "in" (DEDR 698) | an amount one or two places after 060 (new texts) | no | 6 of 49 against 12.9% | 0.62 |
| 838 | *viḷai* "produce" (DEDR 5437) | a carrier or number right after it | no | 1 of 21 against 17% | 0.98 |
| 838 | *eḷ* "sesame" (DEDR 839) | at Lothal, Chanhu-daro, Gujarat sites, abroad | direction only | 3 of 24 against 10% | 0.45 |
| 838 | *viḷai*, redesign | another crop word on the face | **yes** | 6 of 24 against 10% (distinct texts 4 of 19 against 11%, P 0.16) | 0.023 |
| 838 | *eḷ*, redesign | on pottery (oil jars) | no | 0 of 24 against 10% | 1.0 |
| 407 | *kiḷai* "kindred" (DEDR 2018) | Mohenjo-daro house-mates both carry it | direction only | 10 pairs against 9.6 | 0.46 |
| 407 | *tuṇi* "cloth" (DEDR 3307) | at coast sites or abroad | no | 7 of 127 against 10% | 0.98 |
| 407 | *kiḷai*, redesign | a fish crest on the face | **yes** | 65 of 127 against 20% (distinct texts 23 of 69 against 25%, P 0.07) | 1e-14 |
| 407 | *tuṇi*, redesign | a trade verb on the face | no | 1 of 127 against 3% | 0.98 |
| 842 | *tuṇai* "deputy" (DEDR 3308), texts seen | last sign of the text | yes | 5 of 5 against 29% | 0.002 |
| 842 | *tuṇai*, texts seen | month or assembly opener on the face | yes | 4 of 5 against 4% | 1e-5 |
| 611 | *kuṭai* "umbrella" (DEDR 1663), texts seen | the quarter word 820 right before it | yes | 2 of 6 against 1.5% | 0.003 |
| 611 | *kuṭai*, texts seen | jar, royal *aracu* or gate within two after it | yes | 3 of 8 against 11% | 0.046 |

Answers:
- **692**: *kūṭṭam* "assembly" is built on (seal size x1.45 in the fifth pass, great cities here). *nāṭu* "district" missed twice in this pass and stays alive as second word. The split that still has to come: a district word would be tied to one region; 692 avoids both land and crop words, which goes with an office title.
- **711**: *vaḷḷam* wins. Its tablets have a who-face and an amount face, as a grain measure on a ration chit should.
- **060**: *-iṉ* "of" wins this split; *uḷ* "in" stays as second word.
- **838**: *viḷai* "produce" is built on; *eḷ* "sesame" is second word.
- **407**: *kiḷai* "kindred, family" wins. The tree drawing is the pun: DEDR 2018 *kiḷai* "to branch, multiply (as families); kindred, herd, group". Cloth *tuṇi* has now missed four times.
- **842** *tuṇai* "deputy" closes office texts (`920-001-235-220-520-692-060-482 / ... 842`: "in the month, one, Bamboo-star Star chief, of the Assembly ... deputy"). **611** *kuṭai* is the Umbrella house: "the quarter of the Umbrella" (`820-611`) on the Dholavira signboard, at Lothal (`820-611-000`) and at Harappa. Both are built on, counted wide.
- **405 / 406 / 407 from the drawings.** The second catalogue draws all three as one sign (M169, a Y-fork with side branches). Photos looked at: H-134 and H-207 (405), H-50, L-28, M-170 (406), H-151, H-420, H-132, M-534 (407), with L-37, H-21 and H-158. In every legible one the sign is a Y-fork with one or two small side ticks; the photos do not show a shape that separates 405 from 406 from 407 (judged "same family" in all legible cases; which of the three each is could not be told from the drawing). So the split is the first catalogue's, not the scribes'. Job 3 gave 406 the word of 407 by frames (P 0.089); 408 (the goat-set copy variant) pointed the same way. 405 keeps *nūl* "thread" (wide) as the cotton-line reading; whether 405 is also *kiḷai* is the open question for the next pass.

## 4. Job 3: the next 25 signs

Ranking (`sound_v6_job3_rank.py`, `work_data/sound_v6/gains_v6.csv`): faces each sign alone keeps from reading under the list after jobs 1-2. Only picture (shape, second-catalogue drawing) and slot (first / middle / last, counted, before the jar) were printed. 999 (no shape: an unclassified sign) was skipped and 804 taken in its place. All 50 predictions were written into `sound_v6_job3.py` in one go before any was computed; one redesign for each double miss in `sound_v6_job3b.py`, all written before running.

| sign | word | A | B | C (redesign) | now |
|---|---|---|---|---|---|
| 321 | *paṭi* "rung, ration" (variant of 320) | frames of 320/323: too few | **yes**: on tablets 14 of 15 against 36% (P 6e-6; 14 are the hare set's copies) | | building; second word *muyal* "hare" |
| 592 | *kūṭu* "crate" | goods words 1 of 13 (no) | frames of 590 (no) | *paṭṭi* "fold, hamlet": place frames 2 against 1 (direction) | testing |
| 703 | *aḷavu* "measure" | number two away 3 of 16 against 11% (direction) | tablets 1 of 15 (no) | *nāḻi* "cup": cup frames 1 against 0 (direction) | testing |
| 773 | *maka* "child of" | frames of 752/760 (P 0.11, direction) | **yes**: crest on the face 7 of 14 against 21% (P 0.015) | | building |
| 772 | *maka* (one sign with 773) | **yes**: frames of 773 (P 0.078) | **yes**: frames of 752/760 (P 0.091) | | building |
| 927 | *irutiṅkaḷ* "two months" (merge with 904) | **yes**: frames of 904 (P 0.018) | **yes**: month/day words 3 of 11 against 7% (P 0.043) | | building |
| 554 | *paṟai* "grain measure" | frames of 540/530 (direction) | tall count near it 0 of 48 (no) | tablets 5 of 19 (no) | testing |
| 064 | *parutti* "cotton" (merge with 390) | frames of 390 (P 0.19, direction) | spindle/chest 0 of 14 (no) | *kavar* "fork": frames of 415 (direction) | testing |
| 422 | *par̤aṉam* "paddy field" (DEDR 4112) | **yes**: frames of 421/423/424 (P 0.008) | crop/land words 1 of 9 (no) | | building, with 421, 423, 424 |
| 136 | *āḷ* "man" | frames of 090 (no) | ration words 0 of 16 (no) | *aṭimai* "bondsman": frames of 097/717 (direction) | testing |
| 844 | *cūṭu* "sheaves" (variant of 845) | frames of 845 (no) | **yes**: crop word on the face 9 of 16 against 11% (P 2e-5) | | building |
| 603 | *kutir* "grain bin" | frames of 605 (no) | mound F 0 of 3 (no) | *katavu* "door": door frames (direction) | testing |
| 098 | *kōṉ* "lord" | person frames (direction) | seal size: too few | *ammai* "lady": frames of 140 (P 0.16, direction) | testing |
| 408 | *kiḷai* | frames of 407 (direction) | crest 1 of 10 (no) | short counts 6 to tall 2 (direction) | testing |
| 406 | *kiḷai* (merge with 407) | **yes**: frames of 407 (P 0.089) | crest 1 of 11 (no) | | building |
| 336 | *ūr* "town" (variant of 335) | **yes**: frames of 335 (P 0.056) | tablets 8 of 15 against 36% (direction) | | building |
| 621 | *katavu* "door" | gate/guard frames (no) | house-mates (direction) | *kōṭṭai* "store": frames of 575 (direction) | testing |
| 323 | *paṭi* (merge with 320) | **yes**: frames of 320 (P 0.072) | **yes**: month on the face 2 of 7 against 5% (P 0.039) | | building |
| 243 | *vēymīn* "Bamboo-star" | frames of 235 (no) | another crest (no) | *vāḷai* "scabbard-fish": frames of 233 (direction) | testing |
| 130 | *ur̤avaṉ* "ploughman" (DEDR 688) | mound F: too few | crop words 0 of 17 (no) | *aṭiyāṉ* "servant": frames (direction) | testing |
| 697 | *valai* "net" (DEDR 5288) | fish words 0 of 10 (no) | coast 0 of 10 (no) | *kaṭṭu* "bundle": tags 0 of 10 (no) | testing |
| 776 | *pū* "flower" (DEDR 4345) | frames of 777/782 (no) | crop words 1 of 11 (no) | Mohenjo-daro 1 of 11 (no) | testing |
| 642 | *pal* "many" (merge with 630) | **yes**: frames of 630/632/636 (P 0.018) | fewer numbers 3 of 8 against 45% (direction) | | building |
| 101 | *mutu* "elder" (variant of 100) | frames of 100 (direction) | **yes**: seals x2.32 bigger (n 5, P 0.011) | | building |
| 804 | *il* "house" | frames of 803 (no) | crest after 0 of 3 (no) | *kūṭu* "crate": frames of 226 (direction) | testing |

11 of 25 came true and are built on (plus 421, 423, 424 through the 422 frame test and the copy swaps). The merge trick (second catalogue draws the two as one): 5 of 6 came true. Picture-variant guesses without a second-catalogue merge did worse: 5 of 9.

## 5. The value list

Full table: `work_data/values_master3.csv` (sign, sound, English, DEDR, status, report, second word): 189 signs, 153 strict (47 of them base values: numbers, jar, man, fish, spear, comb, carriers, staff-bearer, tree, elder, cup, load comb), 8 wide, 26 testing, 2 paused (167, 350). Per-pass detail with the evidence of every test: `work_data/sound_v6/values_v6.csv`.

New or changed in this pass:

| sign | sound | English | status | second word |
|---|---|---|---|---|
| 060 | *-iṉ* | of (joiner after an opener) | strict | *uḷ* "in" |
| 407 | *kiḷai* | kindred, family | strict | *tuṇi* "cloth" (four misses) |
| 406 | *kiḷai* | kindred (variant of 407) | strict | |
| 408 | *kiḷai* | herd, lot (counted tree) | testing | |
| 692 | *kūṭṭam* | assembly | strict | *nāṭu* "district" |
| 711 | *vaḷḷam* | grain measure (4 marakkāl) | strict | |
| 838 | *viḷai* | produce | strict | *eḷ* "sesame" |
| 842 | *tuṇai* | deputy | wide | |
| 611 | *kuṭai* | umbrella: a ruling house | wide | |
| 341 | *kalai* | stag, deer | testing | |
| 321 | *paṭi* | rung, ration measure | strict | *muyal* "hare" |
| 323 | *paṭi* | ration measure | strict | |
| 421, 422, 423, 424 | *par̤aṉam* | paddy field | strict | |
| 772, 773 | *maka* | child of | strict | |
| 927 | *irutiṅkaḷ* | two months | strict | |
| 844 | *cūṭu* | bundle of sheaves | strict | |
| 336 | *ūr* | town | strict | |
| 642 | *pal* | many | strict | |
| 101 | *mutu* | elder | strict | |
| 592 | *paṭṭi* | fold, hamlet | testing | *kūṭu* "crate" |
| 703 | *nāḻi* | cup measure | testing | *aḷavu* "measure" |
| 554 | *paṟai* | grain measure | testing | |
| 064 | *kavar* | fork, branch | testing | *parutti* "cotton" |
| 136 | *aṭimai* | bondsman | testing | |
| 603 | *katavu* | door | testing | *kutir* "grain bin" |
| 098 | *ammai* | lady | testing | *kōṉ* "lord" |
| 621 | *kōṭṭai* | store, fort | testing | *katavu* "door" |
| 243 | *vāḷai* | scabbard-fish | testing | *vēymīn* |
| 130 | *aṭiyāṉ* | servant | testing | *ur̤avaṉ* "ploughman" |
| 697 | *kaṭṭu* | bundle | testing | *valai* "net" |
| 776 | *pū* | flower | testing | |
| 804 | *kūṭu* | crate | testing | *il* "house" |

Notes added to existing values: 255 *mutal* (crocodile tablets, T3), 806 *viḷai* (plant tablets), 520 *vēḷ* and 923 *maruppu* (elephant tests, direction only).

Totals with the sixth list (complete faces, first catalogue; new texts = complete second-catalogue lines with no partner):

| group | strict | wide | of |
|---|---|---|---|
| all complete faces | 1,970 (997 distinct texts) | 2,160 (1,126) | 3,600 (2,162) |
| seals | 738 | 820 | 1,540 |
| goods objects | 1,232 | 1,340 | 2,060 |
| copper tablets | 135 | 142 | 196 |
| new texts | 215 | 254 | 627 |
| new-text seals | 121 | 142 | 346 |
| new-text goods | 94 | 112 | 281 |

READINGS.md: readings 121-140 added (14 copper sets with their pictures, 4 first-catalogue texts opened by this pass, 2 new texts).

## 6. What went against, and the rescue tried

- **Elephant pun *vēḷ* / *vēḻam*:** new-text elephant seals carry 520 on 1 of 8 against 6% (P 0.39); rescue on tags 1 of 6 against 13% (P 0.57). Both pointed the right way on very few objects. The first-catalogue seal number (10 against 4.4) stands; the new texts have only 8 elephant seals. Next: elephant-seal texts in the photographs of other collections.
- **Ivory beyond the copper tablets:** 923 on elephant seals 1 of 49 (direction); on ivory/bone rods 0 of 48 (against). The tusk reading stands on the copper tablets where it was found; rods write other words (the comb 400, house names).
- **The copper set's words do not travel to seals of the same animal:** 145 against 159 by shuffle (P 0.99); without the unicorn 17 against 24.7 (P 0.99). Read: the animal belongs to the record, not to a house. This is now part of the reading in section 2d.
- **Deer signs with hill and field:** 1 of 28 (direction); on tablets 12 of 28 against 36% (direction). 341 stays testing; the photo substitution (deer sign for the stag picture) is its evidence.
- **692:** both words missed on the face-word tests (persons 17 of 89, land 3 of 89, crops 5 of 89). Rescue for *kūṭṭam* came true (great cities 81 of 89, P 0.014); *nāṭu* has two misses here.
- **838:** *viḷai* missed on carrier/number (1 of 21); rescue came true on crop words (6 of 24; 4 of 19 distinct texts, P 0.16). *eḷ*: coast 3 of 24 (direction), pots 0 of 24 (against).
- **407 as cloth:** coast 7 of 127, trade verbs 1 of 127 (both against). Paused as the main word; kept as second word.
- **060 as "in":** amount after it 6 of 49 against 12.9% (against).
- **Job 3:** 14 of 25 missed both A and B. Round two gave each a new word or test: 0 of 14 came true (11 direction only, 3 against: 554 on tablets, 697 on tags, 776 at Mohenjo-daro). They stay testing; 697 and 776 have had three tests each and need a third word next.
- **Copies:** several picture results rest on copies of one text (crocodile 11 copies of 1 text; elephant 11 copies of 2; 321 14 of 15 on the hare set). The unit scan, which counts each text once, keeps the plant, buffalo, rhinoceros and stag ties but not the crocodile tie (1 text). Growing the sample: more pictured tablets from the Harappa excavations of 1986 onwards, and the miniature-tablet picture codes in the second catalogue (codes 910, 441, 371, 930, 831 could not be matched to picture names from the partnered texts; a picture-by-picture link from the photos would open the new texts to the picture test).
