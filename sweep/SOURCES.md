# SOURCES: every raw source on disk in /home/claude/ivc

All paths are relative to `/home/claude/ivc` and were checked with ls/find on 2026-11-17. Where an old leads file said a source is missing and it is on disk (or the reverse), this file follows the disk. Corrections to the old notes are in the last section.

Short names used below: Lipi = the numeric catalogue of 5,679 rows (signs as three-digit numbers). Mayig = the P-code catalogue. CISI = Corpus of Indus Seals and Inscriptions. Mahadevan = the 1977 concordance. HARP = Harappa Archaeological Research Project.

---

## 1. Scanned books and excavation reports

Page counts from pdfinfo. "text" means a text layer or OCR text sits beside the PDF.

| Work | Path | Pages | Notes |
|---|---|---|---|
| CISI, Collections in Pakistan (PDF) | `evidence/tmp/cisi_pakistan_pages/cisi_pakistan.pdf` | 486 | Mohenjo-daro and Harappa plates. Leaf n### numbers in crop names are Internet Archive leaves. Page 480 render: `evidence/tmp/cisi_pakistan_pages/cisi_pakistan_pdf_page_480_for_xml_0479.png`. Data-page renders 477-479 and H-775 to H-945 enlargements: `evidence/tmp/cisi_pakistan_pages/data_h786_h941/` (9 PNG). |
| CISI Pakistan, OCR | `evidence/tmp/cisi_pakistan_ocr/pakistan_djvu.xml`; `evidence/tmp/cisi_xml/Corpus of Indus Seals and Inscriptions. Collections in Pakistan_djvu.txt` and `.xml`; `evidence/tmp/m1825_source_route_20260531/cisi_pakistan_djvu.txt`, `cisi_pakistan_djvu.xml`, `cisi_pakistan_scandata.xml` | n/a | Text layers. Used to find a leaf from an object number. |
| CISI, Collections in India (text only) | `evidence/tmp/cisi_xml/Corpus of Indus Seals and Inscriptions. Collections in India_djvu.txt` and `.xml` | n/a | No PDF of CISI India is on disk. Page images of it exist only as crops and single leaves (`cisi_india_n###` file names, for example `evidence/tmp/820_m314_source_pages/India_n113_w2000.jpg`, `evidence/tmp/861_suffix_source_routes/India_n129_w2000.jpg`, `evidence/tmp/m315_cisi1/`, and the 27 labelled CISI 1 panels under `research/data/sign_crosswalk/source_panels/`). |
| CISI Pakistan leaf, high resolution | `evidence/tmp/h940_higher_res_route/cisi_pakistan_n374_max.jpg`; `evidence/tmp/h940_higher_res_route/ia_jp2/cisi_pakistan_0374.jp2` | 1 leaf | H-939 and H-940, 600 dpi class. |
| CISI public-route page sets | `evidence/tmp/effective_unicity_directionality_public_route_probe/` (281 JPG); `evidence/tmp/effective_unicity_directionality_public_route_probe_v2/` (280 JPG); `evidence/tmp/002_y_branch_gap_public_source_acquisition/pages/` (65 page images) | 281 / 280 / 65 | Whole CISI pages pulled for the direction and 002-Y work. |
| Mahadevan 1977, The Indus Script: Texts, Concordance and Tables | `evidence/tmp/cisi_xml/The Indus Script. Text, Concordance and Tables -Iravathan Mahadevan_djvu.txt` (674 KB) and `..._djvu.xml` (15 MB) | n/a | Full OCR, including Appendix II codebook. Page scans: `evidence/tmp/mahadevan_m77_pages/` (9 pages, PNG and JP2: 0066, 0084, 0093, 0101, 0254, 0324, 0491, 0617, 0683; 7 derived crops in `derived/`) and `evidence/tmp/mahadevan_m2104_pages/` (8 JPG: n66, n93, n101, n254, n324, n491, n617, n683). |
| Marshall, Mohenjo-daro and the Indus Civilization, vol. III | `evidence/tmp/marshall_vol3/` | 2 pages as scans (0114, 0205) plus full djvu XML | `48270_0114.png`, `48270_0205.png`, `48270_0205_iiif_full_max.jpg`, `48270_djvu.xml`, 15 derived crops of plate CXIV (objects 529-533) in `derived/`. Separate plate CXIV copies: `evidence/tmp/m2104_raw_source/marshall_plate_cxiv_529_533_originalpath.jpg`, `marshall_plate_cxiv_529_533_harappa_curl.jpg`, `blogspot_iv31.jpg`. |
| Vats, Excavations at Harappa, vol. II (text) | `evidence/tmp/032_002_861_603_slot_source_normalization/vats_excavations_at_harappa_vol2.pdf` | 520 | OCR beside it: `vats_vol2_djvu.txt` (1.7 MB), `vats_vol2_djvu.xml` (23 MB). Contact sheets of pages 320-390 and 391-520 in the same folder (`vats_contact_pages_320_390/`, `vats_contact_pages_391_520/`). Archive metadata: `evidence/tmp/vats_vol2_archive_metadata.json`. |
| Vats, Excavations at Harappa, vol. II (plates) | `evidence/tmp/032_002_861_603_slot_source_normalization/vats_excavations_at_harappa_vol2_plates.pdf` | 288 | Every plate page rendered at `evidence/tmp/032_002_861_603_slot_source_normalization/vats_plates_contact_all/p-001.png` to `p-288.png`. Plate XCIV is p-196, XCVI is p-200, XCVIII is p-204. OCR: `vats_plates_djvu.txt`. 300 dpi renders: `vats_plate_XCIV_p196_300dpi-196.png`, `vats_plate_XCVIII_p204_300dpi-204.png`. |
| Vats vol. I | not on disk | | See section 8. |
| Mackay, Chanhu-daro Excavations 1935-36 | `evidence/tmp/chanhudaro_mackay_1943/chanhudaro_mackay_1943.pdf` | 466 | Text `chanhudaro_djvu.txt`; plate pages `plate-417.png`, `plate-418.png`, `plate420-417.png`, `plate420-418.png`; crops in `crops/`, `crops_final/`, `crops_high/`; crop manifests are the four CSVs in the folder (for example `crops/chanhudaro_c10_c60_c65_crops_manifest.csv`). Plates LI and LII hold the seals. |
| Parpola 1994, Deciphering the Indus Script | `evidence/tmp/parpola_1994_signlist/parpola_1994_deciphering_sindhilanguagelibrary.pdf` | 392 | Text `pages_60_90.txt`, `fig5_1_p70_71.txt`. Figure 5.1 sign-list pages rendered at `rendered/fig5_1-088.png` to `fig5_1-094.png`, sign 40-43 and sign 41 crops, and `rendered/parpola41_h2148_visual_comparison.png`. Tamil appendix pages and Table 10.1 renders: `research/campaigns/integrated_20260906/evidence_inventory/parpola1994_pdfindex296.txt` to `300.txt`, `parpola1994_compounds_pdfindex296.png`, `parpola1994_compounds_pdfindex300.png`, `parpola1994_table10_1_pdfindex199.png`, `parpola1994_pdfindex199.txt`. |
| Parpola 2019, inscriptions on the Harappan bone rods | `evidence/tmp/pdfs/parpola_2019_bone_rods.pdf` | 6 | Text `evidence/tmp/parpola_2019_bone_rods.txt`. Figure 1 text 12 crops: `evidence/tmp/pdfs/parpola_2019_fig1_text12_crop.png`, `..._crop2.png`, `..._crop3.png`, page render `parpola_2019_page2-2.png`. Text 7 (M-2109, M-2111) crops: `evidence/tmp/parpola_text7_scope_gate/derived/parpola2019_fig1_text_no7_m2109_m2111_crop.png`, `research/data/sign_crosswalk/source_panels/m77_text7_concordance/parpola2019_fig1_text7_m2109_m2111.png`. |
| Bisht 2015, Dholavira excavation report | `evidence/tmp/source_route_hunt_20260530/Dholavira-Bisht2015.pdf` | 115 | Text `Dholavira-Bisht2015.txt` (excerpt; about 20 pages carry no text layer, and the seal-table pages are image only). Page renders `dholavira_pages/` and `dholavira_pages_p14_22/`; page 18 items 9, 10, 11 whole and sign-band crops (`dholavira_page18_item9_whole.png`, `..._item10_signband.png`, and the rest of the six). |
| Kenoyer and Meadow 1997, Harappa 1995-96 | `evidence/tmp/h2147_source_route/kenoyer_meadow_1997_harappa.pdf` | 34 | Text `kenoyer_meadow_1997_harappa.txt`. H-2147 (H95-2514 Fig. 10.17) crops: `evidence/tmp/h2147_source_route/h2147_h95_2514_fig10_item17_crop.png` and 3 more, page renders `p-20.png` to `page-24.png`. 600 dpi page 20 and raw recrops: `evidence/tmp/h940_higher_res_route/h2147_kenoyer1997_page20_600dpi.png`, `evidence/tmp/h940_higher_res_route/derived/h2147_fig10_item17_*.png` (16), `evidence/tmp/h940_higher_res_route/pdfimages_h2147_p20/` (25 extracted images). |
| Kenoyer 2000, tiny steatite seals at Harappa | `evidence/tmp/h2148_h2100_h2152_110_route/kenoyer2000_tiny_steatite_seals_harappa.pdf` | 21 | Text `kenoyer2000_tiny_steatite_seals_harappa.txt`. |
| Kenoyer 2005, Harappa 2000-2001 | `evidence/tmp/h2148_h2100_h2152_110_route/kenoyer2005_harappa_2000_2001.pdf` (identical copy `curl_kenoyer2005.pdf`) | 19 | Text `kenoyer2005_harappa_2000_2001.txt`, `kenoyer2005_fig14_pages_17_18.txt`. Fig. 14 pages `kenoyer2005_page-16.png`, `kenoyer2005_page-17.png`, `kenoyer2005_page-18.png`; 21 Fig. 14 crops in `derived/` (H-2148 item 1, H-2100, H-2152). |
| Kenoyer and Meadow 2010, inscribed objects of Harappa | `evidence/tmp/h2148_h2100_h2152_110_route/kenoyer_meadow_2010_inscribed_objects_harappa.pdf` | 15 | Text `.txt` and `_layout.txt` beside it. |
| RIHN 2007, Indus Project report (Japanese) | `evidence/tmp/h2148_h2100_h2152_110_route/rihn_2007_indus_houkokusyo.pdf` | 234 | Text `rihn_2007_indus_houkokusyo.txt`. Source page: `evidence/tmp/820_rhin_source_pages/Pakistan_n160_w2000.jpg`. |
| Gadd 1932, Seals of ancient Indian style found at Ur | `evidence/tmp/gadd_ur/gadd_1932_33779.pdf` | 44 | Text layer is empty (44 bytes), so the page renders `evidence/tmp/gadd_ur/page-01.png` onward (34 PNG) are the readable copy. Also `gadd_first20.txt`. |
| Bhaskar 2022, IJHS 57(3) | `evidence/tmp/m1206_bhaskar/Bhaskar2022_IJHS_57_3_1.pdf` | 20 | Text `Bhaskar2022_IJHS_57_3_1.txt`. Fig. 3 (M-1206) crops in `derived/` (8). |
| Bhaskar, S1 zoomorphic icon catalogue (PDF and Excel) | `evidence/tmp/m1206_bhaskar/S1-IndusZoomorphicIconCatalogue.pdf` (12 pages; same file at `evidence/tmp/pdfs/S1-IndusZoomorphicIconCatalogue_20260531.pdf`); `evidence/tmp/m1206_bhaskar/43539_2022_52_MOESM1_ESM.xlsx` | 12 | Text `S1-IndusZoomorphicIconCatalogue.txt`. The Excel file is the same catalogue as a table; it has never been opened. |
| RMRL Bulletin No. 6 (June 2025) | `evidence/tmp/m1206_bhaskar/bulletin_No_6_June_2025.pdf` | 50 | Text `bulletin_No_6_June_2025.txt`; page renders `bulletin_page9-09.png`, `bulletin_page15-15.png`, `page18-18.png`. |
| Daggumati and Revesz 2021, allographs in undeciphered scripts | `evidence/tmp/h1302_h1303_direction_prior_work/daggumati_revesz_2021_allographs_nature_article.pdf` (copy `..._curl.pdf`) | 11 | HTML, text and page renders in `evidence/tmp/h1302_h1303_direction_prior_work/derived/pdf_pages/` (for example `nature_page-07.png`). |

