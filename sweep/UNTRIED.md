# UNTRIED: ideas the old notes named and never ran

Merged from the "Ideas named but never run" lists in `sweep/out/leads_00.md` to `leads_14.md`, de-duplicated. Each line: the idea, what running it takes, the data it needs. Paths are relative to `/home/claude/ivc`; the full inventory is `sweep/SOURCES.md`. Short names: Lipi = `research/data/open_prototype/lipi/metadata_filtered.csv` (called LIPI below); Mayig features = `evidence/tmp/mayig_feature_namespace_probe/repo/indus-valley-script-corpus-ad2f1e218a34b8c33c57de0d6cb8d99272765bbb/features/`; seal photos = `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images/` (SEALS); reports = `research/data/open_prototype/reports/`.

Items marked [new] were proposed by a reader and not named by the old logs. Items marked [blocked] need a source that is not on disk (see SOURCES.md section 8).

---

## 1. Tail and terminal grammar: 002-390-X, 032-002-861, 125, 705, 820

1. Source-bound blind token-boxing of M-119, M-735, M-70, M-71, then M-41's continuous band, with a family and register null. Takes: draw boxes from the photo with the reading hidden, score against Lipi strings. Data: SEALS (`M-119_a.jpg`, `M-735_a.jpg`, `M-70_a.jpg`, `M-71_a.jpg`, `M-41_a.jpg`), `evidence/tmp/002390x_source_normalization/`, `evidence/tmp/002390x_token_boundary_adjudication/`, LIPI.
2. Freeze the 002-390-X table and score each source-visible row before reading its photo; open predictions exist for H-1993 (closes on 095), M-1825 and Dholavira 4237.1 (close on 705), Sktd-1 (continues on 125). Takes: write predictions, then read photos. Data: `evidence/tmp/002390x_source_normalization/`, Sktd-1 crops; H-1993 and M-1825 are [blocked] (CISI 3.1).
3. Hunt a source-bound exception to the 002-390 frame: 125 terminal after 002-390, or 095, 692, 705 continuing after it; search terminal 125 inside any source-bound 002-390-X context. Takes: LIPI filter, then photo check of each hit. Data: LIPI, SEALS.
4. Build all source-visible 125-to-632 and non-125-to-632 environments and test whether 632-032 clusters after 002-390-125 across separate source families; find a third strict source-visible 125 branch family. Takes: LIPI join with source-visible flags. Data: LIPI, `reports/campaign_032_002_861_*`.
5. Photograph-check the three non-125 632-032 rows (predecessors 368, 504, 892) and the M-1188 row; the three governed 530 rows C-57, M-623, 4182.1 for the one-complement shape, plus find a fifth 530 row. Takes: locate each in SEALS or CISI leaves. Data: SEALS (`M-623_*`), Mackay PDF for C-57, LIPI. M-1188 and C-57 have no image on disk.
6. Dimension-only twins 3335.1, M-71, H-42 (all 29 x 29 x 0 with a Bull1:J symbol): test whether they link. Takes: LIPI dimension filter, photo comparison. Data: LIPI, SEALS (`M-71_a.jpg`, `H-42_*`).
7. Copy test of 3335.1 against M-746 and M-965 (source-visible 390-590-032 seals). Takes: sign-for-sign comparison of the row with the photos. Data: SEALS (`M-746_a.jpg`, `M-965_a.jpg`), `evidence/tmp/002390x_390590032_family_recheck_20260531/`, LIPI row 3335.1.
8. Collapse by site, register, object type, source route, exact formula and signless formula, then ask whether the branch predicts tail class. Takes: one script over the strict layer. Data: LIPI, `reports/campaign_032_002_post_y_all_002_rows.csv`.
9. Length-matched closure test for the 817/820/861 split; bare-versus-tailed 002-861 contrast with M-19 and M-175 added; minimal-pair test with closure-family and branch-family Y in matched frames. Takes: matched-frame script, no GPU. Data: `reports/campaign_032_002_post_y_*`, `research/data/sign_crosswalk/source_panels/damaged_boundary_fragment_closure/`.
10. Terminal space for H-444, M-723, M-1044 recut with the metric used on M-91 and M-240; measure M-1750 when acquired; re-measure M-91, M-240 and the four bare controls with one ruler and no overlay; find a bare closure row with terminal space comparable to the 120 px tailed windows. Takes: pixel measurement on crops. Data: `evidence/tmp/032_002_861_bare_edge_source_controls/`, `evidence/tmp/032_002_861_terminal_space_recut_v2/`, SEALS. M-1750 [blocked].
11. Photograph-check the five unphotographed 220-032-002-861 rows (62.1, 1434.1, 2313.1, 3147.1, 3421.1) and measure terminal space on each. Takes: find each in SEALS/CISI. Data: LIPI, SEALS, Mackay PDF (62.1 is Chanhu-daro).
12. Post-861 spacing features for 533-717: distance from 861 to the physical edge, terminal cluster separation, A/a agreement; a third independent source-visible 533-717 row; source-route M-1954 and M-1973; blind layout test with 533 and 717 cropped separately; collect no-icon SEAL:R rows from unseen objects; count 533 and 717 separately outside the pair (533 in 2 rows, 717 in 41). Takes: layout measurement plus LIPI counts. Data: `evidence/tmp/032_002_861_533717_*`, LIPI. M-1954 and M-1973 have no image on disk.
13. Extend X-before-240 from 603, 636, 642 to all X values; count 603 after 032-002-861 across all rows versus after other tails; after-240 subframe count over the strict layer; count 240-031-002-861 with the head before 240; within-site-type split of the 240-032 contrast with object-level dedup. Takes: LIPI queries. Data: LIPI, `reports/campaign_032_002_861_x240_*`.
14. Graphic-identity check of H-1137, H-1138, H-1846 for the 603 lock; recrop the H-1138 edge to count units; orientation check of H-1138 slot boundaries under R/L and visual LTR. Takes: image crops. Data: `evidence/tmp/032_002_861_603_slot_source_normalization/H1138_*`, `H1846_*`, `032_002_861_603_graphic_identity_packet/`. H-1137 has no image on disk.
15. Check H-360 (Vats XCVIII 584) and H-1845 (Harappa H2000-4484 Fig. 42.05) against what the rows say. Data: `evidence/tmp/032_002_861_603_slot_source_normalization/H360_*`, SEALS `H-360_*`. H-1845 has no image.
16. Glyph-form check of the 820 at M-1677 and M-1045 against terminal 820 rows; compare 705 and 706 on the same sign band for the 033 rows. Data: SEALS `M-1045_a.jpg`; M-1677 [blocked].
17. Direction-reversal reading of the nine empty-prefix 002-861-X rows (416, 698, 096). Takes: reverse strings and test against the frames. Data: LIPI.
18. Per-head polarity table for focus signs across all rows; strict-layer polarity test (125 vs non-125 with label shuffle within the strict layer); apply the four left-router cases (220-004, 390-004, 226-032, 205-032) across all governed rows; consolidated 125 tail parser on the full strict layer; terminal-governor counts with damaged slots counted and not counted; the 002 odds ratio on Harappa-only rows. Takes: scripts over LIPI. Data: LIPI, `research/docs/archive/campaign_032_002_861_002390x_risky_parse_model_v1_20260531.md`.
19. Check 390-004-002-817 against a second photo witness (only M-984 is source-visible); compare M-41 and Sktd-1 for 125 and 820 only; count glyphs on Sktd-1's top band. Data: SEALS `M-984_A.jpg`, `M-41_a.jpg`, `Sktd-1_a.jpg`.
20. Remove numeral tokens and 700 from every row and rerun the bidirectional test; test 407 opener against site-only and type-only nulls; 705 closers against 817/820 across the 499 rows; propagation run over the adjacency graph from the eleven rejected-anchor signs. Data: LIPI, `reports/`.

