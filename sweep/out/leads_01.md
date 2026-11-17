# Leads from reader 01 (salvage sweep, chunk_01)

Read: all 27 files in chunk_01, start to finish (research/docs/archive/campaign_032_002_861_002390x_*.md). I also read the 3335.1 acquisition packet, which the chunk files cite but which is not on my list.

Reruns: I reran the counts below from research/data/open_prototype/lipi/metadata_filtered.csv (5,679 rows). Scripts are in /tmp/sweep01/ (rerun.py, heads.py, dedupe_heads.py, sign_terminal.py, orient.py, matched_left.py, perm_390.py, stats.py, icon_class.py).

Conventions used below. "Distinct" means each distinct text string counted once; "raw" means every metadata row. "Row stops at X" means X is the last sign of the stored string. Stored order is the order in the file. The H-773 note in the chunk says R/L objects are read physically reversed, so a stored-order "stop" is a physical "start" for R/L objects. Every finding below is in stored order.

---

### 1. The sign after 002 decides whether the row stops, across ten heads

- What was seen: 002 occurs 851 times in the metadata. The sign right after it (the head) decides a lot. Distinct texts, row stops right at the head:
  - 861: 122 of 150 (raw 140 of 174)
  - 817: 120 of 128 (raw 148 of 156)
  - 820: 84 of 92 (raw 94 of 102)
  - 000: 44 of 55 (raw 47 of 58)
  - 824: 9 of 9
  - 390: 0 of 15 (raw 0 of 15)
  - 031: 0 of 15
  - 368: 0 of 12
  - 220: 0 of 11
  - 595: 0 of 7
  - 405: 0 of 4 distinct (raw 0 of 32)
  - Pooled: heads 817/820/824/861/000 stop 379 of 434 distinct texts. Heads 405/031/390/368/220/056/595 stop 0 of 65.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv (rerun: /tmp/sweep01/heads.py and dedupe_heads.py). Named but not opened: research/data/open_prototype/reports/campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv.
- Old label: "002-390-X" is the object. The file says the 390 branch is "frame-conditioned, not intrinsic", and the 002-861 frame is never scored as a frame. The campaign is named 032-002-861, and 861 is the largest head (174 raw rows, 11 times the 390 frame).
- Why alive: The 15-frame 390 set was the smallest head class the campaign looked at. The same stop/continue split shows across all of the 002 heads that have seven or more rows. Taking the distinct texts, 405's apparent size was a formula: 29 of its 32 raw rows are one string, +520-240-002-405-501+, and once that is collapsed 405 has 4 texts, all continuing. Duplicates do not produce the split. The split lives in the heads.
- What it would mean if true: 002 works as an opener and the head after it is a slot that sets closure. The 390 branch is one row of a bigger table, and 434 distinct texts have a closing head, against 65 with an opening head. A naive two-by-two test treating each distinct text as independent gives p near 2e-10 for 390 against 861 alone. Rows from one formula family are not independent, so read that p as an upper limit on how sure we should be.
- Cheapest next move: Split the head table by site (Mohenjo-daro against Harappa) and by object type (SEAL:S against TAB:B), counting distinct texts. If 0 of 65 against 379 of 434 holds inside both halves, the split is not a site or form artifact.

### 2. Sign-level closers and openers across the whole corpus

- What was seen: Distinct texts, share in which the sign is the last sign of the row:
  - Closers: 817 150/180 (83%), 091 15/19 (79%), 692 52/70 (74%), 820 160/219 (73%), 861 151/216 (70%), 824 13/19 (68%).
  - Middle: 000 547/1434 (38%), 095 8/22 (36%), 125 15/56 (27%), 705 40/169 (24%), 590 42/175 (24%).
  - Openers: 390 18/235 (8%), 405 5/75 (7%), 002 27/736 (4%), 740 19/1382 (1%).
  - Outside the 002-390 frame (raw rows): 692 stops in 58 of 76 (76%), 125 in 17 of 55 (31%), 705 in 57 of 217 (26%), 095 in 6 of 28 (21%).
