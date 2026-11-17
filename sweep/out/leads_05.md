# Leads from reader 05 (salvage sweep, chunk_05)

Scope: all 36 files on chunk_05, read end to end. Numbers are copied from the old notes and their summary files on disk; nothing was re-run. Paths are relative to /home/claude/ivc. Old verdict words are kept only as labels.

### Stored-order bigram asymmetry survives every control
- What was seen: Leave-one-row-out bigram scoring, stored sequence against reversed sequence. Harsh Indus scope (365 rows) gives stored-win share 0.841096, with max null 0. Under site|type|symbol block holdout it is 0.827397 (null 0). Mohenjo-daro alone 0.816038 (null 0.002); Harappa alone 0.741071 (null 0.004); site-balanced median 0.803571 (max paired null 0.003 over 1,000 iterations). Exact-duplicate-collapsed broad Lipi baseline: stored order beats reversed in 1,705 of 1,798 collapsed rows. Random-flip null on the policy-controlled set: mean 0.471134, p95 0.526027, against 354 R/L rows and 11 L/R rows. Comparators on the same scoring: Linear B Series D 0.996403; SumTablets 0.935484; Pictish 0.802139; Kudurru 0.666667; totem 0.654472; weather icons 0.503733; barn stars 0.072165.
- Where: research/docs/archive/effective_unicity_directionality_comparator.md; research/docs/archive/effective_unicity_directionality_block_controls.md; research/docs/archive/effective_unicity_directionality_site_balance.md; research/docs/archive/effective_unicity_directionality_site_profiles.md; research/docs/archive/effective_unicity_directionality_policy_controls.md; research/docs/archive/effective_unicity_methods_note.md. Summaries: research/data/open_prototype/reports/effective_unicity_directionality_comparator_summary.json, research/data/open_prototype/reports/effective_unicity_directionality_block_controls_summary.json, research/data/open_prototype/reports/effective_unicity_directionality_site_balance_summary.json, research/data/open_prototype/reports/effective_unicity_directionality_policy_controls_summary.json. Tool: research/data/open_prototype/tools/effective_unicity_directionality_comparator.mjs.
- Old label: "directionality" not promoted. The notes cite the R/L field as a source convention: the field was copied from Yajnadevam/Lipi `dir.` into metadata_filtered.csv and was not computed from source images (research/docs/archive/evidence_ledger.md, M-1206 provenance entry). Leave-site-out drops it to 0.753425 (null 0.100).
- Why it is alive: The asymmetry is not one site, not one object type, not one symbol family, and not one row. Every hostile holdout and every resampling leaves the null at 0 or near 0. The only remaining rival is a metadata convention, and a convention that flips with the reading direction of the scribal hand would still be a real linguistic signal. The Lipi `dir.` field is the best available proxy for the order in which signs were written, so its agreement with stored order is data, not noise.
- What it would mean if true: Stored order in the Lipi corpus is reading order, and the direction field records it. Bigram directionality can then be used as a test for affix position (prefix against suffix), and the directional frames found below (I...T scaffolds, 060-920 cap) become positional grammar rather than coincidence.
- Cheapest next move: Re-score the harsh scope on tablets only and on seals only, separately, using the existing comparator script, and print both stored-win shares next to the R/L counts. That splits the convention question from the medium question in one run.

### Lothal breaks the directional signal
- What was seen: Lothal alone gives stored-win share 0.312500 with null 0.988. Adding Lothal to the balanced Mohenjo-daro plus Harappa sample drops the median and the null rises to 0.528. Everywhere else the asymmetry sits between 0.74 and 0.83.
- Where: research/docs/archive/effective_unicity_directionality_site_profiles.md; research/docs/archive/effective_unicity_directionality_site_balance.md; research/data/open_prototype/reports/effective_unicity_directionality_site_profiles.csv.
- Old label: The site profile was logged as a failed site, and the balanced result was reported with Lothal removed.
- Why it is alive: AGENTS.md says a reading that works at one site and not another is information. Lothal is the one site outside the Mohenjo-daro and Harappa core, and its inscriptions are a different medium mix. If stored order is reading order, Lothal should look the same. It does not, so either Lothal uses another convention or the signal is a Mohenjo-daro and Harappa writing habit.
- What it would mean if true: The Indus writing system had at least two local conventions for order, one of them associated with the Indus heartland cities, and Lothal's text is in the other one.
- Cheapest next move: Count Lothal rows by medium (seal, tablet, other) and by the dir. field. Then score the Lothal seals alone against the Mohenjo-daro seals alone, so the site effect and the medium effect are separated.

### H-1682: a seal described left-to-right next to R/L tablets
- What was seen: Meadow and Kenoyer 2000 Fig. 4.1 is the steatite seal H96-2796/6876-01, locally H-1682. Lipi row 810.1 records H-1682 as type SEAL:S with dir. R/L, text +154-003-617-033+. The source describes its text as left-to-right on the seal. The matched tablets H-2218 to H-2239 are recorded R/L. H-1682 is one of 365 scored rows and favors stored order by 10.091788 log-probability units (2.018358 per transition). Dropping it moves the harsh share from 0.841096 to 0.840659 (difference 0.000437).
- Where: research/docs/archive/effective_unicity_directionality_physical_orientation_closure_20260712.md; research/data/open_prototype/reports/effective_unicity_directionality_influence_rows.csv (row H-1682, scope all_harsh); research/data/open_prototype/reports/effective_unicity_directionality_influence_families.csv.
- Old label: "Physical-direction promotion CLOSED" (the 2026-07-12 closure note). Reason given: H-1682 shows that `dir.` is not one physical-orientation label across seal and tablet media.
- Why it is alive: The closure note read a counterexample as a refutation of the label. The stronger reading is that the R/L field tracks the face or impression orientation of the object and not the text. A seal is read from the impression, a tablet from the face, so one object type can flip relative to the other. That is a measurable mechanism, and it predicts that the Lipi direction label is a medium-relative coordinate, which the stored-order result would then absorb.
- What it would mean if true: The 0.841 asymmetry is about stored sign order plus a medium-relative label. Reading direction can be recovered for any object from its physical form, and the Lipi dir. field becomes a lookup of medium and face, not of language.
- Cheapest next move: Four-field object labels (face, image vs impression, transformation applied to get the reading, proposed direction) for H-1682 and for the eleven H-2218 to H-2239 tablets. Then check whether the seal and tablet flip is predicted by the transformation field.

