# Leads from reader 08

Reader id: 08. Reading list: `sweep/chunks/chunk_08`, 39 files in `research/docs/archive/` (all read in full, start to finish).

Read outside the chunk, because the chunk files name them as the evidence behind their verdicts: the three stroke-run gates `research/docs/archive/m010_five_stroke_run_segmentation_gate_20260712.md`, `m020_six_stroke_run_segmentation_gate_20260712.md`, `m072_five_stroke_run_segmentation_gate_20260712.md`; `research/data/sign_crosswalk/artifact_witnesses.csv`; and the stored panel images for M-32 A and M-20 A/a. The visual counts I give below are mine, made by eye on those stored images. They are not blind counts and they are one panel each.

Terms used below. A Lipi code is a three-digit sign number from our numeric catalogue (e.g. `034`). A Mayig code is a `P` number from the Parpola-style catalogue (e.g. `P123`). A token is one code in a row. A run is a set of adjacent identical strokes. Paid source: see the last section (CISI 3.1).

---

### Numeric codes look like stroke counts: 002 = two, 003 = three, 005 = five, and 032 + 033 split a five-stroke run
- What was seen: M-10 is a five-stroke run that Lipi writes as `032 033` and Mayig writes as one `P151`. The gate says Lipi's neighbourhoods make `032` the two-stroke member and `033` the three-stroke member (2 + 3 = 5). M-72 is a five-stroke run written by Lipi as `003 002` (3 + 2 = 5) and by Mayig as one `P125`. The gate says Mayig's feature metadata describes "the three-stroke and two-stroke neighborhoods represented by `P123/W003` and `P122/W002`", so Mayig gives the same counts on its own. Alignments in the files: `156 003` and `154 003` line up with `P004 P123` (M-80, M-93, M-132, M-102); `156 004` lines up with `P004 P124` (M-96); on M-20, position 2 is `005` over `P125` and position 3 is `002` over `P122`. My own count on the stored M-32 A panel (`research/data/sign_crosswalk/source_panels/390_P086_merge/M-32_A_CISI1_pdf53_print17.png`, Lipi `390 003 002 817`): the group the code `003` sits on reads as three strokes, and the short pair the code `002` sits on reads as two.
- Where: `research/docs/archive/m010_five_stroke_run_segmentation_gate_20260712.md`; `.../m072_five_stroke_run_segmentation_gate_20260712.md`; `.../m020_six_stroke_run_segmentation_gate_20260712.md`; `research/docs/archive/lipi_154_156_comparanda_packet.md` (alignment table); `research/data/sign_crosswalk/artifact_witnesses.csv` (rows `lipi:2539.1` M-10, `lipi:2600.1` M-72, `lipi:2548.1` M-20); the 390 panel set in `research/data/sign_crosswalk/source_panels/390_P086_merge/`.
- Old label: each gate calls its count split "atomicity unresolved" and refuses to take either tokenisation as the sign-unit count. None of the gates connects the number on the code to the number of strokes it sits on.
- Why it is alive: both five-stroke objects sum exactly to five with the two codes' stroke counts. Mayig's own metadata gives W002 = two and W003 = three strokes, and the code `002` aligns to `P122` in M-20 with `005` aligned to `P125` (five strokes per the M-10 and M-72 gates). Every alignment in the files that carries a stroke count agrees with the code number. The one contrary number is M-20's six-stroke run, which is one Lipi token (`036`), not a 00N or 03N pair. That is a counterexample to "the code is always a count token", and the rule has to cover it (see entry on `036`).
- What it would mean if true: the stroke-bundle codes are a stroke-count notation. For these signs that makes a number slot, the first number candidate the project has, and it means the 00N series (002, 003, 004, 005) and the 03N series (032, 033, 034, 036) are two count series, each reading as N strokes.
- Cheapest next move: count strokes blind (labels hidden, grade strokes only) on 8 to 10 stored panels for each of codes 002, 003, 004, 005 and for 032, 033, 036, using the CISI plates already on disk. If the counts match the codes, write it into MAP.md as a measured line.

