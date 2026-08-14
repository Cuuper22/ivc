# Lipi Semantic Anchor Prediction Probe

Date: 2026-05-24

## Purpose

This note tests the most tempting shortcut to meaning and reports that it fails. A semantic anchor is a metadata field whose values might plausibly be tied to what an inscription says — the object's iconography, material, or shape — so that predicting it from signs would be a first foothold. The danger is that such a field is predictable for boring reasons, such as long inscriptions sitting on big objects. To guard against that, each test is compared against a blocked label-shuffle null: the labels are shuffled among rows that already match on the suspect shortcut, so anything the shuffled version achieves is what the shortcut alone can produce. This probe follows the [Lipi semantic anchor target audit](lipi_semantic_anchor_target_audit.md). It asks whether candidate semantic-anchor metadata fields are predicted by signs after preserving obvious catalog shortcuts with those nulls.

This is not a semantic reading. It does not assign meanings, sign values, phonetics, language identity, or translations. The labels are still `lipi` catalog metadata — `lipi` being the project's filtered working corpus — from a T3 planning source, meaning unverified data useful for direction but never admissible as proof.

## Local Artifacts

```text
data/open_prototype/tools/lipi_semantic_anchor_prediction_probe.mjs
data/open_prototype/reports/lipi_semantic_anchor_prediction_observed.csv
data/open_prototype/reports/lipi_semantic_anchor_prediction_iterations.csv
data/open_prototype/reports/lipi_semantic_anchor_prediction_summary.csv
data/open_prototype/reports/lipi_semantic_anchor_prediction_summary.json
```

Source file:

```text
data/open_prototype/lipi/metadata_filtered.csv
```

Scope:

```text
source_rows: 5679
numeric_clean_source_rows: 2887
exact_sequence_families: 1798
min_label_families: 30
iterations_per_block: 3
```

The low iteration count is deliberate for this scout because each target/block/model combination uses leave-one-out prediction. Larger deterministic runs can be launched with `IVC_SEMANTIC_ANCHOR_ITERATIONS`, but the first result is already strong enough to decide that no target should be promoted.

## Targets

Targets tested:

```text
symbol
cult
material
shape
boss
type
horizontal_bin
vertical_bin
thickness_bin
area_bin
aspect_bin
```

Observed predictors:

- Majority.
- Length.
- Type.
- Site.
- Material.
- Shape.
- Direction.
- Edge frame.
- Length+type+site.
- Material+shape.
- Token NB over exact sign tokens.

Predictors that directly duplicate the target are skipped. For example, `type` is not used as a shortcut predictor for target `type`.

Blocked label-shuffle nulls:

- Global.
- Length.
- Type.
- Site.
- Type+site.
- Material.
- Shape.
- Direction.
- Length+type+site.
- Material+shape.
- Edge frame.
- Target-specific hard proxy block.

A proxy is another field that stands in for the target closely enough to predict it without any sign information. The hard proxy blocks preserve the strongest obvious catalog tangles for each target. For example, `symbol` preserves length, type, site, shape, cult field, and material.

## Observed Shortcut Models

The observed results already show why these targets cannot be treated naively.

| Target | Majority Acc | Best Shortcut Acc | Token NB Acc | Token NB Macro-F1 |
| --- | ---: | ---: | ---: | ---: |
| `symbol` | 0.310924 | 0.363445 (`material_shape`) | 0.276261 | 0.093696 |
| `cult` | 0.633461 | 0.655172 (`material_shape`) | 0.605364 | 0.193756 |
| `material` | 0.756238 | 0.905950 (`length_type_site`) | 0.736404 | 0.325959 |
| `shape` | 0.635287 | 0.835411 (`length_type_site`) | 0.675810 | 0.237947 |
| `boss` | 0.755975 | 0.823899 (`material_shape`) | 0.724528 | 0.247964 |
| `type` | 0.578947 | 0.896491 (`material_shape`) | 0.621637 | 0.305709 |
| `horizontal_bin` | 0.398930 | 0.485731 (`length_type_site`) | 0.444114 | 0.314026 |
| `vertical_bin` | 0.356122 | 0.627098 (`length_type_site`) | 0.465507 | 0.430971 |
| `thickness_bin` | 0.436019 | 0.554502 (`length_type_site`) | 0.482227 | 0.310822 |
| `area_bin` | 0.373750 | 0.588125 (`length_type_site`) | 0.441875 | 0.384212 |
| `aspect_bin` | 0.618182 | 0.838245 (`material_shape`) | 0.638871 | 0.459526 |

