# Lipi Class Robustness Probe

Date: 2026-05-24

## Purpose

This experiment directly attacks the strongest current metadata scout result: `class` prediction in the broad filtered `lipi` planning layer.

The prior [Lipi stratified class probe](lipi_stratified_class_probe.md) found that `class` labels were predictable from sign tokens inside eligible site, artifact-type, and type-site strata. This probe asks whether that signal survives two simpler explanations:

- High-frequency edge signs.
- Repeated formula/template families.

This remains a T3 planning-layer scout. The `class` labels come from filtered `lipi`, not from an authoritative corpus. The result does not assign meanings, sign values, phonetics, language identity, or translations.

## Local Artifacts

```text
data/open_prototype/tools/lipi_class_robustness_probe.mjs
data/open_prototype/reports/lipi_class_robustness_inventory.csv
data/open_prototype/reports/lipi_class_robustness_results.csv
data/open_prototype/reports/lipi_class_robustness_summary.json
```

Source file:

```text
data/open_prototype/reports/lipi_scope_rows.csv
```

Scope:

```text
readiness_bucket = lipi_numeric_clean_candidate
source_rows = 2887
target = class
min_stratum_rows = 90
min_label_rows = 12
```

The top-10 edge signs removed in the edge-removal policies are:

```text
740, 700, 400, 520, 033, 032, 861, 817, 820, 034
```

## Policies

The probe evaluates six policy layers:

| Policy | Transform | Family collapse |
| --- | --- | --- |
| `exact_sequence_collapsed` | none | exact sequence |
| `edge_frame_collapsed` | none | first/last edge frame |
| `one_edit_family_collapsed` | none | connected one-edit neighborhoods |
| `top10_edge_removed_exact_sequence_collapsed` | remove top-10 edge signs | exact sequence |
| `top10_edge_removed_edge_frame_collapsed` | remove top-10 edge signs | first/last edge frame |
| `top10_edge_removed_one_edit_family_collapsed` | remove top-10 edge signs | connected one-edit neighborhoods |

Each family receives the majority `class`, `site`, and `type` labels from its source rows. The prediction task then uses leave-one-out models:

- Majority.
- Length.
- Edge frame.
- Token NB.

## Inventory

| Policy | Families | Tokens | Unique Signs | Source Weight | Largest Family Records | Largest Source Weight |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| exact sequence | 1798 | 8212 | 571 | 2887 | 1 | 117 |
| edge frame | 1408 | 6288 | 554 | 2887 | 21 | 117 |
| one-edit family | 1098 | 6011 | 509 | 2887 | 241 | 810 |
| top-10 edge removed, exact sequence | 1658 | 5913 | 561 | 2517 | 1 | 43 |
| top-10 edge removed, edge frame | 1550 | 5506 | 556 | 2517 | 6 | 43 |
| top-10 edge removed, one-edit family | 838 | 3991 | 476 | 2517 | 377 | 650 |

The one-edit policies are deliberately aggressive. They are not natural formula families; they are blunt anti-template stress tests.

## Overall Results

Overall `class` prediction:

| Policy | Rows | Labels | Majority Share | Majority Acc | Length Acc | Edge-Frame Acc | Token NB Acc | Token NB Macro-F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| exact sequence | 1750 | 12 | 0.212571 | 0.212571 | 0.399429 | 0.496571 | 0.525714 | 0.356200 |
| edge frame | 1354 | 11 | 0.252585 | 0.252585 | 0.414328 | 0.414328 | 0.496307 | 0.354094 |
| one-edit family | 1082 | 11 | 0.206100 | 0.206100 | 0.442699 | 0.463956 | 0.423290 | 0.311090 |
| top-10 edge removed, exact sequence | 1623 | 11 | 0.216882 | 0.216882 | 0.259396 | 0.309920 | 0.474430 | 0.331172 |
| top-10 edge removed, edge frame | 1515 | 11 | 0.227063 | 0.227063 | 0.264026 | 0.264026 | 0.476568 | 0.308648 |
| top-10 edge removed, one-edit family | 814 | 9 | 0.212531 | 0.212531 | 0.374693 | 0.382064 | 0.372236 | 0.228813 |

