# Brahmi Source-Token Descent Gate v2

Date: 2026-05-30

This is the second descendant-script back-door attempt. The first gate compared a handful of local source/canonical probes against early Brahmi. This v2 gate instead tokenizes source-image crops from already-built blind-packet answer keys, compares the resulting Indus token crops to early Brahmi glyphs, and runs both shape and label nulls before allowing even a candidate-only descent line.

It produces no accepted descent line, no phonetic value, and no candidate-only row.

## Source Surface

Brahmi side:

- Source: `https://www.indoskript.phil.uni-wuerzburg.de`
- Date filter: manuscripts dated `<= -100`
- Early manuscript limit: 36
- Parsed Brahmi glyph rows retained: 1,342
- Output: `data/brahmi/indoskript_brahmi_features_v2.csv`

Indus side:

- Source rows came only from existing answer-keyed source crops in `data/open_prototype/reports/*answer_key.csv`.
- Synthetic rows were excluded before tokenization.
- A source crop was admitted only if projection-gap segmentation recovered exactly the catalog token count.
- Both visual-left-to-right catalog order and visual-left-to-right catalog reverse assignments were emitted, so the gate did not assume a direction.
- Legacy isolated source-token probes for local `220` and `110` were retained as hostile continuity checks.

Counts:

| Quantity | Count |
| --- | ---: |
| Source answer-key rows considered | 104 |
| Rows with exact projection-gap count | 61 |
| Source-token feature records | 611 |
| Source-token segment rows | 611 |
| Sign/orientation families with >= 2 samples | 83 |

## Forger / Nulls

Each sign/orientation family had to clear two independent gates:

1. Shape-evolution null: for each token sample in a family, generate 200 random perturbations and compare them to the same 1,342-glyph Brahmi feature set.
2. Label-shuffle null: for each family, shuffle Brahmi labels 1,000 times over the observed nearest-glyph positions.

The pre-registered survival rule was intentionally harsh:

```text
>= 2 samples
100% modal Brahmi-label agreement
shape null <= 0.01
label null <= 0.01
```

Even then, a survivor would only become `candidate_only_requires_manual_visual_descent_review`, not an accepted phonetic anchor.

## Results

All 83 tested sign/orientation families failed. Candidate-only rows: 0. Accepted phonetic anchors: 0.

Top near-misses, sorted by the stress harness:

| Sign | Orientation policy | Samples | Modal Brahmi label | Modal share | Shape null | Label null | Decision |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| `817` | `visual_ltr_catalog_reverse` | 2 | `dhya` | 1.000000 | 0.025000 | 1.000000 | failed |
| `527` | `visual_ltr_catalog_order` | 6 | `ra` | 1.000000 | 0.035000 | 0.031000 | failed |
| `472` | `visual_ltr_catalog_reverse` | 2 | `ra` | 1.000000 | 0.040000 | 1.000000 | failed |
| `060` | `visual_ltr_catalog_reverse` | 2 | `ka` | 1.000000 | 0.040000 | 1.000000 | failed |
| `061` | `visual_ltr_catalog_order` | 4 | `ra` | 1.000000 | 0.047500 | 0.020000 | failed |

The closest rows fail exactly where they need to fail. Their shape-null rates are above the `0.01` bar, their label-null rates are above the `0.01` bar, or both.

## Duplicate-Collapse Audit

A skeptic-side duplicate audit then asked whether raw family agreement was inflated by exact token-crop reuse across answer-key packets. The answer is yes for the near-misses, and the original null failure was already enough even before this audit.

Audit outputs:

- `data/brahmi/source_token_duplicate_collapse_audit_v2.csv`
- `data/brahmi/source_token_duplicate_collapse_audit_v2_summary.json`

Across the 83 family rows:

| Duplicate-collapse status | Count |
| --- | ---: |
| Raw not unanimous | 53 |
| Raw unanimity collapses below two unique token hashes | 18 |
| Raw unanimity is single-CISI only | 6 |
| Raw unanimity survives duplicate collapse but original null failed | 6 |

The top five near-misses become weaker under this audit:

| Sign | Raw samples | Unique token hashes | Unique CISIs | Modal label | Duplicate status |
| --- | ---: | ---: | ---: | --- | --- |
| `817` | 2 | 1 | 1 | `dhya` | collapses below two hashes |
| `527` | 6 | 2 | 1 | `ra` | single-CISI only |
| `472` | 2 | 1 | 1 | `ra` | collapses below two hashes |
| `060` | 2 | 1 | 1 | `ka` | collapses below two hashes |
| `061` | 4 | 2 | 1 | `ra` | single-CISI only |

## Priority C Stress

The anchored-collapse stress harness now reads the v2 family table and forces the top v2 near-misses as explicitly rejected constraints. The strongest v2 rejected stress set fixes five signs:

```text
817=dhya;527=ra;472=ra;060=ka;061=ra
```

This leaves `4365.209462` label-symmetry bits from the `4410.970864`-bit unanchored baseline. It is not a collapse and it is not a reading. It is a guardrail showing that even forcing the best rejected v2 rows only produces the same mechanical reduction as any five fixed labels.

## Outputs

- `data/brahmi/tools/build_brahmi_source_token_descent_gate_v2.py`
- `data/brahmi/source_token_brahmi_descent_v2_summary.json`
- `data/brahmi/source_token_descent_inventory_v2.csv`
- `data/brahmi/source_token_segments_v2.csv`
- `data/brahmi/source_token_brahmi_neighbors_v2.csv`
- `data/brahmi/source_token_family_descent_summary_v2.csv`
- `data/brahmi/source_token_shape_null_iterations_v2.csv`
- `data/brahmi/source_token_label_null_iterations_v2.csv`
- `data/brahmi/source_token_duplicate_collapse_audit_v2.csv`
- `data/brahmi/source_token_duplicate_collapse_audit_v2_summary.json`
- `data/brahmi/source_token_descent_fetch_log_v2.csv`
- `data/open_prototype/reports/anchored_constraint_collapse_stress_summary.json`

## Decision

No morphological descent line survives. No Brahmi-derived phonetic anchor is accepted. The useful residue is the larger source-tokenized adversarial gate: 1,342 early Brahmi glyphs, 611 source-token crops, 83 sign/orientation families, and a zero-survivor result under measured shape and label nulls.
