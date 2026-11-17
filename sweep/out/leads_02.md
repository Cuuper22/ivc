# Sweep 02 leads

Reader 02, chunk 02. Read in full: AGENTS.md, TASK.md, and the 29 short notes on the 032-002-861 and 002-390-X lanes. The 380 KB risky parse model (`research/docs/archive/campaign_032_002_861_002390x_risky_parse_model_v1_20260531.md`, 7,291 lines) was read through its opening rules, its verdict tables, the test runs on 125, 530, 705, 000, 3335.1 and 235, the consolidation blocks, and the final expansion and consolidation runs. The rest was scanned for named bets and sources. The quarantined `source_normalized_family_collapse` artifact is marked sealed in the notes and was not opened.

Checked against the data in this pass: the Lipi catalogue `research/data/open_prototype/lipi/metadata_filtered.csv` (5,679 rows). Counts marked "(checked)" below were recounted from that file. The local Bisht 2015 PDF was text-searched as well (see the Dholavira entry).

Plain-word key for the entries:
- Lipi row: one line of the Lipi catalogue. Sign numbers like 002 and 390 are catalogue numbers, not readings. Row IDs like 3335.1 are catalogue IDs.
- Object labels like M-70, H-1993, Sktd-1 are seal IDs used in the notes.
- Frame: the pair 002-390 with the sign after it. The sign after 390 is called the branch.
- Strict: the row can be checked against an inspectable published photograph. Panel-bound: the labelled seal is on a published plate, but sign order is not visible.
- Copy family: near-identical rows that may be one stock phrase copied.
- Prespecified: the rule was written down before the test ran.

---

### 1. The sign after 002-390 splits the frame into closing and continuing branches, tested before the data was looked at
- What was seen: The Lipi file has exactly 15 rows with 002-390 followed by another sign (checked). The prespecified table (continuing: 125, 530, 590; closing: 072, 095, 140, 346, 692, 705, 707) matches all 15 frames. The notes give canonical rows 3503, repeated-branch subset 8/8, source-route-or-strict subset 9/9, strict subset 4/4. Within-frame label shuffle: prespecified-class p = 0.0001998 (a shuffle this clean shows up about 2 times in 10,000); discovery p = 0.0241758. Non-frame terminality shuffle: false-positive rate 0.00003, repeated-branch 0.00089. Those rates mean that when the signs are reshuffled by chance, a pattern this clean almost never shows up. Direction: the branch sign predicts whether the phrase continues.
- Where: `research/docs/archive/campaign_032_002_861_002390x_risky_parse_model_v1_20260531.md` (prespecified branch-table block, around lines 809-850); the 15 frames in `research/data/open_prototype/lipi/metadata_filtered.csv`; report `research/data/open_prototype/reports/risky_002390_canonical_branch_selector_forger_20260531.csv` and its `_frames.csv` and `_by_branch.csv` siblings.
- Old label: Demoted in later consolidation to "frame-conditioned polarity, not a sign value," and 390 demoted to "mixed inventory head." Reasons given: cross-head transfer matched 19 of 26 non-390 frames (described as "mixed"), and the all-head post-hoc adversary ranks 390 first of 9 eligible heads with Bonferroni p 0.2176.
- Why it is alive: The table was written before the test, so 15/15 is not a fit to the data. The 19/26 cross-head figure is 73%, and the 530 branch matched 3/3 of its non-390 rows, so the branch rule has data outside the 390 frame. The all-head number is the main contrary result, and it is answered here: the table never claimed 390 is special. It claims the sign after the frame decides the continuation, and the all-head test does not touch that claim.
- What it would mean if true: 002-390 is a two-way slot. The sign after 390 picks whether the phrase ends or goes on: 125, 530 and 590 must be followed by at least one more sign; 072, 095, 140, 346, 692, 705 and 707 must end it.
- Cheapest next move: Freeze the table and score each source-visible 002-390-X row before its photograph is read. Open predictions already exist for H-1993 (closes on 095), M-1825 and 4237.1 (close on 705), and Sktd-1 (continues on 125). A photo that breaks one of them breaks the table.

