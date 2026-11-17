# Salvage sweep, reader 00: leads

Read in full: the 33 paths listed in sweep/chunks/chunk_00 (research/docs/archive/; all paths relative to /home/claude/ivc). That includes active_decipherment_attempt.md (1,846 lines), read start to finish in chunks.

Two kinds of number appear below:
- "my pass" means I re-ran the count in this session on research/data/open_prototype/lipi/metadata_filtered.csv (5,679 data rows; a row is one side of one object; I took every 3-digit token from the text field, in order, and counted rows).
- "log" means the figure as the archive document reports it, under that document's own filter. Log figures are not reproduced by my pass and are labelled so.

Caveat: the logs cite crop and panel folders under tmp/ (for example tmp/3335_source_identity_recheck_20260531/). Neither /home/claude/ivc nor research/ has a tmp/ folder, so I did not see those images. Every visual claim below rests on the log's description of them.

---

### 1. 034 and 004 as a three-against-four stroke pair
- What was seen:
  - M-315 `+390-034-002-374-228-741+` (SEAL:S, square) against M-984 `+390-004-002-817+` (SEAL:S, Bull1, square). The 034 row runs on past 002; the 004 row closes after 817. My pass: the full M-315 string occurs once; 390 followed by 004 then 002 occurs in 12 rows (SEAL:S, TAB:B, TAG:L); the exact string `390-004-002-817` occurs in 4.
  - M-2104 (ROD) `+151-097-700-034+` against M-478, M-479, M-480 and M-1425 (TAB:B) `+400-097-700-004+`. Log: with 097 as left context, 700-004 appears at 4/9 against 700-034 at 1/116; right-tail Fisher p = 0.0000628573. The log counts the four 004 rows as two evidence units.
  - Sign-order counts, my pass: 034 is the last sign in 129 of the 155 rows that contain it (83%); 004 is last in 35 of 86 rows. Bigram 034-700 occurs in 14 rows and 700-034 in 113; bigram 004-700 occurs in 0 rows and 700-004 in 9. Log's own figure for the last-sign rate is 149 of 181 (a different filter).
  - Exact single-sign rows, my pass: `+034+` in 11 rows (9 pottery POT:T:g, 2 TAB:B). The log also reports 11. `+004+` alone occurs in 6 rows, all pottery.
  - Blind sort (log): three reviewers converged on S003-S005 as the strongest visual pair. Unblinded it is M-984 impression a (local 004) and M-315 upper face (local 034). The M-315 lower impression did not join.
  - Parpola's prose (log, text no. 12): the rod carries "three pots", and the tablet parallels "four pots".
- Where: research/docs/archive/active_decipherment_attempt.md (entries "M-315 strict blind sort", "M-2104 count-compound stress test", "M-2104 004 family-dependence adjudication", "M-2104 gate recheck, Harappa side", "M-1584 source check"); metadata rows 2833.1, 2453.1, 2527.1, 2962.1, 2963.1, 2964.1, 3710.1.
- Old label: "count_hypothesis_unvalidated" (M-2104); "negative gate result" (M-315); "crosswalk-dark" (034).
- Why it is alive: one reading accounts for four things at once: the three-against-four parallels, the 097 left-context skew, the 034-700 bigram (14 rows) with no 004-700 rows, and the 83% row-final rate of 034. Both minimal pairs put the sign in the same slot and end the sequence differently, which is what a count does. Blind readers found the pair similar, which is what two stroke bundles one stroke apart would look like. The only contrary figure is the Harappa-side resolution (a U/V unit with three secure strokes and a possible fourth). That is a limit on what the image shows, not a count.
- What it would mean if true: 034 and 004 are stroke tallies (three and four), written after a unit sign (700, which Parpola reads as a pot). Indus numerals were then bundles of strokes, and the lone 034 on pottery is a potmark for three.
- Cheapest next move: count strokes at native resolution, without labels, on the Marshall Pl. CXIV no. 532 leaf (IGNCA 48270_0205, 2601 x 3483, per the log), on M-984 impression a and on the M-315 upper face.

### 2. The copper register: 407 in repeated TAB:C frames
- What was seen (my pass): token 407 occurs in 113 rows (TAB:C, SEAL:R, SEAL:S, TAB:B, SEAL:C, MISC, TAG:P). Bigram 407-845 in 24 rows (TAB:C, SEAL:R, SEAL:S); bigram 407-061 in 23 rows; bigram 061-845 in 21 rows, all TAB:C. Token 845 in 52 rows. The exact string `+407-845-220-415+` occurs in 4 rows, all TAB:C (M-507, M-508, M-1456, M-1457). The exact string `+407-061-845-240-798+` occurs on six TAB:C rows (M-567, M-568, M-569, M-1515, M-1516, M-1517).
- Log: 407 in 53 of 444 SEAL:R or TAB:C rows, against 17 of 3,059 background; rank 1 of 714; Bonferroni p = 1.26e-31; max-stat label shuffle (3,000 iterations) false-positive rate 0. It survives excluding Mohenjo-daro (14/159 against 11/1812; Bonferroni 3.16e-7) and excluding Harappa (46/363 against 7/1958; 2.36e-28). Copper TAB:C: 18 of 94.
- External: CDLI P136689 line 2 reads "6(disz) ma-na uruda me-luh-ha" (six minas of Meluhha copper), checked live 2026-05-31. P228742 is lexical-list support only.
- Where: research/docs/archive/brief_407_rectangular_copper_register_20260531.md; research/docs/archive/brief_terminal_governor_unicity_20260531.md (the 845 and 095 notes); metadata rows above.
- Old label: "promoted candidate, not accepted; register/carrier class, copper a subtype; diffuse semantic bridge only."
- Why it is alive: the enrichment survives every block the log tried. The copper frame is a chain (407, a middle sign, 845, a closer) rather than one repeated text, and 845's copper signal vanishes without 407, so the two signs sit in one slot. The external line is a commodity phrase, which is the job a register sign on copper tablets would do. The contrary figure: 407 also occurs on SEAL:R, SEAL:S, TAB:B and MISC rows (my pass), so the sign is not copper-only.
- What it would mean if true: 407 is a commodity determinative ("copper of Meluhha") that opens copper-tablet lines, and 845 names the item.
- Cheapest next move: the log's own falsifier, run as a blind sort of the TAB:C rows with and without 407. A second check is 407 with 001, 803 or 415, which occurs in 26 rows (my pass; see entry 30).

