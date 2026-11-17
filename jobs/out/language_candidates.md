# The language behind the seals: candidates head to head, and the first sounds

Reading order = stored order reversed. Scripts (run from `/home/claude/ivc`): `work_scripts/lang_dedr_fetch.py` (pulls the whole Dravidian Etymological Dictionary, DEDR, Burrow and Emeneau 1984, from the DSAL site into `/tmp/dedr/`, 5,549 numbered entries), `lang_dedr_grep.py` (search it), `lang_score.py` (scoreboard), `lang_pun_chance.py` and `lang_pun_chance_skt.py` (how cheap a pun is, Tamil and Sanskrit), `lang_checks.py` (tests the sound values predict), `lang_numfish.py` (number + fish units), `lang_read15.py` (reads seals aloud). Sanskrit: Monier-Williams XML already on disk. Tags: **looked up** = taken from the named source; **guess** = mine; **measured** = a number out of our data.

## Verdict

**Early Dravidian.** It is the only candidate where the sign pictures sound like the jobs their slots do: 9 of 12 picture-and-job pairs work in Dravidian and in no other language at full strength (`lang_score.py`). In a slot-specific test against the whole Tamil side of DEDR, the 9 picture words have a look-alike carrying exactly the meaning the slot needs 7 times under a strict sound match, where chance gives 0.97 (P 1e-6); 9 times under a loose match against 3.08 (P 8e-6) (`lang_pun_chance.py`, measured). Two of the sound values then explained measured facts nobody built them for: the jar read as *kuṭi* "house, lineage" predicts that the sign before a jar is a family name and the sign before the other closers is not (17 same-house pairs against 10.3 by chance, P 0.028; other closers 1 against 5.4, measured); the man sign read as *āḷ* "to rule, to manage a household" predicts that `[name] jar man` seals are big, and they are the biggest seals in the corpus (median 778 mm2 against 645 for `[name] jar`, measured).

Grammar alone throws out Sumerian and Elamite as the home language (both put the possessed noun first) and leaves Dravidian, Munda, Indo-Aryan and Burushaski level. The puns split them.

## 1. Grammar fit

Measured facts from our files: (a) `[name] jar` closes 557 of 743 jar uses and `[name] jar man` 54 times: possessor, ending on the possessor, then the possessed. (b) Class or title sign after the name. (c) Count before the counted thing (1,418 "n X" owned counts; cup counted first 388 of about 470). (d) Two stroke systems: full-height for cups, boxes, jars; short for trees, fish, crop, women. (e) Names are built front-to-back as [house crest] [self] [tag], modifier first.