---

## 2. Seal and tablet photographs

### 2a. The whole-seal photo cache (the only large photo set)

Folder: `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images/` (call it S below).

- 6,870 JPG, 202 MB. Copy of the Yajnadevam "lipi" web app image folder. Mapping from seal ID to files: `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/src/assets/data/seal_id_and_image_mapping.json` (3,318 seal IDs, 6,570 files; 300 files unmapped: 286 named `volN_page_N_seal_N_no_valid_id.jpg` and 16 duplicates).
- Name pattern: `<Object>_<Side>.jpg`, for example `M-478_A.jpg`, `H-938_A_bis.jpg`, `M-855_A.jpg`. Side is A, B, C, D, E, F or lower-case `a` (impression); `_bis` is a second photo of the same side.
- Counts by prefix: M (Mohenjo-daro) 3,166; H (Harappa) 2,177; L (Lothal) 472; K (Kalibangan) 196; Pk 122; C (Chanhu-daro) 94; B 56; Rhd 42; Mr 20; Sb 17; Kd 17; Ns 16; Ad 16; Dmd 15; G 14; others under 10 each (Skh, Nd, Jk, Trg, Sktd and more).
- H objects in the cache run H-1 to H-1019 only. Nothing from H-1020 up (H-1138, H-1930, H-1993, H-2147, H-2148 and so on) is in it.
- Third-party images of related surfaces, not independent objects.
- The 286 `no_valid_id` files are seal photographs with a page and seal number but no catalogue number. Each can be bound to a catalogue number by reading the page in CISI.

### 2b. Plate crops of seals and tablets (cut from CISI, Vats, Marshall, Mackay, Kenoyer)

All under `evidence/tmp/`. File counts in brackets.