### 2. The four source-visible rows inside the frame split two continuing, two closing, in the predicted direction
- What was seen: Four rows in the frame have a strict photograph (checked against Lipi): M-119 (row 2646.1, `151-337-484-002-390-125-632-032-900-563`, continues), M-735 (row 3159.1, `740-760-235-002-390-125-195`, continues), M-70 (row 2598.1, `226-032-002-390-692`, closes), M-71 (row 2599.1, `151-279-142-002-390-095`, closes). Token-boundary adjudication found all four boxed windows compatible with the catalogue order. M-70 and M-71 show that 125 is not required after 002-390.
- Where: `research/docs/archive/campaign_032_002_861_002390x_source_normalized_contrast.md`; `..._token_boundary_adjudication.md`; `..._source_tiered_prev_gate_20260531.md`; the "Strict source-visible microparser" block in the risky model (around line 6847). Crops in `evidence/tmp/002390x_source_normalization/` (M119, M735, M70, M71 signband files).
- Old label: "Survives tiny," with the caveat that 095 has one strict witness and 705 has none.
- Why it is alive: These four rows are every source-visible row inside the frame. The 2:2 split runs the way the table predicts, and the closing pair shows that continuation is not forced by 002-390. The main objection is the sample size. The sample is the whole source-visible set in this frame, so growing it means finding new source rows.
- What it would mean if true: The grammar is visible in photographs, not only in catalogue text. That is the point the copied-formula rival says cannot be shown.
- Cheapest next move: Blind token-boxing of these four windows: boxes drawn from the photograph with the claimed reading hidden. The protocol is already written in the token-boundary readiness note and has not been run.

### 3. 3335.1 is the only other row where a 032-002-390 frame takes something other than 692
- What was seen: Lipi row 3335.1 (unknown site, Bull1:J) reads `740-205-032-002-390-590-032`, the only row with 032 before 002-390 apart from M-70 (`226-032-002-390-692`, checked). The inherited chunk `390-590-032` occurs in 7 rows. Reversed `390-590-032-002` occurs in 3 Lothal rows, which the notes call L-139, L-196 and L-198; the Lipi file has the same string in rows 2081.1, 2116.1 and 2118.2 (checked). Pivot count: 3 of 7 chunks followed by 002, against 0 of 10 for non-390 `590-032`, p = 0.051471. The notes call that borderline. Exact-prefix sibling `740-205-032-002` at M-143 takes `252-840` with no 125.
- Where: `research/docs/archive/campaign_032_002_861_002390x_source_upgrade_impact_audit_20260531.md`; risky model "Twentieth Test Run: 590-032 Bridge Pivot Stress" (around line 1338) and the "3335/H-773 Risk Bets" block (around line 2341); `evidence/tmp/3335_source_identity_recheck_20260531/` and `evidence/tmp/002390x_3335_yajnadevam_*` directories.
- Old label: "Source-blocked; object-ID blocked; private-collection contact pending." The notes also say that if 3335.1 fails, the whole branch model dies.
- Why it is alive: Binding this one row would give the 032 lane a second, strict branch witness, which the notes say the lane lacks. The impact audit calls it the highest single-object unlock because M-70 is already strict. If it binds with the 590-032 tail, it is the only strict row in which a continuing branch is not 125, which tests the table in a new way.
- What it would mean if true: 032 opens a frame where a formula chunk is carried inside the 002-390 slot, rather than being a closing sign.
- Cheapest next move: Search published plate captions and OCR for the exact string `740-205-032-002-390-590-032` and for `3335`. The notes report that CISI XML and the Mayig corpus returned nothing, so the next step is the private-collection contact the notes flag. The Lothal `390-590-032-002` rows are the second route to test the chunk.

### 4. Sktd-1's stray lower-field sign is probably the leading 390 of its own row
- What was seen: Lipi row 3875.1 (Surkotada) is `+390-004-002-390-125-820+`, six signs. The frame used everywhere is `004-002-390-125-820`, five signs (checked). The published plate (CISI India leaf n397, labelled Sktd-1 A and a) shows a top band plus one separate lower-field sign near the left side (A) or right side (a). The notes say the top band is "visually compatible" with the central `002-390-125` window. The strictness audit fails the single-line test because of the wrapped layout.
- Where: `research/docs/archive/campaign_032_002_861_002390x_sktd1_side_pair_recheck_20260531.md` and `..._sktd1_strictness_audit_20260531.md`. Crops: `evidence/tmp/002390x_source_normalization/Sktd1_face_A_signband.jpg`, `Sktd1_impression_a_signband.jpg`, `Sktd1_*_full_panel.jpg`.
- Old label: "Panel-bound pressure, not strict; wrapped layout; the 004 split is blocked."
- Why it is alive: The unexplained stray sign is the only thing the notes cannot place. The row has one more sign than the frame, and that extra sign is the leading 390. If the top band holds the five-sign run `004-002-390-125-820`, the wrap is a placement effect and the lower sign is the first token. Then Sktd-1 becomes a second 004 witness that continues on 125, sitting next to H-1993 (004 then 095, closes). That would be the matched 004 split the notes say is missing.
- What it would mean if true: 004 does not pick the branch by itself. The same left sign 004 gives a closing branch (095) and a continuing branch (125), so the choice is made inside the frame.
- Cheapest next move: Count the glyphs on the top band of the two crops. Five on top supports the placement reading; six on top breaks it. The count takes minutes, not a new source.

