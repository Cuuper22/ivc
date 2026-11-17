# Leads, sweep 07 (chunk 07)

Read: all 35 files on the chunk list, start to finish (research/docs/archive/h940_* through lipi_034_m2104_*). Also read, outside the list, because the notes name them and the answers decide the leads: the pinned Mayig feature files under evidence/tmp/mayig_feature_namespace_probe/, research/data/sign_crosswalk/crosswalk_edges.csv, and the source-panel folders under research/data/sign_crosswalk/source_panels/. Nothing was written except this file.

"Checked this run" marks a number I computed in this sweep from files on disk. Every other number is quoted from a note, with the note named.

Terms, in plain words:
- Lipi: the project's own numeric sign labels, such as 034. A transcription code, not a reading.
- Mayig: the pinned catalogue repository (commit ad2f1e2). It gives each sign a Parpola-style P-code, a plain description of its shape, and cross-references to Wells numbers (W-codes) and Mahadevan numbers (M-codes).
- R/L: the recorded reading-direction field, inherited from the corpus metadata. No note checked it against the images.
- Stroke: one vertical line.

---

## Finds, ranked by the bet I would make

### 1. Lipi numbers are Wells numbers, and the 00n, 03n and 70n series write stroke count and stroke height
- What was seen: The crosswalk edges were built by positional alignment on the same object, with no Wells numbers involved. Checked this run: in 166 of 189 Lipi-to-Mayig edges, the linked Mayig feature lists the Wells code W followed by the same three digits as the Lipi number. Examples: 002 to P122 (lists W002), 032 to P145 (W032), 033 to P147 (W033), 003 to P123 (W003), 016 to P126 (W016), 415 to P092 (W415), 740 to P324 (W740). Shuffling the Lipi labels across the same 189 edges, 2000 times, gave a mean of 1.29 matches, a maximum of 6, and no draw at or above 166. The Mayig descriptions then read as a numeral series:
  - 001 (P121): one simple half-height stroke.
  - 002 (P122): two adjacent half-height strokes.
  - 003 (P123): three adjacent half-height strokes.
  - 004 (P124): four adjacent half-height strokes.
  - 005 (P125): five simple vertical strokes.
  - 006 and 016 (P126): six short vertical strokes.
  - 031 (P144): one full-height stroke.
  - 032 (P145): two adjacent full-height strokes.
  - 033 (P147): three adjacent full-height strokes.
  - 034 (no positional edge; Wells W034 is linked to P150): four adjacent full-height strokes.
  - 70n series: 700 (P310) a simple U; 701 (P311) a U with two small strokes inside the top; 703 (P312) a U with three small strokes; 704 to 707 (P316) a U with a long vertical stroke inserted.
- Where: research/data/sign_crosswalk/crosswalk_edges.csv; evidence/tmp/mayig_feature_namespace_probe/repo/indus-valley-script-corpus-ad2f1e218a34b8c33c57de0d6cb8d99272765bbb/features/ (397 JSON files; the ones named here are P040, P041, P092, P121 to P126, P144, P145, P147, P150, P217, P050, P310 to P316).
- Old label: lipi_034_crosswalk_darkness_diagnostic called 034 "coverage absent from overlap"; the p041 namespace table called same-number matches "a separate namespace". Both treated the shared number as something to guard against, not as data.
- Why it is alive: The shared number held in 166 of 189 edges against a shuffle control that averaged 1.29. The 034 "crosswalk dark" label is true only of the positional layer. The pinned Mayig repository already carries a P150 record for W034, so the catalogue does have a shape for 034.
- What it would mean if true: Lipi's 00n, 03n and 70n codes are a numeral system written as stroke count times height, with 70n a U carrying a stroke count. Every sign-identity fight in this chunk (002 versus 032 at M-143, 034 versus 415, 110 versus 112) becomes a count-and-height question that a plate can answer.
- Cheapest next move: Count strokes and measure stroke height on source plates. M-21 A (research/data/sign_crosswalk/source_panels/740_P324/) and the M-140, M-143 and M-154 panels (source_panels/002_P122_conflicts/) are already on disk. Check whether the two-stroke signs (002, 032) differ in height as Mayig says.
- Contrary, once: 23 of 189 edges do not match (for example 920 to P154 where Wells lists W900, and 798 to P230 where Wells lists W550 and W555). The Wells lists are catalogue text, not checked against pixels. The Lipi direction field is also still unchecked.

