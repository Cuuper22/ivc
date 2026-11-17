# Gulf round seals, second pass: new sequences read off the printed plates

Job of 2026-11-17. Tables: `work_data/gulf2/sequences.csv` (26 rows), log `work_data/gulf2/log_checks.txt`. Scripts: `work_scripts/gulf2_01_checks.py`, `gulf2_02_strict.py` (they reuse the abroad4 home models and matched home draws). No word is attached to any sign. Sign numbers are our Lipi (Wells) numbers. Reading order is right to left on the impression unless the row says otherwise.

## What was found

1. **The browser opened what plain fetch could not, and it paid: 14 new round-seal or cylinder-seal texts from outside the Indus region, 5 probable repeats of seals we hold, 4 maybes, 3 rows with no Indus text.** The key page was Vidale, Desset and Frenez 2021 (open PDF, Journal of Archaeological Studies 12/4), whose Fig. 4 reprints Laursen's plate of 28 inscribed Gulf-type seals with Laursen 2010's Table 1 numbers; Laursen 2010's own PDF (harappa.com) gives the source of each number (Kjaerum, Al-Sindi, Gadd, Amiet, Hallo and Buchanan). Also new: the Jalalabad cylinder (Iran) and the McMahon cylinder fragment (British Museum 1960,0718.1.1, Sistan or Swat, photographed on the museum page). By place: Bahrain 5 (Laursen nos. 6, 7, 8, 9, and the pseudo-text no. 11), Failaka 1 (no. 13), Iran 3 (Amiet no. 15, Jalalabad, McMahon), Mesopotamia 3 (Babylon no. 23, Gadd no. 24, Langdon no. 25), unprovenanced Yale 2 (nos. 26, 27).
2. **The person sign keeps turning up, and it is the one result that holds even when only the clear drawings are counted.** 9 of the 12 new texts of 2+ signs hold 090 or 091 (75%); matched home seal texts of the same lengths give 0.72 of 12 (6%), 95% range 0 to 3, P of 9 or more by chance 0.00005. Strict version, counting only the three texts where the man is clear on the page or named by the authors (Gadd no. 24, Jalalabad, McMahon fragment): 3 of 12, chance gives 0.74, P 0.034. Person tokens are 16 of 61 drawn signs (26%) against 1.1% in matched home seals. In plain words: chance does not put a man or twin-men sign into these texts; it points the same way as the old 12 of 16 and as Vidale's reading of Parpola's groups.
3. **The job-class order is worse than at home, same direction as before.** Over the 6 new texts that have neighbouring identified signs (15 steps): sign-pair model 8.44 bits per step against 5.96 for matched home texts (95% range 4.29 to 7.94, P 0.007); frame v2 8.34 against 6.52 [5.21, 8.00] (P 0.0085). Pooled with the 21 round seals already scored (27 texts, 83 steps): sign pair 9.29 against 5.86 (+3.44, P 0.0005), frame v2 8.84 against 6.66 (+2.18, P 0.0005). In plain words: the home habits for which sign follows which guess these texts worse than they guess home seals, and adding the new ones makes the gap larger (+3.79 before, +3.44 now), not smaller.
4. **The stroke-then-person unit shows up once among the new ones, at Jalalabad (003 then 090, the stroke group is eroded and uncertain).** So the old count of 6 round texts holding it becomes 7, from a pool that is now larger. Chance for this is not computed here: the sample of new texts with an identified stroke next to an identified person is one.
5. **Where the signs are known the texts end badly for a home reader.** Known last signs of the new texts: 031, 527, 090, 032. 527 and 090 sit in the after-jar title class and 031/032 are numbers; none is a jar or a closer. The jar 740 does not appear at all (741 appears once, at the head of Jalalabad, effaced).

## What went against

- **Most signs could not be named.** Of 84 signs drawn across the 16 texts, 30 got a Lipi number, all marked unsure except where the authors give numbers (Jalalabad) or the drawing is plain (strokes, clear men). 54 are ALT (a drawn sign I could not match). The page images are low-resolution bitmaps with signs 10 to 40 pixels tall. So the order test rests on 15 steps in 6 texts, and the identified signs are the conspicuous ones (men, strokes, grids), which biases the person-sign count upward. The strict count (3 of 12) is the number to hold; it still beats chance, at P 0.034.
- The unigram cost does not go up for the new texts alone (6.71 against 7.22, P of higher 0.83): the extra cost is in the order, not in the choice of signs, which is what the old set said for the sign-pair gap.
- Five rows are probable repeats and four more are maybes judged by shape, sign count and findspot only (no catalogue number ties them).
- The Linear Elamite seal (Laursen no. 28) and the two-V mark seal (no. 56) carry no Indus text; no. 11 is pseudo-script by Laursen's own account and is kept out of every count.

## The new sequences

