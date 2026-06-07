# Lipi Metadata Prediction Probe

Date: 2026-05-24

## Purpose

This experiment asks whether the filtered `lipi` sign sequences predict independent metadata better than duplicate-calibrated structured nulls.

It follows the [Lipi structured null comparator](lipi_structured_null_comparator.md). That comparator showed that explicit nonlinguistic administrative and emblem formulae can beat observed bidirectional masked-sign prediction. The next question is whether observed signs carry metadata structure that those nulls do not reproduce.

This is still a T3 planning-layer probe. The metadata labels are from filtered `lipi`, not an authoritative corpus. The result does not assign meanings, sign values, phonetics, language identity, or translations.

## Local Artifacts

```text
data/open_prototype/tools/lipi_metadata_prediction_probe.mjs
data/open_prototype/reports/lipi_metadata_prediction_iterations.csv
data/open_prototype/reports/lipi_metadata_prediction_summary.csv
data/open_prototype/reports/lipi_metadata_prediction_summary.json
```

Source file:

```text
data/open_prototype/reports/lipi_scope_rows.csv
```

Scope:

```text
readiness_bucket = lipi_numeric_clean_candidate
source_rows = 2887
exact_sequence_families = 1798
min_label_rows = 40
iterations_per_control = 5
```

The probe collapses exact sign sequences before prediction. Each sequence family receives the majority metadata label for the target field, so repeated formula rows do not dominate the result.

## Targets And Models

Targets attempted:

```text
type, site, region, material, complete, direction, class
```

The `complete` target did not have at least two eligible labels after filtering, so no prediction row is reported for it.

Models:

- Majority: leave-one-out majority label.
- Length: label distribution by inscription length.
- Edge frame: label distribution by length, first sign, and last sign, falling back to length/majority.
- Token NB: leave-one-out multinomial Naive Bayes over sign tokens.

The controls are family-level versions of the structured nulls:

- Duplicate-matched position slots.
- Administrative register code.
- Emblem formula code.
- Mixed admin-emblem code.

## Observed Metadata Prediction

Observed family-level results:

| Target | Rows | Labels | Majority Accuracy | Edge Accuracy | Token NB Accuracy | Token NB Macro-F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| type | 1,678 | 5 | 0.589988 | 0.579261 | 0.633492 | 0.370160 |
| site | 1,669 | 3 | 0.579389 | 0.605752 | 0.654284 | 0.423297 |
| region | 1,777 | 3 | 0.576815 | 0.611142 | 0.638717 | 0.411017 |
| material | 1,563 | 4 | 0.756238 | 0.737044 | 0.736404 | 0.325959 |
| direction | 1,798 | 2 | 0.953281 | 0.948832 | 0.942158 | 0.494534 |
| class | 1,697 | 9 | 0.219210 | 0.515616 | 0.543312 | 0.474895 |

Material and direction are not useful wins here. Material is dominated by `Steatite`, and direction is dominated by `R/L`; token prediction does not improve over majority.

The strongest observed targets are `class`, `site`, `region`, and `type`, but they need different caveats.

## Structured Null Comparison

Token NB accuracy against structured null means:

| Target | Observed | Position-Slot Null | Admin Null | Emblem Null | Mixed Null |
| --- | ---: | ---: | ---: | ---: | ---: |
| type | 0.633492 | 0.553635 | 0.534088 | 0.535399 | 0.644458 |
| site | 0.654284 | 0.548832 | 0.543919 | 0.535051 | 0.649731 |
| region | 0.638717 | 0.547327 | 0.541925 | 0.530557 | 0.642994 |
| material | 0.736404 | 0.732054 | 0.717594 | 0.714651 | 0.723608 |
| direction | 0.942158 | 0.946608 | 0.944494 | 0.939711 | 0.934816 |
| class | 0.543312 | 0.289452 | 0.281791 | 0.270359 | 0.271538 |

The mixed admin-emblem null matches or exceeds `type`, `site`, and `region` because it intentionally gives tablet-like rows one generator and seal-like rows another. Since artifact type, site, and region are correlated in the planning layer, those targets are not independent enough yet.

The `class` target survives this first structured-null pass. Observed Token NB accuracy is 0.543312 with macro-F1 0.474895, while structured null token accuracies range from 0.270359 to 0.289452. Edge-frame prediction also remains higher observed than all structured nulls for `class`. A later source audit downgrades the interpretation of this result.

## Interpretation

This probe narrows the target again:

- Metadata prediction is not automatically stronger evidence than sequence prediction.
- Type, site, and region are entangled; a null that encodes artifact type can nearly reproduce or exceed those scores.
- Material and direction are currently dominated by majority labels.
- The strongest surviving metadata signal in this pass is inscription `class`, but later source audit shows it must be treated as an unverified source-code field rather than independent semantic metadata.

The result supports only this claim:

```text
In the filtered `lipi` numeric-clean planning layer, exact-sequence-collapsed sign tokens predict inscription class better than duplicate-calibrated structured nulls in this scout, while type/site/region prediction is confounded by artifact-type mixtures.
```

Later boundary:

```text
The Lipi class field audit found no upstream definition-like text for the class abbreviations and found several labels that are near-proxies for length, site, type, or completeness. Therefore the class result is a source-field stress test, not semantic evidence.
```

It does not support:

- Accepted reading direction.
- Accepted sign segmentation.
- Sign meanings.
- Semantic slots.
- Phonetic values.
- Language identity.
- Translation.
- A conclusion that IVC is linguistic or nonlinguistic.

## Next Falsification

Follow-up completed:

- [Lipi stratified class probe](lipi_stratified_class_probe.md) tested class prediction within eligible site, artifact-type, and type-site strata.
- [Lipi class robustness probe](lipi_class_robustness_probe.md) tested class prediction under edge-removal and formula-family controls.
- [Lipi class field audit](lipi_class_field_audit.md) downgraded `class` to an unverified source-code field.
- [Lipi class proxy-control probe](lipi_class_proxy_control_probe.md) showed that `class` remains sign-recoverable after proxy controls, which supports a source-internal coding or circularity interpretation.
- [Lipi semantic anchor target audit](lipi_semantic_anchor_target_audit.md) identified clearer-provenance next targets: `symbol`, `cult`, `material`, `shape`, `boss`, `type`, and coarse dimension bins, all requiring proxy-blocked controls.
- [Lipi semantic anchor prediction probe](lipi_semantic_anchor_prediction_probe.md) ran those proxy-blocked controls and found no candidate clean enough for semantic interpretation.

The next metadata tests should now avoid treating `class` as independent evidence:

- Compare class prediction against source/cataloging convention controls.
- Remove near-pure length/site/type proxy labels and rerun class prediction.
- Run blocked semantic-anchor prediction for material, dimensions, iconography, and artifact type.
- Repeat on an authoritative or image-validated corpus before treating any metadata result as more than a scout.
