# Leads, sweep 10

Read in full: all 37 files on the reading list (chunk_10), including the 1,825-line `research/docs/archive/open_prototype_results.md`. Paths below are relative to `/home/claude/ivc` unless shown absolute.

Re-tallies run by this sweep (read-only, no repo file edited; scripts in `/tmp/sweep10/`, outside the repo):
- `research/data/open_prototype/reports/lipi_scope_rows.csv` (5,679 rows; 2,883 numeric-clean; 1,798 distinct clean texts)
- `research/data/open_prototype/reports/overlap_probe.csv` (179 Lipi-Mayig overlap rows; 150 count-matched)
- `research/data/open_prototype/mayig/records_index.csv` (179 Mayig side records)
- Mayig feature files: `evidence/tmp/mayig_feature_namespace_probe/repo/indus-valley-script-corpus-ad2f1e218a34b8c33c57de0d6cb8d99272765bbb/features/` (397 JSON; each has `wells_graphemes` and a description)

Verification note: the path and the counts on the Lipi-to-Wells identity, the stroke table, the 817/861 and 900/920 splits, and the 002 governor were re-tallied in this run. A few figures (the 31.37 enrichment for 034, the 740 initial/final counts, the 615/617 row counts, the 331-of-397 Wells count, the 101/100 row counts, and the exact per-token row counts for 001 to 036) were taken from the notes or from earlier passes and have not been re-tallied; check them before relying on them.

Terms used here: Lipi = the numeric sign catalogue (codes like 740); Mayig = the P-code catalogue (codes like P324); Wells = the W-numbers that Mayig's feature files attach to its P-codes; CISI = Corpus of Indus Seals and Inscriptions; "token" = one catalogue code.

---

### Lipi numeric codes are the Wells numbers Mayig records, and Mayig's stroke codes spell out a numeral series
- What was seen: Mayig's feature files list a Wells number for 331 of its 397 codes. In the 784 count-matched aligned positions whose Mayig code has a Wells number, the Lipi token equals one of that code's Wells numbers at 692 positions (88.3%). Shuffling the Mayig codes within each row (2,000 iterations) gives a mean of 136.4 matches and a maximum of 178. Top pairs: P324→740 (73), P122→002 (57), P050→220 (27), P086→390 (25), P145→032 (20), P120→060 (17), P217→520 (15), P062→240 (14), P378→820 (14), P060→235 (13), P058→233 (13), P385→861 (12), P385→817 (12), P202→368 (10), P123→003 (10), P147→033 (10). The stroke codes read straight from their descriptions: P121 = W001 (one half-height stroke), P122 = W002 (two), P123 = W003 (three), P124 = W004/W014 (four), P125 = W005/W015 (five), P126 = W006/W016 (six), P127 = W007/W017 (seven), P128 = W018 (eight); P144 = W031 (one full-height), P145 = W032 (two), P147 = W033 (three), P150 = W034 (four), P151 = W035 (five). Lipi 001 aligns to P121 at 7 positions, 004 to P124 at 4, 005 to P125 at 2, 017 to P127 at 2, 035 to P151 at 1. Full counts from the Lipi file: 001 = 210 rows, 002 = 824, 003 = 253, 004 = 97, 005 = 49, 006 = 7, 007 = 5, 031 = 250, 032 = 568, 033 = 486, 034 = 164, 035 = 25, 036 = 6.
- Where: `research/data/open_prototype/reports/overlap_probe.csv`, `research/data/open_prototype/reports/lipi_scope_rows.csv`, the Mayig feature JSONs named above (P121–P151 and P324, P122, P123, P145, P147, P378, P385, P217, P050, P154, P009, P010, P127, P125, P151, P268, P092, P230, P234, P041, P058, P363, P037 read directly).
- Old label: "sign_system_unmapped" on every overlap row (`overlap_probe`); "numeric labels are not portable across systems" (`research/docs/archive/p041_mayig_parpola41_crosswalk_falsification_gate.md`, which ruled out Parpola sign no. 41 = Mayig P041 by number). Reason: Parpola, Lipi and Mayig each number signs, so equal numbers were treated as coincidence.
- Why it is alive: the test that killed the P041 shortcut compares Parpola numbers, which Lipi never used. The Lipi-to-Wells identity is a different comparison and it holds at 692 of 784 positions against shuffles that reach at most 178. It agrees with the P041 gate's own single overlap pair (Mayig P041 maps to W112 and sits on Lipi 112 in M-33). Contrary numbers, once: 92 of 784 positions disagree, the largest being P230 against 798 (6) and P154 against 920 (4). Mayig might have built its Wells column from Lipi, which would make the match circular; the 92 disagreements argue against a forced copy but do not settle provenance.
- What it would mean if true: the Lipi tokens are a Wells-numbered list, so every Lipi token carries a Wells description. The 1–8 short-stroke series and the 1–5 full-height series are then a counting system written with strokes, and it is the first category in the corpus that carries a meaning we can read off the catalogue without any sound value.
- Cheapest next move: list the Mayig provenance of the `wells_graphemes` field. Then tabulate every Lipi token in the 2,883 clean rows against its Wells description, starting with 031 (expected: one full-height stroke, P144), 006 (six short, P126), 036 (six full-height, unlisted in Wells), 034 (four full-height, P150).

### 034 is four full-height strokes (Mayig P150, Wells W034), not an unidentified short mark
- What was seen: Mayig P150 reads "Four adjacent full-height vertical strokes" and carries Wells W034. P150 appears in 0 of the 179 Mayig side records (`records_index.csv`) and in 0 of the 179 overlap rows, so no Lipi 034 position can align to it. Lipi 034 has 164 token rows, 123 in the clean layer, and only 11 distinct clean texts. It is the most enriched short mark in the multi-side queue (enrichment 31.37 in `research/docs/archive/open_prototype_results.md`, short-mark section). Its two-token companions: 700-034 (109 rows with 700 first, 14 with 700 last).
- Where: `research/data/open_prototype/reports/crosswalk_high_frequency_sample.csv` and `research/docs/archive/lipi_034_crosswalk_darkness_diagnostic.md` (named in `research/docs/archive/lipi_variant_crosswalk_pressure.md`, not on the reading list; I did not open it), Mayig feature `P150.json`, `research/data/open_prototype/lipi/metadata_filtered.csv`.
- Old label: "crosswalk-dark"; "034 is absent upstream of candidate generation... needs more coverage or authoritative sign-list mapping" (`lipi_variant_crosswalk_pressure.md`). Reason: no overlap row carries 034.
- Why it is alive: the authoritative sign-list mapping already exists in Mayig's own feature record (P150 to W034, described as four full-height strokes). The darkness is a scope fact: the 179 Mayig records are all Mohenjo-daro unicorn seals (`research/data/open_prototype/reports/metadata_scope_probe.md` and `research/docs/archive/metadata_scope_probe.md`), and the 034 tokens sit on Harappa tablets. Contrary number, once: the 164 rows overstate the sign, because 21 of the H-series side texts are identical copies of +700-034+.
- What it would mean if true: the 033/034 contrast is a contrast of three full-height strokes against four. Every branch the old agents parked under "034 unknown" becomes a counting question that a plate can answer by stroke count.
- Cheapest next move: count strokes on the 034-bearing side of the 22 H-series tablets (H-2218 to H-2239, figure 4 of the Meadow–Kenoyer publication) and on any Harappa tablet plate in the CISI set that is already in `research/data/sign_crosswalk/source_panels/`.

