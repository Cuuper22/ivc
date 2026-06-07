# Directionality Visual Preflight Failures

Date: 2026-05-29

Status: failure ledger. Accepted claim increment: 0.

This note records why the v2c/v2d directionality source-normalization path still cannot be reviewed or scored as a blind packet.

## v2c

v2c fixed the DjVu OCR parser bug: five-value `WORD coords` are `x1,y1,x2,y2,baseline`, not polygon points. That repair was real, but it did not make the packet reviewer-ready. Human visual preflight of `tmp/effective_unicity_directionality_blind_packet_v2c/directionality_no_overlay_v2c_blind_contact_sheet.png` found remaining printed catalogue/page cues, including `H-662 a`, `H-158 A`, `M-1315 A`, `M-171 A`, `M-365 A`, and `M-386 A`-style labels in routed real-negative neighborhoods.

Decision: reject before review. There is no meaningful reviewer false-positive rate for v2c because the blind condition failed.

## v2d

The cleaned v2d shortlist removes the most obvious first-draft leaks, but it is still not a packet:

- The real fixed denominator is 9, not 12. `H-421`, `M-127`, and `M-1322` are still reserve rows in the CSV and may be promoted only in a new pre-registered manifest before review.
- Crop worlds are mixed. Targets are mostly signband strips, while controls include tablet/object panels, animal/icon context, and elephant/object context.
- Page-layout slivers remain visible in rows such as `H-654`, `M-1310`, `M-386`, and `M-1322`.
- `M-1310` target and `M-1315` control share source page `n202`; `M-1320` target and `M-1322` reserve share `n203`, so page-style leakage must be controlled in any future packet.

Decision: keep as a manual crop-QA draft only. It cannot produce a false-positive denominator.

## v2e

`data/open_prototype/tools/effective_unicity_directionality_signband_pool_v2e.py` widens the search to 38 public plate-route CISIs and emits 488 candidate crops. The geometry ranking is intentionally permissive and over-inclusive. The v2e contact sheets still contain visible labels, page slivers, and broad icon/object panels, so v2e is only a source pool for later manual visual QC.

## v2f

`data/open_prototype/tools/effective_unicity_directionality_homogeneous_packet_v2f_preflight.py` tests whether the v2e pool can be converted into a same-crop-world no-overlay packet. It fails before review.

- Strict v2e reuse has compact signband targets for `H-654`, `M-1310`, and `M-1320`, but not `M-811`.
- Strict reuse has only seven original fixed real-negative CISIs: `H-158`, `M-1315`, `M-171`, `M-365`, `M-386`, `M-525`, and `M-527`.
- Target/control source-page collisions remain: `M-1310` shares page `n202` with `M-1315` and `M-1314`; `M-1320` shares page `n203` with `M-1322`.
- The derived top-strip lane is acquisition only. It still misses `M-1320` and `M-811` before visual review, and it cannot create a false-positive denominator without a new fixed manifest and forger packet.

Decision: reject as a blind packet. Keep only as crop-acquisition and gate-failure evidence.

Main machine ledger: `data/open_prototype/reports/effective_unicity_directionality_visual_preflight_failures.csv`.
