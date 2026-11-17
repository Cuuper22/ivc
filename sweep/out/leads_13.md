# Salvage sweep leads, reader 13

Chunk: /home/claude/ivc/sweep/chunks/chunk_13 (486 paths: about 480 JSON result summaries plus data READMEs). This file holds 25 finds, followed by negative results kept for the record and the two closing lists. Each lead gives its status: built on, tested, or paused.

---

## 1. Stored order beats reversed order in Indus Lipi rows

- **What was seen:** On the exact-collapsed Lipi sequences, the stored order is higher than the reversed order in 1704 of 1798 rows (stored_win_share 0.94772). Mean stored-minus-reversed is 2.499961 per transition, and the maximum null share is 0. On the harsh scope (top 10 edges removed, one-edit families collapsed, 365 rows) the figure is 307 of 365 (0.841096). By site: Mohenjo-daro 0.816038 (212 rows, null share 0.002); Harappa 0.741071 (112 rows, null share 0.004). With Mohenjo-daro and Harappa balanced to 112 rows each, the mean is 0.804496 (p05 0.776786, p95 0.834821; paired null share 0.003). The largest single-row shift in the influence controls is 0.010552. Contrary numbers: Lothal 0.3125 (16 rows, null share 0.988), and the matched-overlap subset at 0.363636 with null share 1. Linear B Series D gives 0.996403 (277 of 278), so the comparator matches or exceeds the Indus figure.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/effective_unicity_directionality_comparator_summary.json; effective_unicity_directionality_site_profiles_summary.json; effective_unicity_directionality_site_balance_summary.json; effective_unicity_directionality_influence_controls_summary.json; effective_unicity_directionality_skeptic_controls_summary.json; effective_unicity_directionality_policy_controls_summary.json (all in the same reports directory).
- **Old label:** The comparator file says directionality alone is "not a writing-specific diagnostic", because Linear B and other comparators match it.
- **Why it is alive:** The result holds under site balancing, under single-row removal, and under the policy controls (random row, site and direction-label flips all give null share 0). Linear B is a real script with a stored direction, so a match with it is what a writing signal should look like. Lothal is 16 rows at one site, so its low share can come from sampling or from source conversion rather than from a reversed script.
- **What it would mean if true:** The stored sequence is the reading order of a written text, so every sequence-based test in this sweep gains a direction.
- **Cheapest next move:** Split the Lothal rows by source convention and check whether their stored order follows the publication source instead of the object. If Lothal follows the publication order and the other sites do not, the split is found. Status: tested. The writing-specific claim is paused until that split runs.

## 2. Masked-sign local constraint on Indus sequences

- **What was seen:** Leave-one-row-out masked-sign top-1 is 0.279591 (top-5 0.5341). Shuffle nulls: global token shuffle mean 0.1064 (max 0.1275); row-internal 0.120083 (max 0.1375); position slot 0.165233 (max 0.198333); edge frame 0.165025 (max 0.190833); register-blocked position 0.169358 (max 0.2); template admin code 0.087867 (max 0.115). The Indus figure is above every null maximum. On the same kind of test: SumTablets 0.171753 (top-5 0.373681); Linear B clean IVC-cap bidirectional top-1 0.4359; Linear B gapped leave-one-out 0.2943 (top-5 0.6388). Contrary numbers: Linear B gapped (0.2943) and Pictish stones (0.4503, top-5 0.614) both sit above Indus.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/effective_unicity_nonlinguistic_comparator_summary.json; effective_unicity_known_script_comparator_summary.json; effective_unicity_sumtablets_comparator_summary.json; effective_unicity_realworld_nonlinguistic_comparator_summary.json.
- **Old label:** The file's decision: survives the masked-sign forger gate as a local context constraint. The broad bidirectional figure (0.325865) was rejected because the admin (0.472924), emblem (0.443351) and mixed (0.415069) generators equal or exceed it. Masked top-1 is not promoted alone, since Pictish is higher.
- **Why it is alive:** Indus beats SumTablets by a wide gap, and SumTablets' own controls peak near 0.04 to 0.06. A neighbour constraint that predicts a masked sign above every shuffle maximum does not need any sign value to be read.
- **What it would mean if true:** Indus sequences carry sign-to-sign constraints beyond frequency and position. Under a language reading these are syntax-like neighbours. It does not give meaning.
- **Cheapest next move:** Rerun the Indus and Linear B gapped tests with sequence lengths matched, so that 0.2796 and 0.2943 are compared on the same length mix. Status: tested. Paused on the length-matched rerun.

## 3. 741-060 followed by 920 in every exact copy

- **What was seen:** In raw rows, 920 follows 741-060 in 31 of 31; in exact dedup, 30 of 30. Seven sites: Mohenjo-daro 19, Harappa 5, Dholavira 2, Lothal 2, Chanhu-daro 1, Kalibangan 1, Rakhigarhi 1. Types: SEAL:S 24, TAB:I 3, TAB:B 2, TAG:P 1, TAG:R 1. Fisher p 1.4692670982228672e-64. Witnesses include C-16, H-1309, H-2127, H-2128 and H-89. Contrary numbers: in the maxstat tournament, 741-060 to 920 ranks 6th by best hit (30). The successor-shuffle null for it has a mean null max hit of 39.2578 (mean null max share 0.330924). The file records p_ge_30_of_30 as 0, which needs reading against that mean before anyone uses it. Higher tournament rows: 002-817 to END 105 of 108; 002-861 to END 102 of 126.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/risky_741060920*.json (the risky file for this formula); /home/claude/ivc/research/data/open_prototype/reports/consolidate_formula_operator_maxstat_20260531_summary.json.
- **Old label:** promoted_candidate_metadata_layer (risky file). The tournament gives it no decision above 6th place.
- **Why it is alive:** 30 exact cells across seven sites and five types, with no exception. The tournament ranks by best hit without a site-balance step, so a broad END-bound bigram such as 002-817 can score high on the site mix it happens to have.
- **What it would mean if true:** 741-060 then 920 is a fixed two-sign unit inside free text, likely a phrase or a formula rather than a chance pair.
- **Cheapest next move:** Rerun the maxstat tournament with the sites balanced by a per-site cap, and see whether 741-060 to 920 keeps its place. Status: tested. Promotion waits on that rerun.