### 2. The M-2104 kill condition counts the wrong thing: 034 is four full-height strokes, not three
- What was seen: M-2104 (+151-097-700-034+) was killed because its 034 side "failed exact three" (lipi_034_m1206_terminal_triad.md), and the blind adjudication's kill line reads "a discrete U/pot-like unit plus three vertical strokes" (lipi_034_m2104_blind_visual_adjudication.md). Mayig says 004 is four half-height strokes (P124) and 034 is four full-height strokes (P150, via W034). So the M-2104 contrast is four against four, and the difference is height, not count. The comparator M-478 (+400-097-700-004+) shares 097 and 700 in the same positions as M-2104. The three blind adjudicators saw "a U/pot-like unit adjacent to a count-like group of four vertical strokes" on M-478, which is 700 plus 004. Height was never measured on either object.
- Where: lipi_034_m2104_blind_visual_adjudication.md; lipi_034_m2104_004_family_dependence.md; lipi_034_m1206_terminal_triad.md (M-2104 line); Mayig P124.json and P150.json.
- Old label: "failed exact three" for M-2104, and "the 700-034 side of this extraction fails" as the kill condition.
- Why it is alive: The verdict was produced by a three-stroke test the catalogue does not support for 034. Three independent adjudicators already saw the U plus a four-stroke group on M-478. The M-2104 gate needs a height-and-count test, which has not been run.
- What it would mean if true: M-2104 is a clean test of 034 = four full-height strokes, sitting next to 004 = four half-height strokes on the same U frame. The whole 700 plus count template becomes one repeated pattern across M-478 and M-2104.
- Cheapest next move: Re-run the blind count on the M-2104 034 side against "four full-height strokes" and the M-478 004 side against "four half-height strokes". Re-crop M-478 A from CISI India n150 (the crop is not on this disk). The kill line becomes "not four full-height strokes".
- Contrary, once: the two rows also differ in their first sign (151 against 400), so M-2104 and M-478 are not a clean one-sign contrast.

### 3. The recorded R/L field makes all five companion panels disagree with the Mayig identity of 700; reading L/R makes all five agree
- What was seen: Under recorded R/L, five source panels put 700 on the vertical bar and 032, 033 or 034 on the loop, leaf or V: H-938 B (+034-700+), H-910 B (+700-034+), H-930 B (+700-032+), H-789 B (+033-700+), H-942 B (+033-700+). Mayig says 700 is a U (P310, W700), and 03x is a bar of full-height strokes (P145, P147, P150). Under forced L/R, every panel fits both: H-938 B has 034 as the left vertical group and 700 as the right loop/cross; H-910 B has 700 as the left loop/leaf (U) and 034 as the right rake; H-930 B has 700 as the left V/leaf and 032 as the right bar group; H-789 B has 033 as the left bar group and 700 as the right loop/oval; H-942 B has 033 as the left bar group and 700 as the right V/leaf.
- Where: lipi_034_m1206_h938_b_component_probe.md; lipi_034_m1206_h910_component_probe.md; lipi_034_m1206_independent_direction_controls_gate.md; lipi_034_m1206_direction_policy_provenance.md; lipi_034_m1206_h938_h910_direction_sensitivity_gate.md; Mayig P145, P147, P150, P310.
- Old label: "conditional negative under recorded R/L"; forced L/R "not accepted because no checked source/transcription-policy evidence currently licenses replacing the recorded fields."
- Why it is alive: The R/L value was inherited from the corpus metadata and never checked against images. The only evidence behind the 034 negative is that field. The Mayig identity is catalogue text, so it is a hint and not a ruling, but it points the same way as the panels in all five cases. The H-938 B probe itself says the left vertical component "visually resembles the M-1206 target terminal and the H-938 A/A bis exact-side 415 controls". Under L/R that left component is the 034 bar, and the 034-to-415 closeness is no longer a counterfactual.
- What it would mean if true: The 034 = loop/leaf negative was produced by the direction field. In these companion sides the bar is the 03x numeral and the U is 700.
- Cheapest next move: Count the strokes in the bar group on the existing crops. Predicted under Mayig plus L/R: H-789 B left group shows three full-height strokes; H-930 B right group shows two; H-942 B left group shows three. The stroke count on those bars is the splitting observation: it confirms L/R if the counts match, and kills this lead if they do not. H-942 B is on CISI Pakistan n374, printed p. 340.

