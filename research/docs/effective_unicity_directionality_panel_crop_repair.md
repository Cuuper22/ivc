# Directionality Panel-Crop Repair

Date: 2026-05-29

Status: preflight inventory only. Accepted claim increment: 0.

## What This Note Is

This note records a repair effort on the image crops used by the directionality campaign — the workstream that tests whether Indus inscriptions really read in their recorded order. That campaign cannot advance without a blind packet: a bundle of seal-image crops shown to reviewers who cannot see the catalog answers. Several packet versions in a row (`v2b`, `v2c`, `v2d`, `v2e`, `v2f`) failed before review because the crops themselves gave the game away. This note explains why, and inventories the rebuilt crop pools.

Two terms recur below. The denominator is the fixed set of control crops — rows that should yield nothing — against which a reviewer's false-positive rate is measured; it is fixed before review and must never be shrunk afterwards. A crop world is the visual kind of a crop: a signband strip (the horizontal band of signs), an object panel, an animal/icon panel. Targets and controls must share one crop world, or their appearance alone tells a reviewer which is which.

## Root Cause

The v2b directionality packet failed after blind review because real denominator rows leaked catalogue/page labels. v2c fixed a concrete DjVu OCR parser bug: five-value `WORD coords` are `x1,y1,x2,y2,baseline`, not polygon points. The old parser treated the fifth value as a y-coordinate, creating tall bogus OCR boxes and unreliable masks.

That fix was necessary but not sufficient. v2c still cropped page context around catalogue labels and then tried to erase text. Human visual preflight found remaining printed labels and page-neighbor cues, so v2c is recorded as `v2c_packet_created_failed_visual_preflight_no_claim_promotion`.

## New Artifacts

- `data/open_prototype/tools/effective_unicity_directionality_public_route_probe_v2.py`: corrected public CISI OCR route probe.
- `data/open_prototype/reports/effective_unicity_directionality_public_route_probe_v2_summary.json`: 79 target rows, 93 route rows, 38 public plate-route candidates, one data/register-only route, 40 not found.
- `data/open_prototype/tools/effective_unicity_directionality_panel_crop_repair.py`: object-panel/signband crop candidate inventory with crop-world, denominator, OCR-overlap, and source-geometry fields.
- `data/open_prototype/tools/effective_unicity_directionality_panel_crop_shortlist_v2d.py`: reproducible cleaned-shortlist emitter; it records the visual-QC draft but does not create a blind packet or accepted denominator.
- `data/open_prototype/reports/effective_unicity_directionality_panel_crop_repair_v2_summary.json`: 278 candidate rows across 22 CISIs; 182 geometry-clean rows by OCR/label-box criteria; 21 of 22 automatic best rows geometry-clean; no row reviewer-ready from geometry alone.
- `data/open_prototype/reports/effective_unicity_directionality_panel_crop_repair_v2d_manual_shortlist_draft.csv`: first manual visual shortlist draft with 4 targets and 12 negative/reserve candidates; visual QC rejected several rows.
- `data/open_prototype/reports/effective_unicity_directionality_panel_crop_repair_v2d_manual_shortlist_clean_draft.csv`: cleaned manual shortlist draft with 4 targets, 9 fixed real-negative candidates, and 3 reserves after removing the visibly leaking/metadata-contaminated draft rows.
- `tmp/effective_unicity_directionality_panel_crop_repair/visual_qc_manual_shortlist_v2d_clean_draft.jpg`: visual QC sheet for the cleaned shortlist draft.
- `docs/effective_unicity_directionality_visual_preflight_failures.md`: explicit visual-preflight failure ledger for v2c, v2d, and the widened v2e pool.
- `data/open_prototype/reports/effective_unicity_directionality_visual_preflight_failures.csv`: row-level failure annotations naming the leaking labels, denominator problem, crop-world asymmetry, and page-layout cues.
- `data/open_prototype/tools/effective_unicity_directionality_signband_pool_v2e.py`: widened signband-like candidate-pool builder across 38 public plate-route CISIs.
- `data/open_prototype/reports/effective_unicity_directionality_signband_pool_v2e_summary.json`: 488 candidate rows; 4 target CISIs and 27 non-target CISIs have possible-or-strong signband-like geometry, but geometry alone is over-inclusive and not reviewer-ready.
- `data/open_prototype/tools/effective_unicity_directionality_homogeneous_packet_v2f_preflight.py`: homogeneous signband-strip packet gate for v2e reuse and derived top-strip acquisition.
- `data/open_prototype/reports/effective_unicity_directionality_homogeneous_packet_v2f_preflight_summary.json`: v2f failed preflight; no packet promoted and accepted claim increment remains 0.

## Current Preflight Result

The repair produced candidate crop inventories, not a result. The cleaned v2d shortlist has four target crop candidates, nine fixed real-negative candidates, and three reserve candidates after removing obvious first-draft leaks: the old `H-665` page-context crop with the visible `H-662 a` label, `M-525` metadata/handwriting contamination, and the `H-659` label leak. The retained `H-665` row is a different, tighter component candidate; it is not the rejected page-context crop.

The cleaned shortlist still fails packet preflight. The fixed denominator is 9, not 12, because reserve rows remain excluded until a new manifest promotes them before review. It also mixes crop worlds: target rows are mostly signband strips, while some controls are tablet/object panels or animal/icon panels. `data/open_prototype/tools/effective_unicity_directionality_signband_pool_v2e.py` widens the pool to find comparable signband-like rows, but that pool is also only a visual-QA surface.

The v2f homogeneous gate tests whether the widened v2e pool can honestly become a same-crop-world packet. It cannot. The strict reuse lane finds compact target strips for `H-654`, `M-1310`, and `M-1320`, but not `M-811`; under the same gate it has only seven original fixed real-negative CISIs and source-page collisions between `M-1310`/`M-1315`/`M-1314` on `n202` and `M-1320`/`M-1322` on `n203`. A derived top-strip lane is acquisition infrastructure only: it still misses `M-1320` and `M-811` before visual review, has six original fixed real-negative CISIs, and cannot produce an FPR — a false-positive rate — without a new blind packet.

The future v2f standard is now explicit: at least 12 fixed real signband-negative CISIs, at least 12 source-real nonlinguistic null crops, at least 32 fixed-seed synthetic nulls across matched texture/noise, asemic stroke, mirror/reversal, and shuffled/collage families, plus auxiliary sentinels that never count in the denominator. A null crop is a control image with no real inscription structure in it; a sentinel is a check row included to watch reviewer behaviour, never to prop up the denominator. Any hard or uncertain target-like/directional call on a denominator row fails the apparatus.

The next packet must not mix target signband strips with negative page panels. Every target and negative must share the same `crop_kind`, `crop_stage`, enhancement protocol, and comparable geometry. Any visible label, page-context cue, duplicate image hash, non-comparable crop, or target-like uncertainty in the fixed denominator fails the whole packet instead of shrinking the denominator.

## Interpretation Boundary

These artifacts validate no source order, physical direction, sign identity, sign meaning, phonetic value, language family, translation, or accepted structural claim. They only expose candidate crop pools and the exact failure mechanisms that a future blind packet has to survive.