### Frame I...T scaffolds run forward and die reversed
- What was seen: Formula pattern probe for scaffolds that start with I and end with T: 22 raw forward hits, 0 reversed, and 1.25 under the shuffle null. Mayig gives 23. Anchor frames L740...L817 (6 rows), L740...L861 (4 rows), and the P385 merge L740...P385 (10 rows).
- Where: research/docs/archive/formula_pattern_probe.md; research/data/open_prototype/reports/formula_pattern_summary.json; research/data/open_prototype/reports/formula_pattern_sequences.csv; research/data/open_prototype/reports/formula_anchor_pairs.csv; research/data/open_prototype/reports/formula_class_transition_counts.csv.
- Old label: Probe only; the note stops short of a formula claim. The shuffle null is recorded but not interpreted.
- Why it is alive: 22 against 0 in reverse, with a shuffle expectation of 1.25, is a directional result of the kind the stored-order asymmetry predicts. The L740 frame is the same 740 opener that the register family and 060-920 cap use, so the scaffolds may be one grammar seen from three ends.
- What it would mean if true: Indus formulae have a fixed opening at 740 and fixed closing units (817, 861, 920, 385). The scaffold is a template that a reader can fill, not a coincidence of adjacent signs.
- Cheapest next move: Split the 22 I...T hits by site and by medium and check whether the 740 opener and the closing unit appear in each site's inscriptions independently.

### Restricted terminal tail 002-861-533-717
- What was seen: In 4,135 strict raw rows (3,074 after exact text/site/type/symbol dedup), 533-717 is the only candidate in the restricted 002-861 tail. Across 144 rows it is 2 of 144 overall; at Mohenjo-daro, inside SEAL:R with no icon, it is 2 of 7. Worst recorded false-positive rate 0.006.
- Where: research/data/open_prototype/reports/campaign_032_002_861_restricted_tail_forger_summary.json; research/docs/archive/findings_dossier.md (line 28); research/docs/archive/evidence_ledger.md (533-717 entry).
- Old label: The one accepted structural finding in the main dossier. The label is "accepted", but the evidence ledger reads it as a restricted tail with a small count.
- Why it is alive: It is the single item that passed a forger with FPR 0.006, so it is the strongest structural result in the file set. Two of seven at one site-and-medium cell is small, but a closing tail that appears only in a narrow context is exactly how a formula end behaves.
- What it would mean if true: 533-717 is a terminal unit that closes a 002-861 tail. Its appearance on an unadorned seal at Mohenjo-daro means a formula closer existed independently of iconography.
- Cheapest next move: Pull all 2 of 144 overall hits and the 5 non-hits in the Mohenjo-daro cell from the restricted-tail CSV, and check each against CISI plates for whether 533-717 really is the last sign.

### 002-Y terminality branches and the 817 partition
- What was seen: All-002 leave-one-out terminality from the y_class field: accuracy 0.885772, Brier 0.097554, logloss 0.331038. The register-only baseline is 0.579158. Adjacent 032-002 gives 0.906250. Post-hoc partition forger: best high-terminal versus low-terminal split puts 817 in 820 partitions against 390, 368, 031 and 220 at z 13.211692 with FPR 0 over 10,000 iterations per null.
- Where: research/data/open_prototype/reports/campaign_032_002_y_matched_terminality_summary.json; research/data/open_prototype/reports/campaign_032_002_y_posthoc_partition_forger_summary.json; research/docs/archive/findings_dossier.md (lines 47 and 49).
- Old label: The 002-Y branch was closed and demoted; the partition forger was labelled post hoc, which the note treats as a reason to ignore it.
- Why it is alive: Post hoc partitions are the expected situation when you search for the best split. A forger that is allowed to find its own best partition and still does not reach z 13 is a stronger control than most, and the null already had that freedom. The 817 closer is the one closing sign in the high-terminal set.
- What it would mean if true: The sign after Y sorts formulae into two families that close differently, and 817 is the closer for one of them. The 002 formula has a branch point, not a flat list.
- Cheapest next move: Recompute the partition with 817 removed from the feature set. If the split survives, it is not a closer label leaking into its own prediction.

### 002-390-X branch: the next sign after 390 depends on 002
- What was seen: 002-390-X field has 15 rows and 10 different next signs after 390. 125 is the largest raw group. The 390-X context adversary kept the 002 conditioning live: generic 390-X alone does not explain 125 or 095 behaviour.
- Where: research/docs/archive/experiment_backlog.md (line 822); research/docs/archive/evidence_ledger.md (entries for 2026-05-29 and 2026-05-30, 002-390-125 and family-collapsed branch ecology).
- Old label: "Next non-acquisition experiment should compare 002-conditioned 390-X behaviour against matched controls." Status is a live branch with no value assigned.
- Why it is alive: Ten next signs from fifteen rows is a branch with real diversity, and the adversary did not kill the 002 conditioning. A sign that changes what follows it depending on what preceded it is a branching formula, which a closer or a case marker can produce.
- What it would mean if true: 390 is a slot whose meaning shifts with the preceding 002. One reading: 002 selects a sub-class, 390 is a head, and 125 is its dependent.
- Cheapest next move: Build the matched left-context control named in the backlog: 002-390-X rows against 002-non-390 rows with the same immediate predecessor, and compare next-sign entropy.