- Tail and terminal work on 032-002-861 and 002-390-X: `002390x_390405_m34_m41_source_check_20260531/` (10), `002390x_390590032_family_recheck_20260531/` (4), `002390x_blind_boundary_packet/` (11), `002390x_h773_vats_side_guard_20260531/` (2), `002390x_intrinsic_sign_behavior_recheck/` (1), `002390x_m143_prefix_control_20260531/` (9), `002390x_source_normalization/` (32), `002390x_token_boundary_adjudication/` (15), `002390x_token_boundary_readiness/` (1), `032_002_861_220032_source_visible_contrast_packet/` (1), `032_002_861_220032_terminal_space_recut/` (1), `032_002_861_390004_exact_prefix_source_gate/` (1), `032_002_861_533717_blind_layout_gate/` (6), `032_002_861_533717_register_controls/` (23), `032_002_861_533717_source_family_independence/` (1), `032_002_861_603_graphic_identity_packet/` (18), `032_002_861_603_h1138_h360_tokenization_gate/` (15), `032_002_861_603_slot_source_normalization/` (526, Vats crops and contact sheets), `032_002_861_bare_edge_source_controls/` (21), `032_002_861_slot_control_source_routes/`, `032_002_861_source_first_terminal_space/` (1), `032_002_861_source_normalized_tail_predictor_packet/` (1), `032_002_861_source_token_attachment/` (7), `032_002_861_suffix_split/` (19), `032_002_861_terminal_space_blind_recut/` (2), `032_002_861_terminal_space_recut_v2/` (4), `032_002_branch_tail_source_acquisition/` (19), `032_002_branch_tail_token_order/` (5), `032_002_source_routes/` (3), `032_002_y_source_function_batch/` (42), `032_002_y_token_box_scaffold_v1/` (9), `3335_source_identity_recheck_20260531/` (5, CISI Pakistan n124-n126), `390004_exact_prefix_probe/` (65), `820_m314_source_pages/` (3), `820_rhin_source_pages/` (1), `861_suffix_source_routes/` (4), `002_y_branch_gap_blind_packet/` (29), `002_y_branch_gap_public_source_acquisition/` (196: 130 crops in `crops/`, 65 pages in `pages/`, one contact sheet).
- Blind packets (key files are not in the folder unless noted): `blind_060920_terminal_cap_20260531/` (13), `blind_741060920_terminal_cluster_20260531/` (13), `blind_806_prefix_series_20260531/` (13), `blind_boundary_packet_20260530/` (11), `blind_boundary_packet_alpha/` (11), `cisi_m2104_packet/` (43), `effective_unicity_directionality_blind_packet/` (44), `..._blind_packet_v2/` (91), `..._blind_packet_v2b/` (70), `..._blind_packet_v2c/` (70), `..._homogeneous_packet_v2f/` (103), `effective_unicity_m70_blind_packet/` (19), `source_box_blind_packet_v1/` (20), `source_box_negative_control_v2/` (19).
- Direction and component work: `effective_unicity_directionality_panel_crop_repair/` (964 files, object-panel and sign-band crops), `effective_unicity_directionality_signband_pool_v2e/` (978 files, 976 PNG crops across 38 CISI plate routes), `independent_direction_controls/` (17), `h910_component_probe/` (12), `h938_b_component_probe/` (6), `h940_higher_res_route/` (57), `h319_h1284_source_route_recheck/` (3), `h1302_h1303_cisi_public_route_check/` (2), `h2147_source_route/` (11), `h2148_h2100_h2152_110_route/` (35, 24 PNG crops of Kenoyer 2005 Fig. 14).
- M-1206, M-37, 034 and 220 work: `m1206_034_cohesion_gate/` (14), `m1206_034_next_source_normalized_blind_component_control_20260526/` (22, includes `blind_master_key.csv`), `m1206_034_terminal_component_gate/` (17), `m1206_m37_blind_visual_comparanda/` (45, includes `derived/verified_panel_crops/` with the H-938/H-939/H-940/H-941/H-942/H-786 panel crops), `m1206_m37_terminal_recut_gate/` (11), `m1206_singleton_controls/` (4), `m1206_source_normalized_component_packet/` (4), `m1206_terminal_triad_source_recheck/` (33), `m12_token_count_audit/` (13), `m1584_cisi2/` (17), `m2104_raw_source/` (19), `m315_cisi1/` (30), `m315_second_slot_controls/` (90, includes `blind_master_key.csv` files), `m685_cisi2/` (25), `m77_parpola_recurrence_gate/` (24, CISI India nos. 33 and 65-69), `parpola_sign60_local220_middle_probe/` (15), `parpola_sign60_local220_strict_probe/` (17), `parpola_text7_scope_gate/` (1).
- Risky-bet source checks: `risky_154806_series_prefix_source_probe_20260531/` (9), `risky_400740_source_visible_probe_20260531/` (7), `risky_740407590_source_probe_20260531/` (5).
- Route hunts: `source_route_hunt_20260530/` (18), `source_route_recheck_20260531/` (13; CISI Pakistan n358 H-773 A and B at 2400 px), `m1825_source_route_20260531/` (text only, no image of M-1825).
- Susa tablet SB 5614: `susa_3881_source_check/` (10 JPG: museum photos `SB5614_0000229537_OG.JPG`, `SB5614_0000229538_OG.JPG` and sign-band crops).
- Loose images at the top of the folder: `h654_r2_components_radius0.jpg` to `radius5.jpg`, `h665_route_boxes_debug.jpg`.

### 2c. Labelled CISI 1 panels and source witnesses (in the research data)

- `research/data/sign_crosswalk/source_panels/`: 63 PNG crops in 27 subfolders, one per crosswalk question (390_P086_merge, 740_P324, 817_861_P385_conflict, 002_P122_conflicts, 032_P145_conflict, m004, m007, m010, m020, m025, m041, m045, m072, m081, m098, m105, m106, m111, m120, m141, m161, m162, m77_text7_concordance, p000_damage_span_policy, damaged_boundary_fragment_closure, lipi_000_sign_bearing_policy, ambiguous_zero_overlap_policy). Each has a manifest. Example: `research/data/sign_crosswalk/source_panels/390_P086_merge/M-32_A_CISI1_pdf53_print17.png`.
- `research/data/mahadevan_20260905/source_witnesses/`: `H-306_A.jpg`, `H-306_B.jpg`, `Mahadevan_086.png`, `_087`, `_089`, `_095`, `_096`, `_103`, `_328`, `_342`, `_403`, `vats_553_555.png`, `manifest.json`.
- `research/data/brahmi/source_token_crops_v2/`: 303 files, single-sign crops from named seals (for example `M_70_B001_2_7d422dee267e4d5a.png`).
- `research/data/meluhha/source_images/louvre_AO22310_shu_ilishu_de_clercq_plate9_no83.jpg` with `.provenance.json`: the Louvre Shu-ilishu cylinder seal (AO 22310) image.

---

## 3. Plates and plate-like figures

- Vats vol. II plates XCIV, XCVI, XCVIII and all 288 plate pages: see section 1. Plate crops: `evidence/tmp/032_002_861_603_slot_source_normalization/H1138_Vats_Plate_XCIV_346_crop_tight.png` and 5 more of H-1138; `H360_Vats_Plate_XCVIII_584_full_labeled_crop.png`, `..._signband_crop.png`; `Vats_Plate_XCIV_344_348_row_crop.png`; `Vats_Plate_XCVIII_581_584_row_crop.png`; `H1846_H95_2672_Figure11_11_broad_crop.png` and 3 more (H-1846, Harappa report H95-2672 Fig. 11.11); `evidence/tmp/002390x_h773_vats_side_guard_20260531/Vats_Plate_XCIV_351_candidate_H773B_tight_from_v2.png`.
- Mackay plates LI and LII: in `evidence/tmp/chanhudaro_mackay_1943/` (section 1).
- Marshall plate CXIV (objects 529-533, including 532): `evidence/tmp/m2104_raw_source/` and `evidence/tmp/marshall_vol3/derived/`.
- Parpola 1994 Figure 5.1 sign list: `evidence/tmp/parpola_1994_signlist/rendered/`.
- Kenoyer 2005 Fig. 14 and Kenoyer and Meadow 1997 Fig. 10: see section 1.
- CISI plate pages: section 1.

---

## 4. Sign pictures and sign lists

