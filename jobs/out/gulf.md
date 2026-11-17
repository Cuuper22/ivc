# Gulf material from the published literature, and the test of [stroke][person]

Job of 2026-11-17. Scripts: `work_scripts/gulf_01_score_ours.py` (scores every round seal we hold). Tables: `work_data/gulf/ours_scored.csv` (our 41 round faces scored), `work_data/gulf/literature_pieces.csv` (19 published pieces). No word is attached to any sign. Sign numbers are our Lipi (Wells) numbers.

## What was found

1. **No new sign sequence could be reached, so the new-material test could not run.** Every free page I could open gives how many signs a Gulf seal has, never which signs. Zero new texts were added to the 37 round texts. The unit stands where it stood: 6 of 37 round texts, 1 of 3,426 other home texts. The prediction (other counts 2, 3, 4 if it is a number; stays "one" if a title; absent if chance) is still untested on anything new.
2. **The count of Gulf-type seals is larger than our catalogue.** Vidale 2005, the one full text I got, lists Gulf pieces by sign count: a Failaka stamp with 6 to 8 signs, a Bahrain round seal with 4 signs, a Bahrain round seal with 5, a partial Bahrain seal with 2 signs ("perhaps" twin men or a doubled man), a Bahrain prism seal with 3, a Susa stamp with 7 signs, and two Parpola-catalogue round seals with 6 signs each. We hold 1 Bahrain round seal and 2 at Failaka (3 and 4 signs). At least 3 to 5 pieces are not in our catalogue (the Failaka 6-to-8, the Bahrain 4-sign, the Bahrain 2-sign, the Bahrain prism, and probably one 6-sign Parpola piece). Their signs are in figures I could not open.
3. **A published number agrees with our person-sign finding.** Vidale, passing on Parpola, says the man sign and twin men are very rare at Mohenjo-daro and become more common as western texts depart from Indus norms: under 10 percent of texts in the group Parpola judges certainly Indus in order, almost 50 percent in the "probably Indus" group, over 60 percent in the non-Indus group, about 70 percent in the most uncertain. Ours: a person sign in 16 of 23 foreign and unknown-site round texts (70 percent), and 2 of 15 home round faces. Different counting, same direction, from a different hand. What it opens: the person-sign rate can be checked against Parpola's four groups once the catalogue is in hand.
4. **Nobody I could read notes the stroke before the man.** Vidale's text has no sentence on strokes or numbers with the western signs (searched for "stroke", "number", "count", "tally"). Laursen's abstract speaks of prefixed twin signs only. So the unit [short stroke][person] is ours, as far as these sources go.

## Our own pieces, scored (all 41 round faces, 37 with two or more signs)

Unit = a short stroke sign (001-005, 055) directly before a person sign (090, 091, 093, 095), in reading order.

| group | texts of 2+ signs | unit | tall stroke (031-036) before person | person sign present | person sign last | jar 740 present / last | home fixed phrase present |
|---|---|---|---|---|---|---|---|
| abroad (Gulf, Mesopotamia, Iran) | 16 | 3 | 0 | 12 | 2 | 1 / 1 | 1 |
| unknown site | 7 | 2 | 0 | 4 | 1 | 1 / 1 | 0 |
| home round | 14 | 1 | 0 | 1 | 0 | 0 / 0 | 4 |
| all | 37 | 6 | 0 | 17 | 3 | 2 / 2 | 5 |
| new literature pieces | 0 scorable | - | - | - | - | - | - |
| ours and new together | 37 | 6 | 0 | 17 | 3 | 2 / 2 | 5 |

The six unit texts, with position of the unit in the text:

| id | site | animal | text (reading order) | stroke | place | person ends text |
|---|---|---|---|---|---|---|
| 148.1 | Failaka | none given | 716-350-001-090 | 001 | 3rd-4th of 4 | yes (090) |
| 3863.1 | Bahrain | short-horned bull | 190-060-055-090-160 | 055 | 3rd-4th of 5 | no |
| 3888.1 | unknown | other | 032-132-000-055-090 | 055 | 4th-5th of 5 | yes (090) |
| 5223.1 | unknown | short-horned bull | 160-384-133-001-090-000 | 001 | 4th-5th of 6 | no (a lost sign follows) |
| 5229.1 | Saar | none | 055-220-091-001-093-031 | 001 before 093 | 4th-5th of 6 | no |
| 4247.1 | Dholavira (home) | short-horned bull | 000-255-368-001-091-806 | 001 before 091 | 4th-5th of 6 | no |

