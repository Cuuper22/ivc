# Leads, sweep reader 09

Nine finds from the 36 files on chunk 09. I read every file in full and edited no other file. Numbers marked (recount) I recomputed in this pass from the row files under research/data/open_prototype, using read-only counts and exact tests. The rest come from the notes. Paths are relative to /home/claude/ivc.

Terms used below: FRAME700 is the project's label for two-sign rows built on sign 700, such as +700-034+. The companion is the other sign in such a row (032, 033 or 034). H-series means the 22 tablets H-2218 to H-2239. TAB:I and TAB:B are the catalogue's tablet types. A face is a physical side. The catalogue's "side index" is the row number, and the face readings below assume the row number is the physical face. Checking that assumption comes first in find 2. p is an exact two-sided test (Fisher). BH q is the false-discovery-rate adjusted p used in the notes.

### 1. Triangular tablets have three faces, so the "C side" and "two-side" conflicts are a missing third face
- What was seen: In the catalogue, H-353, H-983, H-2204, H-2211 and H-357 are TAB:I prisms with a triangular cross-section, each recorded with 2 sides. H-355 is triangular with 3 sides and carries two +700-033+ rows. The H-series tablets are triangular with 3 sides; the five I checked (H-2218, H-2219, H-2221, H-2237, H-2238) all are, and Kenoyer and Meadow 2010, as quoted in the validation note, call the whole group triangular in section. (recount) Among Harappa TAB:I artifacts in the multi-side rows, 67 are triangular: 35 record 2 sides and 32 record 3. H-2204 is recorded locally as 19 x 7.3 x 0 with 2 rows. The public Kenoyer 1997 entry (Fig 10.07) gives 19 x 7.3 x 3.5 with 3 incised sides, which is the mismatch the source-lead audit could not reconcile. H-352 and H-354 are typed SEAL:R in the catalogue, but Parpola 2019 calls the H-352/353/354 group triangular-prism tablets.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv (cross-section, sides, type, dimensions); research/data/open_prototype/reports/lipi_multiside_mark_rows.csv; research/docs/archive/lipi_frame700_034_messy_panel_reconciliation.md (H-983 and H-353 "C side"); research/docs/archive/lipi_frame700_034_independent_source_lead_audit.md (H-2204); research/docs/archive/lipi_multiside_mark_validation_queue.md (H-2218 to H-2239).
- Old label: "true C-side hazard, source-policy issue, blocks clean-control use" (messy-panel reconciliation); "thickness/side-count mismatch to resolve rather than smooth over" (source-lead audit); "three-side duplicate series, validate before interpreting" (validation queue). None of these checked the cross-section field.
- Why it is alive: On a triangular prism a third panel is the expected third face, so the C panel that blocks H-353 and H-983 as clean controls may just be a face. If that face carries text, both can serve as controls once faces are indexed, instead of being discarded. Strongest contrary, once: a triangular section does not force writing onto all three faces. A blank third face would make the two-side records correct.
- What it would mean if true: Side counts in this catalogue are face counts for prisms, and triangular TAB:I tablets are three-face documents as a class. The C-side and two-row conflicts are one object-format variable with a physical cause.
- Cheapest next move: Read the C panel of H-353 on the Internet Archive CISI leaves that the notes already locate (leaves n265 and n696), and record whether it carries a short row or is blank.