- Publisher drawings of 12 of Mahadevan's 417 signs: `research/campaigns/integrated_20260906/evidence_inventory/recovered/glyph_059.png`, `glyph_060.png`, `glyph_065.png` to `glyph_073.png`, `glyph_211.png`. The inventory report says the other 405 can be recovered from the existing manifest: `research/campaigns/integrated_20260906/evidence_inventory/recovery_manifest.json`, `REPORT.md`.
- Mahadevan codebook pages: `research/campaigns/integrated_20260906/completion/sources/page_60.png`, `page_82.png`, `page_801.png`, `page_802.png`, with `original_ocr_extracts.json`, `1380_2452_adjudication.json`, `source_image_inventory.json`.
- Sign inventory tables: `research/data/sign_crosswalk/signs.csv`, `research/data/sign_crosswalk/sign_systems.csv`.
- Parpola sign list: `evidence/tmp/parpola_1994_signlist/rendered/fig5_1-088.png` to `fig5_1-094.png` (Figure 5.1, PDF pages 88-94), sign 41 crops, `research/data/sign_crosswalk/p041_parpola41_namespace_table_20260712.csv`.
- Brahmi letter pictures (IndoSkript, for the Indus to Brahmi shape comparison): `research/data/brahmi/indoskript_letter_images/` (580 files), `research/data/brahmi/indoskript_letter_images_v2/` (1,342 files); tables `research/data/brahmi/indoskript_brahmi_glyphs.csv`, `indoskript_brahmi_manuscripts.csv`, `indoskript_brahmi_features.csv`, `indoskript_brahmi_features_v2.csv`, `indus_shape_probe_features.csv`, `indus_brahmi_nearest_neighbors.csv`.
- Sign crops for the Brahmi source-token gates: `research/data/brahmi/source_token_crops_v2/` (303), `research/data/brahmi/source_token_segments_v2.csv`, `source_token_descent_inventory_v2.csv`.
- Bhaskar zoomorphic icon catalogue (animal sign counts): section 1.
- Mayig sign features, 397 JSON files, one per P-sign, with Wells numbers and descriptions: `evidence/tmp/mayig_feature_namespace_probe/repo/indus-valley-script-corpus-ad2f1e218a34b8c33c57de0d6cb8d99272765bbb/features/`. Single copies: `evidence/tmp/mayig_feature_fetch/` (P076, P091, P122, P145, P205, P378, P385), `evidence/tmp/p041_mayig_route/features__P041.json`, `evidence/tmp/mayig_feature_namespace_probe/features/` (22 files, P000 onward).
- Yajnadevam's own sign tables: `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/src/assets/data/decipher.csv`, `allographs.csv`, `symbol-frequency.json`.
- Mahadevan field-code sign definitions: Appendix II of the Mahadevan text (section 1); the link from the digital three-digit field codes to that codebook is not built.

---

## 5. Datasets, catalogues and crosswalk tables

### 5a. Inscription catalogues

| What | Path | Size |
|---|---|---|
| Lipi table, current | `evidence/tmp/lipi_current_inscriptions_20260526.csv` | 5,679 rows, 38 columns |
| Lipi, filtered working copy | `research/data/open_prototype/lipi/metadata_filtered.csv` | 5,679 rows, 35 columns (id, cisi, site, symbol, type, text, direction, dimensions, cross-section, sides, condition, class, excavation id) |
| Lipi, two copies and pinned commit | `evidence/tmp/002390x_3335_yajnadevam_provenance_20260531/inscriptions_current.csv`, `inscriptions_pinned_b272ad99.csv`, `github_commit_main_path.json` | same size |
| Lipi in the cloned app | `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/src/assets/data/inscriptions.csv` | 1.2 MB; differs from the top-level copy from byte 300 on |
| Lipi scope rows (readiness bucket, direction, text, class) | `research/data/open_prototype/reports/lipi_scope_rows.csv` | 5,679 rows; 2,887 numeric-clean |
| Mahadevan concordance, one row per sign occurrence | `research/data/mahadevan_20260905/concordance_rows.csv`; `concordance_documents.json.gz`; `paired_objects.json`; `front_families.json`; `four_by_three_grid.json`; `conditional_radix_algebra.json`; `scalar_counterexamples.json`; `summary.json` | 3,916 rows, 2,575 strict texts |
| Mayig record index (179 Mohenjo-daro unicorn-seal side records) | `research/data/open_prototype/mayig/records_index.csv`, `tree_manifest.csv`, `commit.json`, `sample_record.json`, `audit_summary.json` | 179 rows |
| Mayig corpus, full commit | `evidence/tmp/mayig_feature_namespace_probe/mayig_commit.zip` (328 KB) and extracted `repo/` (623 files at commit ad2f1e21) | 397 features |
| Yajnadevam "lipi" app, full clone | `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/` | 6,999 files, 568 MB; includes the git history in `_git_history/` |
| Campaign report tables | `research/data/open_prototype/reports/` | 2,032 files (CSV and JSON): every row table behind the notes, for example `campaign_032_002_post_y_all_002_rows.csv` (813 rows), `lipi_multiside_mark_rows.csv` (1,808), `lipi_short_mark_companion_context_rows.csv` (353), `lipi_frame700_subtype_rows.csv` (353), `lipi_multiside_mark_validation_queue.csv` (397) |
| Scripts for those reports | `research/data/open_prototype/tools/` | 342 files |
| Top-level campaign scripts | `evidence/tmp/run_032_002_861_*.py` and the other `run_*.py` (56), `evidence/tmp/make_032_002_y_token_boxes_v1.py` | |
| Open prototype overview | `research/data/open_prototype/README.md` | |
| SQLite build of the data | `db/ivc.sqlite`, `db/schema.sql`, `db/build_db.mjs` | |

### 5b. Known-script and non-writing comparators

- Linear B Series D: `research/data/open_prototype/known_scripts/linear_b_series_d/Samples.txt`.
- SumTablets (Sumerian transliterations): `research/data/open_prototype/known_scripts/sumtablets/sumtablets_line_sequences.csv`, `sumtablets_sample_rows.jsonl`, `sumtablets_source_manifest.json`. This is a sample; the full 91,606-tablet set is not on disk.
- Sproat 2014 non-linguistic sign systems (Indus bar seals, Pictish, Vinca, Kudurrus, totem poles, barn stars, weather icons, Asian emoticons): `research/data/open_prototype/nonlinguistic/sproat2014/corpora.zip`, extracted XML in `research/data/open_prototype/nonlinguistic/sproat2014/corpora/corpora/`, `sproat2014_extracted_sequences.csv`, `sproat2014_manifest.json`.

### 5c. Crosswalk tables between sign-numbering systems

- Lipi to Mayig P-code edges (189): `research/data/sign_crosswalk/crosswalk_edges.csv`, with `edge_pressure_summary.csv`, `evidence_refs.csv`, `namespace_gates.csv`, `artifact_witnesses.csv`, `audit_issues.csv`, `review_events.csv`, `manifest.json`, `README.md`, and per-edge gates `edge_00001_source_gate_20260712.json` to `edge_00005_source_gate_20260712.json`.
- Positional crosswalk candidates: `research/data/open_prototype/reports/crosswalk_lipi_to_mayig_candidates.csv`, `crosswalk_mayig_to_lipi_candidates.csv`, `crosswalk_alignment_pairs.csv`, `crosswalk_collision_summary.csv`, `crosswalk_high_frequency_sample.csv`, `crosswalk_summary.json`, `overlap_probe.csv` (179 Lipi-Mayig overlap rows).
- Parpola 41 / Mayig P041 / Lipi 110: `research/data/sign_crosswalk/p041_parpola41_namespace_table_20260712.csv`.
- P385 (817 and 861) collision: `research/data/sign_crosswalk/p385_merge_collision_gate_20260712.json`. M-105 position concordance: `m105_source_position_concordance_20260712.csv`. M-77 text 7 object concordance: `m77_text7_object_concordance_20260712.csv`.
- Lipi variant pressure (154/156 and others): `research/data/open_prototype/reports/lipi_variant_crosswalk_pressure_pairs.csv`, `lipi_154_156_crosswalk_pressure.csv`.
- Mahadevan object numbers to Lipi object numbers: not built (the Lipi side has excavation numbers; the join is untried).
- Mahadevan field codes to the 1977 codebook: not built.

### 5d. Cuneiform and external-anchor tables

