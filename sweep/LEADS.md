# LEADS: merged finds from 15 readers (leads_00 to leads_14)

77 merged entries. Entry numbers are theme.number. Each entry gives readers (R00 to R14), what was seen, best case, boldest reading, cheapest next move, old label last.

## Plain words
- Lipi: three-digit sign catalogue, research/data/open_prototype/lipi/metadata_filtered.csv, 5,679 rows (one per inscribed side). Stored order is Lipi order; reader 14's direction note says it is reversed for R/L texts, so "last in stored order" can be "first in conventional reading".
- Mayig: P-code catalogue (179 overlap records, all Mohenjo-daro unicorn seals; pinned commit ad2f1e218a34b8c33c57de0d6cb8d99272765bbb; 397 feature files carrying Wells W-codes). Wells, Mahadevan (M-codes), Parpola (1994 sign list, 2019 bone rods) are the other catalogues.
- Object IDs: M- Mohenjo-daro, H- Harappa, C- Chanhu-daro, K-, Sktd-1 Surkotada, Ns- Nausharo; row IDs like 3335.1. Types: SEAL:S, SEAL:R, TAB:B, TAB:I, TAB:C (copper), ROD, POT:T:g, TAG.
- Tests: shuffle and forger nulls, Fisher p, held-out, leave-site-out, blind sorts, strict (source-visible) rows, BH q.
- Source conflicts kept, not reconciled: strict rows 4,011 against 4,135; 002 to P122 counts 57/2 against 57/60; whether the note to Andreas Fuls was sent or only drafted (check draft against sent).

## Top 25
1. 1.1 head after 002 sets stop: 379 of 434 closing heads against 0 of 65 (8 readers)
2. 1.5 002/060 governors, leave-site top-3 0.787 against 0.177
3. 1.6 741/742/745 select cap 060-920: 30 of 30, Fisher 1.47e-64
4. 7.1 Lipi numbers equal Wells: 166 of 189 edges, 692 of 784
5. 2.3 prefix 154/158-806 selects 465-475: 6 of 6 against 3 of 58
6. 6.1 H-series: 66 of 66 roles, 64 of 66 texts, p 3.19e-11
7. 1.2 002-390 branch table 15 of 15, p 0.0001998
8. 4.2 034 four full-height against 004: Fisher p 0.0000628573
9. 2.2 520-220-X count slot, 28 of 59, OR 3.71
10. 9.1 407 copper register, 53 of 444 against 17 of 3,059
11. 1.7 533-717, forger rate 0.00018
12. 1.10 240 picks 032: 9 of 12 against 46 of 239, OR 12.59
13. 10.1 stored order: 1,705 of 1,798
14. 7.4 817 and 861 one sign P385
15. 3.1 220 fish in three systems
16. 1.3 matched left: 390 stops 0 of 14, 0 of 20,000 shuffles
17. 1.8 603 lock null 0.0004
18. 1.11 032 lanes, 840 tail 33 rows
19. 8.1 Ur 3898.1 and the Meluhha line
20. 5.1 cup reverse count, 72.69 bits
21. 6.2 700-03x set, 125/109/89 rows
22. 1.15 530 linker, forger 0.0043
23. 1.20 390 host marker holdout 12 of 12
24. 12.1 3335.1 photo
25. 12.2 Dholavira 4237.1 / M-1825

## Rules that predict
- 1.5 terminal governors: top-3 0.787 over 456 leave-site rows against 0.177; 0.761, 0.806, 0.778 with blocks removed.
- 1.1 002-Y partition leave-one-out 0.885772 against 0.579158 (0.884298 against 0.611570 without Mohenjo SEAL:S); open/closed leave-site X 72 of 85, head 40 of 53, visual 61 of 90.
- 2.3 prefix-806: 6 of 6 against 3 of 58; 9 of 9 against 0 of 55; 29 of 29 against 3 of 81; 154-806 16 of 16.
- 1.20 390 host marker: holdout 12 of 12; 0.913043 (63 of 69), 0.958678 (116 of 121).
- 1.2 branch table 15 of 15; strict 4 of 4.
- 6.1 H-series: 66 of 66 roles, 64 of 66 texts; 6.3 codebook masked side 0.525 against 0.099.
- 5.2 and 6.x Parpola reverse clue 7 of 7; 1.3 predecessor 235 22 of 23, and 3 of 3 for 125.
- 1.6 741-060 to 920 30 of 30 (38 of 38 R14).
- 10.1 stored order: leave-source-out 0.832877; Lothal retrain 54 of 58; direction head 0.8913.
- 10.2 masked-sign 0.279591; gapped 0.294314.
- 5.1 roof/tick 3.x gains 7.63, 29.03, 9.31 bits; categorical count 72.69 bits; form predicts face 37 of 44.
- 4.3 034 size AUC 0.701087; 7.8 class code 0.5433 against 0.2895.
- 7.1 Lipi=Wells 166 of 189.

## Finds that touch each other
- 002 head slot: 1.1, 1.2, 1.3, 1.5, 7.4 (817/861 one sign), 4.1 (002 = two strokes), 12.1.
- 520-220-415: 2.2, 3.1 (220 fish), 4.2 (034 four), 6.2, 7.3 (110 person, sign 41).
- 034/033/700: 4.2, 4.3, 6.1, 6.2, 11.1.
- 603, 240, 060-692: 1.8, 1.9, 1.10.
- 407, P086, copper, Meluhha: 7.2, 9.1, 8.1, 2.4.
- 3335.1, 390-590-032, M-143: 1.13, 12.1.
- 705, 4237.1, M-1825: 1.16, 12.2.
## Theme 1. Endings of texts and what governs them

Order note used by the readers: Lipi order is "stored order". R01 and R14 report that the reading-direction note says stored order is physically reversed for R/L objects, so a stored-order "last sign" is a conventional "first sign" (R14: stored-final = conventional opening). Every entry below says "last" or "closes" in stored order unless it says otherwise.

### 1.1 The sign after 002 sets whether the row stops (8 readers: 00, 01, 02, 03, 04, 05, 10, 14)
- Seen: In the all-002 rows, closing heads 817, 820, 861, 824 and 000 stop the row; opening heads 390, 368, 031, 220, 595 and 405 never do. R01, distinct texts, row stops at the head: 861 122 of 150 (raw 140 of 174); 817 120 of 128 (raw 148 of 156); 820 84 of 92 (raw 94 of 102); 000 44 of 55 (raw 47 of 58); 824 9 of 9; 390 0 of 15; 031 0 of 15; 368 0 of 12; 220 0 of 11; 595 0 of 7; 405 0 of 4 distinct (0 of 32 raw, because 29 of the 32 are one string, +520-240-002-405-501+). Pooled: closing heads 379 of 434 distinct texts, opening heads 0 of 65 (naive p near 2e-10). R00/R04/R05 strict dedup, 499 all-002 rows: closure pole 817/820 = 174 rows, branch pole 390/368/031/220 = 43 rows, 861 left out as leaky (119 rows). Terminal counts: 817 100 of 103; 820 66 of 71; 861 95 of 119; 824 6 of 6; 390 0 of 14; 368 0 of 11; 031 0 of 9; 220 0 of 9; 297, 405, 595, 900 each 0 of 4. R10, 272 distinct clean texts with 002 as penultimate: final 817 (89), 861 (85), 820 (62) = 236 of 272 (86.8%). R14 rerun: 861/817/820 after 002 are stored-final in 382 of 432 (88.4%), after any other sign 135 of 206 (65.5%); with every row holding 060, 741, 742 or 745 removed, 382 of 430 (88.8%) against 100 of 163 (61.3%); paper figures pooled OR 2.11 (95% 1.38 to 3.21, permutation p 0.0003), per sign 861 OR 4.0, 817 6.2, 820 4.9 (Holm p 0.007, 0.009, 0.003); 390, 368, 220, 595, 031 are stored-final 0 of 15, 11, 10, 7, 11.
- Best case: The same head set separates inside matched left contexts (entry 1.3: 390 0 of 14 against other heads 125 of 197, zero of 20,000 shuffles). Post-hoc partition: best split z = 13.211692, terminal-rate gap 0.954023, worst false-positive rate 0 over 10,000 iterations in each of six null models. Y-class leave-one-out accuracy 0.885772 against 0.579158 for site/type/symbol (499 rows); with Mohenjo-daro SEAL:S removed 0.884298 against 0.611570; adjacent 032-002 subset alone 0.906250 (R05). Leave-one-site-out open/closed prediction: head identity 40 of 53 (0.755), X identity 72 of 85 (0.847), visual-context proxy 61 of 90 (0.678) (R02). Per-sign baselines: 817 and 820 are stored-final 0.91 and 0.80 anywhere, 390 and 368 0.10 and 0.07 (R14).
- Boldest reading: 002 opens a two-pole slot, closing against continuing, like a verb frame with two conjugations; 861 is the largest head (174 raw rows, 11 times the 390 frame) and was never scored as a frame. Read as a numeral (002 = two strokes, entry 4.1) before a closing sign, it is a count before a noun (R10).
- Next move: Split the head table by site (Mohenjo-daro against Harappa) and type (SEAL:S against TAB:B) on distinct texts; run the length-matched closure test (within each text-length bucket, closure-class Y as last sign against other Y); site-held-out refit on the 499 rows; add M-19 and M-175 (entry 1.18). Counter figure, once: adjacent 032-002 fails the post-hoc partition (z 1.526, false-positive rate 0.5205 for z and 0.7552 for the gap).
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; research/data/open_prototype/reports/campaign_032_002_post_y_all_002_rows.csv; research/data/open_prototype/reports/campaign_032_002_y_posthoc_partition_forger_summary.json; research/data/open_prototype/reports/campaign_032_002_y_matched_terminality_summary.json; research/docs/archive/active_decipherment_attempt.md; research/docs/archive/campaign_002_y_partition_source_queue.md; research/docs/archive/campaign_032_002_y_matched_terminality.md; research/docs/archive/campaign_032_002_y_skeptic_holdout.md; research/docs/archive/methods_terminal_governor_effective_unicity_20260531.md; research/publications/20261001/PAPER_2_v0.2.md (section 7); research/data/open_prototype/reports/campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv.
- Old label: "structural candidate, not accepted"; "real closure/continuation pole split in the metadata layer"; "a replication of a known pattern"; the skeptic note's text-length match scored as a tautology, so the length-matched test was never run.