## 2. Reading direction and stored order

1. Rerun stored-order on L/R-only and R/L-only subsets; on Harappa TAB:B and TAB:I rows; on Mayig rows with a site split; on M77, CISI or ICIT; on Lothal split by source convention. Data: LIPI, `reports/direction_order_baseline_summary.json`, `research/data/open_prototype/mayig/records_index.csv`.
2. Remove H-1302, H-1303, H-1822 from the directionality set and recompute stored-win share; four-field object labels (face, image vs impression, transformation, proposed direction) for the Lipi direction field. Data: LIPI, `reports/h1302_h1303_source_provenance_gate_summary.json`.
3. Mirror-pair direction table and Daggumati and Revesz's mirror claim tested on any object. Data: `evidence/tmp/h1302_h1303_direction_prior_work/`, LIPI.
4. Nonlinguistic administrative or emblem baseline for the stored-order win; ten more synthetic admin streams at matched length to see whether any reaches 0.325865; terminal-class prediction after exact terminal signs are removed. Data: `research/data/open_prototype/nonlinguistic/sproat2014/`, LIPI.
5. New blind packet to the v2f standard (12 real sign-band negatives, 12 real nonlinguistic nulls, 32 fixed-seed synthetic nulls). Data: `evidence/tmp/effective_unicity_directionality_homogeneous_packet_v2f/`, `evidence/tmp/effective_unicity_directionality_signband_pool_v2e/`.
6. Stored-order metric definition: read "stored-win" in the linked directionality document; strict-filter LIPI to settle 4,011 vs 4,135 strict rows. Data: `research/docs/archive/`, LIPI.