### 5. H-1993 has a second catalogue reading the same string
- What was seen: Lipi row 744.2 (Harappa) reads `+740-000-220-004-002-390-095+` (checked). The 2023 Singh et al. supplement lists "ICIT 744 (H-1993)" in the same sign-string neighbourhood, and the notes name the figure as Harappa report H96-2769 Figure 17.07. The supplement download returned 403, so only the web view was read.
- Where: `research/docs/archive/campaign_032_002_861_002390x_source_route_hunt_20260530.md`; `..._source_tiered_prev_gate_20260531.md` (points to a H-1993 acquisition packet, which is not on my list and was not opened). Supplement URL: harappa.com/sites/default/files/pdf/43539_2023_102_MOESM2_ESM.pdf.
- Old label: "Route-only, source-dark for 095."
- Why it is alive: Two catalogues agree on the string. That agreement is evidence about the transcription, not about the photograph, but it is a second independent record of the only 004 row that closes on 095. The notes also guard ICIT 4348 as a different object, so the agreement is not an artefact of a mix-up.
- What it would mean if true: The 004-split pair (H-1993 closes, Sktd-1 continues) is two catalogues deep, which is enough to build the next step on.
- Cheapest next move: Pull the text layer of the supplement PDF (web view) for "H96-2769" and "17.07" and look for the figure caption. The image of Figure 17.07 is the other route.

### 6. The 220-032 split after 861: five photographed rows show closure and tails on the same preframe, and the longest line closes
- What was seen: Seven Lipi rows start 220-032-002-861 (checked): 62.1 (Chanhu-daro), 1434.1 (Harappa), 2313.1, 2618.1 (M-91), 2763.1 (M-240), 3147.1, 3421.1. Five have photographs: bare closure at H-444, M-723 and M-1044; tailed at M-91 (`255-416`) and M-240 (`603`). Measured lines: bare 700, 925, 600 px; tailed 450 px (M-91) and 420 px (M-240). Bare post-861 margins 28, 38, 38 px; tailed rows touch the edge (0 px gap). Tail windows 195 px and 120 px.
- Where: `research/docs/archive/campaign_032_002_861_220032_source_visible_contrast_packet.md`; `..._register_length_*_test.md`; `..._terminal_space_recut.md`. Crops: `evidence/tmp/032_002_861_220032_source_visible_contrast_packet/` and `evidence/tmp/032_002_861_220032_terminal_space_recut/`.
- Old label: "Terminal-space adversary survives; grammar promotion blocked." The adversary says bare rows had no room for a tail-sized slot.
- Why it is alive: The room story has the wrong sign for the longest line. The longest measured line, M-723 at 925 px, is bare, and the two tailed lines are the two shortest (420 and 450 px). Room is therefore not what decides the outcome in this sample. The split also survived the broad-register and total-length tests in the break test.
- What it would mean if true: After the same stem, 861 can end the phrase or take an optional tail. That is a choice made in the phrase, which is what a grammar slot is.
- Cheapest next move: Photograph-check the five unphotographed rows with this prefix (62.1, 1434.1, 2313.1, 3147.1, 3421.1). Each one adds to either the bare side or the tail side, and the terminal-space measurement runs the same way on each.

### 7. H-55 and M-1750 share the stem `390-004-002-861` and differ only in 125
- What was seen: Harappa row 1114.1 (H-55) is `+390-004-002-861-125+` (checked). Its CISI India leaf n217 (printed p. 182) shows a same-line five-glyph band. Mohenjo-daro row 2450.1 (M-1750) is `+390-004-002-861+` (checked) and is source-dark. Direct searches in the CISI Pakistan XML failed; the notes say the plate sequence reaches M-1657 and M-1658 before M-1750 appears "later."
- Where: `research/docs/archive/campaign_032_002_861_390004_exact_prefix_source_gate.md`; `..._branch_125_ecology.md`; crops in `evidence/tmp/032_002_861_390004_exact_prefix_source_gate/`.
- Old label: "Exact-prefix alternation acquisition-gated; not promoted."
- Why it is alive: This is a same-stem pair: identical four signs, and one row adds 125 at the end. Among the 59 occurrences of 125 in the file, only 1 is directly after 002-861 (H-55), and 17 are terminal. The only photographed side is H-55, so the bare side is the missing half, and it is one page search away.
- What it would mean if true: 861 takes an optional 125 addendum that is decided after the stem, not by the stem.
- Cheapest next move: Page through the CISI Pakistan volume from the M-1658 plate forward until the M-1750 label appears. The notes list the search as failed by string match, so this is a page search, not a string search.