### 1.2 The sign after 002-390 splits the frame into continuing and closing branches (7 readers: 00, 01, 02, 03, 04, 05, 13)
- Seen: The Lipi file has exactly 15 rows with 002-390 followed by another sign, 15 different full texts, 10 distinct next signs. A table written before the test (continuing: 125, 530, 590; closing: 072, 095, 140, 346, 692, 705, 707) matches all 15 frames; canonical rows 3503; repeated-branch subset 8 of 8; source-route-or-strict subset 9 of 9; strict subset 4 of 4. 125 follows 390 in 4 of 15 rows (M-38, M-119, M-735, Sktd-1) and always continues in frame. The four source-visible rows: M-119 (2646.1 +151-337-484-002-390-125-632-032-900-563+, continues), M-735 (3159.1 +740-760-235-002-390-125-195+, continues), M-70 (2598.1 +226-032-002-390-692+, closes), M-71 (2599.1 +151-279-142-002-390-095+, closes); token-boundary adjudication found all four boxed windows compatible with catalogue order. Outside the frame (R03): 692 terminal 58 of 77; 095 continuing 22 of 30; 125 continuing 38 of 59; 705 continuing 160 of 219. 125 is terminal in 17 rows outside the frame; 095, 692 and 705 continue in 200 rows outside it (R00). 390-125 inside 002-390 is 4 of 4 continuing, outside it 3 terminal and 2 continuing; 390-095 inside 2 of 2 terminal.
- Best case: Prespecified-class label-shuffle p = 0.0001998 (discovery p = 0.0241758); non-frame terminality shuffle false-positive rate 0.00003, repeated-branch 0.00089; cross-head transfer matched 19 of 26 non-390 frames; 530 matched 3 of 3 outside 390. Replacement-forger for 125 (at least four raw rows, at least two strict, no terminal row after the branch): label shuffle 0.004360 (50,000 shuffles), within site/type 0.012460, strict against non-strict 0.017660; the within terminal/continuing bucket gives 0.397360 and site/type/terminal 1.000000. Generic 390-X alone does not explain 125 or 095 behaviour; 002 conditioning stays live (R05). Open predictions already written: H-1993 closes on 095; M-1825 and Dholavira 4237.1 close on 705; Sktd-1 continues on 125.
- Boldest reading: 002-390 is a two-way slot and the photograph shows it: the sign after 390 decides end or go on, and the 2:2 split of the four strict rows runs the predicted way, so the grammar is visible in photographs and not only in catalogue text. All-head post-hoc rank puts 390 first of 9 heads (Bonferroni 0.2176); the table claims the sign after the frame decides continuation, not that 390 is special.
- Next move: Freeze the table and score each source-visible 002-390-X row before reading its photograph; blind token-boxing of the four strict windows (protocol written, not run); per-head polarity table for every focus sign across all rows, not only frames; add a third strict 125 family.
- Where: research/docs/archive/campaign_032_002_861_002390x_risky_parse_model_v1_20260531.md (prespecified branch-table block around lines 809-850); research/data/open_prototype/reports/risky_002390_canonical_branch_selector_forger_20260531.csv (and _frames.csv, _by_branch.csv); research/docs/archive/campaign_032_002_861_002390x_source_normalized_contrast.md; ..._token_boundary_adjudication.md; ..._replacement_branch_forger.md; ..._branch_sign_ecology_20260531.md; ..._source_bound_intrinsic_sign_behavior_recheck.md; ..._family_collapsed_branch_ecology.md; research/docs/archive/experiment_backlog.md (line 822); crops in evidence/tmp/002390x_source_normalization/ (M119, M735, M70, M71 signband files).
- Old label: "frame-conditioned polarity, not a sign value"; 390 "mixed inventory head"; "intrinsic-behaviour shortcut rejected"; "survives tiny"; "live source-normalized structural candidate, not an accepted claim".

### 1.3 Left context sets the menu, the head picks the branch (4 readers: 01, 02, 03, 13)
- Seen: With the complete sign string before 002 as the matching key, the 11 predecessor groups that hold a 390 head and at least two heads: 390 never stops (0 of 14), other heads stop 125 of 197; expected 7.7 stops under label shuffles inside groups; 0 of 20,000 shuffles reached 0 (R01). Predecessor 235, 35 distinct texts: closing heads 861, 817, 820, 824 stop 22 of 23 (exception 2851.1, 861 followed by 360 520 919 140); open heads 031, 460, 717, 392, 906, 390, 405, 220, 374, 065 stop 0 of 12; singleton heads 112, 285, 457 stop 3 of 3. Predecessor 032: 861 stops 8 of 10, 390 0 of 2; predecessor 004: 817 3 of 4, 861 3 of 4, 390 0 of 2 (H-1993 with 095 after, Sktd-1 with 125 after), 365 0 of 2; predecessor 031: 817 5 of 5, 861 6 of 8, 390 0 of 1; predecessor 803: 820 7 of 8, 861 5 of 6, 390 0 of 1. Opening the head set to every 002 head gives 66 predecessor groups (of 139) with two or more heads at radius 1 and 85 radius-2 groups (of 405). R03: one left context, six heads: M-708 left 740-061 takes 817 (2), 390, 400, 455, 575, 703 (1 each); seven of 15 target frames have full-left controls with other heads. Radius scan: splits only at left radius 1 (004 and 032), none at radius 2+; compound-left router groups 004 = 095/125 and 032 = 590/692; provisional router 235 direct; 220-004 -> 095; 390-004 -> 125; 226-032 -> 692; 205-032 -> 590-032. R02: the 15 frames are 15 different texts; the copies sit in 405 (29 of 32 rows, +520-240-002-405-501+, all Harappa TAB:B) and Lothal (+090-740-220-055-001-741-500-705+ 11 rows; +740-048-002-817+ 11 rows, 10 Lothal "Elep" objects), not in the frames.
- Best case: The matched paradigm the old files call missing (same left, different heads, different closure) shows in many groups, not only 004 and 032. The old scan only let heads 390, 125, 095, 692, 705 vote. M-143 and 3335.1 split after the full prefix 740-205-032-002 into 252 and 390 (entry 12.1).
- Boldest reading: The head after 002 is a menu item chosen by a second-stage selector and the left context only supplies the menu; the router collapses to a one-sign selector (the sign before 002) for 004 and 032.
- Next move: Put the 35 texts of predecessor 235 on one sheet with full tails and check whether open heads take a 125 tail (3 of 12 do); apply the four named router cases to the strict layer and count matches; list the sign after each of the six M-708 heads; list every row beginning 740-205 and tabulate heads.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv (rerun scripts /tmp/sweep01/matched_left.py, perm_390.py, heads.py by R01); research/docs/archive/campaign_032_002_861_002390x_left_context_radius_scan_20260531.md; ..._full_left_formula_controls_20260531.md; ..._risky_parse_model_v1_20260531.md ("Forty-Fifth"); ..._near_frame_scout_20260531.md.
- Old label: "Branch alternatives exist only at radius 1 ... source-blocked"; "0 exact full-left groups with multiple 002-390-X branch alternatives"; "strong anti-determinism control".

### 1.4 Per-sign closer tilt and head/tail asymmetry (6 readers: 01, 03, 04, 08, 11, 14)
- Seen: R01, distinct texts, share in which the sign is last: 817 150 of 180 (83%); 091 15 of 19 (79%); 692 52 of 70 (74%); 820 160 of 219 (73%); 861 151 of 216 (70%); 824 13 of 19 (68%). Middle: 000 547 of 1434 (38%); 095 8 of 22; 125 15 of 56 (27%); 705 40 of 169 (24%); 590 42 of 175 (24%). Openers: 390 18 of 235 (8%); 405 5 of 75; 002 27 of 736 (4%); 740 19 of 1382 (1%). Outside the 002-390 frame (raw): 692 stops 58 of 76 (76%), 125 17 of 55 (31%), 705 57 of 217 (26%), 095 6 of 28 (21%). R03: 692 total 58 occurrences, 0 after 861, 47 terminal; 705 total 174 (0 after 861, 48 terminal); 416 total 46 (29 terminal); 698 total 10 (10 terminal); 125 total 50 (15 terminal). R08 edge table: 740 total 1,238, initial 858, terminal 3 (edge share 0.695477); 033 33 initial vs 149 terminal; 032 32 vs 137; 817 1 vs 139; 034 14 vs 107; 861 35 vs 111. R11: 817 terminal share 0.916667 (12 tokens), 861 0.833333 (12). R14: 060 itself is stored-final in 3 of 222 occurrences.
- Best case: Closure is a per-sign tilt that holds whether or not 002 comes before; 817 has never been in a gate. The old rejection of "692 closes" rested on one source-visible continuing 692 (M-21) while its own table already had 58 of 76 closing. Stored-versus-reversed wins survive removal of the top 10 edge signs (entry 10.1).
- Boldest reading: Signs carry a closure value, a grammar-like feature usable before any sound or meaning is fixed; there is a fixed head class (740, 700, 400, 520) and a fixed tail class (032, 033, 034, 817, 820, 861) - a template with an opening and a closing slot.
- Next move: For each sign with 19+ distinct texts, compare its stop rate with that of other signs in texts of the same length; run a null that keeps only each sign's initial-versus-terminal rate and compare its stored-versus-reversed win (never run); check 692's post-861 count of 0 against a random sample of other terminal signs. Contrary number, once: in stored order 740 is almost never last (19 of 1,382); among R/L texts 891 start with 740 and 10 end with it, so the "closing jar sign 740" line reads correctly only with R/L reversal applied; the repo should state which order each claim uses.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv (/tmp/sweep01/sign_terminal.py, orient.py); research/docs/archive/campaign_032_002_861_002390x_branch_sign_ecology_20260531.md; research/docs/archive/lipi_broad_order_baseline.md; lipi_dedup_order_baseline.md; lipi_edge_removed_baseline.md; lipi_family_downweight_baseline.md; research/docs/archive/structural_sign_classes.md.
- Old label: "reject the shortcut that 125 intrinsically means continuation or that 095/692/705 intrinsically mean closure"; "T3 structural scout evidence only".