## 3. Sign 034, 033, 700, short marks, tablets, H-series

1. Blind stroke and tine count on one packet: M-1206 terminal core, M-37 strict core, H-938 A and A bis, H-940 A, last sign of H-942 A, bar groups of H-789 B, H-930 B, H-942 B. Takes: count on the existing crops. Data: `evidence/tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/`, `evidence/tmp/independent_direction_controls/derived/`, SEALS.
2. Stroke count and height on the M-2104 034 side and M-478 004 side; blind segmentation of M-479 and M-480; stroke counts across the 00N and 03N codes as a count-to-code test; native-resolution stroke count on Marshall plate CXIV no. 532. Data: `evidence/tmp/cisi_m2104_packet/`, `evidence/tmp/m2104_raw_source/`, `evidence/tmp/marshall_vol3/`.
3. Count strokes in the high-resolution M-1584 mark (four full-height strokes would be the first direct pottery-tally count). Data: `evidence/tmp/m1584_cisi2/`; high-resolution scan [blocked, requested].
4. Pottery share of single-sign rows for 032, 033, 002, 700 (only 034 measured, 9 of 11); stroke-count test on the nine pottery 034 singles. Data: LIPI.
5. Co-occurrence over the full Lipi export: 110 with 415, 700 with 415, 034 with 700; count Lipi 167 and 137 and find their companions; check Lipi 110 as a short-side token. Data: LIPI, `reports/lipi_multiside_mark_rows.csv`.
6. Whether Lipi 034 and Mahadevan M034 are the same sign (Lipi 034 is a Wells number; Mayig cross-references M034 on P041). Data: `research/data/sign_crosswalk/p041_parpola41_namespace_table_20260712.csv`, `research/data/mahadevan_20260905/concordance_rows.csv`.
7. Remeasure the 309 eligible rows under one protocol; grow the 034 size-tier sample (margin interval -0.010581 to 0.134992 includes 0); size control within one dated deposit; dimension-bin tests inside SEAL:S, TAB:B, TAB:I; tablet-versus-seal split for every formula family; Harappa TAB:I copy-family audit to excavation numbers. Data: LIPI, `reports/frame700_034_size_tier_heldout_20260712_*`, `reports/lipi_frame700_subtype_rows.csv`.
8. Substitution test of 032, 033, 034 next to 700 in a source-normalized panel graph (full triad, cross-family); ordered-scale test of 032, 033, 034. Data: `research/docs/archive/lipi_frame700_034_source_panel_graph.md`, LIPI. Needs more source panels ([blocked] for some, CISI 3.1).
9. Physical side adjacency on triangular tablets; whether recurrent side marks correlate with side position, size, manufacturing group, find context; face-exclusivity of companion marks; plate check that row index equals physical face on H-353 and two others. Data: LIPI, SEALS (`H-352_*`, `H-353_*`, `H-354_*`), `reports/lipi_short_mark_companion_context_rows.csv`.
10. Mirror-variant collapse test on reversed companion marks (033 vs mirrored 034): H-2238 side 1 against H-2230 side 1; crop page 6 of the Nature article and compare with local strings; crosswalk the article's inline glyphs to Lipi strings. Data: `evidence/tmp/h1302_h1303_direction_prior_work/`; H-2230 and H-2238 images [blocked].
11. Higher-resolution Fig. 4 or source plates for all 22 H-series tablets; compare public A/B/C labels on H-2219 with CISI labels; image-side check of the H-2219 thumbnails; H-2218 to H-2239 side 2 and 3 stroke counts. Data: `reports/h2219_public_image_leads.csv`, `reports/h2218_h2239_public_image_lead_search.csv`. Fig. 4 PDF returned 403.
12. Validate side-mark structure of the mixed short-long and TAB:B/TAB:I core queues without the H-series template; companion-text sign-inventory gate (Parpola obverse recurrence mapping 415 and 016); source check of 154 vs 156 and 033 vs 034. Data: LIPI, `reports/lipi_multiside_mark_validation_queue.csv`.
13. Maker-mark comparison across manufacturing groups in the H-series; Mahadevan side-ordering criterion (find the written rule). Data: LIPI, `research/data/mahadevan_20260905/`.
14. Shape claim: do tablet shape and cross-section carry information (shape and cross-section columns exist). Data: LIPI.
15. Vats plate XCVI check of H-916 (object 12516) against local hook 12516456; Parpola 2019 triangular-prism check for H-352 to H-354. Data: `evidence/tmp/032_002_861_603_slot_source_normalization/vats_plates_contact_all/`, SEALS (`H-916_*`, `H-35[234]_*`), `evidence/tmp/pdfs/parpola_2019_bone_rods.pdf`.

