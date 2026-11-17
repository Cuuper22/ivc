# Outside match through cotton and cloth: the foreign objects, the cuneiform side, the loan candidates

Scripts (in `work_scripts/`, run `python3` from there): `abroad2_01_cdli_meluhha.py` (pulls every CDLI text with Meluhha in it, 202 texts), `abroad2_02_foreign.py` and `abroad2_03_formula.py` (foreign objects and the count-then-tree formula), `abroad2_04_scan_atf.py` (Meluhha lines in context), `abroad2_05_705_390.py`, `abroad2_06_loanskeleton.py` (word-shape match, Sumerian cloth words against Dravidian cloth words), `abroad2_07_overrep.py`, `abroad2_08_cdli_cloth.py` (cloth words with Dilmun, Elam, Magan, Meluhha), `abroad2_09_grade.py`. Tables and logs in `work_data/abroad2/`. Every script has its predictions at the top. Reading order = stored order reversed. `measured` = a number out of a script, `looked up` = from a page fetched today (link given), `guess` = mine.

Plain words used below. *Face*: one text on one object side. *Name slot*: the place just before the closing jar sign (740, "of the house"). *Tree family*: the signs 390, 392, 405, 406, 407, one tree drawing with several numbers. *Count formula*: a number sign standing right before the counted thing. *Sealing*: a lump of clay pressed with a seal, used to close a jar, bag or bale. *Word shape*: first consonant class plus second consonant class of a word, vowels ignored. *Loan*: a word one language took from another.

## What was found

**No cuneiform text or word lines up with an Indus text yet. What this pass did find is that the cotton formula travelled whole to Mesopotamia and Oman, and that the cuneiform side counts cloth the way our cloth sign is counted.**