| fact | Dravidian | Munda | Indo-Aryan (Vedic) | Elamite | Sumerian | Burushaski |
|---|---|---|---|---|---|---|
| (a) possessor + ending, then possessed | yes. Genitive is the oblique stem used as a modifier before the head; SOV; adjectives before nouns (looked up: Britannica, Dravidian languages). Genitive sounds: Old Tamil *-in*, *-atu*, *-uṭaiya* (looked up: Wikipedia, Tamil grammar, gives -atu, -uṭaiya); oblique augments *-aṭṭ-/-att-* (e.g. maram, obl. *marattu-*, DEDR 4711, looked up) | yes. Santali "strictly head-last"; genitive *-rɛn* (animate), *-aˀk*, *-rɛaˀk* (inanimate) (looked up: Wikipedia, Santali) | yes. Genitive *-sya/-asya*; possessor-first compounds (*rāja-puruṣa* "king's man") (Pāṇini's stock example; guess from memory) | **no**. Modifier follows head; class suffix of the head copied on the possessor: *u sunki-k Hatamti-k* "I, king of Elam"; later *šak X-na* "son of X" (looked up: Wikipedia, Elamite) | **no**. Genitive phrase follows its head: *e2 lugal-a(k)* "the king's house" (looked up: Wikipedia, Sumerian) | yes. "The genitive is placed before the thing possessed: *Hunzue tham*"; genitive *-e*, *-mo* for f-class (looked up: Wikipedia, Burushaski) |
| (b) title after name | yes (head-last) | yes | either order | yes (apposition) | yes (apposition) | yes |
| (c) number before noun | yes | yes; Santali uses numeral classifiers (looked up) | yes | not found | **no**: *dumu eš5* "three children", though accounts write "3 dumu" (looked up) | yes |
| (d) two count systems split containers vs living things | no: Dravidian splits humans off (*-war* on numerals for humans, looked up Britannica); our short strokes count women together with fish and trees | no: Santali animacy puts trees with inanimates (looked up) | no numeral classes | not found | humans vs rest (looked up) | partial: x-class countables vs y-class mass, fruit trees in y (looked up) |
| (e) modifier-first names | yes | yes | yes | no | no | yes |

Facts that split: (a) and (c) remove Sumerian and Elamite as the language of the home seals. No language matches (d) as grammar; I read (d) as a script convention for measures against heads (guess), so it splits nothing. The other fact that splits is abroad: the round Gulf seals put the man sign first (twin-men 091 first on 4 of 6) and never after a jar (0 of 15). That is the head-first order of Sumerian, Akkadian and Elamite seal legends ("PN, servant of X", guess from memory of the Mesopotamian formula). The home language is head-last; the round seals spell a head-first formula. Two languages, two orders, on one sign set.

## 2. Pictures as words

Every Dravidian form below is looked up in DEDR (entry number given). Sanskrit forms are looked up in Monier-Williams on disk. Munda forms: Santali fish *hakô*, star *ipil*, tree *daru*, leaf *sakam*, man *herel*, two *bar*, three *pe* (looked up: Wiktionary Santali Swadesh list); no Munda pot, comb, spear or carrying-pole word was found online in the time I had. Sumerian: *dug* pot, *lu2* man, *ku6* fish, *gidru* staff/sceptre (from memory, not checked). Elamite and Burushaski: no lexicon reached for these objects.

| sign, slot job (measured) | picture word | the job word it sounds like | where it works |
|---|---|---|---|
| 740 jar; possessive ending, closes 557 of 743, before the house name slot | Ta. *kuṭam* waterpot (DEDR 1651); also Te. *aṭika*, Go. *aṭkā*, Kur. *aṛī* earthen pot (DEDR 75) | Ta. *kuṭi* house, family, lineage; *kuṭiy-āḷ* tenant (DEDR 1655). Second route: pot *aṭ-* ~ oblique/genitive *-aṭṭ-/-atu* | **Dravidian only.** Munda genitive *-rɛn/-aˀk*, Sanskrit *-sya*, Sumerian *-ak*, Burushaski *-e*: no pot word sounds like them |
| 090 man; after the jar 54 times | Ta. *āḷ* man, husband, servant, labourer (DEDR 399) | Ta. *āḷ* to rule, reign, "control or manage (as a household)"; *āṇṭār* owner, master (DEDR 5157) | **Dravidian** (sound and meaning). Sumerian *lu2* "man of" has the meaning but the wrong order; Sanskrit *puruṣa* "man; member of a race" meaning only |
| 220 fish; house crests open names (same fish in 15 of 23 house pairs) | Ta. *mīṉ* fish (DEDR 4885) | Ta. *mīṉ* star (inside DEDR 4876) | **Dravidian**. Sanskrit *matsya* fish, "personified as a prince" (MW): meaning only |
| 016+220 six + fish: a fixed unit (15 of 16 sixes before a fish are six + plain fish, never a crest fish; measured) | *aṟu-mīn* "six-star" = Pleiades (looked up: Parpola on harappa.com) | a star name, so a god or clan name | **Dravidian** |
| 017 seven; opens names (11) and is a whole name (7) | Ta. *ēr̤u* seven (DEDR 910) | Ta. *er̤u* to rise, ascend "as heavenly body" (DEDR 851); *er̤u-mīn* seven-star = Great Bear, and `017-220` is the whole text of H-9 (looked up: Parpola) | **Dravidian**; Sanskrit *saptarṣi* (seven sages) meaning only |
| 400 comb; after the jar 11 times; comb seals smallest (420 mm2); `[name] jar comb` median 240 mm2 (measured) | Ta. *cīppu*, Ma. *cīrppu* comb (DEDR 1610) | Ta. *ciṟu*, *cīṟ* before vowels: small, young (DEDR 1594) | **Dravidian**; Sanskrit *kaṅkata* comb ~ *kanīyas* younger, smaller (MW): near sound |
| 520 spear; a class sign | Ta. *vēl* spear; *vēlaṉ* spearman, Skanda (DEDR 5536) | Ta. *vēḷ* petty ruler, chief; *vēḷir* ancient chiefs; Kur. *bēlas* king (DEDR 5545) | **Dravidian only** |
| 142 person with staff; whole name on 15 seals | Ta. *kōl* stick, staff (DEDR 2237) | Ta. *kō, kōṉ* emperor, king, great man (DEDR 2177) | **Dravidian**; Sumerian *gidru* staff = sceptre, meaning only |
| 154/158 load-carrier; closes the granary-area load tags | Ta. *kā* pole with ropes to carry loads; *kāvaṭi* (DEDR 1417) | Ta. *kā* to guard, preserve; *kāval* guard, protection; *kāvalaṉ* protector, king (DEDR 1416) | **Dravidian**; Sanskrit *bhāra* load ~ *bhara* maintaining: weak |
| 390 tree; ends 29 names | Ta. *maram* tree (DEDR 4711) | Ta. *maṟam* valour, war; *maṟavōṉ* warrior (DEDR 4763) | Dravidian (r against ṟ: near sound) |
| 100 three-headed person; ends 42 of 42 names | Ta. *mūṉṟu*, *mu-* three (DEDR 5052) | Ta. *mutu* old; *mutiyavaṉ* elder, senior (DEDR 4954) | Dravidian (near sound) |
| 002 two / 091 twin men | Ta. *iru* two; *iraṭṭai* pair, twins (DEDR 474) | Ta. *iru* to be, abide, belong to (DEDR 480) | Dravidian (meaning of the job open) |

Wins (`lang_score.py`): Dravidian 10.5 of 12, Indo-Aryan 3.0, Sumerian 1.0, Munda 0, Elamite 0, Burushaski 0. Pairs that work in one language only at full strength: 9, all Dravidian.

**How cheap is a Tamil pun?** (`lang_pun_chance.py`, measured.) Any "job" meaning is cheap: 48% of Tamil headwords have a 3-letter look-alike meaning one of king, house, star, small, guard and so on. The slot-specific test is what counts: for each picture the look-alike must carry the meaning that slot needs. Strict match (3 letters, vowel length and dots merged): 7 of 9 against 0.97 expected, P 1.0e-6. Loose match (2 letters): 9 of 9 against 3.08, P 7.6e-6. I chose the slot meanings after seeing the words; the slot jobs themselves come from earlier data (jar = possessive, comb seals small, spear and carrier = classes), so this is tuning on meanings, not on slots.

**The same test in Sanskrit** (`lang_pun_chance_skt.py`, rival run on Monier-Williams, 190k headwords, every Sanskrit word for each picture tried, which favours Sanskrit): 3-letter match 6 of 9 against 5.03 expected for one word per picture (P 0.37); 4-letter match 6 of 9 against 2.85 (P 0.021, and lower still once the extra synonyms are paid for). Sanskrit misses the fish/star, seven/rise and tree/warrior pairs that Tamil gets from single words. Tamil, one word per picture, P 1e-6; Sanskrit, many words per picture, P 0.02 at best. The Sanskrit hits are raw look-alike counts I have not read one by one; the Tamil hits are each read above.

## 3. Numbers inside names

Measured (`lang_numfish.py`): numbers written right before a fish sign: 2 (278, mostly the opener's two strokes), 1 (34), 3 (34), 6 (16), 4 (9), 7 (1). Six goes with the plain fish only (15 of 16). This is a word, not a count: Dravidian *aṟu-mīn* "six-star", the Pleiades (looked up). The six + fish unit stands alone as a whole text (H-1086, H-1028), sits at the start (6) or middle (8). Seven + fish is the whole of H-9: *er̤u-mīn*, the Great Bear (Parpola, credited; he read both, here they sit in the name slot where a god or clan name belongs).

Numbers that stand inside names in Dravidian as homophones (DEDR): *ēr̤u* seven ~ *er̤u* rise; *iru* two ~ *iru* abide; *mū* three ~ *mutu* old; *āṟu* six ~ *āṟu* way, river (DEDR 405); *nāl* four, *ai* five. Santali *bar*, *pe*, *pon* and Sanskrit *dvi*, *tri*, *sapta* gave no homophone with a name-job meaning. Twelve (055) and the seven-favouring signs (585, 575, 503) found no Dravidian pun yet (guess: 055 "twelve" is a calendar word, Tamil *paṉṉiraṇṭu*; open).

## 4. Outside words

| word recorded abroad or in the oldest Veda | source | sounds like | matches a sign in its slot? |
|---|---|---|---|
| Meluhha | Parpola: Dravidian *mēl-akam* "high country" (looked up: Wikipedia, Meluhha). DEDR 5086 *mēl* above, high, west; DEDR 7 *akam* inside, house, place | Dravidian; Sanskrit *mleccha* "to speak indistinctly like a foreigner" (MW) is the loan of it. Witzel offers para-Munda *jar-tila* wild sesame (looked up) | no sign yet |
| Akkadian *ellu* sesame oil | Dravidian *eḷ, eḷḷu* sesame, *eṇṇey* sesame oil (DEDR 854; Southworth per Wikipedia, Meluhha) | Dravidian. Sanskrit *tila* does not | open: find a crop sign counted on tablets with an oil container |
| Meluhhan people in Sumer: Ur-Lamma "son of Meluhha", oil rations to "men of Meluhha", a "speckled Meluhha dog", "1 dar (bird) of Meluhha" | `research/data/meluhha/cuneiform_attestations_expanded.csv` (on disk) | names are Sumerian; no Indus-language name survives, only "(..)ibra, man of Meluhha" (looked up) | no |
| Rigveda words with *ka-/ki-* prefixes (*kīnāśa* ploughman, *karpāsa* cotton) | Witzel, Kuiper (looked up: Wikipedia, Substratum in Vedic Sanskrit) | Munda-like prefixing language | no sign tested |
| Rigveda *kulāya* nest, *kulpha* ankle, *daṇḍa* stick, *khala* threshing floor | Zvelebil's Dravidian etymologies (looked up, same page) | Dravidian | *daṇḍa* stick sits on the person-with-staff picture, but the slot word I propose is *kōl* |
| Witzel: Dravidian loans appear only from the middle Rigveda; 30 to 40 in all | same page | counts for a non-Dravidian language in the earliest Punjab | the strongest contrary fact; see check 1 |

Reading of it (guess): Meluhha and sesame point Dravidian; the Punjab of the earliest Rigveda points to a prefixing language. Both fit if the seals' language is Dravidian and a second, Munda-like language sat in the north-east Punjab. The round seals already show the script spelling a second language abroad.

## 5. First sound values (building on these)

| sign | picture | word | sound | slot evidence (measured) | pun |
|---|---|---|---|---|---|
| 740 | jar | *kuṭam* pot → *kuṭi* | **-kuṭi** "house of, of" | closes names; pre-jar sign shared in houses 17 vs 10.3, other closers 1 vs 5.4 | strong |
| 090 | man | *āḷ* | **āḷ** "man; one who manages (a house)" | follows jar 54 times; `jar man` seals biggest (778 mm2) | strong |
| 220 | plain fish | *mīṉ* | **mīn** "star" | commonest one-sign name (19 seals) | strong |
| 235, 240, 233, 231 | marked fish | *mīṉ* + a mark | **mīn-** + a crest word (unknown) | house crests, same fish in 15 of 23 house pairs | sound of the fish part strong; marks open |
| 016+220 | six + fish | *aṟu-mīn* | **aṟumīn** Pleiades | fixed unit, plain fish only (15 of 16) | strong |
| 017 | seven strokes | *ēr̤u* / *er̤u* | **er̤u** "seven; rising" | opens 11 names, whole name on 7 | good |
| 400 | comb | *cīrppu* → *ciṟu* | **ciṟ** "junior, small" | after jar 11; smallest seals (420; `jar comb` 240) | good |
| 520 | spear | *vēl* → *vēḷ* | **vēḷ** "chief" | class sign; citadel test mixed (below) | good |
| 142 | person with staff | *kōl* → *kō* | **kō** "king, great man" | whole name on 15 seals; size test against it (below) | good sound, weak data |
| 151/154/156/158 | load-carrier | *kā* pole → *kā* guard | **kā** "keeper, guard" | closes granary-area load tags | good |
| 390 | tree | *maram* → *maṟam* | **maṟam** "warrior" | ends 29 names | near |
| 100 | three-headed person | *mū* → *mutu* | **mū(tu)** "elder" | ends 42 of 42 names | near |
| 001-005, 012-018, 031-034 | strokes | Dravidian numerals | **oru, iru, mū, nāl, ai, aṟu, er̤u, eṭṭu** | counts | numbers |

## Fifteen seals read aloud (`lang_read15.py`, 49 complete seal texts read wholly with these values)

| object | site | signs | read | gloss | name-like in Dravidian? |
|---|---|---|---|---|---|
| M-185 | Mohenjo-daro | 220-520 | mīn vēḷ | Star-chief | yes: Old Tamil chief names end in *vēḷ* (guess from memory: *Iruṅkōvēḷ*) |
| M-1912 | Mohenjo-daro | 003-220-520 | mū mīn vēḷ | Three-star chief | yes, a star-group name + title |
| H-148 | Harappa | 235-240-520 | mīn₂₃₅ mīn₂₄₀ vēḷ | (crest A)(crest B) chief | yes: two house crests + title |
| K-32 | Kalibangan | 231-520 | mīn₂₃₁ vēḷ | (crest D) chief | yes |
| M-294 | Mohenjo-daro | 003-220-740 | mū mīn-kuṭi | of the Three-star house | yes: *X-kuṭi* is a house/clan name form (DEDR 1655 *kuṭi* lineage) |
| H-669 | Harappa | 032-220-740 | iru mīn-kuṭi | of the Two-star house | yes |
| M-1669 | Mohenjo-daro | 390-740 | maṟam-kuṭi | of the Warrior house | yes |
| C-17 | Chanhu-daro | 100-740 | mū(tu)-kuṭi | of the Elder house | yes |
| H-502 | Harappa | 032-220-740-090 | iru mīn-kuṭi āḷ | manager of the Two-star house | yes: *kuṭiy-āḷ* is an attested compound (DEDR 1655) |
| L-41 | Lothal | 817-002-233-740-090 | [opener] iru mīn₂₃₃-kuṭi āḷ | manager of house (crest C) | yes |
| Ns-5 | Nausharo | 820-002-016-220-740-090 | [opener] iru aṟu-mīn-kuṭi āḷ | manager of the Pleiades house | yes: the six-star is the Murukaṉ/Skanda group, and *vēlaṉ* (spear-bearer) is Skanda (DEDR 5536) |
| H-1056 | Harappa | 003-220-740-090-400 | mū mīn-kuṭi āḷ ciṟ | junior manager of the Three-star house | yes |
| M-1312 | Mohenjo-daro | 220-740-400 | mīn-kuṭi ciṟ | junior of the Star house | yes |
| H-514 | Harappa | 820-002-016-220-151 | [opener] iru aṟu-mīn kā | keeper (of the) Pleiades | yes, a temple-keeper title |
| M-1828 | Mohenjo-daro | 142-156 | kō kā | king's keeper / royal guard | yes |

What comes out is name-like in Dravidian on every one of the 15: star and star-group names, house names in *-kuṭi*, and titles *vēḷ*, *āḷ*, *ciṟ*, *kā*, *kō* in the head-last slots. The `2 + fish` reading (*iru mīn*) takes the opener's two strokes as part of the name; it may belong to the opener.

## Three checks

1. **Run the same slot-specific pun test on Munda and Burushaski dictionaries at equal depth.** This is the check that can sink Dravidian: my Dravidian search used all 5,549 DEDR entries, while Munda had a Swadesh list. Free routes: Bodding's *A Santal Dictionary* (scans on archive.org, `in.ernet.dli.2015.31960` is vol. 5); Berger's Burushaski dictionary. Sanskrit was run (above). Not yet run for Munda or Burushaski.
2. **The jar as *kuṭi* "house" (run).** Prediction: house-mates share the sign before a closing jar, not the sign before other closers. Result: jar 17 pairs against 10.3 by chance (P 0.028, 327 seals); spear/person/comb/carrier 1 against 5.4 (167 seals). It strengthens the proposal. It also settles the split left in the diary (parser's pre-closer 12 vs 12.6 against jar-only 15 vs 9.3): the house name sits before the jar only.
3. **Rank words should go with seal size and town zone (run; mixed).**
   - *āḷ* "manager": `[name] jar man` median 778 mm2, the biggest group; `[name] jar` 645; bare `[name] man` 593 (n 8). Strengthens.
   - *ciṟ* "junior": `[name] jar comb` median 240 mm2 (11 seals), the smallest. Strengthens.
   - *vēḷ* "chief": spear closers in citadels 12 of 82 against 11.9 by chance (P 0.53): no excess overall. By site: Dholavira castle 5 of 13 against 5 of 31, Kalibangan citadel 3 of 14 against 1 of 7; Mohenjo-daro 2 of 26 against 99 of 666; Harappa 2 of 29 against 18 of 148. It stands at Dholavira and Kalibangan. Rescue: *vēḷ* is a lineage title (the Vēḷir were a class of chiefs spread across the land), so spear seals should cluster by house rather than by zone. That is the next test.
   - *kō* "king": seals carrying 142 have a median of 572 mm2 against 618 for other seals (P 0.70); names ending in 142 are smaller (427). Against the rank reading. Rescue: 142 is a name word (*Kō-*, "great man", common in Old Tamil personal names, guess) rather than a rank, so size does not follow. Second rescue: the staff is *kōl* "rod, measuring rod" and the person-with-staff is an office of measuring. Both untested.

## Things to carry forward

- `measured` House-mates share the sign before a closing jar (17 vs 10.3, P 0.028), not before any other closer (1 vs 5.4).
- `measured` `[name] jar man` seals are the biggest (median 778 mm2), `[name] jar comb` the smallest (240).
- `measured` Six + fish is a fixed unit with the plain fish only (15 of 16).
- `measured` 9 picture words have a Tamil look-alike carrying the meaning their slot needs: 7 of 9 strict (chance 0.97), 9 of 9 loose (chance 3.08).
- `guess` The language of the home seals is early Dravidian; jar = *-kuṭi* "house of", man = *āḷ* "manager", fish = *mīn* "star", comb = *ciṟ* "junior", spear = *vēḷ* "chief", carrier = *kā* "keeper", staff-person = *kō* "king".
- `guess` The round seals abroad spell a head-first language (Sumerian, Akkadian or Elamite seal formula) with Indus signs.