## 4. Sign 41, 110, 415, 220 (fish, cup), 060

1. Open Vats plate XCVI objects 448 and 452 and mark which counter sign is the cup and which the fish (Lipi 220 lines up with Mahadevan 328 cup, Lipi 700 with 59 fish). Takes: look at one plate. Data: `evidence/tmp/032_002_861_603_slot_source_normalization/vats_plates_contact_all/p-200.png`, `research/data/decoding_followup_20260907/summary.json`.
2. Cup-and-fish swap null on Mahadevan; reverse cup count against physical volume or weight. Data: `research/data/mahadevan_20260905/concordance_rows.csv`.
3. Print-resolution images of M-37, H-938 A, H-940 A for the 220 fish family; plate check of the 520 position on M-126, M-37, M-73 (spear vs pincer); sort sign 60 vs 70 on the Fig. 5.1 crops; check 074 (H-2145 slot 1) and 016 (H-942 slot 3) on plates. Data: `evidence/tmp/parpola_sign60_local220_*_probe/`, `evidence/tmp/parpola_1994_signlist/rendered/`, SEALS.
4. Same-physical-side identity check for H-2148 against the local 110 row; blind comparison of H-2100, H-2152, Kanmer 4881.1 forms against H-940 B, the H-2147 right component, H-2148's one-sign panel; Kenoyer Fig. 14.1 against Parpola 1994 to fix the sign-41 numbering; route checks via RIHN 2012 Kanmer volume row "project08-1285". Data: `evidence/tmp/h2148_h2100_h2152_110_route/`, `evidence/tmp/h940_higher_res_route/`, `evidence/tmp/parpola_1994_signlist/`. Kanmer volume not on disk.
5. Parpola 107 test for 415: comb-ending of text 7 against terminal 415 on M-2109 and M-2111; Parpola's description of sign 107 vs Lipi 400. Data: `research/data/sign_crosswalk/source_panels/m77_text7_concordance/`, `evidence/tmp/pdfs/parpola_2019_bone_rods.pdf`.
6. 520-220-415 against 520-220-034 site by site (allograph split); split 520-220-415 rows by object shape and by slot before 220-415; direction-free component test for 034 and 415 on H-938 B and H-910 B. Data: LIPI, `evidence/tmp/h938_b_component_probe/`, `evidence/tmp/h910_component_probe/`.
7. Source-image check of H-1930 and M-855 to see whether 817 and 861 are one glyph or two; read 39 medial 861 rows and 10 medial 817 rows for neighbour identity; use the Brahmi v3 pre-review filter on 817 and 060 only; check the 920 leaf on the five P154-aligned positions. Data: SEALS `M-855_A.jpg`; H-1930 [blocked, Harappa H96-3049 Fig. 18.10]; LIPI; `research/data/brahmi/`.
8. Source-token crops of 527 and 061 (two or three more), then rerun the v2 Brahmi nulls. Data: `research/data/brahmi/source_token_crops_v2/`.
9. 740 register family against M-1669 and C-87 plate images; 158-806 Phyt support count against its floor note; 806 holdout token boxing; per-object 617 check on the 60 complete CISI rows. Data: `reports/`, Mackay PDF; M-1669 [blocked].