### 2. The H-series is one three-face formula, and 034 and the 861-003 pair swap faces 1 and 2
- What was seen: The validation queue's signature counts for the 22 H-series tablets are 13, 7, 1 and 1. Read as faces: in all 21 H-series tablets that carry 034, the 034 row and the 861-003 row sit on faces 1 and 2 in opposite order. 034 is on face 2 in 13 of them and on face 1 in 8. Face 3 carries 156 (or 154) with 003 in all 22. (recount) In TAB:I short rows, 156 appears 21 times, all on face 3. 003 appears 50 times and 22 of them are on face 3; the signatures put two 003 rows on each H-series tablet, so 44 of the 50 are H-series. The 22 triangular artifacts with a face-3 003/156/154 row are exactly the H-series. The codebook note: observed side roles predict a masked side at top-1 0.525 against 0.099 for frequency (162 predictions). Without the H-series the same test gives 0.229 against 0.156 (96 predictions).
- Where: research/data/open_prototype/reports/lipi_multiside_mark_validation_queue.csv; research/data/open_prototype/reports/lipi_multiside_mark_sequence_families.csv; research/docs/archive/lipi_short_mark_functional_codebook.md; research/docs/archive/h2218_h2239_series_validation_sheet.md (not read in this pass); H-series identifiers in the excavation-idno column of research/data/open_prototype/lipi/metadata_filtered.csv.
- Old label: "copied or batch-specific side-role system, one-series trap" (functional codebook); "overfitting risk" (validation queue).
- Why it is alive: Two blocks that swap inside a fixed three-face frame is the substitution pattern the project's own gate asks about, and here it holds in all 21 tablets that carry 034. The codebook note says a reading that works at one site and one tablet type stands there; the H-series is one of each. The notes say the tablets come from secondary deposits outside the perimeter wall in Trench 11, Period 3B, so one production run is the simplest reading and a real one. Strongest contrary, once: one batch can be copied from one exemplar, so the swap may be one scribe's choice with no wider content. The broader codebook result is consistent with that.
- What it would mean if true: The 22 tablets are one complete short text on three faces. 034 and 861-003 are two interchangeable phrases in a variable slot on faces 1 and 2, and face 3 is a fixed heading.
- Cheapest next move: Pull the 22 plates (identifiers in the metadata excavation-idno column and the queue note). For each tablet, record which face carries 034 and which carries 861-003, then check whether the 13-to-8 split follows any visible variable such as plate number, dimensions or mould.

### 3. The 060 long row: four 034 tablets and one 033 tablet share one frame, and H-1845 (034) and H-237 (033) carry the identical long row
- What was seen: (recount, subtype rows) The token 060 sits in 8 subtype rows: 034 six times (H-1138, H-1824, H-1845, H-1846, H-351, H-823), 033 once (H-237), 032 once (H-1309). Five TAB:B tablets share the frame 240;692;740 plus one variable third token. +740-603-240-060-692+ is on H-1138 (034, short row after the longer row) and H-1846 (034, before). +740-642-240-060-692+ is on H-1845 (034, before, 23.6 x 11.5 x 3 mm) and H-237 (033, after, 21 x 11 mm). +740-636-240-060-692+ is on H-823 (034, before). So H-1845 and H-237 carry the same longer row with companions 034 and 033 on the same tablet type. H-1138 and H-1846 carry the same longer row with the same companion 034 and opposite face order.
- Where: research/data/open_prototype/reports/lipi_frame700_subtype_rows.csv (longer_texts, short_text, side_relation, dimensions); research/docs/archive/lipi_frame700_034_long_context_substitution.md (token 060 in the matched-triad test: 6 hits for 034, 0 for 033, 1 for 032; delta 5.5; uncorrected p 0.0068; BH q 0.077 over 75 token tests).
- Old label: "fails correction; moderate-pressure material" (long-context substitution). That test counts only matched triads, so H-237 was never in it.
- Why it is alive: A same-text, different-companion pair within one tablet type is the minimal contrast the project keeps asking for, and the notes never named this pair. H-1138 and H-1846 show that face order can flip with the text held fixed, so face order does not follow the text. Strongest contrary, once: H-237 is a 033 with the same long row, so the 060 association is not one-directional.
- What it would mean if true: 033 and 034 are two companion marks for one longer text, and the tablet decides which mark goes on which face. The companion would be a layout choice, not a property of the text.
- Cheapest next move: Read the plates for H-1845 and H-237. Confirm the short face shows 034 on one and 033 on the other, and that the longer text is the same sign sequence on both.

### 4. 033 and 032 attach to different longer rows: +400-740-176+ sits on 20 of 137 033 rows and 2 of 102 032 rows
- What was seen: (recount, companion context rows) 20 of 137 033 rows carry +400-740-176+ in their longer text, against 2 of 102 032 rows (p = 0.00054). Excluding H-2218 to H-2239, which carry no longer text, it is 20 of 136 against 2 of 102 (p = 0.00052). 034 rows carry it 9 times in 114. The companion audit tested 033 against everything else, which folds the 034 rows into the comparison and dilutes it.
- Where: research/data/open_prototype/reports/lipi_short_mark_companion_context_rows.csv (longer_texts); research/docs/archive/lipi_short_mark_companion_context_audit.md; research/docs/archive/lipi_short_mark_context_orientation_audit.md.
- Old label: "raw-only hint; fails blocked correction (BH 0.058 Fisher, 0.082 permutation for 033); copy-family heavy" (companion context audit).
- Why it is alive: The pairwise contrast is the one that carries the signal, and it is a depletion as much as an enrichment: 032 almost never sits on this longer row. Multiplying the exact p by the audit's 90 tests gives about 0.05 (my arithmetic). Strongest contrary, once: the 20 rows fall on about 16 distinct artifacts, so the effective sample is small.
- What it would mean if true: 033 and 032 are different companions because they go with different kinds of longer text. 032 attaches to +740-031-001-140+ (3 rows in the audit) and almost never to the 400-740 family.
- Cheapest next move: Check the 2 rows of 032 that carry +400-740-176+ against their plates. If they are catalogue duplicates of 033 rows or misread companions, the contrast is an error. If not, it stands.