## 4. 154 and 158 prefixes select a 465..475 successor band (806 series)

- **What was seen:** A rule trained on Harappa only (prefixes 154 and 158 followed by successor band 465..475) hits 23 of 23 at Harappa against 0 of 23 controls (Fisher 1.2145605314292647e-13). Held out to non-Harappa sites it hits 6 of 6 against 3 of 58 controls (Fisher 1.1203829020606104e-06). The prefix-only rule across all sites hits 29 of 29 against 3 of 81 (Fisher 1.600720818212485e-23). Extended with 155 and 100, non-Harappa hits 9 of 9 against 0 of 55 (Fisher 3.631004997603842e-11). Separately, 154-806 is followed by 467..474 in 16 of 16 raw rows and 14 of 14 exact-dedup rows: Harappa 12 of 12, Mohenjo-daro 3 of 3, Dholavira 1 of 1, non-Harappa 4 of 4. Contrary numbers: the forger lists 91 competitor bigrams with at least the same support, and 741-060 has its best window at 913..920.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/risky_806_prefix_series_geographic_holdout*.json; risky_154806_series_prefix_forger*.json; risky_806_prefix_context_split*.json (same reports directory).
- **Old label:** promoted_candidate_metadata_layer (806 holdout). candidate (154-806 forger). The context split is recorded as candidate_survives_first_context_split_test.
- **Why it is alive:** The rule was fitted at one site and then held at other sites, and the non-Harappa 6 of 6 is a true holdout. The context split separates two lanes: 154, 155 and 100 point to a seal lane (seal type, reverse, no icon); 158 points to a TAB:B and phytographic lane. The seal-type contrast gives Fisher 4.755686672792613e-06.
- **What it would mean if true:** 154 and 158 are series prefixes that choose the second-sign band, and that choice separates seals from phytographic tablets. That is a classifying code inside the sign sequence.
- **Cheapest next move:** Run the lane split on objects from a site with no Harappa rows and with 158-806 present, to see whether the lane split holds at a third site. Status: tested. The context split has passed its first test.

## 5. Exact stems ending in 590, 255, 920 and END

- **What was seen:** 740-390 to 590: 41 raw rows, 40 followed by 590; exact dedup 37, with 36 followed by 590; seven sites; one exception, M-1669 (Mohenjo-daro, SEAL:S, Bull1:W), with END next. 690-435 to 255: raw 30, followed by 255 in 29; exact dedup 26, followed in 25; three sites; one exception, a Harappa TAB:B row with 176 next. 002-817 to END: 105 of 108 exact collapsed, across 10 sites and 9 types. 060-920 to END: 51 of 52, across 9 sites. Contrary numbers: 740-100 to 415 at 27 of 79, and 002-820 to END at 70 of 75 sit in the same tournament family without a separate decision.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/risky_740390590*.json; risky_690435255*.json; consolidate_formula_operator_maxstat_20260531_summary.json (all in reports/).
- **Old label:** 740-390 to 590: candidate_survives_exact_dedup_cross_site_probe_but_has_one_exception. 690-435 to 255: candidate, recorded as weaker than 741-060 and the 806 series. 002-817 to END and 060-920 to END: no separate decision recorded in the tournament file.
- **Why it is alive:** The END counts for 002-817 and 060-920 each span 9 to 10 sites and 9 types, so they are not one site's copy. Each exception is a single row.
- **What it would mean if true:** These two-sign closers mark where a text ends, a closing formula used across sites.
- **Cheapest next move:** Check the two exception rows (M-1669 and the Harappa TAB:B row) on the source images, to see whether the END or the following sign is the real last pair of the object's text. Status: tested. Paused on the exception check.

## 6. Positional crosswalk from Lipi signs to the Mayig P-namespace

- **What was seen:** 136 eligible records; 739 aligned positions; 189 Lipi signs; 160 Mayig signs. Strongest pairs: 740 to P324, 73 of 73; 390 to P086, 25 of 25; 060 to P120, 17 of 17; 520 to P217, 15 of 15; 240 to P062, 14 of 14; 820 to P378, 14 of 14; 002 to P122, 57 of 60 (counter-examples P145:2, P300:1); 220 to P050, 27 of 29 (counter-examples P056:1, P060:1); 032 to P145, 20 of 21 (counter P122:1); 741 to P325, 10 of 13 (counter P324:3). Grade counts: high 14, medium 21, low 27, conflicted 6, sparse 121. The sparse grade holds most of the records, which is the contrary number.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/crosswalk_lipi_to_mayig_candidates.csv; crosswalk_summary.json (same directory); /home/claude/ivc/research/data/sign_crosswalk/README.md.
- **Old label:** Mapping state is recorded as uncertain, needing image or authoritative sign-list validation. The sign_crosswalk README records zero accepted edges and 8 empty witness sequences; its audit passed with caveats.
- **Why it is alive:** 740 to P324 has no counter-example in 73 positions, and the 390, 060, 520 and 240 pairs have none either. The alignment used count-matched artifacts with the R/L direction fixed, so the match is constrained by more than a single sign.
- **What it would mean if true:** The Lipi list and the Mayig list number the same signs, and each Lipi count can be read through its Mayig name.
- **Cheapest next move:** Run a within-artifact shuffle null on alignment consistency. This is named but has never been run. Status: built on the candidate CSV only. Paused until that null runs.