- Where: metadata_filtered.csv (rerun: /tmp/sweep01/sign_terminal.py and orient.py). Also research/docs/archive/campaign_032_002_861_002390x_branch_sign_ecology_20260531.md, section "Focus-sign ecology outside the frame".
- Old label: Rejected. The file says to "reject the shortcut that 125 intrinsically means continuation or that 095/692/705 intrinsically mean closure." For 692 it says closure "cannot be generalized to sign 692 alone." Its own table already had 58 of 76 non-frame 692 rows closing, and the rejection rested on one source-visible continuing 692 (M-21).
- Why alive: Closure is a per-sign tilt that holds whether or not 002 comes before. 692 closes 74% of the time in distinct texts and 76% outside the frame. 817 closes 83% of the time and has never been in a gate at all. The old rejection was made on a small number of rows. Order-of-stop is a usable constraint with no reading attached.
- What it would mean if true: Signs carry a closure value, and that value is a grammar-like feature the decipherment can use before any sound or meaning is fixed.
- Cheapest next move: For each sign with 19 or more distinct texts, compare its stop rate with the stop rate of all other signs in texts of the same length. If 817, 692 and 820 stay high, the tilt is not a length effect.
- Contrary number (stated once): In stored order 740 is almost never last (19 of 1,382). Among R/L texts, 891 start with 740 and 10 end with it. The MAP line "closing jar sign 740" reads correctly only if R/L reversal is applied. The repo should say which order each claim uses.

### 3. The head split holds inside matched predecessor groups, and 390 is the open head

- What was seen: Take the complete sign string before 002 as the matching key. Within the 11 predecessor groups that contain a 390 head and at least two heads, the 390-headed rows never stop (0 of 14). Other heads in those groups stop 125 times out of 197. Shuffling the stop labels inside each group gives an expected 7.7 stops for 390. Zero of 20,000 shuffles reached 0, so P is below 5e-5 under that null.
- Predecessor 235, 35 distinct texts, a single matched group:
  - Closing heads 861, 817, 820 and 824: 22 of 23 stop at the head. The one that continues is 2851.1 (861 followed by 360 520 919 140).
  - Open heads 031, 460, 717, 392, 906, 390, 405, 220, 374 and 065: 0 of 12 stop at the head.
  - Singleton heads 112, 285 and 457: all 3 stop.
  - The 390 and 405 rows in this group carry 125 tails: M-38 (125 632 032), M-735 (125 195), M-41 (125 820). Lohumjo-daro 1981.1 has 392 then 590 125.
- Other groups (distinct texts): predecessor 032: 861 stops 8 of 10, 390 stops 0 of 2. Predecessor 004: 817 3 of 4, 861 3 of 4, 390 0 of 2 (H-1993 with 095 after it, Sktd-1 with 125 after it), 365 0 of 2. Predecessor 031: 817 5 of 5, 861 6 of 8, 390 0 of 1. Predecessor 803: 820 7 of 8, 861 5 of 6, 390 0 of 1.
- Where: rerun /tmp/sweep01/matched_left.py, perm_390.py, heads.py. Old file: research/docs/archive/campaign_032_002_861_002390x_left_context_radius_scan_20260531.md.
- Old label: "Branch alternatives exist only at radius 1 ... 004 and 032 ... source-blocked." Also "0 exact full-left groups with multiple 002-390-X branch alternatives." The old scan only let heads 390, 125, 095, 692 and 705 vote, so it could only find splits where two 390 frames share a predecessor.
- Why alive: Opening the head set to every 002 head gives 66 predecessor groups (of 139) with two or more heads at radius 1, and 85 radius-2 groups (of 405). The matched paradigm the old files say is missing (same left, different heads, different closure) shows up in many groups, not just 004 and 032. The old verdict is a label that came from the narrow head set.
- What it would mean if true: The head is the branch, and the predecessor only sets the menu. 390 is an open head that a closing head can replace in the same left context. Continuation after an open head is then decided by the next sign: 125 in three rows, 095 in H-1993, 692 in M-70, 590 in several.
- Cheapest next move: Pull the 35 texts of predecessor 235 onto one sheet with their full tails and check whether the open heads always take a 125 tail. Three of the twelve open-head rows put 125 right after the head. If the rest do not carry 125, the 125 tail is a property of those three heads, not of open heads in general.

