# Lipi Short-Mark Functional Codebook

Date: 2026-05-24

## Question

This note makes a real attempt at decipherment, but of jobs rather than words. A short mark is a one- or two-sign row on an object that carries writing on more than one side; a side role is a guess at what each such side is doing, named from the signs that recur on it. A codebook is a table of those roles — if the sides of one object follow a system, then knowing some of an object's sides should let us predict the rest. The risk is that any apparent system comes from one repeated series of near-identical tablets. The question: can the side-role labels on multi-side short-mark artifacts predict each other, or is the apparent structure mostly a one-series trap?

This is a direct decipherment attempt at the functional layer. It tries to recover a codebook of side roles, not phonetic values or prose translation.

## Analyst Labels

These labels are temporary names over observed sign co-occurrence:

FRAME700 is the project's label for short rows built on sign `700`, and a subtype is which second sign accompanies it.

```text
FRAME700_SUBTYPE032 = side contains 700 and 032
FRAME700_SUBTYPE033 = side contains 700 and 033
FRAME700_SUBTYPE034 = side contains 700 and 034
FRAME003_ROLE861 = side contains 861 and 003
FRAME003_ROLE15X = side contains 154/156 and 003
PAIR156_176 = side contains 156 and 176
```

They are not accepted meanings.

## Coverage

```text
validation_queue_artifacts: 397
artifacts_with_two_or_more_functional_labels: 70
```

Most common labels:

```text
FRAME700_SUBTYPE033: 136
FRAME700_SUBTYPE034: 114
FRAME700_SUBTYPE032: 102
FRAME003_ROLE861: 29
FRAME003_ROLE15X: 22
```

## Strongest Rules

| Antecedent | Consequent | Co-Occurrence | Confidence | Lift |
| --- | --- | ---: | ---: | ---: |
| `FRAME003_ROLE15X` | `FRAME003_ROLE861` | 22 | 1.000000 | 13.689655 |
| `FRAME003_ROLE861` | `FRAME003_ROLE15X` | 22 | 0.758621 | 13.689655 |
| `FRAME003_ROLE15X` | `FRAME700_SUBTYPE034` | 21 | 0.954545 | 3.324163 |
| `FRAME003_ROLE861` | `FRAME700_SUBTYPE034` | 21 | 0.724138 | 2.521779 |

This is the H-2218 through H-2239 template speaking loudly.

## Missing-Role Prediction

Task:

```text
Mask one functional side label on an artifact.
Predict it from the remaining labels.
Leave the target artifact out of training.
Compare frequency, type/site/sides, and observed-role-context models.
```

| Scope | Model | Predictions | Top-1 | Top-3 | Median Rank |
| --- | --- | ---: | ---: | ---: | ---: |
| All validation queue | Frequency | 162 | 0.098765 | 0.395062 | 4 |
| All validation queue | Type/site/sides | 162 | 0.228395 | 0.654321 | 3 |
| All validation queue | Observed role context | 162 | 0.524691 | 0.660494 | 1 |
| Excluding H-2218 through H-2239 | Frequency | 96 | 0.156250 | 0.437500 | 6 |
| Excluding H-2218 through H-2239 | Type/site/sides | 96 | 0.156250 | 0.427083 | 5 |
| Excluding H-2218 through H-2239 | Observed role context | 96 | 0.229167 | 0.437500 | 4 |

## Current Read

With the H-series included, observed side roles predict other side roles strongly. That is a real functional-codebook signal.

After removing H-2218 through H-2239, the signal is weak. The broad short-mark queue does not yet have a stable codebook. The live decipherment foothold is therefore narrow:

```text
H-2218 through H-2239 likely preserve a copied or batch-specific side-role system.
FRAME700_SUBTYPE034 is the best broader lead.
FRAME700_SUBTYPE033 and FRAME700_SUBTYPE032 need separate qualifier tests, not immediate merging.
```

## Next Direct Attack

Attack the broader `032/033/034` system directly:

```text
Within artifacts carrying a FRAME700 subtype, predict subtype 032/033/034 from:
- artifact type/site/sides
- dimensions
- side relation
- long-side text family
- duplicate-family membership
```

If `034` still separates after H-series removal and exact `700` context conditioning, it becomes the first serious broad functional qualifier candidate.

Status: executed in [Lipi FRAME700 subtype discrimination](lipi_frame700_subtype_discrimination.md). `034` remains live as a weak distributional subtype candidate, but the best surviving signal is dimension/form-context shaped, not semantic or phonetic.

## Artifacts

```text
data/open_prototype/tools/lipi_short_mark_functional_codebook.mjs
data/open_prototype/reports/lipi_short_mark_functional_codebook_artifacts.csv
data/open_prototype/reports/lipi_short_mark_functional_codebook_rules.csv
data/open_prototype/reports/lipi_short_mark_functional_codebook_predictions.csv
data/open_prototype/reports/lipi_short_mark_functional_codebook_summary.json
```

## Boundary

No sign meaning, numerical value, phonetic reading, language identity, or translation is accepted.