### 4. 034 and 415 may be two stroke-bundles that differ in count: 034 four full-height strokes, 415 a pitchfork with tines
- What was seen: The Mayig record for 415 (P092) is "pitchfork with tines", with a tines count as its feature. The M-37 strict core is "a comb/rake with a horizontal top bar and a central stem" (lipi_034_m1206_m37_terminal_recut_gate.md). The M-1206 terminal core was called an "upright-rib match" by reviewer A (lipi_034_m1206_terminal_component_gate.md), and the packet called it a "parallel vertical terminal family core". The blind clusters put M-1206 nearest H-938 A/A bis, a 415 control. The old "fine-form split" (M-37 comb versus M-1206 vertical bundle) was described by shape and never counted.
- Where: lipi_034_m1206_m37_terminal_recut_gate.md; lipi_034_m1206_source_normalized_component_packet.md; lipi_034_m1206_terminal_component_gate.md; lipi_034_m1206_m37_415_fine_form_binning.md; Mayig P092.json, P150.json.
- Old label: four open hypotheses (allograph, separate signs in one family, source-side artifact, transcription split), with "no discriminator" recorded.
- Why it is alive: Shape clustering cannot separate two stroke-bundles, so the blind packets were never able to decide between allograph and separate signs. A stroke count on the M-1206 terminal core and a tine count on the 415 cores is the discriminator the notes asked for and never ran.
- What it would mean if true: 034 and 415 are not allographs. They are different counts and bar types inside one stroke-bundle family, which fits the numeral series in find 1 and the 415 pitchfork.
- Cheapest next move: Count the upright strokes in the M-1206 terminal core (crops T002 and T003 in the terminal gate; the crops are not on disk, so re-crop from CISI Pakistan n181). Count the tines on the M-37 strict core, H-938 A/A bis and H-940 A. If M-1206 shows four strokes and the 415 cores show a pitchfork with a different count, the allograph question closes toward separate signs.