### Short side labels are a frame sign 700 plus a count of tall strokes, and +700-033+ is the most repeated text in the clean layer
- What was seen: two-token rows with 700 and a tall numeral: 700 first with 033 (125 rows), 034 (109), 032 (89); 700 last with 033 (32), 032 (18), 034 (14). So 700 comes first in 323 of 387 such rows. The most repeated numeric text in the clean layer is +700-033+, at 117 rows (TAB:I 60, TAB:B 53, SEAL:R 2, SEAL:CY 1, POT:T:g 1; all Harappa). The full Lipi file has 1,351 exact duplicate rows in the clean layer, and the top 117-row text accounts for 9% of the clean rows.
- Where: `research/data/open_prototype/reports/lipi_scope_rows.csv`; `research/data/open_prototype/reports/lipi_short_mark_context_orientation_rows.csv` and `..._context_orientation_summary.json` (plus `lipi_short_mark_orientation_rows.csv` and `lipi_short_mark_orientation_companions.csv`); `research/docs/archive/open_prototype_results.md` (short-mark and dedup sections).
- Old label: "exact duplicate rows inflate within-split scores" (dedup baseline); "700 companion marks are 700-first overall; reversed forms are type-conditioned" (orientation audit). Reason: duplicates were treated as memorization to remove.
- Why it is alive: a tablet label copied onto many tablets is a physical fact, not a statistical artifact. Taking the duplicates out removes the tablet-side formula the catalogue records most often. Reversed orders (700 last, 55 to 64 rows depending on the count) are the minority the orientation audit flagged; those may be mirror impressions.
- What it would mean if true: the short side of a Harappa tablet is a fixed frame, 700, plus a tall-stroke count from 1 to 4 (031 to 034), and the frame-plus-count pattern is the label the scribes stamped across dozens of tablets.
- Cheapest next move: check a sample of the 117 +700-033+ rows against the source plates (CISI or HARP) to see whether they are separate physical tablets or repeated catalogue entries for one tablet.

### H-2218 to H-2239: one three-side template in all 22 rows, with the same count-role on each side
- What was seen: all 22 rows fit one +861-003+ side, one +700-03x+ side, and one +15x-003+ side. Side 3 is always the +15x-003+ role (22 of 22). The role 700-03x carries +700-034+ in 21 rows and +700-033+ in 1 (H-2238). The role 15x-003 carries +156-003+ in 21 and +154-003+ in 1 (H-2237). The row-wise role permutation gives p = 3.19e-11 (`research/docs/archive/open_prototype_results.md`, side-role template section; file `research/data/open_prototype/reports/lipi_h2218_h2239_side_role_summary.json`, and the templates CSV beside it). Sides 1 and 2 swap in 7 rows (template 700-861-15x in 9 rows, 861-700-15x in 13).
- Where: `research/data/open_prototype/reports/lipi_h2218_h2239_side_role_templates.csv`, `..._side_role_counts.csv`, `..._side_role_tests.csv`, `research/data/open_prototype/reports/lipi_h2218_h2239_side_order_confound.csv`, `research/data/open_prototype/reports/h2218_h2239_dimension_side_order.csv`; series sheet `research/docs/archive/open_prototype_results.md` (H-2218 section); image leads for H-2219 only (three low-resolution thumbnails, 97x57 to 99x49 px).
- Old label: "sharper image-validation target; plate check pending for all rows." Reason: no plate has been checked, so no physical side order is accepted.
- Why it is alive: the series is one manufacturing batch under Meadow and Kenoyer's grouping, and the text template holds across every row. The two contested pairs (154/156 and 033/034) each appear as a single-row deviation in the same role slot as the 21-row majority, so the deviation is a single-object event, not a second population. The rowwise permutation is the only test here that does not depend on the batch.
- What it would mean if true: the H-series is a fixed three-part label: one object type, one count (+700-03x) and one 3-short-stroke role (+15x-003+) on side 3. Both contested pairs are then count or spelling variants inside the same role.
- Cheapest next move: pull the 22 side-3 and side-2 plates (figure 4 of the Meadow–Kenoyer publication, already mapped to rows in `research/data/open_prototype/reports/lipi_h2218_h2239_fig4_mapping.csv`) and count strokes in the 700-03x and 15x-003 roles for H-2237 and H-2238 first.