### 3. The 220-415 closer shared by the 520 stem and the copper frame
- What was seen (my pass): bigram 220-415 in 75 rows (ROD, SEAL:R, SEAL:S, TAB:B, TAB:C, TAB:I); rows ending in 220-415: 29; exact `+520-220-415+` in 17 rows (SEAL:S, TAB:B, TAB:I). The copper strings `+407-845-220-415+` (four TAB:C rows, above) and `+407-845-220-415-798-000[` (M-1295, SEAL:R) end in the same 220-415 unit. M-1954 (SEAL:R, no icon) reads `+740-407-590-031-752-033-705-220-415-798-002-861+` (metadata row 2422.1), which carries both 407 and the 220-415-798-002-861 tail.
- Log: 520-220-415 splits Harappa 19 of 22 broad rows with 415 against Mohenjo-daro 8 of 26.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv rows 2983.1-2984.1, 3733.1-3734.1, 3600.1, 2422.1, 3711.1, 2377.1; research/docs/archive/active_decipherment_attempt.md ("520-220 Formula Stem Campaign").
- Old label: "fixed formula stem; X terminal/class/closure slot; 415 default" (520-220); the copper frames as "local formula/source-family work".
- Why it is alive: the copper frame and the 520 stem end in the same two signs. If 407-845 and 520 fill the same first slot, the "stem" is a slot with two fillers, one Harappa and one Mohenjo-daro copper. That would tie the Harappa title-formula reading to the copper commodity reading.
- What it would mean if true: 520, 407-845 and 220-415 form one closing unit with a class prefix. The prefix marks the commodity or office, and the closer stays the same.
- Cheapest next move: count rows where the slot before 220-415 is 520 against 407 or 845, split by site and type (metadata query, no images needed).

### 4. 415 as Parpola's text-7 terminal sign 107 (comb or rake)
- What was seen: local rods M-2109 and M-2111 (ROD, R/L; metadata rows 4042.1, 4044.1) both read `+400-000-220-415+`. Log (Parpola 2019, text no. 7): the text ends uniquely in sign 107, which Parpola 1994 Fig. 5.1 draws as a comb or rake-like sign. The log recut M-37 (SEAL:S) and reads 415 there as a comb-or-rake form with a stem.
- Where: research/docs/archive/active_decipherment_attempt.md ("Parpola text no. 7 scope / namespace gate", "Parpola text no. 7 feature namespace bridge gate", "M-37 terminal recut gate").
- Old label: "namespace gate, no exact string family; numeric shortcuts blocked." The log blocked the numeric route (local 107 is not Parpola 107). It did not test the visual route, where the comb ending of text 7 and the terminal 415 of the rods would be the same graphic.
- Why it is alive: the one structural fact Parpola gives about text 7 (it ends in a comb) matches a terminal 415 on the two local rows for that text. The numbers are not the bridge; the drawing is. The contrary figure: the log's M-77 check (a five-sign seal string, not the same family) downgraded Parpola's recurrence sentence. That weakens the text-7 set as a family but leaves the terminal match.
- What it would mean if true: 415 is a comb sign, and the 520-220-415 closer is a comb ending on Harappa tablets.
- Cheapest next move: a blind sort of the terminal 415 panels (M-37, H-938 A, H-940 A, and the two rods if imaged) against the Fig. 5.1 comb 107 crop that the log's packets name.

### 5. Parpola's reverse-side clue points at the shorter local row, seven objects out of seven
- What was seen (log): in H-938, H-939, H-1284 and H-2145, Parpola's VIIII reverse clue aligns with the shorter `034/700` companion row, not the longer 415 row. In H-940, H-2147 and H-2148, the sign-41 reverse clue aligns with the shorter `110` row. My pass confirms the rows: H-938 1818.1 `+520-220-415+` (L/R) and 1818.2 `+034-700+` (R/L); H-939 1819.1 `+700-034+` and 1819.2 `+520-220-415+` (L/R); H-1284 4069.1 `+520-220-415+` and 4069.2 `+700-034+` (L/R); H-2145 827.1 `+700-034+` and 827.2 `+074-220-415+`; H-940 1820.2 `+110+`; H-2147 673.1 `]110+`; H-2148 481.2 `+110+` (direction NR).
- Where: research/docs/archive/active_decipherment_attempt.md ("Parpola reverse/local short-side consistency gate"); metadata rows above.
- Old label: "role-consistent" (log); "same-role inference, not a stated same-side source bridge."
- Why it is alive: seven objects, seven matches. The prior-work clue was read off Parpola's text and only then checked against the local rows, so it is a prediction that could have failed. The log is right that it is a same-role inference, and that is the claim the argument needs.
- What it would mean if true: Parpola's reverse-side sign numbers mark the short side of each group. The shorter rows carry the sign Parpola names (34 or 110), and the 415 rows are the long side.
- Cheapest next move: compute how often a random reverse-side assignment lands on the shorter row across every object Parpola cites. The log has no chance baseline, so this is counting from the log's list and the metadata.

### 6. 110 as Parpola sign 41 (kneeling pot), H-2148
- What was seen: H-2148 has two rows: 481.1 `+520-220-415+` (R/L) and 481.2 `+110+` (NR). Kenoyer 2005 Figure 14.1 shows a one-sign panel and a three-sign panel on one H2001-5142 face (log). Parpola 1994 Fig. 5.1 sign 41 is the anthropomorphic / kneeling-pot family, on PDF p. 88 (printed p. 70).
- Where: research/docs/archive/active_decipherment_attempt.md ("H-2148 110 source route", "110 crosswalk decision gate", "Parpola 1994 sign 41 convention gate", "H-2148 same-side identity gate", "P041 / Parpola 41 falsification gate").
- Old label: "public_visual_route_count_mapped and cleanest branch candidate"; "same_side_identity_pending"; "conflict-gated" for the Mayig P041 route.
- Why it is alive: the one-sign panel and the local 110 row agree in count; the sign-41 pot suits a short vessel-like unit; and the 110 row sits on the reverse side that the seven-object pattern predicts (entry 5). The Mayig P041 route is a namespace trap that the log already showed, so no crosswalk is needed to make the case.
- Contrary, once: the 110 row is NR (not rotated), so the reverse assignment for this object rests on a direction field that is not R/L.
- What it would mean if true: local 110 is Parpola's kneeling-pot sign 41, a vessel-bearer determinative placed on the short side of a group of tablets that share an obverse text.
- Cheapest next move: settle the same-side label. Either the Harappa/Fuls reply on H2001-5142 side labelling (sent, per the log), or the CISI 3.1 end matter for H-2148.

### 7. The R/L direction policy holds in three independent controls
- What was seen (log): under recorded R/L, 700 lands on the vertical or bar component in H-930 B (`+700-032+`), H-789 B (`+033-700+`) and H-942 B (`+033-700+`), and 032 or 033 land on a V, leaf or loop-like component. A coin-flip direction policy gives all three together with probability 1/8 = 0.125 (my arithmetic, treating the three calls as independent 50/50).
- Contrary, once: direction is recorded per row, not per object. In H-938 the 415 row is L/R and its 034-700 companion is R/L; in H-942 the 016 row is L/R and the 033-700 row R/L; H-939 and H-1284 are L/R on both rows; H-910, H-930 and H-789 are R/L on both rows (my check of the metadata). So the H-938 and H-910 comparison depends on a per-row field.
- Where: research/docs/archive/active_decipherment_attempt.md ("M-1206 direction policy provenance", "M-1206 independent direction controls gate", "H-938/H-910 direction sensitivity gate"); research/data/open_prototype/lipi/metadata_filtered.csv field "dir.".
- Old label: "working corpus policy only; not computed from images."
- Why it is alive: the policy comes from the Lipi "dir." column and has passed three checks against source-visible components. It is a working policy that could have failed and did not.
- What it would mean if true: the stored direction is the physical order for most rows, and 700 is a vertical bar sign across the 700 frames.
- Cheapest next move: check the dir. field against the side labels on M-37 and M-1206 (A and a). Both are source-visible, so this is a direct test.

