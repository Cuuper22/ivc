# Leads from chunk 04 (reader 04)

Read: all 38 files on the reading list (research/docs/archive/...). Numbers marked [my count] were recomputed by me from research/data/open_prototype/lipi/metadata_filtered.csv (rows containing [ or ] excluded; no dedup unless the entry says so) or from research/data/open_prototype/reports/campaign_032_002_post_y_all_002_rows.csv (strict dedup as the note defines it: strict complete closed, then dedup on text, site, type, idx_002). Every other number is quoted from a note and named as such. No Colab or GPU run was made. The quarantined columns (sanskrit, translation, notes) were not read.

Terms: "row" = one inscription's sign string. 032, 002, 220, 390 and so on are catalogue sign numbers with no reading attached. "Closes" = the row ends on that sign. "Unique texts" = distinct sign strings. "Copy family" = one string repeated over many objects.

## Paid source (for Cúper)

CISI volume 3.1 (Corpus of Indus Seals and Inscriptions, Mohenjo-daro and Harappa supplement, ISBN 978-951-41-1040-5). Price per the Tiedekirja reply in research/docs/archive/cisi31_access_acquisition_routes.md: EUR 70 for the book plus EUR 48.25 UPS to the USA, total EUR 118.25. No legal digital access. Invoice requested, not paid. Why it matters: a secondary review (quoted in the same note) gives its range as Mohenjo-daro m1660 to m2132 and Harappa h1020 to h2590. On this chunk's list, M-1677 (outside 820 extension), M-1728 (820 row in the 240 frame), M-1737, M-1763, M-1788, M-1825 (390-705 tail) and H-1993 (blocking object) fall in those ranges. The note records 3761 black-and-white photographs and double-size inscription reproductions with excavation numbers. Free route first: the Finna record lists nine Finnish libraries. The note does not record an interlibrary loan request.

---

### 1. 032 has three right-hand lanes, and the sign before it picks the lane
- What was seen: [my count] 032 occurs 502 times in clean rows; 216 close the row and 42 are followed by 002. Among the 408 with a sign before them: after 220 (56 rows) 24 go on to 002 and 15 close; after any other sign (352 rows) 17 go on to 002 and 154 close. By left sign: 700-032 = 95 rows, 89 close at 032, 93 at Harappa; 740-032 = 58 rows, 33 followed by 840, 1 closes; 220-032 = 56 rows, 37 at Mohenjo-daro.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; research/docs/archive/campaign_032_after_220_function.md.
- Old label: "032 after A-220 is a tail-selector; 002 is the lane" (campaign_032_after_220_function.md, campaign_032_002_tail.md). The after-220 note lists "terminal, 840, 700, 000, 031" as outside-A-220 continuations, describes them as different, and does not analyze them.
- Why it is alive: the 002 lane exists after 220 (43 percent) and is nearly absent elsewhere (5 percent). The two largest 032 frames in the file, 700-032 and 740-032, were never run as frames. A reading with three lanes explains all 502 occurrences better than one A-220 construction does.
- What it would mean if true: 032 is a slot whose right-hand content is set by the left frame. A-220-032-002 is one of three licensed continuations, and the 240 selector result is one branch of a larger table.
- Cheapest next move: tabulate next sign after 032 for every left sign, on strict dedup, across all sites. All the data is on disk. No new source.

### 2. The sign 840 is a second tail after 032 that no campaign followed up
- What was seen: [my count] 840 occurs 110 times; 38 directly after 032. 740-032-840: 33 rows, 22 unique texts, closes at 840 in 12 rows; sites Harappa 17, Mohenjo-daro 12, Lothal 2, Chanhu-daro 1, Dholavira 1. 032-840: 38 rows, 27 unique texts, closes at 840 in 14; sites Harappa 18, Mohenjo-daro 15, Lothal 2, Bakkar Buthi 1, Chanhu-daro 1, Dholavira 1. Types: SEAL:S 15 and TAB:B 17 in the 032-840 rows.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; research/docs/archive/campaign_032_after_220_function.md (names 840 as a top continuation).
- Old label: none. 840 is named once as a top outside-A-220 continuation and dropped.
- Why it is alive: 22 unique texts out of 33 rows means the lane is not one copy. It appears on six sites and on both seals and tablets, which the 002 lane (almost all Mohenjo-daro seals) does not.
- What it would mean if true: 032 licenses two separate tails, 002 and 840. 840 may be the non-A-220 counterpart of the 002 lane, and the 032 slot has a broader class of heads than the post-002 work assumed.
- Cheapest next move: list the 22 unique 740-032-840 texts with object numbers and sites; check whether 840 carries the same register as the 002 lane.

### 3. The 700 sign marks a face or heading on Harappa tablets, but it is copy-driven
- What was seen: [my count] 700 is in 503 clean rows but only 74 unique texts. The three most common are +700-033+ (125 rows), +700-034+ (109) and +700-032+ (89). 700 is the first sign in 391 of the 503 rows, the last in 83, and in the middle in 29. Rows with 700 record two sides in 410 (82 percent), against 828 of 3738 rows without it (22 percent). Controlled by type: TAB:B 230 of 251 two-sided with 700, against 377 of 658 without; TAB:I 172 of 208 against 295 of 442. Harappa holds 474 of the 503.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv (fields: text, sides, type, site). Related: research/docs/archive/campaign_520_220_formula_stem.md (companion classes 700-034, 700-032, 700-033 called "sparse").
- Old label: companion-side classes "sparse; does not yet prove side grammar" (campaign_520_220_formula_stem.md).
- Why it is alive: the association with two-sided objects survives the tablet-type control, and 700 also sits on the counter face of the fish objects (entry 6). A header or face sign on two-sided Harappa tablets would explain why the 700-X pairs are so frequent. The copy count is the signal here: each bare 700-0xx text is a label written on many faces.
- What it would mean if true: the 700-X pairs are face headers. The companion-side work is not sparse; its evidence was counted as copies. Each 700-X text names a face class.
- Cheapest next move: for each of the three bare 700-0xx texts, list objects and sides. Then check whether the two faces of one object carry 700-X on one face and a different text on the other.