### 033 and 034 tablets differ in width and aspect ratio at raw p 0.036 and 0.042
- What was seen: in the 26-artifact mixed `+400-740-176+` family, the 033 group (n=17 horizontal, 16 area) has mean horizontal 13.735 mm against 11.588 mm for the 034 group (n=8), exact permutation p = 0.035523. Aspect ratio: 2.030 against 1.607, p = 0.041961. Area (93.5 against 86.1, p = 0.307) and vertical (6.90 against 7.61, p = 0.205) do not separate. Restricted to the canonical long-side-1/short-side-2 subset, horizontal p = 0.254 and aspect p = 0.239. Contrary numbers, once: no test survives Bonferroni or Benjamini–Hochberg across the six tests.
- Where: `research/data/open_prototype/reports/lipi_tab_i_mixed_400_740_176_dimension_probe_tests.csv`, `..._dimension_probe_rows.csv`, `..._side_context.csv` (all in `research/data/open_prototype/reports/`).
- Old label: "weak raw flags; no corrected signal; not metrological evidence" (dimension probe). Reason: multiple-test correction removed both raw flags.
- Why it is alive: the 033 tablets are the 3-stroke ones and the 034 tablets are the 4-stroke ones (lead 2). A count written on a longer tablet and a count written on a narrower one is a layout choice, and that choice is the only raw split with a direction that the stroke reading predicts.
- What it would mean if true: the tablet format depends on the stroke count written on it. That makes the width of the tablet a second record of the count.
- Cheapest next move: measure width on source-validated rows only (the 26 artifacts' plates) and rerun the same test with the stroke count as the label.

### 817 and 861 are both Wells graphemes of P385, and in the 002-governed closing slot they are used equally, but they differ in position
- What was seen: Mayig's feature file for P385 lists W817 and W861 together (`P385.json`). In 002-governed closings, 817 occurs in 89 distinct clean texts and 861 in 85. Elsewhere they differ: 817 occurs in 120 distinct clean texts with 109 final and 10 medial; 861 in 144 with 98 final and 39 medial. A two-sided Fisher exact test on final against non-final gives p ≈ 5.2e-6. Overlap positions: 861 aligns to P385 at 13 positions and 817 at 12.
- Where: `research/data/open_prototype/reports/lipi_scope_rows.csv` (distinct clean texts); Mayig `P385.json` in the feature folder above; `research/data/sign_crosswalk/source_panels/817_861_P385_conflict/` and `research/data/sign_crosswalk/p385_merge_collision_gate_20260712.json` (on disk, not opened).
- Old label: "terminal-operator candidate cluster"; "817/861 merge passes a structural screen but remains unvalidated epigraphically" (`structural_sign_classes` and sensitivity sections of `open_prototype_results.md`). Reason: the merge was never checked against a plate.
- Why it is alive: Wells, which Mayig cites, already lists both numbers for one Mayig sign. In the one slot where the two are used most (after 002) they are interchangeable (89 against 85). A closing sign spelled two ways is a common pattern in scripts with variant forms.
- What it would mean if true: one closing sign with two spellings, used as a fixed closer after 002, with 861 also used medially (39 times) where 817 almost never is (10 times).
- Contrary number, once: 861 is medial in 39 of 144 texts and 817 in 10 of 120; a true allograph should not split by position this way. Either the two forms carry different sense, or 861 is a second sign with the P385 shape.
- Cheapest next move: read the 39 medial 861 rows against their neighbours. If they show the same neighbours as the closing 817 rows, the split is positional and the merge stands. If the neighbours differ, the two codes are separate signs.

### 002 governs the closing sign: 236 of 272 texts ending in 002-X end in 817, 861 or 820
- What was seen: among 272 distinct clean texts whose penultimate token is 002, the final token is 817 (89), 861 (85) or 820 (62). The three together cover 236 of 272 (86.8%). 060 governs a different closing set: 920 (45), 692 (26), 820 (20), 550 (19). In the full Lipi file 060 sits in a medial position in 144 of its 145 occurrences, and 002 in 439 of 455 (distinct clean texts).
- Where: `research/data/open_prototype/reports/lipi_scope_rows.csv`; `research/docs/archive/methods_terminal_governor_effective_unicity_20260531.md` (the 002/060 terminal-governor test: target-penult top-3 0.787 across 456 rows against 0.177 for non-target penults, final-shuffle null p = 0/1000, block stress holds at top-3 0.761 to 0.806).
- Old label: "structural candidate, not decipherment." Reason: the test was run on the unreduced data; the note names source-token collapse as the decisive next test, which has not run.
- Why it is alive: 002 is the Lipi and Wells code for two half-height strokes (P122 = W002), and the closing set it governs is the same closing set as 817/861 (lead above). A numeral that precedes a closing sign reads like a count before a noun. The frequency confound the note checked (002 top-3 0.856 across 313 rows) does not rule this out; it is the same governor.
- What it would mean if true: the closing sign after "2" is a counted item. The 002 governor is then a grammar of counts.
- Cheapest next move: the note's own next test (collapse by source family, rerun held-out prediction). Also run M-77 (`+832-390-803-002-861+`) and M-72 (`+740-255-705-140-003-002-861+`) through it as held-out texts. Both end in 002-861, and M-77 is in the M-77 conflict gate with its closing pair never checked against the governor.

### 900 and 920 both align to Mayig P154, and they behave differently in position
- What was seen: in the count-matched overlap, Lipi 900 aligns to P154 (right parenthesis, W900) at 6 positions and Lipi 920 aligns to P154 at 5. Lipi 920 aligns to P160 (right parenthesis with a leaf, W920) at 2. In the distinct clean texts, 900 is medial in 40 of 50 and final in 9; 920 is final in 56 of 91 and medial in 32. M-98 has 900 as a final token on the plate. Two-token 920 contexts: 060-920 (45 texts).
- Where: `research/data/open_prototype/reports/overlap_probe.csv`; `research/docs/archive/m098_terminal_parenthesis_omission_gate_20260712.md`; Mayig `P154.json` and `P160.json`.
- Old label: "P154-like" missing terminal sign (M-98 gate); "900 = P154" edge "not promoted as a global rule." Reason: one object only.
- Why it is alive: Wells separates the two codes by a leaf. Lipi's 920 at P154 is the only conflict with Wells in the parenthesis family. The position split (900 medial, 920 closing) fits two different signs better than one sign with two spellings.
- What it would mean if true: two parentheses, one plain and one with a leaf, used in different positions in the text. The leaf-parenthesis closes the text; the plain one sits inside it.
- Cheapest next move: check the five P154-aligned positions coded as 920 on the plates for a leaf. The leaf is visible or not; no reading is needed.

### 520 is W520 and P217 (spear or arrow) at 15 of 16 positions; the M-126 and M-162 readings put it on P230 (pincer)
- What was seen: Lipi 520 aligns to P217 at 15 positions and to P160 at 1. Wells gives P217 = W520, described as an isosceles triangle on a vertical line (arrow or spear). M-73 (`+400-520-897+` over `P098 P217 P181 P000`) matches again. The M-126 gate reads Lipi 520 against Mayig P230 (`+520-552-060-692+` over `P000 P230 P234 P120 P256`). Wells gives P230 = W550 and W555, and P234 = W551. Lipi 798 aligns to P230 at 8 positions and to P075 (W798, leaf with pincers) at 4. Lipi 520 is initial in 130 of its 155 occurrences; Lipi 552 has only 9 occurrences in the whole file.
- Where: `research/docs/archive/m162_complementary_pair_segmentation_gate_20260712.md` (the "probable_520" missing unit); No standalone M-126 gate note is on disk; the M-126 reading is taken from the M-162 gate and the P000 damage-span gate (`research/docs/archive/p000_damage_span_policy_gate_20260712.md`); `research/docs/archive/m77_text7_object_concordance_decision_20260712.md` (M-37 bridge, `520/P217`).
- Old label: "compound or omission; unresolved" (M-161 and M-162 gates); "source-visible six units; probable missing Lipi unit before 552" (M-162). Reason: the 520 in M-126 was read as P230, and the M-162 gate used that to place a missing unit.
- Why it is alive: the M-126 reading is object-level and was checked against a plate. The 15-to-1 pattern against P217 is a count across the whole layer. Both readings stay alive until one observation splits them.
- What it would mean if true: either Lipi 520 is a two-sign token (spear and pincer) or the M-126 reading is wrong. If Lipi 798 is the pincer, the missing M-162 unit is 798 and not 520, so the M-162 gate's inference shifts.
- Cheapest next move: crop the 520 position on M-126 and compare it with the 520 position on M-37 and M-73 (the source panels for those objects are in `research/data/sign_crosswalk/source_panels/`). The pincer and the spear are visibly different graphics.

### Lipi 617 is a two-grid token; Wells places single grids at 615 and 616, and 617 has no Mayig code
- What was seen: five overlap objects (M-4, M-25, M-45, M-81, M-161) show Lipi 617 where Mayig writes P268 P268, and the source plates show two grids on each. The Wells column places single grids at W615 (P268) and W616 (P269, a grid with a tall stroke on one side). W617 appears in no Mayig feature. Lipi 615 appears in 70 rows of the full file and 617 in 75 rows.
- Where: `research/docs/archive/m004_617_overlap_policy_closure_20260712.md`, `research/docs/archive/m025_double_grid_pair_segmentation_gate_20260712.md`, `research/docs/archive/m045_double_grid_pair_segmentation_gate_20260712.md`, `research/docs/archive/m081_double_grid_pair_segmentation_gate_20260712.md`, `research/docs/archive/m161_mismatch_gate_20260712.md`; source panels under `research/data/sign_crosswalk/source_panels/m004_double_grid_pair/`, `m025_double_grid_pair/`, `m045_double_grid_pair/`, `m081_double_grid_pair/`.
- Old label: "compound_or_omission_policy unresolved" (M-161); "617 = P268 P268 is a catalogue expansion candidate, five of five" (M-4 closure, accepted for the five overlap rows only). Reason: no rule for Lipi-only 617 rows.
- Why it is alive: 617 is the one token in the corpus where the source has been checked five times with zero counterexamples. Wells numbering puts the single grid at 615, so 617 reads most simply as a doubled grid token with its own number. The 75 Lipi rows outside the overlap that carry 617 are then two-grid rows as well, which would move a large block of counts.
- What it would mean if true: Lipi writes doubled signs as single tokens with their own numbers; 617 (two grids), 821 (two wheels, M-111) and 036 (two three-stroke groups, M-20) are then the same convention.
- Contrary number, once: Lipi does not always collapse doubles. 033-033 appears adjacent in 14 Lipi rows (6 in the clean layer, e.g. H-1670 at 731.1, H-1899 at 628.2) and 032-032 in 4 rows. Those rows have no Mayig check.
- Cheapest next move: check the 14 rows with 033-033 and the 4 with 032-032 against plates. The collapse convention holds if those rows show one double-stroke group written as two tokens, and fails if they show two separate groups.

### Every Mayig repeat is a Lipi-short mismatch (8 of 8)
- What was seen: eight Mayig side records contain two identical consecutive graphemes: M-4 (P268), M-20 (P147), M-25 (P268), M-45 (P268), M-81 (P268), M-105 (P324), M-111 (P378), M-161 (P268). All eight are count-mismatch rows, and in all eight Lipi has fewer tokens than Mayig. Lipi writes the double as 617, 036, 821, or in M-105 as 000-000.
- Where: `research/data/open_prototype/mayig/records_index.csv`; `research/data/open_prototype/reports/overlap_probe.csv`; `research/docs/archive/mismatch_collation_queue.md`.
- Old label: "unflagged_mayig_extra... cannot be resolved statistically from the current open data." Reason: a repeat could be a real double, a segmentation split, or a transcription convention.
- Why it is alive: every case of a double in the Mayig layer is a Lipi-short case. Repeat doubling alone explains the whole Mayig-extra class. That is a rule, not a list of exceptions.
- What it would mean if true: Mayig writes every double as two graphemes; Lipi writes every double as one token; the counts on all doubles differ by one, and any count-based statistic built on either layer is off by the number of doubles.
- Cheapest next move: count consecutive identical Lipi tokens across the full layer (done here: 12 clean rows) and check whether each sits on a Mayig double; that shows which side of the convention the 12 rows fall on.

### Two numerals are missing Mayig overlap cases: 001 to 005 are numbered strokes, 031 to 035 are numbered tall strokes, and 032 splits as 2 plus 3 in one object and as 035 in another
- What was seen: the same Mayig code is written two ways in Lipi. P151 (five full-height strokes) is Lipi 032+033 in M-10 and Lipi 035 in M-16 (`+820-130-035-171+` over `P378 P026 P151 P346`). P125 (five short strokes) is Lipi 003+002 in M-72 and Lipi 005 in M-40 (`+391-002-527-475-005+`) and M-138 (`+740-900-005+`). The Mayig stroke-count sets for 3 full-height strokes include variants P148 (with a tree, W045/W046), P149 (with a caret, W044), P152 and P153 (angled strokes, no Wells). Lipi 033 aligns to P147 only (10 positions), so the variants have no separate Lipi token yet.
- Where: `research/docs/archive/m072_five_stroke_run_segmentation_gate_20260712.md`, `research/docs/archive/m010_five_stroke_run_segmentation_gate_20260712.md`, `research/docs/archive/m020_six_stroke_run_segmentation_gate_20260712.md`; Mayig stroke features in the feature folder above.
- Old label: "atomicity unresolved" (M-10, M-20, M-72). Reason: the source shows one run; the catalogues cut it differently, so neither count was adopted.
- Why it is alive: a count of five written 2+3 or 3+2 is an additive numeral, and Lipi uses both orders. The additive reading is the one that accounts for both the 032+033 and 003+002 splits. Contrary number, once: 032-002 is the most common numeral pair (32 rows), which is 4, not 5, so the additive rule is not general.
- What it would mean if true: Lipi writes numbers as sums of stroke tokens, Mayig and Wells write them as single codes. Both are correct; the sum rule is the Lipi convention.
- Cheapest next move: tabulate every adjacent pair of numeral tokens in the full Lipi file and see whether the pair totals are 5 (003-002, 032-033) and 6 (033-033) more often than chance. The shuffle test in this sweep is the template.

### The Lipi numerals in the object-level gates: each "missing" Mayig sign is the Wells code the gate names
- What was seen: the three gates that found a Mayig omission each name a Lipi token that Wells assigns to the Mayig code they name. M-41 has a missing middle fish; the gate calls it "P058-like" and Lipi has 233 in that position. Wells gives P058 = W233, and Lipi 233 aligns to P058 at 13 positions. M-98 has a missing terminal right parenthesis, "P154-like"; Lipi has 900, Wells gives P154 = W900. M-120 has a detached diamond, "P363-like"; Lipi has 858, Wells gives P363 = W858.
- Where: `research/docs/archive/m041_middle_fish_omission_gate_20260712.md`, `research/docs/archive/m098_terminal_parenthesis_omission_gate_20260712.md`, `research/docs/archive/m120_slash_compound_source_decision_20260712.md`.
- Old label: "do not promote a global 233 = P058 rule" (M-41); "do not promote a global 900 = P154 edge" (M-98); "no global 858 = P363 edge" (M-120). Reason: each gate refused a global mapping from one object.
- Why it is alive: the three objects are the only Mayig omissions checked against plates, and each omitted sign is exactly the Wells code of the Mayig code its gate chose. Three objects matching the same namespace is more than one object.
- What it would mean if true: the omitted signs in the Mayig layer are recoverable from Lipi, so Mayig's missing units can be restored without a source plate for each case.
- Cheapest next move: run the Lipi-token restore on every Mayig-short overlap row and check the restored count against the source plate for the 4 Lipi-short cases already checked (M-10, M-72, M-41, M-98).

### BASE string: 520-220-415 sits in 12 distinct clean texts, and 220-415 (fish, pitchfork) in 51
- What was seen: the seven-object BASE string +520-220-415+ (M-37, H-938, H-939, H-1284, H-940, H-2148, H-2240) is a contiguous run in 12 distinct clean texts (28 rows). The tail 220-415 is contiguous in 51 distinct clean texts (85 rows). 520-033 is contiguous in 49 distinct clean texts. The U position (415) is pitchfork (P092 = W415; `research/data/open_prototype/reports/` alignment shows 415 at P092 in 5 positions). The H-942 variant `+520-220-016+` has 016 at the same position, and Lipi 016 aligns to P126 (six short strokes, W016) at 6 positions.
- Where: `research/docs/archive/m77_text7_object_concordance_decision_20260712.md`, `research/docs/archive/m77_parpola_recurrence_conflict_gate.md`, `research/docs/archive/p041_mayig_parpola41_crosswalk_falsification_gate.md` (namespace), Mayig `P092.json`, `P126.json`, `P217.json`, `P050.json`.
- Old label: "exact companion string survives across 7 named objects; M-77 is an adversarial conflict control; 415 = 016 not accepted" (M-77 gates). Reason: the M-77 recurrence sentence did not match the local companion family.
- Why it is alive: the 220-415 tail is common enough to be a formula unit, and the variant at the U slot in H-942 is six strokes, not another pitchfork. A count in the closing position is the same pattern as the 002/817/861 closers.
- What it would mean if true: the BASE string is a three-picture label (arrow or spear, fish, pitchfork) and H-942 writes its closing picture as a count of six.
- Cheapest next move: check the 12 distinct BASE-containing clean texts and the 51 with 220-415 for the closing sign, and count strokes in the H-942 closing position.

### M-37 bridge: the Wells descriptions agree with Parpola's sign descriptions at all three positions
- What was seen: the M-37 bridge aligns Lipi 520 to P217, 220 to P050, 415 to P092. Wells numbers these as W520 (isosceles triangle on a vertical line, arrow or spear), W220 (fish with no other decoration), W415 (pitchfork with tines). The M-77 gate states Parpola's descriptions of signs 189 (spear or arrow) and 60 (plain fish), and identifies U as the unnumbered first sign in reading order. Positional counts: 520-P217 15, 220-P050 28, 415-P092 5.
- Where: `research/docs/archive/m77_text7_object_concordance_decision_20260712.md`; Mayig `P217.json`, `P050.json`, `P092.json`.
- Old label: "object-bound positional graphic bridge; no sign value accepted." Reason: a bridge at one object was not extended.
- Why it is alive: two of three positions agree in content (arrow and fish) with a published description, and the third (pitchfork) is the unnumbered U. Three independent pictures in reading order is a picture label.
- What it would mean if true: the BASE label names three things: a spear or arrow, a fish, and a pitchfork. Meanings-first guess: the label is a short list of picture-names (for example an object, an animal, a tool), not a grammar.
- Cheapest next move: pull Parpola's description of sign 107 (the text no. 7 final sign) and check whether Lipi 400 (initial in 181 of 203 occurrences) matches it. If it does, Lipi 400 is a candidate for sign 107 in the four-sign text.

### H-2147 and H-940 put the BASE string and the 110 side on opposite sides of the object
- What was seen: H-940 has BASE on 1820.1 and +110+ on 1820.2. H-2148 has the same arrangement (481.1 and 481.2). H-2147 has ]110+ on 673.1 and ]220-415+ on 673.2, the reverse. H-2240 has BASE on 816.1 and +869-575+ on 816.2. The Lipi 110 token has no Mayig alignment.
- Where: `research/docs/archive/m77_parpola_recurrence_conflict_gate.md` (local matrix); `research/docs/archive/p041_mayig_parpola41_crosswalk_falsification_gate.md` (H-2148 chain).
- Old label: "strong_same_role_inference"; "same-side identity pending" (H-2148). Reason: the sides were not checked against plates.
- Why it is alive: the swap is the same A/B swap the H-series shows in 7 of 22 rows. If side order is arbitrary in the catalogue, BASE and 110 would appear both ways round, which is what the data show.
- What it would mean if true: BASE and 110 are one two-sided pair in which the object's face decides which label is up; the side order in the catalogue is not a reading order.
- Cheapest next move: compare the plates of H-2147 and H-940 for which face carries BASE.

