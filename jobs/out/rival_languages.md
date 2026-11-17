# Rival languages given the same pun test at full strength

Result: Dravidian is ahead of every rival, and the gap shows exactly where the dictionary-size correction bites. On whole-word and 4-letter look-alikes Dravidian gets 6 and 7 of 9 pictures against chance 0.46 and 1.02 (P 4e-7 and 6e-7). Munda gets 0 of 9 on both, against chance 0.22 and 1.00. Sumerian gets 1 of 8, Indo-Aryan 0 of 7 (Turner) and 4 of 9 against 4.5 (Monier-Williams, whose chance is saturated). Burushaski and Elamite have too few usable words to be tested at full strength; they score 0 with chance near 0, which says nothing either way.

Tags: **looked up** = taken from a named source; **measured** = a number out of the scripts below; **guess** = mine.

Files: `work_scripts/rival_lexicons.py` (dictionaries into tables), `rival_pun_test.py` (the test), `rival_report.py` (tables and per-sign detail), `rival_read15.py` (the 15 seals), `rival_ocr_werchikwar.py` (re-OCR of Lorimer). Dictionaries and their origins: `work_data/lexicons/SOURCES.md`. Raw results: `work_data/lexicons/pun_results_core.json`, `pun_results_allsyn.json`.

## 1. What was downloaded (looked up)

Santali: Campbell 1899 (12,543 entries parsed), Bodding vol 5 (only the R-to-end volume is open; 2,065), Wiktionary Santali (1,016). Mundari: Bhadra 1931 (5,189). Munda pooled: 20,795. Burushaski: Lorimer's Werchikwar-English Vocabulary 1962 (Yasin; the Archive's OCR was garbage, I re-OCRed the scan and the parser kept 1,397 entries), the Barken Hunza dictionary (429, only ba- to be-), Starling Swadesh lists (to confirm plain words). Sumerian: Halloran Sumerian Lexicon v3 (4,519), Wiktionary (1,598). Elamite: Hinz-Koch 1987 (2,550, German glosses, names left out). Indo-Aryan: Turner CDIAL (7,295 Old Indo-Aryan headwords) and Monier-Williams (277,409 sense lines). Dravidian: DEDR Tamil side (3,015). Hoffmann's Encyclopaedia Mundarica (7 volumes) is saved but its OCR cannot be cut into entries. ePSD2 and Berger's Burushaski dictionaries were not reachable or not open. Berger's Yasin Swadesh words (Starling): fish *ɕumu* (a Shina loan), man *hir*, tree *drakht* (Urdu loan) with native *hun* "wood".

## 2. The test, identical for every language (`rival_pun_test.py`)

Same nine pictures (jar, man, fish, seven, comb, spear, staff-person, load-carrier, tree), same nine slot meanings as `lang_pun_chance.py` (house/family; rule/manage/master; star; rise/ascend; small/young/junior; chief/king/ruler/lord; king/chief/lord/emperor; guard/protect/keep; warrior/valour/bravery), same sound-alike rule (headwords share the first L letters with diacritics removed; a different entry must carry the slot meaning). Changes made so the contest is fair:
- Picture words are found by rule in each dictionary (an entry whose first gloss terms say "pot/jar", "man", "fish", "seven", "comb", "spear", "staff/stick/rod", "carrying pole", "tree"), never by hand. Every synonym found is paid for: chance for a slot = 1 - (1-p)^k with k picture words.
- Chance p is measured inside the same dictionary, among entries with the same key length, so a bigger dictionary raises its own chance and wins nothing. Also run with every dictionary cut to 3,000 entries.
- Three strictness levels: 3 letters (original), 4 letters, whole word (homophone). 3 letters saturates in big dictionaries, so 4 letters and whole word carry the weight.
- German glosses (Elamite) use German slot words.
- Odds = chance of getting at least that many slot-right hits by luck (Poisson-binomial over the slots). Low odds = the pictures sound like their jobs.

### 2a. Side by side (picture words = the plain noun; narrow slot meanings) (measured)

Hits / slots that have a picture word, chance expectation, odds.