### 4. 400-740 is a productive Harappa tablet opener
- What was seen: [my count] 400-740 is in 198 clean rows, 103 unique texts; it opens the row in 191. Sites: Harappa 172, Mohenjo-daro 21, Kalibangan 2, Dholavira 1, Rajanpur 1, Nausharo 1. Types: TAB:B 89, TAB:I 88, ROD 9.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; the fish-counter main faces H-912 (+400-740-760-220-416+) and H-1192 (+400-740-767-220-416+) in research/data/decoding_followup_20260907/summary.json and the decoding note.
- Old label: none. 400-740 is not a frame in any campaign; 520-220 and 740-220 were.
- Why it is alive: 103 distinct texts under one opener is the most varied Harappa frame in the file. The same opener starts the fish-counter main faces, so one template may cover tablets and seals on that site. A varying third sign after a fixed opener is the shape an administrative template takes.
- What it would mean if true: Harappa tablets share one template: fixed opener 400-740, variable third sign, closing formula. The 520-220 and 240-220 frames sit inside that template.
- Cheapest next move: tabulate the third sign across the 103 texts; compare its values with the 520-220-X and 240-220-X closers.

### 5. The largest exact formulas are single texts repeated on many tablets
- What was seen: [my count] +400-740-176+ = 39 rows, 1 unique text: 38 Harappa, 1 Mohenjo-daro; types TAB:I 33, TAB:B 3, SEAL:R 2, ROD 1. The prefix 520-240-002 = 29 rows, 1 unique text, all Harappa TAB:B. The "29 of 44 close at 002" in research/docs/archive/campaign_unit_boundary_520_vs_220.md is this one text.
- Where: research/data/open_prototype/reports/campaign_exact3_formula_counts.csv (ranks 400-740-176 first at 39); research/data/open_prototype/lipi/metadata_filtered.csv; research/docs/archive/campaign_520_220_formula_stem.md (calls 400-740-176 the top exact formula).
- Old label: "major exact formula" (formula stem note); "520 closure to 002 at 0.66" (unit boundary note), not checked for copies there.
- Why it is alive: one text on 39 objects is a fact about issue, not about grammar. An administrative label written or stamped on many tablets predicts exactly this. The copy count per text per site is a count of issued labels.
- What it would mean if true: the most frequent formulas are issue labels. Their frequency measures administrative output, and grammar claims built on raw counts are inflated.
- Cheapest next move: for the 39 +400-740-176+ rows, list excavation numbers. If they are distinct physical tablets from one trench, the count is real output.

### 6. One photo decides whether Lipi 220 is the fish or the cup
- What was seen: Mahadevan's counter on object 448 reads 95-328-59 and on object 452 reads 95-59-328 (decoding note, source-linked). In Lipi, the counter on 448 (H-912 and H-1191, same excavation reference 8650c448, so not independent) reads +220-700-004+, and on 452 (H-1192) reads +700-220-004+. Position by position, Lipi 220 lines up with Mahadevan 328 (cup-shaped) and Lipi 700 with Mahadevan 59 (fish-shaped).
- Where: research/docs/archive/decoding_followup_20260907.md; research/data/decoding_followup_20260907/summary.json; Vats vol. II plates on disk at evidence/tmp/032_002_861_603_slot_source_normalization/vats_excavations_at_harappa_vol2_plates.pdf (the decoding note gives PDF page index 199 for plate XCVI; I did not open the PDF).
- Old label: "physical identity of the main inscriptions not proved; no automatic crosswalk merger" (decoding note). The formula notes treat Lipi 220 as fish or leaf family from prior-work pressure (campaign_520_220_formula_stem.md; P050 shadow mapping).
- Why it is alive: this is a direct split between two readings. If the positional lineup holds, 220 is a cup and the fish premise for the 220 slot fails, which affects the 520-220-X, 240-220-X and 740-220-X frames. If it does not hold, the swap is a Lipi-only change and the premise stands. One photo answers it.
- What it would mean if true: the 220 slot carries a cup-type unit, and every semantic line that began from fish needs re-keying. The fish-square phonetic work also changes, since its operators sit on fish bases.
- Cheapest next move: open plate XCVI objects 448 and 452. Mark which counter sign is the cup and which is the fish. Compare with Lipi 220 and 700.