## 7. 817 and 861 may be one sign split by the catalogue

- **What was seen:** 817 occurs in 189 rows and 861 in 238. The two occur together in 2 rows: H-1930 (+408-817-920-002-861+) and M-855 (+861-260-832-390-590-002-817-690-544+). In both co-occurring rows, 002 sits between the two signs. 817 is last in 161 rows; 861 is last in 144 rows. 861 follows 002 in 153 rows; 817 follows 002 in 137. Both map to Mayig P385, 12 of 12 each. Contrary number: the two signs do appear together in 2 rows, so they are not simply interchangeable in every row.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/lipi_scope_rows.csv (2887 numeric-clean rows of 5679 total); crosswalk_lipi_to_mayig_candidates.csv (same directory); /home/claude/ivc/research/data/sign_crosswalk/README.md (lists 817 and 861 to P385 as an unresolved pressure pair).
- **Old label:** Unresolved pressure pair in the sign_crosswalk README.
- **Why it is alive:** Same Mayig slot, same neighbour (002), mostly terminal. A catalogue that lists one glyph under two numbers would give exactly this pattern: two counts, one slot, and 002 always close by.
- **What it would mean if true:** One sign with the combined occurrences of both numbers, which makes it a larger and better-measured sign. The two co-occurring rows would then be catalogue or copy errors.
- **Cheapest next move:** Look at the source images of H-1930 and M-855, to see whether 817 and 861 are drawn as two glyphs or as one. Status: tested on counts. The source check has not been run.

## 8. Sign 220 as a fish-leaf family across three naming systems

- **What was seen:** Crosswalk 220 to P050: 27 of 29 (medium grade). The Parpola 2019 article's sign no. 60 is a plain fish. Mayig P050 is an undecorated fish witness in the namespace. Local 220 has the fish-leaf family shape. Middle crops support broad fish/leaf-family compatibility for M-37, H-938 A and H-940 A, with S009/M-37 strongest. Contrary numbers: the strict-family gate found no sign-specific bridge, and two of three visual reads do not allow a sign-60-specific match. The panels are low-resolution cached derivatives.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/parpola_sign60_local220_fish_bridge_probe*; parpola_sign60_local220_middle_crop*; parpola_sign60_local220_strict_fish_family*; replacement_p050_local220_strict_fish_family_source_gate_20260712* (same directory).
- **Old label:** Replacement gate of 2026-07-12: park P050 strict identity. The pinned evidence earns broad fish/leaf-family pressure only.
- **Why it is alive:** Three naming systems (the crosswalk, Parpola and Mayig) point to the same family for 220, and the visual family shape recurs in three objects.
- **What it would mean if true:** 220 is a fish sign. Entry 15's 520-220 frame would then carry a fish sign in its middle slot.
- **Cheapest next move:** Obtain print-resolution images of M-37, H-938 A and H-940 A. This is named but has never been run. Status: paused on image resolution.

## 9. Sign 034 as a physical size tier

- **What was seen:** On 309 eligible artifact rows (111 positives for 034, 198 negatives), the dimension model's held-out ROC AUC is 0.701087 (balanced accuracy 0.661207; recall for 034 0.756757). Grouped-bootstrap 95% CI: 0.606806 to 0.78903 (median 0.695575). Matched nulls: administrative format AUC mean 0.597158 (p95 0.654323; null share 0.0015); emblem copy-family mean 0.616055 (p95 0.662687; null share 0.001). Median areas: 032 at 146.85 mm2 (85 rows); 033 at 117.15 (113 rows); 034 at 101.25 (111 rows, 21 of them H-series). Token 034 is in short-mark role 115 times against 9 elsewhere (enrichment 31.364491). Contrary numbers: the gate failed. The dimension-minus-format AUC interval runs from -0.010581 to 0.134992 (median 0.05872), so its lower bound is below zero. The H-series complete holdout (22 rows, 21 positives) gives AUC 0.47619, which is degenerate because almost every row is positive.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/frame700_034_size_tier_heldout_20260712_summary.json; lipi_frame700_subtype_blocked_null_summary.json; lipi_frame700_subtype_summary.json; lipi_short_mark_functional_codebook_summary.json; lipi_multiside_mark_summary.json (same directory).
- **Old label:** CLOSE_034_OBJECT_SIZE_OR_METROLOGICAL_TIER_UNDER_CURRENT_LOCAL_EVIDENCE. The gate failed on the lower bound of the dimension-minus-format interval.
- **Why it is alive:** The AUC clears both matched nulls by wide margins. The blocked null gives 034 a top-1 of 0.677419 against a null of 0.18129 (p 0). The short-mark enrichment is large.
- **What it would mean if true:** 034 marks a size or measure tier, so the Indus numerals carry a physical scale.
- **Cheapest next move:** Remeasure the 309 eligible rows under one protocol. This is named but has never been run. Status: paused by its own gate. The next step is measuring, not reanalysis.

## 10. Source class code predicted from sign tokens