### 8. 034 and 415 at two ends of one object; a same-site triad
- What was seen: H-938 carries `+520-220-415+` (A, A bis) and `+034-700+` (B), on one object. H-910 B carries `+700-034+` with its components reversed. Under recorded R/L, 034 is the loop or leaf in both H-938 B and H-910 B, so direct 034 = 415 component identity is negative under that policy; under forced L/R the assignment flips (log). M-1206 `+520-220-034+` (Gaur, SEAL:S, square) has a terminal component that its blind neighbours put beside H-938 A (415) and M-37 (415). Same-site, same-shape triad: M-1912 `+520-220-003+` (metadata row 2441.1, CISI 3.1-gated), M-1206 (034), M-37 `+520-220-415+` (SEAL:S, square).
- Where: research/docs/archive/active_decipherment_attempt.md ("M-1206 034 cohesion gate", "M-1206 terminal component gate", "H-938 same-object source-panel audit", "H-938/H-910 component checks", "M-1912 source gate", "M-1206 allograph decision gate").
- Old label: "allograph, separate visual-family sign, source-side artifact and transcription-policy split all remain live."
- Why it is alive: within H-938, 034 and 415 sit side by side, and the M-1206 terminal stays visually stable under reversal and reordering (two blind readers agreed). A triad with one prefix (520-220) and three different closers is the cleanest small set in the log.
- What it would mean if true: 034 and 415 are one terminal drawn in two halves (bundle and leaf), and the reading depends on which half is read first.
- Cheapest next move: a direction-free test. Mark only the loop/leaf and the bundle on H-938 B and H-910 B, without using R/L, and check whether the same component sits on the same physical side.

### 9. Stored order beats its alternative 83% of the time under formula-family controls
- What was seen (log): under the harsh leave-source-convention-out gate on site|type|material|symbol|cult|direction, the stored-win share is 0.832877, with the maximum admissible null at 0.020000. The source-convention collapse (175 rows) gives 0.805714 against a null maximum of 0.005000. The exact L/R set is null-compatible; the harsh L/R set (11 rows) gives stored-win 0. Route-conditioned: 38 public-route rows in the top 79 give 0.684211; source-page collapse 0.625; route-label nulls reproduce or beat it.
- Where: research/docs/archive/active_decipherment_attempt.md ("directionality formula-family controls", "directionality route-conditioned support gate"). The log also links docs/effective_unicity_directionality_formula_family_controls.md, which is not on this chunk and not under research/docs/archive/.
- Old label: "survives the metadata-only source-convention gate; does not validate physical direction; route-conditioned support does not promote it."
- Why it is alive: the metadata-only survival is the strongest direction figure in the log, and it survives the family collapse that removed the earlier directional claims.
- What it would mean if true: the stored Lipi order is the physical reading order for most multi-sign seals, so every order-based claim in this log can be read at face value.
- Cheapest next move: read the definition of "stored-win" in the linked document (not on this chunk), then run the harsh metric on the L/R-only and R/L-only subsets separately.

### 10. A two-pole split under 002: closers (817, 820) against continuers (390, 368, 031, 220)
- What was seen (log): 499 strict deduplicated all-002 rows. Closure pole 817/820 (174 rows); branch pole 390/368/031/220 (43 rows); 861 kept out as leaky (119 rows). Best split z = 13.211692 and terminal-rate gap 0.954023; worst false-positive rate 0 across 10,000 iterations per null model. The adjacent 032-002 scope fails (worst FPR 0.5205 for z, 0.7552 for the gap). Y-class predicts terminality at accuracy 0.885772 against 0.579158 for site/type/symbol. Terminal counts: 817 100 of 103; 820 66 of 71; 861 95 of 119.
- Where: research/docs/archive/active_decipherment_attempt.md ("matched terminality campaign", "post-hoc partition control", "broad 002-Y partition source queue", "post-Y continuation campaign"); research/docs/archive/campaign_002_y_partition_source_queue.md.
- Old label: "real closure/continuation pole split in the metadata layer"; "source normalization bottleneck" (the branch pole had route hooks only on 390 until public CISI routes for 368, 031 and 220 were added).
- Why it is alive: the post-hoc partition test lets every null corpus choose its own best cut under the same thresholds, and none beats the real split in 10,000 tries. A two-pole Y slot is a clean grammatical claim with a source route (the public CISI routes for 368, 031 and 220 listed in the log).
- Contrary, once: Y-class is informed by terminality, so the log flags the next gate as a source-boxed, family-blocked holdout.
- What it would mean if true: 002 opens a Y slot with two poles, closing and continuing. That is a verb-like frame, and the 817/820 and 390/368 classes are its two conjugations.
- Cheapest next move: a site-held-out refit on the 499 rows (metadata only), then the source boxes for one 817 row and one 390 row.

### 11. 240 selects the 032 lane (the 240-220-032 selector)
- What was seen: my pass finds 9 rows with the string 240-220-032 (SEAL:R, SEAL:S); bigram 220-032 in 56 rows. Log: 314 clean known-next 220 rows, 251 strict frame-text dedup units. 240 goes to 032 at 9/12 against 46/239 for other frames. It survives no-companion (9/12 against 43/215) and matched site/type/frame/text blocking (9/12 against 35/150). The main block is Mohenjo-daro SEAL:S at 6/7 against 23/104; without that block it is 3/5 against 12/46. Seven of nine 240-220-032 rows continue after 032.
- Visual packet (log): bare closures H-444, M-723, M-1044; simple tail M-240 `603`; compound tail M-91 `255-416`. Source-visible.
- Where: research/docs/archive/active_decipherment_attempt.md ("240-220-032 selector contrast", "220-032 source-visible contrast packet", "220-032 register/length falsification test", "220-032 terminal-space recut", "source-first terminal-space campaign").
- Old label: "best live sign-function candidate; positional formula or constructional selector"; terminal space "blocks grammar promotion."
- Why it is alive: the 240 effect survives every filter the log set. The terminal-space objection is a measurement problem: tailed rows have 120-525 px of terminal content and bare rows 28-45 px, and no bare row has room comparable to the tailed ones. Until a bare row with comparable room turns up, the confound is open in both directions.
- What it would mean if true: 240 is an entry selector into a typed continuation after 032, and the choice among closure, simple tail and compound tail is positional.
- Cheapest next move: find or photograph a bare-closure row with terminal space comparable to the 120 px tailed windows.