### 7. Sign 220 closes a row only after some left signs
- What was seen: [my count] 220 closes the row after 520 in 4 of 58 rows, after 440 in 4 of 7, after 032 in 4 of 6, after 000 in 4 of 17, after 740 in 3 of 47, after 240 in 2 of 14, after 176 in 1 of 13. After 002 it never closes (0 of 10), nor after 590 (0 of 8) or 318 (0 of 11). The four bare +520-220+ rows are 282.2 and 1351.1 (Harappa TAB:I) and 2710.1 and 3371.1 (Mohenjo-daro SEAL:S).
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; research/docs/archive/campaign_520_220_formula_stem.md (lists the four bare rows); research/docs/archive/campaign_032_002_post_y_continuation_campaign.md (220 after 002 closes 0 of 9 on strict dedup).
- Old label: "520-220 is a fixed stem with X optional" (formula stem); "220 continuation-heavy after 002" (post-Y note).
- Why it is alive: the same sign closes or continues depending on the sign before it, and the pattern splits cleanly: 002, 590 and 318 never close, while 520, 440, 032 and 000 close in most of their few rows. The left sign works as a function-class marker.
- What it would mean if true: 220 is a head that closes after some left signs and opens after others. That supports the "left frame conditions the terminal" lead and makes 220 a syntactic hinge, not a fixed ending.
- Cheapest next move: list the X-220 rows for X in 440, 032 and 000 with copy and site status. The 4-of-6 and 4-of-7 cells are small and need checking before they carry weight.

### 8. 220-455 and 220-065 are non-closing tails made of distinct texts
- What was seen: [my count] 220-455: 10 rows, 10 unique texts, closes 0 times; sites Mohenjo-daro 4, Harappa 3, Kalibangan 1, Dholavira 1, Karzakan 1; 7 of the 10 are SEAL:S. 220-065: 7 rows, 7 unique texts, closes 0 times; Mohenjo-daro 6, Kalibangan 1; all SEAL:S. The post-tail note lists 002-220-455 (4 rows) and 002-220-065 (3 rows), all still needing a source route.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; research/docs/archive/campaign_032_002_post_y_tail_family_campaign.md; research/docs/archive/campaign_a_220_x_strict_dedup_companion.md (002-220-455: 5 rows, 5 unique units).
- Old label: "branch-head candidate with a strong next-sign split" (tail-family note); "secondary compact candidate" (strict dedup note).
- Why it is alive: these tails carry no copy inflation. Seventeen distinct texts, none closing, on several sites, and they are not tied to 032 or 002. They are the cleanest branch evidence in the file by copy count.
- What it would mean if true: 220 takes two portable complement tails (455 and 065). That is a grammar-level branch that sits outside the 002 construction.
- Cheapest next move: search the CISI Pakistan volume on disk (evidence/tmp/cisi_pakistan_pages/cisi_pakistan.pdf) and the Mackay Chanhu-daro scan (evidence/tmp/chanhudaro_mackay_1943/chanhudaro_mackay_1943.pdf) for these texts' object numbers. That moves them from route-needed to route-checked.

### 9. 390-590 is the large 390 lane, and two blocked rows contain it beside 032
- What was seen: [my count] 390-590: 61 rows, 50 unique texts, closes at 590 in 8 rows; sites Mohenjo-daro 29, Harappa 22, Dholavira 4, Chanhu-daro 2, Allahdino, Kish, Gonur Depe and Unknown 1 each; types SEAL:S 43, TAB:B 16. Two blocked rows contain it: H-597 (+740-390-590-070-032-002-861+, 032 two signs after 590) and unknown-ID 3335.1 (+740-205-032-002-390-590-032+, 032 directly after 590).
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; research/docs/archive/campaign_032_002_source_normalized_branch_tail_admissibility.md (3335.1 blocked until object ID).
- Old label: "390 = branch head, 0 of 14 close after 002" (post-Y note). The 390-590 lane outside 002 was never measured. 3335.1 "blocked until object ID is resolved".
- Why it is alive: the branch-head claim for 390 rests on 14 rows, all after 002. The 390-590 lane has 61 rows and 50 distinct texts across eight sites or areas. Both rows that show 390-590 next to 032 are the ones the recursive-032 question needs.
- What it would mean if true: 390 is a complement-taking head whose complement is 590, and 032 returns as a delimiter inside the tail. That is the recursive-032 hypothesis, and it would tie the 032 slot to the 390 lane.
- Cheapest next move: pull the 61 rows; count rows where 032 follows 590 within two signs; check whether those rows share H-597's register.

### 10. 390-705 closes, and 705 closes often outside 002
- What was seen: [my count] 390-705: 2 rows, 2 unique texts (Mohenjo-daro and Dholavira); both end at 705. 705 occurs 176 times in clean rows and closes 48 times; its left neighbour is 033 in 89 rows (Mohenjo-daro 65, Harappa 18; types SEAL:S 39, TAB:C 20, TAB:B 15, SEAL:R 8). 033-706 occurs 42 times and closes 14 times.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; research/docs/archive/campaign_032_002_source_normalized_branch_tail_admissibility.md (M-1825 and Dholavira 4237.1 are the 390-705 rows; both blocked); research/docs/archive/deep_research_landscape_20260611.md (the Dholavira object and blocked-object list).
- Old label: "002-390-705 needs a route; one has no object ID" (admissibility note). The all-002 model never measured 705 outside 002.
- Why it is alive: a branch head (390) whose complement (705) closes is a two-step closure, not an open branch. 705 closes far more often than any branch sign, and it appears in a 033-705 frame that no campaign ran. 705 and 706 look like a pair, which could be a variant pair or two signs.
- What it would mean if true: 705 is a closing class sign outside the 002 construction, and 390 opens into it. The 033-705 frame is a second closing construction.
- Cheapest next move: compare 705 and 706 on the same signband in the Mohenjo-daro plates for the 033 rows. Fetch M-1825 once CISI 3.1 is available (see paid source).