## 5. Crosswalks and sign identity

1. Crosswalk Lipi and Mayig through CISI rows that carry both a Lipi number and a P-number, replacing the unaccepted provisional edges. Data: `research/data/sign_crosswalk/crosswalk_edges.csv`, `research/data/open_prototype/mayig/records_index.csv`, LIPI.
2. Within-artifact shuffle null on the Lipi-to-Mayig alignment; Mayig P-to-V-to-W table from the 397 feature files to re-key any Mayig count to Parpola numbers; whether Mayig derived its Wells column from Lipi; align Mayig P144 and P126 to Lipi 031 and 006; non-unicorn Mayig material (all 179 records are Mohenjo-daro unicorn seals). Data: Mayig features, `reports/overlap_probe.csv`.
3. Mahadevan-to-Lipi object join through shared excavation numbers (Lipi side 5,147 rows). Data: `research/data/mahadevan_20260905/concordance_rows.csv`, LIPI.
4. Map the digital three-digit field codes (fs80 variants) to the 1977 codebook. Data: `evidence/tmp/cisi_xml/The Indus Script. Text, Concordance and Tables -Iravathan Mahadevan_djvu.txt`, `research/campaigns/integrated_20260906/completion/sources/`.
5. Find the class-code definitions (CISI, ICIT, Mahadevan, Wells/Fuls, upstream repo); rerun the class-code nulls at 1,000 iterations; cross-tabulate class codes against numeral tokens and 700; class prediction after removing under-threshold strata. Data: LIPI, `reports/lipi_class_field_audit_summary.json`, `reports/lipi_stratified_class_summary.json`.
6. Recover the other 405 publisher drawings of the 417 signs. Data: `research/campaigns/integrated_20260906/evidence_inventory/recovery_manifest.json`.
7. Yajnadevam allograph-group split. Data: `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/src/assets/data/allographs.csv`, `decipher.csv`.
8. Quarantined translation column: alignment count against sign rows, for autopsy only. Data: `research/data/quarantine/`.
9. Sign 12 and sign 104 (no assigned meaning) as standalone tests. Data: LIPI, concordance.

## 6. Photographs and source binding (take the photo, read the row)

1. Bind the 286 `no_valid_id` seal photos to catalogue numbers by reading their CISI/Vats pages. Data: SEALS `*_no_valid_id.jpg`, `evidence/tmp/cisi_pakistan_pages/cisi_pakistan.pdf`.
2. Bind Dholavira Acc. 8758 and 4237.1 to ZA-12:2 and to six-sign images; OCR the image-only seal-table pages; check item 10 at higher resolution to count the sign band. Data: `evidence/tmp/source_route_hunt_20260530/Dholavira-Bisht2015.pdf`, `dholavira_page18_item10_signband.png`.
3. Source images for M-240 (HR 4098324), M-1044 (HR 4399551), M-1728 (DK-E 1585079), M-1677 (DK11358130). Data: [blocked] archive images; M-240, M-1044 are in SEALS.
4. Orientation and side checks: H-1138; H-773 which side the CISI crop shows (741 window 0-75); M-32 and M-177 as impressions of one seal; H-2237 vs H-2233, H-366, M-102 vs M-132, H-1682; M-313 and M-316 for 390-034 patterns. Data: SEALS (`H-773_*`, `M-32_a.jpg`, `M-177_a.jpg`, `H-366_*`, `M-102_a.jpg`, `M-132_a.jpg`, `M-313_*`, `M-316_*`), `evidence/tmp/source_route_recheck_20260531/`.
5. Check M-41 status (2569.1) as a Mayig-aligned 002-405 row; resolve duplicate-family status of M-479 against CISI India n150 and rerun the 097 left-context Fisher test with M-479 counted once. Data: `evidence/tmp/002390x_390405_m34_m41_source_check_20260531/`, `evidence/tmp/cisi_m2104_packet/family_dependence/`.
6. Fuller Mayig/Parpola records for the six P0 Mohenjo-daro 034 objects; Mitchell 1986 no. 7 fig. 111, Parpola 1994 p. 131, Aruz and Wallenfels 2003 no. 301b for BM 120573. Data: Mayig features, Parpola 1994 PDF; the others [blocked].
7. Side-label notes for H-786 and H-941 from CISI 3.1 tables or HARP end matter; object records H-1521 to H-2583; CISI 3.1 HARP pages 207-360 and 423-441. [blocked] (paid).
8. Higher-resolution scan of the Bisht page 18 item 10 (count the sign band directly); H-1822 local row (its raw ID is 550). Data: `evidence/tmp/source_route_hunt_20260530/`, LIPI.
9. Library or interlibrary-loan route for CISI 3.1 and CISI 3.2/3.3 untraced objects (3335.1). [blocked]

