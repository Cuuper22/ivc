# Brahmi Shape-Descent Vector

Date: 2026-05-30

This directory contains adversarial Brahmi back-door datasets and null gates.

Source:

- Indoskript homepage: `https://www.indoskript.phil.uni-wuerzburg.de/`
- Manuscript index: `https://www.indoskript.phil.uni-wuerzburg.de/manuscripts`
- Letter tables: `https://www.indoskript.phil.uni-wuerzburg.de/letters/table/<manuscript_id>`

First gate generated files:

- `tools/build_indoskript_brahmi_shape_gate.py`: fetches early Brahmi glyph metadata/images, extracts shape features, compares Indus probes to Brahmi glyphs, and runs the random shape-evolution null.
- `indoskript_brahmi_manuscripts.csv`: 399 parsed Indoskript manuscript rows.
- `indoskript_brahmi_glyphs.csv`: parsed glyph rows from the first 12 early manuscripts at date <= -100, vocalization `a`.
- `indoskript_brahmi_features.csv`: glyph provenance, local cached image path, hashes, and basic shape metrics.
- `indus_shape_probe_features.csv`: local Indus source/canonical probe metadata and shape metrics.
- `indus_brahmi_nearest_neighbors.csv`: top 10 Brahmi nearest neighbors for each Indus probe.
- `brahmi_shape_descent_null_iterations.csv`: random shape-evolution nearest-neighbor iterations for actual Indus source probes.
- `brahmi_shape_descent_null_summary.json`: decision record.
- `indoskript_brahmi_fetch_log.csv`: URL/status/byte/hash fetch log.
- `indoskript_letter_images/`: cached Indoskript letter images used or acquired during the scrape. Indoskript states CC BY-NC-ND 4.0; treat this as local provenance-backed research cache, not a redistribution package.

Current result: no Brahmi descent line or phonetic anchor is accepted. The three local `220` source probes fail both family consistency and the random shape-evolution null: top-1 Brahmi labels are `kaṃ`, `o`, and `ka`, with null <= observed shares `0.576000`, `0.438000`, and `0.656000`. The local `110` source probe nearest-neighbor is `a`, with null <= observed share `0.666000`.

Second gate generated files:

- `tools/build_brahmi_source_token_descent_gate_v2.py`: expands the Brahmi side to 36 early manuscripts and compares exact projection-gap source-token crops against Brahmi glyphs.
- `indoskript_brahmi_features_v2.csv`: 1,342 early Brahmi glyph features.
- `source_token_descent_inventory_v2.csv`: 104 answer-key source rows considered; 61 pass exact projection-gap token count.
- `source_token_segments_v2.csv`: 611 source-token feature rows under direction-agnostic assignment policies plus legacy probes.
- `source_token_brahmi_neighbors_v2.csv`: top 10 Brahmi nearest neighbors for each source-token crop.
- `source_token_family_descent_summary_v2.csv`: 83 sign/orientation families with >= 2 samples; all fail shape or label nulls.
- `source_token_shape_null_iterations_v2.csv`: sampled random shape-evolution null iterations.
- `source_token_label_null_iterations_v2.csv`: sampled label-shuffle null iterations.
- `source_token_duplicate_collapse_audit_v2.csv` and `source_token_duplicate_collapse_audit_v2_summary.json`: skeptic audit for exact token-hash and CISI-level repetition in source-token families.
- `source_token_brahmi_descent_v2_summary.json`: decision record.
- `source_token_descent_fetch_log_v2.csv`: URL/status/byte/hash fetch log.
- `indoskript_letter_images_v2/` and `source_token_crops_v2/`: local research caches for provenance-backed reruns.

V2 result: no candidate-only row and no accepted phonetic anchor. The closest rows (`817=dhya`, `527=ra`, `472=ra`, `060=ka`, `061=ra`) all fail the pre-registered null gates. A duplicate-collapse audit adds another skeptic boundary: `817`, `472`, and `060` collapse below two unique token hashes, while `527` and `061` are single-CISI only. See `docs/brahmi_source_token_descent_gate_v2.md`.

Third gate generated files:

- `tools/build_brahmi_independent_source_token_gate_v3.mjs`: blocks v2 sign/orientation families before visual review unless they have at least three unique token hashes, three unique CISIs, three unique source paths, unanimity after duplicate collapse, unchanged modal label after collapse, and original shape/label null shares <= 0.01.
- `brahmi_independent_source_token_gate_v3.csv`: family-level independence and blocked-reason table.
- `brahmi_independent_source_token_gate_v3_summary.json`: decision record.

V3 result: all 83 v2 families are blocked before review. Review-packet eligible rows = 0, candidate-only rows = 0, accepted phonetic anchors = 0. The v2 near-misses are stopped at the independence floor: `817`, `472`, and `060` have one unique token hash and one CISI; `527` and `061` have two unique token hashes and one CISI. See `docs/brahmi_independent_source_token_gate_v3.md`.

Real-token impostor forger generated files:

- `tools/build_brahmi_real_token_impostor_forger_v3.mjs`: samples actual Indus source-token crops from other signs as impostor families, excluding the same CISI, source path, exact token hash, and assigned sign.
- `brahmi_real_token_impostor_forger_v3.csv`: family-level impostor-null results with v2 modal labels and v3 CISI-collapsed labels.
- `brahmi_real_token_impostor_forger_iterations_v3.csv`: sampled impostor iteration rows for audit.
- `brahmi_real_token_impostor_forger_v3_summary.json`: decision record.
- `tools/audit_brahmi_real_token_low_null_replacement_20260531.mjs`: replacement-branch low-null reaudit that does not read the quarantined `v3b` artifacts.
- `brahmi_real_token_low_null_reaudit_20260531.csv`: row-level low-null blocker taxonomy from the replacement run.
- `brahmi_real_token_low_null_reaudit_20260531_summary.json`: decision record for the 21 low-null rows from the replacement run.

Real-token result: no candidate-only row and no accepted phonetic anchor. Of 83 v2 families, 82 had full 1,000-iteration impostor runs, 61 had real-token impostor null share above `0.01`, 21 had null share at or below `0.01` but still failed v3 independence and v2 acceptance, and one legacy isolated-token family had an insufficient impostor pool. See `docs/brahmi_real_token_impostor_forger_v3.md`.

Replacement low-null reaudit result: the 21 low-null rows do not contain hidden survivors. All 21 fail the original shape-null threshold, 19 also fail the label-null threshold, 21 fail v3 preflight, 11 fail minimum source-token independence, 14 fail duplicate-collapse unanimity, and no row passes both minimum independence and duplicate-collapse unanimity. See `docs/brahmi_real_token_low_null_reaudit_20260531.md`.