### 4. 390 and 405 may be one head slot split by catalogue (Mayig P086 merge)

- What was seen:
  - M-41 (2569.1, Mohenjo-daro, Bull1:W SAN, 33.5 x 34.8) reads +740-636-240-233-235-002-405-125-820+.
  - Sktd-1 (3875.1, Surkotada) reads +390-004-002-390-125-820+.
  - Same tail, 125 820, under heads 405 and 390 with different predecessors (235 for M-41, 004 for Sktd-1).
  - The 405 class is 4 distinct texts once the duplicate string is collapsed (see entry 1).
  - research/data/sign_crosswalk/source_panels/390_P086_merge/manifest.csv maps 390, 405, 406 and 407 to one Mayig code, P086. It records the 390 rows as "dominant_member" and the 405, 406 and 407 rows as "source_visible_noninjective_merge_member." Its panels are on disk: M-12, M-17, M-32, M-82 (390), M-34 and M-172 (405), M-170 (406), M-171 (407).
- Where: metadata_filtered.csv; the manifest and eight CISI1 panel images above; the Mayig check in research/docs/archive/campaign_032_002_861_002390x_current_decision_state_20260531.md.
- Old label: "390/405 collision adversary blocks p086 collapse" — "29 of 32 rows are one formula; weak 405/406/407 to P086 edges remain unaccepted." M-34 and M-41 "align locally to 002-405."
- Why alive: After collapse, the 405 head has 4 texts, and one of them (M-41) has the same 125 820 tail as the 390 row Sktd-1. The model that says "one head slot, split by catalogue" predicts exactly that pair. Both rows continue, and both continue with 125 820.
- Contrary number (stated once): By eye, at this resolution, the first glyph of M-32 (390, position 1 in the manifest) is a large ring, and the first glyph of M-172 (405, position 1) is a hatched lozenge. They look different to me. Either the P086 merge is a code-level merge only, or my reading of the panels is wrong.
- What it would mean if true: The open-head class roughly doubles, and the two 125 820 tails pool into one instance.
- Cheapest next move: Put the matching-position glyphs side by side at full resolution: position 1 of M-32, M-17, M-171 and M-172, plus position 5 of M-34. Count the strokes in each. One sheet, one look.

### 5. 125 continues after open heads and stops after 861 once

- What was seen: 125 follows 390 in 4 rows and 405 in 1 row (M-41). It follows 392 (with 590 between) in row 1981.1. Row 1114.1 (Harappa SEAL:S) reads +390-004-002-861-125+: here 125 is the last sign after the closing head 861, with 390-004 before 002. Chanhu-daro 76.1 reads +125-002-861+ with 125 before 002.
- Where: metadata_filtered.csv. The old file says the terminal-125 search "inside true 002-390-X contexts" was still to run; this row is outside that frame.
- Old label: "125 is not intrinsically continuation-bearing; terminal 125 exists outside this frame" (17 non-frame terminal cases).
- Why alive: 125 looks like a continuer only after open heads (390, 405, 392) and a closer after closing heads (861 in 1114.1). That fits the head-slot model in entries 1 and 3 with no value attached to 125.
- What it would mean if true: 125 is a tail sign that follows open heads, and its "continuation" is a property of its environment, not of the sign.
- Contrary number (stated once): 1114.1 is a clean 125 stop inside a 002-head frame. It is the only one I found.
- Cheapest next move: Pull the source image for 1114.1 and check whether its last glyph matches the 125 glyph in the M-119 or M-735 panels already on disk.

### 6. The 390-590-032 unit is a portable chunk with 7 raw rows

