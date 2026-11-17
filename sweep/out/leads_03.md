# Leads from reader 03 (chunk_03, 032-002-861 and 002-390-X archive)

Scope: the 422-file archive at /home/claude/ivc/research/docs/archive/, read through its campaign_032_002_861_* notes, the 002390x decision and forger files, the 220032, 390004, 533717, 603, x240 and 002-861 tail sets, and the risky parse model log (read by heading and selected test runs, not in full). Numbers below are quoted from the docs as written; I spot-checked the forger nulls, the 240 bridge-lock null, the 3/7 vs 0/10 pivot p-value, the 4237.1 OCR conflict and the terminal-space margins against the files. No Lipi, Mayig or metadata CSV query was run in this sweep.

### Terminal space after the tail is wider when a tail is present
- What was seen: In the terminal-space recut, tailed terminal windows are 195px (M-91) and 120px (M-240, 420px line, share 0.286). The source-visible bare controls have post-terminal margins of 28px (H-444, 700px line) and 38px (M-1044, 600px line). The doc calls the terminal-space attack "positive, not merely pending" and notes the smallest tailed width (120px) against the largest bare margin (38px).
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_220032_terminal_space_recut.md; campaign_032_002_861_220032_source_visible_contrast_packet.md; campaign_032_002_861_220032_register_length_kill_test.md. Bare controls H-444, M-1763, M-723, M-1044; tailed rows M-91, M-240.
- Old label: "terminal-space adversary" that the recut was built to test; survived in the recut, with the limit that margins come from an existing overlay, not a fresh resegmentation.
- Why it is alive: The gap is large (120-195px against 28-38px) and runs in the direction that a real post-terminal tail would predict. The old adversary was "tail takes space the terminal does not use," and the bare rows show that the space after a terminal is small, so the tail is occupying room the terminal would otherwise leave empty. A reader who argues that the sign is only layout would have to explain why bare rows leave so little room at all.
- What it would mean if true: The 002-861 tail is a real written element with its own width, not a copying or spacing artefact. Every sign that carries a tail, not only the 220-032 family, would then have a measurable physical footprint that can be checked against a source.
- Cheapest next move: Re-measure the terminal and tail widths on the source photographs for M-91, M-240 and the four bare controls with the same ruler, in one pass, with no overlay. If the gap holds, the number becomes the first metric that does not depend on the old adversary.

### Strict 125 branch in source-normalized rows has a low label-shuffle null
- What was seen: The forger table for the target event (125 with at least four raw rows, at least two strict source-visible rows, no terminal row after the branch): label shuffle FPR 0.004360 (50,000 shuffles); within site/type buckets 0.012460; strict versus non-strict 0.017660; within terminal/continuing status 0.397360; within site/type/terminal buckets 1.000000. Strict pair M-119 (484->125, continuing) and M-735 (235->125, continuing); the non-125 strict pair is M-70 and M-71 (both terminal).
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_replacement_branch_forger.md; campaign_032_002_861_002390x_source_normalized_contrast.md; campaign_032_002_861_002390x_source_tiered_prev_gate_20260531.md.
- Old label: "live source-normalized structural candidate, not an accepted claim." The 1.000000 site/type/terminal bucket and the 0.397360 terminal-status null were the stated reasons for not promoting.
- Why it is alive: Five null models with four below 0.02 is a strong structural result for a two-row strict core. The 0.397 result only says the terminal-status bucket explains much of the pattern, which is a claim about polarity, and that is the claim under test. Polarity (125 continuing, non-125 closing) is clean in all four strict rows.
- What it would mean if true: 125 is a sign that opens a continuation, and the terminal/continuing split is a property of the sign, not of the object. That would be a rule with a number on it.
- Cheapest next move: Add the strict core rows from the non-source-visible set in a blind check: take M-119, M-735, M-70, M-71 and the next strict rows, shuffle their labels within the strict layer only, and report the fraction where 125 stays continuing. This is a rerun from the 4,011-row strict layer, not new data.

### 125 polarity holds only inside frames, not outside them
- What was seen: Outside the 15 adjacent frames, the focus signs keep their polarity at different rates: 095 non-frame continuing 22/30; 125 non-frame continuing 38/59; 692 non-frame terminal 58/77; 705 non-frame continuing 160/219. The intrinsic shortcut ("sign X always terminal or always continuing") was tested on H-55 (+390-004-002-861-125+, terminal 125), H-660 (+520-095-033-706-240-798+, continuing 095), M-21 (continuing 692), M-118 and M-714 (continuing 705). The same 125 is terminal in H-55 and continuing in other rows.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_branch_sign_ecology_20260531.md; campaign_032_002_861_002390x_source_bound_intrinsic_sign_behavior_recheck.md; campaign_032_002_861_002390x_family_collapsed_branch_ecology.md; campaign_032_002_861_002390x_reearned_family_collapse.md.
- Old label: "intrinsic-behaviour shortcut rejected." The rejection was the verdict.
- Why it is alive: A rejected shortcut is not a dead one: the rate of each sign's polarity outside frames is stable (95 at 22/30 continuing, 692 at 58/77 terminal, 705 at 160/219 continuing), which is what a sign with a stable role would show. The H-55 counterexample is one row and can be read as the wrong head class.
- What it would mean if true: Each focus sign has a role that is set by the sign before it, and it is a stable role, not a random one. This would make the head sign, not the branch sign, the thing that carries the polarity.
- Cheapest next move: Tabulate each focus sign's polarity by the head sign directly before it (the 390-X or 002-X left neighbour) across all rows, not only frames. Report the rate per head. The data already sits in the strict layer.