| language (dictionary) | entries | 3 letters | 4 letters | whole word |
|---|---|---|---|---|
| **Dravidian (DEDR Tamil)** | 3,010 | 7/9, 2.67, 6e-4 | 7/9, 1.02, 6e-7 | 6/9, 0.46, 4e-7 |
| Dravidian with the 2 hand-added rows left out | 3,008 | 5/9, 2.54, 4e-2 | 5/9, 0.93, 2e-4 | 4/9, 0.38, 2e-4 |
| Santali, Campbell | 12,542 | 3/9, 1.57, 0.2 | 0/9, 0.23, 1 | 0/9, 0.03, 1 |
| Santali, Bodding vol 5 | 2,065 | 0/6, 0.50, 1 | 0/6, 0.11, 1 | 0/6, 0.02, 1 |
| Santali, Wiktionary | 999 | 0/8, 0.01, 1 | 0/8, 0.00, 1 | 0/8, 0.00, 1 |
| Mundari, Bhadra | 5,189 | 2/8, 1.04, 0.3 | 0/8, 0.24, 1 | 0/8, 0.03, 1 |
| **Munda pooled** | 20,795 | 5/9, 3.92, 0.3 | 0/9, 1.00, 1 | 0/9, 0.22, 1 |
| Burushaski, Lorimer Yasin | 1,397 | 0/6, 0.08, 1 | 0/6, 0.02, 1 | 0/6, 0.01, 1 |
| Burushaski pooled with Barken | 1,826 | 0/6, 0.23, 1 | 0/6, 0.03, 1 | 0/6, 0.01, 1 |
| Sumerian, Halloran | 4,519 | 2/8, 2.80, 0.9 | 1/8, 1.06, 0.7 | 1/8, 0.62, 0.5 |
| Sumerian pooled with Wiktionary | 6,026 | 2/9, 3.78, 1 | 1/9, 1.61, 0.8 | 1/9, 1.09, 0.7 |
| Elamite, Hinz-Koch | 2,550 | 0/4, 0.18, 1 | 0/4, 0.06, 1 | 0/4, 0.00, 1 |
| Indo-Aryan, Turner | 7,295 | 3/7, 2.54, 0.5 | 1/7, 0.97, 0.7 | 0/7, 0.03, 1 |
| Sanskrit, Monier-Williams | 277,409 | 8/9, 8.25, 1 | 8/9, 8.09, 1 | 4/9, 4.54, 0.8 |
| Indo-Aryan pooled | 284,704 | 8/9, 8.25, 1 | 8/9, 8.09, 1 | 4/9, 4.72, 0.9 |

Counting every synonym as a candidate (`pun_results_allsyn.json`): Dravidian 8/9 (chance 3.49, 2e-4) at 3 letters, 8/9 (1.48, 6e-8) at 4 letters, 6/9 (0.58, 1e-6) whole word. Best rival: Campbell 5/9 (3.10, 0.1) at 3 letters and 2/9 (0.70, 0.1) at 4 letters; Munda pooled 2/9 (1.77, 0.6) at 4 letters, 0/9 whole word; Halloran Sumerian 2/9 whole word against 0.89 (0.2). Wider slot meanings (broad list) leave the order the same: Dravidian 4 letters 6/9 against 1.53 (2e-4), Munda pooled 2/9 against 1.71 (0.6).

Cut to 3,000 entries each, mean over 30 draws (hits/chance, whole word): Dravidian 5.9/0.46; Campbell 0/0.01; Bhadra 0/0.02; Munda pooled 0/0.04; Halloran 0.8/0.45; Turner 0/0.01; Monier-Williams 0.3/0.26. Cutting a big dictionary also deletes its real partner words, so the in-dictionary chance above is the number I stand on; the cut run agrees.

### 2b. Dravidian rerun with the same adjustment

The adjusted Dravidian figure is the first row of the table: 7 of 9 at chance 2.67 (3 letters) and 7 of 9 at chance 1.02 (4 letters). The original 7-of-9 against 0.97 had one hand-picked word per picture; with every Tamil word for each picture paid for, the 3-letter odds fall from 1e-6 to 6e-4 and the 4-letter odds stay at 6e-7. Two things to know: (1) `lang_pun_chance.py` hand-adds two rows the parser misses (*āḷ* "man, servant" and *maram* "tree"); without them Dravidian is 5 of 9, odds 2e-4 at 4 letters and whole word, still far ahead. (2) The 3-letter test is weak for all languages; 4 letters and whole word are the ones that separate them.

