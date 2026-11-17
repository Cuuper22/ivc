# The possessive model: jar = "of", jar + man = "'s man"

Scripts: `work_scripts/possessive_A.py`, `possessive_A2.py` (part A), `gloss2.py`, `gloss2_sample.py` (part B). Tables: `work_data/possessive/` (`after_jar_signs.csv`, `jar_texts.csv`, `master_servant_pairs.csv`, `master_servant_pairs_wide.csv`, `master_servant_pairs_multisign.csv`), `work_data/gloss2_all.csv`, `work_data/gloss2_lexicon.txt`. Reading order = stored order reversed. Part A counts distinct (site, text) non-tablet texts with a complete edge: 1,764 texts, 733 jar uses, jar last 583 times (the brief's 743 / 557 count a slightly different set; same picture).

## Boldest reading, built on

1. The jar is the possessive ending and the text is a noun phrase: `[opener] [name] jar [relation noun]`. Genitive before head noun, title after name, count before counted thing.
2. What follows the jar is a short list of nouns, and it follows the jar the way a head noun follows its possessor: man (090) is after the jar in 50 of its 68 seal texts (74%), the table-X (679) 10 of 13 (77%), X-with-vertical (565) 4 of 9, barred rectangle (621) 3 of 15, comb (400) 16 of 75 (21%), stroke 001 14 of 110.
3. The spear (520) and the porters (151, 154, 156, 158) do the jar's job instead: the spear follows a jar in 0 of 152 uses and ends the text 86% of the time; porters follow a jar 2 of 47 (151), 0 of 25 (154), 0 of 32 (156). They are the other endings that close a name: `[name] spear`, `[name] porter`. Man, 679, 621 are nouns after the jar. Comb is both: 37 seals end in a bare comb, 16 take it after the jar.
4. "X's man" is an agent or steward, not a lesser seal-holder. Seal faces: `of X` median 645 mm2 (n 491), `X's man` 758 (n 46; Mann-Whitney p 0.10), jar + 679 713, jar + stroke 504, jar + comb 258 (n 10, the small rods and tiny seals). The man seals run larger, not smaller; same direction for name lengths 1 and 3 (724 against 576, 853 against 713), opposite at length 2 (471 against 576). The comb is what makes a seal small.
5. A name is crest + self + tag. The learned crests (first sign of a multi-sign name) are 061, 125, 140, 231, 233, 235, 240, 368, 416, 503, 705, 803, 806 and the tags (last sign) 055, 070, 100, 176, 388, 390, 400, 405, 460, 482, 585, 615, 690, 752, 760, 798, 900, 904, 920, 923 (`work_data/gloss2_lexicon.txt`).

## Master-servant pairs (the test)

Servant = text `[name] jar 090`. Owner = text `[name] jar` and nothing after. Names compared sign for sign, openers ignored. All object types, edges allowed to be broken when the name is whole: 819 owner texts, 89 servant texts.

- 21 of 89 servant texts have an owner text with the identical name (113 text pairs): 8 pairs in the same excavation area, 32 at the same site, 73 at another site. For names of two or more signs: 9 of 70 servants, 35 pairs (2 same area, 10 same site, 23 other site). Owner seals match another owner seal of the same name 411 of 819 (50%), 244 of 608 for multi-sign names (40%). So a servant's master is found as an owner at roughly a third of the rate owners find each other.
- Same house or room is rare in the data: the master-and-servant pairs in one excavation area are the ones below. The "same-house" test at block level gives one pair (last-two-sign match M-199 and M-850, both Mohenjo-daro DKG First Street).
- House-mate version at Mohenjo-daro and Harappa (blocks known, names of two or more signs): the servant's first name sign (crest) is shared by an owner seal of the same house in 3 of 21 servant seals (14%) against 15 of 266 owner seals (6%). Last sign: 1 of 21 against 21 of 266. Small numbers; the direction is the one the reading predicts for the crest, and the pairs are listed.
- First design (complete texts only, same site): 8 exact same-site servant-owner matches against 9.2 when owner names are shuffled over owner sites (max 12 in 300 shuffles). The names of masters are drawn from the owner pool as often as chance, so the same-site count does not by itself split the reading from "man is a name part". The pairs with rare, multi-sign names are the test and they are what survives.

Pairs (servant seal and object name / owner seal and object name), multi-sign masters first, then the one-sign masters in the same area:

| master name (signs) | servant (cisi, site, area) | owner (cisi, site, area) | place |
|---|---|---|---|
| 415-100 (pitchfork + three-headed person) | H-188 `415-100-740-090-400`, Harappa, F Granery | H-847 `415-100-740`, Harappa, F Granery | same area |
| 415-100 | H-1978 `415-100-740-090-400`, Harappa, E Trench | H-1991 `415-100-740`, Harappa, E Trench 54 | same site |
| 415-100 | H-188, H-1978 | M-1886, M-363, M-427, M-699, M-727, M-839, M-850, M-869 (Mohenjo-daro: Loop Lane, HR, DKE, HRB, DKG N 21IV, DKG S 1III, DKG First Street) | other site (8 owner seals) |
| 240-415-100 (whisker fish crest + pitchfork + three-headed person) | M-199 `861-002-240-415-100-740-090`, Mohenjo-daro DKG First Street | M-144 `817-002-240-415-100-740`, Mohenjo-daro DKG | same area |
| 240-415-100 | M-1746 `817-002-240-415-100-740-090`, DKG (S) 7II | M-144; M-1418 `240-415-100-740`, HRB 2IX | same site |
| 240-415-100 | Gola Dhoro (Bagasra) Trench Eo 11 (no cisi) | M-144, M-1418 | other site |
| 240-803-585 | M-492 `240-803-585-740-090`, DKG (S) 9IV | M-2030 `240-803-585-740` | same site |
| 705-255 (U-with-stroke + odd animal) | M-100 `861-002-705-255-740-090`, DKE Trench E | M-72 (DKG N 14II), M-286 (DKG S 12V), M-785 (SD 4) | same site |
| 705-255 | H-1840 `550-060-705-255-740-090`, Harappa E Trench 11 | M-72, M-286, M-785 | other site |
| 233-176 (barred fish + seated person) | M-230 `233-176-740-090`, Mohenjo-daro VSA lane 3 | L-35, L-55 `233-176-740`, Lothal | other site |
| 061 | H-565 `061-171-035-740-090`, Harappa F Trench VI | H-521 `061-740`, Harappa F Trench VI | same area |
| 061 | M-265 `061-171-035-740-090`, DKG (S) 9VIII; M-947 `...-090-400`, DKG (S) 7VII | M-204 `817-002-061-740`, DKG (S) 7III | same area |
| 176 (seated person) | M-15 `861-002-176-740-090`, DKG (S) 10III | M-1755 (DKG S 12V), M-511 and M-512 (DKG S 6II) | same area |
| 792 | H-2143 and an unnumbered Harappa seal `792-740-090`, F | M-424, M-953, M-1382 `792-740` | other site |

Reading: `415-100` is a master with owner seals in two cities and two servant seals, one of them in the same Harappa granery area as the master's own seal; `240-415-100` and `240-803-585` are masters whose servants and owners sit in Mohenjo-daro's DKG quarter. Full lists with every house and text: `work_data/possessive/master_servant_pairs*.csv`.

## Parser

`work_scripts/gloss2.py` reads each text as opener + name (crest, self, tag) + possessive jar + relation noun, with counts owned by the sign they count (the first job's ownership table), load tags `[A-comb or count][crop][porter]` as "n loads of crop, carried", and multi-face tablets as records, one line per face.

- Coverage on 2,162 distinct complete texts: 1,957 (90.5%) get a role for every sign with names of at most four signs and an allowed ending; 1,775 (82.1%) with names of at most three signs and one jar. First parser: 1,487 (68.8%). Rerunning the first parser's own test (more than half the signs in template roles, at most two free name signs) on the new roles gives 54.7%, because name signs are free signs there; the two tight numbers do not measure the same thing.
- By object type (new / first): seals 87.5 / 68.1, tablets 95.5 / 75.6, pottery 99.3 / 65.9, copper tablets 86.2 / 58.5, other 97.3 / 57.1.
- 60 glosses with object names, sites and findspots: `GLOSSES.md`.

## Next

Servants of `415-100` and `240-415-100`: read the photographs of H-188, H-847, H-1978, H-1991, M-144, M-199, M-1746, M-1418 for the same hand or workshop. Test the spear as "of the office" by the same pair search on `[name] spear` against `[name] jar`. Take the crest list as the first column of a sound-values hunt.