- **What was seen:** The class field has nine values (IM, IT, LC, LP, MS, MT, SC, SP, SS), with majority 0.2192. Token naive Bayes reaches 0.5433 accuracy (macro F1 0.4749), against a duplicate-matched null of 0.2895 (p95 0.2997), an administrative null of 0.2818 and an emblem null of 0.2704. Stratified by TAB:I: token naive Bayes 0.7295, against an emblem null of 0.3525 (p95 0.4) and a duplicate null of 0.4295. SEAL:R: 0.5345, against nulls of about 0.23 to 0.27. TAB:B: 0.5202, against an administrative null of 0.2621. Contrary numbers: the null runs used only 5 iterations, and the class field could not be matched to any definition in the upstream text (class_definition_matches_found 0 across 67 scanned text files).
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/lipi_metadata_prediction_summary.json; lipi_stratified_class_summary.json; lipi_class_field_audit_summary.json; the class column of /home/claude/ivc/research/data/open_prototype/reports/lipi_scope_rows.csv.
- **Old label:** The class audit says to treat lipi.class as an unverified source code. The null rows are all null_ge 0, but at 5 iterations.
- **Why it is alive:** Tokens beat every structured null on every stratum shown. The widest gap is in TAB:I, where the token figure is 0.7295 and the highest null is 0.4295.
- **What it would mean if true:** The source's class codes sort texts by a real category (for example genre or function), and the sign tokens carry that category.
- **Cheapest next move:** Rerun the nulls at 1000 iterations, and find the upstream definition of the class codes in yajnadevam/lipi at head b272ad99c253ba7fa1e4cd91f48cce31f6d02bf4. Status: tested at 5 iterations. Paused on the definition.

## 11. Quarantined gloss columns in the upstream Lipi CSV

- **What was seen:** The class audit records readme_claims_deciphered as true and translation_columns_present as true. The quarantined columns are sanskrit, translation and notes. This reader did not open the quarantined columns.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/lipi_class_field_audit_summary.json; /home/claude/ivc/research/data/quarantine/README.md; upstream repository yajnadevam/lipi, branch main, head b272ad99c253ba7fa1e4cd91f48cce31f6d02bf4.
- **Old label:** Quarantined. The quarantine README excludes the botched-run artifacts from accepted-claim evidence unless re-earned. Allowed uses are read_for_autopsy_only and code_reference_only.
- **Why it is alive:** The upstream README claims decipherment. If the translation column lines up row by row with the sign sequences, it gives a parallel text for every other test in this sweep. Contrary number: the class field has zero definition matches, so the labels in that CSV may not be reliable.
- **What it would mean if true:** A parallel text exists, and each sequence result can be checked against a gloss.
- **Cheapest next move:** Under the read_for_autopsy_only rule, count whether the translation column lines up one-to-one with the sign rows. That is an alignment count only, with no accepted claim. Status: paused. Not opened by this reader.

## 12. Sign 603 locked to 060 692 after 240

- **What was seen:** Sign 603 sits before 060 692 after 240 in 3 rows, all in the frame 740-603-240-060-692 (H-1138, H-1846, H-1137). In the post-861 tail, 603 appears in 3 rows (M-240, M-714, M-1273); 603 appears 7 times in all. Lock null (20000 iterations): false-positive rate 0.0004 for this specific lock; 0.04 for any bridge sign locked to a pair; 0.04 for any non-background bridge. After 240, the sub-frame 002 861 leads to X=482 in 7 of 9 rows; the sub-frame 060 692 carries 603 (3), 642 (2) and 636 (2). Contrary numbers: 3 rows is a small base, and the 0.04 rate for any non-background bridge shows that a lock of this kind is not rare at this scale.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/campaign_032_002_861_x240_bridge_lock_null_summary.json; campaign_032_002_861_x240_bridge_summary.json; campaign_032_002_861_x240_subframe_migration_summary.json (same directory).
- **Old label:** The file's decision: "bridge_lock_pattern_is_weak_to_moderate_distributional_support_not_a_promotion".
- **Why it is alive:** The specific lock has a 0.0004 false-positive rate, and all three rows share one frame.
- **What it would mean if true:** 603 is a fixed connector between the 240 slot and the 060 692 pair.
- **Cheapest next move:** Check whether H-1137, H-1138 and H-1846 are the same graphic object, or find an independent second X-before-240 context. Status: paused. Promotion waits on that context.

## 13. Terminal unit 533 717 after 002 861

- **What was seen:** The restricted tail unit 533 717 after the fixed prefix 002 861 (terminal, lengths 1 to 3, minimum support 2) has observed max support 2 and one candidate, in M-376 and M-391. Forger nulls: global context shuffle false-positive rate 0.00018 (50000 iterations); site-type-symbol shuffle 0.0006; strict_raw context shuffle worst case 0.0006. Register test: 2 of 7 Mohenjo-daro no-icon SEAL:R rows with 002-861 carry it; 2 of 3 cuboid-convex no-icon SEAL:R rows carry it; no Mohenjo-daro SEAL:S row carries it. Contrary number: the row-internal token shuffle false-positive rate is 0.0042, with null max support 3, which is above the observed support of 2.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/campaign_032_002_861_restricted_tail_forger_summary.json; campaign_032_002_861_533717_register_test_summary.json; campaign_032_002_861_tail_rarity_register_scan_summary.json (same directory).
- **Old label:** restricted_tail_pattern_not_promotable_under_forger. The register test recommends a conditional register candidate. The tail-rarity scan recommends narrowing to a subclass or apposition candidate, not a whole-register marker.
- **Why it is alive:** The global shuffle false-positive rate is 0.00018, and the register split places the unit in no-icon SEAL:R rows and not in SEAL:S rows.
- **What it would mean if true:** 533 717 marks a subclass of no-icon seal, with 002 861 as its register label.
- **Cheapest next move:** Collect no-icon SEAL:R rows from objects not yet seen, and test 533 717 there. The current base is 2 of 7 and 2 of 3. Status: paused under the forger rule.

## 14. Sign 032 after 240 across frame text