### 8. The two-sign ending 533-717 appears in exactly two rows of the whole Lipi file
- What was seen: The token 533 occurs in exactly two Lipi rows (checked): 2872.1 (M-376, `740-100-176-002-861-533-717`) and 2887.1 (M-391, `405-845-686-740-793-003-233-805-002-861-533-717`). Both are Mohenjo-daro SEAL:R with no icon. The token 717 occurs in 55 rows (checked). Among 002-861 rows: 533-717 in 2 of 3 cuboid-convex no-icon SEAL:R rows and 0 of 71 Mohenjo-daro SEAL:S rows. The two pair rows come from different leaves (CISI India n129, p. 94; n131, p. 96), with different excavation IDs (HR 1574426; DK-i 60) and lengths (7; 12).
- Where: `research/docs/archive/campaign_032_002_861_533717_register_test.md`; `..._source_family_independence.md`; `..._source_layout_discriminator.md`; `..._component_ecology.md`; crops in `evidence/tmp/032_002_861_533717_source_family_independence/` and `..._blind_layout_gate/`.
- Old label: "One narrow register/family cell; semantics unproven; rare addendum."
- Why it is alive: 533 never appears outside this pair, so it cannot be a free-standing sign that picks up 717 by chance. The two rows differ on excavation ID, length and leaf, which is what the notes asked for before counting them as two witnesses. The family-cell rival needs a shared source, and the notes already found different leaves for the two.
- What it would mean if true: 533-717 is a frozen two-sign terminal unit, a formula ending that is restricted to one seal register. The unit is a whole, not two readable signs.
- Cheapest next move: Source-route the two source-pending 002-861 controls, M-1954 and M-1973, and check whether their post-861 zone is empty. Those are the only missing comparison rows in the register.

