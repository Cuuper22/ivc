# Lipi Semantic Anchor Target Audit

Date: 2026-05-24

## Purpose

This note picks the next thing to test, and lists what must be controlled before the test is allowed to count. `lipi` is the project's filtered working corpus of Indus sign sequences. A semantic anchor is a metadata field whose values might plausibly be tied to what an inscription says — iconography, material, object shape — so that predicting it from signs would be a first foothold toward meaning. The `class` field was an earlier candidate and was downgraded. This audit asks which `lipi` metadata fields can safely become the next semantic-anchor prediction targets.

It does not test meaning. It does not assign sign values. It does not treat `lipi` as authoritative. It only decides which catalog labels have enough coverage and which proxy controls must be built before any semantic-anchor experiment is allowed. A proxy is another field that stands in for the target closely enough to predict it without any sign information.

## Local Artifacts

```text
data/open_prototype/tools/lipi_semantic_anchor_target_audit.mjs
data/open_prototype/reports/lipi_semantic_anchor_target_summary.csv
data/open_prototype/reports/lipi_semantic_anchor_label_proxy.csv
data/open_prototype/reports/lipi_semantic_anchor_dimension_bins.csv
data/open_prototype/reports/lipi_semantic_anchor_target_summary.json
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
min_target_families: 150
```

## Method

The audit uses the same strict `lipi_numeric_clean_candidate` gate used in the broad structural work. A gate here is a set of conditions a row must pass before it is allowed into the experiment:

- CISI-style ID is present.
- Numeric text is present.
- `complete = Y`.
- Direction is `R/L` or `L/R`.
- Parsed token count matches `text length`.
- No bracketed text, slash compounds, `000` unknown signs, or question markers.

Exact duplicate numeric sign sequences are collapsed into 1,798 families. Each family receives the majority metadata value among its source rows.

Targets are then checked for:

- Number of family labels with at least 30 families.
- Majority-label domination.
- Metadata proxy risk from length, artifact type, site, region, material, shape, iconography, cult field, period, phase, direction, and dimension bins.
- Sign proxy risk from first sign, last sign, and edge frame.

Dimension bins are coarse audit bins, not metrological readings:

```text
horizontal_bin: h_000_015, h_015_025, h_025_035, h_gt_035
vertical_bin: v_000_010, v_010_020, v_020_030, v_gt_030
thickness_bin: th_000_003, th_003_007, th_007_012, th_gt_012
area_bin: area_0000_0200, area_0200_0500, area_0500_1000, area_gt_1000
aspect_bin: aspect_tall, aspect_squareish, aspect_wide, aspect_very_wide
```

## Target Gate

Fields with enough diversity for the next prediction experiment:

| Target | Role | Families With Label | Eligible Families | Eligible Labels | Majority Label | Majority Share | Status |
| --- | --- | ---: | ---: | ---: | --- | ---: | --- |
| `symbol` | Iconography | 1,211 | 952 | 10 | `Bull1:W` | 0.310924 | Needs proxy-block controls |
| `cult` | Iconography/cult apparatus | 887 | 783 | 5 | `SAN` | 0.633461 | Needs proxy-block controls |
| `material` | Material | 1,599 | 1,563 | 4 | `Steatite` | 0.756238 | Needs proxy-block controls |
| `shape` | Object form | 1,716 | 1,604 | 6 | `square` | 0.635287 | Needs proxy-block controls |
| `boss` | Object form | 877 | 795 | 4 | `PB` | 0.755975 | Needs proxy-block controls |
| `type` | Artifact context | 1,798 | 1,710 | 6 | `SEAL:S` | 0.578947 | Needs proxy-block controls |
| `horizontal_bin` | Dimension | 1,682 | 1,682 | 4 | `h_015_025` | 0.398930 | Needs proxy-block controls |
| `vertical_bin` | Dimension | 1,609 | 1,609 | 4 | `v_020_030` | 0.356122 | Needs proxy-block controls |
| `thickness_bin` | Dimension | 844 | 844 | 4 | `th_007_012` | 0.436019 | Needs proxy-block controls |
| `area_bin` | Dimension | 1,600 | 1,600 | 4 | `area_0500_1000` | 0.373750 | Needs proxy-block controls |
| `aspect_bin` | Dimension | 1,600 | 1,595 | 3 | `aspect_squareish` | 0.618182 | Needs proxy-block controls |

Fields that should be used mainly as controls, not semantic anchors:

| Target | Role | Eligible Families | Eligible Labels | Reason |
| --- | --- | ---: | ---: | --- |
| `site` | Archaeological context | 1,740 | 5 | Control for site/site-specific catalog structure |
| `region` | Archaeological context | 1,777 | 3 | Control for site-region entanglement |
| `period` | Chronological context | 749 | 4 | Control for excavated/catalog context |
| `phase` | Chronological context | 982 | 12 | Control for chronological/catalog context |
| `direction` | Catalog direction | 1,798 | 2 | Majority dominated by `R/L` |
| `condition` | Preservation | 1,795 | 4 | Preservation control, not semantic anchor |

`color` is not a good next target in this pass: it has 700 eligible families but is 90 percent `White` among eligible labels.

## Proxy Warnings

Every candidate anchor needs blocked controls before prediction.

Examples from the label-proxy table:

- `symbol = Bull1:S` is 100 percent `shape = square` among rows with shape data.
- `symbol = Gaur` is 100 percent `cult = Trough` among rows with cult data.
- `type = TAB:C` is 100 percent `material = Copper`.
- `type = SEAL:S` is 99.1919 percent `shape = square`.
- `shape = cuboid-convex` is 98.9899 percent `type = SEAL:R`.
- Many candidate labels are also nearly all `R/L`, so direction must be treated as a background catalog skew rather than evidence.

These are not flaws to hide. They are the exact controls the next semantic-anchor experiment must preserve.

## Interpretation

The audit gives a better next path than the downgraded `class` field:

- Iconography targets: `symbol`, `cult`.
- Object/material targets: `material`, `shape`, `boss`, `type`.
- Dimension targets: horizontal, vertical, thickness, area, and aspect bins.
- Required controls: site, region, period, phase, direction, length, type, material, shape, and edge frame.

The result supports only this claim:

```text
In the filtered `lipi` T3 planning layer — the project's tier label for unverified working data, useful for direction but never admissible as proof — several clearer-provenance catalog fields have enough exact-sequence-collapsed label coverage to support proxy-blocked semantic-anchor prediction experiments.
```

It does not support:

- Iconographic meaning for any sign.
- Material or commodity readings.
- Metrological readings.
- Semantic slots.
- Sign values.
- Phonetic values.
- Language identity.
- Translation.

## Next Falsification

The next experiment should predict `symbol`, `cult`, `material`, `shape`, `type`, and dimension bins from sign sequences only under blocked label-shuffle nulls that preserve:

- Length.
- Type.
- Site.
- Type-site.
- Material.
- Shape.
- Direction.
- Edge frame or first/last sign class.

A target is interesting only if sign-token prediction beats these blocked nulls and cannot be matched by length, type, site, material, shape, direction, or edge-frame shortcuts.

Follow-up:

- [Lipi semantic anchor prediction probe](lipi_semantic_anchor_prediction_probe.md) ran the first blocked-null pass and found no candidate target clean enough for semantic interpretation.