### The after-240 subframe table: a hinge sign between X and a closing material
- What was seen: 240 sits between a branch sign X and a subframe in the bridge rows. The after-240 subframe table: <END> 33 rows; 002-861 9 rows; 060-692 7 rows; 002-817 5 rows; 031-032-171 4 rows. Example rows: M-941 +000-642-240-031-002-861+ (642 before 240; tail 031-002-861 after); M-706 +740-773-240-002-861-031+; M-280 +740-482-240-002-944-920-140+; M-41 +740-636-240-233-235-002-405-125-820+.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_x240_internal_subframes.md; campaign_032_002_861_x240_subframe_migration.md; campaign_032_002_861_x240_post861_bridge_cluster_scan.md; campaign_032_002_861_x240_bridge_ecology.md.
- Old label: "bridge" mechanism; the subframe was called "internal" and the 240 hinge treated as a connector, with the interpretation paused.
- Why it is alive: 240 is the only sign that appears between a branch sign (X) and a material that is then closed by 002-861 or by a 060-692 or 002-817 subframe. The 002-861, 060-692 and 002-817 subframes are the three largest named post-240 classes after <END> (9, 7 and 5 rows), and all three are closing or near-closing forms, so 240 looks like a sign that moves a branch into a terminal form. This ranking is from the subframe table as written, not rechecked.
- What it would mean if true: 240 is a terminal-approach marker. It would mark the point where the X-branch ends and the closing material starts, which is the structure the 002-861 tail depends on.
- Cheapest next move: Count the after-240 subframes across the full strict layer (not only the bridge-set rows) and check whether the terminal share of 240-followed rows is higher than the terminal share of rows with another sign at that position. Both counts exist in the strict layer.