The result has two parts:

- Edge-sign removal alone does not erase the class signal. Token NB remains around 0.474 to 0.477 accuracy after top-10 edge removal.
- The harshest combined policy downgrades the result. Token NB remains above majority, but its raw accuracy no longer beats the length and edge-frame controls. Its macro-F1 remains higher than those controls, which means the residual signal is not only majority-class guessing.

## Stratified Stress Results

Selected harsh-control rows under `top10_edge_removed_one_edit_family_collapsed`:

| Stratum | Rows | Labels | Majority Share | Majority Acc | Length Acc | Edge-Frame Acc | Token NB Acc | Token NB Macro-F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Mohenjo-daro | 512 | 9 | 0.230469 | 0.230469 | 0.308594 | 0.320313 | 0.398438 | 0.247401 |
| SEAL:R | 100 | 5 | 0.300000 | 0.300000 | 0.380000 | 0.380000 | 0.490000 | 0.429610 |
| SEAL:S | 526 | 9 | 0.262357 | 0.262357 | 0.410646 | 0.420152 | 0.384030 | 0.192108 |
| SEAL:S@Mohenjo-daro | 367 | 8 | 0.269755 | 0.269755 | 0.416894 | 0.419619 | 0.405995 | 0.234466 |

The result is mixed:

- Mohenjo-daro and SEAL:R remain nontrivial under the harshest policy.
- SEAL:S and SEAL:S@Mohenjo-daro still beat majority, but raw accuracy is matched or exceeded by length/edge-frame controls.
- Some strata that were strong earlier become too small or label-thinned under the harshest policy. `TAB:I` drops out of the selected harsh-control table, and `TAB:B` falls to 48 rows, so those should not be treated as robust under this policy.

## Interpretation

The class result survives a direct attack, but in a downgraded form.

Supported claim:

```text
In the filtered `lipi` numeric-clean planning layer, catalog `class` labels remain partly predictable after high-frequency edge-sign removal and formula-family downweighting. The residual is strongest as macro-F1 and in selected strata, but the harshest combined control shows that simple length/edge-frame structure can match or exceed Token NB raw accuracy in some important scopes.
```

Not supported:

- A claim that `class` labels are ancient semantic classes.
- A claim that sign tokens encode meanings.
- A claim that the residual is language-specific.
- Accepted sign values.
- Accepted readings.
- Translation.

The later [Lipi class field audit](lipi_class_field_audit.md) makes the boundary stricter. `class` is now downgraded to an unverified source-code field because no upstream definition-like text was found for the abbreviations, and several labels are near-proxies for length, site, type, or completeness.

The later [Lipi class proxy-control probe](lipi_class_proxy_control_probe.md) confirms that the field is still sign-recoverable after proxy-heavy labels are removed and labels are shuffled within length/type/site blocks. That strengthens the source-internal coding or circularity interpretation, not a semantic interpretation.

The most honest current status is:

```text
Class remains useful as a source-field stress target, but it is not clean enough for semantic interpretation. The next move is finding an external definition for the codes, removing proxy labels, and repeating the protocol on authoritative or image-validated data.
```

## Next Falsification

Next tests:

- Find external definitions for the `class` abbreviations, if they exist.
- Identify whether `class` labels are copied from catalog abbreviations, modern grouping decisions, inferred object functions, or decipherment-internal labels.
- Repeat class prediction after removing low-row strata that fall below the original eligibility threshold after transformation.
- Repeat class prediction after removing near-pure length/site/type proxy labels.
- Rerun the same class protocol on an authoritative corpus or an image-validated subset.
- Run known-script scarcity comparators with artificial catalog classes to measure how often catalog metadata creates similar predictability.