### Lipi 101 is the bracketed form of 100: P009 (three-headed person) is W100, P010 (bracketed) is W101 and W103
- What was seen: Lipi 100 aligns to P009 (three heads) at 3 positions and to P062 at 1. Lipi 101 aligns to P010 (bracketed by right parentheses, W101/W103) at 1 position, and to the M-7 compound (P154 P009 P154) in the object-level alignment. Lipi 101 occurs in 8 rows and 100 in 129. The two codes never sit next to 900 (0 adjacencies in the full file), and 101 is most often preceded by 740 (for example +407-845-140-740-101-923-240-002-861+).
- Where: `research/docs/archive/m007_bracketed_three_head_compound_gate_20260712.md`; Mayig `P009.json` and `P010.json`.
- Old label: "compound-level count 9; P010-like; do not count P154-P009 as adjacency" (M-7 gate). Reason: Lipi's bracket marks and the three-headed figure are one compound on the plate.
- Why it is alive: Lipi uses 900 for a bracket on its own (M-98) and 101 for the bracketed figure (M-7). That is the pattern you get when a single bracket is a separate sign and a bracketed figure is written as a compound.
- What it would mean if true: 101 is the three-headed figure with brackets, 100 the figure alone, and the brackets are not counted separately when they wrap a figure.
- Cheapest next move: count 100-900 and 900-100 adjacencies across all 5,679 rows (zero in the clean layer, to be checked across the full file, which this sweep did for the clean layer only).