See 5e for the "cuneiform exports" detail. Tables on disk: `research/data/meluhha/` (73 files). Key ones: `cuneiform_attestations_expanded.csv` (16 expanded rows), `cuneiform_seed_attestations.csv`, `cuneiform_source_routes.csv`, `cuneiform_fetch_log.csv`, `cdli_current_meluhha_artifacts.csv`, `cdli_current_line_contexts.csv`, `cdli_meluhha_context_leads.csv`, `cdli_meluhha_context_lead_query_plan.csv`, `control_toponyms.csv`, `external_indus_objects.csv`, `gulf_type_indus_external_queue.csv` (22 Gulf-type rows, Laursen 2010 entries 6-27), `gadd_ur_accession_bridge_audit.csv`, `bm120573_object_bridge_audit.csv`, `failaka_kjaerum_acquisition_20260531.csv`, `meluhha_indus_join_surface.csv`, `object_level_onomastic_value_attempts.csv`, `external_phonetic_anchor_candidates.csv`, `susa_3881_sb5614_source_check_20260531.json`.

### 5e. Cuneiform exports

No CDLI or ETCSL text export and no full SumTablets set is on disk. What exists: the CDLI query results in `research/data/meluhha/` listed in 5d (Meluhha-related lines and artifacts only), the SumTablets sample in 5b, and the Kjaerum Failaka publication record `evidence/tmp/v1_external_acquisition_20260531/cdli_publication_1773730_kjaerum_failaka.json`.

### 5f. Other data folders

- `research/data/decoding_followup_20260907/summary.json` (fish-square, counter and held-out dictionary packet).
- `research/data/semantic_search_20260906/` (12 JSON files: coface candidates, fish context profiles, modifier ranking, repeat markers, graphic hypotheses).
- `research/data/slm/` (13 files: `ivc_from_scratch_scaling_20260712`, `ivc_transfer_exact_exposure_20260712`); code in `slm/`.
- `research/data/claim_ledger/claims.json` (retired ledger).
- `research/data/quarantine/` and `evidence/tmp/quarantine_bad_successor_20260531T0104/`: outputs of a broken run. Autopsy only.
- `research/campaigns/integrated_20260906/`: seven-route campaign, including `route_a/`, `route_b/` (46 published copper types from Parpola 2008 in `route_b/published_copper_type_network.json`, 19 relations in `copper_correspondences.json`), `route_c/`, `route_d/`, and `evidence_inventory/` (`tamil_compounds.json`, `tamil_compounds_relations.json`, `dravidian_lexical_examples.json`, 8 entries).
- Parpola 2008 copper-tablet paper: only its text pages `research/campaigns/integrated_20260906/evidence_inventory/parpola2008_pdfindex1.txt`, `parpola2008_pdfindex2.txt`, `parpola2008_pdfindex3.txt`. The PDF itself is not on disk.
- `research/extensions_20261001/` and `research/extensions_20261117/` (extension runs), `research/publications/20260907/`, `research/publications/20261001/` (papers), `research/docs/archive/` (422 notes), `research/docs/` (6 top-level notes).
- Acquisition manifests: `evidence/tmp/041_source_acquisition_20260611/sources_manifest.csv`, `claim_verification_ledger.csv`, `README.md`.
- Embeddings code (no store files): `embeddings/validate_recovery.py`. The two parquet stores it reads are not on disk.

---

## 6. Dictionaries and word lists

All inside the cloned Yajnadevam app, `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/`:

- Monier-Williams Sanskrit dictionary, full XML: `dev-tools/ashtadhyayi/assets/mw.xml` (67.6 MB; 283,809 records; 192,482 distinct headwords). This is the dictionary used by the fish-square and key-search runs in `research/data/decoding_followup_20260907/summary.json`.
- Monier-Williams, keyed JSON: `src/assets/data/mw.json` (903 KB), `src/assets/data/mw_redirects.json`.
- Verb roots: `src/assets/data/dhatu.json` (572 KB), `src/assets/vidyut/vidyut_dhatupatha_5.tsv` (57 KB), `dev-tools/ashtadhyayi/assets/data.json` (2,259 root rows), `dev-tools/ashtadhyayi/assets/dhatuforms_vidyut_shuddha_kartari.json`, `dhatuforms_vidyut_shuddha_krut.json`.
- Derivation records: `src/assets/data/prakriyas.json` (4 MB).
- Short glosses (Apte, Wilson, RV, Vaidya): `src/assets/data/lexicons.json`.
- Glossing lines for the claimed Indus text: `glossing.csv` (3,495 rows), `src/assets/data/translations.csv`, `words.csv`, `words_old.csv`, `words_temporarily_rejected.csv`, `synonym_groups.json`, `xlits.csv`, `unknown.txt` (Sanskrit-looking tokens), `keyboard-tests.csv`, `urls.csv`.
- Dravidian forms: Parpola 1994 Table 10.1 render and Tamil appendix pages (section 1), `research/campaigns/integrated_20260906/evidence_inventory/dravidian_lexical_examples.json`, `tamil_compounds.json`. No Dravidian Etymological Dictionary, no Munda, Elamite or Sumerian dictionary is on disk.

---

## 7. Photos by object

S = `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images/` (section 2a). "S: X" means file `S/X`. All other paths are full repo-relative. Every file name below was found by file-name search under `evidence/tmp`, `research/data` and `research/campaigns`.

### Objects you named

| Object | Image on disk |
|---|---|
| M-153 | S: `M-153_a.jpg`. No plate crop. |
| M-1112 | S: `M-1112_a.jpg`. No plate crop. |
| M-478 | S: `M-478_A.jpg`, `M-478_B.jpg`, `M-478_C.jpg`, `M-478_E.jpg`. Plate crops: `evidence/tmp/cisi_m2104_packet/crops/m478_a_inscription_crop.png`, `crops/m478_b_scene_crop.png`, `closeups/m478_a_u_count_closeup.png`, `overlays/m478_a_segmentation_overlay.png`, `family_dependence/cisi_india_n150_m478_m480_plate_cluster_crop.png`, `family_dependence/cisi_india_n835_m478_m481_data_rows_crop.png`, `m479/cisi_india_n19_m478_m479_pot_context_crop.png` (all inside `evidence/tmp/cisi_m2104_packet/`). |
| M-2104 | Not in S. Marshall plate CXIV (objects 529-533, no. 532 is the M-2104 family): `evidence/tmp/m2104_raw_source/marshall_plate_cxiv_529_533_originalpath.jpg`; crops `evidence/tmp/m2104_raw_source/derived/m2104_marshall_532_crop_overlay.png` (15 files in `derived/`); `evidence/tmp/marshall_vol3/48270_0205.png` and 15 crops in `evidence/tmp/marshall_vol3/derived/` (for example `m2104_ia_48270_0205_no532_pair_rot90_enhanced4x.png`). Parpola 2019 Figure 1 text 12: `evidence/tmp/cisi_m2104_packet/crops/m2104_parpola_fig1_text12_crop.png`, overlay `evidence/tmp/cisi_m2104_packet/overlays/m2104_parpola_fig1_text12_segmentation_overlay.png`. Mahadevan pages: `evidence/tmp/mahadevan_m2104_pages/`. Related family: M-479 (S: `M-479_A.jpg`, `M-479_B.jpg`; crops in `evidence/tmp/cisi_m2104_packet/m479/`), M-480 (S: `M-480_a.jpg`, `M-480_b.jpg`; crops in `evidence/tmp/cisi_m2104_packet/crops/m480_a_inscription_crop.png`), M-1425 (S: `M-1425_a.jpg`, `M-1425_E.jpg`; `evidence/tmp/cisi_m2104_packet/crops/m1425_a_inscription_crop.png`). |
| H-2147 | Not in S. Kenoyer and Meadow 1997 Fig. 10 item 17: `evidence/tmp/h2147_source_route/h2147_h95_2514_fig10_item17_crop.png`, `h2147_h95_2514_fig10_item17_context_crop.png`, `h2147_h95_2514_fig10_17_table_row_crop.png`; `evidence/tmp/h940_higher_res_route/derived/h2147_fig10_item17_raw_fullrow_recrop.png`, `h2147_fig10_item17_face_raw_recrop.png`, `h2147_fig10_item17_left_component_raw_recrop.png`, `h2147_fig10_item17_right_component_raw_recrop.png` (16 files in `derived/`); 600 dpi page `evidence/tmp/h940_higher_res_route/h2147_kenoyer1997_page20_600dpi.png`; side-by-side sheet with H-940 and H-2148: `evidence/tmp/h2148_h2100_h2152_110_route/derived/h940_h2147_h2148_110_branch_neutral_precheck_sheet.png`. |
| H-2148 | Not in S. Kenoyer 2005 Fig. 14 item 1: `evidence/tmp/h2148_h2100_h2152_110_route/derived/h2148_kenoyer2005_fig14_item1_context_crop.png`, `h2148_kenoyer2005_fig14_item1_left_single_panel_crop.png`, `h2148_kenoyer2005_fig14_item1_right_three_sign_panel_crop.png`, `h2148_kenoyer2005_fig14_full_crop.png` (21 files in `derived/`); pages `evidence/tmp/h2148_h2100_h2152_110_route/kenoyer2005_page-16.png`, `kenoyer2005_page-17.png`, `kenoyer2005_page-18.png`; Parpola 41 comparison `evidence/tmp/parpola_1994_signlist/rendered/parpola41_h2148_visual_comparison.png`. The same Fig. 14 crops cover H-2100 and H-2152. |
| H-1930 | No image on disk. Lipi row 771.1/771.2, Harappa report figure H96-3049 Fig. 18.10. Not in S (S stops at H-1019). Not in any crop folder. |
| M-855 | S: `M-855_A.jpg`. No plate crop. |
| Vats plate XCVI, objects 448 and 452 | Whole plate: `evidence/tmp/032_002_861_603_slot_source_normalization/vats_plates_contact_all/p-200.png` (plate XCVI; 448 is in the fourth row of three above the 452 row; the plate is 40 dpi class, so the PDF page is the sharper copy: `evidence/tmp/032_002_861_603_slot_source_normalization/vats_excavations_at_harappa_vol2_plates.pdf`, page 200). Lipi rows: H-912 and H-1191 share excavation ref `8650c448`; H-1192 is `8650c452`. S has H-912: `H-912_A.jpg`, `H-912_B.jpg`, `H-912_A_bis.jpg`, `H-912_B_bis.jpg`. S has no H-1191 or H-1192. |