### 5. 034 comes before the longer row on TAB:B and 033 comes after it on TAB:I, and both tablet types point the same way
- What was seen: (recount, companion context rows, before or after only) TAB:B: 034 is before the longer row in 23 of 27 rows, 033 in 23 of 54 (p = 0.0003). TAB:I: 034 is before in 17 of 38, 033 in 9 of 45 (p = 0.019). On TAB:B, 034 sits on face 1 in 32 of 42 rows. Among rectangular TAB:B tablets it is 18 face-1 rows against 5 face-2 rows.
- Where: research/data/open_prototype/reports/lipi_short_mark_companion_context_rows.csv; research/data/open_prototype/reports/lipi_multiside_mark_rows.csv; research/docs/archive/lipi_short_mark_companion_context_audit.md (the corrected marginal: 033 after and 034 not after, BH 0.036).
- Old label: "corrected catalogue-side relation; does not establish physical side order" (companion context audit).
- Why it is alive: A mixing artifact would reverse direction between types. It does not. Both types put 034 before and 033 after, and the gap is larger on TAB:B. Strongest contrary, once: on TAB:I the split is 17 of 38 against 9 of 45, which is much weaker, and catalogue side order is not yet face order.
- What it would mean if true: 033 and 034 are two face positions for one companion slot, and the tablet type sets how often each is used. 034 is the mark that precedes the longer text and 033 the mark that follows it.
- Cheapest next move: On the plates of the 23 TAB:B tablets with 034 before the longer row, check whether the longer text sits on the second physical face.

### 6. The 034 small-object residue survives removal of the H-series
- What was seen: For the non-H rows, the dimension model recalls 034 in 63 of 93 cases (0.677). Against the harshest of four blocked shuffles, the 95th percentile is 0.559, and none of 100 shuffles reached the observed 034 recall. The horizontal bin h_10_13 holds 20 of 93 034 rows against 18 of 238 others (lift 2.84). The object-level area test for 034 after H-series removal gives p = 0.0036, BH q = 0.104, the lowest flag that survives.
- Where: research/data/open_prototype/reports/lipi_frame700_subtype_rows.csv; research/data/open_prototype/reports/lipi_frame700_subtype_blocked_null_iterations.csv; research/data/open_prototype/reports/lipi_short_mark_dimension_no_h_series_token_tests.csv; research/docs/archive/lipi_frame700_subtype_blocked_null.md.
- Old label: "dimension and form-context shaped; object-format default" (subtype discrimination and blocked null); "A2/A3 boundary; H-series plus a weaker 034 lead" (dimension stress).
- Why it is alive: Two methods, same subtype, same direction (small objects), and it passes a null that holds type, sides, order, context and relation fixed. The "object format" label treats the object as an alternative to the sign, but the object is where the sign gets written. Strongest contrary, once: the frequency baseline scores 0 on 034 by construction, and the dimension model gains its 034 recall by giving up 033 (033 top-1 0.368, against 1.0 for frequency).
- What it would mean if true: 034 is a size-grade mark written on small tablets. Guessing freely: a unit or grade for small pieces.
- Cheapest next move: Run one exact area test for 034 inside cross-section and type blocks on the non-H rows. That tests whether a within-block version pushes BH q under 0.05.