Source for every Laursen number is Laursen 2010, "The westward transmission of Indus Valley sealing technology", Arabian Archaeology and Epigraphy 21: https://www.harappa.com/sites/default/files/pdf/The_westward_transmission_of_Indus_Valle.pdf (Table 1 and Fig. 9 caption) and the plate in https://jarcs.ut.ac.ir/article_81265_f85f962ddf0a7a91b4da2c938352e375.pdf (Fig. 4, page 10 of the PDF). Signs shown with ? are the best match; runner-ups are in the csv column `signs_marked`.

| id | place | publication and number | animal | signs (reading order) | picture |
|---|---|---|---|---|---|
| G2-01 | Bahrain | Kjaerum 1994 fig. 1726; Laursen no. 6 | bull, broken | 091? (alt 090-090), two signs survive | broken seal |
| G2-02 | Bahrain | Kjaerum 1994 fig. 1725; Laursen no. 7 | bull | 090?-090?-055?-002?-ALT | bull below text |
| G2-03 | Bahrain | Srivastava 1991 fig. 55; Laursen no. 8 | bull | 090?-ALT-031?-ALT-ALT | bull |
| G2-04 | Bahrain | Al-Sindi 1999 no. 182; Laursen no. 9 | none (text only) | 055?-ALT-090?-090?-031? | horizontal text only |
| G2-05 | Bahrain, Karzakkan | Laursen fig. 1b, no. 11 | bull | 091-032?-003? (pseudo-script) | bull; not counted |
| G2-06 | Failaka | Kjaerum 1983 no. 279; Laursen no. 13 | bull | 220?-six ALT (7 signs) | bull, Dilmun-type boss |
| G2-07 | Iran | Amiet 1973 pl. 23a-b; Laursen no. 15 | bull | 091?-ALT-ALT-ALT | bull |
| G2-08 | Babylon | Gadd 1932 pl. III/15-18; Laursen no. 23 | bull and manger | five ALT | bull and manger |
| G2-09 | Mesopotamia (Ur collection) | Gadd 1932; Laursen no. 24 | two bulls | 220?-090-090-527? | two bulls, large thick seal |
| G2-10 | Mesopotamia | Langdon 1932 p. 48; Laursen no. 25 | bull | seven ALT | bull |
| G2-11 | unprovenanced (Yale) | Hallo & Buchanan 1981 no. 1088; Laursen no. 26 | bull | ALT-090?-090?-ALT | bull |
| G2-12 | unprovenanced (Yale) | Buchanan 1981 no. 1089; Laursen no. 27 | cattle-like | ALT-ALT-090?-ALT-ALT | animal |
| G2-13 | Jalalabad, Fars, Iran (NMI 2698) | Vidale, Desset & Frenez 2021 figs. 1-3 | none, snake-man scene | 741?-032-090-003?-090? (authors' numbers; reading direction disputed) | cylinder |
| G2-14 | Sistan or Swat | BM 1960,0718.1.1 (McMahon) | none | 090?-ALT-090?-090?-032? (mirror of the seal, photo) | cylinder fragment |

Probable repeats (not counted again): Laursen no. 14 = our 3881.1 Susa; no. 16 = 3897.1 Ur; no. 18 = 5231.1 Ur (man and trident-tree, clear); no. 21 = 3898.1 Ur (trident, leaf-oval, stroke, box, strokes); no. 12 = 147.1 Failaka. Maybes: no. 10 Janabiyah (our 5232.1), no. 17 Ur (3899.1), no. 20 Ur (5225.1), no. 22 Girsu (5222.1). Parpola's own reading of no. 10, in his sign numbers, is in `sequences.csv`. Not scored: no. 19 (one hook sign), no. 28 (Linear Elamite), no. 56 (two V marks).

## Sources reached and not reached

Reached: Laursen 2010 PDF; Vidale-Desset-Frenez 2021 PDF; British Museum record and photograph for the McMahon fragment (cookie banner declined).
Not reached: Fuls corpus (indus.epigraphica.de answers 401 Unauthorized, a sign-in wall, skipped); Parpola 1994, CISI vol. 3, Kjaerum 1983 and 1994, Al-Sindi 1999 (not online); the Desset CISI 3.3 chapter on orbi.uliege.be (the file link was refused by the browser pane, the record page opened); Vidale's DAI and Melammu figures (not read for lack of time, same seals as Laursen's plate); Penn, Louvre, Bahrain and Kuwait museum pages (not tried). Laursen's own Fig. 9 plate is blank in the harappa copy, and the rotated Table 1 could not be read to the site level, so places for nos. 6-9 come from Fig. 4's colour key and the Fig. 9 source list (Kjaerum and Al-Sindi are Bahrain publications). One attempt to load a PDF-reading script into a page was stopped by the tool's permission check and was not retried; reading was done by screenshot.

## Next

Rerun `gulf2_01_checks.py` after the 54 ALT signs are named. Best route: the Laursen plate at higher resolution (the printed article or the 2020 chapter) or Parpola 1994, then key the signs into `sequences.csv` column `signs_best`; the script reads that column.