- **What was seen:** After 240, the next sign is 032 in 9 of 12 frame-text dedup units (0.75), against 46 of 239 units elsewhere (0.192469). Risk difference 0.557531; odds ratio raw 12.586957, Haldane-adjusted 11.294931. In matched site-type blocks: 9 of 12 against 35 of 150 (odds ratio raw 9.857143, adjusted 8.830986). Contrary number: the base is 12 units, so a small change in dedup would move the rate.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/campaign_a_220_x_240_contrast_summary.json.
- **Old label:** The file carries no decision field.
- **Why it is alive:** The odds ratio holds after site-type blocking (adjusted 8.83), so one site does not appear to drive it.
- **What it would mean if true:** 240 is followed by 032 as a fixed frame step, so the pair 240 032 is a unit.
- **Cheapest next move:** Rerun the site-type-matched contrast with frame dedup done at object level, and see whether the 12 units grow. Status: tested once. No decision recorded.

## 15. Third slot 415 after 520-220

- **What was seen:** The 520-220-X cluster has 52 rows, 51 objects and 21 exact-three rows. Third slot 415: 28 rows, 17 of them exact three; sites Harappa, Lothal and Mohenjo-daro; companions 700-034 (4), 700-032 (2) and 110 (2). P(415 | 520-220) is 0.4667, against P(415 | 220 not after 520) of 0.1909. Context-slot null: third-slot accuracy 0.6875 against site-type accuracy 0.8125 (gain -0.125). Global closure shuffle null mean 0.51298; third-slot null share 0.0148; within-site shuffle null share 0.2302; within-type 0.5286. Contrary numbers: the context-slot model is below the site-type model by 0.125, and the within-site null share is 0.2302.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/vector4_context_association_summary.json; campaign_520_220_x_context_slot_null_summary.json; campaign_520_220_x_summary.json; campaign_unit_boundary_520_vs_220_summary.json (same directory).
- **Old label:** "vector4_context_slot_candidate_not_sign_meaning".
- **Why it is alive:** The conditional gap is large (0.4667 against 0.1909), and the global null share is 0.0148.
- **What it would mean if true:** 415 closes a fixed 520-220 frame. That is a formula slot, not a site habit.
- **Cheapest next move:** Rerun the 520-220 slot against a within-site null that also matches frame length. Status: paused. The within-site null is the test that splits the two readings.

## 16. Unigram 407 as a Mohenjo-daro TAB:C opener

- **What was seen:** Unigram 407 in Mohenjo-daro TAB:C: unit rows 60, support 25, expected 2.05292, precision 0.416667, recall 0.333333, lift 12.177778, z 16.520717. Targeted nulls (2000 iterations): 407 Copper z 15.92; 407 TAB:C z 16.40. Global shuffle null share 0. Contrary number: the within-site-type shuffle null share is 1, so site-type composition accounts for the signal under that null.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/vector4_context_association_summary.json; vector4_targeted_context_nulls_20260531_summary.json (same directory).
- **Old label:** not_claim_eligible. Stopped under the within-site-type null. Kept as a site-composition lead.
- **Why it is alive:** The lift (12.18) and z (16.52) are large, and the signal survives the global shuffle. The within-site-type null asks whether site-type mix explains the opener, which is a different question from whether the opener is real.
- **What it would mean if true:** A Mohenjo-daro scribal habit of opening TAB:C with 407.
- **Cheapest next move:** Run a site-only null and a type-only null separately, to see which factor explains the 407 opener. Status: stopped under the site-type null. Kept as a lead.

## 17. Brahmi "ra" matches at 527 and 061

- **What was seen:** Real-token impostor null: 527 "ra" in catalogue order has share 0.000 (zero of 1000 at or above observed); 061 "ra" has 0.008; 061 "ja" reversed has 0.103. Other rows at 0.000 include 740 ra, 798 ra, 002 ra and 861 ra. Contrary numbers: the v3 gate blocked all 83 families before review: 83 on the shape null (above 0.01) and 58 on fewer than 3 unique CISIs. Row 527 has one CISI.
- **Where:** /home/claude/ivc/research/data/brahmi/brahmi_real_token_impostor_forger_v3_summary.json; brahmi_shape_descent_null_summary.json; /home/claude/ivc/research/data/brahmi/ (READMEs); /home/claude/ivc/research/data/sign_crosswalk/README.md.
- **Old label:** Blocked by the v3 independence gate (3 unique token hashes, 3 CISIs, 3 source paths, unanimity, null share at most 0.01).
- **Why it is alive:** Zero of 1000 real-token impostors reach the observed share, which is among the lowest null shares in the Brahmi set. The block is on source count, not on the statistics.
- **What it would mean if true:** Indus 527 shares its shape with Brahmi "ra" in catalogue order, which would be a letter-level match.
- **Cheapest next move:** Find two more independent CISI sources for the Brahmi "ra" sign. Status: paused on source count.

## 18. Three-role template in the H-2218 to H-2239 objects

- **What was seen:** All 22 local objects H-2218 to H-2239 fit a three-role inventory: one +861-003+ side, one +700-03x+ side and one +15x-003+ side. Side 3 is always +15x-003+ (22 of 22; exact permutation p 3.186635545325e-11). Exact texts: +861-003+ (22); +700-034+ (21); +700-033+ (1); +156-003+ (21); +154-003+ (1). Of 397 validation-queue rows, non-H rows with the complete template: 0. Contrary numbers: the side-order A against B probe shows no significant split (horizontal p 0.506889; vertical p 0.666035). Manufacturing groups (6, 9 and 7 objects): horizontal F 6.766736, permutation p 0.00875. Singletons H-2237 and H-2238 both fall in group 3; the exact-pair probability for that is 0.090909.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/lipi_h2218_h2239_* summaries (same directory); lipi_short_mark_functional_codebook_summary.json for the FRAME003 role co-occurrence (22 artifacts, lift 13.689655).
- **Old label:** The template occurs only inside the H-series. Manufacturing-group confound: group 3 holds both singleton variants.
- **Why it is alive:** A hard template of 22 of 22 side-3 matches at p 3.2e-11 is what a workshop stamping a fixed code on a batch would produce.
- **What it would mean if true:** The H-series is one production batch with a fixed three-face code, which is a manufacturing record rather than a text.
- **Cheapest next move:** Check whether group 3 is one maker by comparing maker marks on the object bases. Status: paused by the workshop confound.