### 7. All five carriers of the 002;416;861 long row take 034, and the copy family is one production unit
- What was seen: (recount) The only subtype rows whose long-row tokens are 002;416;861 are H-2094, H-2095, H-2096, H-2097 and H-910. All five carry 034: 5 of 93 034 rows against 0 of 238 others (p = 0.0016). H-2094, H-2095 and H-2096 share one sequence family. H-2097 reverses to +034-700+. H-910 (hook 10994470) is the only carrier outside that family.
- Where: research/data/open_prototype/reports/lipi_frame700_subtype_rows.csv; research/docs/archive/lipi_frame700_034_independent_triad_audit.md; research/docs/archive/lipi_frame700_034_long_context_substitution.md.
- Old label: "copy-family pressure; H-910 demoted to independence rank 50" (independent triad audit).
- Why it is alive: Copy pressure is a reason to count the copies as one act. It is also what a production unit looks like: one mould or workshop batch that writes 034 with this long row every time. Strongest contrary, once: the family is one act, so the p = 0.0016 rests on one observation, not five.
- What it would mean if true: 034 is the companion in one workshop's formula. H-910 would be the second production run that confirms the pairing.
- Cheapest next move: Find H-910's plate (hook 10994470) on the free Vats 1940 plate route or in CISI. The notes do not yet map it to a plate. Check its 034 row and long row.

### 8. An outside computation flagged the same pair
- What was seen: A computational analysis (Khanna and Merriam, International Journal of Computer Applications, December 2025) reports 700-034 as statistically noticeable. The validation packet quarantines it as support and keeps it only as a pointer.
- Where: research/docs/archive/lipi_frame700_034_residue_validation_packet.md (quarantine note).
- Old label: "quarantined; may not be cited as support".
- Why it is alive: Credit in one line: an independent method found the pair without our controls. Quarantine is a verdict, and AGENTS voids those. Their method is a hint list.
- What it would mean if true: The 700-034 pair is a broad statistical fact, not an artifact of how our catalogue was sliced.
- Cheapest next move: Read their method section and find the statistic that flags 700-034.

### 9. Class labels are predicted from sign text above structured nulls (weakest find)
- What was seen: Token prediction of catalogue class beats the four structured nulls in all 11 eligible strata. The smallest gap to the mixed admin-emblem null is 0.096 (SEAL:S at Harappa), and no null iteration reached the observed score in any stratum. Across the whole layer, token accuracy is 0.543 against 0.270 to 0.289 for the nulls.
- Where: research/data/open_prototype/reports/lipi_stratified_class_summary.csv; research/docs/archive/lipi_metadata_prediction_probe.md; research/docs/archive/lipi_stratified_class_probe.md.
- Old label: "source-field stress test; sign-recoverable after proxy controls, so circular or source-internal" (later class audit, as summarised in the notes).
- Why it is alive: The downgrade reads sign-recoverability as circularity. The strongest defender says that if cataloguers grouped inscriptions by sign content, the catalogue's class is a record of how readers grouped texts, which is information. Strongest contrary, once: that is the same as circularity, and nothing here separates the two.
- What it would mean if true: Class is a scribal genre (label, ticket, seal text) recoverable from the signs.
- Cheapest next move: Check whether research/data/mahadevan_20260905/concordance_rows.csv defines the class codes.

## Checked and dropped in this pass

- "034 is Harappa-only": every FRAME700 subtype row is Harappa (032, 033 and 034 alike), so this is not a property of 034.
- "034 more often stands alone on its object": true only with the H-series (49 of 114 in the notes). Without it, 034 has 28 of 93 with no longer text, 033 has 36 of 136 and 032 has 29 of 102.
- "861 and 034 bridge the H-series and the 002;416;861 family": (recount) none of the 90 non-H Harappa multi-side objects that carry 034 also carry an 861 short row. Eight carry 861 without 034. The 861-034 link exists only inside the H-series.
- "Reversed order tracks triangular shape": no. 10 of 14 reversed TAB:I rows are rectangular.
- "034 against 033 side order reverses between tablet types": no. Both types put 034 before and 033 after (find 5).

## Sources on disk