### The stored order holds at 95% and the Mayig side-by-side scaffold has 22 hits against 0 reversed
- What was seen: stored order beats reversed in 2,748 of 2,887 numeric-clean rows and in 1,705 of 1,798 distinct clean texts (94.8%). The Mayig I...T scaffold (first sign from a start set, last from an end set) gives 22 hits in the observed order, 0 reversed and 1.25 under shuffles. Lipi 740 is initial in 636 of 885 occurrences and final in 3.
- Where: `research/docs/archive/open_prototype_results.md` (direction and order sections, `lipi_broad_order_summary.json`, `lipi_dedup_order_summary.json`); `research/data/open_prototype/reports/formula_pattern_summary.json`.
- Old label: "A2 structural evidence only" and "not semantic". Reason: order was treated as a scout result, not a direction reading.
- Why it is alive: direction is measured on 2,887 rows with no reversed majority, and the initial-and-final scaffold does not appear when the text is reversed. A catalogue direction that goes against this would be a scribal convention, not an error.
- What it would mean if true: stored order is the reading direction for the bulk of the corpus; the H-1302 and H-1303 mirror claim is an exception to test, not a rule.
- Cheapest next move: run the scaffold test on the H-1302 and H-1303 rows alone (two rows) and on the 17-object packet.

### Inside-text context survives removing the ten most common edge signs at about 2.4 times the best simple baseline
- What was seen: with 740, 700, 400, 520, 033, 032, 861, 817, 820 and 034 removed from edges, bidirectional top-1 is 0.222222, against 0.092508 for the best simple baseline (length-position), giving a ratio of 2.40. Frequency top-1 is 0.072383 and position top-1 is 0.088449. Held-out artifact types and sites stay between 0.176 and 0.199.
- Where: `research/docs/archive/open_prototype_results.md` (edge-removal section); `research/data/open_prototype/reports/lipi_edge_removed_summary.json`.
- Old label: "stricter structural residue; not a semantic or translation result." Reason: the removal was a control.
- Why it is alive: the context signal does not come from the edge signs alone. Removing the numerals (001–007, 031–036) and the frame sign 700 is the sharper version of the same control, and nothing has been run on it.
- What it would mean if true: inside-text sign-to-sign rules are not a numeral effect; they reach the non-numeral signs too.
- Cheapest next move: remove the numeral tokens and 700 as well, and rerun the same bidirectional test on the rest.

