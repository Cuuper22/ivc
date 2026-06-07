# Lipi Class Field Audit

Date: 2026-05-24

## Purpose

This audit checks whether the filtered `lipi` `class` field can be treated as independent metadata for decipherment research.

The prior metadata probes found that `class` was the strongest remaining metadata scout target. The robustness probe then showed that the signal weakens under edge-sign and formula-family controls. This source audit asks the simpler question: what is this field, and is it defined well enough to support semantic interpretation?

Answer: no. It is still useful as a stress-test target, but it must not be treated as an independent semantic label.

## Local Artifacts

```text
data/open_prototype/tools/lipi_class_field_audit.mjs
data/open_prototype/reports/lipi_class_field_counts.csv
data/open_prototype/reports/lipi_class_field_by_type.csv
data/open_prototype/reports/lipi_class_field_by_site.csv
data/open_prototype/reports/lipi_class_field_by_length.csv
data/open_prototype/reports/lipi_class_field_examples.csv
data/open_prototype/reports/lipi_class_field_audit_summary.json
```

Source inputs:

```text
data/open_prototype/lipi/metadata_filtered.csv
data/open_prototype/reports/lipi_scope_rows.csv
https://github.com/yajnadevam/lipi
```

Upstream repository state checked:

```text
repo: yajnadevam/lipi
branch: main
branch_head_sha: b272ad99c253ba7fa1e4cd91f48cce31f6d02bf4
scanned_text_files: 67
```

## Source Context

The upstream repository is not a neutral corpus source. Its README presents a decipherment claim, and the raw `inscriptions.csv` includes `sanskrit`, `translation`, and `notes` columns. Those three columns remain quarantined.

The audit scanned 67 text-like upstream files for definition-like uses of `class` or the observed class codes. It found:

```text
class_definition_matches_found: 0
translation_columns_present: true
class_column_in_raw_csv: true
class_column_hidden_from_main_table_headers: true
class_column_before_claim_columns: true
```

The current upstream raw CSV has 5,679 non-empty data lines, matching the local filtered row count. A naive CSV parser sees only 3,841 rows because the claim-bearing text fields are not safe to parse with the simple parser used for these local scout tools. Therefore this audit uses the already-filtered local metadata layer for class counts, not the raw claim-bearing CSV.

## Class Inventory

The local filtered layer has:

```text
all_rows: 5679
numeric_clean_rows: 2887
class_values_all_rows: 25
class_values_numeric_clean: 21
```

Top class values:

| Class | All Rows | Numeric-Clean Rows | Complete-Y Share | Top Type | Top Type Share | Top Site | Top Site Share | Top Length | Top Length Share |
| --- | ---: | ---: | ---: | --- | ---: | --- | ---: | --- | ---: |
| ?? | 1341 | 2 | 0.001491 | SEAL:S | 0.264728 | Harappa | 0.447427 | 2+? | 0.176734 |
| SS | 709 | 661 | 1.000000 | SEAL:S | 0.315938 | Harappa | 0.527504 | 2 | 0.417489 |
| UC | 666 | 0 | 0.000000 | TAB:I | 0.243243 | Harappa | 0.576577 | 1+? | 0.381381 |
| SC | 606 | 452 | 1.000000 | SEAL:S | 0.354785 | Harappa | 0.448845 | 3 | 0.346535 |
| VN | 355 | 321 | 1.000000 | TAB:I | 0.484507 | Harappa | 0.985915 | 2 | 0.946479 |
| MT | 330 | 319 | 1.000000 | TAB:B | 0.300000 | Mohenjo-daro | 0.469697 | 4 | 0.336364 |
| IT | 276 | 269 | 1.000000 | SEAL:S | 0.673913 | Mohenjo-daro | 0.655797 | 5 | 0.420290 |
| SP | 225 | 212 | 1.000000 | SEAL:S | 0.626667 | Mohenjo-daro | 0.435556 | 5 | 0.577778 |
| LP | 212 | 197 | 1.000000 | SEAL:S | 0.768868 | Mohenjo-daro | 0.627358 | 7 | 0.457547 |
| TS | 168 | 0 | 1.000000 | SEAL:S | 0.208333 | Mohenjo-daro | 0.357143 | 1 | 0.988095 |

Several labels are heavily shaped by simple metadata:

- `TS`: 98.8095 percent length 1.
- `VN`: 98.5915 percent Harappa and 94.6479 percent length 2.
- `NV`: 98.4127 percent Harappa and 95.2381 percent length 2.
- `NU`: 73.0539 percent `POT:T:g` and 83.8323 percent length 1.
- `PN`: 84.9057 percent length 2.
- `UC`: zero numeric-clean rows, so it is not part of the current structural class prediction target.

This explains part of the previous class predictability. Some `class` labels are not independent of object type, site, completeness, and length.

## Interpretation

The `class` field should be downgraded:

```text
Before this audit:
T3 metadata scout target.

After this audit:
T3 source-code field, useful only for stress testing and source archaeology. Not admissible as independent semantic metadata.
```

Supported claim:

```text
In the filtered `lipi` planning layer, the `class` field is a structured source code that is statistically related to signs, lengths, sites, and artifact types. It is useful for finding where the source's own classification layer tracks sign structure.
```

Not supported:

- That `class` labels are ancient categories.
- That `class` labels are independent catalog facts.
- That a sign sequence predicts semantic class.
- That any `class` code has an accepted meaning.
- Any sign reading, phonetic value, language identity, or translation.

## Consequence For Previous Results

The [Lipi metadata prediction probe](lipi_metadata_prediction_probe.md), [Lipi stratified class probe](lipi_stratified_class_probe.md), and [Lipi class robustness probe](lipi_class_robustness_probe.md) remain useful, but only as source-field stress tests.

They no longer support even a weak semantic scout claim. The most they show is that `lipi.class` is internally structured and partly recoverable from sign strings under some controls.

The later [Lipi class proxy-control probe](lipi_class_proxy_control_probe.md) confirms this boundary. `lipi.class` remains recoverable from exact sign tokens after proxy-heavy labels are removed and labels are shuffled within length/type/site blocks. That strengthens the circularity/source-code interpretation rather than the semantic interpretation.

## Next Falsification

Next steps:

- Find an external definition for the class abbreviations, if one exists in CISI, ICIT, Mahadevan, or another catalog source.
- Remove labels that are near-pure length/site/type proxies and rerun class prediction.
- Treat `class` as a candidate leakage field in future metadata tests.
- Repeat metadata prediction on fields with clearer provenance: site, material, dimensions, iconography, and artifact type.
- Prefer image-validated or authoritative catalog layers before using any field as semantic evidence.