- research/data/open_prototype/lipi/metadata_filtered.csv: 5,679-row catalogue with cross-section, sides, type, dimensions, excavation identifier.
- research/data/open_prototype/reports/lipi_multiside_mark_rows.csv: 1,808 multi-side rows with side index and short-mark flags.
- research/data/open_prototype/reports/lipi_short_mark_companion_context_rows.csv: 353 companion rows (032/033/034) with side relation and longer-row text, H-series included.
- research/data/open_prototype/reports/lipi_frame700_subtype_rows.csv: 353 subtype rows with dimensions, sequence families and longer-row tokens.
- research/data/open_prototype/reports/lipi_multiside_mark_validation_queue.csv and lipi_multiside_mark_sequence_families.csv: signature families including H-2218 to H-2239.
- research/data/open_prototype/reports/lipi_short_mark_dimension_no_h_series_token_tests.csv: dimension tests with the H-series removed.
- research/data/open_prototype/reports/lipi_frame700_subtype_blocked_null_iterations.csv: the 100 shuffles behind the 034 recall result.
- research/data/open_prototype/reports/lipi_stratified_class_summary.csv: class prediction by stratum.
- research/data/open_prototype/reports/lipi_h2218_h2239_series_validation_sheet.csv and research/docs/archive/h2218_h2239_series_validation_sheet.md: the H-series sheet (not read in this pass).
- research/docs/archive/lipi_frame700_034_ia_cisi_page_locator.md: Internet Archive CISI leaf locators (not read in this pass).
- research/docs/archive/lipi_tab_i_mixed_400_740_176_side_context.md: the 26 TAB:I artifacts in the mixed family (not read in this pass).
- research/data/mahadevan_20260905/concordance_rows.csv: the Mahadevan concordance rows (not read in this pass).
- Outside, named in the notes: the Internet Archive bundle "TheIndusScript.TextConcordanceAndTablesIravathanMahadevan" (CISI volumes 1 and 2 as scans); Kenoyer and Meadow 2010 (harappa.com PDF); Kenoyer 1997 (harappa.com PDF); Parpola 2019 on inscribed bone and ivory rods (Helsinki PDF); Vats 1940 plates (harappa.com); the Khanna and Merriam 2025 paper (ijcaonline PDF).
- CISI volume 3.1 (paid, needed for about 11 objects in the source route audit): the harappa.com page gives no price and no free PDF. It offers a Buy button and an Amazon US link. Cúper should read the price from the Buy link.

## Ideas named but never run

- A panel-graph substitution test on one full triad, once source panels exist (research/docs/archive/lipi_frame700_034_source_panel_graph.md).
- A source-resolved cross-family substitution test (same note).
- Semantic-anchor prediction rerun with more iterations on the vertical and horizontal bins, within SEAL:S, TAB:B and TAB:I strata, with sign-class blocks in place of raw edge-frame blocks (research/docs/archive/lipi_semantic_anchor_prediction_probe.md).
- Whether 700, 034, 033, 032 and 003 predict side count, row index, longer-row token class or measurements after type and site controls (research/docs/archive/lipi_multiside_mark_scope_probe.md). Partly run in the dimension stress audit.
- Comparison of short-mark behaviour with known administrative token systems and known multi-side tablets (same note).
- Source check of 154 against 156, and 033 against 034, as visual variants on the H-series (research/docs/archive/lipi_multiside_mark_validation_queue.md).
- Whether local side order matches published plate order (same note).
- Mirror-variant collapse test on reversed companion marks, after Daggumati and Revesz 2021 (research/docs/archive/lipi_frame700_034_prior_research_pressure_probe.md).
- Administrative-economics comparison after Rao 2018, and stronger non-linguistic baselines after Nair 2026 (same note).
- Reproduction of the subtype and leakage profiles on an authoritative corpus, CISI volume 3.1 or ICIT (research/docs/archive/lipi_leakage_control_baseline.md; research/docs/archive/lipi_frame700_subtype_blocked_null.md).
- Non-linguistic administrative and emblem controls run against the 034 subtype profile (research/docs/archive/lipi_leakage_control_baseline.md).
- Class prediction rerun after removing strata that fall below the eligibility thresholds, and compared with source conventions (research/docs/archive/lipi_stratified_class_probe.md; research/docs/archive/lipi_metadata_prediction_probe.md).
- The Vats 1940 plate XCVI check of H-916 (object 12516) against the local hook 12516456 (research/docs/archive/lipi_frame700_034_source_acquisition_manifest.md).
- The Parpola 2019 triangular-prism check for H-352, H-353 and H-354 (research/docs/archive/lipi_frame700_034_local_contrast_public_lead_audit.md).
- Added in this pass, not in the notes: a face-exclusivity test that asks, for each companion mark, whether it sits on one face only, inside cross-section blocks. It replaces the side-index balance test, which asked a different question (research/docs/archive/lipi_short_mark_orientation_audit.md). Also, a plate check that row index equals physical face on three known tablets (H-353, one H-series tablet, one two-side triangular tablet).