## 19. Paired faces with variable reverse stroke counts (Mahadevan)

- **What was seen:** 3916 surface records; 2906 catalogued objects; 3573 nonempty lines; strict rows 2575; strict unique strings 1659; strict sign inventory 390. 85 strict two-face cup-plus-long-stroke objects; 39 distinct front strings; 8 front strings with a variable reverse count; 4 front strings observed with 2, 3 and 4 reverse strokes; 34 core grid objects. Reverse stroke counts of 1 to 5 correspond to drawn strokes of signs 86, 87, 89, 95 and 96. Contrary number: the 85 two-face objects are a small share of the 2906 catalogued objects.
- **Where:** /home/claude/ivc/research/data/mahadevan_20260905/summary.json; /home/claude/ivc/research/data/mahadevan_20260905/README.md.
- **Old label:** None stated. The file is a catalogue summary.
- **Why it is alive:** The same front string carrying 2, 3 and 4 reverse strokes is a paired test. A numeric tally would show a pattern in the reverse face's area or count, and the 8 variable fronts give within-front comparisons.
- **What it would mean if true:** The reverse strokes are a tally attached to a fixed front, so the front strings are labels with a count.
- **Cheapest next move:** Compare drawn area of the reverse face against stroke count within the 4 variable fronts. This is a purely geometric test on the catalogue. Status: built on the catalogue, untested. MAP.md holds a belief about area falling per extra stroke. That is outside this chunk and was not checked here.

## 20. Counter-face pairs and held-out dictionary matches

- **What was seen:** Counterfield records 4448, 4452 and 5461 share the main face [173, 59, 347, 342, 176] with counter faces [95, 328, 59] or [95, 59, 328]. H-912 and H-1191 have main +400-740-760-220-416+ with counter +220-700-004+; H-1192 has main +400-740-767-220-416+ with counter +700-220-004+. Held-out phonetic dictionary: 4 of 56 whole-syllable matches; 7 of 49 expanded matches; 3 of 36 and 4 of 36 for vowel runs. New accepted translations: 0. Contrary numbers: 4 of 56 is about 7 percent, and no translation was accepted.
- **Where:** /home/claude/ivc/research/data/decoding_followup_20260907/summary.json; the Mahadevan files in /home/claude/ivc/research/data/mahadevan_20260905/.
- **Old label:** No accepted translation. Phonetic matches are recorded only.
- **Why it is alive:** The same five-sign main face recurs across three counter-face records, and the 220 and 700-004 pair recurs across H-912, H-1191 and H-1192. A counter face would then be a gloss in fixed form.
- **What it would mean if true:** The counter face is a fixed translation of the main face, a bilingual frame.
- **Cheapest next move:** Run the held-out dictionary on a fresh set of held-out items that was not used to choose the matches. Status: paused. No translation accepted.

## 21. Phytographic symbol with 158-806

- **What was seen:** Bigram 158-806 with symbol Phyt: z 12.84, worst null share 0, support 5. The file records that it closed on the pre-set support floor, with the note "3 below floor 5". That note does not match support 5 on its face, and it needs reading against the file before use. Contrary number: the support is 5 rows.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/vector4_targeted_context_nulls_20260531_summary.json.
- **Old label:** Closed on the pre-set support floor; not claim-eligible. The file says this is not a failure of the test.
- **Why it is alive:** z 12.84 with worst null 0 is a clean pattern on five rows, and it agrees with the context split in entry 4, where 158 leads to the phytographic lane.
- **What it would mean if true:** 158-806 is the phytographic marker that the entry 4 split describes.
- **Cheapest next move:** Reconcile the support count with the floor note, then add H-series rows carrying Phyt to reach the floor. Status: paused on the floor.

## 22. Local 110 as Parpola sign 41 (H-2148 branch)

- **What was seen:** Local token 110 appears in six rows (an earlier count of three was corrected). H-940, H-2147 and H-2148 form the three-object Parpola sign-41 branch. H-2148 is the cleanest count-mapped target: a one-sign face in H2001-5142, Kenoyer 2005 Figure 14.1. The role inference is recorded as "strong same-role inference". The Parpola reverse-side clue matches the shorter companion row in all seven checked objects (role consistency only). Contrary numbers: Mayig P041 maps to Parpola V141, Wells W112 and Mahadevan M034, so the naive numeric shortcut from 110 to 41 is rejected. M-77 is source-visible on CISI India n68, which creates a source-normalization conflict with the Parpola recurrence control.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/h2148_*; h940_*; p041_*; parpola1994_sign41_convention_gate*; parpola41_mayig_namespace_probe*; m77_parpola_recurrence_conflict_gate* (all in reports/).
- **Old label:** The local 110 to Parpola 41 crosswalk is unaccepted. The naive numeric shortcut is rejected.
- **Why it is alive:** The role inference holds across the three objects, and H-2148 gives a count-mapped one-sign face.
- **What it would mean if true:** Local 110 is Parpola sign 41, which gives one local sign a published reading in a standard list.
- **Cheapest next move:** Decide which Parpola numbering applies (1994 or 2019) by checking Kenoyer Figure 14.1 against the 1994 sign list. Status: paused on namespace resolution.