### 036 is one token for six strokes on M-20
- What was seen: M-20's row is `+390-005-002-861-036-460-513+` (7 tokens). Its six full-height strokes sit after the diamond `861` and before the three-triangle form, and the gate says Lipi writes them as one `036`. Mayig writes them as two `P147`, and the gate states "Mayig defines each P147 as three adjacent full-height vertical strokes" (so 3 + 3 = 6). Under the 03N = N reading from entry 1, `036` = six.
- Where: `research/docs/archive/m020_six_stroke_run_segmentation_gate_20260712.md`; `research/data/sign_crosswalk/artifact_witnesses.csv` row `lipi:2548.1`; panel `research/data/sign_crosswalk/source_panels/m020_six_stroke_run_segmentation/M-20_A_a_CISI1_pdf49_print13.png`.
- Old label: gate closes the duplication branch and says "do not accept a general `036 = P147 P147` rule."
- Why it is alive: the 03N series is the only family in the files where a single code has a count of six that is written as one token on a plate that shows six strokes. Denying a general rule is correct for `036 = P147 P147`, but the rule being tested is different: the code number is the stroke count. The M-20 gate never tested that.
- What it would mean if true: 036 means six strokes. Lipi writes a six-run as one count token and Mayig writes it as two three-stroke units. That is the first direct count-to-token pair in the corpus.
- Cheapest next move: find every other row in the metadata layer that carries 036 or 035 and check the plate for the stroke count. I did not find a 035 in the files I read.

### 034 may be four strokes, not three. Parpola's count and the blind sort disagree, and that disagreement is the split to test
- What was seen: the M-2104 notes say the raw plate (IA leaf 48270_0205, Marshall Plate CXIV no. 532) shows "3 secure adjacent strokes + possible fourth/boundary mark", and the team reads it "three-vs-four ambiguous". Parpola's text no. 12 reads `UIII` ("three pots") for M-2104 and `UIIII` for M-478/M-480/M-1425 ("four pots"). In the M-315 blind sort (`research/docs/archive/lipi_034_m315_blind_390x002_sort.md`), the M-315 upper face "clusters with M-984 004 across all strict blind reviewers", which is a four-stroke control on the same frame. The lower M-315 witness does not join that cluster.
- Where: `research/docs/archive/lipi_034_m2104_marshall532_visual_adjudication.md`; `.../lipi_034_m2104_marshall_vol3_cxiv_source_adjudication.md`; `.../lipi_034_m2104_parpola_extraction.md`; `.../lipi_034_m315_blind_390x002_sort.md`; `.../lipi_034_m315_second_slot_decision_gate.md`; `.../lipi_034_post_m315_reprioritization.md`.
- Old label: "exact 034 = three = failed at current public-source resolution" (the M-2104 gate); M-315 "fails the current blind upgrade gate" with "upper-witness 004-pressure".
- Why it is alive: the 034/004 pair sits in the same frame twice (`097-700-034` vs `097-700-004`; `390-034-002` vs `390-004-002`). Under the 03N = N and 00N = N reading (entry 1), 034 and 004 are two codes for the same count of four, the same way `033` and `003` are two codes for three, and `032` and `002` are two codes for two. That makes the M-315 upper-face result an expected outcome, not a failure, and it gives the M-2104 "possible fourth" a reading. Parpola's `UIII` is the one count it contradicts.
- What it would mean if true: the M-2104 pot-count cluster (`700-034`) is four pots, the same count as its tablet parallels (`700-004`), and the difference between them is a shape allograph, not a count. Parpola's `UIII` is a miscount or a three-stroke-plus-boundary reading. That also explains the reason the local rows never separated 034 from 004 by count.
- Cheapest next move: blind-count the strokes of the 034 cluster on both M-315 witnesses (CISI 1 p. 78, IA leaf `n113`) and on the M-2104 plate. Also count the 033 and 032 clusters on the calibration panels H-789 B and H-930 B (entry 13). Each count is a single split: if M-315 upper reads three, the four-stroke reading is dead; if it reads four, the Parpola count is the one in question.

### The Marshall "five characters" for no. 532 reconciles with three different counts; the image picks one
- What was seen: Marshall describes no. 532 as having five deeply incised characters. The local row has four tokens (`151 097 700 034`). The M-2104 gates call this "the central segmentation warning" and leave it open. Three counts put the components at five: (a) `151` and `097` read as one joined unit, plus `700` (U), plus three strokes (`034` = 3): 1 + 1 + 3 = 5; (b) `700` (U) plus four strokes (`034` = 4): 1 + 4 = 5; (c) `151`, `097`, `700` as three characters plus two strokes: 3 + 2 = 5. The 034-as-three and 034-as-four readings both fit the five, depending on how `151-097` is counted.
- Where: `research/docs/archive/lipi_034_m2104_raw_source_alias_route.md`; `.../lipi_034_m2104_marshall532_visual_adjudication.md`; `.../lipi_034_m2104_marshall_vol3_cxiv_source_adjudication.md`.
- Old label: "Marshall's five-character note can be ignored: Fail." Then "a live warning."
- Why it is alive: the warning is treated as a blocker. It is a counting problem that the plate can settle, and each of the three counts predicts a different visible shape at no. 532.
- What it would mean if true: whichever count fits the plate also fixes the count of 034, and so the stroke notation in entry 1.
- Cheapest next move: on the no. 532 crop, mark the lead glyph and check whether the first two incised marks are one joined sign. Count the strokes after the U. Compare to the three counts above.