### 12. 002 introduces the post-032 branch
- What was seen (log, deduplicated units): A-220-032 goes on to next 002 in 24 of 55 against 16 of 257 outside 032 (odds ratio 11.66). Core 002-861/820/817 in 16 of 55 against 8 of 257 (OR 12.77). Core terminal tails in 14 of 55 against 6 of 257 (OR 14.28). Removing Mohenjo-daro SEAL:S from strict rows: A-220 next 002 in 6 of 28 against 12 of 387 outside (21% against 3%). Adjacent strict 032-002 rows: 817 4/4 terminal, 820 6/7, 861 7/9, 390 0/2.
- Where: research/docs/archive/active_decipherment_attempt.md ("032-002 tail campaign", "032-002-Y leave-one-block campaign", "032-002 post-Y continuation campaign").
- Old label: "promote A-220-032-002-{861,820,817} as a live short continuation/closure formula" (log); "002 is a post-032 branch introducer candidate."
- Why it is alive: the odds ratios are large and the effect holds in the leave-one-block test. The counts are small (55 and 28), but the direction is stable across every scope the log tried.
- Contrary, once: with the Mohenjo-daro block removed, the terminal-tail contrast falls to 5 of 28 against 6 of 387, the weakest number in the chain.
- What it would mean if true: 002 is a clause-level branch particle after the 032 frame, and 817, 820 and 861 are the closing choices it offers.
- Cheapest next move: the same odds ratio on Harappa-only rows (metadata query). That tests the block that dominates the count.

### 13. The restricted post-002-861 tail: 533-717 and its register
- What was seen: the log's fixed-prefix control leaves one survivor across the raw (4,135 rows) and deduplicated (3,074 rows) scopes: 533-717, with witnesses M-376 `+740-100-176-002-861-533-717+` and M-391 `+405-845-686-740-793-003-233-805-002-861-533-717+`. Worst recorded FPR 0.006; context-shuffle FPR 0.0002 globally and 0.0010 within site/type/symbol. My pass: 533 occurs in 2 rows and 717 in 41 rows; the bigram 533-717 occurs in 2 rows, both SEAL:R. Both witnesses are SEAL:R, cuboid-convex, no icon. Log: 2 of 144 strict 002-861 rows carry the tail. Mohenjo-daro SEAL:R with 002-861 splits into bare 3, 533-717 2, 603 1, long tail 1.
- Where: research/docs/archive/active_decipherment_attempt.md ("accepted 002-861 restricted-tail finding", "533-717 register test", "533-717 source-family independence", "post-861 tail ecology"); metadata rows 2872.1, 2887.1, 2422.1.
- Old label: "accepted structural claim" (the restricted-tail finding), later "one single source/register-family cell, not a value."
- Why it is alive: the fixed-prefix control was built to reject exactly this kind of claim, and one survivor still remains across both scopes. The register is a physical-object class (uncovered rectangular and cuboid seals), which gives a second reason a tail could be locked to it. Row 2422.1 (M-1954) puts the register and the copper frame (entry 2) on one no-icon SEAL:R cell.
- What it would mean if true: 533-717 is a fixed final unit that only rectangular no-icon seals close with, and the no-icon register carries both the 533-717 closer and the 407 copper marker.
- Cheapest next move: count 533 and 717 separately across the strict rows, outside the pair. If 717 appears in unrelated frames, the pair is a shared compound. If neither appears outside 533-717 or 002-861, the pair is locked to the register.

### 14. 603 as the only shared sign between the Harappa X-before-240 frame and the post-002-861 tails
- What was seen: my pass finds 603 in 7 rows (SEAL:C, SEAL:R, SEAL:S, TAB:B). Log: across 4,011 strict rows, three are terminal after 002-861 (M-240, M-714, M-1273), three form the Harappa string `+740-603-240-060-692+` (H-1137, H-1138, H-1846), and one is weak `+000-603-091-190+`. H-1138 is visible in Vats Plate XCIV no. 346 (p. 345); H-1846 in Kenoyer and Meadow 1997 Figure 11.11; H-1137 is a route note only. The X-before-240 frame has 95 strict rows and 28 distinct X signs. The string 240-060-692 occurs 7 times, always after 740, with X = 603 (3), 642 (2) and 636 (2). Sign 636 is in 15 of 15 X-before-240 frames and 0 after 861; 642 is in 7 of 7 and 0 after 861.
- Where: research/docs/archive/active_decipherment_attempt.md ("603 mobility campaign", "603 source-route pass", "603 source-normalized slot-family campaign", "X-before-240 internal subframe campaign", "X-before-240 interpretation pass"); metadata rows 3139.1 (M-714), 3580.1 (M-1273).
- Old label: "live bridge candidate, not a value"; "copied-template artifact" is the rival.
- Why it is alive: 603 is the only non-background sign that appears in both constructions. Two of its three Harappa rows are source-visible, which the log says survives the duplicate-collapse check as two source-visible objects.
- Contrary, once: H-1137, H-1138 and H-1846 may come from one copied tablet family, which would make the Harappa side a single witness.
- What it would mean if true: 603 is a mobile addendum or classifier that can close a Mohenjo-daro seal after 002-861 and also close a Harappa tablet formula.
- Cheapest next move: a cross-context graphic check. Put H-1846 (Figure 11.11) and M-1273 (CISI Pakistan leaf n195, source-routed) at the same scale, with 636 and 642 as blind controls.

### 15. Terminal governors: 002 and 060 choose their closers from a small set
- What was seen (log, exact-collapsed cells): 002-817 108 (105 terminal), 002-820 75 (70), 060-920 52 (51), 060-550 24 (23), 060-820 23 (23). Terminal-label shuffle p = 0 of 5,000; row-internal order null p = 0 of 2,000; penultimate-final independence null over 2,127 terminal text families p = 0 of 5,000. Held-out final-sign prediction: governors 002 and 060 reach top-3 accuracy 0.787 over 456 leave-site rows (mean effective candidates 6.39), against 0.177 over 1,138 non-governor penultimate rows (15.71). Removing Mohenjo-daro SEAL:S: 0.761 (234 rows); removing Harappa SEAL:S: 0.806 (407 rows); removing both: 0.778 (185 rows). Non-governor 240 reaches 0.652 over 23 rows; 740 is 0.090 over 133 rows; 220 is 0.286 over 56; 390 is 0.127 over 55.
- Where: research/docs/archive/brief_terminal_governor_network_20260531.md; research/docs/archive/brief_terminal_governor_unicity_20260531.md.
- Old label: "promoted structural candidate, not accepted"; the lower branches fall below the n >= 20 floor when Mohenjo-daro SEAL:S is removed.
- Why it is alive: this is the cleanest held-out result in the chunk. The predictive gap survives every block the log removed, and effective candidates shrink from 15.71 to 6.39.
- Contrary, once: the 240 mimic reaches 0.652 on 23 rows, and the lower branches (060-550, 060-820, 060-692) drop out below the floor without the large seal block.
- What it would mean if true: 002 and 060 are clause-final governors of a closed closing set, so the slot grammar has at least one closure operator.
- Cheapest next move: rerun the leave-site top-3 on TAB:B and TAB:I rows only, to see whether the gap holds where the seal blocks are absent.