### 5. The 520-220-X terminal slot holds a stroke count or a pitchfork, and 006 and 016 point to one shared Mayig feature
- What was seen: Terminal Mayig codes (checked this run): 003 to P123 (positional edge, 10 of 10), three half-height strokes (M-1912, source-gated); 016 to P126 (positional edge, 6 of 6), six short vertical strokes; by the Wells identity from find 1, 006 also lands on P126 (W006 is listed there, but no positional edge exists for 006); by the same identity 034 lands on P150, four full-height strokes (no positional edge; M-1206 carries 034); 415 to P092 (positional edge, 5 of 6), pitchfork with tines (M-37 is among its witnesses; H-938 A is a 415 object). The fixed head is 520, which maps to P217 "isosceles triangle on top of a vertical line (arrow? spear?)", and 220, which maps to P050 "fish with no other decoration". Local rows: K-150 +520-220-006+ (local only), H-942 +520-220-016+ (source-visible full signband; the terminal sign is not isolated).
- Where: lipi_034_m1206_terminal_triad.md; lipi_034_m1206_k150_h942_singleton_controls_source_gate.md; lipi_034_m1206_allograph_decision_gate.md; Mayig P123, P126, P150, P092, P217, P050.
- Old label: 006 and 016 treated as separate singletons ("K-150 acquisition only", "H-942 full-signband control, not terminal-comparable"); the 003 and 034 terminals treated as allographic questions.
- Why it is alive: In one frame, the terminal is a numeral slot. Two different Lipi codes (006 by the Wells identity, 016 by positional alignment) land on the same six-stroke feature. If that is right, the H-942 last sign and K-150's last sign should look alike, which is a test the notes never set up.
- What it would mean if true: 520-220 is a fixed head (arrow-triangle over a fish) followed by a quantity slot. The terminal of these seals and tablets counts strokes.
- Cheapest next move: Count the strokes on the last sign of H-942 A (CISI Pakistan n374, printed p. 340, which is source-visible). A count of six short strokes would tie 016 to the 006 feature with no K-150 source needed.

### 6. The 110 branch: Lipi 110 is Wells 110, which Mayig puts on P040 "person with U", not P041; and four of its six rows sit on objects that also carry a 415
- What was seen: The 110 exact rows are six: H-2148 481.2, H-2147 673.1, H-2100 817.2, H-2152 865.1, H-940 1820.2, and Kanmer 4881.1 (p41 namespace table). Mayig P040 is "person with U" and lists W110 and W111. P041 is "person with U with vertical stroke inserted, stroke has a small dot at the bottom" and lists W112 and M034. The branch tested 110 as Parpola sign 41 (P041). No positional edge exists for 110; the P040 link is the Wells identity from find 1. The 112 to P041 edge has one support and no counter. On the same object, four of the six 110 rows also carry a 415-family row: H-940 (1820.1 +520-220-415+ and 1820.2 +110+), H-2148 (481.1 +520-220-415+ and 481.2 +110+), H-2147 (673.2 ]220-415+ and 673.1 ]110+), and H-2152 (865.2 ]220-415+ and 865.1 +110[). H-2100 is the exception, with a 400-000 partner. The H-2148 one-sign panel is described as "a central vertical body with branching or limb-like strokes", which reads like a figure.
- Where: research/data/sign_crosswalk/p041_parpola41_namespace_table_20260712.csv (N02, N05, R03); research/docs/archive/h940_h2147_h2148_110_sign41_gate.md; h940_h2147_h2148_110_branch_visual_precheck.md; Mayig P040.json and P041.json; evidence/tmp/h2148_h2100_h2152_110_route/ (Kenoyer 2005 PDFs; the OCR text files in that folder are empty).
- Old label: "controlled crosswalk hypothesis"; the H-2147 panel "component-level only"; H-940 B "not visually binding".
- Why it is alive: The 110-with-415 same-object pairing repeats in four of six rows, and the sign-41 link was only a reverse-side clue. The Wells identity points 110 at the adjacent person-with-U code (P040), and the branch never tested that. Both person codes (P040, P041) are "U plus person" motifs, which is where the one-sign H-2148 limb figure would sit.
- What it would mean if true: 110 is a person-with-U sign. 415 is its usual partner on the other side of the object. The sign-41 story is one of two adjacent person codes, and the family is not confined to one reverse cluster.
- Cheapest next move: Rasterise pages 17 and 18 of kenoyer2005_harappa_2000_2001.pdf and look at the H2001-5142 one-sign panel for a U beneath the figure. A U with a vertical stroke inserted would support P041, and a bare U with a figure would support P040. Then count the 110 to 415 pairs across the full Lipi export, which is not on disk here.