### M-20's early five-stroke and two-stroke runs were never examined, only the six-stroke run
- What was seen: by position, Lipi `005` sits over Mayig `P125` (five strokes per the M-72 gate) and Lipi `002` over `P122` (two strokes per Mayig's W002) on M-20, before the diamond `861`/`P385`. The gate examines only the six-stroke run after the diamond. The stored plate (M-20 A and a) shows a multi-stroke group on the left of the diamond and a second group on the right. I did not secure a count on either by eye.
- Where: `research/docs/archive/m020_six_stroke_run_segmentation_gate_20260712.md`; `research/data/sign_crosswalk/artifact_witnesses.csv` row `lipi:2548.1` and `mayig:M-20A`; panel `.../source_panels/m020_six_stroke_run_segmentation/M-20_A_a_CISI1_pdf49_print13.png`.
- Old label: none. The gate never mentions the early runs.
- Why it is alive: if the two early runs exist as a five-run plus a two-run, M-20 would show `005 002` = five and two on the plate, which is the same two-count pattern as the M-72 split. That would be a second independent object with the 00N codes matched to counts.
- What it would mean if true: M-20 has three count groups (5, 2, 6) on one seal, and the count notation holds across the object.
- Cheapest next move: count the group left of the diamond on M-20 A and a, one stroke at a time, with the labels hidden.

### The 390-merge's stated reason ("feature-preserving") fails for 405 vs 407
- What was seen: the 390/405/406/407 to P086 gate (`research/docs/archive/lipi_390_405_406_407_mayig_p086_merge_gate_20260712.md`) accepts the merge because "Mayig keeps the visible distinctions in feature fields." Its own panel table gives feature tails: M-34 (Lipi 405) `[2,3,2,0]`; M-170 (406) `[2,3,1,0]`; M-171 (407) `[2,3,2,1]`; M-172 (405) `[2,3,2,1]`. M-171 (407) and M-172 (405) have identical feature tails and different Lipi codes.
- Where: the 390/P086 gate file above; panel manifest `research/data/sign_crosswalk/source_panels/390_P086_merge/manifest.csv`.
- Old label: "accepted for analysis only in a feature-preserving Mayig lane."
- Why it is alive: the stated reason for the merge is a feature that separates the members. For 405 vs 407 it does not separate them in the pinned data. Either Lipi's 405/407 split is noise or Mayig's features are too coarse for the pair. Both possibilities are testable with the existing panels.
- What it would mean if true: the four-member merge is a three-member merge (390/406 separate, 405 and 407 indistinct), and the feature-preservation rule needs a counterexample clause.
- Cheapest next move: pull the Mayig feature rows for the two M-34 and M-172 panels and look for any field that differs; if none, record 405 vs 407 as a Lipi-only split.

### 154 and 156 are both Mayig P004 with the same 003, so H-2237's contrast looks like a shape allograph of one sign, not a count
- What was seen: the 154/156 packet gives `M-102 154 003 -> P004 P123`, `M-80 156 003 -> P004 P123`, `M-93 156 003 -> P004 P123`, `M-132 156 003 -> P004 P123`. So in every alignment both 154 and 156 land on `P004`, and the trailing `003` lands on `P123` (three strokes, per entry 1). H-2237 (`154-003`) vs H-2233 (`156-003`) therefore differ only in the first code, which Mayig treats as one sign.
- Where: `research/docs/archive/lipi_154_156_comparanda_packet.md`.
- Old label: "allograph/crosswalk collapse: active competing explanation." "Alive but source-gated."
- Why it is alive: the alignments show the two codes sit in one Mayig slot with the same count next to them. That is the allograph result the packet predicted, and it is now measured.
- What it would mean if true: the H-series "majority" (21 rows) is one sign pattern, and H-2237 is a shape variant of the same pot sign. The H-2237 lead is closed as a count difference and open as a shape difference.
- Cheapest next move: check the Mayig `P004` feature file for a shape field that could split 154 from 156, then look at H-2237 vs H-2233 panels.

### The 520-220-X frame has four terminal codes across five objects, and the H-789 companion row joins the 034 line
- What was seen: `M-1912 +520-220-003+`, `M-1206 +520-220-034+`, `M-37 +520-220-415+` (from the reprioritization file), `M-715 +520-220-016-741-556-000[` (Parpola conflict row), and H-789's longer companion `+400-520-220-016+` (calibration file). So the frame `520-220` carries terminal codes 003, 016, 034 and 415. H-789 is a 033 control. Its long row joins the frame that carries the 034 target M-1206.
- Where: `research/docs/archive/lipi_034_post_m315_reprioritization.md`; `research/docs/archive/lipi_034_m2104_parpola_extraction.md` (M-715); `research/docs/archive/lipi_frame700_034_clean_two_panel_close_read.md` (H-789).
- Old label: none for the frame as a whole. The M-1206/M-37 pair was treated as the "naive terminal-substitution story" that weakened.
- Why it is alive: one frame, four terminal codes, five objects, all from two sites. A frame with a stable front and a variable last token is the signature of a closed formula with a count or class slot at the end.
- What it would mean if true: the terminal slot of the `520-220` formula is a count or a class, and 003/016/034/415 are its values. That ties 034 to the terminal-count reading in entry 1.
- Cheapest next move: list every row beginning `520-220` in the metadata and check whether the terminal code tracks stroke count on the plate for each object.

### M-1206 and M-37 show the same face order, so 034 vs 415 may be one visual class split by transcription
- What was seen: the reprioritization file gives face orders by the broad classes T (triangular), L (split leaf), R (rake/bundle): `M-37 A R-L-T`, `M-1206 A+E R-L-T`, `M-1206 A R-L-T`, `M-37 a T-L-R`, `M-1206 a T-L-R`. The two objects match in both faces and both witnesses. The file's own H1/H2/H3 hypotheses predict the 034/415 split is an allograph or policy split (H2).
- Where: `research/docs/archive/lipi_034_post_m315_reprioritization.md`; the 415 fine-form packet it cites (H-786, H-938, H-940, H-941).
- Old label: "naive terminal-substitution story weakened."
- Why it is alive: the observed orders are identical in both faces and both impressions across the two objects that differ only in the last code. That is exactly what an allograph split predicts, and nobody checked the allograph branch against the stroke reading.
- What it would mean if true: 034 and 415 are the same terminal sign written two ways, and the 520-220 frame has one terminal class, not four.
- Cheapest next move: blind-sort the terminal crops of M-1206 and M-37 with H-938 and H-940 (415 controls) and see whether 034 and 415 separate.

### The jar sign 740 is almost always initial, and the namespace identity for it is accepted
- What was seen: the edge table gives `740`: total 1,238, initial 858, terminal 3 (edge share 0.695477). The 740/P324 gate accepts the exact namespace edge: 73 aligned positions, 0 counterexamples, three source panels (M-15, M-21, M-29), and P324 is "the classic jar symbol with two horizontal handles" in Mayig's feature file.
- Where: `research/docs/archive/lipi_broad_order_baseline.md`, `.../lipi_dedup_order_baseline.md`, `.../lipi_edge_removed_baseline.md` (edge table); `research/data/sign_crosswalk/source_panels/740_P324/manifest.csv`; the 740/P324 gate file under `research/data/sign_crosswalk/`.
- Old label: the edge table calls 740 "the top edge sign"; the gate calls the jar identity "not a sign meaning."
- Why it is alive: the drawing identity of 740 is the jar, and it is a physical object the Harappans made and traded. Standing at the front of 858 of 1,238 rows is what a commodity or vessel heading does in accounting. This is the meaning-first hypothesis the rules ask for, and it starts from a drawing identity the project has already accepted.
- What it would mean if true: 740 heads a row as the commodity, and the count or class that follows is the quantity. That fits entry 1 if the terminal count codes (032 to 034) are quantities.
- Cheapest next move: among rows that start with 740, tabulate the terminal codes against all other rows. If 032 to 034 end 740-initial rows at a higher rate than other rows, the commodity-plus-count reading has a measured number.

### Head and tail asymmetry is the main driver of the stored-order win, and I cannot separate them from the files alone
- What was seen: stored order beats reversed order in 1,705 of 1,798 rows after exact-duplicate collapse (0.948276). After top-10 edge removal it is 1,383 of 1,530 (0.903922). After one-edit family collapse, top-10 removed, it is 750 of 837 (0.896057). The edge table shows strong head/tail asymmetry: `740` 858 initial vs 3 terminal; `033` 33 initial vs 149 terminal; `032` 32 vs 137; `817` 1 vs 139; `034` 14 vs 107; `861` 35 vs 111.
- Where: `research/docs/archive/lipi_broad_order_baseline.md`, `.../lipi_dedup_order_baseline.md`, `.../lipi_edge_removed_baseline.md`, `.../lipi_family_downweight_baseline.md`.
- Old label: "T3 structural scout evidence only"; "not accepted reading direction."
- Why it is alive: the order win survives every control the files ran, and the head/tail asymmetry is the strongest structural fact in the set. The files do not test whether a plain head-tail asymmetry (with no order dependency beyond the first and last token) reproduces the win.
- What it would mean if true: there is a fixed head class (initial-heavy signs: 740, 700, 400, 520) and a fixed tail class (terminal-heavy: 032, 033, 034, 817, 820, 861). That is a template with an opening and a closing slot.
- Cheapest next move: run the same stored-versus-reversed test on a null that keeps only each sign's initial-versus-terminal rate and nothing else (the file's own "nonlinguistic baseline" next step, never run). If the null gives a similar win share, the order signal is edge asymmetry.