## 23. Stored order on the Mayig P-namespace and on Mohenjo-daro seal rows

- **What was seen:** Mayig P-namespace directionality is 0.94375 on exact-collapsed rows (null share 0.075); its harsh subset is 0.666667 (null share 0.05). Mohenjo-daro SEAL:S, one site and one type with 138 rows in the file: actual higher than reversed in 130; reversed higher in 4; 3 ties (the three counts sum to 137, so one row is unaccounted for); mean actual-minus-reversed 5.549892. With edges 740 and 002 removed: actual higher in 114, reversed higher in 12, mean 2.594706. Contrary number: the Mayig harsh subset (0.666667) is well below the Indus harsh figure (0.841096).
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/direction_order_baseline_summary.json; effective_unicity_directionality_comparator_summary.json (Mayig rows) (same directory).
- **Old label:** The directionality comparator treats directionality as non-diagnostic. No separate verdict for Mayig.
- **Why it is alive:** The seal-level order holds after the two most common edges are removed (114 against 12), so the signal is not just those two edges.
- **What it would mean if true:** The Mayig text also has stored order, which gives a second script with the same direction signal.
- **Cheapest next move:** Rerun the seal-level stored-order test on the Mayig rows with a site split. Status: tested once.

## 24. Mirrored-writing correction risk on H-1302, H-1303 and H-1822

- **What was seen:** A published article names H-1302, H-1303 and H-1822 as mirrored-writing cases after a comparison with CISI. The provenance gate file treats them as correction-risk acquisition priorities. This reader did not read the file in full.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/h1302_h1303_source_provenance_gate_summary.json.
- **Old label:** Correction-risk acquisition priority.
- **Why it is alive:** If these three rows are mirror images, their stored order in entries 1 and 23 is reversed, and they pull the stored-win share down rather than holding it up. Their effect on row counts is small, but it can be measured.
- **What it would mean if true:** Some stored-order counts depend on mirror-image sources, so the directionality share needs a source-side audit.
- **Cheapest next move:** Drop the three rows from the directionality set and recompute stored_win_share. Status: paused.

## 25. Sign 390 as a host marker that inherits X-subtype continuation

- **What was seen:** After a framed 390 (002 frame), 11 of 15 successors fall in the framed X set (0.733). Unframed 390 gives 78 of 249 (0.313). Holdout: non-390 rows with the same X cover 12 of 15 rows with 390, and pass 12 of 12 covered rows. Uncovered or tied: M-70 (tie on 692), M-232 (707, uncovered) and -:3335.1 (tie on 590). Predictor on the collapsed scope with head_x_pair: 0.913043 (63 of 69 covered); raw 0.958678 (116 of 121). Contrary numbers: x_slot_sign (raw 0.765182) and scope_cell (raw 0.694545) both sit well below.
- **Where:** /home/claude/ivc/research/data/open_prototype/reports/campaign_032_002_861_002390x_expand_390_non390_holdout_20260531_summary.json; campaign_032_002_861_002390x_expand_002_frame_marker_control_20260531_summary.json; campaign_032_002_861_002390x_consolidate_family_collapse_predictor_20260531_summary.json (same directory).
- **Old label:** EXPAND_390_RIGHT_EDGE_HOST_BY_X_SUBTYPE: survives_first_holdout.
- **Why it is alive:** 12 of 12 covered rows pass the holdout, and framed and unframed 390 differ in successor behaviour (0.733 against 0.313).
- **What it would mean if true:** 390 is a host or container sign whose continuation is set by the X subtype, not by a value of its own.
- **Cheapest next move:** Check the three uncovered or tied rows (M-70, M-232 and -:3335.1) for a different X subtype, then run the holdout on a second set of sites. Status: tested once. Survives the first holdout.

---

## Negative results kept for the record

- **Meluhha external anchors (research/data/meluhha/):** No external phonetic candidate survives. The forger null share is 1.0 for each positive target (me-luh-ha, ma2-me-luh-ha, lu2-sun2-zi-da, szu-i3-li2-su). Name detector false-positive rates: lu2-sun2-zi-da 0.933333; szu-i3-li2-su 0.994286. The one strict object-level attempt (3898.1 / U17649) was rejected: U17649 is Indus-only, and target-site shuffled nulls reproduce the same strict pattern in 0.6857 of iterations. Gadd 3899.1 / U8685 was verified, with zero micro-bilingual objects. BM 120573 (U.7683) is cuneiform-only, with nineteen source-side phrases kept as cuneiform context leads only.
- **Decoding follow-up (entry 20):** New accepted translations 0.
- **Brahmi real-token low-null reaudit:** 21 rows; none survives.
- **400 primary face (research/data/open_prototype/reports/risky_400_primary_face_heading_forger*):** Within-artifact side-shuffle p = 0.175. Demoted.
- **465 terminal subseries (risky_465 file):** Terminal Fisher right tail 0.0770, exact dedup n 1. Stopped as a promoted candidate.
- **752-615 to 503 (risky_752615503):** Raw 29 of 29, but exact dedup leaves 2 cells from one site (a copy family). Stopped as a general structural candidate; kept as a local TAB:C formula.
- **Restricted tail forger (entry 13):** Not promotable under the forger.
- **Lothal in the directionality set (entry 1):** Open, not resolved as negative. Listed as the split to run.

---

## Sources on disk