### Other objects the leads files say need a photo check

Objects with only a cache photo list the S files. "none" means no image anywhere on disk.

| Object | Image on disk |
|---|---|
| M-1584 | CISI Pakistan leaves: `evidence/tmp/m1584_cisi2/n267_w2000.jpg`; sign close-up `evidence/tmp/m1584_cisi2/derived/n266_m1584_sign_close_2x.png` (12 files in `derived/`). Not in S. |
| M-315 | S: `M-315_a.jpg`. Crops: `evidence/tmp/m315_cisi1/n113_w2000.jpg`, `evidence/tmp/m315_cisi1/derived/m315_page78_header_context.png`, `evidence/tmp/m315_second_slot_controls/derived/preblind_token2_crops/M-315_upper_face_034_candidate.png`. |
| M-685 | S: `M-685_a.jpg`. Crops: `evidence/tmp/m685_cisi2/n71_w2000.jpg`, `evidence/tmp/m685_cisi2/derived/m685_face_signs_close_gray_autocontrast.png`. |
| M-1206 | S: `M-1206_a.jpg`, `_A4CF_100_`, `_AE`, `_B`, `_C`, `_D`, `_E`, `_F`, `_e_1_` (9 files, `M-1206_<suffix>.jpg`). Crops: `evidence/tmp/m1206_terminal_triad_source_recheck/`, `evidence/tmp/m1206_bhaskar/derived/m1206_fig3_signs_close.png`, `evidence/tmp/m1206_034_cohesion_gate/derived/`, `evidence/tmp/m1206_034_terminal_component_gate/derived/`. |
| M-37 | S: `M-37_a.jpg`. Crops: `evidence/tmp/m1206_m37_terminal_recut_gate/derived/m37_terminal_recut_contact_sheet.png`, `evidence/tmp/m1206_terminal_triad_source_recheck/derived/m37_A_full_displaycoords.png`, `research/data/sign_crosswalk/source_panels/m77_text7_concordance/cisi1_pdf55_print19_m35_m37.jpg`. |
| M-126, M-73 | S: `M-126_a.jpg`, `M-73_a.jpg`. Panels: `research/data/sign_crosswalk/source_panels/p000_damage_span_policy/M-126_A_a_CISI1_pdf78_print42.png`, `.../M-73_A_a_CISI1_pdf68_print32.png`. |
| H-938 | S: `H-938_A.jpg`, `H-938_A_bis.jpg`, `H-938_B.jpg`. Crops: `evidence/tmp/h938_b_component_probe/` (6), `evidence/tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H938_A_bis_panel.png`, `evidence/tmp/independent_direction_controls/derived/H938_B_source_panel.png`. |
| H-939, H-940, H-941, H-942, H-786 | S: `H-939_A.jpg`, `_A_bis`, `_B`, `_B_bis`; `H-940_A.jpg`, `H-940_B.jpg`; `H-941_A.jpg`, `_A_bis`, `_B`, `_B_bis`; `H-942_A.jpg`, `H-942_B.jpg`; `H-786_A.jpg`, `H-786_B.jpg`. Panels: `evidence/tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/` (`H940_A_panel.png`, `H941_B_bis_panel.png`, `H939_B_bis_panel.png`, `H786_A_panel.png`); high-resolution H-940: `evidence/tmp/h940_higher_res_route/derived/h940_b_panel_no_label_from_iiif_max.png`; H-942: `evidence/tmp/m1206_singleton_controls/derived/h942/H942_A_signband_from_cisi_pakistan_n374.png`. |
| H-910, H-930, H-789 | S: `H-910_A.jpg`, `H-910_B.jpg`; `H-930_A.jpg`, `H-930_B.jpg`; `H-789_A.jpg`, `H-789_B.jpg`. Panels: `evidence/tmp/h910_component_probe/` (12), `evidence/tmp/independent_direction_controls/derived/H930_B_source_panel_v2.png`, `H789_B_source_panel_v2.png`, `evidence/tmp/independent_direction_controls/cisi_pakistan_n359_h789_w2000.jpg`. |
| M-1825 | none (no image anywhere on disk; the route folder `evidence/tmp/m1825_source_route_20260531/` holds only OCR text). Source: CISI 3.1 or museum BJ 25710. |
| Sktd-1 | S: `Sktd-1_a.jpg`. Crops: `evidence/tmp/002390x_source_normalization/Sktd1_impression_a_full_panel.jpg`, `evidence/tmp/002390x_token_boundary_adjudication/N005_Sktd1_boxed.jpg`. |
| H-1993, H-1803 | none. Source: Harappa report H96-2769 Fig. 17.07 and CISI 3.1 photo pages 207-360. |
| M-119, M-735, M-70, M-71 | S: `M-119_a.jpg`, `M-119_B.jpg`; `M-735_a.jpg`; `M-70_a.jpg`; `M-71_a.jpg`. Crops: `evidence/tmp/002390x_source_normalization/M119_impression_a_full_panel.jpg`, `M735_face_A_signband.jpg`, `M71_impression_a_signband.jpg`; boxed versions `evidence/tmp/002390x_token_boundary_adjudication/N001_M119_boxed.jpg` to `N004_M71_boxed.jpg`; M-70: `evidence/tmp/032_002_branch_tail_source_acquisition/M70_impression_a_signband_from_cisi_india_n066.png`, `evidence/tmp/effective_unicity_m70_blind_packet/m70_blind_token_box_contact_sheet.png`. |
| M-41, M-34 | S: `M-41_a.jpg`; `M-34_a.jpg`, `M-34_a_bis.jpg`. Crops: `evidence/tmp/002390x_390405_m34_m41_source_check_20260531/M41_A_signband_x2.jpg` (10 files), `research/data/sign_crosswalk/source_panels/m041_middle_fish_omission/M-41_A_a_CISI1_pdf57_print21.png`, `research/data/sign_crosswalk/source_panels/390_P086_merge/M-34_A_CISI1_pdf54_print18.png`. |
| M-1750 | none. Source: CISI Pakistan sequence after M-1658 (M-1658 is in S: `M-1658_A.jpg`, `_A_bis`, `_B`, `_B_bis`, `_F`). |
| M-240, M-91 | S: `M-240_a.jpg`, `M-91_a.jpg`. Crops: `evidence/tmp/032_002_branch_tail_source_acquisition/M240_face_A_signband_from_cisi_india_n095.png`, `M91_face_A_signband_from_cisi_india_n071.png`, token-order overlays in `evidence/tmp/032_002_branch_tail_token_order/`, `evidence/tmp/032_002_861_source_token_attachment/`. |
| H-444, M-723, M-1044 | S: `H-444_a.jpg`, `M-723_a.jpg`, `M-1044_a.jpg` (also `M-1043_a_M-1044_A.jpg`). Bare-edge overlays: `evidence/tmp/032_002_861_bare_edge_source_controls/H444_bare_edge_overlay.png`, `M723_bare_edge_overlay.png`, `M1044_bare_edge_overlay.png`. |
| H-55 | S: `H-55_a.jpg`. Crops: `evidence/tmp/390004_exact_prefix_probe/crops3/H55_A_panel_correct_enhanced.jpg`, `evidence/tmp/032_002_861_390004_exact_prefix_source_gate/campaign_032_002_861_390004_exact_prefix_source_gate_H55_source_contact_sheet.jpg`. |
| H-773 | S: `H-773_a.jpg`, `H-773_b.jpg`. Crops: `evidence/tmp/source_route_recheck_20260531/cisi_pakistan_n358_h773_A_signband_tight_w2400.jpg`, `cisi_pakistan_n358_h773_B_full_w2400.jpg`; Vats XCIV 351: `evidence/tmp/002390x_h773_vats_side_guard_20260531/Vats_Plate_XCIV_351_candidate_H773B_tight_from_v2.png`. |
| C-57, C-87 | none in S or crops. Chanhu-daro plates LI and LII are in the Mackay PDF; crops of C-10, C-60, C-65 only (`evidence/tmp/chanhudaro_mackay_1943/crops/`). |
| M-623 | S: `M-623_A.jpg`, `M-623_C.jpg`, `M-623_D.jpg`, `M-623_a_iE.jpg`. |
| M-1188, M-1954, M-1973, M-1677, M-1728, M-1912, M-1669 | none. (M-1045 is in S: `M-1045_a.jpg`.) Source for M-1677, M-1728, M-1825: CISI 3.1. |
| H-1138 | none in S. Vats plate XCIV no. 346 crops: `evidence/tmp/032_002_861_603_slot_source_normalization/H1138_Vats_Plate_XCIV_346_crop_tight.png`, `..._crop_wide.png`, `..._full_labeled_crop.png`, `..._signband_upper.png`, `..._reverse_lower.png`, `..._source_panel.png`; plus `evidence/tmp/032_002_861_603_graphic_identity_packet/` and `evidence/tmp/032_002_861_603_h1138_h360_tokenization_gate/`. |
| H-1137, H-1845 | none. H-1845 source: Harappa H2000-4484 Fig. 42.05. |
| H-1846 | none in S. Crops: `evidence/tmp/032_002_861_603_slot_source_normalization/H1846_H95_2672_Figure11_11_broad_crop.png` and 3 more; `evidence/tmp/032_002_861_603_graphic_identity_packet/H1846_harappa_603_source_context_unassigned_full_band.png`. |
| H-360 | S: `H-360_A.jpg`, `H-360_B.jpg`, `H-360_C.jpg`. Vats XCVIII no. 584: `evidence/tmp/032_002_861_603_slot_source_normalization/H360_Vats_Plate_XCVIII_584_full_labeled_crop.png`, `H360_Vats_Plate_XCVIII_584_signband_crop.png`. |
| H-355, H-933, H-960, H-233, H-352, H-353, H-354, H-916 | S only: `H-355_A.jpg`, `_B`, `_C`; `H-933_A.jpg`, `_B`; `H-960_A.jpg`, `_B`, `H-960_1_A.jpg`, `H-960_1_B.jpg`; `H-233_A.jpg`, `_B`; `H-352_A.jpg`, `_B`, `_C`; `H-353_A.jpg`, `_B`, `_C`; `H-354_A.jpg`, `_B`, `_C`; `H-916_A.jpg`, `_A_bis`, `_B`. |
| H-1302, H-1303, H-1822 | no object photo. Only article and CISI contents pages: `evidence/tmp/h1302_h1303_cisi_public_route_check/derived/cisi_pakistan_contents_page-006.png`, `evidence/tmp/h1302_h1303_direction_prior_work/derived/pdf_pages/nature_page-07.png`. |
| H-319, H-1284 | S: `H-319_A.jpg`, `H-319_B.jpg`. Register row: `evidence/tmp/h319_h1284_source_route_recheck/cisi_india_n406_h319_register_row_crop2.png`. H-1284: none beyond that register row. |
| H-2100, H-2152 | See H-2148 (same Kenoyer 2005 Fig. 14). |
| H-2145, H-2218 to H-2241 (H-series three-role tablets), H-1682, H-2233, H-2237, H-2240, H-2241 | none. Public thumbnails are only named in `research/data/open_prototype/reports/h2218_h2239_public_image_lead_search.csv` and `h2219_public_image_leads.csv`. |
| M-32, M-177, M-14, M-1, M-10, M-20, M-72, M-12 | S: `M-32_a.jpg`, `M-177_a.jpg`, `M-14_a.jpg`, `M-1_a.jpg` (+B,C,D), `M-10_a.jpg` (+B,C,D), `M-20_a.jpg`, `M-72_a.jpg` (+B,C,D), `M-12_a.jpg`. Panels in `research/data/sign_crosswalk/source_panels/` (for example `390_P086_merge/M-32_A_CISI1_pdf53_print17.png`, `817_861_P385_conflict/M-177_A_CISI1_pdf87_print51.png`, `m010_five_stroke_run/M-10_A_a_CISI1_pdf45_print9.png`, `m020_six_stroke_run_segmentation/M-20_A_a_CISI1_pdf49_print13.png`, `m072_five_stroke_run/M-72_A_a_CISI1_pdf67_print31.png`); M-12 audit: `evidence/tmp/m12_token_count_audit/M12_A_signband_source.png`. |
| M-102, M-132, M-313, M-316, H-366 | S: `M-102_a.jpg`, `M-132_a.jpg`, `M-313_a.jpg` (+B, F), `M-316_a.jpg` (+C, D), `H-366_A.jpg` (+B, C, E). |
| M-746, M-965, M-984, M-451, M-1452 | S: `M-746_a.jpg`, `M-965_a.jpg`, `M-984_A.jpg` (+`M-984_a_bis.jpg`), `M-451_A.jpg` (+B, C), `M-1452_A.jpg` (+B). Crops: `evidence/tmp/002390x_390590032_family_recheck_20260531/M746_pair_cisi_pakistan_n90_w2400_crop.png`, `M965_pair_cisi_pakistan_n128_w2400_crop.png`; `evidence/tmp/m315_second_slot_controls/derived/expanded_first3_context_crops/M-984_impression_a_390-004-002_control_clean_control.png`; `evidence/tmp/risky_740407590_source_probe_20260531/M-1452_A_x4_contrast.png`. |
| M-2109, M-2111 (bone rods) | none of the rods; only the Parpola 2019 Fig. 1 text 7 crop: `evidence/tmp/parpola_text7_scope_gate/derived/parpola2019_fig1_text_no7_m2109_m2111_crop.png`. |
| 3335.1 | none (private collection). Identity checks only: `evidence/tmp/3335_source_identity_recheck_20260531/`. |
| Dholavira 8758, 4237.1 | Bisht page 18 items 9-11: `evidence/tmp/source_route_hunt_20260530/dholavira_page18_item10_signband.png`, `..._item9_signband.png`, `..._item11_signband.png`. The seal-table pages for Acc. 8758 and 4237.1 are image only in the PDF. |
| Susa SB 5614 (9537, 9538) | `evidence/tmp/susa_3881_source_check/SB5614_0000229537_OG.JPG`, `SB5614_0000229538_OG.JPG`, `SB5614_9537_signband_object_tight.jpg`. |
| Ur and Gadd objects | Page renders of Gadd 1932: `evidence/tmp/gadd_ur/page-01.png` onward. |
| Shu-ilishu cylinder seal AO 22310 | `research/data/meluhha/source_images/louvre_AO22310_shu_ilishu_de_clercq_plate9_no83.jpg`. |