### H-2237 and H-2238 are adjacent singleton exceptions in a 22-object run
- What was seen: the H-series run H-2218 to H-2239 is 22 objects. The 154/156 packet says H-2237 is the only object with `+154-003+` where the majority has `+156-003+` (21 rows). The 034 lane note says H-2238 is `+700-033+` where the series majority is `+700-034+`. Two adjacent catalogue numbers are each the only exception, each by one token.
- Where: `research/docs/archive/lipi_154_156_comparanda_packet.md`; `research/docs/archive/lipi_frame700_034_ia_cisi_page_locator.md` and the H-series control note (`lipi_034_mayig_acquisition_targets.md`).
- Old label: "single exception ... either a real contrast or a wobble in our own transcription."
- Why it is alive: two exceptions in consecutive catalogue numbers suggest a shared physical source (one tray, one findspot) or one transcription pass with a systematic slip. Either is cheap to check and each gives a different answer.
- What it would mean if true: if they share a findspot, the H-series is one workshop batch with two marked variants. If they are a transcription pass, the H-series codes carry transcription noise at the token level.
- Cheapest next move: pull the findspot, excavation number and museum fields for H-2237 and H-2238 from the metadata, and see whether they match each other and the 21 majority rows.

### The two calibration objects put a 03N count next to 700 on the short side, and the long side carries 004 or 016
- What was seen: H-930 A `+740-900-004+` (long) and H-930 B `+700-032+` (short). H-789 A `+400-520-220-016+` (long) and H-789 B `+033-700+` (short). In both objects the short side pairs 700 with a 03N code. H-930 B is `032` (two strokes, per entry 1) and H-789 B is `033` (three).
- Where: `research/docs/archive/lipi_frame700_034_clean_two_panel_close_read.md`; `research/docs/archive/lipi_frame700_034_ia_cisi_visual_inspection.md`.
- Old label: "clean control for the independent lane ... not subtype validation."
- Why it is alive: these are the two cleanest two-panel objects in the set, and they give a direct count pair: the short side carries 2 and 3 strokes next to 700. They are the most useful counting objects the files name, and nobody has counted their strokes.
- What it would mean if true: the 03N codes are counts, and the H-930 and H-789 short sides are the cleanest measured pair for the count ladder.
- Cheapest next move: blind-count the stroke group beside 700 on H-930 B (CISI Pakistan leaf 374) and H-789 B (leaf 359). Predicted counts from entry 1: two and three.

