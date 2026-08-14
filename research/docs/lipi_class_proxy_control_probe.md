# Lipi Class Proxy-Control Probe

Date: 2026-05-24

This note is a control probe. It exists to attack a result we already have, by removing every boring explanation for it and seeing what is left standing.

The result under attack: a column in our dataset called `class` can be predicted from the signs on the object. The boring explanation is that `class` is really just a restatement of the object's length, site, or type — what we call a proxy. So this note strips out the labels that are mostly proxies, then shuffles the remaining labels within matched blocks of rows to build a null model. A null model is a deliberately meaningless version of the data; if your real result cannot beat it, your result was noise.

Note where this lands. The finding survives, and surviving makes it more worrying rather than less, because the most likely remaining explanation is circularity: the class codes may have been derived from the inscriptions in the first place.

## Purpose

This experiment follows the [Lipi class field audit](lipi_class_field_audit.md). That audit downgraded `lipi.class` from metadata scout target to unverified source-code field because no upstream definition-like text was found for the class abbreviations, and several class values are near-proxies for length, site, type, or completeness.

This probe asks a narrower question:

```text
Is the remaining `class` predictability only length/site/type leakage, or does it track exact sign structure after those row-metadata proxies are controlled?
```

This is not a semantic test. If the result survives, the best interpretation is that `lipi.class` is sign-internal or source-internal coding. That can reveal how the source labels its own corpus, but it cannot establish ancient meaning.

## Local Artifacts

```text
data/open_prototype/tools/lipi_class_proxy_control_probe.mjs
data/open_prototype/reports/lipi_class_proxy_control_observed.csv
data/open_prototype/reports/lipi_class_proxy_control_iterations.csv
data/open_prototype/reports/lipi_class_proxy_control_summary.csv
data/open_prototype/reports/lipi_class_proxy_control_summary.json
```

Source files:

```text
data/open_prototype/reports/lipi_scope_rows.csv
data/open_prototype/reports/lipi_class_field_counts.csv
```

Scope:

```text
readiness_bucket = lipi_numeric_clean_candidate
source_rows = 2887
exact_sequence_families = 1798
min_label_rows = 12
iterations_per_shuffle_block = 20
```

## Label Filters

Three versions of the data: everything eligible, then two progressively harsher versions with proxy-heavy labels stripped out.

The probe uses three label filters:

| Filter | Rows | Labels | Removed Labels |
| --- | ---: | ---: | --- |
| `all_eligible` | 1750 | 12 | none |
| `source_proxy_ge_0_80_removed` | 1729 | 11 | `PN` |
| `source_proxy_ge_0_65_removed` | 1230 | 7 | `IT`, `LP`, `MS`, `PN`, `VX` |

The removed labels are based on the source-field audit. A class label is removed when its highest source-audit share across type, site, or length reaches the threshold.

## Observed Predictors

Five models per filter, from a dumb one that always guesses the commonest label up to one that reads the sign tokens. Leave-one-out means each row is predicted by a model trained on every row but itself.

Observed leave-one-out results:

| Filter | Model | Rows | Labels | Accuracy | Macro-F1 |
| --- | --- | ---: | ---: | ---: | ---: |
| all eligible | majority | 1750 | 12 | 0.212571 | 0.029218 |
| all eligible | length | 1750 | 12 | 0.399429 | 0.195489 |
| all eligible | length+type+site | 1750 | 12 | 0.374286 | 0.221261 |
| all eligible | edge frame | 1750 | 12 | 0.390857 | 0.263002 |
| all eligible | token NB | 1750 | 12 | 0.525714 | 0.356200 |
| proxy >= 0.80 removed | token NB | 1729 | 11 | 0.533256 | 0.393925 |
| proxy >= 0.65 removed | majority | 1230 | 7 | 0.302439 | 0.066346 |
| proxy >= 0.65 removed | length | 1230 | 7 | 0.443902 | 0.303378 |
| proxy >= 0.65 removed | length+type+site | 1230 | 7 | 0.412195 | 0.294880 |
| proxy >= 0.65 removed | edge frame | 1230 | 7 | 0.474797 | 0.346487 |
| proxy >= 0.65 removed | token NB | 1230 | 7 | 0.643089 | 0.522030 |

Removing proxy-heavy labels does not weaken token prediction. It strengthens it, which is a warning sign: the remaining `class` labels are likely closer to sign-internal source coding.

## Metadata-Block Label Shuffles

This is the null model. Labels are scrambled among rows that already match on length, type, and site, while the sign strings stay put. Any score the shuffled data still reaches is a score the real result had to beat to mean anything.

The probe shuffles labels inside blocks while preserving sign strings. This tests whether token prediction is only recovering metadata block structure.

Shuffle blocks:

- Global.
- Length.
- Type.
- Site.
- Type+site.
- Length+type+site.

Hardest block for Token NB:

| Filter | Observed Token NB Acc | Length+Type+Site Null Mean | Null P95 | Gap | Observed Macro-F1 | Null Macro-F1 Mean | Macro-F1 Gap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all eligible | 0.525714 | 0.254029 | 0.269457 | 0.271686 | 0.356200 | 0.127197 | 0.229003 |
| proxy >= 0.80 removed | 0.533256 | 0.256564 | 0.267322 | 0.276692 | 0.393925 | 0.139046 | 0.254879 |
| proxy >= 0.65 removed | 0.643089 | 0.322154 | 0.345528 | 0.320935 | 0.522030 | 0.209834 | 0.312197 |

No null iteration reaches observed Token NB accuracy or macro-F1 in these filters.

## Interpretation

The result survives the simple row-metadata proxy explanation:

```text
Within the filtered `lipi` numeric-clean planning layer, `class` labels are recoverable from exact sign tokens even after high-purity proxy labels are removed and labels are shuffled within length/type/site blocks.
```

But this is not semantic evidence. Because the class codes are undefined and may have been produced from the inscriptions themselves, the residual — the part of the signal left after every controlled explanation is removed — is likely source-internal coding, not external metadata.

The upgraded interpretation is:

```text
`lipi.class` tracks sign structure beyond length, type, and site. That makes it useful for source archaeology and circularity detection. It does not make it useful as an independent target for decipherment semantics.
```

Not supported:

- Ancient semantic classes.
- Independent catalog categories.
- Sign meanings.
- Phonetic values.
- Language identity.
- Translation.

## Consequence

Future metadata experiments should not use `class` as a semantic target unless an external definition is found and its independence from the sign string is established.

The next stronger target is not more `class` modeling. It is a clearer-provenance metadata target:

- Material.
- Dimensions.
- Iconography or field symbol.
- Artifact type, with stronger artifact-type nulls.
- Site only after site/type/period entanglement is explicitly modeled.

The first gate — the test each candidate target must pass before it is used — is now recorded in [Lipi semantic anchor target audit](lipi_semantic_anchor_target_audit.md).

## Next Falsification

Falsification means the next tests are chosen for their power to break this result, not to confirm it. The last item is the sharpest: build a script where we know the labels were made from the signs, and see how easily a model "rediscovers" them.

Next tests:

- Try to locate class-code definitions in CISI, ICIT, Mahadevan, Wells/Fuls, or source spreadsheets.
- Treat `class` as a possible sign-derived annotation and test for circularity by predicting it from only the first sign, last sign, and fixed sign sets.
- Run iconography/field-symbol prediction with the same metadata-block shuffle controls.
- Build a known-script comparator where artificial source labels are derived from sign sequences, then measure how easily a model "rediscovers" them.