### 1.5 002 and 060 govern small closer sets, scored on held-out sites (5 readers: 00, 05, 10, 13, 14)
- Seen: Exact-collapsed cells: 002-817 108 (105 terminal), 002-820 75 (70), 060-920 52 (51), 060-550 24 (23), 060-820 23 (23). Terminal-label shuffle p = 0 of 5,000; row-internal order null 0 of 2,000; penultimate-final independence null over 2,127 terminal text families 0 of 5,000. Held-out final-sign prediction, governors 002 and 060: top-3 0.787 over 456 leave-site rows (mean effective candidates 6.39) against 0.177 over 1,138 non-governor penultimate rows (15.71); minus Mohenjo-daro SEAL:S 0.761 (234 rows); minus Harappa SEAL:S 0.806 (407); minus both 0.778 (185). Non-governor comparators: 240 0.652 over 23 rows; 740 0.090 over 133; 220 0.286 over 56; 390 0.127 over 55; 002 frequency confound top-3 0.856 over 313 rows (R10). 060 closes with 920 (45), 692 (26), 820 (20), 550 (19) (R10); 060 is medial in 144 of 145 occurrences and 002 in 439 of 455 distinct texts. Tournament (R13): 002-817 -> END 105 of 108 exact across 10 sites and 9 types; 060-920 -> END 51 of 52 across 9 sites; 002-820 -> END 70 of 75; 002-861 -> END 102 of 126; 740-100 -> 415 27 of 79.
- Best case: Cleanest held-out result in the archive: effective candidates fall from 15.71 to 6.39 and the gap survives every block removed.
- Boldest reading: 002 and 060 are clause-final governors of a closed closing set; the slot grammar has at least one closure operator, and the 002 closing set is the same set as 817/861 (entry 7.4).
- Next move: Rerun leave-site top-3 on TAB:B and TAB:I rows only; collapse by source family and rerun (the note's decisive next test); run M-77 (+832-390-803-002-861+) and M-72 (+740-255-705-140-003-002-861+) through it as held-out texts; rerun with damaged slots at M-55/M-60 set to counting and to non-counting (entry 7.12). Contrary figure, once: the 240 mimic reaches 0.652 on 23 rows, and lower branches (060-550, 060-820, 060-692) fall under the n >= 20 floor without Mohenjo-daro SEAL:S.
- Where: research/docs/archive/brief_terminal_governor_network_20260531.md; research/docs/archive/brief_terminal_governor_unicity_20260531.md; research/docs/archive/methods_terminal_governor_effective_unicity_20260531.md; research/data/open_prototype/reports/consolidate_formula_operator_maxstat_20260531_summary.json; research/data/open_prototype/reports/lipi_scope_rows.csv.
- Old label: "promoted structural candidate, not accepted"; the tournament gives no separate decision for 002-817 and 060-920 -> END.

### 1.6 741, 742, 745 select the cap 060-920 (4 readers: 00, 05, 13, 14)
- Seen: 741-060 is followed by 920 in 31 of 31 raw rows and 30 of 30 exact cells, all 31 ending after 920. 060-920: 53 raw rows (52 exact cells, 51 terminal); predecessor 741 supplies 30 cells, 742 supplies 7, 745 supplies 3; right-tail Fisher p = 1.47e-64; successor-shuffle null (5,000) never reached 30 of 30. 741, 742 or 745 precedes 060-920 in 40 of 52 object-collapsed cells and the sibling caps 060-692, 060-550, 060-820 in 0 of 84. Seven sites (Mohenjo-daro 19, Harappa 5, Dholavira 2, Lothal 2, Chanhu-daro 1, Kalibangan 1, Rakhigarhi 1); types SEAL:S 24, TAB:I 3, TAB:B 2, TAG:P 1, TAG:R 1; witnesses C-16, H-1309, H-2127, H-2128, H-89. R14 rerun on the whole table: 060-920 65 times, 920 stored-final in 64; 741-060 -> 920 38 of 38; 742-060 -> 920 9 of 9. One exact row continues past 920: Unknown +740-100-415-927-060-920-031+. M-105 carries 060-920 beside 000 tokens. Blind packet 1 (741-060-920): reader recovered 5 of 6 as same-cluster; packet 2 (non-741 060-920): 6 of 6 positives called cap-like, 5 of 6 controls rejected, one low-confidence false positive. R13 tournament: ranks 6th by best match (30), mean null max 39.2578 (mean null max share 0.330924); R05 rank 4 of 3,270 by best successor support.
- Best case: 0 of 5,000 successor shuffles reaching 30 of 30 is the strongest null in the archive against bigram-frequency artifacts; blind readers recognise the cap as a picture unit. The May dossier calls it the single strongest frontier result.
- Boldest reading: 741, 742, 745 are three shapes of one selector sign that picks the cap and nothing else; in conventional order 920 opens a text and 741/742/745 + 060 is a fixed opening formula, a title or name slot (R14).
- Next move: Token-boxed source check on the 38 741-060-920 occurrences with real CISI numbers (count plates on disk first); a blind sort of 741-060 rows on TAB and TAG objects; box the exception rows; rerun the tournament with a per-site cap; list the bigrams with the largest stored-minus-reversed margin and see where 060-920 and 741-060-920 fall.
- Where: research/docs/archive/brief_741060920_terminal_formula_20260531.md; research/docs/archive/findings_dossier_formula_operator_20260531.md; research/data/open_prototype/reports/risky_741060920*.json; research/data/open_prototype/reports/blind_060920_terminal_cap_20260531_answer_key.csv; blind_741060920_terminal_cluster_20260531_answer_key.csv; evidence/tmp/blind_060920_terminal_cap_20260531/ and blind_741060920_terminal_cluster_20260531/ (13 JPG each, no key file in the folders).
- Old label: "promoted visual candidate; not accepted"; the brief says do not enter it as accepted until a token-boxed source audit and a stricter graphic null both pass (neither run); not retracted.

### 1.7 The two-sign ending 533-717 after 002-861 (7 readers: 00, 02, 03, 04, 05, 13, 14)
- Seen: 533 occurs in exactly two rows, 2872.1 (M-376, +740-100-176-002-861-533-717+; CISI India n129, p. 94; 39.4 x 11.4 mm; HR 1574426; 7 signs) and 2887.1 (M-391, +405-845-686-740-793-003-233-805-002-861-533-717+; CISI India n131, p. 96; 42 x 10 mm; DK-i 60; 12 signs), both Mohenjo-daro SEAL:R, no icon, cuboid-convex. 717 occurs in 41 to 55 rows depending on filter (R00 41, R02 55, R14 49 rows/55 occurrences, R03 37 independent). In the strict raw layer (4,135 rows; 3,074 exact-deduped) it is the only survivor of the restricted 002-861 tail: 2 of 144 overall, 2 of 7 Mohenjo no-icon SEAL:R, 2 of 3 cuboid-convex no-icon SEAL:R, 0 of 71 Mohenjo SEAL:S. Controls: M-355 (long tail 360-520-919-140), M-1267 (bare), M-1273 (603), M-1954 and M-1973 (bare, source-pending). 861-533-717 closes at 717 both times; 861-603 closes at 603 3 of 3 (all Mohenjo-daro). R14: 531 occurs in five rows (C-75 +740-531-060-692+; H-37 and K-17 +740-531+; M-1911 +621-390-531-002-820+; M-26 +090-740-531-060-692+) and never takes 717; Mayig P228 maps one-to-many to W531 and W533.
- Best case: Forger rates: worst recorded 0.006; global context shuffle 0.00018 (50,000); site-type-symbol shuffle 0.0006; context shuffle 0.0002 globally and 0.0010 inside site/type/symbol. 533 never occurs outside this pair, so it cannot be a free sign that picked up 717; the two rows differ in leaf, excavation ID and length (7 and 12). Row 2422.1 (M-1954, +740-407-590-031-752-033-705-220-415-798-002-861+) places the register and the copper frame on one no-icon SEAL:R cell.
- Boldest reading: 533-717 is a frozen closing unit locked to the uncovered rectangular and cuboid seal register, a register label after 002-861; if 531 and 533 are one family split by the catalogue the pair is a fine-split variant of a broader 531/533 terminal sign.
- Next move: Source-route M-1954 and M-1973 and check their post-861 zone; count 533 and 717 separately outside the pair (717 in unrelated frames means a shared compound); crop 533 alone from M-376 and M-391 through the blind layout gate; collect no-icon SEAL:R rows not yet seen; box the 531 slot on C-75, H-37, K-17, M-1911, M-26; search 533 and 717 outside Mohenjo-daro. Contrary figure, once: row-internal token shuffle false-positive rate 0.0042 with null max support 3, and a broad any-prefix search finds 96 repeated terminal bigram cells in strict raw rows (40 after exact dedup).
- Where: research/docs/archive/campaign_032_002_861_533717_register_test.md; ..._source_family_independence.md; ..._source_layout_discriminator.md; ..._component_ecology.md; ..._blind_layout_gate.md; ..._focus_contrast.md; research/data/open_prototype/reports/campaign_032_002_861_restricted_tail_forger_summary.json; ..._533717_register_test_summary.json; ..._tail_rarity_register_scan_summary.json; research/docs/archive/findings_dossier.md (line 28); research/docs/archive/completion_gap_matrix.md; research/docs/archive/replacement_run_checkpoint_20260712.md; crops in evidence/tmp/032_002_861_533717_*.
- Old label: "accepted structural claim" (restricted-tail finding), later "one single source/register-family cell, not a value"; "restricted_tail_pattern_not_promotable_under_forger"; "taxonomy-sensitive".

### 1.8 603 closes Mohenjo-daro rows after 861 and sits in a Harappa formula (5 readers: 00, 02, 03, 05, 13)
- Seen: 603 occurs in 7 rows (SEAL:C, SEAL:R, SEAL:S, TAB:B). After 002-861: M-240 (+520-240-220-032-002-861-603+), M-714 (3139.1 +740-585-017-033-705-233-798-803-002-861-603+), M-1273 (3580.1 +740-055-002-861-603+). In Harappa the string +740-603-240-060-692+ is on H-1137, H-1138 (Vats Plate XCIV no. 346, p. 345) and H-1846 (Kenoyer and Meadow 1997 Fig. 11.11; H95-2672); 240-060-692 occurs 7 times, always after 740, X = 603 (3), 642 (2), 636 (2). 636 is in 15 of 15 X-before-240 frames and 0 after 861; 642 in 7 of 7 and 0 after 861. H-1138 X-slot is slot 4 under R/L and slot 2 under visual left-to-right. The 2026-07-12 closure assumed five units on H-1138 and flags a possible clipped unit. The closure tested the Lipi number, not the glyph: the Mohenjo-daro post-861 rows end on a ladder/window glyph; H-1846 has a window-like form at one edge (740 forward or 692 reversed).
- Best case: Lock null (20,000 iterations): false-positive rate 0.0004 for 603 locked to 060-692; 0.04 for any bridge sign locked to one subframe. 603 is the only non-background sign in both constructions; two of three Harappa rows are source-visible (H-1138, H-1846); 603 is the only shared sign between the X-before-240 frame (95 strict rows, 28 distinct X signs) and the post-861 tails.
- Boldest reading: 603 is a mobile connector or classifier that closes a Mohenjo-daro seal after 002-861 and a Harappa tablet formula; if the window glyph carries different catalogue numbers in the two places, the numbering split one unit and the glyph is the stable object.
- Next move: Crop the H-1138 edge and count the units; mark H-1138 slot boundaries under both readings; table every Harappa formula row with a window-shaped unit against its Lipi number, extended to 636 and 642; compare H-1846 (Fig. 11.11) with M-1273 (CISI Pakistan leaf n195) at one scale; count 603 after 861 across all rows against 603 after other tails. Contrary figures, once: H-1137, H-1138 and H-1846 may be one copied tablet family; the 0.04 rate shows a lock of this kind is not rare at this scale.
- Where: research/docs/archive/campaign_032_002_861_603_cross_context_graphic_closure_20260712.md; ..._603_mobility.md; ..._603_x240_bridge_hypotheses.md; ..._603_h1138_h360_tokenization_gate.md; ..._603_slot_substitution.md; ..._603_graphic_identity_packet.md; ..._x240_bridge_lock_null.md; research/data/open_prototype/reports/campaign_032_002_861_x240_bridge_lock_null_summary.json; overlays in evidence/tmp/032_002_861_603_slot_source_normalization/, evidence/tmp/032_002_861_603_h1138_h360_tokenization_gate/.
- Old label: "live bridge candidate, not a value"; "Closed: cross-context 603 identity not source-supported"; "bridge_lock_pattern_is_weak_to_moderate_distributional_support_not_a_promotion".

### 1.9 The 240 hinge between X and a closing subframe (1 reader: 03)
- Seen: After 240 the subframe table reads <END> 33 rows; 002-861 9; 060-692 7; 002-817 5; 031-032-171 4. Rows: M-941 +000-642-240-031-002-861+; M-706 +740-773-240-002-861-031+ (same tail 031-002-861 after 240 at different positions, heads 642 and 773); M-280 +740-482-240-002-944-920-140+; M-41 +740-636-240-233-235-002-405-125-820+. 482-X-240-002-861: 8 rows, 7 of them to 002-861, 6 family cells. 636: 15 X-240 rows, 12 family cells; H-360 (Vats XCVIII no. 584) source-visible. 642: 7 rows, 6 family cells; H-1845 (Harappa.com H2000-4484, Fig. 42.05) public route; H-237 metadata-only (ref 424.2). 000 is the bridge control (810 occurrences).
- Best case: The three largest named post-240 classes after <END> are all closing or near-closing forms; 482 is the closest non-603 sign to 603's bridge behaviour.
- Boldest reading: 240 is a terminal-approach marker, the hinge that moves a branch into closing material; X-240 is a class of signs with a shared bridge role and 603 is the member whose subframe locks.
- Next move: Count after-240 subframes across the full strict layer and compare the terminal share of 240-followed rows with other signs at that position; pull H-1845 and H-360; count 240-031-002-861 across the strict layer with the head before 240.
- Where: research/docs/archive/campaign_032_002_861_x240_internal_subframes.md; ..._x240_subframe_migration.md; ..._x240_post861_bridge_cluster_scan.md; ..._x240_bridge_ecology.md; ..._x240_family_cell_bridge_audit.md; ..._603_636_642_external_ecology.md.
- Old label: "bridge" mechanism, interpretation paused; X-240 "class" member pressure.

### 1.10 240 picks 032, and then the row closes or takes a tail (6 readers: 00, 02, 03, 04, 05, 13)
- Seen: 240 goes to 032 at 9 of 12 frame-text dedup units (0.75) against 46 of 239 elsewhere (0.192469); odds ratio raw 12.586957, Haldane-adjusted 11.294931; matched site/type blocks 9 of 12 against 35 of 150 (OR 9.857143, adjusted 8.830986); no-companion 9 of 12 against 43 of 215. The main block is Mohenjo-daro SEAL:S at 6 of 7 against 23 of 104; without it 3 of 5 against 12 of 46. 314 clean known-next 220 rows, 251 strict frame-text units, 260 site/type/frame/text blocks. Nine strict 240-220-032 units: two close at 032, five go to 002, two go on without 002 (M-631 +520-033-706-240-220-032-368-263+; M-1265 +740-055-240-220-032-806+); M-22 +740-904-176-220-032-798-000[ (right end censored). 240-220 also takes 002 (M-1990 +740-760-440-240-220-002-861+), 255 (M-133 +527-550-240-220-255-812-906-388+), 415 (M-369 +740-690-435-255-240-220-415-806-742-060-920+). After 032, seven of the nine 240-220-032 rows continue. Terminal-space check on the 220-032-002-861 rows (seven Lipi rows: 62.1 Chanhu-daro, 1434.1 Harappa, 2313.1, 2618.1 M-91, 2763.1 M-240, 3147.1, 3421.1): bare closures H-444 (700 px line), M-723 (925), M-1044 (600), M-1763; post-861 margins 28, 38, 38 px; tailed rows M-91 (`255-416`, 450 px line, tail window 195 px) and M-240 (`603`, 420 px, window 120 px) touch the edge; R00: tailed rows have 120-525 px of terminal content, bare rows 28-45 px.
- Best case: The effect survives dedup, block dedup and no-companion filters; the longest measured line (M-723, 925 px) is bare and the two tailed lines are the two shortest, so room does not decide the outcome; 120-195 px against 28-38 px runs the direction a real written tail predicts. Visual packet: bare closures H-444, M-723, M-1044; simple tail M-240 `603`; compound tail M-91 `255-416`.
- Boldest reading: 240 is an entry selector into a typed continuation after 032; the choice among closure, simple tail and compound tail is positional; the 240-220 frame takes at least four closers (032, 002, 255, 415) and 032 is one subtype. The tail is a real element with a measurable footprint.
- Next move: Photograph the five unphotographed rows (62.1, 1434.1, 2313.1, 3147.1, 3421.1); re-measure terminal and tail widths with one ruler and no overlay; find a bare-closure row with room comparable to 120 px; compare M-1990 with the nine 240-220-032-002 rows; test 240 -> 032 on M-240 and M-91 without the 220 slot; rerun with object-level dedup.
- Where: research/docs/archive/campaign_a_220_x_240_selector_contrast.md; research/docs/archive/campaign_032_after_220_function.md; research/data/open_prototype/reports/campaign_a_220_x_240_contrast_summary.json; research/docs/archive/campaign_032_002_861_220032_source_visible_contrast_packet.md; ..._220032_terminal_space_recut.md; ..._220032_register_length_*_test.md; evidence/tmp/032_002_861_220032_source_visible_contrast_packet/ and 032_002_861_220032_terminal_space_recut/.
- Old label: "best live sign-function candidate; positional formula or constructional selector"; "terminal-space adversary survives; grammar promotion blocked"; terminal-space recut judged "positive, not merely pending"; margins come from an existing overlay, not a fresh resegmentation.

### 1.11 032 has three right-hand lanes, and 840 is a second tail nobody followed (3 readers: 00, 01, 04)
- Seen: 032 occurs 502 times in clean rows; 216 close the row; 42 are followed by 002. Among 408 with a sign before: after 220 (56 rows) 24 go to 002 and 15 close; after any other sign (352) 17 go to 002 and 154 close. 700-032 = 95 rows, 89 close at 032, 93 at Harappa; 740-032 = 58 rows, 33 followed by 840, 1 closes; 220-032 = 56 rows, 37 at Mohenjo-daro. 840 occurs 110 times, 38 right after 032: 740-032-840 33 rows, 22 unique texts, closes at 840 in 12 (Harappa 17, Mohenjo-daro 12, Lothal 2, Chanhu-daro 1, Dholavira 1); 032-840 38 rows, 27 unique texts, closes at 840 in 14 (Harappa 18, Mohenjo-daro 15, Lothal 2, Bakkar Buthi 1, Chanhu-daro 1, Dholavira 1; types SEAL:S 15, TAB:B 17). 002 after A-220-032: next 002 in 24 of 55 against 16 of 257 outside 032 (OR 11.66); core 002-861/820/817 16 of 55 against 8 of 257 (OR 12.77); core terminal tails 14 of 55 against 6 of 257 (OR 14.28). Without Mohenjo-daro SEAL:S, A-220 next 002 6 of 28 against 12 of 387 (21% against 3%); terminal-tail contrast 5 of 28 against 6 of 387. Adjacent strict 032-002 rows: 817 4 of 4 terminal, 820 6 of 7, 861 7 of 9, 390 0 of 2.
- Best case: The 002 lane exists after 220 (43 percent) and is nearly absent elsewhere (5 percent); 22 unique texts out of 33 rows means 840 is not one copy, and it runs on six sites and on seals and tablets; leave-one-block holds.
- Boldest reading: 032 is a slot whose right-hand content is set by the left frame; 002 is one of three licensed continuations (002, 840, closure) and 840 may be the non-A-220 counterpart of the 002 lane; the A-220-032-002 formula and the 240 selector are one branch of a larger table.
- Next move: Tabulate the next sign after 032 for every left sign on strict dedup across all sites; list the 22 unique 740-032-840 texts with object numbers and compare their register with the 002 lane; list every 032 followed by a sign other than 002 and tag the following sign by its post-Y class; the 002 odds ratio on Harappa-only rows.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; research/docs/archive/campaign_032_after_220_function.md; campaign_032_002_tail.md; campaign_a_220_x_240_selector_contrast.md; campaign_032_002_post_y_continuation_campaign.md; research/docs/archive/active_decipherment_attempt.md ("032-002 tail campaign", "032-002-Y leave-one-block campaign").
- Old label: "032 after A-220 is a tail-selector; 002 is the lane"; "002 = tail-lane operator"; "002 is a post-032 branch introducer candidate"; 840 and the other outside-A-220 continuations were named once and not analysed.

### 1.12 032-002-861 closes at three sites under more than one left frame, with photographed witnesses (5 readers: 00, 02, 04, 05, 11)
- Seen: 032-002-861: 11 rows, 10 unique texts, closes at 861 in 9; Mohenjo-daro 6, Harappa 3, Chanhu-daro 2; all 11 SEAL:S. Left frames: 241-220 (H-444), 520-220 (M-1044), 692 (M-21), 176 (C-60), 390-590-070 (H-597); C-65 unreadable. Continuing rows: M-240 (861-603) and M-91 (861-255-416). Same-line witness matrix (eight rows): M-722 (817, with 240-220-032 before), M-49 (300), H-444 (861, non-240), M-375 (820), C-10 (817, Chanhu), M-21 (861), H-597 (861), C-60 (861, weak). Post-Y tail decisive rows: M-49 (+002-300-350-032-190), M-240 (CISI India leaf n95, p. 60), M-91 (+740-100-798-220-032-002-861-255-416+; leaf n71), M-1677, M-70, 3335.1; token/order adjudication passed M-49, M-240, M-91, M-70. 207 continuing post-Y instances. M-70 blind packet: false-positive rate 0.714286 (yes-only) and 0.777778 (conservative) over two reviewers.
- Best case: 861 closes after 032-002 in frames with no 220 at all (692-032, 176-032, 070-032), so A-220 is one entry route; four rows with plate routes is more source than most of the corpus has; the failed blind packet is a reviewer-looseness problem (over-called controls), not a row problem.
- Boldest reading: 032-002-861 is a site-independent closing formula and M-240 and M-91 share a repeated post-Y family; M-70 and 3335.1 are its other ends.
- Next move: Check whether C-60 and H-597 come from one plate family (all 11 are seals, so this is seal-type portability); rerun the M-70 blind box with the four row images, family-tail signs only, on Mohenjo-daro source panels and not overlays; rerun the coverage null on the eight rows with a second random subset and control.
- Where: research/docs/archive/campaign_032_002_y_branch_model.md; campaign_032_002_y_source_function_batch2.md; ..._batch3_chanhudaro.md; research/docs/archive/source_visible_032_002_y_witness_matrix.md; research/docs/archive/effective_unicity_directionality_m70_source_pilot.md; effective_unicity_m70_blind_token_box_packet.md; research/data/open_prototype/reports/campaign_032_002_branch_tail_token_order_verdicts.csv; ..._token_order_boxes.csv; tmp/032_002_branch_tail_source_acquisition/ (M70 crops from CISI India n066).
- Old label: "the most portable branch"; matrix "retracted after failed control"; M-70 blind packet "not promoted".

### 1.13 The 390-590-032 chunk is a free-floating unit (4 readers: 01, 02, 03, 04)
- Seen: 390 is followed by 590 in 59 of its 235 distinct occurrences (its most common successor); 390-590: 61 rows, 50 unique texts, closes at 590 in 8 (Mohenjo-daro 29, Harappa 22, Dholavira 4, Chanhu-daro 2, Allahdino, Kish, Gonur Depe, Unknown 1 each; SEAL:S 43, TAB:B 16). 390-590-032 occurs in 7 raw rows at 3 sites: Lothal 2081.1 ]390-590-032-002-880[ (L-139), 2116.1 ]390-590-032-002-000[ (L-196), 2118.2 +740-390-590-032-002-000[ (L-198); Mohenjo-daro 2448.1 +740-390-590-032-060-201+, 3169.1 +740-440-220-032-741-390-590-032+, 3359.1 +740-390-590-032-741-527+ (M-1739, M-746, M-965); Unknown 3335.1 +740-205-032-002-390-590-032+. M-746 and M-965 are source-visible (CISI Pakistan n90 and n128). Pivot: 3 of 7 chunks followed by 002 against 0 of 10 for non-390 590-032 (p = 0.051471). H-597 (+740-390-590-070-032-002-861+) has 032 two signs after 590.
- Best case: In the Lothal rows the chunk sits before 002, so it is a unit with its own internal order, not a copy of the 002 frame; the three Lothal strings are not identical (two tails match, 002-000). The adversary's formula-family worry needs identical copies.
- Boldest reading: 390 takes the complement 590 and 032 returns as a delimiter inside the tail (recursive 032); 3335.1 is a legitimate placement of the unit and the 002-390 frame is one place it can sit.
- Next move: Count the distinct objects behind the 7 rows (the two Lothal 002-000 rows may be one); pull the 61 rows and count rows with 032 within two signs of 590; compare the 390-590-032 crops of M-746 and M-965 with the 3335.1 text.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; research/docs/archive/campaign_032_002_861_002390x_390590032_family_recheck_20260531.md; ..._3335_acquisition_packet_20260531.md; research/docs/archive/campaign_032_002_source_normalized_branch_tail_admissibility.md.
- Old label: "portable formula-family chunk" treated as adversarial pressure on 3335.1; "3335.1 blocked until object ID".

### 1.14 125 continues after open heads and closes after 861 once; 235 and 632-032 sit beside it (4 readers: 00, 01, 02, 03)
- Seen: 125 follows 390 in 4 rows and 405 in 1 (M-41 +740-636-240-233-235-002-405-125-820+); 392 then 590 125 in 1981.1 (Lohumjo-daro). 1114.1 (H-55, Harappa SEAL:S) +390-004-002-861-125+ ends in 125 after the closing head 861; Chanhu-daro 76.1 +125-002-861+. M-1750 (2450.1 +390-004-002-861+) is the bare half of the pair, source-dark; of 59 occurrences of 125 only 1 follows 002-861 (H-55) and 17 are terminal. M-41 and Sktd-1 (3875.1 +390-004-002-390-125-820+) share the tail 125-820 under heads 405 and 390 with predecessors 235 and 004. 235 before a 390/405 head takes 125 in 3 of 3 rows (M-38, M-735 under 390; M-41 under 405); closing heads avoid 125 (1 of 1); M-41 signband continuous (evidence/tmp/002390x_390405_m34_m41_source_check_20260531/M41_A_signband_x2.jpg). 632-032 occurs in 7 chunks, 5 end the row; the three without 125 before them (predecessors 368, 504, 892) all end; after-125 chunks end 2 of 4; exceptions M-119 (900-563 continues) and M-1188 (damaged).
- Best case: The 235 rule is the only left-context rule that predicted every row it was given; the 405 class is 4 distinct texts once the duplicate string collapses, one with the same 125-820 tail as a 390 row; 632-032 closes even without 125.
- Boldest reading: 125 continues only after open heads (390, 405, 392) and closes after 861; its "continuation" belongs to its environment; 125-820 is a portable ending whose head is not part of the unit; 235 is a switch left of 002 that brings in 125 after a 390-class head.
- Next move: Token-box M-41's band with the M-119 procedure; search 235-002 rows with non-P086 heads (a 125 under a closing head breaks the rule); compare the 125 and 820 glyphs of M-41 and Sktd-1 in one crop each; pull the 1114.1 source image and match its last glyph to M-119 and M-735; page CISI Pakistan forward from M-1658 for M-1750; photograph-check the three non-125 632-032 rows and M-1188.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; research/docs/archive/campaign_032_002_861_390004_exact_prefix_source_gate.md; ..._390004_branch_125_ecology.md; ..._risky_parse_model_v1_20260531.md ("Fourteenth", "Forty-Eighth", "Forty-Fifth"); ..._sktd1_side_pair_recheck_20260531.md; ..._390405_collision_adversary_20260531.md; crops in evidence/tmp/032_002_861_390004_exact_prefix_source_gate/ (H-55, CISI India n217).
- Old label: "exact-prefix alternation acquisition-gated; not promoted"; "125 is not intrinsically continuation-bearing"; "candidate from aggregate contrast; exact-left shadows sparse".

### 1.15 530 links a head to one complement across four heads and four sites (3 readers: 01, 02, 03)
- Seen: Governed rows 002-H-530-Y: C-57 (002-296-530-000), H-773 (1665.1 +740-798-803-002-390-530-741+), M-623 (002-299-530-820), 4182.1 (002-705-530-904); heads 296, 299, 390, 705; Chanhu-daro, Harappa, Mohenjo-daro, Dholavira; each has exactly one sign after 530. Outside 390, 530 continues 3 of 3; 4 of 4 one-complement rows and 4 of 4 closure-like complements; 590 has 3 of 7 terminal and 1 of 4 closure-like complements; globally 13 of 18 occurrences of 530 continue and 9 of 18 have one complement. H-773 side A: token windows under R/L 741 0-75, 530 75-225, 390 225-340, 002 340-465, 803 465-565, 798 565-695, 740 695-815; Lipi derivative H-773_a.jpg is 269 x 170; CISI Pakistan n358 crop shows seven units (R01 sees seven to eight); side B 1665.2 +700-033-711-335-575-413+; Vats Plate XCIV item 351 / object 12377 is "H-773B, one side only".
- Best case: Forger rates 0.0043 (one-complement-only) and 0.00031 (full shape); 530 is the only branch sign whose shape holds across four heads and four sites; H-773 is the only continuing non-125 row after 390 with a source panel and its unit count matches its local sign count.
- Boldest reading: 530 is a linker (head H joined to one complement Y), not a value; 002-390-530-741 is a second continuing head after 390, so 125 is not the only one.
- Next move: Photograph-check C-57, M-623, 4182.1 and find a fifth governed 530 row (the promotion test); decide which side the n358 crop shows by comparing the 741 window at 0-75; open evidence/tmp/vats_vol2_archive_metadata.json for a plate with the side-A items of the eight H94/H95 tablets; count 530 rows across the strict layer by head. Contrary figure, once: 590 also passes the count-window test.
- Where: research/docs/archive/campaign_032_002_861_002390x_risky_parse_model_v1_20260531.md ("Twenty-Fifth", "Twenty-Sixth", "Twenty-Fourth"); ..._h773_token_box_recheck_20260531.md; ..._h773_side_guard_recheck_20260531.md; ..._h773_lipi_image_map_guard_20260531.md; evidence/tmp/source_route_recheck_20260531/cisi_pakistan_n358_h773_A_signband_tight_w2400.jpg; evidence/tmp/002390x_h773_vats_side_guard_20260531/Vats_Plate_XCIV_351_candidate_H773B_tight_from_v2.png.
- Old label: "complement-linker rule"; "governed one-complement candidate; closure semantics demoted"; "panel-bound, boxed-compatible, not strict".

### 1.16 705 closes the 390 frame at two sites and closes outside 002 (5 readers: 00, 02, 04, 05, 11)
- Seen: 002-390-705 under different left frames: Dholavira 4237.1 (+151-032-388-002-390-705+, SEAL:S, ZA-12:2) and Mohenjo-daro M-1825 (3992.1 +157-031-002-390-705+, 17.5 x 18.5, icon-only, F2 unicorn in Bhaskar S1, pointer BJ25710). Outside 002: 705 occurs 176 times in clean rows and closes 48; its left neighbour is 033 in 89 rows (Mohenjo-daro 65, Harappa 18; SEAL:S 39, TAB:C 20, TAB:B 15, SEAL:R 8); 033-706 occurs 42 times and closes 14. Lothal formula 090-740-220-055-001-741-500-705 (11 rows) ends on 705. 520-033 gives 705/706 in 45 of 52. Counter-rows: Tell Umma 3884.1 +390-004-002-705-127+ continues; Mohenjo-daro 705 sits mid-text in a 14-fold repeated text (+407-321-407-845-033-705-235+).
- Best case: Two predecessors, two sites, both close, so closure does not come from one left context; 705 closes far more often than any branch sign.
- Boldest reading: 705 is a closing class sign outside the 002 construction (033-705 is a second closing frame) and the closure pole has a member beyond 817/820; Dholavira would test whether the 520 frame reaches a second city.
- Next move: Count 705 closers against 817/820 across the 499 rows; compare 705 and 706 on one signband for the 033 rows; fetch M-1825 once CISI 3.1 is in hand; route Tell Umma 3884.1; check the 520-033-705/706 frame for Dholavira rows.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; research/docs/archive/campaign_032_002_861_002390x_source_route_hunt_20260530.md; ..._risky_parse_model_v1_20260531.md ("Nineteenth", "Sixteenth"); research/docs/archive/campaign_032_002_source_normalized_branch_tail_admissibility.md; evidence/tmp/m1206_bhaskar/S1-IndusZoomorphicIconCatalogue.txt.
- Old label: "candidate form if bound; 705 remote/transfer semantics wild"; "002-390-705 needs a route"; "source_image_candidate_unbound".

### 1.17 000 right after 002-H closes 24 of 27 rows (2 readers: 01, 02)
- Seen: 27 rows have 000 directly after 002-H; 24 close after 000. Exceptions: M-451 (+520-000-000-000-906-388+, where 906-388 is terminal in all 3 of its rows), Ns-66 (+892-000-002+, a reset), Rakhigarhi 4148.1 (+740-690-435-255-002-267-000-033+, metadata only). R01: head 000 stops 44 of 55 distinct texts.
- Best case: The M-451 damage claim assumes 906-388 is governed content; its terminal behaviour is what boundary material looks like.
- Boldest reading: 000 is the zero-complement sign: the frame ends on a zero and 002 can start a new frame after it.
- Next move: Close-read Parpola/SAA 2001 Fig. 1 for M-451 and see whether 906-388 follows a boundary; check the three rows where 906-388 is terminal; source-check 4148.1.
- Where: research/docs/archive/campaign_032_002_861_002390x_risky_parse_model_v1_20260531.md (around lines 5204, 5635, 5686).
- Old label: "candidate with serious M-451 damage; not promoted".

### 1.18 Two damaged objects show the edge after 861 on the object (1 reader: 04)
- Seen: M-19 (]000-000-002-861+; CISI PDF 49, print 13) and M-175 (]002-861+; PDF 87, print 51) both show a closed edge after 861; both are left-censored; M-175's 002 is damaged.
- Best case: Physical evidence that 861 is final on the object, where the strict table infers it from catalogue order.
- Boldest reading: 861 moves from catalogue-order terminal to physically terminal.
- Next move: Run the bare-versus-tailed 002-861 contrast with M-19 and M-175 added (needs no new run).
- Where: research/docs/archive/damaged_boundary_fragment_closure_20260712.md; research/data/sign_crosswalk/source_panels/damaged_boundary_fragment_closure/M-19_A_a_CISI1_pdf49_print13.png and M-175_A_a_CISI1_pdf87_print51.png.
- Old label: "left-censored bare terminal 002-861 suffixes; not complete two-sign texts".

### 1.19 Nine empty-prefix 002-861-X rows all carry a tail (1 reader: 03)
- Seen: With nothing before 002, X is 416 (6 rows), 698 (2), 096 (1); all nine non-bare. 416 has 46 occurrences (29 terminal), 698 has 10 (10 terminal). Tail counts: 603 x3, 533-717 x2, 255-416 x1.
- Best case: The only tails that open at line start; no bare row has an empty prefix.
- Boldest reading: A line-initial 002-861 tail stands without a preceding sign; read it reversed and it may match a sign order in the terminal set.
- Next move: Direction-reversal reading of the nine rows against the terminal set.
- Where: research/docs/archive/campaign_032_002_861_post861_minimal_contrast*.md; ..._post861_hypothesis_tournament.md; ..._tail_rarity_register_scan.md.
- Old label: "broad formula/background material rather than restricted-tail evidence".

### 1.20 390 is a host sign whose continuation follows the X subtype (2 readers: 03, 13)
- Seen: After a framed 390 (002 frame), 11 of 15 successors fall in the framed X set (0.733); unframed 390 gives 78 of 249 (0.313). Holdout: non-390 rows with the same X cover 12 of 15 rows with 390 and pass 12 of 12 covered rows. Uncovered or tied: M-70 (tie on 692), M-232 (707), 3335.1 (tie on 590). Predictor with head_x_pair: 0.913043 (63 of 69 covered) collapsed, 0.958678 (116 of 121) raw; x_slot_sign 0.765182; scope_cell 0.694545 (raw).
- Best case: A first holdout survived 12 of 12 and framed and unframed 390 differ.
- Boldest reading: 390 is a container whose continuation is set by the X subtype, with no value of its own.
- Next move: Check the three uncovered rows for a different X subtype; repeat the holdout on a second set of sites.
- Where: research/data/open_prototype/reports/campaign_032_002_861_002390x_expand_390_non390_holdout_20260531_summary.json; ..._expand_002_frame_marker_control_20260531_summary.json; ..._consolidate_family_collapse_predictor_20260531_summary.json.
- Old label: "EXPAND_390_RIGHT_EDGE_HOST_BY_X_SUBTYPE: survives_first_holdout".


## Theme 2. The opening pair and what follows it

### 2.1 740, the jar sign, is the opener (stored order) and 400 sits before it (6 readers: 00, 04, 08, 11, 13, 14)
- Seen: 740 total 1,238, initial 858, terminal 3 (R08; initial share 0.695477 edge); hub score 0.821918 (R11); 400 before 740 in 127 of 140 (R11); 400-740 productive opener, 198 rows, 103 unique texts (R04); 400 tablet frame 187 of 765 against 100 of 2,738, Bonferroni 3.63e-59 (R11); 400-740 head against secondary slot 400 primary face p = 0.175 (R13, kept as a negative). R13 crosswalk: 740-P324 73 of 73 aligned positions.
- Best case: The jar sign opens tablets and seals alike across sites; the 400-740 pair has 103 unique texts, so it is productive and not one copied row.
- Boldest reading: 740 is the title or "of" marker of the template; 400 a rank slot before it. In conventional order 740 may close (see 1.4 contrary figure).
- Next move: Tabulate what follows 740-400 by site; pair the opener with face role; fix the order convention in one sentence before any claim.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv; sweep/out/leads_04.md, leads_08.md, leads_11.md, leads_13.md.
- Old label: "structural scout"; 400 primary face "not significant".

### 2.2 520-220-X: a three-slot frame whose last slot is a counted or pictured sign (8 readers: 00, 04, 05, 06, 07, 08, 10, 13)
- Seen: 520-220-415 occurs in 17 rows (R00; 12 distinct texts and 28 rows by R10); 220-415 closer 75 rows, 51 texts; Harappa 19 of 22 against Mohenjo-daro 8 of 26 (R00). 520-220-X: X in 28 of 59 rows (OR 3.71, R05); object-type split: OR 9.75 on Harappa TAB:I (23.83) against 1.21 at Mohenjo-daro (R00). Terminal codes: M-1912 003, M-1206 034, M-37 415, M-715 016, H-789 +400-520-220-016+, K-150 +520-220-006+ (R07, R08). 415 third slot 0.4667 against 0.1909 (R13). R07: 003 = P123, 016 = P126, 006, 034 = P150, 415 = P092 pitchfork; 520 = P217 arrow or spear; 220 = P050 fish. 415 frame varies on H-942: 415 against 016 (+520-220-016+), first slot 520 against 074 (R06).
- Best case: Four to five different terminal codes sit in one slot and three are stroke counts, so the slot is a number or tally position; M-1206 and M-37 share face order R-L-T (R08).
- Boldest reading: "520 spear, 220 fish, then a number" is a record line: item, fish type, count; 415 is a pictured count.
- Next move: Tabulate the third slot for all 520-220 rows (003, 016, 006, 034, 415); photograph H-942 and H-789; run slot-by-site on Harappa TAB:I.
- Where: sweep/out/leads_00.md, leads_07.md, leads_08.md, leads_10.md, leads_13.md.
- Old label: "BASE 520-220-415 candidate"; frame "object-type dependent".

### 2.3 Prefix 154/158 then 806 selects the 465-475 block (3 readers: 05, 13, 14)
- Seen: Trained on Harappa: non-Harappa 6 of 6 against 3 of 58 (p 1.12e-06); extended 9 of 9 against 0 of 55 (p 3.6e-11); 29 of 29 against 3 of 81; non-Harappa 9 of 9 against 0 of 41 (p 3.99e-10, R05); 154-806 16 of 16 (R13); R14 rerun 154-806 17 of 18, 158-806 13 of 16, misses all 000. 158-806 Phyt z 12.84 (R11).
- Best case: A rule learned at one site predicts every case at the others; the second null (0 of 55) is clean.
- Boldest reading: 806 is a prefix operator that selects a name block 465-475, the first sound-bearing slot (name slots start the sound work).
- Next move: List the 465-475 signs reached; sign-by-sign sheet of the three exceptions of 3 of 58.
- Where: sweep/out/leads_05.md, leads_13.md, leads_14.md.
- Old label: "operator candidate"; 465 negative kept (R13).

### 2.4 740-390 selects 590, and four 740 stems are near-deterministic (4 readers: 00, 05, 13, 14)
- Seen: 740-390 to 590 in 40 of 41; 740-407 16 of 16; 740-405 21 of 22 (demoted by M-1669 and C-87); 690-435 to 255 29 of 30 (M-1206 +740-690-435-255-002-861+); 740-100 to 415 27 of 79 (R13).
- Best case: Four stems at 29 to 100 percent; the register family (390, 405, 407) is one head slot (see 2.4 and 9.1).
- Boldest reading: Opener plus second sign fixes the third.
- Next move: Build the 3-gram determinism table across sites; read M-1669 and C-87.
- Where: sweep/out/leads_05.md, leads_13.md.
- Old label: "exact stems; 740 register family demoted by M-1669, C-87".

### 2.5 700 heads Harappa tablets and short side labels are 700 plus a count (4 readers: 04, 10, 11, 13)
- Seen: 700 on 503 Harappa rows, 74 unique texts; two-sided 410 of 503 against 828 of 3,738 (R04). Short side labels: 700 first in 323 of 387; +700-033+ 117 rows clean (R10); short-side rule 7 of 7 (R11).
- Best case: A face heading plus count; 74 unique texts means variety.
- Boldest reading: 700 (U sign, P310) is "side" or "face" and the count after it is a quantity (see 6.2).
- Next move: List the 74 texts with the sign after 700.
- Where: sweep/out/leads_04.md, leads_10.md, leads_11.md.
- Old label: "face/heading candidate".

### 2.6 A 520 header, 211 modifier and a 3-sign pre-slot (3 readers: 10, 11, 12)
- Seen: 520 header (R11); 211 modifier, six pairs (R11); 520 W520 = P217 against P230 (M-126, M-162, M-73; R10).
- Best case: 520 is two shapes in Mayig, one in Lipi; check on M-126.
- Boldest reading: the header 520 comes in two kinds, spear and a variant.
- Next move: Crop M-126, M-162, M-73.
- Where: sweep/out/leads_10.md, leads_11.md.
- Old label: untested.

## Theme 3. Fish signs and their marks

### 3.1 220 reads as a fish in three independent systems (4 readers: 00, 05, 11, 13; 04 offers a cup alternative; 12 a fish square)
- Seen: Parpola sign 60, Mayig P050, 27 rows (R00, R05); medial share 0.9655 against 0.9630 (R11); three systems agree (R13). 220 closes after some left signs; 220-455 (10 rows, 10 texts) and 220-065 (7 rows) do not close (R04); 220-003 19 rows, 15 texts (R04).
- Best case: Three catalogues call it fish and its behaviour is the same in each.
- Boldest reading: 220 = "fish" (the star-fish word set of the later Tamil mīṉ). One photograph (Mahadevan counter object 448 reads 95-328-59; 452 reads 95-59-328; Lipi 448 +220-700-004+, 452 +700-220-004+; H-912, H-1191, H-1192; Vats plate XCVI) decides fish against cup.
- Next move: Photograph those three H objects; read plate XCVI.
- Where: sweep/out/leads_04.md, leads_05.md, leads_11.md, leads_13.md.
- Old label: "fish candidate".

### 3.2 Fish markers 388, 342 and 211 (1 reader: 12)
- Seen: 342 score 60116; tick388 49,760.76 against tick211 49,874.77 bits; two-role model 258 bits better; tick388-after selected 6 of 7 tasks.
- Best case: The tick before fish 388 beats 211 by 114 bits.
- Boldest reading: two marker roles.
- Next move: Replicate on held-out sites.
- Where: sweep/out/leads_12.md.
- Old label: untested.

### 3.3 Roof 87 plus tick 211 spells 1380 and 2452 (1 reader: 12)
- Seen: 1380 (65 70 211); 2452 (87 59 71); 290 combos; roof 87 10 classes. Tamil-conditioned roof87_tick211 beats identity by 7.63, 29.03, 9.31 bits.
- Best case: 3 held-out gains.
- Boldest reading: 87 is a "roof" class marker on fish names.
- Next move: Extend to more tasks.
- Where: sweep/out/leads_12.md.
- Old label: untested.

### 3.4 Fish compound order and the 267-99 header (1 reader: 12)
- Seen: 65-67 36 against 3 reversed; 267-99 222 against 0; header at four sites.
- Best case: A strong order asymmetry.
- Boldest reading: fixed compound ordering of the star-fish names.
- Next move: Check the four-site header on photos.
- Where: sweep/out/leads_12.md.
- Old label: untested.

### 3.5 Final slot signs and sign 12 final (1 reader: 12)
- Seen: 342 last 741 of 2,575; 211 162 of 193; 176 257; 328 250; sign 12 final 55 of 62; counterexample 358 at text 7244.
- Best case: A small closing set.
- Boldest reading: 211 and 12 are suffixes.
- Next move: Photograph 7244.
- Where: sweep/out/leads_12.md.
- Old label: untested.

### 3.6 336-89 stem with 211 ending, count signs bind to classes, "ka" suffix, Tamil fish compounds (1 reader: 12)
- Seen: 336-89 96 texts; 89-211 38; text 1147; 2275 against 1008; 87 before 59 41 times and 11 reverse; ka suffix across 360 systems; Tamil fish compounds 88 or 89 end in mīṉ.
- Best case: counts and class bind in a regular way.
- Boldest reading: fish word forms are number plus class plus suffix.
- Next move: Check Tamil sample against a second language.
- Where: sweep/out/leads_12.md.
- Old label: untested.

### 3.7 Sign 104 roof; repeated-base null power (1 reader: 12)
- Seen: roof sign 104; null power for repeated bases.
- Best case: nulls are sensitive.
- Boldest reading: 104 and 87 are two roofs.
- Next move: add to 3.3 test.
- Where: sweep/out/leads_12.md.
- Old label: untested.

## Theme 4. Stroke signs and counting

### 4.1 Numeric codes are stroke counts (4 readers: 07, 08, 10, 13)
- Seen: 001 = P121 one half-height stroke; 002 = P122 two; 003 = P123 three; 004 = P124 four; 005 = P125 five; 006 and 016 = P126 six; 031 = P144 one full-height; 032 = P145 two; 033 = P147 three; 034 = P150 four full-height. Sums: M-10 032 + 033 = P151 five; M-72 003 + 002 = P125 five; M-16 sign 035; M-40; M-138; M-20 +390-005-002-861-036-460-513+ six strokes, one token 036 = two P147.
- Best case: The numbers follow the pictures.
- Boldest reading: 002 reads "two", so 002-817 (a count before a noun).
- Next move: Plate counts on named objects.
- Where: sweep/out/leads_07.md, leads_08.md, leads_10.md.
- Old label: "numerals candidate".

### 4.2 034 is four full-height strokes; 004 is four half-height (6 readers: 00, 05, 07, 10, 11, 14)
- Seen: M-2104 +151-097-700-034+ with M-315 +390-034-002-374-228-741+ and M-984 +390-004-002-817+ against M-478/479/480/1425 +400-097-700-004+; Fisher p = 0.0000628573 (4 of 9 against 1 of 116); 034 last in 129 of 155 rows; 0 of 179 Mayig records align 034; six P0 objects (M-2104, M-315, M-1206, M-685, M-1584, M-1963). R07: the M-2104 kill condition counts wrong (034 four full-height against 004 four half-height). UIII and UIIII (R11).
- Best case: 034 sits where 004 should.
- Boldest reading: 034 is a distinct unit "four" (not 004).
- Next move: Plate image of M-2104.
- Where: sweep/out/leads_00.md, leads_07.md, leads_10.md, leads_11.md.
- Old label: "034 FRAME700".

### 4.3 034 frequent and small (3 readers: 07, 09, 14)
- Seen: 182 rows; 11 exact singletons (9 pottery); 032 47, 033 25, 034 11; 034 small-object residue 63 of 93 recall; 20 of 93 against 18 of 238 (p 0.0036, q 0.104); area ratio 0.861, 8 of 10 pairs, 309 tablets; AUC 0.701087 (CI 0.606806 to 0.78903).
- Best case: size tier predicts 034.
- Boldest reading: small objects carry "four".
- Next move: See 11.1.
- Where: sweep/out/leads_07.md, leads_09.md, leads_14.md.
- Old label: untested.

### 4.4 003, 032 and 033 split by companions (3 readers: 06, 09, 10)
- Seen: 033 against 032 and +400-740-176+: 20 of 137 against 2 of 102 (p = 0.00054); 034 before longer row TAB:B 23 of 27 against 23 of 54 (p = 0.0003); TAB:I 17 of 38 against 9 of 45 (p = 0.019).
- Best case: counts show up in context.
- Boldest reading: 033/034 are two counters.
- Next move: See 6.2.
- Where: sweep/out/leads_09.md.
- Old label: untested.

### 4.5 000 as counted unit; M-381 seven tokens (2 readers: 07, 11)
- Seen: M-105, M-27, M-61, M-62 carry 000 as units; M-381 seven tokens against 9/13/9.
- Best case: unit slot.
- Boldest reading: 000 = zero or blank.
- Next move: Photograph M-381.
- Where: sweep/out/leads_07.md, leads_11.md.
- Old label: untested.

### 4.6 M-12 and 617 (3 readers: 04, 10, 14)
- Seen: M-12 ten units against nine tokens; 617 two grids (M-4, M-25, M-45, M-81, M-161; 5 of 5); 617 on 70 rows, 60 complete; 617-142 30 rows.
- Best case: 617 has two forms.
- Boldest reading: 617 is a numeral compound.
- Next move: Photograph the five M objects.
- Where: sweep/out/leads_04.md, leads_10.md, leads_14.md.
- Old label: untested.

### 4.7 002 to P122 count conflict (1 reader: 11)
- Seen: 57 and 2 against 57 and 60 across three counters.
- Best case: the conflict is auditable.
- Boldest reading: one counter wrong.
- Next move: Recount.
- Where: sweep/out/leads_11.md.
- Old label: untested.

## Theme 5. Cup tablets and amounts

### 5.1 Reverse of the cup tablets carries a count that matches the front pattern (2 readers: 12, 14)
- Seen: front 48 342 176 with reverse 2/3/4 and 23/10/2; 14 families; categorical beats arithmetic by 72.69 bits; object form predicts face 37 of 44 against 26 of 44; site and medium predict held expression (740 correct against 718).
- Best case: front to count is learnable.
- Boldest reading: tablet = amount record.
- Next move: Hold out sites.
- Where: sweep/out/leads_12.md.
- Old label: untested.

### 5.2 Paired faces and Fuls equations (2 readers: 13, 14)
- Seen: Mahadevan paired faces; solutions (4,20,36), (6,8,10), (10,8,6), (36,20,4); front-to-count association 285 tablets, 23 against 32.8; held-out 37 against 36.3; Mahadevan 4553/4554/4555 front 342-403-103 strokes 4, 2, 4 (Vats plate XCVII).
- Best case: equations name possible counts.
- Boldest reading: paired faces are a sum.
- Next move: Check the plate XCVII faces.
- Where: sweep/out/leads_13.md, leads_14.md.
- Old label: "paired-face counterexample".

### 5.3 Counter faces 4448, 4452, 5461 (2 readers: 04, 14)
- Seen: cup-fish swap 4448/4452/5461; counters 448 and 452 swap 59 and 328.
- Best case: one photo settles cup or fish (see 3.1).
- Boldest reading: 328 is the cup.
- Next move: Photograph.
- Where: sweep/out/leads_04.md, leads_14.md.
- Old label: untested.

### 5.4 Fish-square key 3 of 36 held (1 reader: 04)
- Seen: 3 of 36; no null; 51-130-15 against 51-130-149-342.
- Best case: weak.
- Boldest reading: a key to cups.
- Next move: build a null.
- Where: sweep/out/leads_04.md.
- Old label: untested.

## Theme 6. Tablet series and multi-face formulas

### 6.1 The H-2218 to H-2239 series: hidden side roles predicted, texts reproduced (4 readers: 00, 06, 10, 13)
- Seen: H-series codebook predicts 66 of 66 hidden-side roles and 64 of 66 exact texts; p = 3.19e-11 (R10, R13); 154/156 and 033/034 minimal pairs (H-2237/H-2233, H-2238/H-2230); H-2237 and H-2238 adjacent (R08); both variants from earliest prefixes (H-2238 H95; H-2237 H96); H-2218 textual-criticism tree and plate (R06, R11); H-2219 stroke groups, rows 856.1 to 856.3.
- Best case: A formula that reproduces unseen sides of a series.
- Boldest reading: the series is a copied form with systematic variants (a ledger family).
- Next move: Open the two misses; photograph H-2218 plate.
- Where: sweep/out/leads_00.md, leads_06.md, leads_10.md, leads_13.md.
- Old label: "H-series codebook".

### 6.2 700-03x is a three-form set; 033 and 034 are split by catalogue batch (4 readers: 06, 09, 10, 14)
- Seen: +700-033+ 125 rows, +700-034+ 109, +700-032+ 89; reversed 033 32, 034 14; batch split H95/H96/H97 (Fisher 0.018); 033/034 width and aspect (p 0.036, 0.042); Nature 2021 mirror-writing tablets H-1302, H-1303, H-1822 all +700-033+.
- Best case: batch effects explain the split.
- Boldest reading: 033 and 034 are one sign in two batches (a catalogue split) or two counts.
- Next move: Photograph a batch-boundary pair.
- Where: sweep/out/leads_06.md, leads_09.md, leads_10.md.
- Old label: "batch artefact candidate".

### 6.3 H-series face swap and codebook (1 reader: 09)
- Seen: 034 on face 2 in 13, face 1 in 8; 156/154-003 face 3 in 22 of 22; codebook 0.525 against 0.099; without H 0.229 against 0.156.
- Best case: face order predicts.
- Boldest reading: the swap marks a pair.
- Next move: Rerun with random face labels.
- Where: sweep/out/leads_09.md.
- Old label: untested.

### 6.4 Triangular tablets and prisms (2 readers: 06, 09)
- Seen: 67 triangular, 35 with 2 sides, 32 with 3; H-353, H-983, H-2204, H-2211, H-357; 13 against 9 template classes; H-355; H-1344 to H-1347; fused excavation numbers (H-941 2703464).
- Best case: counted by face.
- Boldest reading: a 3-face tablet stores three registers.
- Next move: Fix the face-order convention.
- Where: sweep/out/leads_06.md, leads_09.md.
- Old label: untested.

### 6.5 400-740-176 long row beside 033/034 (2 readers: 06, 09)
- Seen: companion on 33 objects (23 within CISI Pakistan H-266 to H-1019); +400-740-176+ 39 rows; 520-240-002 29 rows; H-1997 slide (423.1 +400-740-176-235+); H-2145 four deviations (827.2 +074-220-415+).
- Best case: long copied formula.
- Boldest reading: formulas with a counter.
- Next move: Check the slide.
- Where: sweep/out/leads_04.md, leads_06.md.
- Old label: "copy-driven formulas".

### 6.6 060 long row on H-1138/H-1846/H-1845 against H-237/H-823 (1 reader: 09)
- Seen: long 060 row; also see 1.8.
- Best case: formula copies.
- Boldest reading: two lanes.
- Next move: See 1.8.
- Where: sweep/out/leads_09.md.
- Old label: untested.

### 6.7 Raw-ID runs; 002;416;861 carriers all 034 (2 readers: 06, 09)
- Seen: raw-ID runs 90.1% against 84.2% shuffle, 0 of 2,000; carriers H-2094, H-2095, H-2096, H-2097, H-910 5 of 93 against 0 of 238 (p 0.0016).
- Best case: runs follow IDs.
- Boldest reading: excavation order encodes batches.
- Next move: Compare with find-spot.
- Where: sweep/out/leads_06.md, leads_09.md.
- Old label: untested.

## Theme 7. Links between the sign catalogues

### 7.1 Lipi numbers equal Wells numbers (3 readers: 07, 10, 13)
- Seen: 166 of 189 edges (shuffle mean 1.29, max 6); 692 of 784 = 88.3% (shuffle mean 136.4, max 178); Mayig crosswalk 739 aligned positions; Mayig order 0.94375.
- Best case: counts are overwhelming.
- Boldest reading: Lipi is the Wells catalogue renumbered; bridge Parpola, Mahadevan.
- Next move: Print the 189 edges.
- Where: sweep/out/leads_07.md, leads_10.md, leads_13.md.
- Old label: untested.

### 7.2 Mayig blind spot on 034 and the P086 collision (2 readers: 00, 11)
- Seen: P086 collapses 390, 405, 406, 407 (R00); P086 family 25:2:1:1 (R11); 407 copper z 15.92 and 10.83.
- Best case: names which signs are one in Mayig.
- Boldest reading: 405 and 407 identical tails (M-171, M-172).
- Next move: Split P086.
- Where: sweep/out/leads_00.md, leads_11.md.
- Old label: untested.

### 7.3 P041 collision and sign 41 (3 readers: 05, 07, 11)
- Seen: V141, W112, M034; sign 41 three local codes (034, 110, 112; M-33A 2561.1).
- Best case: namespace collisions give false matches.
- Boldest reading: 110 is a person with U (P040).
- Next move: See 7.4 and 6.1.
- Where: sweep/out/leads_05.md, leads_07.md, leads_11.md.
- Old label: untested.

### 7.4 817 and 861 are one sign, P385 (5 readers: 00, 04, 10, 11, 13)
- Seen: 817 89 against 861 85 after 002; Fisher 5.2e-6 medial; 12 of 12 each; co-occur H-1930, M-855; 817 in 195 objects; M-177 803 round against M-32 817.
- Best case: allograph, so heads 817/861 are one closing sign.
- Boldest reading: closing sign "end".
- Next move: Photograph.
- Where: sweep/out/leads_10.md, leads_11.md, leads_13.md.
- Old label: untested.

### 7.5 900 and 920 P154; 154/156 P004 (2 readers: 08, 10)
- Seen: 900 and 920 both P154; 154 and 156 both P004; 101 bracketed 100 (P010).
- Best case: catalog split.
- Boldest reading: shared signs.
- Next move: Merge.
- Where: sweep/out/leads_08.md, leads_10.md.
- Old label: untested.

### 7.6 4,011 against 4,135 strict count; Dholavira 5 against 6 signs (2 readers: 03, 01)
- Seen: conflict kept.
- Best case: audit.
- Boldest reading: n/a.
- Next move: Reconcile.
- Where: sweep/out/leads_03.md.
- Old label: untested.

### 7.7 Omitted signs equal Wells codes (1 reader: 10)
- Seen: M-41 233 P058; M-98 900 P154; M-120 858 P363.
- Best case: ties.
- Boldest reading: omissions are real signs.
- Next move: Photograph.
- Where: sweep/out/leads_10.md.
- Old label: untested.

### 7.8 Class field and vertical bin recoverable (4 readers: 08, 09, 10, 13)
- Seen: 0.643089 against 0.322154; 0.543 against 0.270 to 0.289; 0.5433 against 0.2895; TAB:I 0.7295; edge-removal 0.222222 against 0.092508.
- Best case: the signs predict the object class.
- Boldest reading: sign sets differ by class.
- Next move: Hold out sites.
- Where: sweep/out/leads_08.md, leads_09.md, leads_10.md, leads_13.md.
- Old label: untested.

### 7.9 Direction codes disagree; mirror impressions (3 readers: 06, 10, 14)
- Seen: Lipi dir. R/L, L/R, NR; mirror impressions; mirror-image direction marks (Daggumati and Revesz 2021, 23 mirrored pairs; sign 851); five companion panels disagree with Mayig 700 = U (H-938 B, H-910 B, H-930 B, H-789 B, H-942 B).
- Best case: direction metadata is wrong in places.
- Boldest reading: re-derive.
- Next move: Photograph.
- Where: sweep/out/leads_06.md, leads_07.md, leads_14.md.
- Old label: untested.

### 7.10 Yajnadevam allograph groups (1 reader: 14)
- Seen: r = 390, 820, 861, 760; etc.
- Best case: matches 7.4.
- Boldest reading: same.
- Next move: Compare.
- Where: sweep/out/leads_14.md.
- Old label: untested.

### 7.11 Evidence map, 286 no-ID crops, quarantined gloss columns (2 readers: 13, 14)
- Seen: 12,950 files, 3.5 GB; 6,870 seal JPG; 286 no_valid_id crops (6,870 files, 3,318 IDs); gloss columns quarantined.
- Best case: unused crops exist.
- Boldest reading: n/a.
- Next move: Index them.
- Where: sweep/out/leads_13.md, leads_14.md.
- Old label: untested.

### 7.12 Damaged-slot policy (M-55, M-60) (1 reader: 00)
- Seen: damaged slots M-55, M-60 counted or not.
- Best case: tidy.
- Boldest reading: n/a.
- Next move: Rerun both ways.
- Where: sweep/out/leads_00.md.
- Old label: untested.

## Theme 8. Seals found abroad

### 8.1 Ur 3898.1 (U17649) +002-004-328-001-803-415+ and the Meluhha line (4 readers: 00, 05, 10, 13)
- Seen: against "ur gun3-a me-luh-ha" null 0.6857; triple 001-803-415 unique; CT 50, 076; BM 120573 (Ur U.7683, Gadd sak-ku-shi). Name-plus-title; forger null 1.0 (R13).
- Best case: a name and title in one text.
- Boldest reading: 415 closes titles.
- Next move: CDLI check.
- Where: sweep/out/leads_00.md, leads_05.md, leads_10.md.
- Old label: "negative null kept".

### 8.2 Kish 1971.1, Tell Umma 3884.1, Gulf queue (3 readers: 02, 06, 14)
- Seen: Kish 1971.1 carries the 390-590 chunk; Tell Umma 3884.1 +390-004-002-705-127+ counterexample; Gulf-type queue Ur PG 401, PG 1847, Susa Amiet 1643; Failaka Kjaerum 279 of 319.
- Best case: formulas abroad.
- Boldest reading: portable.
- Next move: Route.
- Where: sweep/out/leads_02.md, leads_06.md, leads_14.md.
- Old label: untested.

## Theme 9. Pictures and text on copper tablets

### 9.1 407 copper register (3 readers: 00, 11, 13)
- Seen: 407 113 rows; 407-845 24; 407-061-845-240-798 six TAB:C rows; 53 of 444 SEAL:R/TAB:C against 17 of 3,059, Bonferroni 1.26e-31; Mohenjo TAB:C lift 12.18 z 16.52; site-type null share 1; CDLI P136689 "6 ma-na uruda me-luh-ha"; M-1954 row 2422.1.
- Best case: copper register one.
- Boldest reading: 407 is "copper".
- Next move: CDLI.
- Where: sweep/out/leads_00.md, leads_11.md, leads_13.md.
- Old label: untested.

## Theme 10. Outside anchors

### 10.1 Stored order against reversed (8 readers: 00, 04, 05, 08, 10, 11, 13, 14)
- Seen: leave-source-out 0.832877; harsh 365 rows 0.841096; 1,705 of 1,798; 1,704 of 1,798 (0.94772); 2,748 of 2,887; Lothal 0.3125 null 0.988, retrained 54 of 58; Linear B 0.996403, SumTablets 0.935484, Pictish 0.802139; I...T scaffolds 22 against 0 reversed; direction head 0.8913; Mayig repeats 8 of 8; stored 0.948276; harsh leave-site 275/54/36.
- Best case: robust.
- Boldest reading: Lipi stores backwards.
- Next move: Remove the top 10 edge signs.
- Where: sweep/out/leads_05.md, leads_13.md, leads_14.md.
- Old label: untested.

### 10.2 Comparators: Linear B, SumTablets, Pictish (4 readers: 04, 05, 10, 13)
- Seen: masked top-1 0.279591 against nulls max 0.2; Indus 0.283422 against Linear B 0.470200; gapped 0.294347 / 0.294314; synthetic 0.472924, 0.443351, 0.415069 against 0.325865; Pictish 0.450292; barn stars 0.367123; masked at 91 signs; SLM micro 0.89M NLL 4.1165, top-1 25.45%; lift 2.24 against 3.44.
- Best case: Indus rates close to Linear B.
- Boldest reading: syllabic-like.
- Next move: matched corpora.
- Where: sweep/out/leads_04.md, leads_05.md, leads_13.md, leads_14.md.
- Old label: untested.

### 10.3 Brahmi near-misses (4 readers: 00, 04, 05, 13, 14)
- Seen: 'ra' attractor 527 0 of 1000, 061 0.008; 817 = dhya no rescue; Sanskrit key rebuild.
- Best case: rejects.
- Boldest reading: none.
- Next move: stop.
- Where: sweep/out/leads_14.md.
- Old label: negative.

### 10.4 AO 22310, Shu-ilishu image (3 readers: 04, 05, 14)
- Seen: AO 22310 Shu-ilishu seal; image.
- Best case: name.
- Boldest reading: Meluhha interpreter.
- Next move: image.
- Where: sweep/out/leads_04.md.
- Old label: untested.

### 10.5 Anchor economics (1 reader: 00)
- Seen: log2(571!) = 4410.970864 bits.
- Best case: price of anchors.
- Boldest reading: n/a.
- Next move: n/a.
- Where: sweep/out/leads_00.md.
- Old label: untested.

## Theme 11. Object sizes, materials, findspots

### 11.1 Size tiers (2 readers: 09, 13)
- Seen: see 4.3; AUC 0.701087.
- Best case: n/a.
- Boldest reading: n/a.
- Next move: n/a.
- Where: sweep/out/leads_13.md.
- Old label: untested.

## Theme 12. Photo checks that settle a question

### 12.1 3335.1 and the 740-205-032 prefix (6 readers: 00, 01, 02, 03, 05, 11)
- Seen: M-70 +226-032-002-390-692+ against 3335.1 (+740-205-032-002-390-590-032+) against M-143 prefix 740-205-032-002-252-840; pivot 3 of 7 against 0 of 10 p = 0.051471; commits b272ad99 and 0921d91d ("Private collection").
- Best case: one photograph.
- Boldest reading: 3335.1 is the unit's other end.
- Next move: Identify the object.
- Where: sweep/out/leads_01.md, leads_02.md, leads_03.md.
- Old label: "blocked until object ID".

### 12.2 Dholavira 4237.1 and M-1825 (7 readers: 00, 01, 02, 03, 04, 05, 11)
- Seen: 4237.1 = Acc. 8758 (27.62 x 21.31 x 7.11-11.17); Bisht p. 18 item 10 six or seven glyphs against 5-sign Acc. 2118.
- Best case: one page.
- Boldest reading: 705 closes.
- Next move: Bisht 2015.
- Where: sweep/out/leads_01.md.
- Old label: untested.

### 12.3 H-1993 (744.2) Fig. 17.07 (3 readers: 02, 03, 11)
- Seen: second catalogue (Singh 2023 supplement, H96-2769 Fig. 17.07; CISI 3.1).
- Best case: predicts 095.
- Boldest reading: closure.
- Next move: Check.
- Where: sweep/out/leads_02.md.
- Old label: untested.

### 12.4 M-32, M-172, M-126, H-773 (3 readers: 01, 03, 10)
- Seen: M-32/M-177 duplicate; H-773 A (1665.1, 7 signs, CISI Pakistan n358, Vats XCIV 351 side B).
- Best case: glyph checks.
- Boldest reading: n/a.
- Next move: Crop.
- Where: sweep/out/leads_01.md.
- Old label: untested.

### 12.5 CISI paid source (4 readers: 04, 08, 09, 11)
- Seen: CISI 3.1 EUR 70 + EUR 48.25 shipping = EUR 118.25, no digital copy; invoice requested not paid; Finna lists nine Finnish libraries; CISI Pakistan scan free route for 23 objects.
- Best case: library loan first.
- Boldest reading: n/a.
- Next move: Tell Cúper the price and why; library first.
- Where: sweep/out/leads_04.md.
- Old label: untested.