### 11. 220-003 closes across four sites and several left signs
- What was seen: [my count] 220-003: 19 rows, 15 unique texts, closes at 003 in 10. Sites: Mohenjo-daro 11, Harappa 4, Kalibangan 2, Kish 1, Unknown 1. Types: SEAL:S 12, SEAL:R 3, TAB:B 3, TAB:C 1. Left signs in the notes: 740 (10 strict rows, 6 dedup units), 590 (4 rows) and 520 (singleton M-1912).
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; research/docs/archive/campaign_a_220_x_strict_dedup_companion.md; research/docs/archive/campaign_520_220_x_context_slot_nulls.md.
- Old label: "740-220-003 is the surviving 740 branch" (strict dedup note). The context-slot "closure" claim for X was retracted (context-slot nulls note).
- Why it is alive: 003 closes after 220 in three left frames and at Kish, which is outside the core sites. 415 closes only in Harappa-bound frames, and 032 only in the 240 frame. 003 is the one closer that does not need its frame.
- What it would mean if true: the 220 closing set splits into frame-bound closers (415, 032, 055) and one portable closer (003). That makes a useful test of the frame-selection story.
- Cheapest next move: put the 15 unique 220-003 texts in one table with left sign, site and type. Read closure share by left sign.

### 12. 032 hands off to branch heads directly, without 002
- What was seen: M-631 +520-033-706-240-220-032-368-263+ (032 followed by 368, which is a branch head in the 002 layer). M-1265 +740-055-240-220-032-806+ (032 followed by 806). M-22 +740-904-176-220-032-798-000[ (032 followed by 798, right end censored). In the nine strict 240-220-032 units: two close at 032, five go on to 002, and two go on without 002 (368 and 806).
- Where: research/docs/archive/campaign_a_220_x_240_selector_contrast.md (lists M-631 and M-1265 in the source queue); research/docs/archive/campaign_032_after_220_function.md (nine 240-220-032 units; 2 terminal, 5 to 002); research/docs/archive/damaged_boundary_fragment_closure_20260712.md (M-22 censoring).
- Old label: "002 = tail-lane operator" (campaign_032_002_tail.md). "368 = branch head, 0 of 11 close after 002" (post-Y note).
- Why it is alive: if the branch-head class follows 032 as well as 002, then 002 is one operator among several after 032, not the operator. That reading gives 032 its own set of heads.
- What it would mean if true: 032 is the branch slot. 002 is the operator used when the head is a closure-type sign, and 368 or 806 is used when it is a continuation head.
- Cheapest next move: list every 032 in the file followed by a sign other than 002, and tag each following sign by its post-Y class.

### 13. The 032 sign can be left out, and 240-220 takes at least four closers
- What was seen: M-1990 +740-760-440-240-220-002-861+ has 240-220-002-861 with no 032. The 240-220 controls take 032 (nine strict units), 002 (M-1990), 255 (M-133, +527-550-240-220-255-812-906-388+) and 415 (M-369, +740-690-435-255-240-220-415-806-742-060-920+).
- Where: research/docs/archive/campaign_a_220_x_240_selector_contrast.md (internal controls); research/docs/archive/campaign_032_after_220_function.md (controls M-1990, M-133, M-369).
- Old label: "mandatory internal controls" (240 selector note). Not analyzed.
- Why it is alive: if 032 can be left out before 002, the lane is 240-220 plus a tail, and 032 marks one subtype among several.
- What it would mean if true: 240-220 is a frame that takes at least four different closers. The 032 choice is one option, not the frame's identity.
- Cheapest next move: compare M-1990 (240-220-002-861) with the nine 240-220-032-002 rows on shared tail, site and type. That one comparison decides whether 032 is removable.

### 14. The 817/820/861 closure split is the most-tested structural number in the file, and it passed the nulls
- What was seen: [my count, from the post-Y file] strict dedup closes: 861 95 of 119, 817 100 of 103, 820 66 of 71, 390 0 of 14, 368 0 of 11, 031 0 of 9, 220 0 of 9, 824 6 of 6, and singletons 297, 405, 595 and 900 at 0 of 4 each. These match the note exactly. From the notes: leave-one-out accuracy of the Y-class predictor 0.885772 against site/type/symbol 0.579158 (499 rows); post-hoc partition forger best z 13.21 with zero false-positive rate across six null models at 10,000 iterations each; removing Mohenjo-daro SEAL:S leaves 0.884298 against 0.611570.
- Where: research/data/open_prototype/reports/campaign_032_002_post_y_all_002_rows.csv (recounted); research/data/open_prototype/reports/campaign_032_002_y_posthoc_partition_forger_summary.json; research/docs/archive/campaign_032_002_y_matched_terminality.md; research/docs/archive/campaign_032_002_y_skeptic_holdout.md.
- Old label: "structural candidate, not accepted; awaiting a source-normalized holdout" (skeptic note). The "closure/branch" grammar is recorded as accepted only at the corpus layer.
- Why it is alive: no other structural claim in the file has this null record. It held after register removal, family blocking and post-hoc partition. The counter, once: the adjacent 032-002 subset fails the post-hoc partition forger (best z 1.526, false-positive rate 0.5205 for z and 0.7552 for gap).
- What it would mean if true: 817, 820 and 861 form a closure class, and 390, 368, 031, 220, 297, 405, 595 and 900 form a branch class. That is a grammar-level split with no register cause.
- Cheapest next move: the length-matched test the post-Y note asked for and nobody ran. Within each text-length bucket, compare how often closure-class Y (817, 820, 861) is the last sign with how often other Y signs are. The skeptic note's exact text-length plus 002-position match is a tautology and was scored as failed, so this test has not been run.

### 15. 861 closes after 032-002 at three sites, with more than one left frame
- What was seen: [my count] 032-002-861: 11 rows, 10 unique texts, closes at 861 in 9. Sites: Mohenjo-daro 6, Harappa 3, Chanhu-daro 2. All 11 are SEAL:S. Left frames: 241-220 (H-444), 520-220 (M-1044), 692 (M-21), 176 (C-60), 390-590-070 (H-597), with C-65 at Chanhu-daro unreadable. The two continuing rows are M-240 (861-603) and M-91 (861-255-416).
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; research/docs/archive/campaign_032_002_y_source_function_batch2.md (M-21, H-597 row-level); research/docs/archive/campaign_032_002_y_source_function_batch3_chanhudaro.md (C-60 row-level).
- Old label: "the most portable branch" (campaign_032_002_y_branch_model.md).
- Why it is alive: 861 closes after 032-002 in frames that have no 220 at all (692-032, 176-032, 070-032). The A-220 frame is one route into the closure, not the only one.
- What it would mean if true: 032-002-861 is a site-independent closing formula. A-220 is a second entry route.
- Cheapest next move: before counting three sites as three witnesses, check whether C-60 and H-597 come from one plate family. All 11 are seals, so the portability is seal-type portability.

### 16. Two censored 002-861 objects show a closed edge after 861 on the object itself
- What was seen: M-19 (lipi row ]000-000-002-861+; CISI PDF 49, print 13) and M-175 (]002-861+; CISI PDF 87, print 51). The damaged-boundary note records the closed edge after 861 as intact on both objects. Both have an unbounded broken prefix, so they are left-censored; M-175's 002 is damaged and uncertain.
- Where: research/docs/archive/damaged_boundary_fragment_closure_20260712.md; panels research/data/sign_crosswalk/source_panels/damaged_boundary_fragment_closure/M-19_A_a_CISI1_pdf49_print13.png and M-175_A_a_CISI1_pdf87_print51.png.
- Old label: "left-censored bare terminal 002-861 suffixes; not complete two-sign texts" (damaged-boundary note).
- Why it is alive: this is physical evidence that 861 is final on the object. The strict dedup table infers closure from catalogue order. The note wants these two admitted, and states that the next calculation needs no new GPU run.
- What it would mean if true: the 861 closure is seen on the object for at least two cases, which moves 861 from catalogue-order terminal toward physically terminal.
- Cheapest next move: run the bare-versus-tailed 002-861 contrast with M-19 and M-175 added, as the damaged-boundary note specifies. Not yet run.