### 7. The two conflict gates are height disputes at two strokes, and a source plate can settle them
- What was seen: P122 (Lipi 002, two half-height strokes) and P145 (Lipi 032, two full-height strokes) "differ only in stroke height" (lipi_002 gate and lipi_032 gate). At M-140 A, Lipi 002 faces Mayig P145, a height dispute. At M-143 A, Lipi 032 and 002 are swapped against P122 and P145, which is a height swap across two adjacent positions. At M-154 A, Lipi 002 faces P300 (a complex sign), so that one is a segmentation dispute, not height. The gates recorded all three as "source-visible counterexamples" and did not measure height.
- Where: lipi_002_mayig_p122_source_conflict_gate_20260712.md; lipi_032_mayig_p145_source_conflict_gate_20260712.md; source panels research/data/sign_crosswalk/source_panels/002_P122_conflicts/ (M-140 A, M-143 A, M-154 A) and source_panels/740_P324/M-21_A_CISI1_pdf49_print13.png (the dominant-policy witness).
- Old label: "SOURCE_VISIBLE_COUNTEREXAMPLES_BLOCK_EXACT_MAPPING" and "SOURCE_VISIBLE_RECIPROCAL_INVERSION_BLOCKS_EXACT_MAPPING".
- Why it is alive: Both catalogues agree the sign has two strokes and disagree only on height. That is the one thing a plate can measure, and the gates said only that the plates did not decide it.
- What it would mean if true: The 002 and 032 pair is the two-stroke height contrast. One catalogue is wrong about height at M-140 A and M-143 A, and the M-21 witness settles which way the Lipi-to-Mayig policy runs.
- Cheapest next move: Measure the stroke height ratio on the M-21 A panel (Lipi 032 with Mayig P145, the dominant policy) and on the M-143 A panel (the inverted case). If M-21 shows full-height strokes at 032 and M-143 shows half-height strokes at the same position, the Mayig height is right and the M-143 Lipi label is the one in question.

### 8. 034 is a frequent sign, not a singleton, and its single-sign tally falls as the stroke count rises
- What was seen: The darkness note counts 182 rows containing 034: 166 Harappa, 7 Mohenjo-daro; by type 91 TAB:I, 53 TAB:B, 26 POT:T:g, 4 SEAL:S. The M-1584 note calls the same 182 "rows containing 034", while the darkness note calls them "exact 034 rows". The exact bounded single-sign rows are 032: 47, 033: 25, 034: 11, 002: 12, 004: 6, 700: 11. Of the 11 exact 034 singletons, 9 are pottery or clay (lipi_034_m1584_cisi2_source_probe.md). Under the Wells identity, those are two, three and four full-height strokes, and the tally falls 47, 25, 11.
- Where: lipi_034_crosswalk_darkness_diagnostic.md; lipi_034_m1584_cisi2_source_probe.md (M-1584 A, CISI Vol. 2 p. 232, leaf n266, 50 percent view).
- Old label: M-1206 as a "singleton terminal, dangerous"; M-1584 as "pottery/graffiti pressure, not line-text".
- Why it is alive: The 034 branch was built on one seal in one frame. Most 034 rows are on Harappa tablets, which were never sampled visually as a class. Pottery singletons falling away as the stroke count rises looks like a tally.
- What it would mean if true: 034 is a common count sign, and its pottery singletons are tally marks of four strokes. The falling tally with count is what a counting system looks like.
- Cheapest next move: Count the strokes in the high-resolution M-1584 mark (already requested from the Harappa contact). If it shows four full-height strokes, the pottery-tally reading gets its first direct count. Separately, the TAB:I and TAB:B rows with 034 need source plates before any count is claimed.