### 603 locks to one after-240 subframe, 060 692, under a row shuffle
- What was seen: 603 sits in the X slot of rows shaped ...-X-240-... and always takes the same subframe, 060 692. Under label shuffle, P(shuffled 603 locked specifically to 060 692) = 0.000400 (the bridge-lock null doc's figure); the broader class (any low-frequency non-background bridge sign locked to one after-240 subframe) appears at 0.040000. Rows: M-240 +520-240-220-032-002-861-603+, M-714 +740-585-017-033-705-233-798-803-002-861-603+, M-1273 +740-055-002-861-603+; Harappa 740-603-240-060-692 in H-1137, H-1138 (Vats XCIV no. 346), H-1846 (H95-2672, Figure 11.11).
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_603_x240_bridge_hypotheses.md; campaign_032_002_861_x240_bridge_lock_null.md; campaign_032_002_861_603_source_route.md; campaign_032_002_861_603_h1138_h360_tokenization_gate.md.
- Old label: "bridge-lock" pressure; the doc says the broader event is "about the 4% level" and "small-count and model-sensitive."
- Why it is alive: The exact lock of one named sign to one named subframe is 0.000400 under shuffle. The 603 sign also runs into a second context (002-861), which is the first tail sign that bridges between the two contexts. A sign that sits in a bridge and locks to a subframe is a classic connector.
- What it would mean if true: 603 is a connector sign: it is the X member that carries a branch into a 060-692 material and also into the 002-861 tail. That would make 603 the one sign that both branches and terminates.
- Cheapest next move: Pull the H-1138 and H-1846 Harappa images and check whether 740-603-240-060-692 appears in both, since two sources with the same locked string would be the first outside check on the lock.

### 603 at H-1138 depends on the slot order (R/L versus LTR)
- What was seen: H-1138 X-slot is visual slot 4 under R/L reading and visual slot 2 under visual LTR reading. M-1273 (+740-055-002-861-603+) is the clean terminal window for 603.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_603_h1138_h360_tokenization_gate.md; campaign_032_002_861_603_slot_substitution.md; campaign_032_002_861_603_source_normalized_slot_family.md.
- Old label: "orientation policy" open question (R/L versus visual-LTR). The slot-index mapping flips for 603 at H-1138 and the reading was not settled.
- Why it is alive: The two orientations give different X-slot positions for the same 603 sign. If the R/L reading is the right one, 603 sits in a slot that matches its X-class role, and the 060-692 lock becomes an intra-object fact, not a cross-object coincidence.
- What it would mean if true: The sign inventory depends on reading direction in a testable way; the first object that resolves the orientation would fix the slot order for the whole family.
- Cheapest next move: On the H-1138 image, mark the slot boundaries under both readings and check which one puts 603 in the same slot as the other X-class signs at 240-adjacent positions.

### 603 graphic closure: a possible clipped unit on H-1138
- What was seen: The 603 cross-context closure (dated 2026-07-12) assumed five units on H-1138. The doc flags a possible clipped unit, which would change the count and the slot of 603. The graphic identity packet and the slot-substitution set record that 603 has one family cell in the X-240 table.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_603_cross_context_graphic_closure_20260712.md; campaign_032_002_861_603_graphic_identity_packet.md; campaign_032_002_861_603_mobility.md.
- Old label: "closed" (2026-07-12 verdict on the cross-context bridge).
- Why it is alive: The closure rests on an assumed count of five units. A clipped unit at the edge would make H-1138 six units, which changes the slot assignment above and reopens the 603 X-slot question. The verdict assumed the count it was meant to check.
- What it would mean if true: 603's X-slot reading and its bridge into the 002-861 context both depend on one edge unit that has not been looked at.
- Cheapest next move: Crop the H-1138 edge at higher resolution and count the units directly; the answer changes either the closure or the slot result above.

### 533-717 is a two-sign tail unit with zero independent occurrences
- What was seen: 533 has 0 independent occurrences; 717 has 37. The pair 533-717 occurs twice, both after 002-861: M-376 (India n129, 39.4 x 11.4 mm) and M-391 (India n131, 42 x 10 mm). Register: 2/144 overall; 2/7 Mohenjo no-icon SEAL:R; 2/3 cuboid-convex no-icon SEAL:R; 0/71 Mohenjo SEAL:S. Controls: M-355 (long tail 360-520-919-140), M-1267 (bare), M-1273 (603), M-1954 and M-1973 (bare, source-pending).
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_533717_blind_layout_gate.md; campaign_032_002_861_533717_component_ecology.md; campaign_032_002_861_533717_focus_contrast.md; campaign_032_002_861_533717_source_family_independence.md; campaign_032_002_861_533717_source_layout_discriminator.md.
- Old label: "P1 restricted post-861 target" (the forger note) with the register result as a limit.
- Why it is alive: 533 never occurs without 717 in this corpus, which is what a bound unit looks like. The two rows are both source-visible, both terminal after 002-861, and both on the same register. The control set includes other tails, so the test has a comparison.
- What it would mean if true: 533-717 is a single two-sign closing unit that is written as one piece; the 533 sign has no life outside it.
- Cheapest next move: Run the blind layout gate's control rows through the same visual score, with the 533 and 717 signs cropped separately from M-376 and M-391. A match on the crop of 533 alone would break the bound-unit reading.

### 390-004-002 branches to a closing pole at 817
- What was seen: The 390-004-002-Y branch counts: {031:1, 390:1, 705:1, 817:4, 820:1, 861:2}. Four rows 390-004-002-817 share one exact formula; M-984 is source-visible. 125 occurs 59 times locally, 17 terminal, 2 after 861, 1 after 002-861 (H-55).
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_390004_branch_125_ecology.md; campaign_032_002_861_390004_exact_prefix_source_gate.md.
- Old label: "817 closure pole" (one exact formula, source-visible).
- Why it is alive: 817 is the most common Y after 390-004-002 and it is always the same formula. A branch that closes onto one exact formula four times is a closing pole in the way the old agents named it, and M-984 gives it a source witness.
- What it would mean if true: 390-004-002 has a closing branch to 817, and 125 is the open alternative. The two branches would be the two halves of one left context.
- Cheapest next move: Check the four 390-004-002-817 rows against the photographs for any second source witness beyond M-984, since one witness is the whole evidence now.

### 820 is terminal most of the time but turns up after 125 and in a nonterminal place
- What was seen: 820 has 244 global occurrences, 185 terminal, 2 after 125. Destructive scout: 032-002-820-001-440-012 (M-1677) and 032-002-820-000 (M-1045) show nonterminal 820. Forty-Third scout: 820 75/81 terminal.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_risky_parse_model_v1_20260531.md (Forty-Second, Forty-Third, Forty-Fifth consolidated 125 tail parser).
- Old label: "closure pole" for 820 in the tail parser; the nonterminal cases were logged as scout results.
- Why it is alive: 820 is the sign that shows up both with the 125 tail and in two rows where it is not terminal. If 820 can stand as a non-final sign, it is a candidate for the sign that links 125 to the tail and not a closing sign.
- What it would mean if true: 820 is a dual-role sign: final in most rows, medial in two, and the two medial rows both involve 032-002.
- Cheapest next move: Read the M-1677 and M-1045 photographs and check whether the 820 in each is the same glyph form as the terminal 820s; the glyph check is cheap and decides whether the nonterminal rows are one sign or a different one.

### 125-820 shared across two heads (390 and 405)
- What was seen: M-41 +740-636-240-233-235-002-405-125-820+ and Sktd-1 +390-004-002-390-125-820+ share the 125-820 ending. Sktd-1 (row 3875.1) is labelled A/a on CISI India n397, with a wrapped layout and not strict.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_sktd1_side_pair_recheck_20260531.md; campaign_032_002_861_002390x_sktd1_strictness_audit_20260531.md; campaign_032_002_861_002390x_390405_collision_adversary_20260531.md.
- Old label: Sktd-1 "downweighted" (wrapped layout, not strict); the 125-820 ending was not tested across heads.
- Why it is alive: The same two-sign ending appears after two different heads (405 in M-41, 390 in Sktd-1). If 125-820 is a portable ending, it behaves like a closing unit that does not depend on its head, which would be the first ending of that kind in this family.
- What it would mean if true: 125-820 is a closing unit shared across heads, and its head (390 or 405) is not part of the unit.
- Cheapest next move: Compare the M-41 and Sktd-1 photographs for the 125 and 820 glyphs only, in one crop each, to confirm the same two-sign ending before any head-independence claim.

### 002-405-501 is a near-formula that collapses 29 of 32 rows
- What was seen: 002-405-X has 32 rows; 29 are +520-240-002-405-501+. Mayig P122 and P086 pairs include M-34 and M-41 on 002-405.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_390405_collision_adversary_20260531.md; campaign_032_002_861_002390x_mayig_shadow_lane_check_20260531.md; campaign_032_002_861_002390x_near_frame_scout_20260531.md.
- Old label: "collision adversary" for 405 (the formula is almost one row repeated).
- Why it is alive: 29 of 32 rows sharing one formula is the strongest collapse in the family, and the 390 head (which branches 6 ways) does not do this. The contrast is the finding: one head is a near-single formula and the other is a branching head. The old agents used the collapse to discount 405, but a single repeated formula over 29 rows is itself a structure.
- What it would mean if true: 405 is a fixed-formula head: a single compound that a scribe reproduces, which is the opposite of the 390 branching behaviour.
- Cheapest next move: Count how many of the 29 are distinct physical objects (distinct source ids) rather than repeats of one source. If most are separate objects, the formula is a real fixed unit.

### Mayig P086 is shared by 390, 405, 406 and 407, which mixes two Lipi sequences
- What was seen: The provisional crosswalk puts 390, 405, 406 and 407 under P086. The Mayig shadow-lane check found that the pair looks like a shortcut but silently mixes two different Lipi sequences.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_mayig_shadow_lane_check_20260531.md; lipi_002_mayig_p122_source_conflict_gate_20260712.md; lipi_032_mayig_p145_source_conflict_gate_20260712.md.
- Old label: crosswalk trap; the provisional edges were not accepted.
- Why it is alive: A sign shared by four different Lipi signs in one Mayig code is either a coarse class or a sign that has two readings. Either way, the Mayig side is grouping signs by something the Lipi side has not separated, and the grouping could show which Lipi signs are the same class.
- What it would mean if true: P086 is a class code over 390, 405, 406 and 407, which would give the four heads one common class and would connect 405 (the fixed-formula head) to 390 (the branching head).
- Cheapest next move: Pull the Mayig P086 rows and list which Lipi rows they cover; check whether the two mixed sequences are the 390 and 405 ones.

### H-773 side A and side B: one side only, and the 530 chain
- What was seen: H-773 has row 1665.1 side A +740-798-803-002-390-530-741+ and side B row 1665.2 +700-033-711-335-575-413+. Vats Plate XCIV item 351 / object 12377 is "H-773B, one side only." Token windows under R/L: 741 0-75, 530 75-225, 390 225-340, 002 340-465, 803 465-565, 798 565-695, 740 695-815. Lipi derivative H-773_a.jpg is 269 x 170.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_h773_token_box_recheck_20260531.md; campaign_032_002_861_002390x_h773_side_guard_recheck_20260531.md; campaign_032_002_861_002390x_h773_lipi_image_map_guard_20260531.md.
- Old label: side guard (which side the object photograph shows); the row was held because the Vats label names only one side.
- Why it is alive: Side A has 002-390-530 in its token windows, which places a 530 chain on the object. The 530 chain is one of the few portable branch chains (see the 530 find below). If side A is the photographed side, the 530 chain is on a real object.
- What it would mean if true: 002-390-530 would be a chain on a single physical face, with 741 and 740 at the ends, and the object would carry one of the few multi-sign branch chains in the corpus.
- Cheapest next move: Decide which side the N358 crop shows (the Vats plate says one side only) by comparing the 741 window at 0-75 against the photograph, then report which row is attached to the photographed face.

### 530 is the only branch sign that chains across heads
- What was seen: 002-H-530-Y non-390 chains: 3/3 continuing; 530 has 4/4 one-complement rows and 4/4 closure-like complements. Under heads 296, 299 and 705, 530 is continuing 3/3. By contrast 590 has 3/7 terminal and only 1/4 closure-like complements.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_risky_parse_model_v1_20260531.md (Twenty-Fourth X-polarity cross-head transfer; line about 590 as failed adversary for 530 complement-linker rule); campaign_032_002_861_002390x_source_bound_intrinsic_sign_behavior_recheck.md.
- Old label: "complement-linker rule" for 530; 590 was tested as an adversary and not the same.
- Why it is alive: 530 is the one sign whose behaviour transfers across heads. The old agents used 590 as a failed adversary, but 590's failure is a difference from 530, which is what a separate class would look like.
- What it would mean if true: 530 is a linker sign with a fixed role across heads, the first such sign found, and it is the sign the H-773 side A chain depends on.
- Cheapest next move: Count the 530 rows across the strict layer, not only the parse-model set, and report the continuing share by head. The rerun is one query on the strict layer.

### 390-590-032 is a portable chunk, and 3335.1 carries it
- What was seen: Seven rows contain 390-590-032: L-139, L-196, L-198 (Lothal tags); M-1739, M-746, 3335.1 and M-965 (Mohenjo seals). M-746 and M-965 are source-visible at CISI Pakistan n90 and n128. 3335.1 = +740-205-032-002-390-590-032+, 29 x 29 mm, SEAL:S, Bull1:J, RAF, site Unknown. Upstream repo pinned at commit b272ad99c253ba7fa1e4cd91f48cce31f6d02bf4; raw sha256 c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98; 5,679 rows x 38 columns. In commit 0921d91d (2024-09-01, "externalize inscriptions") row 3335 read "museum = Private collection"; sibling 3118.1 also reads Private collection.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_390590032_family_recheck_20260531.md; campaign_032_002_861_002390x_3335_acquisition_packet.md; campaign_032_002_861_002390x_3335_identity_neighborhood_audit.md; campaign_032_002_861_002390x_3335_yajnadevam_provenance_recheck.md; campaign_032_002_861_002390x_3335_private_collection_cluster_probe.md.
- Old label: the 3335 row was held as a museum-provenance problem ("Private collection"), and the chunk was the 390-590-032 family only.
- Why it is alive: The same chunk sits in two source-visible Mohenjo seals (M-746, M-965) and in two Lothal tags, and 3335.1 is the only one with an unknown site. A chunk that appears on a documented seal and on a private-collection row is a copy test: the row's text either matches the photographed seal or it does not.
- What it would mean if true: The 3335.1 record is a real object whose text is the same 390-590-032 chunk as the source-visible seals, which would make the private-collection row a second witness for the chunk in a new location.
- Cheapest next move: Compare the 390-590-032 crop of M-746 and M-965 (source-visible) with the 3335.1 record's text; a match on the three signs is the copy test, and it needs only the pinned commit file already named.

### Row-order bridge M-940 looked like a link and was a row-position artefact
- What was seen: M-940 is row 2243.1 and is source-visible on CISI Pakistan n125. A row-order alignment appeared to bridge M-940 to a neighbouring row; the old agents rejected it as a false bridge.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_3335_source_identity_recheck.md; campaign_032_002_861_002390x_3335_yajnadevam_repo_trace.md.
- Old label: "M-940 row-order false bridge rejected."
- Why it is alive: A row-order bridge that looked real enough to test in the first place is evidence that the data file has adjacent records that align by position. If the upstream file has blocks of rows that were shifted, the 3335 and M-940 neighbourhood may hold other shifted pairs that are real links.
- What it would mean if true: Some apparent sign bridges are position artefacts of the file, and the 3335 neighbourhood is a source of such artefacts that could be sorted out by row-hash comparison.
- Cheapest next move: Hash each row's signs and compare the 3335 neighbourhood rows to the source-visible rows by sign content, not by row number, to list every shifted pair.

### Full-left formula determinism fails: one left context, six heads
- What was seen: M-708 with left 740-061 has six different heads: 817:2, 390:1, 400:1, 455:1, 575:1, 703:1. Seven of 15 target frames have full-left controls with other heads.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_full_left_formula_controls_20260531.md.
- Old label: "strong anti-determinism control" (the claim that a full left context fixes the head was rejected).
- Why it is alive: If one left context can take six different heads, the left context is not what picks the head. The head is picked by something else, and that something would be the sign the old agents called the "class selector."
- What it would mean if true: The head is chosen by a second-stage selector, not by the left context. That is a real grammatical claim about how the head is chosen.
- Cheapest next move: For M-708 and the other six-head left contexts, list the sign that follows each head and check whether the following sign is the selector.

### Final-left router: 004 and 032 split, and no two-sign collision
- What was seen: Splits occur only at left radius 1 (004 and 032), and 0 at radius 2 or more. Forty-Fifth compound-left router: final-left collision groups 004 = 095/125 and 032 = 590/692, with no left-bigram collision. Provisional router: 235 direct; 220-004 -> 095; 390-004 -> 125; 226-032 -> 692; 205-032 -> 590-032.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_left_context_radius_scan_20260531.md; campaign_032_002_861_002390x_risky_parse_model_v1_20260531.md (Forty-Fifth).
- Old label: "provisional" router; the radius scan was a null that rejected deeper context.
- Why it is alive: A split that appears only at radius 1 and is clean (no bigram collision) is a clear rule: the last sign before 002 decides the head for 004 and 032 and nothing else matters. The router's four named cases are a testable table.
- What it would mean if true: Only the sign immediately before 002 is needed to choose between 095 and 125 (after 004) and between 590 and 692 (after 032). The compound-left formula collapses to a one-sign selector in this family.
- Cheapest next move: Apply the four named router cases (220-004, 390-004, 226-032, 205-032) to the strict layer and count how often each predicted head matches the observed head. Report each case.

### Non-frame polarity is stable per head, the 692 terminal class
- What was seen: 692 non-frame terminal 58/77; 692 total 58 occurrences, 0 post-861, 47 terminal. 705 total 174 (0 post-861, 48 terminal). 416 total 46 (29 terminal). 698 total 10 (10 terminal). 125 total 50 (15 terminal).
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_branch_sign_ecology_20260531.md; campaign_032_002_861_tail_ecology (post861 hypothesis tournament and tail-rarity register scan).
- Old label: background counts used to set the tail baseline.
- Why it is alive: 692 is terminal in 75-81% of its rows and never appears after 002-861. A sign that always closes and never sits in the tail is the closing sign that the tail's terminal rule is built on, which makes 692 a control for what a closing sign looks like.
- What it would mean if true: 692 is a closing sign that never takes a tail, which means the tail rule is specific to a small set of signs, not all terminal signs.
- Cheapest next move: Check 692's post-861 count against a random sample of other terminal signs in the strict layer; if 0 is rare for all terminal signs, the tail rule is specific.

### Empty-prefix 002-861-X cluster: 416, 698 and 096 open the tail
- What was seen: When 002-861-X has nothing before 002, the X sign is 416 (6 rows), 698 (2 rows) and 096 (1 row). All nine are non-bare. 416 has 46 occurrences in total, 29 terminal; 698 has 10, all terminal. The tail-count table gives 603:3, 533-717:2, 255-416:1.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_post861_minimal_contrast*.md; campaign_032_002_861_post861_hypothesis_tournament.md; campaign_032_002_861_tail_rarity_register_scan.md; the 603 notes that set 416, 698 and 000 as "broad formula/background."
- Old label: "broad formula/background material rather than restricted-tail evidence" (the 603 and tail notes).
- Why it is alive: Nine rows is the only set of tails that open at the start of the line rather than after a sign, and all nine carry a tail. The old notes read them as background because 416 and 698 are common, but no bare row has an empty prefix.
- What it would mean if true: An empty-prefix 002-861-X is a line-initial tail, which would mean the 002-861 tail can stand without a preceding sign. The tail would be a free-standing unit in these cases, and its direction could be reversed (the reading was never tested).
- Cheapest next move: Run the direction-reversal test on the nine rows: read the 002-861 tail as written right to left, and check whether the reversed string matches a sign-order in the terminal set.

### 482 and 636 X-240 rows are the 240 class members that nearly close
- What was seen: 482 X-240-002-861 has 8 rows, 7 of them to 002-861, with 6 family cells. 636 has 15 X-240 rows, 12 family cells; H-360 (Vats XCVIII no. 584) is source-visible. 642 has 7 X-240 rows, 6 family cells; H-1845 (Harappa.com H2000-4484, Figure 42.05) is a public route; H-237 is metadata-only with ref 424.2. 000 is the bridge control with 810 occurrences.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_603_636_642_external_ecology.md; campaign_032_002_861_x240_family_cell_bridge_audit.md; campaign_032_002_861_603_external_ecology.md.
- Old label: X-240 "class" member pressure; 482 treated as approaching closure without matching 603.
- Why it is alive: 482 sends seven of eight rows into 002-861 through the 240 hinge, which is the closest any non-603 sign has come to 603's bridge behaviour. The class has 636 and 642 as sources with public or source-visible routes, so the class is testable from outside.
- What it would mean if true: X-240 is a class of signs with a shared bridge role, and 603 is only the one member whose subframe locks; the rest approach closure at different strengths.
- Cheapest next move: Pull H-1845 (Harappa.com H2000-4484, Figure 42.05) and H-360 (Vats XCVIII no. 584) and check whether the 240 hinge and the X sign match what the rows say.

### Two 002-861 tails share a 240 hinge in M-941 and M-706
- What was seen: M-941 +000-642-240-031-002-861+ and M-706 +740-773-240-002-861-031+ both have 240 directly before a 002-861 tail. The tail 031-002-861 is the same in both, at different positions.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_x240_post861_bridge_cluster_scan.md; campaign_032_002_861_x240_bridge_ecology.md.
- Old label: bridge cluster; not separately classed.
- Why it is alive: The same 031-002-861 tail follows the 240 hinge in two rows with different heads (642 and 773), which is the head-independence test that the 603 bridge did not pass. It is the same sort of cross-head fact as the 530 chain.
- What it would mean if true: The 240 hinge followed by 031-002-861 is a second portable tail route, separate from 603.
- Cheapest next move: Count 240-031-002-861 across the strict layer and report the head before 240 in each case.

### Strict 4,011 layer versus 4,135 raw count: a counting conflict to resolve
- What was seen: The forger and tail-attachment notes cite "strict raw rows 4,135"; other notes say "4,011 strict." The strict layer is described as 4,011 rows from 5,679 unfiltered in metadata_filtered.csv.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_replacement_branch_forger.md; campaign_032_002_861_002390x_tail_attachment*.md; /home/claude/ivc/research/data/open_prototype/lipi/metadata_filtered.csv.
- Old label: an inconsistency in the counts (not named as a verdict).
- Why it is alive: If 4,135 is the true strict count, about 124 rows have been dropped from the strict layer with no note, and the 603, 533-717 and 125 counts would shift. A count error is a finding about which rows the tests actually saw.
- What it would mean if true: Some tests ran on a layer that differs from the one the notes describe, which means some null results were computed on different data.
- Cheapest next move: Run the strict filter on metadata_filtered.csv directly and report the row count; the file is on disk and the check is one query.

### Dholavira 4237.1 and the page-18 seal: a 5-sign versus 6-sign conflict with a dimension match
- What was seen: Row 4237.1 is +151-032-388-002-390-705+ (6 signs), ZA-12:2, dimensions 27.62 x 21.31 x 7.11-11.17. The OCR mirror lists page-18 item 10 as Acc. No. 2118 with 5 signs. The OCR cluster also shows ZA-12:2, Acc. No. 8758 and the exact dimension string 27.62 x 21.31 x 7.11-11.17, matching the local row. Period 3C-2 in the route hunt against Period 5 in later notes.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_dholavira_4237_source_route_recheck_20260531.md; campaign_032_002_861_002390x_dholavira_8758_acquisition_packet.md; campaign_032_002_861_002390x_dholavira_8758_source_contact.md; campaign_032_002_861_002390x_source_route_hunt_20260530.md.
- Old label: "visual lookalike or wrong-object route" for page-18 item 10; the 8758 route called incomplete (text only, no image bound).
- Why it is alive: The dimension string matches exactly, the locus matches, and the accession cluster points at 8758 in one OCR record. The 5-versus-6 sign count is the only thing against it, and an OCR error on the sign count is a common fault. The period conflict (3C-2 versus 5) is in the same records.
- What it would mean if true: 4237.1 is Acc. No. 8758 at Lower Town ZA-12:2, and the object carries +151-032-388-002-390-705+, which would bring the 705 terminal branch onto a dated Dholavira seal.
- Cheapest next move: Bind Acc. No. 8758 to an image of the six-sign seal from the Bisht 2015 source, or check the sign count on the page-18 crop directly; either answers the 5-versus-6 question.

### H-1993 and H-1803 share Figure 17.07, and the CISI 3.1 volume holds both
- What was seen: H-1993 = row 744.2, +740-000-220-004-002-390-095+, TAB:B Harappa, H96-2769 Figure 17.07, ICIT 744. Figure 17.07 is also on H-1803 (562.1 and 562.2). The full CISI 3.1 HARP photo pages are 207-360, data pages 423-441. CISI vol 3.1 ISBN 978-951-41-1040-5 is also the target for M-1825 (row 3992.1, +157-031-002-390-705+, pointer BJ25710, Bhaskar S1 F2 unicorn only).
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_h1993_image_binding_recheck_20260531.md; campaign_032_002_861_002390x_h1993_source_route_recheck_20260531.md; campaign_032_002_861_002390x_m1825_source_route_recheck_20260531.md; campaign_032_002_861_002390x_cisi31_acquisition_route_20260531.md.
- Old label: source route pending (the photo pages were not yet bound to the row).
- Why it is alive: One book holds the photographs for two rows that share a figure, and the book's photo range (207-360) is a page block that can be checked in one visit. A single source binding would settle both rows, and H-1803 is a second row on the same figure.
- What it would mean if true: 740-000-220-004-002-390-095 is a long branch on a dated Harappa seal, with 095 at the close, and H-1803 would show the same figure with a second reading.
- Cheapest next move: Check the Figure 17.07 photograph in CISI 3.1 (pages 207-360) against the H-1993 string and the H-1803 string, one visit to the book.

### Outside contact on H-1993 is recorded as sent
- What was seen: The H-1993 source contact file records a source contact sent to Andreas Fuls with Omar Khan copied.
- Where: /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_h1993_source_contact*.md.
- Old label: source contact (no verdict).
- Why it is alive: It is an outside route already in motion, and an answer would bind the figure. It is a useful lead for the lead's list.
- What it would mean if true: A named person at the source can confirm the figure binding for H-1993.
- Cheapest next move: Lead should confirm from the record whether this contact was drafted for Cúper to send or sent; the sweep rules say outside email is drafted for Cúper to send, not sent, so this needs checking against the record before any follow-up.

## Sources on disk

- /home/claude/ivc/research/docs/archive/ (422 files): the campaign_032_002_861_* notes read in this sweep (002390x decision state, branch ecology, forger, risky parse model v1 log, 220032, 390004, 533717, 603, x240, tail sets, 3335, H-1993, H-773, Sktd-1, Dholavira 4237.1 and 8758, M-1825, CISI 3.1 notes).
- /home/claude/ivc/research/docs/archive/campaign_032_002_861_002390x_risky_parse_model_v1_20260531.md: 7,291-line parse-bet log (380KB); read by heading and selected test runs, not in full.
- /home/claude/ivc/research/data/open_prototype/lipi/metadata_filtered.csv: 5,679 unfiltered rows; strict layer 4,011 rows per the notes. Not queried in this sweep.
- /home/claude/ivc/evidence/tmp/h2147_source_route/kenoyer_meadow_1997_harappa.txt: Kenoyer/Meadow 1997 text on disk. Not read in this sweep.
- Upstream repo at pinned commit b272ad99c253ba7fa1e4cd91f48cce31f6d02bf4 (row 3335, museum label history in commit 0921d91d): named in the 3335 notes; local path not checked.
- CISI India and Pakistan IA leaves, CISI vol 3.1 (ISBN 978-951-41-1040-5, HARP photo pages 207-360, data pages 423-441): named in the notes; local path not checked.
- Vats Plates (XCIV item 351 / object 12377; XCVIII no. 584; XCIV no. 346): named in the notes; local path not checked.
- Kenoyer/Meadow 2010, Bisht 2015 Dholavira, Singh et al. ESM2: named in the notes; local paths not checked.
- Mayig corpus (P-numbered crosswalk): named in the notes; local path not checked.
- Lipi derivative H-773_a.jpg (269 x 170): named in the notes; local path not checked.
- Harappa.com H2000-4484 (Figure 42.05) and H96-2769 (Figure 17.07): public routes named in the notes.

## Ideas named but never run

- Direction-reversal reading of the nine empty-prefix 002-861-X rows (416, 698, 096): named in the tail notes, not run.
- Bind Acc. No. 8758 (or ZA-12:2) to a six-sign image of the Dholavira seal: named in the 8758 notes as the next gate, not run.
- Copy test of 3335.1 against the source-visible 390-590-032 seals M-746 and M-965: implied by the family recheck, not run.
- Blind layout test of 533-717 controls with the 533 and 717 signs cropped separately: named as a discriminator, not run.
- Strict-layer polarity test (125, non-125 after label shuffle within the strict layer): not run in this form.
- Per-head polarity table for focus signs across all rows (not only frames): named as the way to test the head-sign role, not run.
- After-240 subframe count across the full strict layer: named in the x240 notes as a possible test, not run.
- Orientation check of H-1138 slot boundaries under both R/L and visual LTR: named as open, not run.
- Recrop of the H-1138 edge to count units directly (clipped-unit question for 603): named in the closure note, not run.
- Glyph-form check of the 820 rows at M-1677 and M-1045 against terminal 820 rows: not run.
- Apply the four named left-router cases (220-004, 390-004, 226-032, 205-032) to the strict layer and count matches: not run.
- Count of 240-031-002-861 across the strict layer with the head before 240: not run.
- Strict filter on metadata_filtered.csv to resolve the 4,011 versus 4,135 count: not run.
- Row-hash comparison of the 3335 neighbourhood to list shifted pairs: not run.
- Consolidated 125 tail parser (Forty-Fifth) against the full strict layer: named in the parse log, not run on the full layer.
- Provisional translation-system rule in the parse log (around line 2995): named in the log; not read in this sweep and not treated as evidence.
- The 125-820 terminal-cap bet and the Forty-Ninth M-119 900-563 extension (singleton): named in the parse log; not read in full.