What the table says. The stroke before the person is 001 (four times) or 055 (twice) and nothing else; no two, three or four. The unit sits in the second half of the text in all six, and ends the text in 2. The home fixed phrases (list `work_data/phrases/phrase_list.csv`) that appear in round texts sit in the home round seals (1388.1, 1924.1, 3668.1, 4247.1 via 368-001) and in two Gulf-area seals as single short pairs (5227.1 has 455-220); none of the six unit texts holds a home phrase except 4247.1 (368-001, the Dholavira seal). The jar closes 2 round texts (3889.1, 5222.1); neither holds the unit.

Note on 055: the sign drawing is four small strokes stacked three high. If it means twelve (the dozen sign), the two 055 cases are "twelve" and the four 001 cases "one". Then the stroke before the person takes two values, 1 and 12, which is not a single fixed "one". This was in the brief; the table shows it. It stays a lead, not a result.

## The pieces found in the literature

Full table in `work_data/gulf/literature_pieces.csv`. Sign sequences "as published" are given for none: sources reached gave counts only. Where a piece may be one we already hold, the match is by site and sign count only and is marked unconfirmed.

| piece | site | number | shape / animal | date as published | signs as published | in our catalogue? |
|---|---|---|---|---|---|---|
| Failaka stamp, Vidale fig 3,1 | Failaka | not in text | stamp / short-horned bull | - | 6-8 signs, order not Indus | probably not (ours have 3 and 4) |
| Madinat Hamad seal, fig 3,2 | Bahrain | - | round / bull | 2200-2000 BC | 4 signs, Indus signs in non-Indus order | probably not |
| Bahrain glazed seal, fig 3,3 (with Amorite-name tablet) | Bahrain | - | round / bull | tablet about 2000 BC | 5 signs | maybe 3863.1 (5 signs) |
| Bahrain partial seal | Bahrain | - | - | - | 2 signs, "perhaps" twin men or doubled man | no |
| Bahrain prism seal | Bahrain | - | prism / bull and two caprids | - | 3 signs | no |
| Susa cylinder | Susa (Louvre) | - | cylinder / two bulls | - | 7-9 signs | very likely 3882.1 |
| Susa stamp | Susa | - | round / bull | - | 7 signs | maybe 3881.1 |
| Luristan seal | Louvre | - | - / bull | - | 4 signs, Indus order (Parpola) | 2153.1 |
| Parpola 1994 fig 1718.39 | bought in Mesopotamia | fig 1718.39 | round / bovid | - | 6 signs | maybe 5223.1 |
| Parpola 1994 fig 1719.36 | London purchase | fig 1719.36 | round / bovid | - | 6 hard signs | no |
| Lagash seal | Lagash | - | - / bovid | - | 5-6 signs | maybe 5222.1 (Girsu) |
| Clay sealing said from Jhoka (Umma) | Umma | Ashmolean, no number on page | jar sealing / bull and manger | - | 6-sign line | our Umma tag 3884.1 has 5 signs, so unconfirmed |
| Ur, Gadd 1, BM 120573 | Ur | Gadd 1; Mitchell 7 | rectangular stamp / bull | about 2500 BC | cuneiform line, not Indus | excluded |
| Ur, Gadd 6, BM 122947 | Ur | Gadd 6; Mitchell 17 | cylinder / zebu | Dilmun | none recorded | not inscribed |
| Ur, Gadd 8, BM 118704 | Ur | Gadd 8; Mitchell 11 | round Dilmun type / gazelle, two men | 2000-1800 BC | none | not inscribed |
| Ur, Penn 31-43-76, -74, -75 (Gadd 5, 11, 12) | Ur | as listed | button seals | -75 is 1530-1150 BC | no Indus text recorded | not scorable |
| Twelve Ur seals (BM records, second-hand thread) | Ur | no numbers | circular stamps | one 2500-2000 BC | 5 carry an inscription line, signs not given | cannot be matched to our 5 Ur seals |

Sources and how far I got:

- Vidale 2005, DAI digital edition: https://publications.dainst.org/books/dai/catalog/view/2043/2440/4491 . Full text read through a page-reading tool, drawings and sign tables missing, some scrambled pages. The harappa.com page is excerpt only: https://www.harappa.com/content/short-horned-bull-indus-seals-symbol-families-western-trade . A direct download from the DAI site was stopped by a bot-check page, so I read it only through the tool.
- Laursen 2010: abstract only: https://www.harappa.com/content/westward-transmission-indus-valley-sealing-technology-origin-and-development and summary https://www.harappa.com/blog/story-gulf-type-indus-seal . The page lists a 1.33 MB PDF but the link is behind a Cloudflare check that stopped my download, and the browser extension on Cúper's Chrome was not connected, so I could not open it.
- Laursen and Steinkeller 2017 (book): publisher and shop pages only (https://eisenbrauns.org/books/titles/978-1-57506-756-8.html); harappa.com review page for the related book summary: https://www.harappa.com/content/babylonia-gulf-region-and-indus-archaeological-and-textual-evidence-contact-third-and-early . No text.
- Laursen 2016 (royal-house symbols): review page only: https://www.harappa.com/content/symbols-dilmun%E2%80%99s-royal-house-and-adopted-late-indus-world
- Parpola 1994 (Qala'at al-Bahrain vol. 1): not reached. Known only through Vidale's citations of it. Mention only.
- Kjaerum 1983 and 1994: not reached. Only a photo page with their figure numbers: https://www.harappa.com/node/4078
- During Caspers: summary page only: https://www.harappa.com/content/murghabo-bactrian-archaeological-complex-and-indus-script
- Olijdam and Carter (Saar): summary pages only; neither names an inscribed Saar seal: https://www.harappa.com/content/dilmun-meluhhan-relations-revisited-light-observations-early-dilmun-seal-production-during , https://www.harappa.com/content/saar-and-its-external-relations-new-evidence-interaction-between-bahrain-and-gujarat-during
- Museum pages (record text only, no sign sequences): British Museum https://www.britishmuseum.org/collection/object/W_1928-1009-56 , https://www.britishmuseum.org/collection/object/W_1931-1010-15 , https://www.britishmuseum.org/collection/object/W_1927-0527-201 , A_1947-0416-2; Penn https://collections.penn.museum/collections/object/59243 , /26770 , /37951 ; CDLI P466579 (Ur sealing, no Indus signs). Two further British Museum pages returned only menus. Louvre and Yale Babylonian Collection: no Indus seal page reached.
- Harappa.com blog on the Umma sealing https://www.harappa.com/blog/indus-seal-impression-umma-mesopotamia and Louvre cylinders https://www.harappa.com/blog/indus-cylinder-seals-louvre (the Louvre page names no Indus text).
- Fuls' online corpus (indus.epigraphica.de): the fetch was stopped for lack of permission; not read. The Fuls catalogue lists Failaka, Hajar, Bahrain, Ur, Susa, Kish, Tello and the Iranian sites, which is the same set our catalogue was built on.
- Wikimedia Commons: its search interface refused automated calls (rate limit), no image reached. Archive.org: lending copies only. Kalyanaraman's blog (dilmunseals.blogspot.com) lists Gulf seals but reads them as metalwork vocabulary with no sign sequences usable here; not used.
- Photos: none opened, because none was reachable.

## What the publications say

- **Laursen (2010, abstract only).** Makers: Harappans working in the western orbit invented the Gulf Type seal, and by about 2050 BC it belonged to merchant communities in Dilmun. Dating: early Dilmun, about 2100-2000 BC; the page says nothing of the square seals. Texts: the inscriptions carry unusual prefixed twin signs, and a newly found seal with a fake inscription supports the view that the language was not the Harappan one. Stroke-plus-man group: not mentioned in what I read.
- **Parpola (1994), through Vidale.** Parpola sorts the western texts into four groups by how Indus their sign order is (certainly Indus, probably Indus, non-Indus, extremely uncertain), and holds that many probably write a foreign language. Makers and dates: not in what I read. Stroke group: not mentioned.
- **Vidale (2005, full text without figures).** Makers: Indus immigrants and probably Indus enclaves in the west, trading families, perhaps bead traders, who kept the short-horned bull as a family mark. Language: one or more Semitic languages, possibly Amorite; he suggests the man sign and twin men are family-relation words, "son of" and "descendant of", noting that D'Agostino likened the twins to the Sumerian sign for "son". He calls it a hypothesis and says the five Bahrain texts are too few and worn to test it. Dating: the earliest western seals (before Akkad) copied Indus square seals, then people in Mesopotamia and the Gulf took to round steatite stamps with the bull; this he marks "perhaps". Strokes: nothing.
- Links are in the source list above.

## The short-horned bull and Vidale's argument

Our numbers: 14 of 26 beast seals abroad carry the short-horned bull against 92 of 1,575 at home (P 7e-11); 13 of the 14 abroad are round (the one square is at Salut); among the 23 foreign and unknown-site round texts of 2+ signs, 15 have the bull. At home the 87 bull seals read like ordinary seals (5.79 against 5.66 bits per step).

What survives. Vidale's picture of Indus-descended families in the west keeping the bull is untouched by these numbers; it says the bull is a mark of those families, and a bull on 13 of 14 foreign round seals fits it. His order in time (square copies first, round stamps later) also fits our dates (Kish and Tello square seals earlier; Ur, Susa, Failaka, Bahrain round ones later).
What does not. His premise that the bull on ordinary Indus seals points to the western trade: the 87 bull seals at home carry no text of their own and none of the round-seal phrases (the unit appears once among 2,002 home seal texts, Kalibangan 1898.1, text 575-252-002-093-760-740). The bull follows the round shape rather than the place. So the argument stands for round seals abroad and has nothing under it at home. On his man-sign evidence our numbers agree on rate (16 of 23). On his "son of" reading: a patronymic sign should sit between two name parts. The man sign 090 is in the middle in 6 of 10 round uses (shuffle 5.2) and twin men 091 in 3 of 6 (shuffle 3.3): equal to chance, so no support for it; and a stroke before the person is a feature his reading does not cover. Of the six unit texts, 2 hold the bull, against 15 of 23 for all foreign round texts; the unit is not a bull-seal feature.

## What the added material does to the reading

It leaves it. No new sign sequence was reachable, so nothing was added to the 37 and nothing turned against. The reading (a Gulf-made record of a person with a number, not a home-style name) stays as the one being built on; the prediction made before this job is untouched and open: new Gulf round seals with strokes 2, 3, 4 before the person would make it a count, a stroke that is always 001 or 055 would make it a fixed title, absence would make our six chance. Two things moved a little: the Gulf corpus is bigger than ours by at least three or four pieces (Vidale's counts), and a published rate of man and twin signs in western texts matches ours in direction.

The single source that would settle it: **Parpola 1994, "Harappan inscriptions: an analytical catalogue of the Indus inscriptions from the Near East", in Qala'at al-Bahrain, vol. 1** (Aarhus University Press / Jutland Archaeological Society). It gives drawings and sign sequences of the western texts, the very figures numbered 1717-1719 that Vidale cites. Price: I did not find or check a price. Free routes tried: none gave it. Free routes still open and not tried by me because they need Cúper's browser: the Laursen 2010 PDF on the harappa.com page (1.33 MB, behind the Cloudflare check), Vidale's PDF with figures from the same DAI page (behind a bot-check) or the Academia.edu copy the harappa.com page links, and the Fuls online corpus (permission was not given in my session). Next after that: Kjaerum 1983 (Failaka) and 1994 (Bahrain); the Corpus of Indus Seals and Inscriptions volumes (Parpola and colleagues, Helsinki) for the museum numbers.

## What went against

- The job's central test did not run: zero new sign sequences, so the unit has no new support and no new counter-case. The number to keep: 6 of 37, all stroke 001 or 055, none above "one".
- Vidale's reading of the man and twin signs as "son of" is not helped by our positions (middle 9 of 16 uses against 8.5 by shuffle).
- Several matches between his pieces and our ids rest on site and sign count alone and may be wrong (marked "maybe" in the table).
- The two earlier worries stay: the tally patterns together equal their shuffles (9 against 7.7), and the stroke before the person is only "one" or the dozen sign.

Rescue for the next run: get one source with figures (Parpola 1994 or Laursen 2010) opened in Cúper's browser, key in the 8 to 10 uncatalogued western texts, and rerun `work_scripts/gulf_01_score_ours.py` with them added. The prediction above is already fixed.