### 9. The M-1206 long side (e(1)) is source-visible and carries two signs whose Mayig codes are already source-validated
- What was seen: The e(1) side of M-1206 is visible on CISI Vol. 2 p. 147 (leaf n181), which the terminal triad recheck confirmed. The companion row is +740-690-435-255-002-861+. Edge 740 to P324 is exact (73 of 73, source-validated, P324 = jar, W740). Edge 861 to P385 is a source-validated merge member (12 of 12, W861). Edge 002 to P122 is in conflict (find 7).
- Where: lipi_034_m1206_terminal_triad_source_recheck.md; lipi_034_m1206_terminal_triad.md; research/data/sign_crosswalk/crosswalk_edges.csv (edge_00001, edge_00014); Mayig P324.json, P385.json.
- Old label: the e(1) side was counted as removing the "companion not visible" blocker, and was never read for signs.
- Why it is alive: The e(1) plate is a new six-sign object. Two of its six signs already have exact or merge Mayig codes, so the plate is an out-of-sample check on the same object. If the jar and diamond-leaf sit at the Mayig positions, two exact edges generalise to a new object.
- What it would mean if true: The exact edges work as a reader on new material, so M-1206's long side can be glossed sign by sign.
- Cheapest next move: Crop the e(1) plate from CISI n181 at full resolution, mark the six positions, and check the jar at position 1 and the diamond-leaf at position 6. The pinned repository may also have an M-1206 record outside the Mohenjo-daro unicorn overlap, which the notes did not check.

### 10. The Linear B ceiling and the IVC score may already be in the same range (not like-to-like, one contrary number)
- What was seen: Linear B Series D, blinded, with source-provided gaps and sequence-leave-one-out: bidirectional top-1 0.294347 across all lengths and 0.294314 under the IVC p95 length cap (299 rows). Row-leave-one-out gives 0.300195 and 0.304348. The broad Lipi T3 planning layer scores 0.325865 bidirectional top-1, and the harsh stress condition scores 0.224004. The note says these are not like-to-like.
- Where: research/docs/archive/linear_b_series_d_scarcity_baseline.md; known_script_scarcity_comparator_acquisition_audit.md.
- Old label: "not like-to-like; validates no IVC sign."
- Why it is alive: If the IVC structural score is above the gapped known-script ceiling on a matched task, the Lipi structure is already comparable to a deciphered administrative script. The contrary is the one to state: the Lipi number is a masked-sign test on a planning layer, not the same task as Linear B's gapped test, which is why the note gave it no weight.
- What it would mean if true: The Lipi structure is an administrative-like system, not noise.
- Cheapest next move: Run the Linear B gapped sequence-leave-one-out protocol on the 299 Lipi IVC p95 rows, using the same code. The Linear B data file and tool are not in this checkout (Zenodo DOI 10.5281/zenodo.7404653, MD5 0c9b9190b86840c82cafdbf4f4b8c827, both named in the note).

### 11. The 000 slot is a counted unit that the Lipi count field undercounts
- What was seen: Four objects carry 000 (M-105, M-27, M-61, M-62). Each 000 is one bounded structural unit. Lipi's signs field undercounts: M-27 has signs 6 and length 7. The Mayig P-codes at the 000 positions are P324, P123, P251, P310, so 000 is not a sign number.
- Where: lipi_000_sign_bearing_policy_gate_20260712.md; research/data/sign_crosswalk/source_panels/lipi_000_sign_bearing_policy/ (on disk); research/data/sign_crosswalk/source_panels/m105_unknown_policy/.
- Old label: "closed at 4 of 4 source-inspected objects."
- Why it is alive: The gate closed four objects, but any count hypothesis that reads the signs field is wrong on every row with 000. A 000 that is a bounded stroke unit fits the numeral series in find 1.
- What it would mean if true: 000 is a placeholder for an unread numeral unit. That is a guess, not a finding.
- Cheapest next move: Count how many Lipi rows contain 000, then re-run any count-based hypothesis with length taken from the stored text, as the gate already recommends.

---

## Ideas named but never run