### 17. 861-603 and 861-533-717 close every time they occur, all at Mohenjo-daro
- What was seen: [my count] 861-603: 3 rows, 3 unique texts, all Mohenjo-daro, all close at 603. 861-533-717: 2 rows, both Mohenjo-daro, both close at 717. The completion matrix records the accepted structural finding as 533-717 being the only restricted terminal tail after 002-861, with worst false-positive rate 0.006 and M-376 and M-391 source-visible as same-line terminal-side material.
- Where: research/docs/archive/completion_gap_matrix.md (accepted row, accepted_struct_002_861_533_717_restricted_tail_2026_05_29); research/data/open_prototype/lipi/metadata_filtered.csv.
- Old label: the accepted structural finding (completion matrix). Under the AGENTS rules this verdict is void. Its numbers are quoted here.
- Why it is alive: this is the only accepted structural item in the file and it passed the matched-negative forgers. Its own boundary is the strongest counter: a broad any-prefix search finds 96 repeated terminal bigram cells in strict raw rows and 40 after exact dedup, so the finding holds only for the fixed prefix.
- What it would mean if true: 533-717 is a closing two-sign tail, and the 861 closure has a licensed continuation family.
- Cheapest next move: search the clean rows for 533 and 717 at sites outside Mohenjo-daro. Both witnesses are Mohenjo-daro, so the result has no cross-site check yet.

### 18. 817 and 861 may be one sign with a second element
- What was seen: the token-box scaffold and the Wells/Mayig crosswalk place 817 and 861 in one leaf-or-diamond family (P385 and M267 in the provisional crosswalk; W817 and W861 in Wells). Their terminal rates differ: 817 closes 100 of 103, 861 closes 95 of 119. The repeated tails (603 three times, 533-717 twice, 255-416 once) all come after 861, never after 817.
- Where: research/data/open_prototype/reports/campaign_032_002_y_token_box_scaffold_v1.csv; research/docs/archive/campaign_032_002_y_branch_model.md (hypothesis H5, allograph); research/docs/archive/campaign_032_002_post_y_tail_family_campaign.md.
- Old label: "allograph hypothesis, not tested" (branch model H5). "817/861 are provisional crosswalk pressure" (campaign_032_002_context_branch_campaign.md).
- Why it is alive: if 861 is 817 with a stroke, every 861 tail is a segmentation problem and the leakiness of 861 is a counting artifact. M-12 (below) is the same kind of problem, a visual unit count that disagrees with the catalogue.
- What it would mean if true: the closure class is one sign with two physical variants, and the 817/861 split is a variant effect, not grammar. That would merge two Y values.
- Counter: the 603 and 533-717 tails recur across objects, which argues for a sign, not a stroke.
- Cheapest next move: pick one plate or signband with both an 817 and an 861 and box them side by side. Count the strokes in each.