## 7. External anchors: cuneiform, Gulf seals, Meluhha

1. Open the Shu-ilishu AO 22310 edition and run the object-level onomastic check; search cuneiform for other "interpreter of Meluhha" or Meluhhan names; search for a Meluhhan-Akkadian bilingual. Data: `research/data/meluhha/source_images/louvre_AO22310_shu_ilishu_de_clercq_plate9_no83.jpg`, `research/data/meluhha/cuneiform_attestations_expanded.csv`.
2. Matched non-Meluhha cuneiform controls for Dilmun, Magan, Marhasi, Elam, Gutium, Gubi, Susa. Data: `research/data/meluhha/control_toponyms.csv`, CDLI queries (no export on disk; fetch).
3. Join cuneiform Meluhha attestations to Indus records by site and period (no same-object join was found; site-and-period never tried). Data: `research/data/meluhha/meluhha_indus_join_surface.csv`, LIPI.
4. Meluhha surviving-phrase set (19 context leads, 23 query rows, 4 Ur/Susa/Failaka focus rows, 8 same-site length matches); synthetic same-site same-length forger control for the bridge test. Data: `research/data/meluhha/cdli_meluhha_context_leads.csv`, `research/data/meluhha/cdli_meluhha_context_lead_query_plan.csv`.
5. Gulf-type bridge objects: Kjaerum Failaka 279/319, Failaka 147.1 and 148.1, Amiet Susa 1643, Susa 3882.1 (Louvre SB 2425, AS 41, CCO S.299), Sarzec and Heuzey Girsu pl. 30.3a-b, Mitchell 1986 Ur figs. 106-117, Ur rows 3897.1, 5225.1, 5231.1, Ur grave lists PG 401 and PG 1847; map the 14 unmapped queue rows; Penn PMJ XXX:2 photo for U17649 against Gadd 16. Data: `research/data/meluhha/gulf_type_indus_external_queue.csv`, `evidence/tmp/gadd_ur/`. Catalogues [blocked].
6. BM 120573 (Diqdiqqah U.7683): read the Sumerian inscription for a name or title. Data: `research/data/meluhha/bm120573_object_bridge_audit.csv`.
7. Susa SB 5614 tablets 9537 and 9538: numeral stroke reading on the other faces. Data: `evidence/tmp/susa_3881_source_check/`.
8. Parpola SAA 2001 Fig. 1 for M-451 and test 906-388 as terminal boundary material; frame-reset control after 000. Data: LIPI; Parpola SAA 2001 [blocked]; SEALS `M-451_*`.
9. Mukhopadhyay 2023 administrative semasiography: whether tablet classes carry different formula families from seals. Data: LIPI type field.

## 8. Comparators and nulls

1. Indus under the Linear B source-gapped protocol; length-matched Linear B vs Indus gapped masked-sign test; masked-sign top-1 at Linear B's sign count (91); Linear B Series D as a training set for Indus gaps; Linear B length-matched to the Lipi length histogram. Data: `research/data/open_prototype/known_scripts/linear_b_series_d/Samples.txt`, LIPI.
2. SumTablets comparator with transliterations hidden and revision pinned (full 91,606-tablet set). Data: sample at `research/data/open_prototype/known_scripts/sumtablets/`; full set from Hugging Face.
3. Coptic SCRIPTORIUM continuity comparator as an upper bound. Data: fetch the corpus (none on disk).
4. Re-score Pictish stones with the stored-vs-reversed comparator; known-script comparator with artificial class labels. Data: `research/data/open_prototype/nonlinguistic/sproat2014/corpora/corpora/Pictish.xml`.
5. Nair 2026 scorecard (brevity, repeated formulae, hapax rate, positional rigidity) on the Lipi corpus; request the 1,916-inscription set and code (email for Cúper to send). Data: LIPI.
6. Check `hellosindh/indus-script-synthetic` for contamination before any model touches it. Data: Hugging Face.
7. Reproduce the subtype and leakage profiles on an authoritative corpus (CISI 3.1 or ICIT). [blocked]