## 3. The best puns, sign by sign, against the Dravidian one

Dravidian pairs (picture word ~ look-alike with the slot meaning), all read from the DEDR gloss (looked up):

| sign | Dravidian | best rival and how it compares |
|---|---|---|
| jar 740 "house of" | *kuṭam* waterpot ~ *kuṭi* house, family, lineage (3 letters, strong; same root) | Sanskrit *kuṭa* "a house, family" is itself also a jar word (MW), a homophone of the same kind, but see the note below. Munda: *chàtu* ~ *chàndà* "family dues" only; no pot word sounds like "house". Equal on this sign if Sanskrit *kuṭa*/*kuṭi* are not Dravidian loans (guess: they are listed among suspected Dravidian loans in Vedic, my recollection, not checked in this run). |
| man 090 "manager" | *āḷ* man ~ *āḷ* to rule, whole word | Sanskrit *īśa* "master" / *īśvara* "lord" are also words glossed "man" in MW, whole word, but MW gives 127 man-words so chance on this slot is 0.81. Tamil chance on this slot 0.14. Dravidian clearly better. Munda: none (11 man-words, no hit). |
| fish 220 "star" | *mīṉ* fish ~ *miṉ* shine, star (whole word) | Sanskrit *mīna* fish; MW *mahāmatsya* ~ *mahendra* "a star" is a different word; no same-word pun. Munda *hako*, Sumerian *ha*: none. Dravidian only. |
| seven 017 "rise" | *ēr̤u* ~ *ēṟu* rise, ascend (the heavenly bodies) | Sanskrit: *sapta* has no look-alike with "rise". Munda *eae*, *sat*: none. Dravidian only. |
| comb 400 "junior" | no hit under the plain rule (*cīppu* comb ~ *ciṟu* small is a one-letter-class near sound, found by hand earlier) | Sanskrit *kaṅkata* ~ *kana* "young", *kanittha* "small" (3 letters) is a good near sound and beats Tamil on this sign. Munda *chata* ~ *chabha* "small pot" is noise. |
| spear 520 "chief" | *vēl* spear ~ *vēḷ* petty ruler, chief | Sanskrit *śalya*, *śala* ~ *śāla/śalya* "king of Madra" are names; Munda *barchha* spear ~ *barki* "chief wife" is a poor match. Dravidian better. |
| staff 142 "king" | no hit (*kōl* ~ *kō* are 2 letters apart in key) | Munda *latkao* ~ *lat* "lord", but *lat* is the English word "lord" (the dictionary says so); Sumerian *subar* ~ *sublugal* "subordinate of the king". Both beat Tamil on this sign at 3 letters, neither is a native pun. |
| carrier 154 "keep" | *kā* pole ~ *kā* guard (whole word, same spelling) | Santali *arar* ~ *aras* "a pole placed on top of a cart to keep loads down": a real 3-letter sound-alike with "keep", comparable. Sanskrit saturated. Sumerian *sagks* is OCR noise. Roughly equal on this sign. |
| tree 390 "warrior" | *maram* ~ *maṟam* valour, war (whole word except r/ṟ) | Munda *daru*, *sal*, *babur*: none. Sanskrit *vṛkṣa*: none. Dravidian only. |

Burushaski and Elamite: no picture word in the Lorimer or Hinz-Koch lists has a sound-alike with a slot meaning; the lists hold 1,397 and 2,550 entries and find a picture word for only 6 and 4 of the 9 pictures.

## 4. Grammar side

| | possessive marker | title after name | number before noun |
|---|---|---|---|
| Dravidian | suffix on the possessor, which stands before the possessed: Tamil *aracan-iṉ* "of the king", oblique *mara-tt-* (looked up: Wikipedia, Dravidian languages) | head-last; titles follow in apposition (guess) | yes (as in earlier notes) |
| Munda (Santali, Ho, Mundari) | suffix on the possessor before the possessed: Santali *-rɛn* (animate), *-aˀk* (inanimate); Ho *En Eraaḱ Kolom* "that woman's threshing floor" (looked up: Wikipedia Santali, Ho; source Ghosh 2008) | not found; Santali is "strictly head-last" so modifiers precede nouns (looked up); title-after-name is a guess | yes: noun phrase = (Demonstrative) (Quantifier) (Adjective) Noun, with numeral classifiers (looked up) |
| Burushaski | genitive *-e* / *-mo* on the possessor, placed before the possessed: *Hunzue tham* "the Emir of Hunza" (looked up: Wikipedia Burushaski) | the example above puts the title last after a genitive place name; personal-name order not found | yes: adjectives, numerals and demonstratives always precede the head noun; possessor precedes possessed (looked up: Hunza grammar sketch, Archive `a-grammatical-sketch-of-hunza-burushaski`) |
| Sumerian | genitive phrase follows the head: *e2 lugal-ak* "the king's house"; order noun, adjective, numeral, genitive phrase (looked up: Wikipedia Sumerian) | name then title is the usual order in royal inscriptions (guess from memory) | numeral follows the noun in the standard order (looked up) |
| Elamite | modifiers follow heads and the head's class suffix is copied onto the modifier: *šak Halluduš-Inšušinak-(i)k* "son of H." (looked up: Wikipedia Elamite) | name first, then appositive title + place: *U Šutruk-Nahhunte, šak …, sunki-k Anzan Šušun-ka* "I, S., son of …, king of Anshan and Susa" (looked up, same page) | not found |
| Indo-Aryan (Vedic) | genitive on the possessor; Vedic phrases are mostly head-final (looked up: Hock, citing Schäufele); possessor-first compounds (guess from memory) | either order (guess) | numerals before nouns (guess) |

The grammar facts keep Sumerian and Elamite out of the home seals (possessed noun first, the opposite of `[name] jar man`) and leave Dravidian, Munda, Burushaski and Indo-Aryan level, as before. The puns separate them.

## 5. Where rivals tie or beat Dravidian, and the 15 seals

Rivals tie or beat Dravidian only on signs read at 3 letters, never on whole word or 4 letters, and only on four signs:
- comb 400: Sanskrit *kaṅkata* ~ *kanittha* "small", *kana* "young" (a good pun).
- staff 142: Munda *latkao* ~ *lat* "lord" (an English loan) and Sumerian *subar* ~ *sublugal*.
- carrier 151-158: Santali *arar* ~ *aras* "pole kept on a load".
- jar 740: Sanskrit *kuṭa* "house, family" (a homophone of the Dravidian word).

Reading the 15 seals of `language_candidates.md` with each rival's values (`rival_read15.py`, values = these best puns, blanks where no pun exists):
- Dravidian: all 15 have a value for every sign (as in the earlier note).
- Munda: values for 740 (*chanda* "family dues"), 400 (*chabha* "small"), 520 (*barki* "chief wife"), carrier (*aras* "keep"), 142 (*lat* "lord"); 1 of 15 seals fully covered (M-1828, 142-156: "lord keep"). Fish, man, tree and the three-headed person have no Munda value, so all fish-and-jar seals stay blank.
- Sanskrit: values for 740 (*kuṭa*), 400 (*kanittha*), 090 (*bharitṛ* "sustainer, master"); 0 of 15 covered (fish 220 and spear 520 have none).
- Sumerian (*subar* for 142 only), Burushaski, Elamite: 0 of 15.

## 6. Commitment

Dravidian is the language the pictures sound like. Measured: homophone-level look-alikes 6 of 9 against 0.46 expected (4e-7), 4-letter 7 of 9 against 1.02 (6e-7); the strongest rivals get 0 of 9 (Munda, against 0.22 and 1.00), 1 of 8 (Sumerian), 0 of 7 (Turner Indo-Aryan), and Monier-Williams cannot be told from chance. The margin in odds is at least a factor of 10^5 to 10^6 over the best rival on the strict tests, and about 1,000 to 1 on the 3-letter test (6e-4 against 0.2). Without the two hand-added rows it is still 2e-4 against 0.3 to 1. Burushaski and Elamite stay unranked for lack of dictionary: the lists I could get cover a fraction of the real vocabularies (Berger's Burushaski dictionaries are not open). Next, building on this: put every rival's best pun on the four tied signs (comb, staff, carrier, jar) into the name-slot checks, and get Berger's Burushaski dictionary by a paid or library route (tell Cúper the price when found) to give Burushaski the same run.