- /home/claude/ivc/AGENTS.md: binding rules for the sweep (read in full).
- /home/claude/ivc/sweep/TASK.md: sweep job description (read in full).
- /home/claude/ivc/sweep/chunks/chunk_13: the 486-path reading list for this reader.
- /home/claude/ivc/research/data/open_prototype/reports/effective_unicity_*_summary.json: directionality (comparator, site profiles, site balance, influence, skeptic, policy, formula family, block holdout), masked-sign, known-script, SumTablets and real-world comparators.
- /home/claude/ivc/research/data/open_prototype/reports/lipi_structured_null_summary.json and lipi_synthetic_comparator_summary.json: structured nulls and length-frequency shuffles on the Lipi rows.
- /home/claude/ivc/research/data/open_prototype/reports/lipi_metadata_prediction_summary.json, lipi_stratified_class_summary.json and lipi_class_field_audit_summary.json: class-code prediction and the source-field audit.
- /home/claude/ivc/research/data/open_prototype/reports/lipi_leakage_control_summary.json: leakage-controlled holdout by type.
- /home/claude/ivc/research/data/open_prototype/reports/lipi_frame700_subtype_*.json and frame700_034_size_tier_heldout_20260712_summary.json: sign 034 size-tier work.
- /home/claude/ivc/research/data/open_prototype/reports/lipi_short_mark_functional_codebook_summary.json and lipi_multiside_mark_summary.json: short-mark role counts.
- /home/claude/ivc/research/data/open_prototype/reports/vector4_*.json, campaign_520_220_x_*.json, campaign_unit_boundary_520_vs_220_summary.json and campaign_a_220_x_240_contrast_summary.json: context associations, the 520-220 slot, and the 240-032 contrast.
- /home/claude/ivc/research/data/open_prototype/reports/risky_*.json and consolidate_formula_operator_maxstat_20260531_summary.json: exact successor formulas and the maxstat tournament.
- /home/claude/ivc/research/data/open_prototype/reports/campaign_032_002_861_*.json: bridge-lock, 533 717 register, and 390 holdout results.
- /home/claude/ivc/research/data/open_prototype/reports/crosswalk_lipi_to_mayig_candidates.csv and crosswalk_summary.json: positional crosswalk from Lipi to Mayig.
- /home/claude/ivc/research/data/open_prototype/reports/direction_order_baseline_summary.json: Mohenjo-daro seal stored-order baseline.
- /home/claude/ivc/research/data/open_prototype/reports/h2148_*, h940_*, p041_*, parpola1994_sign41_convention_gate*, parpola41_mayig_namespace_probe*, m77_parpola_recurrence_conflict_gate*: sign-41 branch.
- /home/claude/ivc/research/data/open_prototype/reports/lipi_h2218_h2239_* summaries: H-series three-role template.
- /home/claude/ivc/research/data/open_prototype/reports/parpola_sign60_local220_*.json and replacement_p050_local220_strict_fish_family_source_gate_20260712*: sign 220 fish cluster.
- /home/claude/ivc/research/data/open_prototype/reports/h1302_h1303_source_provenance_gate_summary.json: provenance gate for mirrored-writing cases.
- /home/claude/ivc/research/data/open_prototype/reports/lipi_scope_rows.csv: Lipi scope rows (2887 numeric-clean rows of 5679 total), including the class column.
- /home/claude/ivc/research/data/open_prototype/README.md: open prototype overview.
- /home/claude/ivc/research/data/brahmi/brahmi_real_token_impostor_forger_v3_summary.json, brahmi_shape_descent_null_summary.json, and the brahmi READMEs: Brahmi comparison gates.
- /home/claude/ivc/research/data/meluhha/*: external anchors and Gadd/Ur checks (negative results).
- /home/claude/ivc/research/data/mahadevan_20260905/summary.json and README.md: Mahadevan surface catalogue.
- /home/claude/ivc/research/data/decoding_followup_20260907/summary.json: counter-face and held-out dictionary results.
- /home/claude/ivc/research/data/sign_crosswalk/README.md: crosswalk audit and pressure pairs.
- /home/claude/ivc/research/data/quarantine/README.md: quarantine rules for the botched-run artifacts.

## Ideas named but never run

- Within-artifact shuffle null on the Lipi-to-Mayig crosswalk alignment (entry 6).
- Source-image check of H-1930 and M-855 to see whether 817 and 861 are one glyph or two (entry 7).
- Print-resolution images of M-37, H-938 A and H-940 A for the 220 fish family (entry 8).
- Remeasurement of the 309 eligible rows under one protocol for sign 034 (entry 9).
- Rerun of the class-code nulls at 1000 iterations, and location of the upstream class definitions (entry 10).
- Alignment count of the quarantined translation column against sign rows, read for autopsy only (entry 11).
- Graphic-identity check of H-1137, H-1138 and H-1846 for the 603 lock (entry 12).
- Collection of no-icon SEAL:R rows from unseen objects to test 533 717 (entry 13).
- Site-only and type-only nulls for the 407 opener (entry 16).
- Maker-mark comparison across manufacturing groups in the H-series (entry 18).
- Geometric comparison of reverse-face area against stroke count in the four variable Mahadevan fronts (entry 19).
- Held-out dictionary run on a fresh held-out set (entry 20).
- Reconciliation of the 158-806 Phyt support count with its floor note (entry 21).
- Kenoyer Figure 14.1 check against the 1994 Parpola sign list, to fix the sign-41 numbering (entry 22).
- Stored-order rerun on Mayig rows with a site split (entry 23).
- Removal of H-1302, H-1303 and H-1822 from the directionality set, then recomputation of stored_win_share (entry 24).
- Check of the three uncovered or tied 390 rows, and a holdout on a second set of sites (entry 25).
- Length-matched rerun of the Indus and Linear B gapped masked-sign tests (entry 2).
- Within-site-type split of the 240-032 contrast with object-level dedup (entry 14).
- Lothal split by source convention (entry 1).