### 19. M-12 has ten visual units against nine catalogue tokens
- What was seen: three blind reviewers each counted 10 units on M-12 (blind ID BG001) against 9 in both catalogue witnesses (lipi:2540.1 and mayig:M-12A). On the same packet's false-positive control, M-654 (BG009), reviewers counted 6 against a catalogue 4, a stable overcount in 1 of 6 controls.
- Where: research/data/open_prototype/reports/campaign_m12_token_count_audit_summary.json (on disk); research/docs/archive/campaign_m12_token_count_audit.md.
- Old label: "ambiguity lead only; not a catalogue correction" (M-12 audit).
- Why it is alive: the note calls the two catalogue witnesses independent. Nothing in the note shows that. If both copy one transcription, the 9 is one witness against three reviewers' 10.
- What it would mean if true: the catalogue undercounts one sign in M-12, and a 10-unit seal sits in the set the rest of the file treats as 9-unit.
- Cheapest next move: check whether lipi:2540.1 and mayig:M-12A cite the same publication page. Then box the 10th unit on the M-12 plate.

### 20. Stored order beats reversed order in 130 of 137 multi-sign rows
- What was seen: the clean Mohenjo-daro SEAL:S subset (138 rows, 748 tokens, 191 numeric signs): stored order beats reversed in 130 of 137 multi-sign rows (4 reversed, 3 ties). By length: 1 to 3 signs 21 of 24; 4 to 5 signs 47 of 50; 6 to 8 signs 54 of 55; 9 or more 8 of 8. With 740 and 002 removed: 114 of 134 (12 reversed). The completion matrix quotes a stored-win share of 0.841096 (harsh top-edge removal) and 0.805714 after source-convention collapse.
- Where: research/docs/archive/direction_order_baseline.md; research/docs/archive/effective_unicity_directionality_blind_packet.md; research/docs/archive/completion_gap_matrix.md.
- Old label: "passes the first structural-order gate" (direction-order note); "strongest current candidate, narrowed by adversarial comparator and source-validation failure" (completion matrix).
- Why it is alive: the effect holds on the sign-count control and on rows with 740 and 002 removed, and random row-orientation flips remove it, as they should. It is the most replicated structural number on a single-site subset.
- Counter, once: Pictish and barn-star corpora exceed the Indus masked top-1 (completion matrix), so masked predictability is not writing-specific.
- What it would mean if true: stored order is physical (right-to-left) for most rows, so catalogue order can serve direction-dependent analysis.
- Cheapest next move: list the 4 reversed rows and the 3 ties and check their physical direction on the CISI plates. Those rows test the direction rule directly.

### 21. Masked-sign prediction has a known-script number to beat
- What was seen: Linear B Series D (first 513 clean sequences): bidirectional top-1 0.470200 on all clean rows, 0.435897 after an 8-sign length cap, and 0.294347 on the source-gapped missing-sign test (quoted in the comparator note). Indus, Mohenjo-daro SEAL:S clean subset (748 masked tokens): bidirectional top-1 0.283422; terminal exact-sign top-1 0.043796 (direction-order note). Vector 2 layer: masked top-1 0.279591 (completion matrix).
- Where: research/docs/archive/comparator_benchmark_design.md; research/docs/archive/linear_b_series_d_scarcity_baseline.md; research/data/open_prototype/known_scripts/linear_b_series_d (on disk, not read).
- Old label: "masked prediction is beaten by admin and emblem generators, so not a standalone diagnostic" (lipi structured null comparator, named in the comparator note).
- Why it is alive: the protocols differ (Indus numeric signs against Linear B sign tokens), so the gap is not a result. The Linear B gapped setting exists, and Indus can be run on the same protocol.
- What it would mean if true: Indus signs are predictable at roughly the level of a deciphered administrative script, which places Indus with the administrative class.
- Cheapest next move: run Indus under the Linear B source-gapped sequence-leave-one-out protocol and report the number next to 0.294347.

### 22. The fish-square phonetic key has no chance-level null
- What was seen: four phonological configurations scored 62/166, 59/166, 54/166 and 57/166 training dictionary matches, and 3/36, 4/36, 3/36 and 4/36 held (decoding note, section 1). Whole-inscription runs: 54/146 and 48/149 training, 4/56 and 7/49 held.
- Where: research/docs/archive/decoding_followup_20260907.md; research/data/decoding_followup_20260907/summary.json.
- Old label: "dictionary matches are not translated inscriptions or correct pronunciations" (decoding note). No phonetic claim accepted.
- Why it is alive: the held matches (8 to 11 percent) were never set against a null key. The note says selection used training score only, so the held set is a clean check on this point, and it was not run as one.
- What it would mean if true: the roof and surround marks change vowel quality or quantity, so the square is a spelling system with sound values.
- Cheapest next move: permutation null. Shuffle which onset each fish base receives, 10,000 times, recompute held dictionary matches, and report the share at or above 3 or 4 of 36.