### 9. The 603 bridge was closed by testing the number, not the window glyph
- What was seen: Mohenjo-daro post-861 rows M-240, M-714 and M-1273 end on a rectangular ladder/window glyph. The Harappa five-unit formula `740-603-240-060-692` (H-1138, H-1846) places 603 at unit 2 forward or unit 4 reversed; neither is the window. H-1846 has a window-like form at one edge, which maps to 740 forward or 692 reversed. Across the file, 603 occurs 7 times in 5 registers (per the external-ecology note's table), 3 of them as a post-861 tail. The sister signs 636 (15 occurrences) and 642 (7) never appear at a post-861 tail.
- Where: `research/docs/archive/campaign_032_002_861_603_cross_context_graphic_closure_20260712.md` (the closure); `..._603_636_642_external_ecology.md`; overlays in `evidence/tmp/032_002_861_603_slot_source_normalization/`, `evidence/tmp/032_002_861_603_h1138_h360_tokenization_gate/`, `evidence/tmp/032_002_861_source_token_attachment/`.
- Old label: "Closed: cross-context 603 identity not source-supported."
- Why it is alive: The closure checked whether the Lipi number matched, not whether one glyph carries one number across the Harappa rows. If the window glyph sits under 740 or 692 in Harappa and under 603 at Mohenjo-daro, the inconsistency is in the catalogue numbering, and the glyph is the stable unit. That would reopen one mobile unit linking the two constructions.
- What it would mean if true: One window-shaped unit appears at the end of Mohenjo-daro lines and inside a Harappa tablet formula, and the catalogue split it.
- Cheapest next move: From the existing overlays, tabulate every Harappa formula row with a window-shaped unit and the Lipi number at that position. The same table run on the 636 and 642 rows (the external-ecology note's own next test, extending X-before-240 to all X values) is the other half.

### 10. 705 closes two frames under different predecessors (031 and 388), and the file holds one row where 705 continues
- What was seen: 705 closes M-1825 (Lipi 3992.1, Mohenjo-daro, `157-031-002-390-705`, checked) and Dholavira 4237.1 (`151-032-388-002-390-705`, checked). M-1825 is source-dark. Dholavira 4237.1 has a visual match in Bisht 2015 page 18, item 10 (tree-like 390, short-stroke 002, branch sign, short-stroke sign, final sign). The notes also give a dimension cluster 27.62 x 21.31 x 7.11 to 11.17 mm for ZA-12:2 from a public OCR copy. Counterexample in the file: Tell Umma row 3884.1 reads `390-004-002-705-127` (checked), so 705 is followed by 127. Mohenjo-daro also has 705 in the middle of a 14-fold repeated text (`407-321-407-845-033-705-235`, checked).
- Where: `research/docs/archive/campaign_032_002_861_002390x_source_route_hunt_20260530.md`; risky model "Nineteenth Test Run: 705 Remote Selector Stress" (around line 1281) and the "Sixteenth" and "Expand 4237 source-contact" blocks (around line 4998); PDF at `evidence/tmp/source_route_hunt_20260530/Dholavira-Bisht2015.pdf`.
- Old label: "Candidate form if bound; 705 remote/transfer semantics wild."
- Why it is alive: Two different predecessors, two sites, both close, so the closing behaviour does not come from one left context. The Lothal formula `090-740-220-055-001-741-500-705` (11 rows, checked) also ends on 705. The Tell Umma row is the one place the closure rule can be broken directly.
- What it would mean if true: 705 is a closing class-label that also closes copied formulas. If Tell Umma is right, the closure is not a rule.
- Cheapest next move: Pull the seal-catalogue pages of the PDF. A text check on the local PDF found none of 27.62, 21.31, 7.11, ZA-12 or 8758. About 20 of the 115 pages have almost no text layer, so the seal table is probably image-only. OCR those pages to bind 4237.1 to the locus and dimensions. Separately, route the Tell Umma row.

### 11. The 002-390 frame and the 390-590-032 chunk appear at Gulf and Mesopotamian sites in the file
- What was seen: Tell Umma 3884.1 (`390-004-002-705-127`, Bull1). Kish 1971.1 (`740-390-590-220-003-060-840-416`, Bull1:L) contains the 390-590 pair. Ur, Susa, Failaka and Kish rows also appear (checked). Lothal holds about 208 rows, including the three `390-590-032-002` rows listed in entry 3, and 10 Lothal rows of one text `740-048-002-817` marked as the Elep object type. The notes call Lothal "tags" and treat Tell Umma as needing a source route.
- Where: Lipi rows 3884.1, 1971.1, 3881.1, 3882.1, 3897.1 to 3899.1, 147.1, 148.1; Lothal rows 2081.1, 2116.1, 2118.2, 2093.1 to 2102.1.
- Old label: "Mixed register; Lothal tags wild; Tell Umma needs source-grade route."
- Why it is alive: If the site labels hold, a 002-390 frame and a 390-590 chunk moved with objects into Mesopotamia and the Gulf. That is a physical-world link the decipherment can check against the trade record. The copy rival has the most support hereest at Lothal, where one text repeats 10 times on the same object type, so this has to be separated from copies.
- What it would mean if true: The branch frame is a port or trade formula, carried outside the Indus heartland.
- Cheapest next move: Take the excavation IDs for 3884.1 and 1971.1 from the Lipi file and look each up in a published catalogue. A site label that does not survive that lookup drops the link.

### 12. 235 before a P086 head selects 125 in every row tested, and one file row has a continuous band
- What was seen: Final 235 before 002 with a P086-family head (390 or 405) takes 125 in 3 of 3 rows (M-38, M-735 under 390; M-41 under 405). The closing heads avoid 125 (1 of 1). M-41's signband is continuous and compatible with `...235-002-405-125-820` (source check in `evidence/tmp/002390x_390405_m34_m41_source_check_20260531/M41_A_signband_x2.jpg`).
- Where: risky model "Fourteenth Test Run: 235 + P086 Selector Stress" (around line 1004) and "Thirty-Fifth: Parser Forecast Scope Test" (around line 2049).
- Old label: "Candidate from aggregate contrast; exact-left shadows sparse."
- Why it is alive: This is the only left-context rule that predicted every row it was given, and M-41 gives a third row with a continuous photograph. The sparse-shadow objection is about exact-left minimal pairs, which the notes say do not exist yet for 235.
- What it would mean if true: 235 is a switch placed to the left of 002 that brings in 125 after a 390-class head.
- Cheapest next move: Token-box M-41's band with the same procedure as M-119. Then search the 235-002 rows with non-P086 heads: any row with 125 under a closing head breaks the rule.

### 13. 530 is a one-complement linker across four heads and four sites
- What was seen: Four governed rows 002-H-530-Y: C-57 (`002-296-530-000`), H-773 (Lipi 1665.1, `002-390-530-741`, checked), M-623 (`002-299-530-820`), 4182.1 (`002-705-530-904`). Each has exactly one sign after 530. Heads 296, 299, 390, 705. Sites Chanhu-daro, Harappa, Mohenjo-daro, Dholavira. The forger rates: one-complement-only false-positive 0.0043; full-shape 0.00031. Outside 390, 530 continues in 3 of 3 rows.
- Where: risky model "Twenty-Fifth" and "Twenty-Sixth" test runs (around lines 1599-1700).
- Old label: "Governed one-complement candidate; closure semantics demoted; global 530 chain sign damaged (13 of 18 occurrences continue; 9 of 18 have one complement)."
- Why it is alive: Of the branch signs, 530 is the only one whose one-complement shape holds across four heads and four sites. The forger rates say a shared penultimate position does not explain it. The contrary number, once: 590 also passes the count-window test, so the test does not single out 530 alone.
- What it would mean if true: 530 is a linker: head H linked to one complement Y. It is not a value.
- Cheapest next move: Photograph-check C-57, M-623 and 4182.1. The notes name a fifth governed 530 row with exactly one complement as the promotion test.

### 14. X=000 closes 24 of 27 rows, and each exception is a separate open source question
- What was seen: 27 rows have 000 directly after 002-H. 24 close after 000. Exceptions: M-451 (`520-000-000-000-906-388`), where the tail 906-388 appears in 3 rows, all terminal; Ns-66 (`892-000-002`), a reset; Rakhigarhi 4148.1 (`740-690-435-255-002-267-000-033`, checked), metadata only.
- Where: risky model "Sixteenth" and "EXPAND phase 16:17" blocks (around line 5204); "CONSOLIDATE 16:45, 4148.1 source gate" (around line 5635); "16:49, M-451 / Ns-66 gates" (around line 5686). The M-451 source is a Parpola/SAA 2001 PDF showing the Indus side as a single line, per the notes.
- Old label: "Candidate with serious M-451 damage; not promoted."
- Why it is alive: The M-451 damage claim assumes 906-388 is governed content. The file says 906-388 is terminal in all 3 of its rows, which is what boundary material would look like. If the photograph shows a boundary there, the damage claim goes away. The 4148.1 row cannot be checked from metadata alone, so it is not a counterexample yet.
- What it would mean if true: 000 is the zero-complement sign: the frame ends on a zero, and 002 can start a new frame after it.
- Cheapest next move: Close-read Parpola's Figure 1 for M-451 and see whether 906-388 sits after a boundary. Then check the three rows where 906-388 is terminal.

### 15. When the site is held out, the sign after 002 predicts open or closed better than the visual context does
- What was seen: Leave-one-site-out, predicting open or closed: X identity 72/85 (0.847); head identity 40/53 (0.755); visual-context proxy 61/90 (0.678).
- Where: risky model, "EXPAND phase 18:08: leave-site transfer test" (around line 7244).
- Old label: "Ranked first among transferable signals; the 390 head alone is damaged."
- Why it is alive: The copied-formula rival says visual context should beat the sign identity when a site is held out. It lost on this proxy. The proxy is crude, so the test is weak in one direction only; it does not settle the question, but it does point the other way.
- What it would mean if true: The sign in the branch slot carries the polarity across sites where the copied image does not travel.
- Cheapest next move: Re-run the same held-out test with strict rows only and a shuffled-label baseline.

### 16. 632-032 closes a phrase even without 125 before it
- What was seen: 632-032 occurs in 7 chunks; 5 of 7 end the row. The 3 chunks without 125 before them all end the row, after predecessors 368, 504 and 892. The after-125 chunks end 2 of 4 times. The exceptions are M-119 (`900-563` continues, singleton) and M-1188, a damaged row.
- Where: risky model "Consolidate 14:30" block (around line 3207) and "Forty-Eighth: 632-032 Slot Discipline" (around line 2878).
- Old label: "Candidate terminal compound; title wording demoted."
- Why it is alive: If the 3 non-125 chunks are independent, the closing compound does not depend on 125. That is the claim the title wording gave up.
- What it would mean if true: 632-032 is a reusable closing phrase that 125 can carry, not a rank tail.
- Cheapest next move: Photograph-check the three non-125 rows (predecessors 368, 504, 892) and the M-1188 row.

### 17. The 820 versus 861 icon split was checked on the top symbol only
- What was seen: Top symbols: 861 Bull1:W (5 rows), 820 Bull1:W (4 rows), 817 mixed (Bull1:3, None, Bull1:W/I), 390 two rows (Bull1:T, Bull1:J). The scout looked at these top symbols only.
- Where: risky model "Forty-Fourth: Icon-Class Bridge Scout" (around line 2670). Lipi `symbol` column in `metadata_filtered.csv`. Icon catalogue at `evidence/tmp/m1206_bhaskar/S1-IndusZoomorphicIconCatalogue.txt`.
- Old label: "Wild; emblem bridge not supported by top-symbol overlap."
- Why it is alive: The notes' own revival condition is a separation of 820 and 861 by icon after site and type are controlled. That has not been run across the whole table, where the symbol column is filled for every row.
- What it would mean if true: 820 and 861 are classifier heads for animal or cult classes, not only closers.
- Cheapest next move: Cross-tab symbol by head by site for every row with 817, 820 or 861 as head.

### 18. The 002-390 frame has 15 distinct texts, while the 002-405 and Lothal formulas repeat
- What was seen: All 15 frames are different full texts (checked). The most repeated texts in the file are `400-740-176` (39 rows), `520-240-002-405-501` (29 rows, the copied tablet formula the notes call 002-405), `740-752-615-503` (29, Mohenjo-daro), `090-740-220-055-001-741-500-705` (11, Lothal), `740-048-002-817` (11, 10 Lothal Elep objects).
- Where: `research/data/open_prototype/lipi/metadata_filtered.csv`; `research/docs/archive/campaign_032_002_861_002390x_risky_parse_model_v1_20260531.md` (the 405 comparison, around line 102).
- Old label: Used as the copied-formula rival.
- Why it is alive: This is the best case for grammar over copying: the frame is not repeated, so the branch behaviour is not one pasted formula. The copies are real, but they sit in the 405 and Lothal formulas, not in the 15 frames.
- What it would mean if true: The frame is a productive construction, and the repeated formulas are a separate, copying-based process.
- Cheapest next move: Look at the 002-390 rows' left parts (the signs before 002) for copies that might sit under different full texts.

### 19. Summary of rows that would move the most
- Entries 3, 4 and 7 each name one object whose photograph or page would add a source-visible branch witness to a lane the notes call blocked: 3335.1 (032 lane), Sktd-1's placement (second 004 witness), and M-1750 (bare side of the exact-prefix 861 pair).

---

## Sources on disk

- `research/data/open_prototype/lipi/metadata_filtered.csv` — Lipi catalogue, 5,679 rows; columns include id, cisi, site, symbol, type, text. Every frame count in this file was recounted from it.
- `research/data/open_prototype/reports/` — campaign outputs (CSV and JSON), about 2,017 entries, named throughout the notes.
- `research/data/open_prototype/tools/` — 342 entries (runner scripts and helpers) named in the notes.
- `research/docs/archive/` — the 30 notes on this chunk, plus the risky parse model.
- `evidence/tmp/002390x_source_normalization/` — CISI India leaf n397 (Sktd-1), n066 (M-70, M-71), n076 (M-119); CISI Pakistan n086 (M-735) crops and full pages.
- `evidence/tmp/002390x_intrinsic_sign_behavior_recheck/` — H-660 full page, CISI Pakistan leaf n343.
- `evidence/tmp/002390x_390405_m34_m41_source_check_20260531/` — M-41 signband.
- `evidence/tmp/source_route_hunt_20260530/Dholavira-Bisht2015.pdf` — Bisht 2015 Dholavira excavation report, 115 pages; text layer lacks the 4237.1 dimensions; about 20 of 115 pages have almost no text. Plus `Dholavira-Bisht2015.txt` (excerpt) and page-18 crops.
- `evidence/tmp/032_002_861_390004_exact_prefix_source_gate/` — H-55 contact sheet, CISI India leaf n217.
- `evidence/tmp/032_002_861_220032_source_visible_contrast_packet/`, `..._220032_terminal_space_recut/` — 220-032 blind sheet, comparison sheet.
- `evidence/tmp/032_002_861_533717_*` — register controls, source family independence, blind layout gate.
- `evidence/tmp/032_002_861_603_*` — overlays for M-240, M-714, M-1273; H-1138 (Vats Plate XCIV); H-1846 (H95-2672 Figure 11.11).
- `evidence/tmp/m1206_bhaskar/S1-IndusZoomorphicIconCatalogue.txt` — icon catalogue (lists M-1825 as an F2 unicorn object).
- `evidence/tmp/cisi_pakistan_pages/`, `cisi_pakistan_ocr/`, `cisi_xml/` — CISI volume pages, OCR and XML used for source-binding searches.
- `evidence/tmp/3335_source_identity_recheck_20260531/`, `evidence/tmp/002390x_3335_yajnadevam_*` — 3335.1 identity checks (not opened in this pass).
- Public, web only: Singh et al. 2023 supplement, harappa.com/sites/default/files/pdf/43539_2023_102_MOESM2_ESM.pdf (download returned 403; web view only).
- Public, named in the notes and not checked here: Parpola/SAA 2001 PDF (M-451 Figure 1); a pdfcoffee OCR copy of Bisht 2015 (source of the 4237.1 dimension cluster); the Mayig public-git P-numbered corpus (second corpus for M-70 and the P122/P086 collision guard).

## Ideas named but never run

1. Blind token-boxing of M-119, M-735, M-70 and M-71, with a family/source-register null that does not treat terminal continuation as free evidence (readiness and adjudication notes).
2. Token-box M-41's continuous band with the M-119 procedure (risky model, 125-820 section).
3. Route the 390-004-002-Y controls M-103, M-1844, M-1823, Sktd-1, H-2003, Dholavira 951.1 and Tell Umma 3884.1 to source-grade object routes (exact-prefix note, next batch).
4. Acquire M-1750, or find an equivalent non-public bare control. Page the CISI Pakistan sequence forward from M-1658 for the label (suggested in entry 7).
5. Recut terminal space for H-444, M-723 and M-1044 with the same metric as M-91 and M-240, and measure M-1750 once it is acquired (220-032 recut and exact-prefix notes).
6. Source-route M-1954 and M-1973, the two pending 002-861 controls for 533-717 (register-controls note).
7. Post-861 spacing features for 533-717: distance from 861 to the physical edge, terminal cluster separation, A/a agreement (source-family independence note's next test).
8. A third independent source-visible 533-717 row, which the notes name as the promotion condition.
9. Extend X-before-240 from 603, 636 and 642 to all X values, and ask whether post-861 bridge behaviour concentrates in one class (603 external ecology note's next test).
10. Source-bind the repeated 002-390-705 through M-1825 or Dholavira 4237.1, or a replacement row (source-route and branch-table notes).
11. Bind Dholavira 4237.1 to ZA-12:2 by a caption or seal-table bridge (the notes name the 8758 locus bridge). Suggested here: OCR the image-only seal-table pages of the local Bisht PDF.
12. H96-2769 Figure 17.07 image for H-1993 (H-1993 acquisition packet).
13. Private-collection contact for 3335.1 (notes flag it as pending).
14. Close-read Parpola's Figure 1 for M-451 and test 906-388 as terminal boundary material outside M-451; post-000 frame-reset control (EXPAND/CONSOLIDATE 16:49 block).
15. Hunt a source-bound in-frame exception: 125 terminal after 002-390, or continuing 095, 692 or 705 after 002-390 (intrinsic-behaviour note's next gate).
16. Repeat left-bigram groups (220-004, 390-004, 226-032, 205-032) across all governed rows, not only 002-390 (compound-left router, "next breaking work" list).
17. Icon-class cross-tab for 817, 820 and 861 across all rows, controlling for site and type (icon-class scout's revival condition).
18. Leave-one-site-out transfer with strict rows only, plus a shuffled-label baseline (leave-site test's frontier).
19. Photograph-check the three governed 530 rows C-57, M-623 and 4182.1 for one-complement shape, and find a fifth row (530 falsifier).
20. Source-route Tell Umma 3884.1 and Kish 1971.1 to published catalogue entries; route the three Lothal `390-590-032-002` rows to image binding (entry 11; the notes named Tell Umma only).
21. Build a source-visible crosswalk from CISI rows that carry both a Lipi number and a Mayig P-number, to replace the unaccepted provisional edges (Mayig crosswalk note). The notes give no plan for this; it is suggested here.
22. Photograph-check the three non-125 632-032 rows (predecessors 368, 504, 892) and the M-1188 row (entry 16).
23. Count the glyphs on the top band of Sktd-1's two crops to test the placement reading (entry 4). Named nowhere; suggested here.