## 9. Decoding, language and dictionary tests

1. Permutation null for the fish-square phonetic key (held matches never tested against chance); held-out dictionary run on a fresh held-out set; Sanskrit-dictionary key search rebuild. Data: `research/data/decoding_followup_20260907/summary.json`, `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/dev-tools/ashtadhyayi/assets/mw.xml`.
2. Transcribe Parpola 1994 Table 10.1 (Dravidian fish, star, glitter forms); get DEDR (free route: the online Digital DEDR at dsal.uchicago.edu). Data: `research/campaigns/integrated_20260906/evidence_inventory/parpola1994_table10_1_pdfindex199.png`.
3. Linear Elamite comparisons, Munda, Elamite and Sumerian loan lists run beside Dravidian and Indo-Aryan once a name slot is pinned. Data: none on disk; fetch lexicons.
4. Route D contextual allomorphy mechanism (`next_mechanism` in `research/campaigns/integrated_20260906/route_d/outputs/two_modifier_lattice.json`); companion-field prediction where spelling operation and production convention disagree; 1380/2452 picture difference (raw code 251 vs 13); 1177/3103 tick pair as a same-locality contrast; route B's 362/363 and 3315/3414 short-sign distinctions on source images. Data: `research/campaigns/integrated_20260906/route_a/`, `route_b/`, `route_d/`, `research/data/mahadevan_20260905/`.
5. Bhaskar S1 zoomorphic catalogue (on disk as xlsx, never opened): animal sign counts to test the fish and elephant readings. Data: `evidence/tmp/m1206_bhaskar/43539_2022_52_MOESM1_ESM.xlsx`.
6. Seven-route, 63-task plan in `research/publications/20260907/README.md`: overlapping spellings, geometry and compression, coordinated variation, copying and correction, pragmatics, relational language identification, conservation and arithmetic loops. None run. Data: LIPI, concordance.
7. Mahadevan 4x3 grid and radix algebra follow-ups (geometric comparison of reverse-face area vs stroke count in the four variable fronts). Data: `research/data/mahadevan_20260905/four_by_three_grid.json`.
8. Read the Parpola 2008 copper-type network against the 98 copper text-picture edges. Data: `research/campaigns/integrated_20260906/route_b/`.

## 10. Models, embeddings, compute

1. Pre-registered SLM runs at 0.89M (exists), 7M, 20M parameters with 5 seeds, plus 0.1 to 0.3M widths. Data: `slm/configs/ivc_research_14usd.json`, `research/data/slm/`. Colab.
2. Embedding recovery gate (`embeddings/validate_recovery.py`): stores not on disk and the model was never downloaded. Takes: build the stores, run the gate. Data: `embeddings/`.
3. Colab image scoring for sign 41 and 034. Data: crops in `evidence/tmp/h940_higher_res_route/`, `evidence/tmp/m1206_*`.
4. Row-hash comparison of the 3335 neighbourhood to list shifted pairs; reconcile the upstream commit b272ad99 with the current Lipi table (first differing byte 300). Data: `evidence/tmp/002390x_3335_yajnadevam_provenance_20260531/`.
5. Semantic-anchor prediction rerun with more iterations inside SEAL:S, TAB:B, TAB:I strata using sign-class blocks. Data: LIPI, `reports/lipi_stratified_class_summary.csv`.

## 11. Outreach (drafts for Cúper to send)

Requests logged as sent with no reply: Harappa/Fuls for H-1993; H-319 and H-1284; H-2240 and H-2241; M-1912; H-2237 and H-2238; Dholavira 8758; M-1825 (BJ 25710); 3335.1 (Yajnadevam author); all-side M-1206 (Harappa and Bhaskar); high-resolution M-1584. Not yet drafted: ICIT database access (administrator-gated), Nair 2026 code request.