### Lipi versus Linear B under one masked-sign test: the Indus layer's context lift over a slot null is 2.24, Linear B's 3.44
- What was seen: Linear B Series D (513 clean rows) gives bidirectional top-1 0.470200 against a position-slot null of 0.136725; the lift is 3.44. The IVC-like duplicate-collapsed Lipi layer gives 0.325865 against 0.145622; the lift is 2.24. With an IVC-like length cap (p95, 8 tokens) Linear B gives 0.435897 and the Lipi layer stays at the same value. Structured administrative and emblem codes (built to match the Lipi layer's duplicate profile) give 0.472924 and 0.443351, both above the Indus value.
- Where: `research/docs/archive/open_prototype_results.md` (Linear B and structured null sections); `research/data/open_prototype/known_scripts/linear_b_series_d/` (Samples.txt named in the note, on disk, not opened); `research/data/open_prototype/nonlinguistic/`.
- Old label: "scarcity ceiling; not a translation score." Reason: the comparison was a ceiling for the method.
- Why it is alive: on the same test the Indus layer sits between a slot-randomized null and a real administrative language, and nearer the null. The administrative code generator sits above both, so the metric does not separate language from code, but the lift number does separate the Indus layer from Linear B.
- What it would mean if true: the Indus layer has context about 0.66 of what Linear B has above its slot null, which fits a short-text, heavily formulaic corpus.
- Cheapest next move: rerun the Linear B and Lipi comparison with the Lipi length distribution imposed on Linear B (sample Linear B rows to the Lipi length histogram). If the gap closes, the 2.24 against 3.44 difference is length, not structure.

### Lipi class codes predict sign tokens after length, type and site shuffles, and the signal survives inside the TAB:I stratum
- What was seen: token naive Bayes on the class label gives 0.525714 accuracy on exact sequence families; block shuffles of length, type and site give 0.254029. On rows with a high-proxy class removed, token accuracy is 0.643089 against 0.322154 for the shuffle (macro-F1 0.522030 against 0.209834). In the TAB:I stratum the class token accuracy is 0.729508 and no null iteration reaches it. Class is 98.6% Harappa for VN (vn_harappa_share 0.985915) and 94.6% length 2 (vn_length_2_share 0.946479). TS is 98.8% length 1.
- Where: `research/docs/archive/open_prototype_results.md` (class sections); `research/data/open_prototype/reports/lipi_stratified_class_summary.json`, `research/data/open_prototype/reports/lipi_class_proxy_control_summary.json`, `research/data/open_prototype/reports/lipi_class_field_audit_summary.json`.
- Old label: "not admissible as independent semantic metadata"; "may reflect catalog conventions or circularity." Reason: no upstream definition of the class codes was found in 67 scanned text files; the class codes may be derived from the sign tokens.
- Why it is alive: a cataloguer who coded class from the signs has written down a classification that the signs support. If the classes are derived from the signs, the derivation rule is the content.
- What it would mean if true: class codes are a catalogue's own sign-role grammar; reversing the derivation would show which signs the cataloguer treated as class markers.
- Cheapest next move: cross-tabulate class against the numeral tokens (001–007, 031–036) and against 700. If VN rows carry numeral tokens and TS rows carry none, the class is a numeral category.

### 817 and 861 closing slot and the M-32 and M-177 duplicate: one exact four-sign text on two objects, with the same 003-002-861 ending as M-72
- What was seen: M-32 and M-177 have the same Mayig text P086 P123 P122 P385 (the only exact cross-object duplicate the sweep found in the Mayig layer, from `research/docs/archive/open_prototype_results.md`, formula variant section). That text is 390 followed by three short strokes, two short strokes, and the 817/861 closer. M-72 ends in 003-002-861 as well. The closer pair 002-817 occurs in 89 distinct clean texts and 002-861 in 85.
- Where: `research/docs/archive/open_prototype_results.md` (formula variant section); `research/docs/archive/m072_five_stroke_run_segmentation_gate_20260712.md`; Mayig `m032.json` and `m177.json` (on disk in the Mayig corpus, not opened here).
- Old label: "exact duplicate candidate"; no further check recorded. Reason: the formula variant test was for patterns, not for object identity.
- Why it is alive: two objects with one exact text and the same closing string is what two impressions of one seal look like, and the 002-closer is the commonest closing pattern in the clean layer.
- What it would mean if true: M-32 and M-177 are two impressions of one seal, and the text 390-003-002-861 is a single stored formula.
- Cheapest next move: check whether M-32 and M-177 share a seal, a find site or a catalogue note. A shared object would make them one text, and any count would be off by one.

### Reversed short-mark companions may be mirror impressions, and the Nature 2021 mirrored-writing claim names two packet objects
- What was seen: among 700-companion rows, 700 is last in 55 of 368 rows (orientation audit) and the reversed 033 is 24 rows, 034 13 rows, 032 17 rows. The public lead (`research/docs/archive/h1302_h1303_direction_note_recheck.md`) names H-1302 and H-1303 in a mirrored-writing and corpus-correction discussion. Both are in the 17-object short-mark packet. The public image set has 2 unlabelled object-panel candidates and 0 filled source fields.
- Where: `research/docs/archive/h1302_h1303_direction_note_recheck.md`; `research/data/open_prototype/reports/lipi_short_mark_orientation_rows.csv` and `..._companions.csv`; `research/data/open_prototype/reports/lipi_short_mark_plate_request_packet.csv`.
- Old label: "direction note recheck; acquisition targeting only." Reason: no plate check was possible from the public images.
- Why it is alive: a reversed companion that comes from a mirror impression would explain the 55 reversed rows without any change of sign value, and it would fold the H-1302 and H-1303 claim into the same catalogue fact.
- What it would mean if true: 700-last rows are the mirror impressions of 700-first rows, and the catalogue's direction for those objects is wrong.
- Cheapest next move: check the two unlabelled object panels for H-1302 and H-1303 against the 700-last rows of the orientation audit.

### Exact-sequence closing formula and the 2-stroke numeral
- Folded into 002 governor and 817/861 leads above; no separate entry.

### The Meluhha name-plus-title adjacency is one text, and the 001-803-415 triple is unique in the clean layer
- What was seen: the only adjacency of the name lu2-sun2-zi-da with a Meluhha title in any of 15 CDLI hits is P212982 / CT 50, 076 (line 5 name, line 6 lu2 me-luh-ha-ke4). The other 14 are Ur III Puzrish-Dagan administrative texts. In the clean Lipi layer the Ur object's consecutive triple 001-803-415 (`+002-004-328-001-803-415+`, U17649, route verified) occurs in 1 text, and 803-415 occurs in 1 text. The four-sign target the old agents tested against this object was pattern-only, with forger share 1.000000.
- Where: `research/docs/archive/meluhha_lu_sunzida_anchor_failure.md`; `research/docs/archive/object_level_onomastic_value_attempts.md`; `research/docs/archive/meluhha_external_phonetic_anchor_attempts.md`; `research/data/open_prototype/...` and `research/data/meluhha/` (cuneiform_attestations_expanded.csv, external_indus_objects.csv, control_toponyms.csv, cuneiform_source_routes.csv, cdli_current_lu_sunzida_test.csv named in the notes; `research/data/meluhha/` exists on disk, not opened).
- Old label: "retracted as an external anchor; name-alone false-positive rate 0.933333"; "pattern-only mapping retracted." Reason: name recurrence in 14 Ur III texts and site-only match.
- Why it is alive: a single adjacency of a personal name and a Meluhha title is the one syntactic pattern the sources share with the Shu-ilishu interpreter seal (e-me-bal-me-luh-ha). The Indus side of that pattern would be a two-part name-plus-title, and the Ur object's 001-803-415 is a unique three-sign run in the clean layer.
- What it would mean if true: an Indus two-part name and title exists on an object found in Mesopotamia; the phonetic pairing would be the first object-level link.
- Cheapest next move: the primary edition check of the Shu-ilishu inscription (AO 22310) that the matched-control schema names but never ran; then check whether the Ur object's last two signs (803, 415) are a name and a title in the Gadd or British Museum record.

### The Lipi-to-Wells identity gives a sign-level handle on the Parpola 41 question
- Folded into lead 1 and the H-2148 chain. The P041 gate's one overlap pair is W112, and the Lipi 110 token has no Mayig alignment at all, so the local 110 question is a Wells-number question once a Wells page for W110 is read.

---

## Sources on disk
- `research/data/open_prototype/reports/lipi_scope_rows.csv`: 5,679 Lipi rows with readiness bucket, direction and text; the base layer for every count here.
- `research/data/open_prototype/reports/overlap_probe.csv`: 179 Lipi-Mayig overlap rows with the Mayig graphemes and the count-match flag.
- `research/data/open_prototype/mayig/records_index.csv`: 179 Mayig side records (artifact base, description, graphemes).
- `research/data/open_prototype/lipi/metadata_filtered.csv`: filtered Lipi metadata, 5,679 rows, with dimensions and condition.
- `evidence/tmp/mayig_feature_namespace_probe/repo/indus-valley-script-corpus-ad2f1e218a34b8c33c57de0d6cb8d99272765bbb/features/`: 397 Mayig feature JSON files with Wells numbers and descriptions (the source of the Wells column in lead 1).
- `evidence/tmp/mayig_feature_fetch/P122.json` and `evidence/tmp/p041_mayig_route/features__P041.json`: single feature copies.
- `research/data/sign_crosswalk/`: crosswalk edges, sign systems, namespace gates, source panels per object (`source_panels/` subfolders for m004, m007, m010, m020, m025, m041, m045, m072, m081, m098, m105, m106, m111, m120, m141, m161, m162, m77_text7, p000, 817_861_P385_conflict, 002_P122_conflicts, 032_P145_conflict, 390_P086_merge, 740_P324), plus `p385_merge_collision_gate_20260712.json` and `p041_parpola41_namespace_table_20260712.csv`.
- `research/data/open_prototype/reports/` (about 250 CSV and JSON outputs): the side-role, multi-side, orientation, companion-context, dimension and crosswalk files named in `research/docs/archive/open_prototype_results.md`.
- `research/data/open_prototype/known_scripts/linear_b_series_d/` (Samples.txt named in the Linear B note), `research/data/open_prototype/known_scripts/sumtablets/`, `research/data/open_prototype/known_scripts/sproat2014/`.
- `research/data/open_prototype/nonlinguistic/`: structured null outputs (not opened).
- `research/data/meluhha/`: Meluhha cuneiform and external-object tables named in the Meluhha notes (not opened by this sweep).
- `research/data/brahmi/`, `research/data/mahadevan_20260905/`, `research/data/decoding_followup_20260907/`, `research/data/semantic_search_20260906/`, `research/data/claim_ledger/`, `research/data/quarantine/`, `research/data/open_prototype/tools/`: present on disk, outside this chunk, not opened.
- Source photos and plates: the CISI 1 PDF (SHA-256 `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`, named in the M-gates; its local path is not given in the reading list); the M-77 CISI India page crop (`tmp/m77_parpola_recurrence_gate/`, named in the M-77 gate; not on disk in this checkout as far as the reading list says).
- `research/data/open_prototype/reports/h233_public_slide_visual_lead_audit.csv`, `h2219_public_image_leads.csv`, `h2218_h2239_public_image_lead_search.csv`: public image lead tables (thumbnail-grade).

## Ideas named but never run
- Source-token collapse of the 002/060 terminal governor, then a heavier shuffle (`methods_terminal_governor_effective_unicity_20260531.md`, named as the decisive next test).
- Run the M-77 and M-72 closing pairs (002-861) through the held-out governor test.
- Plate check of the 520 position on M-126, M-37 and M-73 (spear versus pincer).
- Stroke counts on the H-2218 to H-2239 side-2 and side-3 roles (figure 4 mapping exists; no plates checked).
- Read the 39 medial 861 rows and the 10 medial 817 rows for neighbour identity (allograph test).
- Check the 920 leaf on the five P154-aligned positions coded as 920.
- Remove numeral tokens and 700 from every row and rerun the bidirectional test.
- Length-match Linear B to the Lipi length histogram and rerun the 2.24 against 3.44 comparison.
- Cross-tabulate Lipi class codes against numeral tokens and against 700.
- Check whether M-32 and M-177 are impressions of one seal (exact four-sign text).
- Mayig provenance check of `wells_graphemes` (whether Mayig derived its Wells column from Lipi).
- Read Wells's own sign list for W110, W034, W617 and W821, which Mayig does not list (only Mayig's copies were read here).
- Pull Parpola's description of sign 107 and compare with Lipi 400 (guess: Lipi 400 is sign 107 in the text no. 7 four-sign string).
- Count Lipi 167 and 137 (short-mark enrichments 18.06 and 6.71 in the multi-side summary) and find their two-token companions; no note followed them up.
- Check Lipi 110 as a short-side token (it sits alone on the short side in H-940 and H-2148 and has no Mayig alignment).
- Check Lipi 074 (H-2145 slot-1 variant of 520) and 016 (H-942 slot-3 variant of 415) on plates.
- Align Mayig P144 (one full-height stroke) and P126 (six short strokes) to Lipi 031 and 006 (both have Mayig records but no overlap positions).
- Open the Shu-ilishu AO 22310 edition (primary check named in `meluhha_matched_control_schema.md`, never run).
- Matched non-Meluhha cuneiform controls for Dilmun, Magan, Marhasi, Elam, Gutium, Gubi and Susa (named in the matched-control schema, never run).
- Object routes for Kjaerum 279/319, Amiet 1643, Mitchell 1986, Sarzec and Heuzey (named in `object_level_onomastic_value_attempts.md`, never run).
- Failaka rows 147.1 and 148.1: primary object route (Laursen 2010, Kjærum 1983, named, not verified).
- Susa row 3882.1: the Louvre route (SB 2425, AS 41, CCO S.299) and whether the object carries a cuneiform name.
- Ur rows 3897.1, 5225.1, 5231.1: the public British Museum and Gadd route pool, still unmapped.
- BM 120573 (Diqdiqqah, U.7683): Sumerian inscription read for a name or title.
- Non-unicorn Mayig material: the metadata scope probe lists it as the next falsification (all 179 Mayig records are Mohenjo-daro unicorn seals).
- Coptic SCRIPTORIUM as the continuity upper bound (named in the known-script audit, not run).
- SumTablets after revision pinning and transliteration-label hiding (named, not run).
- Plate checks for the 17-object short-mark packet (H-1304, H-1344 to H-1347 are source-dark; H-355, H-933, H-960, H-233, H-1302, H-1303 need plates).
- Parpola 2019 Figure 1 and the M-2109 and M-2111 rod transcriptions (named, not on disk).
- Kenoyer 2005 Figure 14.1 one-sign panel (named in the H-2148 chain).
- The Meadow and Kenoyer 2000 figure 4 PDF (download returned 403; viewer only, per `research/data/open_prototype/reports/h2218_h2239_fig4_visual_availability...`).
- Upstream `yajnadevam/lipi` repository class-code definitions (the 67 scanned files had none).