### Post-Y tail decisive rows (M-240, M-91, M-49, M-70, 3335.1)
- What was seen: 207 continuing post-Y instances. Five decisive rows: M-49 (002-300-350-032-190), M-240 (+520-240-220-032-002-861-603+, on CISI India IA leaf n95, printed p.60), M-91 (+740-100-798-220-032-002-861-255-416+, on CISI India IA leaf n71), M-1677, M-70 (+226-032-002-390-692+, the row-level source-visible one), and unknown 3335.1. Token/order adjudication passed M-49, M-240, M-91 and M-70 at medium confidence on the visible plates.
- Where: research/docs/archive/evidence_ledger.md (2026-05-28 entries); research/docs/archive/effective_unicity_directionality_m70_source_pilot.md; research/docs/archive/effective_unicity_m70_blind_token_box_packet.md; research/data/open_prototype/reports/campaign_032_002_branch_tail_token_order_verdicts.csv; research/data/open_prototype/reports/campaign_032_002_branch_tail_token_order_boxes.csv; tmp/032_002_branch_tail_source_acquisition/ (M70 face and impression crops from CISI India n066).
- Old label: M-70 blind packet failed: false-positive rate 0.714286 with yes-only calls and 0.777778 with conservative calls across two reviewers. The packet was labelled "not promoted".
- Why it is alive: The failure is in the reviewers, not the rows. Two independent reviewers over-called positives in the controls, which means the box method is too loose for these crops, while the rows themselves are source-visible. Four rows with plate routes is more source than most of the corpus has. The shared tail 032-002-861 across M-240 and M-91 is a repeated post-Y family.
- What it would mean if true: The 032-002 post-Y tail is a closing family used across sites (M-240 and M-91 share 032-002-861). M-70 and 3335.1 would be its other ends.
- Cheapest next move: Re-run the M-70 blind box with the four row images, using only the family-tail signs, and with the Mohenjo-daro source panels (not overlays) so that the reviewers cannot see the answer.

### 3335.1: an unbound row with a private-collection source
- What was seen: 3335.1 is an unbound decisive row in the 032-002 post-Y tail. The acquisition packet lists two rows that reference a private collection; the Yajnadevam author is the named holder. The 032-002-861-603 family cell links it to M-240.
- Where: research/data/open_prototype/reports/campaign_032_002_861_002390x_3335_acquisition_packet_20260531_summary.json; research/data/open_prototype/reports/campaign_032_002_861_002390x_3335_acquisition_packet_20260531_target.csv; research/data/open_prototype/reports/campaign_032_002_861_002390x_3335_acquisition_packet_20260531_routes.csv; research/docs/archive/evidence_ledger.md (3335.1 entry).
- Old label: Unbound. The source request is logged as sent and unanswered.
- Why it is alive: A row that closes the same tail as M-240 and sits in a private collection is the single most useful object to acquire. Its sign sequence is already in the Lipi metadata, so the only missing piece is a photograph or a reading.
- What it would mean if true: If the 3335.1 image confirms 032-002-861 at its end, the post-Y tail has three independent witnesses and is no longer a single-plate observation.
- Cheapest next move: Send the single-page request for the 3335.1 photograph to the Yajnadevam author (email draft for Cúper to send), and in the meantime search the Lipi metadata for every 032-002-861 row with a private-collection hook.

### 060-920 terminal cap
- What was seen: 060-920 occurs in 53 raw rows (52 exact-collapsed). The 741-060 to 920 route is 31/31 raw and 30/30 exact, across 7 sites. Exact-collapsed all-bigram tournament ranks 060-920 to END at 4 of 3,270 by best successor support. Successor-shuffle null over bigrams with at least 30 exact cells: 0 of 5,000 reached a 30/30 exact-successor formula. Blind packet 1 (narrow 741-060-920): reader recovered 5 of 6 target panels as same-cluster at medium-low or better. Blind packet 2 (broad non-741 060-920): all 6 of 6 positives called cap-like, 5 of 6 controls rejected, one low-confidence false positive. One exact-collapsed row continues past 920: Unknown +740-100-415-927-060-920-031+.
- Where: research/docs/archive/findings_dossier_formula_operator_20260531.md (line 7 onwards, headed "Promoted Candidate: 060-920 Terminal Cap"); research/data/open_prototype/reports/blind_060920_terminal_cap_20260531_answer_key.csv; research/data/open_prototype/reports/blind_741060920_terminal_cluster_20260531_answer_key.csv.
- Old label: The sibling operator dossier calls it a "Promoted Candidate". The main findings_dossier.md contains no entry that names 060-920, so the retraction status could not be confirmed from the notes I read.
- Why it is alive: 0 of 5,000 successor shuffles reaching 30/30 is the strongest null in the file set against an artefact of bigram frequency. The blind controls were built to reject broad matches and the cap still separated positives from controls. The one row that continues past 920 is an exception that a cap can absorb only if the cap is an end-of-field marker, not an end-of-text marker.
- What it would mean if true: 060-920 is a closing formula unit that marks the end of an inscription's content field, portable across sites and object types. The 741-060 feeder would make 741 the head of a closing formula.
- Cheapest next move: Pull the one exact row past 920 (Unknown +740-100-415-927-060-920-031+) and the one row where 920 is not visually terminal, and check both against plate images to decide whether the 920 boundary is a field end or a line end.

### Prefix-806 operator: 154/158 plus 806 maps to 465 through 475
- What was seen: Expanded 154/155/158/100 scope: 32/32 raw and 26/26 exact-collapsed hits. Non-Harappa exact-collapse: 9 of 9 positives against 0 of 41 controls, Fisher p 3.9913249350800554e-10. The earlier non-Harappa holdout was 6 of 6 positives against 3 of 58 controls, Fisher p 0.0000011203829020606104.
- Where: research/docs/archive/findings_dossier_formula_operator_20260531.md (lines 52 to 54); research/data/open_prototype/reports/blind_806_prefix_series_20260531_answer_key.csv; research/data/open_prototype/reports/blind_806_prefix_series_20260531_manifest.csv.
- Old label: The 158-806 Phyt association was retracted in research/docs/archive/findings_dossier.md (line 408 onwards) as a context-sign association; that retraction concerns the Phyt iconography, not the 806 prefix operator, which is a separate claim.
- Why it is alive: The 806 prefix result is not an iconographic claim. It is a sequence operator. Two independent holdouts give p of order 10^-6 and 10^-10 with controls drawn from outside the Harappa site set, so site clustering cannot explain it.
- What it would mean if true: 806 is a prefix that changes a 154 or 158 head into a 465-475 family member. That is a morphological operator, a count or class change, and the 465 through 475 range is a closed set of readings to test.
- Cheapest next move: Check the 465 to 475 successors for a numeric or class pattern (two readings to try: a count suffix, or a case marker), using the Lipi rows where 806 precedes them, then check the blind packet answer key for any positive that breaks the pattern.