### 16. The 741/742/745 selector and the 060-920 cap
- What was seen (log): 741-060 is followed by 920 in 31 of 31 raw rows and 30 of 30 exact-collapsed cells; all 31 end after 920. 060-920 has 53 raw rows (52 exact cells, 51 terminal). The predecessor 741 supplies 30 of the cells, 742 supplies 7, and 745 supplies 3. Right-tail Fisher p = 1.47e-64 against all other bigrams. The successor-shuffle null (5,000) never reached 30 of 30. Selector: 741, 742 or 745 comes before 060-920 in 40 of 52 object-collapsed cells, and before the sibling caps 060-692, 060-550 and 060-820 in 0 of 84. The result survives leaving out Mohenjo-daro or Harappa. Seven sites; mostly SEAL:S, plus TAB:I, TAB:B, TAG:P and TAG:R.
- My pass, wider: any row containing the bigram 741-060 has 33 rows; any row containing 060-920 has 58. These are wider than the log's counts, which use its own filter, so the log's 31 and 53 are the figures used here.
- Blind visual reads (log): the first read recovered five of six 741-060-920 rows as caps; the second read called all six non-741 060-920 rows cap-like and rejected five of six controls.
- Where: research/docs/archive/brief_741060920_terminal_formula_20260531.md; research/docs/archive/brief_terminal_governor_network_20260531.md (selector subclaim).
- Old label: "promoted visual candidate; not accepted."
- Why it is alive: blind readers recognise the cap as a visual unit, not only in metadata. The selector set is three sign numbers that behave the same way, which is what a syntactic class looks like.
- What it would mean if true: 741, 742 and 745 are three shapes of one selector sign, which picks the closing cap 060-920 and nothing else.
- Cheapest next move: a blind sort of 741-060 rows on TAB and TAG artifacts (not seals). The log's falsifier is a clean source-visible 741-060 row that is not followed by 920.

### 17. Branch polarity after 002-390: 125 continues, 692 and 095 close
- What was seen (log): 15 adjacent 002-390-X rows with 10 distinct next signs. 125 appears in 4 of 15 rows (M-38, M-119, M-735, Sktd-1) and always continues in frame. Source-visible strict core: M-119 and M-735 continue with 125; M-70 (692) and M-71 (095) close. Outside the frame, 125 is terminal in 17 rows; 095, 692 and 705 continue in 200 rows. 390-125 inside 002-390 is 4 of 4 continuing; outside it, 3 terminal and 2 continuing. 390-095 inside 002-390 is 2 of 2 terminal.
- Where: research/docs/archive/active_decipherment_attempt.md ("002-390-125 source-route campaign", "family-collapsed branch ecology", "alpha blind boundary read", "branch-tail prediction", "replacement branch-sign ecology recheck", "source-bound intrinsic sign-behavior guard", "390-X context control"). Panel crops are not on disk (see caveat above).
- Old label: "live as continuation-bearing branch candidate, not value or function."
- Why it is alive: the frame, not the sign, decides polarity. The log's intrinsic shortcut (125 means continue) fails outside the frame, which leaves the frame as the thing that matters. The 002-conditioning survives the generic 390-X alternative.
- Contrary, once: four strict rows is a small set, and no matched same-predecessor arm is strict yet (the 004 arm has H-1993 route-only and Sktd-1 wrapped).
- What it would mean if true: the branch after 002-390 is a polarity choice. 125 keeps the inscription open; 692 and 095 close it.
- Cheapest next move: CISI 3.1 pages for H-1993 (a route in the log; purchase in progress) to make the 004 arm strict, and a tighter Sktd-1 crop.

### 18. The 032 matched lane: M-70 against 3335.1, with a prefix sibling
- What was seen: M-70 `+226-032-002-390-692+` is source-visible (CISI India n66, printed p. 31). 3335.1 `+740-205-032-002-390-590-032+` (29 x 29, SEAL:S, Bull1:J, RAF) has no object ID. My pass finds exactly two rows containing 032-002-390, the same two as the log. M-143 `+740-205-032-002-252-840+` is source-visible on CISI India leaf n80 (printed p. 45) and shares the prefix 740-205-032-002 with 3335.1, but takes 252 next. My pass finds exactly two local rows with the 740-205-032-002 prefix.
- Where: research/docs/archive/campaign_032_002_861_002390x_3335_acquisition_packet_20260531.md; ..._3335_identity_neighborhood_audit_20260531.md; ..._m143_prefix_control_source_recheck_20260531.md; ..._3335_yajnadevam_provenance_recheck_20260531.md; ..._3335_yajnadevam_repo_trace_20260531.md; ..._3335_private_collection_web_scout_20260531.md; ..._3335_yajnadevam_source_contact_20260531.md. Metadata rows 3335.1 (id), M-70, M-143.
- Old label: "single-object matched-gate unlock; external source binding required."
- Why it is alive: this is the only same-predecessor (032) lane where one arm is strict and the other is one row away. A strict pair would split the 002 branch with the predecessor held fixed. The prefix sibling shows that 002 can take 390 or 252 right after 740-205-032-002.
- Contrary, once: 3335.1 may be a copy of the 390-590-032 formula family (seven rows carry that chunk; M-746 and M-965 are the source-visible controls).
- What it would mean if true: after the 032 frame, 002 chooses between 390 and 252 as a branch, and 590-032 closes the 390 branch.
- Cheapest next move: wait on the Yajnadevam reply (request sent). No local route is left, per the log.