### M-1206's source caption and text name two different objects
- What was seen: the Bhaskar 2022 Fig. 3 caption says `M-1206`; the running text says `M-2016 (Fig. 3)`. The CISI 3.1 range (from a 2010 review) is `m1660` to `m2132`, so M-2016 falls in the same unseen volume as M-2104.
- Where: `research/docs/archive/lipi_034_p0_public_lead_search.md`; `research/docs/archive/lipi_034_post_m315_reprioritization.md` (M-1206 as "primary source-visible target").
- Old label: "source-gated ... barred from use until a published source settles it."
- Why it is alive: if the picture is M-2016, the M-1206 "primary source-visible target" is not the object the image shows, and M-2016 is a new object with a possibly matching frame.
- What it would mean if true: the M-1206 cohesion result rests on a picture of another object.
- Cheapest next move: look up M-2016 in the metadata and check its text against the `520-220` frame; and check the Fig. 3 image for the no. printed on the object.

### M-177 has a 803 code on a round P385 form, next to an 817 on M-32 with the same first three tokens
- What was seen: M-177 is `390 003 002 803`; M-32 is `390 003 002 817`. The first three tokens match. The final sign differs (803 vs 817). The 817/861 gate says M-177's final sign "is plainly in the rounded P385 leaf/diamond family, and it has no clear tree at its base, which is what a 803 form would need. It looks much like the rounded M-32 817 form." Nine of ten local 803 alignments go to `P364` (a tree-based leaf).
- Where: `research/docs/archive/` (817/861 gate, file name starts `lipi_817_861_mayig_p385_merge_collision_gate_20260712.md`); `research/data/sign_crosswalk/source_panels/817_861_P385_conflict/manifest.csv`.
- Old label: "contextual collision ... kept as a known exception."
- Why it is alive: one object has a code the image does not support. Either M-177 is miscoded (803 should be 817) or 803 has a round allograph. Either reading changes the 803 mapping for every object.
- What it would mean if true: 803 has no round form, and the one round case is a transcription error. The 803 to P364 mapping stands and the M-177 exception goes away.
- Cheapest next move: check the M-177 A final sign against the M-32 A final sign on the same panel set, and check whether M-177's row was entered by hand.

