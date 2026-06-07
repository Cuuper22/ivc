# Lipi FRAME700 Subtype Blocked Null

Date: 2026-05-25

## Question

Does the weak `FRAME700` subtype signal from the previous experiment survive subtype-label shuffles inside matched object/context blocks?

Target:

```text
+700-032+ vs +700-033+ vs +700-034+
```

This attacks the kill condition:

```text
A blocked permutation preserving type, sides, 700 order, and sequence/context structure matches the dimension-model gain.
```

## Local Artifacts

```text
data/open_prototype/tools/lipi_frame700_subtype_blocked_null.mjs
data/open_prototype/reports/lipi_frame700_subtype_blocked_null_iterations.csv
data/open_prototype/reports/lipi_frame700_subtype_blocked_null_summary.csv
data/open_prototype/reports/lipi_frame700_subtype_blocked_null_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_frame700_subtype_rows.csv
```

## Scope

```text
scope: excluding H-2218 through H-2239
leaveout_mode: sequence_family
target_rows: 331
iterations_per_policy: 100
seed_base: 700032033034
models_tested: frequency; dimensions
```

The model is scored under sequence-family leaveout: same `cisi` and same sequence-family key are excluded from training.

Permutation policy:

```text
Subtype labels are shuffled within predeclared blocks.
Row features remain fixed.
The model is scored against the shuffled labels.
```

This is a feature-label association null. It asks how well the same method can perform when subtype labels are random inside a block that preserves known confounds.

## Observed Result

No-H-series, sequence-family leaveout:

| Model | Top-1 | Top-2 | `034` Top-1 | Top-1 Gain vs Frequency |
| --- | ---: | ---: | ---: | ---: |
| Frequency | 0.410876 | 0.719033 | 0.000000 | 0.000000 |
| Dimensions | 0.435045 | 0.806647 | 0.677419 | 0.024169 |

The overall top-1 gain is small. The interesting residue is `034` recall.

## Blocked Nulls

Dimensions model:

| Block Policy | Null Top-1 Mean | Null Top-1 P95 | P(null >= observed top-1) | Null `034` Mean | Null `034` P95 | P(null >= observed `034`) | P(null >= observed gain) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Global subtype shuffle | 0.356767 | 0.422961 | 0.020000 | 0.187097 | 0.365591 | 0.000000 | 0.020000 |
| Type+sides+`700` order | 0.355227 | 0.410876 | 0.010000 | 0.177849 | 0.387097 | 0.000000 | 0.010000 |
| Type+sides+order+context | 0.361420 | 0.410876 | 0.010000 | 0.231828 | 0.451613 | 0.000000 | 0.010000 |
| Type+sides+order+context+relation | 0.372175 | 0.432024 | 0.050000 | 0.334409 | 0.559140 | 0.000000 | 0.050000 |

The harshest relation-preserving null nearly catches the overall top-1 result: observed `0.435045` versus null p95 `0.432024`. That means the overall classifier result is weak.

But the `034` branch does not collapse in these 100 deterministic shuffles. Observed `034` recall is `0.677419`; the harshest null p95 is `0.559140`, and no null iteration reaches observed `034` recall.

## Current Read

This does not prove a three-way `032/033/034` system. It also does not prove a measure, number, commodity, title, word, or phonetic value.

It does preserve one research lead:

```text
034 has a real distributional residue inside the FRAME700 slot after H-series removal, sequence-family leaveout, and relation-preserving subtype shuffles.
```

The safest interpretation is narrow:

```text
034 is the best current broad FRAME700 subtype candidate.
The signal is dimension/form-context shaped.
Object-format or administrative-format explanation remains the default.
033's +400-740-176+ branch stays source-validation priority, but is probably copy/family-heavy.
032 remains unresolved and useful mainly as a sibling/control subtype.
```

## Consequence

The broad metrological reading is still blocked. The null result does not authorize reading `034` as "small", "measure", or any value.

What it does authorize is continuing source validation on `034` contrast objects, because the signal is not erased by the first blocked permutation attack.

Highest-value validation targets remain:

```text
H-933
H-960
H-233
H-309
H-316
H-353
H-355
H-357
H-1302
H-1303
H-1304
H-1344
H-1345
H-1346
H-1347
```

The decisive source questions are still physical:

- Are catalog rows distinct physical sides?
- Is side order physical, photographic, or editorial?
- Are `032`, `033`, and `034` visually distinct signs in the relevant objects?
- Does `+700-X+` versus `+X-700+` survive image-direction checking?
- Does the `+400-740-176+` pairing survive segmentation checks?

## Boundary

No sign meaning, numerical value, metrological reading, semantic reading, phonetic value, language identity, or translation is accepted.