- Blind stroke and tine count on one packet: the M-1206 terminal core, the M-37 strict core, H-938 A/A bis, H-940 A, the last sign of H-942 A, and the bar groups of H-789 B, H-930 B and H-942 B. The packets only sorted shapes.
- Stroke count and height on the M-2104 034 side and on the M-478 004 side (the notes ran only a three-stroke test).
- Co-occurrence tests across the full Lipi export: 110 with 415; 700 with 415; 034 with 700. In the rows the notes quote, 6 of 11 rows containing 034 have 700 next to it; the other 5 are M-315, M-685, M-1206, M-1584 and M-1963.
- Pottery share of single-sign rows for 032, 033, 002 and 700. Only the 034 share (9 of 11) was measured.
- Mahadevan M034 is cross-referenced on P041 (the pinned Mayig record), and Lipi 034 is a Wells number. Whether Lipi 034 and Mahadevan M034 are the same sign is untested.
- The Wells primary sign list (ICIT). The crosswalk sources table says it is not locally acquired.
- Linear B with citable sign IDs, SumTablets blinded by revision, and Coptic continuity. None was run.
- Acquisitions with no reply in these files: H-2240 and H-2241 (Andreas Fuls); M-1912 (CISI 3.1 or equivalent); H-319 and H-1284 panels; the high-resolution M-1584 mark (Harappa contact); all-side M-1206 (Harappa and Bhaskar).

---

## Sources on disk

- research/docs/archive/ (422 notes; the 35 on this chunk are the ones read above).
- research/data/sign_crosswalk/crosswalk_edges.csv: 189 Lipi-to-Mayig P edges with support, counter and state. Used for find 1.
- research/data/sign_crosswalk/signs.csv, sign_systems.csv, edge_pressure_summary.csv, evidence_refs.csv, audit_issues.csv, review_events.csv, namespace_gates.csv, artifact_witnesses.csv: sign inventory, gates and witness tables.
- research/data/sign_crosswalk/p041_parpola41_namespace_table_20260712.csv: Parpola sign 41, Mayig P041, and Lipi 110 namespace records.
- research/data/sign_crosswalk/source_panels/: labelled CISI panel crops and manifests. Relevant folders: 002_P122_conflicts/ (M-140 A, M-143 A, M-154 A), 032_P145_conflict/ (manifest only), 740_P324/ (M-15, M-21, M-29 A), lipi_000_sign_bearing_policy/, m105_unknown_policy/.
- evidence/tmp/mayig_feature_namespace_probe/repo/.../features/: 397 pinned Mayig feature JSON files (commit ad2f1e218a34b8c33c57de0d6cb8d99272765bbb). Used for finds 1 to 5 and 9.
- evidence/tmp/mayig_feature_fetch/P122.json and P145.json: two more copies of those features, not compared against the repository files.
- evidence/tmp/parpola_1994_signlist/parpola_1994_deciphering_sindhilanguagelibrary.pdf: Parpola 1994, sign no. 41 at printed p. 70 (PDF page 88).
- evidence/tmp/h2148_h2100_h2152_110_route/: Kenoyer 2005 and Kenoyer and Meadow 2010 PDFs for the 110 objects (the matching .txt extracts are empty).
- evidence/tmp/m1206_bhaskar/: Bhaskar 2022 article PDF, S1 zoomorphic catalogue PDF, and the RMRL Bulletin No. 6 (June 2025) PDF.

## Named by the notes but not on this disk

- data/open_prototype/** (the Lipi export metadata_filtered.csv, which the crosswalk sources table gives as sha256 B3E2A94E..., plus all reports and tools). Named throughout the chunk.
- tmp/** (all crops, CISI downloads, the H-938, H-910, H-930, H-789 and M-1206 panel crops, the M-37 recut crops, and the H-942 crops). Named throughout the chunk; re-crop from source where needed.
- Linear B Series D Samples.txt (Zenodo 10.5281/zenodo.7404653, MD5 0c9b9190b86840c82cafdbf4f4b8c827).
- Online only: CISI Vol. 1 and Vol. 2 Internet Archive leaves n54, n150, n181, n265, n266, n267, n359, n372, n374, n406, n474, n837 (the leaves the chunk names); Mayig repository; Wells primary tables.