For most targets, non-sign metadata shortcuts beat Token NB. That is a large warning light, not a subtle one.

## Hardest Token NB Nulls

For each target, the hardest Token NB null is the blocked shuffle with the smallest observed-minus-null accuracy gap.

| Target | Hardest Block | Observed Acc | Null Mean | Gap | Macro-F1 Gap | Unchanged Label Share |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `symbol` | hard proxy | 0.276261 | 0.283613 | -0.007353 | 0.012034 | 0.595938 |
| `cult` | type | 0.605364 | 0.610047 | -0.004683 | 0.001834 | 0.460622 |
| `material` | type | 0.736404 | 0.736618 | -0.000213 | 0.006294 | 0.882917 |
| `shape` | edge frame | 0.675810 | 0.671031 | 0.004780 | 0.008594 | 0.915420 |
| `boss` | type+site | 0.724528 | 0.736268 | -0.011740 | -0.012891 | 0.750524 |
| `type` | edge frame | 0.621637 | 0.620663 | 0.000975 | 0.014746 | 0.898051 |
| `horizontal_bin` | edge frame | 0.444114 | 0.434007 | 0.010107 | 0.006916 | 0.860682 |
| `vertical_bin` | edge frame | 0.465507 | 0.443754 | 0.021753 | 0.022533 | 0.864719 |
| `thickness_bin` | edge frame | 0.482227 | 0.482622 | -0.000395 | 0.000756 | 0.894945 |
| `area_bin` | edge frame | 0.441875 | 0.436042 | 0.005833 | 0.009097 | 0.866875 |
| `aspect_bin` | edge frame | 0.638871 | 0.634901 | 0.003971 | 0.008747 | 0.907419 |

No target gives a clean semantic-anchor win. Several targets are matched or exceeded by the hardest null. The small positive gaps on shape, type, and dimension bins are too close to edge-frame-preserved nulls to promote.

The high unchanged-label share in the edge-frame nulls is itself informative: edge-frame blocks are very tight. They test whether interior signs add much beyond the edge frame, and this scout says "not much" for these metadata targets.

## Interpretation

The result is a downgrade for naive semantic anchoring:

```text
In the filtered `lipi` T3 planning layer, candidate semantic-anchor metadata labels are mostly explained by catalog/object-form proxies, majority structure, or edge-frame structure.
```

This does not mean there is no semantic structure in the inscriptions. It means this particular broad metadata route is not yet clean enough to support semantic claims.

Current consequence:

- Do not infer iconographic meanings from `symbol` prediction.
- Do not infer cult/ritual meaning from `cult` prediction.
- Do not infer material or commodity readings from `material`.
- Do not infer object-form semantics from `shape`, `boss`, or `type`.
- Treat dimension-bin residues as a possible next scout only after edge-frame and artifact-form controls are strengthened.

## Result

This probe supports only this claim:

```text
Candidate semantic-anchor metadata in filtered `lipi` can be prediction-tested, but the first proxy-blocked pass finds no clean target that survives catalog/object-form and edge-frame controls strongly enough for semantic interpretation.
```

It does not support:

- Iconographic readings.
- Cultic readings.
- Material or commodity readings.
- Metrological readings.
- Semantic slots.
- Sign values.
- Phonetic values.
- Language identity.
- Translation.

## Next Falsification

The next semantic-anchor pass should be stricter and narrower:

- Increase deterministic iterations for only the two weakest possible residues: `vertical_bin` and perhaps `horizontal_bin`.
- Replace raw edge-frame blocks with structural sign-class blocks so singleton-heavy edge frames do not create mostly unchanged nulls.
- Run within artifact-type strata, especially `SEAL:S`, `TAB:B`, and `TAB:I`, before comparing iconography or dimensions.
- Repeat on an authoritative or image-validated corpus before treating any metadata association as admissible evidence.

Follow-up:

- [Lipi dimension residue stress probe](lipi_dimension_residue_stress_probe.md) ran the dimension-bin stress pass and found that metadata shortcuts beat sign-token prediction for every dimension target.