### Plate-mates are a comparator set the files never used
- What was seen: the Marshall Plate CXIV file is named `marshall_plate_cxiv_529_533` (the rods 529 to 533, of which no. 532 is M-2104). The M-478 plate header is `MOHENJO-DARO 478-481` (M-478/479/480 are on it; M-481 is on the same header). The M-685 page header is `MOHENJO-DARO 683-686` (M-683, M-684, M-686 share it). The M-315 page is `MOHENJO-DARO 313-317` (M-313, M-316 share it, and the Kenoyer note groups them).
- Where: `research/docs/archive/lipi_034_m2104_raw_source_alias_route.md` and the M-2104 file list (`tmp/m2104_raw_source/...`, not on disk here); `research/docs/archive/lipi_034_m2104_m479_source_probe.md` (plate header); `research/docs/archive/lipi_034_p0_public_lead_search.md` (M-315 Kenoyer grouping); `research/docs/archive/lipi_frame700_034_ia_cisi_visual_inspection.md`.
- Old label: none. The files use same-plate members only as family-dependence controls (the duplicate-family warning).
- Why it is alive: same-plate neighbours are the cleanest comparators available, since they share excavation, material and carving style. Nobody has checked whether M-481, M-683/684/686, M-313/316, or rods 529/530/531/533 are in the local rows.
- What it would mean if true: a plate-mate with the same text string is a copy, which weakens its vote; one with a different string is a free comparator.
- Cheapest next move: search the metadata for M-481, M-683, M-684, M-686, M-313, M-316 and rods with `CXIV:529/530/531/533` in their excavation field.

### The excavation field may be built by string joining; the M-2104 bridge uses the same field
- What was seen: the M-315 CISI 1 data row reads `M-315 1395 VS 1190 ASI 63.10.117 HU 318`. The local row reads `VS 1190395`. The source splits `1395` and `VS 1190` into separate columns; the local field looks like `VS 1190` joined to `395`. The M-2104 bridge is `VS 875CXIV:532`, from the same field generator.
- Where: `research/docs/archive/lipi_034_m315_cisi1_source_probe.md`; `research/docs/archive/lipi_034_m315_second_slot_decision_gate.md`; `research/docs/archive/lipi_034_m2104_m77_identity_and_segmentation_probe.md` (the local bridge row).
- Old label: "catalogue-data warning, not a fatal contradiction."
- Why it is alive: if the generator joins columns, every excavation string built the same way is suspect, including the M-2104 bridge the whole identity case depends on.
- What it would mean if true: the M-2104 identity bridge is internal to a field the generator built, which is a second reason it is not an external bridge.
- Cheapest next move: count local excavation strings that end in a three-digit tail after a `VS` number, and check the M-2104 row against CISI 3.1 end matter once it is in hand.

### The `class` field is still sign-recoverable after proxy controls, and its definition was never searched for in the books
- What was seen: after removing proxy-heavy labels (1,230 rows, 7 labels), token NB accuracy is 0.643089 against a null mean of 0.322154 (P95 0.345528), macro-F1 0.522030 vs null mean 0.209834. No null iteration reaches the observed score. The class audit scanned 67 text files in the upstream repository and found 0 definition matches.
- Where: `research/docs/archive/lipi_class_proxy_control_probe.md`; `.../lipi_class_robustness_probe.md`; `.../lipi_class_field_audit.md`.
- Old label: "source-internal coding or circularity; not semantic."
- Why it is alive: the field is recoverable from tokens at a margin the null cannot reach. A source's own labelling grammar is a useful thing to read even if it is not ancient. Its codes (SS, SC, VN, MT, IT, SP, LP, TS, VX, NU) may encode a sign-role grammar that the upstream author used to read the signs.
- What it would mean if true: the upstream source has a sign-role typology that can be recovered and checked against the stroke counts in entry 1.
- Cheapest next move: search the books on disk and the CISI and Mahadevan volumes for the class codes (named in the audit, never run), and build the known-script comparator the notes name but never built.