### 23. A two-sign spelling and one sign may alternate in one construction
- What was seen: 51-130-15 and 51-130-149-342 (Mahadevan sign numbers). Compact witnesses: 2549:0, 4649:10. Expanded witnesses: 1013:0, 1619:10, 2091:0. With 176 added: compact 4447:20, 4478:20, 4480:20, 4577:10, 4579:10; expanded 4666:10.
- Where: research/docs/archive/decoding_followup_20260907.md (section 2); research/data/mahadevan_20260905/concordance_rows.csv (frozen Mahadevan concordance on disk).
- Old label: "candidate for mixed full and compressed notation; scholarly priority not established; not decoded" (decoding note).
- Why it is alive: sign 15 is drawn as a jar-headed carrier and sign 342 as a jar, so 149 plus 342 can spell the carrier's construction. The alternation runs across eight witnesses in one construction.
- Counter, once: the compact and expanded pairs share the 51 130 construction and differ only by 176, so the evidence is one construction seen twice, not two independent confirmations.
- What it would mean if true: a logogram and a two-sign spelling alternate, which is a ligature-type or logographic-plus-phonetic writing practice outside the fish family.
- Cheapest next move: in the Mahadevan concordance rows, confirm each witness's object and construction. Check whether Lipi numbering matches these Mahadevan numbers for 15, 149 and 342.

### 24. Brahmi near-miss 817 = dhya has had no rescue attempt
- What was seen: the Brahmi v2 near-miss set: 817=dhya, 527=ra, 472=ra, 060=ka, 061=ra. Shape and label nulls failed. The v3 gate blocked all 83 families (it requires at least three unique token hashes, three unique CISIs, three unique source paths, unanimous duplicate collapse, unchanged label, and nulls at or below 0.01). The real-token autopsy: 21 rows with low impostor share; all 21 fail the shape threshold, 19 fail the label threshold, 11 fail source independence, none pass both.
- Where: research/docs/archive/brahmi_source_token_descent_gate_v2.md; research/docs/archive/brahmi_independent_source_token_gate_v3.md; research/docs/archive/brahmi_real_token_low_null_reaudit_20260531.md; research/docs/archive/completion_gap_matrix.md.
- Old label: "rejected; all 83 failed; accepted anchors 0" and "v3 blocks every family before review".
- Why it is alive: 817 is the hard closure (100 of 103 close). A dhya reading gives the strongest closing sign a syllable value. AGENTS rule 5 requires two honestly different rescue attempts before a broken reading is paused. None is recorded.
- What it would mean if true: the hard closure has a syllable value, and the closure class has a phonetic face.
- Cheapest next move: rescue 1, rerun the shape null for 817 with 861 folded in (both sit in P385 and M267). Rescue 2, the same rerun with an independence threshold set from the 817 token count rather than the global rule. No new source needed.

### 25. The Ur seal U17649 mapping puts 415 on the closing slot of the 520-220-415 formula
- What was seen: the proposed Gadd Ur mapping for U17649 (3898.1) is 002=ur, 004=gun3, 328=a, 001=me, 803=luh, 415=ha. The cuneiform phrase "ur gun3-a me-luh-ha" has six syllables, and the mapping covers six signs. 415 is the closing sign of the 17 exact +520-220-415+ rows.
- Where: research/docs/archive/completion_gap_matrix.md (object-level onomastic harness); research/docs/archive/gadd_ur_accession_bridge_audit.md.
- Old label: "rejected: U17649 is Indus-only and the cuneiform is a separate text; same-site shuffled nulls reproduce the pattern at 0.6857."
- Why it is alive: a null that reproduces the pattern 68.6 percent of the time has almost no power to reject, so the rejection says the test was too weak, not that the mapping is wrong. The six-sign match and the 415 ending link an Ur seal to the most frequent closing formula.
- What it would mean if true: 520-220-415 is a name-type formula ending in -ha, which gives the title or name reading an object-level link.
- Cheapest next move: check whether U17649's Indus string is six signs and ends in 415. That is one lookup in the Gadd bridge data.

### 26. The contact-anchor lane has three image routes
- What was seen: Louvre AO 22310, the Shu-ilishu cylinder seal, whose cuneiform names its owner an interpreter of the Meluhhan language (about 2020 BCE; a contact anchor, not a bilingual). BM 120573: a steatite stamp seal from Diqdiqqah (Ur), excavation no. U.7683, with a doubtful Gadd reading. The Meluhha CDLI query leaves 19 cuneiform phrases and 23 query and site bridge rows (completion matrix).
- Where: research/docs/archive/external_anchor_shu_ilishu_AO22310_candidate_20260611.md; research/docs/archive/deep_research_landscape_20260611.md; research/docs/archive/completion_gap_matrix.md.
- Old label: "external anchors 0; contact anchor only" (deep research note). Lu-Sunzida retracted at false-positive rate 0.933 to 0.994.
- Why it is alive: the Louvre seal names the Meluhhan language in an Akkadian-period text, which is the only person-level link in the file. The Ur seals carry Indus sequences found in Mesopotamia, which is an object-level link.
- What it would mean if true: a dated Mesopotamian witness that Meluhha was a language label, which ties the Indus sign inventory to named Akkadian-period people.
- Cheapest next move: obtain the Penn Museum Expedition image of the Shu-ilishu seal (Wikimedia is blocked in this environment, per the deep-research run). Read its wording against the 19 surviving phrases.

---

## Sources on disk

