# H-2218 Through H-2239 Slot Grammar Reconstruction

Date: 2026-05-25

This note is a reconstruction experiment. It measures how formulaic the H-2218 through H-2239 tablet series is by hiding one side of each tablet at a time and asking whether the other two sides predict what the hidden side says. If the series behaves like a fixed three-slot formula, the hidden side should be recoverable.

## Question

If one side of each H-series tablet is hidden, can the other two sides reconstruct the missing side role and exact side text?

This is a structural experiment on the current catalog-side layer — the recorded transcriptions, not verified images. It is not a source-image result.

## Inputs

- Input: `data/open_prototype/reports/lipi_h2218_h2239_side_role_templates.csv`
- Script: `data/open_prototype/tools/lipi_h2218_h2239_slot_grammar_reconstruction.mjs`
- Predictions: `data/open_prototype/reports/lipi_h2218_h2239_slot_grammar_predictions.csv`
- Failures: `data/open_prototype/reports/lipi_h2218_h2239_slot_grammar_failures.csv`
- Summary: `data/open_prototype/reports/lipi_h2218_h2239_slot_grammar_summary.json`

## Method

For each of the 22 H-series objects, each side was hidden once, giving 66 hidden-side rows.

The role-family model used only the two visible side roles and the known three-role inventory (role families are bookkeeping labels for the three kinds of side text in this series):

```text
role_861_003
role_700_03x
role_15x_003
```

The exact-text model then predicted the most common exact text for the missing role from the other 21 objects.

Baselines:

```text
side-index majority text
global majority text
```

## Result

```text
objects: 22
hidden-side predictions: 66
role-family predictions correct: 66/66
exact-text predictions correct: 64/66
side-index majority correct: 47/66
global majority correct: 22/66
accepted decipherment claims: 0
```

The two exact-text failures are exactly the two singleton minimal-contrast variants:

| Object | Hidden side | Role | Actual | Role-majority prediction | Consequence |
| --- | ---: | --- | --- | --- | --- |
| `H-2237` | 3 | `role_15x_003` | `+154-003+` | `+156-003+` | Singleton `154/156` variant. |
| `H-2238` | 1 | `role_700_03x` | `+700-033+` | `+700-034+` | Singleton `033/034` variant. |

## Interpretation

Within H-2218 through H-2239, the side inventory behaves like a constrained three-slot formula. The two singleton variants preserve the role family but break exact-text majority reconstruction.

That is the point: the current catalog-side layer does not make the variants disappear as random noise. It isolates them as the only exact-text breaks inside an otherwise reconstructable role inventory.

## Downgrade And Kill Boundaries

Locke — the team's adversarial reviewer — warns that this experiment can look fancier than it is if we let it. The warning matters here.

This result is downgraded if:

```text
the source side order is editorial rather than physical
the 22 objects are copied/template products rather than independent attestations
the diagnostic 154/156 or 033/034 strokes fail under source images
the invariant sides are not source-invariant
the pattern does not recur outside this H-series batch
```

This result is killed as slot-grammar evidence if source images show:

```text
side assignments are wrong
sign identities are wrong
the variants are damage, reconstruction, or catalog normalization artifacts
role families cannot be separated without hand-grouping
```

## Claim Status

Strongest safe wording:

```text
The series contains a source-targeted, internally reconstructable three-role formula with two singleton exact-text variants.
```

Forbidden upgrades from this experiment:

```text
meaning
phonetic value
word or morpheme
commodity, measure, tax, license, owner, title, or administrative reading
generalization beyond H-2218 through H-2239
```

Accepted claims:

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted numerical values: 0
accepted side functions: 0
accepted source mappings from this experiment: 0
```