### Dimension bins: the largest Token NB gap is vertical_bin, and the files name a SEAL:S-only run that was never done
- What was seen: vertical_bin Token NB 0.465507, hardest null (edge frame) 0.449037, gap 0.016470 (macro-F1 gap 0.013710). Length+type+site reaches 0.627098. The file's own next step: "artifact-type-specific dimension probes inside SEAL:S, TAB:B, and TAB:I" (named, not run).
- Where: `research/docs/archive/lipi_dimension_residue_stress_probe.md`.
- Old label: "better explained by artifact class, site, material, shape, direction and edge-frame structure."
- Why it is alive: the vertical gap is the only one of five above 0.016 and the only one where the null is an edge-frame null, not a metadata null. Inside one artifact type the metadata shortcut weakens, so the sign signal could show.
- What it would mean if true: a height-coding signal in the stroke-count notation (count tokens and bin heights co-vary).
- Cheapest next move: run the vertical-bin test on SEAL:S alone with the same nulls.

### 097 in front of 700-004 is enriched, but the enrichment is one family
- What was seen: among 700-004 rows, 097 precedes in 4 of 9 (4/9); among 700-034 rows, in 1 of 116 (1/116). Right-tail Fisher p = 0.0000628573. The four 004 rows are one copied formula (M-478, M-479, M-480, M-1425 family), which the family-dependence adjudication collapses to two evidence units.
- Where: `research/docs/archive/lipi_034_m2104_count_compound_stress.md`; `.../lipi_034_m2104_m479_source_probe.md`; `.../lipi_034_m2104_target_side_gate_recheck.md`.
- Old label: "count hypothesis unvalidated"; "targeting signal, not a sign value."
- Why it is alive: the p-value is measured. Even as one family it is the only neighbour frame in the files that splits 034 from 004 by its left context. Read plainly: if the 097 context holds in an independent family, the 034/004 split has a left-context marker that is not the count itself.
- What it would mean if true: 097 is a left-context marker for four-stroke tokens, a second route to the count reading.
- Cheapest next move: find any second independent 700-004 family in the metadata and recount 097 in front of it.

### M-1584 is a single 034 on a pottery rim (standalone)
- What was seen: `+034+` alone on a pot rim, CISI 2 p. 232, `M-1584 A (50 %)` under "GRAFFITI on pottery, rim." It is the only single-sign pottery mark in the P0 set.
- Where: `research/docs/archive/lipi_034_p0_public_lead_search.md`; `.../lipi_034_post_m315_reprioritization.md` (potmark lane).
- Old label: "secondary pottery/graffiti singleton ... low-resolution, fragmentary."
- Why it is alive: a standalone count mark on a vessel is the most count-like context in the set. If 034 is four (entry 3), it is a four-count mark on a pot.
- What it would mean if true: standalone 03N marks on vessels are tallies.
- Cheapest next move: list every single-sign pottery row in the metadata and tabulate the codes; check whether they are all 00N or 03N.

### M-685's iconography conflicts with two sources, and the local field is the one that disagrees
- What was seen: CISI 2 p. 37 header reads `'unicorn' II`; Bhaskar S1 reads Unicorn with text marker b; local lipi reads `Bull1`. M-685's local row is `]034-204+`, the only adjacent 034-204 pair in the filtered layer.
- Where: `research/docs/archive/lipi_034_m685_cisi2_source_probe.md`; `.../lipi_034_p0_public_lead_search.md`.
- Old label: "iconography conflict recorded, not resolved; local metadata cannot be used as if source-perfect."
- Why it is alive: the local iconography field may be wrong for more rows than M-685. Bhaskar S1 is an iconography key with text markers and is on disk as a source (`tmp/m1206_bhaskar/S1-IndusZoomorphicIconCatalogue.pdf` in the working tree that the files name, not present in this checkout).
- What it would mean if true: the iconography field is unreliable, and any text-by-animal analysis has to start from S1 and not the local field.
- Cheapest next move: compare the local iconography field with S1 for all rows with a text marker.

---

## Paid source

CISI 3.1 (Corpus of Indus Seals and Inscriptions vol. 3.1). Tiedekirja offered the hardbound volume at EUR 70, plus UPS shipping to the USA at EUR 48.25, total EUR 118.25. No legal digital copy exists (`research/docs/archive/lipi_034_m2104_cisi31_bridge_route_probe.md`). Why it matters: the M-2104 identity bridge and its end matter (pp. 413 to 443) are not reachable otherwise, and CISI 3.1 is the one route the files name for the 03N and 00N count checks on plates not in the existing collection. The M-2104 notes say the invoice request was sent and nothing was paid. Cúper's call.