---

## 8. Paid or missing sources

| Source | Why it matters | Price | Free route named |
|---|---|---|---|
| CISI vol. 3.1, Mohenjo-daro and Harappa supplement (Parpola, Pande, Koskikallio, with Meadow and Kenoyer; Helsinki 2010; ISBN 978-951-41-1040-5; 504 pp.; HARP photo pages 207-360, data pages 423-441) | Photographs for H-1521 to H-2583 and M-1660 to M-2132: H-1993, H-1803, M-1825, M-1677, M-1728, M-1737, M-1763, M-1788, M-2104 identity bridge, the 03N and 00N stroke counts, about 11 objects in the source-route audit | EUR 70 for the book plus EUR 48.25 UPS to the USA, EUR 118.25 in total (Tiedekirja quote; invoice requested, nothing paid). No digital edition exists. The harappa.com page shows a Buy button and an Amazon US link with no price. | Finna lists nine Finnish libraries holding it. Ask one for a scan of pages 207-360 and 423-441 (interlibrary loan has not been requested). Details: `research/docs/archive/cisi31_access_acquisition_routes.md`. |
| Kjaerum, Failaka catalogue (nos. 279, 319), Mitchell 1986 (Ur figs. 106-117), Amiet 1972 no. 1643 and 1973 pl. 23a-b (Susa), Sarzec and Heuzey pl. 30.3a-b (Girsu), Gadd 1932 pl. I nos. 2-5, 17, 18 | Object-level bridges for the Gulf-type rows in `research/data/meluhha/gulf_type_indus_external_queue.csv`; 14 of its 22 rows have no mapping | Not priced in the notes | Acquisition pages for Kjaerum are in `evidence/tmp/v1_external_acquisition_20260531/` (Aarhus University Press, CiNii, Open Library) and give no catalogue pages. Gadd 1932 is on disk (44 page images). |
| Vats, Excavations at Harappa vol. I | Vol. I seal crops (entry 14 of the leads) | Not priced | Not on disk. Vol. II is. Check the same Internet Archive source that supplied `evidence/tmp/vats_vol2_archive_metadata.json`. |
| CISI vol. 1 and 2 as PDF (India collection) | Only OCR text and single leaves are on disk; plate checks of M-series objects need leaves n54, n150, n181, n265-n267, n359, n372, n374, n406, n474, n837 | Free (Internet Archive) | Internet Archive scans of "Corpus of Indus Seals and Inscriptions" India volume (djvu text is already in `evidence/tmp/cisi_xml/`). |
| ICIT occurrence database (Wells sign list, ICIT numbers) | Independent text set, Wells primary sign list for W110, W034, W617, W821 | Not priced; access is administrator-gated (HTTP 401) | Mayig's copy of Wells numbers is on disk (397 feature files). An access request to the administrator is drafted in the notes for Cúper to send. |
| Singh et al. 2023 supplement ESM2 (harappa.com/sites/default/files/pdf/43539_2023_102_MOESM2_ESM.pdf) | ICIT 744 / H-1993 and related row identities | Free | Download returned 403; viewable on the web only. |
| Meadow and Kenoyer 2000 Figure 4 PDF | H-2218 to H-2239 side order | Free | Download returned 403; viewer only. |
| Bisht 2015 individual-seal list (PDFCoffee mirror) | Acc. 2118, 8758, 4237.1 dimensions and locus | Free | The Bisht PDF is on disk, but its seal-table pages are image only: OCR them. |
| Nair 2026 (arXiv 2604.17828) code and 1,916-inscription set | Independent text set and synthetic-baseline scorecard | Free on request | Email to the authors; Cúper sends. |
| Hugging Face `hellosindh/indus-script-synthetic` | Contamination check before using it | Free | Not downloaded; huggingface.co was blocked in an earlier environment. |
| Bhaskar 2022 Fig. 3 / S1 xlsx | Animal sign counts | Free | On disk (`evidence/tmp/m1206_bhaskar/43539_2022_52_MOESM1_ESM.xlsx`). |
| Parpola 2008 copper-tablet paper (PDF) | 46 copper types | Free | Only 3 text pages on disk (section 5f). |
| Parpola SAA 2001 PDF (M-451 Figure 1) | 906-388 boundary check | Free | Not on disk. |
| Kenoyer-Meadow HARP PDF excerpt; Penn Museum PMJ XXX:2 photograph of U17649 | Ur 002-004-415 check | Free / museum | Not on disk. |
| Dravidian Etymological Dictionary (DEDR) | Dravidian lexical test; the campaign cites DEDR numbers but holds no copy | Free route first | The Digital Dravidian Etymological Dictionary is online at the University of Chicago DSAL site (dsal.uchicago.edu). |
| Full SumTablets (91,606 tablets) and CDLI/ETCSL exports | Second comparator, cuneiform name searches | Free | Hugging Face dataset with the revision pinned; CDLI bulk export. Neither is downloaded. |
| Wells primary sign tables | Wells numbers outside Mayig | Not priced | Not on disk. |
| Museum and holder photographs requested by email, no reply logged | H-1993 (Harappa/Fuls), H-319 and H-1284, H-2240 and H-2241, M-1912, H-2237 and H-2238, Dholavira 8758, M-1825 (BJ 25710), 3335.1 (Yajnadevam author), all-side M-1206, high-resolution M-1584 mark | | Requests are in `research/docs/archive/source_access_requests.md`. |
| Embedding stores `embeddings/store_images.parquet`, `store_text.parquet` | `embeddings/validate_recovery.py` | | Not on disk. |
| CISI vol. 3.2 and 3.3 (untraced objects) | 3335.1 | Not priced | Not checked. |

---

## 9. Corrections to the old leads notes (the disk wins)

- Said missing, on disk: Kenoyer 2005 (`evidence/tmp/h2148_h2100_h2152_110_route/kenoyer2005_harappa_2000_2001.pdf`); Parpola 2019 bone rods PDF and text; the CISI Pakistan PDF; Mahadevan 1977 text and page scans; the Louvre AO 22310 image (`research/data/meluhha/source_images/`); the Bhaskar S1 Excel file; `evidence/tmp/` as a whole (old notes cite `tmp/...`; the real root is `evidence/tmp/`).
- Said on disk, not found: `Parpola_2008_copper.pdf` (the leads place it in `research/campaigns/integrated_20260906/evidence_inventory/recovered/`; only 12 glyph PNGs are there); the DAINST Gulf-Indus reference PDF (not in `evidence/tmp/v1_external_acquisition_20260531/`); `research/data/non-linguistic-symbols/corpora.zip` (use `research/data/open_prototype/nonlinguistic/sproat2014/corpora.zip`); a separate `data/brahmi/` (it is `research/data/brahmi/`).