### 740 register family: 740-390 to 590 and its siblings
- What was seen: 740-390 to 590 in 40 of 41 raw rows. 740-407 in 16 of 16. 740-405 in 21 of 22.
- Where: research/docs/archive/findings_dossier_formula_operator_20260531.md (the 740-H-590 register family entry); research/docs/archive/evidence_ledger.md.
- Old label: Demoted by M-1669 and C-87 (the dossier's own wording).
- Why it is alive: 40 of 41, 16 of 16, and 21 of 22 are three near-complete sequence matches on different tails of the same opener. The demotion cites two single rows, and a single row is a weak reason to demote a family of three.
- What it would mean if true: 740 is a register opener with three fixed continuations that can be read as a sequence of field entries, similar to the 060-920 cap.
- Cheapest next move: Re-check M-1669 and C-87 against their plate images, since the note names them as the demoting rows.

### 520-220-X terminal frame and the 415 comparanda
- What was seen: 520 starts 263 rows; the slot-2 heads are 220 (59), 033 (52), 240 (44). The 520-220 to 415 continuation is 28 of 59. Seventeen exact 520-220-415 rows, 16 of them from Harappa. Odds ratio for 520-220 is 3.71.
- Where: research/docs/archive/evidence_ledger.md (2026-05-26 unit-boundary campaign; 415 comparanda entry); research/docs/archive/experiment_backlog.md (P0 campaigns for 034/415 and 520-220).
- Old label: The 034 versus 415 allograph question is open: the frame is not promoted because the 415 comparanda are mostly Harappa.
- Why it is alive: 16 of 17 exact rows from one site is a sampling skew, yes, but a 3.71 odds ratio on a 263-row starting set with three named heads is a construction rule rather than a sign coincidence. Each head has a different slot-3 profile, which is the signature of a grammar with separate branches.
- What it would mean if true: 520-220 is a fixed opener that selects 415 as its closing unit, and 034 may be its allograph in another site.
- Cheapest next move: Count 520-220-415 against 520-220-034 at each site separately; if 415 appears only at Harappa and 034 only elsewhere, the allograph question has its answer as a site split.

### 240 to 032 selector
- What was seen: 240 before 032 has odds ratio 12.59. The 240-220-032 selector contrast ran on 477 220-occurrence rows, 314 clean known-next rows, 251 strict frame-text dedup units and 260 site/type/frame/text block units.
- Where: research/docs/archive/evidence_ledger.md (2026-05-26 entry for the 240-220-032 selector contrast, and the 240 to 032 odds ratio entry).
- Old label: Selector contrast; the pass was reported after a mechanic validation found a definition-label problem and was then repaired.
- Why it is alive: An odds ratio of 12.59 is the largest in the chunk, and it survives both strict dedup and block-level dedup, which is the test most selectors fail. 240 and 032 are also the two tails in the M-240 row, linking the selector to the post-Y tail.
- What it would mean if true: 240 chooses 032 as the next sign, so 240 is a selector class and 032 is its marked successor. Together with the 520-220 frame it gives a two-selector grammar.
- Cheapest next move: Test the selector on the 032-002 post-Y rows alone: does 240 predict 032 across M-240 and M-91 without the 220 slot in between?

### 603 bridge
- What was seen: 603 bridge is recorded as an X-before-240 family cell in the evidence ledger. M-240 is +520-240-220-032-002-861-603+, which puts 603 at the far end of the 240 row.
- Where: research/docs/archive/evidence_ledger.md (603 bridge entry); research/docs/archive/evidence_ledger.md (2026-05-28 M-240 entry).
- Old label: Bridge; no value assigned.
- Why it is alive: 603 is the terminal sign of the M-240 row, which is one of the source-visible decisive rows above. If 603 closes 032-002-861, the bridge joins the 240 selector to the post-Y tail.
- What it would mean if true: 603 is a closing sign that appears only after the 032-002-861 tail, making the chain 240 -> 032 -> 002 -> 861 -> 603 a single frame.
- Cheapest next move: Count 603 after 861 across all rows, and compare with 603 after any other tail.

### M-2104 count compound: 700-034 against 700-004
- What was seen: The count-compound stress test on 700-034 (the UIII hypothesis) against 700-004 (UIIII). Full planning corpus: 116 forward 700-034 rows, 14 reversed 034-700 rows, 9 forward 700-004 rows, 0 reversed 004-700 rows. In the narrow 097-700-X frame there is one 034 row (M-2104 +151-097-700-034+) and four 004 rows (M-478, M-479, M-480, M-1425, all +400-097-700-004+). The 097 left context is enriched for 700-004 over 700-034: 4 of 9 against 1 of 116, right-tail Fisher p 0.0000628573.
- Where: research/docs/archive/evidence_ledger.md (M-2104 count-compound entry, 2026-05 rows); research/docs/archive/evidence_ledger.md (M-479 source probe entry); research/docs/archive/experiment_backlog.md (034 P0 campaigns).
- Old label: "count_hypothesis_unvalidated", with no accepted 034 = three, 004 = four, role, or translation. The 004 side collapses to one repeated exact sequence family.
- Why it is alive: The Fisher result is independent of the duplicate problem, because it counts the 097 left context and not the 004 family. The collapse is a reason to treat the 004 evidence as one unit, not a reason to drop the count. The Parpola tablets M-478, M-480 and M-1425 carry the 400-097-700-004 sequence, so the source tablets are independent evidence of the 004 side even if their text repeats. M-2104 has a Marshall no. 532 image and a source route: image-reachable, but failing the exact-count gate.
- What it would mean if true: 700 is a numeral-role marker, 034 reads as three and 004 as four, and the chain 097-700-X is a count compound (a number with a unit). This is the first candidate numerical reading in the chunk.
- Cheapest next move: Resolve the duplicate status of M-479 against CISI India n150 (the notes flag it as duplicate-family risk), then re-run the 4-of-9 Fisher test with M-479 counted once.

### Parpola sign 41, the 110 branch and H-2148
- What was seen: The checked local Lipi metadata has six 110 token rows, not three, and the Parpola branch is count-mapped. H-2148 is Kenoyer 2005 Figure 14.1, object H2001-5142 / 11759-01, an incised fired-steatite flat rectangular tablet. Parpola 2019 groups H-938, H-939, H-1284 and H-2145 as tablets with VIIII on the reverse; H-2240 exactly repeats the local +520-220-415+ companion row, and H-2241 keeps fragmentary 415 pressure.
- Where: research/docs/archive/evidence_ledger.md (H-940/H-2147/H-2148 110 gate entries, H-2148 same-side identity gate, and Parpola obverse recurrence stress gate); evidence/tmp/h2148_h2100_h2152_110_route/ holds the Kenoyer 2000 steatite seals PDF. Note: the Kenoyer 2005 PDF was not located on disk, only the 2000 volume.
- Old label: "Crosswalk decision gate": the 110 to sign 41 crosswalk is blocked on same-physical-side identity; the notes say the clean single-panel source image for H-2148 must be tied to the local row.
- Why it is alive: The strongest defender reads Parpola's sign 41 as a count mark (VIIII on the reverse is a numeral), and H-2148 is a tablet with a clean single panel, which gives the strongest visual match in the file set. The 110 token count is six, not three, which means the local row mapping has already found the extra rows the crosswalk needs.
- What it would mean if true: The 110 sign is the sign-41 numeral in the Parpola list, and the reverse VIIII tablets are its counted instances. That gives a direct, object-level numeral that does not depend on any other reading.
- Cheapest next move: Obtain the Kenoyer 2005 Figure 14.1 image and compare H-2148's single panel with the local row's text; if the 110 row is the reverse of the VIIII tablets, the crosswalk is closed by one comparison.

### Parpola sign 60 as a fish and the local 220 bridge
- What was seen: Parpola 2019 and 1994 anchor sign 60 as the plain fish. Mayig P050 is an undecorated fish witness, and 27 current overlap rows align local 220 to P050. The middle-crop blind check groups the Parpola line drawings as a fish-or-leaf family and finds M-37, H-938 A and H-940 A compatible with it. In the strict gate, three readings split: one sees sign-specific support for S009-S011, and two see only broad fish/leaf neighbourhood support.
- Where: research/docs/archive/evidence_ledger.md (Parpola sign 60 / local 220 fish bridge probe, middle-crop probe, strict fish-family gate); research/data/open_prototype/reports/ Mayig overlap files for P050.
- Old label: Strengthens but does not accept the candidate; the strict gate reads it as fish-neighbourhood support.
- Why it is alive: 27 overlap rows aligning 220 to the fish sign is a count, and the 220 slot is one of the three most frequent heads in the 520 frame. A broad fish family with a sign-specific subset is what an iconic sign looks like when it is drawn in several forms.
- What it would mean if true: The 220 head is a fish-determinative, and 520-220 is a fish-marked head, which ties the frame above to a semantic class (food, fish, a commodity).
- Cheapest next move: Compare 220 occurrences against non-220 occurrences in the 27 overlap rows by site and by medium; if the fish reading is right, 220 should be enriched in fish-bearing contexts from the Mohenjo-daro seals.

### Mayig P041 namespace collision
- What was seen: Parsing all 397 pinned Mayig feature files: P041 maps to V141, W112 and M034, not to Parpola sign 41. Mayig's V041 occurs under P301, described as a small hatched box with diagonal and vertical corner strokes.
- Where: research/docs/archive/evidence_ledger.md (P041 falsification gate and the Parpola 41 / Mayig namespace probe entries); research/data/ Mayig feature namespace probe repo under evidence/tmp/mayig_feature_namespace_probe/ (README at its root).
- Old label: Namespace trap, "rejected as a shortcut". The Parpola 1994 convention source is the one to use.
- Why it is alive: The collision is an observed fact about the Mayig numbering, and it means any earlier Mayig-keyed count of sign 41 used the wrong sign. A namespace collision in a feature table is a systematic error, so it can also be a source of signal if the mapping is consistent within a family.
- What it would mean if true: Mayig's P-numbers index feature families, not Parpola signs, so Mayig counts can be re-keyed to Parpola sign numbers through the V and W columns.
- Cheapest next move: Build the full P-to-V-to-W table from the 397 files and check which P-features map to a single Parpola number; those are the usable keys.

### Formula variant slot: P324 against P385 and the duplicate M-32/M-177 group
- What was seen: Shared-edge-frame pairs 69 observed against 69.620 expected. P324...P385 10 observed against 9.612 expected. Exact duplicate group M-32/M-177 P086 P123 P122 P385. 75 near pairs in 14 frame families. The slot candidate is P324 _ </s> with P095, P265 and P368 as fillers. The variant null gives 129 observed against 159.806 mean, which means fewer variant pairs than an edge-preserving null expects.
- Where: research/docs/archive/formula_variant_probe.md; research/docs/archive/formula_variant_null_model.md; research/data/open_prototype/reports/formula_variant_pairs.csv; research/data/open_prototype/reports/formula_variant_slot_candidates.csv; research/data/open_prototype/reports/formula_variant_frame_families.csv; research/data/open_prototype/reports/formula_variant_null_summary.json.
- Old label: Probe; the null model's lower count was read as no variant structure.
- Why it is alive: The P324...P385 pair (10 against 9.612) is the only edge-pair above expectation, and P385 is the same closer that the L740...P385 merge uses. A slot with three fillers (P095, P265, P368) is a placeholder, a lot of the 75 near pairs may be the same slot filled by different signs.
- What it would mean if true: P324 _ </s> is a slot in a formula that takes numeric or class fillers, and P385 is its closer. The low overall variant count means the slot is rare and specific, not generic.
- Cheapest next move: Check whether the three fillers P095, P265 and P368 are the same sign class in Mayig's own feature table; if they share a class, the slot is a class slot.

### Indus gapped predictability matches Linear B on the IVC-capped control
- What was seen: Gapped held-out Indus score 0.294314 against Linear B Series D IVC-capped gapped score 0.294347 (median rank 3). Masked top-1: Indus 0.279591 (top-5 0.534096); Linear B IVC-capped 0.435897 (top-5 0.698006). Context-profile singletons 93.345009%. Coverage curve from 0.223077 at 10 percent to 0.279591 at 100 percent. Label-symmetry bound log2(V!) gives 4,410.970864 bits.
- Where: research/docs/archive/effective_unicity_known_script_comparator.md; research/docs/archive/effective_unicity_methods_note.md; research/data/open_prototype/reports/effective_unicity_known_script_comparator_summary.json; research/data/open_prototype/reports/linear_b_series_d_gapped_heldout_summary.json; research/data/open_prototype/reports/effective_unicity_degeneracy_summary.json.
- Old label: Comparator; the masked-sign gap to Linear B (0.279591 against 0.435897) is read as Indus being less predictable.
- Why it is alive: The gapped scores agree to four decimal places, which is the number that matters when you ask whether a 1,798-row Indus set carries the same local predictability as a real script. The masked gap may come from the 571-sign alphabet and the 93.345009 percent context-profile singleton rate rather than from the language; this has not been tested.
- What it would mean if true: Indus local sign structure is as strong as Linear B's once the masking is gapped, so a bigram-level reading model would transfer across the two systems.
- Cheapest next move: Run the gapped held-out on Indus with the 513 Linear B Series D rows used as training for the Indus gaps, to check whether the agreement holds across the two training sets.

### Indus is less predictable than synthetic admin and emblem streams
- What was seen: The broad bidirectional predictor scores 0.325865 on the Indus corpus. Simple shuffles do not reproduce it. Structured nonlinguistic generators do, at 0.472924, 0.443351 and 0.415069 (synthetic admin and emblem nulls).
- Where: research/docs/archive/effective_unicity_nonlinguistic_comparator.md (line 60 onward); research/data/open_prototype/reports/effective_unicity_nonlinguistic_comparator_summary.json.
- Old label: Simple shuffles do not reproduce the predictor, so the nonlinguistic null is read as weak. The generators beat Indus, and the notes do not conclude from that.
- Why it is alive: The synthetic streams are more predictable than Indus, so the Indus corpus carries more variation than these admin and emblem generators do. That is a point against a simple tally or emblem reading, and a point for a richer system; the defender would say so, and the number is the only evidence offered.
- What it would mean if true: Indus is more varied than a counting or emblem system, so the case for a language (rather than tallies) gets a number.
- Cheapest next move: Generate ten more synthetic admin streams with the same length and duplicate profile, and check whether any of them reaches 0.325865; if none does, the gap is a stable finding.

### Real-world nonlinguistic and ambiguous comparators
- What was seen: Pictish stones (ambiguous symbol system) top-1 / top-5 0.450292 / 0.614035 (187 sequences, 684 tokens). Barn stars and hex signs (known nonwriting decorative) 0.367123 / 0.673973 (97 sequences). Vinca 0.088561 with null 0.75. Totem 0.085485 with null 0.05.
- Where: research/docs/archive/effective_unicity_realworld_nonlinguistic_comparator.md; research/data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_comparator_summary.json; research/data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_null_summary.csv.
- Old label: Non-writing baselines. Pictish is labelled ambiguous; barn stars is a known nonwriting system.
- Why it is alive: Pictish sits at 0.450292, close to the Linear B IVC-capped level, while the decorative system barn stars is at 0.367123. Pictish is the one real symbol system that is still disputed as writing, so it is the closest published comparator to Indus.
- What it would mean if true: If Pictish is a writing system, Indus stored order is typical of writing and the 0.28 masked score is within range.
- Cheapest next move: Re-score Pictish with the Indus directionality comparator (stored vs reversed); if its share sits near 0.5, the directional signal is specific to Indus.

### Gadd Ur accession bridge: object-level Indus, no bilingual
- What was seen: Gadd 1932 accession 3898.1 (U17649, Gadd 16; Penn PMJ XXX:2) and 3899.1 (U8685, Gadd 15) mapped at object level to Indus objects. Zero micro-bilinguals. The strict mapped onomastic assignment for U17649 is 002=ur; 004=gun3; 328=a; 001=me; 803=luh; 415=ha. BM 120573 (U.7683) is an Indus-style stamp seal with a Sumerian inscription, outside the local external-object rows.
- Where: research/docs/archive/gadd_ur_accession_bridge_audit.md; evidence/tmp/gadd_ur/gadd_1932_33779.pdf (Gadd 1932 text, 33779); evidence/tmp/gadd_ur/pages_10_24_contact.jpg and pages_22_34_contact.jpg; research/data/meluhha/gadd_ur_accession_bridge_audit.csv; research/data/meluhha/bm120573_object_bridge_audit.csv; research/docs/archive/findings_dossier.md (line 611 onward on the onomastic stress test).
- Old label: Accession bridge; the onomastic set is rejected as an anchor because it is unverified. "Rejected anchors" in the stress test.
- Why it is alive: U17649 is a Penn object with a Gadd publication page, which is a real object link, and the strict mapped onomastic assignment gives 002 = ur (city name) and 004 = gun3 (a Sumerian sign value). If the two Gadd objects carry Indus signs with Sumerian reading, that is a cross-script anchor at the object level.
- What it would mean if true: 002 is the sign for Ur, and 415 = ha and 001 = me are pinned by the Ur onomastic context. Four signs get values from a real Mesopotamian name.
- Cheapest next move: Pull the Penn PMJ XXX:2 photograph for U17649 and check the 002, 004 and 415 sign identities against the Gadd 16 drawing on page 10-24 of the PDF.

### AO 22310: Akkadian "interpreter of Meluhha"
- What was seen: Louvre AO 22310, Shu-ilishu cylinder seal, De Clercq plate 9 no. 83. The Louvre gives the language as Akkadian and the inscription as "Shilishu, the interpreter of (the land of) Meluhha". The record is not excavated provenience (attribution by style). Possehl treats a true Akkadian-Meluhhan bilingual as something that might exist, not something AO 22310 supplies.
- Where: research/docs/archive/external_anchor_shu_ilishu_AO22310_candidate_20260611.md; research/data/meluhha/source_images/louvre_AO22310_shu_ilishu_de_clercq_plate9_no83.jpg; research/data/meluhha/source_images/louvre_AO22310_shu_ilishu_de_clercq_plate9_no83.provenance.json.
- Old label: External-anchor candidate; accepted external anchors: 0. The note says it is not a bilingual and carries no Indus text.
- Why it is alive: An Akkadian scholarly record that names a person as an interpreter of Meluhha is a direct attestation of the name Meluhha in Mesopotamian text, which is the only outside source that uses the country name. It can point a search for Meluhhan-language material in Akkadian-language seals and tablets.
- What it would mean if true: The Mesopotamian scribes had Meluhhan interpreters, so a Meluhhan language existed in their administration, and a Meluhhan-Akkadian glossary or bilingual is a plausible object class.
- Cheapest next move: Search Mesopotamian cuneiform for other "interpreter of Meluhha" or Meluhha-language personal names, using the cuneiform attestation files already on disk.

### Failaka: Kjaerum 1983 catalogue targets
- What was seen: Laursen Table 1 gives catalogue targets Kjaerum 1983 cat. 279 and 319 for Failaka. CDLI 1773730 is adjacent to them, not the same object. A physical copy of the Kjaerum catalogue is needed to confirm.
- Where: research/docs/archive/failaka_kjaerum_acquisition_20260531.md; research/data/meluhha/failaka_kjaerum_acquisition_20260531.csv; research/data/meluhha/failaka_kjaerum_acquisition_20260531_summary.json; tmp/v1_external_acquisition_20260531/ (Aarhus, CINII, OpenLibrary and DAINST pages, and cdli_publication_1773730_kjaerum_failaka.json).
- Old label: Acquisition target, not an anchor. The adjacent CDLI object is not confirmed.
- Why it is alive: Failaka is an Indus-age Gulf site with Indus-style material, so catalogue entries 279 and 319 could be Indus seals or tablets in Mesopotamian context. The DAINST Gulf-Indus reference PDF is already on disk.
- What it would mean if true: An Indus object found in a Mesopotamian-Gulf context gives an object-level bridge with a dated stratum.
- Cheapest next move: Read the DAINST Gulf-Indus reference PDF (tmp/v1_external_acquisition_20260531/dainst_gulf_indus_reference.pdf) for any mention of Kjaerum 279 or 319 before asking for the physical catalogue.

### Brahmi descent (failed, kept as a stress filter)
- What was seen: Shape-descent test of Indus source tokens against 1,342 early Brahmi glyph features from 36 Indoskript manuscripts and 611 Indus source-token features from 61 projection-gap rows. 83 sign/orientation families with at least 2 samples; all 83 failed; candidate-only rows 0 and accepted anchors 0. Near-misses: 817=dhya, 527=ra, 472=ra, 060=ka, 061=ra. Earlier local 220 probes: top neighbours kam, o, ka, with random shape-evolution nulls equal to or beating observed nearest distances at 0.576000, 0.438000 and 0.656000.
- Where: research/docs/archive/findings_dossier.md (lines 567 to 611, 781 to 806, and 825 to 827); data/brahmi/ directory named in the dossier (not located on disk under the same root).
- Old label: Retracted as phonetic anchor and as language identification. The notes call the route reusable infrastructure only.
- Why it is alive: 817 and 060 are two of the signs the 817 partition and the 060-920 cap depend on, so the near-misses name readings that the other finds can test. The shape null is the honest rival, and it is now recorded.
- What it would mean if true: 817 is a dhya-type syllable closing a 002-861 tail, which would give a phonetic value to the closer identified in the partition find.
- Cheapest next move: Use the v3 pre-review filter (named in the dossier) on 817 and 060 only, with a visual check against the Brahmi source panels, before any further shape test.

### Unbound objects: Dholavira 4237.1 and M-1825
- What was seen: Dholavira 4237.1 (ZA-12:2) is unbound and repeats 705. M-1825 (BJ25710) is a sign-band dark row. The 2026-05 and 2026-06 source requests for these rows are logged as sent and unanswered.
- Where: research/docs/archive/evidence_ledger.md (Dholavira 4237.1 and M-1825 entries); research/docs/archive/experiment_backlog.md (acquisition list).
- Old label: Unbound; source-dark.
- Why it is alive: A repeated 705 at Dholavira is a second site for the 520-033-705/706 construction (520-033 gives 705/706 in 45 of 52), so Dholavira would test whether the 520 frame reaches a second city.
- What it would mean if true: The 520 frame is a Harappa-Dholavira construction, not a Harappa-only one.
- Cheapest next move: Send the Dholavira 8758 request as already drafted, and check the 520-033-705/706 frame for Dholavira rows in the existing Lipi metadata.

### Sources on disk

- research/docs/archive/*.md (36 chunk notes): the directionality, known-script, nonlinguistic, formula, Parpola, external-anchor and dossier files named in each entry above.
- research/docs/archive/findings_dossier.md (877 lines): full ledger; one accepted structural finding (002-861-533-717).
- research/docs/archive/findings_dossier_formula_operator_20260531.md: 060-920 cap, prefix-806 operator, 740-H-590 register family, {090,091} external circular cap.
- research/docs/archive/evidence_ledger.md (376 lines): dated evidence entries for 034/415, 520-220, 240-032, 603, 3335.1, H-series, Parpola 41 and 60.
- research/docs/archive/experiment_backlog.md (850 lines): ordered queue, acquisition status, P0 campaigns.
- research/data/open_prototype/reports/effective_unicity_directionality_*.csv and *_summary.json: comparator, block, site, policy, route, skeptic, influence and source-queue outputs.
- research/data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_*, blind_packet_* and m70_blind_token_box_*: blind packet manifests, answer keys and reviews.
- research/data/open_prototype/reports/blind_060920_terminal_cap_20260531_*, blind_741060920_terminal_cluster_20260531_*, blind_806_prefix_series_20260531_*: answer keys and manifests.
- research/data/open_prototype/reports/campaign_032_002_861_restricted_tail_forger_summary.json; campaign_032_002_y_matched_terminality_summary.json; campaign_032_002_y_posthoc_partition_forger_summary.json.
- research/data/open_prototype/reports/campaign_032_002_861_002390x_3335_acquisition_packet_20260531_*: 3335.1 target, routes, blockers, search queries.
- research/data/open_prototype/reports/formula_pattern_*.csv and formula_variant_*.csv: scaffold, anchor and variant pair outputs.
- research/data/open_prototype/reports/frame700_034_size_tier_heldout_20260712_*: size-tier gate predictions and nulls.
- research/data/open_prototype/reports/effective_unicity_known_script_comparator*, effective_unicity_degeneracy_*, linear_b_series_d_gapped_*: known-script and degeneracy outputs.
- research/data/open_prototype/reports/effective_unicity_nonlinguistic_comparator*, effective_unicity_realworld_nonlinguistic_*: nonlinguistic comparator outputs.
- research/data/open_prototype/lipi/metadata_filtered.csv: Lipi metadata with the dir. field and sign strings.
- research/data/open_prototype/known_scripts/linear_b_series_d/Samples.txt and known_scripts/sumtablets/ (line sequences, sample rows, source manifest).
- research/data/open_prototype/nonlinguistic/sproat2014/ (corpora.zip, extracted sequences, manifest); research/data/non-linguistic-symbols/corpora.zip.
- research/data/open_prototype/tools/: the .mjs and .py scripts for each comparator, forger, blind packet and route probe named above.
- research/data/meluhha/external_indus_objects.csv; gadd_ur_accession_bridge_audit.csv and _summary.json; bm120573_object_bridge_audit.csv; failaka_kjaerum_acquisition_20260531.csv and _summary.json; cuneiform_attestations_expanded.csv; cuneiform_source_routes.csv; control_toponyms.csv.
- research/data/meluhha/source_images/louvre_AO22310_shu_ilishu_de_clercq_plate9_no83.jpg and .provenance.json.
- research/data/meluhha/tools/audit_gadd_ur_accession_bridge.mjs; build_failaka_kjaerum_acquisition_20260531.mjs.
- evidence/tmp/gadd_ur/gadd_1932_33779.pdf (Gadd 1932 text), pages_10_24_contact.jpg, pages_22_34_contact.jpg.
- evidence/tmp/h2148_h2100_h2152_110_route/kenoyer2000_tiny_steatite_seals_harappa.pdf (Kenoyer 2000). The Kenoyer 2005 PDF is named in the notes but was not located on disk.
- evidence/tmp/mayig_feature_namespace_probe/repo/ (Mayig repository at ad2f1e218a34b8c33c57de0d6cb8d99272765bbb; README.md at its root).
- tmp/032_002_branch_tail_source_acquisition/ (M70 face and impression crops from CISI India n066); tmp/032_002_branch_tail_token_order/M70_A_a_token_order_overlay.png.
- tmp/effective_unicity_directionality_blind_packet*/ and tmp/effective_unicity_directionality_public_route_probe/ contact sheets; tmp/effective_unicity_m70_blind_packet/m70_blind_token_box_contact_sheet.png.
- tmp/v1_external_acquisition_20260531/: Aarhus Kjaerum record, CDLI 1773730 JSON, CINII BD0853856X, DAINST Gulf-Indus reference PDF, OpenLibrary OL18985798W.
- tmp/gadd_ur/ (the folder named in the Gadd audit; the PDF and contact sheets sit under evidence/tmp/gadd_ur/).
- research/data/open_prototype/reports/campaign_032_002_861_002390x_* (many campaign reports, including left-context radius scan, 3335 acquisition packet and prefix530 portability files).
- research/data/open_prototype/reports/blind_sidecar_results_20260531.json.
- data/brahmi/ (named in findings_dossier.md; not located under the same root).

### Ideas named but never run

- Four-field object labels (face, image vs impression, transformation, proposed direction) for the Lipi dir. field, to test whether R/L is a medium-relative coordinate (named in the H-1682 closure).
- A new blind packet built to the v2f standard: 12 real signband negatives, 12 real nonlinguistic nulls, 32 fixed-seed synthetic nulls, zero hard or uncertain target-like calls (named in the v2f preflight; never built).
- Same-physical-side identity check for H-2148 against the local 110 row (named in the 110 crosswalk decision gate).
- 002-conditioned 390-X behaviour against matched left-context and full-formula controls (named in the 390-X adversary entry of the backlog).
- Resolve M-479 duplicate-family status against CISI India n150, then re-run the 097 left-context Fisher test with M-479 counted once.
- Grow the 034 size-tier sample; the current margin interval [-0.010581, 0.134992] includes 0. The dimension AUC 0.701087 is a real association, and the gate was failed only on the tier label.
- Pull Mayig P-to-V-to-W table from the 397 pinned feature files, to re-key any Mayig count to Parpola numbers.
- Test whether Lothal seals and Mohenjo-daro seals separate on the stored-order share (named as a site-profile gap).
- Use the Brahmi v3 pre-review filter on 817 and 060 only, with visual checks on the Brahmi source panels.
- Search Mesopotamian cuneiform for other "interpreter of Meluhha" or Meluhha-language names (implied by the AO 22310 external anchor; not run).
- Check Indus gapped predictability with Linear B Series D as a training set for the Indus gaps (implied by the 0.294314 against 0.294347 agreement; not run).
- Re-score Pictish stones with the Indus stored-vs-reversed comparator (not run; the Pictish comparator uses masked and gapped scoring only).
- Generate ten more synthetic admin streams at matched length and duplicate profile, to test whether any reaches 0.325865 (not run).
- Read the DAINST Gulf-Indus reference for mentions of Kjaerum 279 or 319 before asking for the physical catalogue (not run).
- Search for a Meluhhan-Akkadian bilingual; the AO 22310 note says Possehl treats it as something that might exist (not run).
- Count 520-220-415 against 520-220-034 site by site, to test the allograph question as a site split (not run).
- Count 603 after 032-002-861 across all rows and compare with 603 after other tails (not run).
- Build the 740 register family check against M-1669 and C-87 plate images (not run).

- Paid source: Tiedekirja CISI 3.1 at EUR 118.25 (invoice and payment link in research/docs/archive/experiment_backlog.md). It is a paid source; look for a free route to the same plates first and tell Cúper the price and why it matters.
- Acquisition requests logged as sent and unanswered: Harappa/Fuls H-1993 (CISI 3.1 plates 207 to 360); H-319 and H-1284; H-2240 and H-2241; M-1912; group-3 H-2237 and H-2238; Dholavira 8758; M-1825 BJ25710; 3335.1 Yajnadevam author.