- research/data/open_prototype/lipi/metadata_filtered.csv: 5,679-row filtered Lipi metadata (T3). Quarantined columns not read.
- research/data/open_prototype/reports/campaign_032_002_post_y_all_002_rows.csv: 813 all-002 rows; strict dedup gives 499 (my recount matches the notes).
- research/data/open_prototype/reports/campaign_032_002_post_y_tail_family_instances.csv: 207 continuing post-Y instances.
- research/data/open_prototype/reports/campaign_032_002_post_y_branch_rows.csv: 50 adjacent 032-002 rows.
- research/data/open_prototype/reports/campaign_032_002_y_source_function_current_table.csv: source-visible row table (not opened).
- research/data/open_prototype/reports/campaign_032_002_y_token_box_scaffold_v1.csv: provisional token boxes (not opened).
- research/data/open_prototype/reports/campaign_exact3_formula_counts.csv: exact three-sign counts.
- research/data/open_prototype/reports/campaign_032_002_tail_units.csv and campaign_032_002_tail_strict_rows.csv: 032 tail units (not opened).
- research/data/open_prototype/reports/campaign_a_220_x_strict_dedup_units.csv: A-220-X dedup units (not opened).
- research/data/open_prototype/reports/campaign_032_002_y_posthoc_partition_forger_summary.json and campaign_520_220_x_context_slot_null_summary.json: null summaries.
- research/data/open_prototype/reports/campaign_m12_token_count_audit_summary.json: M-12 audit.
- research/data/mahadevan_20260905/: frozen Mahadevan concordance (concordance_rows.csv, concordance_documents.json.gz, paired_objects.json, front_families.json, four_by_three_grid.json, README.md). Only the README and the file names were checked.
- research/data/decoding_followup_20260907/summary.json: fish-square and counter packet summary.
- research/data/sign_crosswalk/source_panels/damaged_boundary_fragment_closure/: four CISI panels (M-19, M-22, M-39, M-175) as PNG.
- research/data/open_prototype/mayig/: Mayig digitization audit files (audit_summary.json, records_index.csv, tree_manifest.csv; not read).
- research/data/open_prototype/known_scripts/linear_b_series_d and sumtablets; research/data/open_prototype/nonlinguistic/sproat2014: comparator data (not read).
- research/data/claim_ledger/claims.json: claim ledger (not read).
- evidence/tmp/cisi_pakistan_pages/cisi_pakistan.pdf: CISI Pakistan volume pages (not opened).
- evidence/tmp/chanhudaro_mackay_1943/chanhudaro_mackay_1943.pdf: Mackay 1943 Chanhu-daro scan (not opened).
- evidence/tmp/032_002_861_603_slot_source_normalization/vats_excavations_at_harappa_vol2.pdf and vats_excavations_at_harappa_vol2_plates.pdf: Vats vol. II and plates (not opened).
- evidence/tmp/032_002_y_source_function_batch/ and related crop folders: the notes' tmp/ crop paths resolve here, since the repo root has no tmp/ folder.
- evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/dev-tools/ashtadhyayi/assets/mw.xml: Monier-Williams dictionary used by the fish-square test (not read).
- research/docs/archive/: the 38 files on the reading list, plus named notes not on the list: external_anchor_shu_ilishu_AO22310_candidate_20260611.md, gadd_ur_accession_bridge_audit.md, source_route_updates_20260611.md, lipi_structured_null_comparator.md, sign_crosswalk_audit.md, and the lipi_034_* and lipi_frame700_034_* gate notes (not read).

## Ideas named but never run

- Length-matched closure test for the 817/820/861 split (entry 14; post-Y note step H3; skeptic note's replacement never done).
- Bare-versus-tailed 002-861 contrast with M-19 and M-175 added (damaged-boundary note; "needs no new GPU run").
- Minimal-pair branch test: closure-family and branch-family Y alternating in matched frames (post-Y note step 2).
- Permutation null for the fish-square phonetic key (decoding note; held matches never tested against chance).
- Indus under the Linear B source-gapped protocol (comparator design note).
- SumTablets administrative comparator with transliterations hidden and the Hugging Face revision pinned (comparator design note).
- Coptic SCRIPTORIUM continuity comparator as an upper bound (comparator design note).
- Nair 2026 scorecard (arXiv 2604.17828) on the same ICIT/Yajnadevam corpus: reported 1,916 deduplicated inscriptions, 584 unique signs, 11,110 tokens (deep research note). Code is "on request" per that note. Email to the authors is for Cúper to send.
- Mukhopadhyay 2023 administrative semasiography (nature.com s41599-023-02320-7, quoted in the deep research note): test whether tablet classes carry different formula families from seals. Not run.
- CISI volume 3.2 and 3.3 "untraced objects" strand for 3335.1 (deep research note). Not checked.
- indusscript.in export path check (corpus acquisition protocol). Not run.
- ICIT database access request (corpus acquisition protocol names the administrator's address). Draft only; Cúper sends.
- Gulf and Ur bridge queue: Kjaerum Failaka cat. 279 and 319; Mitchell 1986 Ur figures 106 to 117; Amiet Susa 1643; Sarzec and Heuzey Girsu plate 30.3a-b (Gulf Type Indus queue, completion matrix). Not acquired.
- Meluhha surviving-phrase set: 19 cuneiform context leads, 23 query and site bridge rows, 4 Ur, Susa and Failaka focus rows, 8 same-site length matches (completion matrix). Not run past the first pass.
- Source-image routes for M-240 (HR 4098324), M-1044 (HR 4399551), M-1728 (DK-E 1585079), M-1677 (DK11358130) (admissibility and route notes). Archive images not obtained.
- Harappa TAB:I copy-family audit: map every copy of the top TAB:I texts to excavation numbers (entries 5 and 4).
- Tablet versus seal split for every formula family, using the sides and type fields in the metadata (entries 3 and 4). Not run.
- Dholavira 8758 and 4237.1 source routes (deep research note). Blocked.
- Lipi 034 and frame700 allograph gates (research/docs/archive/lipi_034_*.md, lipi_frame700_034_*.md): read by their authors, not by me.