## Sources on disk

Present in this checkout:
- `sweep/chunks/chunk_08`, `sweep/TASK.md`, `AGENTS.md` (the chunk and rules).
- `research/docs/archive/` : the 39 chunk files, plus the three stroke-run gates `m010_five_stroke_run_segmentation_gate_20260712.md`, `m020_six_stroke_run_segmentation_gate_20260712.md`, `m072_five_stroke_run_segmentation_gate_20260712.md`.
- `research/data/sign_crosswalk/artifact_witnesses.csv` (Lipi and Mayig rows for M-10, M-20, M-72).
- `research/data/sign_crosswalk/source_panels/`: panel PNGs and manifests for 390_P086_merge (M-12, M-17, M-32, M-34, M-82, M-170, M-171, M-172), 740_P324 (M-15, M-21, M-29), 817_861_P385_conflict (M-1, M-14, M-15, M-21, M-32, M-148, M-177), m010_five_stroke_run (M-10), m020_six_stroke_run_segmentation (M-20 A and a), m072_five_stroke_run (M-72), plus about 30 other folders of single-object panels (002_P122_conflicts, 032_P145_conflict, m004_double_grid_pair, m025, m045, m081, m105, m161, m77_text7_concordance, and others).
- `research/data/sign_crosswalk/evidence_refs.csv` (pinned Mayig commit `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`, PDF hashes for CISI 1 and Parpola 2019 panel source paths).
- `docs/`: present, not inspected by this reader.

Named in my files but absent in this checkout (not inspected): `data/open_prototype/lipi/metadata_filtered.csv` and `lipi_scope_rows.csv`; `data/open_prototype/mayig/` (records index, commit json, features `P004`, `P122`, `P123`, `P124`, `P125`, `P147`, `P151`); `data/open_prototype/reports/*` (all the CSVs and JSON summaries named in the chunk); `tmp/` (CISI page images, M77 page 0084, Marshall Plate CXIV 529-533 and IA leaf 48270_0205, Parpola page renders, the Bhaskar S1 PDF, the CISI XML bundles, the M-315 and M-2104 crop sets). Also named and not checked: `lipi_034_m1206_034_cohesion_gate.md`, `lipi_034_m1206_terminal_component_gate.md`, `lipi_034_m1206_allograph_decision_gate.md`, `lipi_frame700_034_messy_panel_reconciliation.md`, `lipi_frame700_034_neighbor_family_pressure.md`, `lipi_leakage_control_baseline.md`, `lipi_multiside_mark_scope_probe.md`, `lipi_semantic_anchor_target_audit.md`, `lipi_stratified_class_probe.md`, `lipi_metadata_prediction_probe.md`, `lipi_semantic_anchor_prediction_probe.md`.

External (named, not on disk): Parpola 2019 PDF, Mahadevan 1977 IA scan, Marshall Vol. III IA item `in.gov.ignca.48270`, CISI volumes on IA, Bhaskar 2022, Kenoyer and Meadow 2010, Harappa CISI 3.1 page, Tiedekirja product route.

## Ideas named but never run

- Blind stroke counts across the 00N and 03N codes (my entry 1 test; partly sketched by the stroke-run gates, never run as a count-to-code test).
- Blind segmentation of M-479 and M-480 (named as the next hard test in the M-2104 notes; only M-478 and M-1425 were run).
- Substitution test of 032, 033, 034 next to 700 in a source-normalized panel graph (named; blocked on CISI 3.1 end matter).
- Class code definitions searched in CISI, ICIT, Mahadevan, Wells/Fuls and source spreadsheets (named; only the upstream repository was scanned).
- Known-script comparator with artificial class labels derived from sign sequences, to measure how easily a model rediscovers them (named; never built).
- Nonlinguistic administrative or emblematic baseline for the stored-order win (named; never built).
- Terminal-class prediction after exact terminal signs are removed (named; never run).
- Same order profile on M77, CISI or ICIT (named; never run).
- Dimension-bin tests inside SEAL:S, TAB:B, TAB:I (named; never run).
- M-2016 lookup and Fig. 3 image check (named as a conflict; not run).
- Source checks of H-2237 vs H-2233, H-366, M-102 vs M-132, H-1682 (named as "next source questions"; not run).
- Check of M-313 and M-316 local rows for 390-034 patterns (named by the Kenoyer route; not run).
- Ordered-scale test of 032, 033, 034 (quarantined as a claim in the team review; never run).
- The M-1206 cohesion, terminal-component and allograph gates (named in the reprioritization file as follow-ons; the files exist under those names but were not in my chunk and I did not check them).