- What was seen: 390 is followed by 590 in 59 of its 235 distinct occurrences (its most common successor). The 3-sign chunk 390-590-032 occurs in 7 raw rows across 3 sites:
  - Lothal: 2081.1 ]390-590-032-002-880[, 2116.1 ]390-590-032-002-000[, 2118.2 +740-390-590-032-002-000[
  - Mohenjo-daro: 2448.1 +740-390-590-032-060-201+, 3169.1 +740-440-220-032-741-390-590-032+, 3359.1 +740-390-590-032-741-527+
  - Unknown: 3335.1 +740-205-032-002-390-590-032+
- Where: metadata_filtered.csv (rerun: /tmp/sweep01/rerun.py, sign_terminal.py). Old label: research/docs/archive/campaign_032_002_861_002390x_3335_acquisition_packet_20260531.md calls it a "portable formula-family chunk" and treats it as adversarial pressure on 3335.1.
- Why alive: In 2081.1, 2116.1 and 2118.2 the chunk comes before 002, so it is a free-floating unit, not a copy of the 002 frame. The three Lothal rows are not identical strings. The 3335.1 row's 590 branch is then one more placement of a unit: the pair 390-590 occurs in 59 distinct texts overall. The adversary's formula-family worry needs identical copies, and two of the Lothal tails match (002-000) but the strings differ.
- What it would mean if true: 390-590-032 is a unit with its own internal order. 3335.1 is a legitimate placement, and the 002-390 frame is one of the places the unit can sit.
- Cheapest next move: Count distinct objects behind the 7 rows (the two Lothal 002-000 rows may be one object) and check whether any of them have source panels already on disk.

### 7. 3335.1 and M-143 split after the same complete left context 740-205-032

- What was seen: M-143 (2670.1, Mohenjo-daro, Bull1:J RAF, 23.9 x 24.1) reads +740-205-032-002-252-840+. 3335.1 (Unknown, Bull1:J RAF, 29 x 29) reads +740-205-032-002-390-590-032+. They share the full prefix and the same icon and cult class. Both continue after the head. The old full-left check recorded this exact group: "3335.1 | 740 205 032 | 252:1; 390:1." The M-143 panel is source-visible on CISI India leaf n80, per the m143 recheck.
- Where: metadata_filtered.csv; research/docs/archive/campaign_032_002_861_002390x_m143_prefix_control_source_recheck_20260531.md; research/docs/archive/campaign_032_002_861_002390x_full_left_formula_controls_20260531.md.
- Old label: "M-143 does not identify 3335.1 ... prefix control only." The old full-left count counted only 390 frames, so this group was not counted as a split.
- Why alive: This is a four-sign matched prefix with two different heads (252 and 390), and one side is source-visible. In the radius-3 scan (complete left context before 002), this is one of 41 groups with two or more heads. Both rows are in it. The file treats M-143 as a control. The split is the datum.
- What it would mean if true: The head after 002 is a menu of at least two items for the same left context, and 252 and 390 are two members of it.
- Contrary number (stated once): The two rows differ in size (23.9 x 24.1 against 29 x 29), so they are not the same seal.
- Cheapest next move: List every row whose stored string begins 740-205 and tabulate its heads. If 252 and 390 are the only two, the menu has two items and the split is clean.

### 8. Dholavira 4237.1 may be Acc. 8758: dimensions agree on three of four numbers, and page 18 item 10 is not yet counted

- What was seen:
  - Local row 4237.1 (Dholavira SEAL:S): horizontal 27.6, vertical 0, thickness 7.1 to 11.2. Its text is +151-032-388-002-390-705+.
  - The Bisht-mirror cluster the packet cites for Acc. 8758 / ZA-12:2 is 27.62 x 21.31 x 7.11 to 11.17. 27.6 and 27.62 agree, and 7.1 to 11.2 and 7.11 to 11.17 agree. The local vertical is 0, so 21.31 has no local partner.
  - Page 18, item 10 of Bisht 2015 (evidence/tmp/source_route_hunt_20260530/dholavira_pages/page-018.png; crop dholavira_page18_item10_whole.png): by eye I see about six or seven glyph shapes in the top band. The top band is the sign band. The mirror, as the packet quotes it, gives 5 signs for item 10, which it labels Acc. 2118. That mirror is not on disk. The local Bisht copy (evidence/tmp/source_route_hunt_20260530/Dholavira-Bisht2015.txt) has no individual-seal list, so I could not recheck the 5 and grep found no 8758 or 2118 entries.
  - The mirror's Acc. 8758 entry is described as a unicorn seal with no sign count (per the packet).
- Where: research/docs/archive/campaign_032_002_861_002390x_dholavira_4237_source_route_recheck_20260531.md and dholavira_8758_acquisition_packet_20260531.md; the page-18 images above; metadata row 4237.1.
- Old label: "wrong-object/lookalike pressure": page 18 item 10 is "Acc. 2118 with 5 signs," and 4237.1 has 6. "Metadata cluster pressure only."
- Why alive: The 5-sign count belongs to Acc. 2118, not to Acc. 8758, and the 8758 entry has no sign count. So the wrong-object verdict depends on a count that is not from the goal accession. The dimension match is on the same numbers, rounded. The page-18 eyeball count is six or seven, which is not five. If page 18 item 10 is 8758 with a shifted item number, 4237.1 is a real row with an image, and the repeated 705 line gets a second source.
- What it would mean if true: 4237.1 is a seal with its own picture, and "002-390-705" gets its first image-bound witness outside M-1825.
- Cheapest next move: Get a higher-resolution scan of Bisht 2015 page 18, count the item 10 top band, and check the item 10 caption against the 8758 and 2118 entries in the Bisht catalogue text (the PDFCoffee mirror, which is not on disk).

### 9. H-773 A: visible units and local sign count agree, and a Vats side-A plate may exist

- What was seen: Local row 1665.1 (H-773 A) reads +740-798-803-002-390-530-741+, which is 7 signs. The CISI Pakistan n358 tight crop (evidence/tmp/source_route_recheck_20260531/cisi_pakistan_n358_h773_A_signband_tight_w2400.jpg) has seven units per the file. By eye I see seven to eight. The Vats/Kenoyer 1997 entry, as quoted in the H-773 side-guard recheck, reads "One side only of the above eight H94/H95 tablets" for Plate XCIV item 351, which maps to H-773B (evidence/tmp/002390x_h773_vats_side_guard_20260531/Vats_Plate_XCIV_351_candidate_H773B_tight_from_v2.png). I have only that quote. My grep of the original text timed out.
- Where: metadata row 1665.1; the crops above; research/docs/archive/campaign_032_002_861_002390x_h773_side_guard_recheck_20260531.md; research/docs/archive/campaign_032_002_861_002390x_h773_token_box_recheck_20260531.md.
- Old label: "panel-bound, boxed-compatible, not strict." The Vats route is a side-B guard only.
- Why alive: The only continuing non-125 row after 390 with a source panel has a unit count that matches its local sign count. If the other side of those eight tablets is on another Vats plate, side A of H-773 may be pictured in the same book. That plate shows one side only, so side A is not on it. Whether side A is pictured elsewhere in the book is not checked.
- What it would mean if true: 530 then 741 after 390 is a second continuing head, so 125 is not the only continuing head after 390.
- Cheapest next move: Open evidence/tmp/vats_vol2_archive_metadata.json and find the plate holding the H94/H95 side-A items. Compare to the H-773 A crop. Not checked yet.

---

## Sources on disk

- research/docs/archive/campaign_032_002_861_002390x_*.md: 27 chunk files, all read. Plus the 3335.1 acquisition packet, read as a reference.
- research/data/open_prototype/lipi/metadata_filtered.csv: 5,679 rows, 3,745 distinct texts. Base for every rerun above.
- research/data/open_prototype/mayig/: records_index.csv, tree_manifest.csv, commit.json, sample_record.json, audit_summary.json. Mayig public-git crosswalk. Listed, not analysed.
- research/data/sign_crosswalk/source_panels/390_P086_merge/: eight CISI1 panels (M-12, M-17, M-32, M-82, M-34, M-170, M-171, M-172) plus manifest.csv. M-32 and M-172 viewed.
- research/data/sign_crosswalk/source_panels/m161_mismatch/ and m106_damage_span/: CISI1 panels. Listed only.
- research/data/open_prototype/reports/campaign_032_002_861_002390x_*.csv and .json: campaign outputs (about 935 files). Only the names cited in the chunk were checked.
- evidence/tmp/source_route_hunt_20260530/Dholavira-Bisht2015.txt and .pdf: Bisht 2015 full text (OCR). No 8758 or 2118 entries found by grep.
- evidence/tmp/source_route_hunt_20260530/dholavira_pages/page-018.png and dholavira_page18_item{9,10,11}_{whole,signband}.png: Bisht page 18 photos. Item 10 viewed.
- evidence/tmp/source_route_recheck_20260531/cisi_pakistan_n358_h773_A*.jpg and cisi_pakistan_n358_h773_B_full_w2400.jpg: CISI Pakistan page n358, H-773 A and B. H-773 A signband viewed.
- evidence/tmp/002390x_h773_vats_side_guard_20260531/Vats_Plate_XCIV_351_candidate_H773B_tight_from_v2.png: Vats Plate XCIV item 351, side B.
- evidence/tmp/vats_vol2_archive_metadata.json: Vats vol 2 archive metadata. Not opened.
- evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/src/assets/data/seal_id_and_image_mapping.json: Lipi image map. Not opened.
- evidence/tmp/m1206_bhaskar/S1-IndusZoomorphicIconCatalogue.txt and .pdf: Bhaskar S1 icon catalogue (lists M-1825 as F2 unicorn). Not opened by me.
- evidence/tmp/h2148_h2100_h2152_110_route/kenoyer2000_tiny_steatite_seals_harappa.pdf and curl_kenoyer2005.pdf: present. Not opened.
- research/data/mahadevan_20260905/source_witnesses/vats_553_555.png and research/tools/verify_vats_numerical_plate.py: present. Not opened.
- Not on disk: the PDFCoffee Bisht mirror with the individual-seal list (Acc. 2118 and 8758); the Singh et al. ESM2 supplement; the CISI 3.1 volume (not owned). Not checked: the Kenoyer-Meadow HARP PDF excerpt.

## Ideas named but never run

- Build all source-visible 125 -> 632 and non-125 -> 632 environments, and test whether 632-032 clusters after 002-390-125 across separate source families (linguistic_decision_gate, experiment 2).
- Find a third strict source-visible 125 branch family (family_independence_stress, next gate).
- Search for terminal 125 inside true 002-390-X source-bound contexts (current_decision_state, useful work item 5).
- Run the "collapse by site, register, object type, source route, exact formula, signless formula" batch and test whether the branch predicts tail class after the collapse (competing_linguist_hypotheses, next batch items 3 to 5). Entry 1 is a cheap version of this on the full 002 head set.
- Bind Sktd-1 strictly from a cleaner source, or find a dual strict 004 pair (current_decision_state, useful work item 2).
- Library or interlibrary-loan fallback for CISI 3.1 if the Tiedekirja payment link stalls (cisi31_public_access_guard).
- Find a non-IA route to M-1825 (museum archive, HARP entry, or excavation plate) (m1825_source_route_recheck).
- Dimension-only twins: 3335.1, M-71 (2599.1, Bull1:J SAN) and H-42 (1101.1, Bull1:J RAN) all measure 29 x 29 x 0 with a Bull1:J symbol. Nothing else links them. Untested.
- Check the source status of M-41 (2569.1). The Mayig check names it as aligning to 002-405, but I did not find a source panel for it on disk.
- Higher-resolution scan of Bisht page 18 item 10, to count the sign band directly (entry 8).
- Mayig P122 P086 as a crosswalk pair: guarded out by the file, not run as a test.