1. **The goods formula "two, four, tree" is on two foreign objects exactly as at home.** `measured` At home the short-stroke 4 (sign 004) stands right before a tree-family sign on 39 of 90 places (chance expectation 2.6) and the adjacent pair `002-004` is followed by a tree sign in 16 of 20 places (390 ten times, 407 four, 405 twice). Abroad, `002-004` occurs twice and both times a tree sign follows: Umma (`127 705 002 004 390`) and Salut in Oman (`595 278 002 004 392`). A third foreign object, the Ra's al-Junayz jar sherd, has `004 405`. Tree sign right after a 4 abroad: 3 of 6 places against 43% at home (consistent, P 0.53) and against 2.8% for a random sign (P 0.0004). Reading: the home goods line "[opener] two shares, four, cotton" (`817 002 004 390`, 6 home seals) is the same line that sits on a clay sealing at Umma and a seal at Salut. The writing of cotton lots was exported unchanged. `abroad2_03_formula.py`, `formula_log.txt`.
2. **The Umma object is a jar or bale sealing, and it carries the cotton lot line.** The home catalogue lists it as 3884.1, TAG:L, clay, unicorn bull, excavation number 1931.120; that number is the Ashmolean accession given in Parpola's caption. `looked up`: Parpola's figure caption says "typically Harappan square stamp seal" on the front and cloth on the back ([Parpola 1994, fig. 7.16, free PDF](https://sindhilanguagelibrary.com/assets/documents/pdf/647f088f1fff3.pdf)); Tosi, quoted on [harappa.com](https://www.harappa.com/blog/indus-seal-impression-umma-mesopotamia), says the back shows cloth tied over a jar mouth with a string and a knot hole, that it was in the Louvre before 1914, is said to come from Jokha (ancient Umma, unconfirmed), went to Oxford in 1931, and may have been made in Mesopotamia for an Indus expatriate; he counts six signs, our catalogue has five (open: the Ashmolean photograph would settle whether the strokes are one group of six). Our reading: `[127 bowman] [705 ship or measure] 2·4 [390 cotton]`, "a consignment of (six) cotton". The cloth on the back is the standard jar cover and does not by itself say the jar held cotton.
3. **Cloth is counted by the piece, cotton in lots: a new split on our own data.** `measured` Counted places (a count sign right before): 407 has the tall two before it on 9 of 28, 390 on 2 of 90 (P 3e-5). Cotton runs 3 to 8 (65 of 90 are 3 to 5, 21 of 90 are 6 or more, 4 of 90 are 1 or 2). The cuneiform side does the same: the Umma account CM 26, 136 counts garments one or two at a time (`2 tug2 guz-za`, `1 tug2`), wool is weighed in minas and talents ([P320486](https://cdli.earth/artifacts/320486), [P108448](https://cdli.earth/artifacts/108448)). This supports 407 = cloth by the piece (tuṇi) against 390 = raw fibre in lots, from inside the Indus data. `abroad2_09_grade.py`.
4. **The Girsu Meluhha village and wool.** `looked up` and `measured` from the 202 CDLI texts: 46 are from Girsu, 4 from Umma, 20 from Ur; periods Ur III 60, Old Babylonian 41, Old Akkadian 17, Lagash II 10, Neo-Assyrian 59. The Ur III Girsu wool text CT 3 pl. 17 (BM 14594) records wool (about 41 minas plus 2 talents 50 minas) with Ur-Lamma "son of Meluhha"; the Guabba tablet MVN 7, 420 places the "Meluhha village" at Guabba ([Vermaak 2008, free](https://www.ancientportsantiques.com/wp-content/uploads/Documents/PLACES/IndOc-Gulf/Lagash-Vermaak2008.pdf): over fifty Ur III texts tie Guabba to weaving, about 4,270 women and 1,800 children on one list; he finds no Sumerian textile term tied to Meluhha and does not claim the weavers were Meluhhan). Reading: the one Meluhhan household we can name handled wool, and its village sat in the weaving district. That is the cuneiform shape a "boxed-cotton house" with an agent in Mesopotamia would leave, and it is what to search next (see predictions).
5. **A Mesopotamian cloth text mentions a trip to Meluhha.** CM 26, 136 (Umma, Ur III, governor's expenditure) issues garments to messengers, one of them the courier Utu-illat "when he went to Meluhha". This is the only cloth-plus-Meluhha line in the 202 texts.
6. **Foreign-set share.** `measured` tree-family signs on 11 of 69 foreign objects against 371 of 3,680 distinct home texts (1.56 times, P 0.09; named foreign sites only 1.79 times, P 0.056). The earlier square-seal figure (5 of 14) stays the stronger version.

**What each new lead predicts next.**
- The Ashmolean photograph of 1931.120 should show `705 / two / four / tree` at the right end and settle five against six signs. If a sixth sign is a jar, the line becomes a name plus lot.
- Salut and other Oman tower seals that end in a count plus a tree sign should be found with jars, not with houses: the formula is a contents line.
- The Ur-Lamma family texts at Girsu (Guabba, wool, barley) should carry a title or a seal from a trading house; a seal impression on a Guabba wool tablet is the cuneiform-side find that would be the outside match.

## Foreign objects that carry the box or the tree family

Reading order. Source for findspot where stated is the link; "catalogue" = the Lipi metadata only, not looked up.

| id | site, region | object | animal | text (reading order) | our reading | findspot, date, what is known |
|---|---|---|---|---|---|---|
| 3884.1 | Tell Umma (said), Mesopotamia | clay sealing, tag | unicorn bull | `127 705 002 004 390` | [bowman] ship/measure, 2·4 (six), cotton | AN 1931.120; cloth on reverse; no date; provenance unconfirmed ([Tosi via harappa.com](https://www.harappa.com/blog/indus-seal-impression-umma-mesopotamia)) |
| 1971.1 | Kish, Mesopotamia | square seal | bull | `416 840 060 003 220 590 390 740` | of the house [416 pair 060 three star] boxed-cotton | "plain level" about 9 m down, before Sargon by layer but with a Sargonic pommel; Langdon 1931 (details in `travelled_name.md`) |
| 4155.1 | Gonur Depe, Turkmenistan | square seal | elephant | `285 002 235 220 125 590 390 740` | of the house [285] two [bamboo-star star hunter] boxed-cotton | excavated by Sarianidi in 2004; eight signs; sequences paralleled in the Indus Valley ([CISI 3.3 introduction](https://orbi.uliege.be/bitstream/2268/333796/1/Desset%20F%202022%20in%20CISI%203.3%201763.pdf)); room not given there, seal catalogue left to CISI 3.4 |
| 3335.1 | unprovenanced | square seal | bull | `032 590 390 002 032 205 740` | two, boxed-cotton, two-two [205], of the house | none |
| 16.1 | Altyn-depe, Turkmenistan | square seal | none | `415 390` | branch-cotton (a name) | one of three Indus-type seals excavated in southern Turkmenistan (CISI 3.3 introduction); layer not looked up |
| 3885.1 | Tello (Girsu), Mesopotamia | square seal | tiger | `384 440 390 220 000` | [384 440] cotton star [lost] | catalogue: "3rd millennium"; not looked up |
| 3881.1 | Susa, Iran | cylinder | gaur | `000 365 090 407 604 700` | [lost] [365] man, cloth, [604] cup | catalogue: late 3rd millennium; cloth sign beside the man sign |
| 5231.1 | Ur, Mesopotamia | cylinder | none | `090 405` | man, thread | catalogue; Gadd 1932 accession not looked up |
| 4173.1 | Salut ST1, Oman | square seal | gaur | `595 278 002 004 392` | [595 278] two·four (six) [392 tree] | tower ST1, interior Oman; the chlorite square seal is called probably the best Indus-inspired seal found in Oman ([harappa.com](https://www.harappa.com/blog/new-indus-finds-salut-oman)); Indus pottery and merchants living there ([Frenez and others 2016 abstract](https://archaeopresspublishing.com/ojs/index.php/PSAS/article/view/1247)); tower findspot not given in the pages I could open |
| 3865.1 | Ra's al-Junayz, Oman | jar sherd | none | `004 405` | four thread | catalogue: period II; Cleuziou and Tosi 1994 is the lead ([Black boats of Magan, issuu](https://issuu.com/heritageonline/docs/1994_cleuziou___tosi-_black_boats_o)); not opened |
| 3892.1 | unprovenanced | square seal | none | `900 590 368 002` | [900] box, [368] two | none |
| 5465.1 | unprovenanced | square seal | gaur | `370 031 741 840 390` | garlic-motif, one, jar-dot, pair, cotton | none |

Not one of these has a textile find reported with it in the sources I could open. The Gonur, Altyn-depe and Salut contexts need CISI 3.3/3.4 and the Salut report to be read in full.

## Loanword candidates (cuneiform word, Dravidian word, shape match)

I could reach CDLI (search works), not ePSD2 or ORACC (TLS fails through the proxy). Dates are the earliest I saw.

| cuneiform word | where and when | Dravidian word | sound line-up | verdict |
|---|---|---|---|---|
| *kidinnû / kitinnû*, "cotton" (debated, Zawadzki; Quillien argues for it) | Neo-Babylonian temple texts, about 500 BC, 50 texts ([Quillien 2019](https://journals.openedition.org/ethnoecologie/4239)) | *kiṇṭaṉ* "coarse cotton cloth" (Tamil), Kannada *giṇṭa*, Telugu *giṇṭemu* (DEDR 1540, checked in the local copy) | k = k, i = i; Akkadian has no retroflex, so ṇṭ comes out as -din- / -tin-; ending -aṉ against -nû. Three of four segments | the only one with a published Dravidian proposal (Muthukumaran 2016, as reported by Quillien); 1,500 years after the Indus phase, so it says nothing about Ur III; Quillien notes Sumerian has no cotton word |
| *karpasu*, cotton muslin | Uruk, 253 BC | none: no DEDR entry; Skt *karpāsa* | none | Indo-Aryan, not ours |
| *tug2* "cloth, garment" (Sumerian) | proto-cuneiform onward (also `TUG2 DILMUN` at Uruk III) | *tuṇi* "cloth" (DEDR 3307; Malayalam, Kota, Toda, Kodagu, Kolami cognates) | t-u-?: first two segments match, g against ṇ does not | low; Sumerian is older than the Indus phase, so a loan would run the other way or be chance |
| *pisan* "basket, container, box" (Sumerian; Ur III `pisan tug2-ga`, UET 3 752) | Ur III, earlier date not checked | *peṭṭi* "box, chest" (DEDR 4388; marked as related to Skt *peṭaka*) | p = p, i/e = i/e, s against ṭṭ does not | low; it is the box half of 590-390, so it is the one worth a second test |
| *gu* "string, thread" | Sumerian | *kaṇṭu* "ball of thread" (DEDR 1177) | g/k match, vowel differs | low |
| no cuneiform form found for | *parutti* (3976, cognates to Gondi, Kui, Kuwi), *pañci* (3836), *nūl* (3726) | | | none. No Ur III or Akkadian cloth word has the shape p-r-t or p-n-c |

**Test of the whole class.** `measured` Sumerian words glossed as cloth, garment, yarn, wool, flax, linen, spindle, weaving, cotton, textile (50, from the Wiktionary and Halloran lists) against Dravidian entries glossed likewise (93): 196 shape matches against 139 expected by shuffling, 1,408 of 20,000 shuffles as high (P 0.07, more matches than chance but not significant). With a wider keyword list (89 and 143 words) 507 against 380, P 0.05. The excess is carried by p/b-initial pairs (bar-, bal- against par-, pal-), not by tug / tuṇi. Direction: slightly toward shared shapes, no pair stands alone. `skeleton_log.txt`.

## What went against, with the rescue tried

- **No cloth or cotton word with a Meluhha tag.** CDLI searches for `tug2`, `gada` or `siki` next to Meluhha, and for `tug2`/`gada` with Magan: zero lines. What exists: `tug2 elam` (Ur III, Lagash II, Old Babylonian), `gada dilmun-u3-la2` (Fara period, two texts), and `TUG2 DILMUN` in an Uruk III proto-cuneiform text (`cdli_cloth_east.csv`). The Meluhha goods in the 202 texts are timber, copper, carnelian, birds, a dog, a chair of Meluhha wood. Rescue one (new test): the Indus export may have been named by garment type, not origin; the one Umma garment line (CM 26, 136) is a trip to Meluhha with cloth going out. Rescue two (new idea): cotton reached Mesopotamia as raw fibre or padding and is unnamed before the first millennium (Quillien: Sumerian has no cotton word); that fits cotton being counted in lots on our side and not on any Ur III list. Standing: cotton is invisible in Ur III records, so the match must come from an object (Umma) and a seal, not from a word list.
- **"705 + count + tree" frame (the Umma line) is not special.** A tree sign within the next four signs after 705: 29 of 218 places against 24.4 expected; it is 17 of 20 on copper tablets only because copper tablets are full of 407. Against as a general frame. Rescue: the Umma line is the `002-004 tree` end, which does hold (item 1).
- **Grade reading of the number (Ur III cloth grades 1 to 5, "fourth grade").** Against: 4 of 90 counts before 390 are 1 or 2 and 21 are 6 or more. Rescue: grade can still sit on the 407 side, where 11 of 28 counts are 4, but the 407 counts are mostly pairs (9 of 28), which is piece counting.
- **Count on the Umma tag.** Our catalogue has five signs, Tosi six. Open until the photograph is read.
- **Over-representation abroad is modest** (1.56 times, P 0.09 for the whole foreign set).
- **Susa and Ur cloth and thread signs sit next to the man sign (2 of 2 round seals with a fibre sign)**; at home the fibre signs are next to 090 only 5 of 257 places (4.7 expected). Round seals are short and man-rich (15 of 23), so I read it as a lead for a "cloth-man / thread-man" craft title, not a result.

## Seals with both scripts, or owned by someone named in cuneiform

Every one I could find or the repository audit lists carries one script only.
- Shu-ilishu, "Meluhha interpreter": Akkadian cylinder, Louvre AO 22310, Naram-Sin period or later (Boehmer via Parpola 1994 p. 131); cuneiform and a scene, no Indus signs; the scene looks bought from a ready-cut workshop stock.
- BM 120573 (Ur U.7683, Gadd 1932 no. 1): Indus-style stamp seal, bull, with archaic cuneiform (reading uncertain, "sak-ku-shi-?"); no Indus signs ([repo audit](../../research/data/meluhha/bm120573_object_bridge_audit_summary.json)).
- BM 120228 (Gadd no. 17): round stamp seal, five common Indus signs in an order found nowhere at home; Indus only.
- Kish IM 1822 (Mackay 1925): Indus square seal whose sign string recurs on Mohenjo-daro M-228 (`240 636 740`); our Kish 1970.1 is `240 643 (lost)`, same fish-first start. Indus only.
- Dilmun Gulf seals ("palace of Rimum, servant of Inzak"): cuneiform only (`abroad_seals.md`).
- Ur 3898.1 and 3899.1: Indus only (repo audit). Sealings with cloth on the back besides Umma: none found outside the Indus, Lothal's cloth-backed sealings are at home and their catalogue is closed (Frenez; price and a free copy not found).

## Sources I could not open for free

- Parpola, Parpola and Brunswig 1977, "The Meluhha village", JESHO 20 ([JSTOR 3631775](https://katalog.lib.cas.cz/KNAV/EdsRecord/edsjsr,edsjsr.10.2307.3631775)); no free copy found, price not looked up. CDLI texts used instead.
- Laursen and Steinkeller 2017, *Babylonia, the Gulf Region and the Indus* (Eisenbrauns/Penn State, [listing](https://eisenbrauns.org/books/titles/978-1-57506-756-8.html)); not opened, price not looked up. The repository has its Table 1 queue.
- CISI 3.4 (Gonur seal catalogue) is not yet published; CISI 3.3 front matter is free (link above).
- Frenez and others 2016 on Salut: landing page only; ePSD2 and ORACC would not load through the proxy.

## Notes for MAP.md (not edited)

- `measured` `002-004` then a tree sign: 16 of 20 at home, 2 of 2 abroad (Umma, Salut); 4 then tree 39 of 90 home, 3 of 6 abroad.
- `measured` 407 is counted with a tall two on 9 of 28 places, 390 on 2 of 90 (P 3e-5): cloth by the piece, cotton in lots.
- `guess` Umma 1931.120 = jar sealing "six cotton" from an Indus hand; Girsu wool texts with Ur-Lamma son of Meluhha are the cuneiform side to search.
- `measured` Went against: no Meluhha-tagged cloth word in CDLI; no loan candidate fits a cotton word; 705-tree frame at chance.