### 19. The repeated 002-390-705 closer, at two sites with different prefixes
- What was seen: Dholavira 4237.1 `+151-032-388-002-390-705+` (SEAL:S; 27.62 x 21.31 x 7.11-11.17 mm per the log's OCR mirror) and Mohenjo-daro M-1825 `+157-031-002-390-705+` (17.5 x 18.5; metadata row 3992.1). Two local rows end in 002-390-705 under different leading frames at two sites. Dholavira item 10 on the Bisht page 18 looks compatible with the reversed string; the log's OCR mirror gives the matching ZA-12:2 locus.
- Where: research/docs/archive/campaign_032_002_861_002390x_dholavira_8758_acquisition_packet_20260531.md; ..._m1825_acquisition_packet_20260531.md; ..._dholavira_8758_source_contact_20260531.md; ..._m1825_source_contact_20260531.md; research/docs/archive/active_decipherment_attempt.md ("Dholavira 4237.1 metadata-cluster route").
- Old label: "source_image_candidate_unbound"; "not strict 705."
- Why it is alive: two sites, two different leading frames, one closer, both ending 002-390-705. That is the independence the log asked for on the 705 side, and it turns up in the metadata, not from one copied object.
- Contrary, once: M-1825 is secondary and icon-only; the Bisht page item is a five-sign lookalike unless it is bridged.
- What it would mean if true: 705 closes the 390 branch in two places, so the closure pole has a second member outside the 817/820 pair.
- Cheapest next move: wait on the two requests (sent). Locally, count 705 closers against 817/820 across the 499 rows (entry 10).

### 20. The H-series three-role codebook, with the 154/156 and 033/034 minimal pairs
- What was seen (log): all 22 objects H-2218 to H-2239 fit a three-side template (+861-003+, +700-03x+, +15x-003+). Hidden-side role family 66 of 66; exact text 64 of 66; side-index majority 47 of 66; global majority 22 of 66. The two exact-text failures are H-2237 side 3 (`+154-003+` against predicted `+156-003+`) and H-2238 side 1 (`+700-033+` against predicted `+700-034+`). Minimal pairs: H-2237/H-2233 (154/156) and H-2238/H-2230 (033/034), group 3, template 700|861|15x, 10 x 6.5 mm (H-2237, H-2233). My pass confirms the rows: H-2237 at 794.1-794.3 and H-2233 at 878.1-878.3 carry these texts. Variant placement: both singletons in group 3 with the same template; exact pair p = 0.025974, adjacent in Fig. 4 p = 0.012987.
- Dimensions (log): 003, 156 and 861 are smaller on the horizontal, area and aspect; the H-series explains them, and after removal no flagged token survives. 034 remains at p = 0.003599, BH q = 0.104371.
- Mayig overlap (log): 154 and 156 both align to P004. Reverse P004 is led by 156 (5 rows), with 154 as runner-up (1 row).
- Where: research/docs/archive/active_decipherment_attempt.md ("H-Series Role Template", "Minimal contrast packet", "Variant localization null", "H-Series Slot Grammar Reconstruction", "154/156 Comparanda", "Variant Crosswalk Pressure"); metadata rows above.
- Old label: the log's top-ranked candidate, "H-series batch/side-role codebook."
- Why it is alive: 66 of 66 hidden side roles are predicted, and the only two exact-text misses are the two minimal pairs the log wanted to test. A workshop batch formula predicts the regularity but not which side carries the subtype bit, so the misses carry information.
- Contrary, once: the singleton variants cluster exactly where a workshop template would put them (the log's own null).
- What it would mean if true: the H-series is a batch record. 861-003 is a batch or class tag, 700-03x is the subtype, 15x-003 is a check side, and 154/156 and 033/034 are real subtype bits.
- Cheapest next move: the side-3 panels of H-2237 and H-2233 sorted blind (requested from Harappa, sent per the log).

### 21. 034 as a distributional subtype of FRAME700, with pottery singles
- What was seen (log): FRAME700 non-H rows: 331; 034 rows: 93. Dimension classifier top-1 0.435045 against frequency 0.410876. 034 recall 0.677419 against a blocked-null 95th percentile of 0.548387; across four blocked-null policies the null never reached the 034 recall (p = 0). Strongest 034 feature: horizontal bin h_10_13, 20 of 93 against 18 of 238, lift 2.843489. Dimensions p = 0.003599 for 034 after the H-series is removed.
- Long-context substitution (log) does not survive correction (token 060 p = 0.0068, BH q 0.077; corrected tests 0).
- My pass: exact `+034+` rows are 11, of which 9 are pottery (POT:T:g: M-1584 at 3807.1, Ns-72 at Nausharo 5373.1, Derawar Ther 5419.1, and six Harappa pots at 334.1, 711.1, 728.2, 990.1, 3938.1, 4134.1) and 2 are TAB:B (879.1, 1269.2).
- Where: research/docs/archive/active_decipherment_attempt.md ("FRAME700 Subtype Discrimination", "FRAME700 Blocked Null", "Prior Research Pressure Check", "Long Context Substitution", "034 Crosswalk Darkness Diagnostic").
- Old label: "distributional residue; object/form-context; not function."
- Why it is alive: 034 is the only FRAME700 class that beats every blocked null on recall. It also appears alone on nine pottery pieces at five sites, which is how a sign used as a count or a mark would appear.
- Contrary, once: long-context substitution gives no corrected survivor, and the dimension signal is form-shaped.
- What it would mean if true: 034 is a standalone mark on pots and a count suffix on tablets, the same sign in two registers.
- Cheapest next move: compare the nine pottery 034 singles with the single 033 and 032 pottery marks (metadata query), side by side.

### 22. The Mayig overlap blind spot, with the clean 032 and 033 maps
- What was seen (log): the Mayig overlap is 179 rows, all Mohenjo-daro SEAL:S. Clean maps: 032 aligns in 21 rows, top P145 in 20; 033 aligns in 9 rows, top P147 in 9; 034 aligns in 0 rows (182 broad rows). Six P0 Mohenjo-daro 034 objects are missing from Mayig (M-2104, M-315, M-1206, M-685, M-1584, M-1963), and the public Mayig repo stops at m184. 390 maps to P086 with support 25; 405 (2), 406 (1) and 407 (1), none accepted.
- Where: research/docs/archive/active_decipherment_attempt.md ("Variant crosswalk pressure", "034 crosswalk darkness diagnostic", "034 Mayig acquisition list"); research/docs/archive/ambiguous_zero_overlap_policy_gate_20260712.md (M-55 and M-60 colocation).
- Old label: "034 is crosswalk-dark; a coverage problem before it is an allograph problem."
- Why it is alive: 032 and 033 already map cleanly, so the sign list works where it has coverage. The 034 gap is coverage, not evidence for or against a split. Filling six objects would settle 034 against 033 fast.
- Contrary, once: 154 and 156 both map to P004, which the log reads as a collapse signal that is "active, not proven."
- What it would mean if true: 034 and 033 are distinct sign-list entries and the local split is real. 154 and 156 might be one sign-list entry in Mayig.
- Cheapest next move: obtain the fuller Mayig/Parpola records for the six P0 numbers (named in the log, not run), or match the 179 rows by M-number against the local 033 and 034 rows.

### 23. The 390, 405, 406, 407 collision on Mayig P086
- What was seen (log): Mayig P086 has provisional edges from local 390 (support 25, medium-low), 405 (2, very low), 406 (1, very low) and 407 (1, very low). None accepted. In 002-405-X, 29 of 32 frames are one Harappa cylindrical formula `+520-240-002-405-501+`. Other 405 frames: M-34 `+740-336-176-002-405-372-374+`, M-41 `+740-636-240-233-235-002-405-125-820+` (405 followed by 125), H-22 `+740-920-320-233-806-002-405-321+`.
- Where: research/docs/archive/campaign_032_002_861_002390x_390405_collision_*_20260531.md.
- Old label: "blocks P086 collapse; no values."
- Why it is alive: four local signs share one Mayig sign, one of them the copper marker 407. An allograph family 390/405/406/407 would tie the branch head 390 to the copper register sign. M-41 shows 125 after 405, so the 125 continuation may not be limited to 390.
- Contrary, once: the 405 edge has two rows, and the 002-405-501 cluster is one repeated formula.
- What it would mean if true: 390, 405, 406 and 407 are one sign in several forms, and the copper register and the 002-390 branch share a graphic unit.
- Cheapest next move: a blind sort of 390 and 405 rows (M-34, M-41, H-22 against M-32 and M-984 as controls) by stroke pattern, using the crops the log already names.

### 24. The 'ra' attractor in the Brahmi shape-descent gates
- What was seen (log, v2 and v3): the nearest Brahmi label 'ra' is modal for several Indus families. 527 order: 6 samples, modal share 1.0, shape null 0.035, label null 0.031, real-token impostor share 0.000000. 061 order: 4 samples, shape null 0.0475, label null 0.02, impostor share 0.008000. 472 reverse: 2 samples, modal share 1.0, label null 1.0, impostor share 0.248; 472 order impostor share 0.530. Corpus: 1,342 Brahmi glyph rows (dated <= -100), 611 Indus source-token crops, 83 sign/orientation families, all blocked.
- Duplicate audit (log): 527 order is 2 token hashes from 1 CISI object; 061 order is the same.
- Where: research/docs/archive/brahmi_shape_descent_gate.md; brahmi_source_token_descent_gate_v2.md; brahmi_independent_source_token_gate_v3.md; brahmi_real_token_*_v3.md; brahmi_real_token_low_null_reaudit_20260531.md. The directory research/data/brahmi/ exists (42 entries); its features CSV was not opened in this pass.
- Old label: "retracted as descendant-script phonetic anchor"; "zero review candidates."
- Why it is alive: two different Indus signs (527 and 061, order) converge on the same Brahmi label, and for 527 almost no real Indus token from another sign reproduces it. The label is a single Brahmi letter, which is a convergence worth testing even on one object.
- Contrary, once: every near-miss is single-object or two-hash, which the v3 gate blocks.
- What it would mean if true: 527, 061 and 472 are allographs of one sign that reads 'ra' in Brahmi, which is the one descent line the log did not remove.
- Cheapest next move: acquire two or three more independent source-token crops of 527 and 061 and rerun the v2 nulls. The log names this as the next valid step.

### 25. Local 220 as the fish sign (Parpola 60) in the 520-220 head
- What was seen (log): Parpola 1994 sign 60 is a plain fish; Mayig P050 is an undecorated fish witness; local 220 to P050 has 27 overlap rows. M-37 `+520-220-415+` shows a fish-like middle component. Source crops N005 (M-37), N006 (H-938 A) and N007 (H-940 A) fall in a broad fish/leaf family; N008 (H-942 A) is too blurred. Strict gate: three reads split; the conservative read is "broad fish/leaf family only; sign-60-only not accepted." My pass: 220 occurs in 360 rows.
- Where: research/docs/archive/active_decipherment_attempt.md ("Parpola sign 60 / local 220 fish bridge check", "Parpola sign 60 / local 220 middle-crop check", "strict Parpola sign 60 / local 220 fish-family gate").
- Old label: "local220_sign60_candidate_strengthened_not_accepted"; "broad fish/leaf-family only."
- Why it is alive: 220 heads the 520-220-415 stem. A fish-headed stem with a comb-like closer is a commodity-plus-count formula, which fits the other readings in this chunk.
- Contrary, once: the broad fish/leaf family includes Parpola 70, which the packets could not separate from 60.
- What it would mean if true: 220 is a fish determinative in the head slot of the 520 stem.
- Cheapest next move: a sign-60-versus-70 sort on the Fig. 5.1 crops against the three source-visible 220 panels (M-37, H-938 A, H-940 A).

### 26. The 520-220 stem depends on object type
- What was seen (log): 520-220 has 67 bigram occurrences, 59 at inscription start; 520 starts 263 rows; P(415 | 220 after 520) = 28/60 = 0.4667 against 63/330 = 0.1909 otherwise, odds ratio 3.71. Harappa odds ratio 9.75; Harappa TAB:I 23.83; Mohenjo-daro 1.21. The broad ^+520-220-X frame has 52 rows, 51 objects and 16 third-slot values. My pass: bigram 520-220 occurs in 58 rows, and 232 rows start with 520 (both wider than the log's counts, so the log's figures are the ones above).
- Where: research/docs/archive/active_decipherment_attempt.md ("520-220 Formula Stem Campaign", "unit-boundary campaign"); research/docs/archive/campaign_520_220_formula_stem.md (named in the log; not on this chunk).
- Old label: "fixed formula stem; X terminal/class/closure slot; 415 default; semantic hypotheses institutional/title or seal-owner."
- Why it is alive: the effect comes almost entirely from Harappa TAB:I (odds ratio 23.83), and the Mohenjo-daro control is near 1. A formula bound to one object class looks like a tablet-issue formula.
- What it would mean if true: 520-220-415 is an issue formula on Harappa TAB:I tablets, and its closer marks the issue class.
- Cheapest next move: the 520-220-415 rows split by object shape (rectangular against cylindrical), metadata only.

### 27. Damaged-slot policy at M-55 and M-60
- What was seen (log, source-checked 2026-07-12): M-55 Lipi `+000-760-463-510-001-692+` with Mayig P000 (10% loss) has six structural slots; the damaged slot is initial and 760 is not. M-60 Lipi `+151-000+` with Mayig P001 P000 (40% loss) has two slots; 151 is not terminal.
- Where: research/docs/archive/ambiguous_zero_overlap_policy_gate_20260712.md.
- Old label: "accepted normalization policy; class closed 2/2."
- Why it is alive: the policy changes length and terminal counts, so any terminal-rate figure in this chunk that counted M-60's 151 as terminal (or M-55's 760 as initial) moves.
- What it would mean if true: nothing new. This is bookkeeping, and it is the reason to recheck entries 15 and 22 on the corrected rows.
- Cheapest next move: rerun the terminal-governor counts (entry 15) with the damaged slots set to non-counting and then to counting, and report both.

### 28. Anchor economics for the 571-sign set
- What was seen (log): the strict collapsed Lipi working set has 571 observed signs. With no accepted anchor, label-symmetry degeneracy is log2(571!) = 4410.970864 bits. Forced rejected stresses remove 9.157347 bits (one neighbour) up to 100.590993 bits (eleven forced signs). Ideal accepted anchors: 10 remove 91.459136 bits; 50 remove 454.678720 bits (residual 3956.292144).
- Where: research/docs/archive/anchored_constraint_collapse_stress.md.
- Old label: "guardrail; no anchored collapse accepted."
- Why it is alive: the log's own note says the curve is slow "unless [anchors] also unlocked strong contextual propagation." Nothing in the chunk runs that propagation.
- What it would mean if true: a modest anchor set, propagated across adjacency, could force most of the 571 labels. The bits figure is the ceiling without that propagation.
- Cheapest next move: a propagation run over the adjacency graph from the eleven rejected-anchor signs (the log's strongest rejected set), counting forced labels per step.

### 29. BM 120573: a cuneiform line on an Indus-style bull seal from Ur
- What was seen (log): British Museum 120573 (registration 1928,1009.56; excavation U.7683; Diqdiqqah, Ur, surface) is a rectangular grey steatite stamp seal, 27 x 24 mm, with a bull design and a cuneiform line. Gadd 1932 no. 1 reads it doubtfully as sak-ku-shi-? (first sign SAG or KA, second KU or LU, third probably SHI). Local Ur rows (3897.1, 3898.1, 3899.1, 5225.1, 5231.1) are circular or unknown; none maps.
- Where: research/docs/archive/bm120573_object_bridge_audit.md.
- Old label: "real object-level cuneiform route; not an accepted external Indus phonetic anchor."
- Why it is alive: it is the only object in the chunk that carries both scripts. The shape mismatch rules out the local Ur rows, not the object, and the object still ties Ur to an Indus-style seal.
- What it would mean if true: an Indus-style seal from Ur carries a cuneiform name, which makes one of its signs a name slot.
- Cheapest next move: check Mitchell 1986 no. 7 fig. 111 and Parpola 1994 p. 131 (both named in the log, not checked), and Aruz and Wallenfels 2003 no. 301b.

### 30. Meluhha in cuneiform and in the Indus string at Ur (3898.1)
- What was seen: local row 3898.1 (Ur, circular, SEAL:C) `+002-004-328-001-803-415+` has six signs. The cuneiform phrase "ur gun3-a me-luh-ha" on a separate Ur text has six syllables. The log's forced map is 002=ur, 004=gun3, 328=a, 001=me, 803=luh, 415=ha. My pass: the triple 001-803-415 occurs in one row only (3898.1). Co-occurrence: 407 with 001, 803 or 415 occurs in 26 rows (SEAL:R, SEAL:S, TAB:B, TAB:C).
- Log's Failaka and Kish candidates, all rejected as length or pattern fits: Kish me-luh-ha (3 forced), Failaka ma2-me-luh-ha (4), lu2-sun2-zi-da (4), szu-i3-li2-su (4).
- Where: research/docs/archive/anchored_constraint_collapse_stress.md; research/docs/archive/bm120573_object_bridge_audit.md; metadata row 3898.1.
- Old label: "rejected same-site onomastic; U17649 is Indus-only; site-matched shuffle control reproduces the strict mapped pattern at share 0.6857."
- Why it is alive: six signs against six syllables is an exact length match, and the three signs that would spell me-luh-ha form a triple that occurs once in the whole metadata. The copper line in entry 2 names the same Meluhha. Both observations point the same way.
- Contrary, once: 0.6857 of site-matched shuffles reproduce the mapped pattern, so the match is not distinctive at the object level.
- What it would mean if true: the Indus string spells Meluhha on Ur, and 407 is the copper marker that the commodity line names.
- Cheapest next move: the blind neighbour count. Take the other rows of the 407 frames (entry 2) and check whether 415, 803 or 001 recur in them (metadata query, 26 rows).

---

## Sources on disk

Read in full (33 paths listed in research/docs/archive/ in sweep/chunks/chunk_00; the chunk lists 33, not the 37 the first pass noted):
- accuracy_framework.md
- active_decipherment_attempt.md
- ambiguous_zero_overlap_policy_gate_20260712.md
- anchored_constraint_collapse_stress.md
- blind_boundary_packet_20260530.md
- blind_boundary_packet_alpha.md
- bm120573_object_bridge_audit.md
- brahmi_independent_source_token_gate_v3.md
- brahmi_real_token_impostor_*_v3.md
- brahmi_real_token_low_null_reaudit_20260531.md
- brahmi_shape_descent_gate.md
- brahmi_source_token_descent_gate_v2.md
- brief_407_rectangular_copper_register_20260531.md
- brief_741060920_terminal_formula_20260531.md
- brief_terminal_governor_network_20260531.md
- brief_terminal_governor_unicity_20260531.md
- campaign_002_y_branch_gap_blind_packet.md
- campaign_002_y_branch_gap_public_source_acquisition.md
- campaign_002_y_partition_source_queue.md
- campaign_032_002_861_002390125_branch_source_route.md
- campaign_032_002_861_002390x_3335_acquisition_packet_20260531.md
- campaign_032_002_861_002390x_3335_identity_neighborhood_audit_20260531.md
- campaign_032_002_861_002390x_3335_private_collection_cluster_*_20260531.md
- campaign_032_002_861_002390x_3335_private_collection_web_scout_20260531.md
- campaign_032_002_861_002390x_3335_source_identity_recheck_20260531.md
- campaign_032_002_861_002390x_3335_yajnadevam_provenance_recheck_20260531.md
- campaign_032_002_861_002390x_3335_yajnadevam_repo_trace_20260531.md
- campaign_032_002_861_002390x_3335_yajnadevam_source_contact_20260531.md
- campaign_032_002_861_002390x_390405_collision_*_20260531.md
- campaign_032_002_861_002390x_390590032_family_recheck_20260531.md
- campaign_032_002_861_002390x_390_context_*_20260531.md
- campaign_032_002_861_002390x_alpha_blind_boundary_read.md
- campaign_032_002_861_002390x_blind_boundary_packet.md

Repo data checked in this pass:
- research/data/open_prototype/lipi/metadata_filtered.csv: 5,679 data rows, 35 columns (id, site, type, shape, dir., text, horizontal(mm), vertical(mm), and others). Every "my pass" count above comes from this file.
- research/data/brahmi/ (exists, 42 entries); research/data/brahmi/indoskript_brahmi_features_v2.csv exists, not opened in this pass.
- research/data/sign_crosswalk/ (24 entries) and research/data/sign_crosswalk/source_panels/ambiguous_zero_overlap_policy/ (exists, not opened).
- research/data/open_prototype/reports/ (2,017 entries) and research/data/meluhha/ (73 entries), named in logs; not opened.

Named in the logs but not present here:
- /home/claude/ivc/tmp and research/tmp (all crop and panel folders cited by the logs).
- docs/effective_unicity_directionality_formula_family_controls.md (entry 9).
- research/docs/archive/campaign_520_220_formula_stem.md is on disk but is not on this chunk; it was not read by this reader.

## Ideas named but never run

Named in the logs, not run:
- Fuller Mayig/Parpola records for the six P0 Mohenjo-daro 034 objects (entry 22).
- Mitchell 1986 no. 7 fig. 111, Parpola 1994 p. 131, Aruz and Wallenfels 2003 no. 301b, for BM 120573 (entry 29).
- Native-resolution stroke count on the Marshall Pl. CXIV no. 532 leaf, IGNCA 48270_0205 (entry 1).
- Read the definition of "stored-win" in the linked directionality document (entry 9).
- Source-token crops of 527 and 061, two or three more independent ones, then rerun the v2 nulls (entry 24).
- Acquire a bare-closure row with terminal space comparable to the 120 px tailed windows (entry 11).

Reader proposals, not named by the logs (marked as proposals):
- Proposal: a Parpola 107 test for 415 on the visual route, comparing the comb-ending of text 7 with the terminal 415 of M-2109 and M-2111 (entry 4).
- Proposal: a stroke-count test on the nine pottery 034 singles, to see whether pot marks carry three strokes (entry 21).
- Proposal: a direction-free component test for 034 and 415 on H-938 B and H-910 B (entry 8).
- Proposal: count 533 and 717 separately across strict rows outside the pair. My pass: 533 in 2 rows, 717 in 41 rows (entry 13).
- Proposal: a sign-60-versus-70 sort on the Fig. 5.1 crops (entry 25).
- Proposal: a propagation run over the adjacency graph from the eleven rejected-anchor signs, counting forced labels per step. The log names the slowdown but does not run it (entry 28).
- Proposal: split the 520-220-415 rows by object shape, and by the slot before 220-415 (entries 3 and 26).
- Proposal: count 705 closers against 817/820 across the 499 rows (entry 19).
- Proposal: rerun the terminal-governor counts with damaged slots counted and not counted (entry 27).
- Proposal: rerun the stored-order metric on the L/R-only and R/L-only subsets separately (entry 9).
- Proposal: the same 002 odds ratio on Harappa-only rows (entry 12).
- Proposal: a leave-site top-3 on TAB:B and TAB:I rows only (entry 15).
