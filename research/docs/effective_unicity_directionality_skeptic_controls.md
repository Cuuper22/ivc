# Effective-Unicity Directionality Skeptic Controls

Date: 2026-05-29

## Purpose

This note records the hostile follow-up controls for the Vector 2 directionality candidate. It does not replace the broad directionality comparator. It tests two tempting support lanes that could easily mislead the analysis:

- a tiny source-visible `861` terminal/tail subset,
- the provisional matched Lipi/Mayig overlap rows.

Both are support-lane tests, not decipherment tests. No phonetic value, translation, sign meaning, or language-family claim follows.

## Result

The tiny source-visible `861` probe is killed as directionality evidence. The observed stored-win share is 1.000000 over 12 target-selected rows, but the strongest null reproduces or exceeds that score with `null >= observed` share 1. It remains a source-visible sensitivity inventory only.

The matched-overlap result is also not admissible support for the directionality candidate. In the exact-collapsed overlap, the Lipi side remains high at 0.937500 with max null >= observed share 0.035000, but the Mayig side is already soft at 0.929134 with max null >= observed share 0.200000. After removing the ten most frequent edge signs, both overlap sides collapse: Lipi side 0.363636 and Mayig side 0.473684, each with max null >= observed share 1.

The broad harsh Indus directionality candidate is not killed by this run, because these controls were scoped to the source-visible `861` subset and matched overlap rows. What is killed is the earlier sentence that matched overlap “shows the order signal in both namespaces” as independent support.

## Primary Rows

| Probe | Scope | Rows | Tokens | Stored win share | Max null >= observed |
| --- | --- | ---: | ---: | ---: | ---: |
| source-visible `861` terminal/tail | tailed and bare source-visible rows | 12 | 87 | 1.000000 | 1 |
| matched overlap, Lipi side | exact-collapsed | 128 | 661 | 0.937500 | 0.035000 |
| matched overlap, Mayig side | exact-collapsed | 127 | 657 | 0.929134 | 0.200000 |
| matched overlap, Lipi side | top-10-edge removed | 22 | 96 | 0.363636 | 1 |
| matched overlap, Mayig side | top-10-edge removed | 19 | 80 | 0.473684 | 1 |

Strongest overlap null attack:

| Corpus | Scope | Control | Observed | Null mean | Null >= observed |
| --- | --- | --- | ---: | ---: | ---: |
| matched overlap, Lipi side | top-10-edge removed | edge-symbol-catalog-position shuffle | 0.363636 | 0.363636 | 1 |

## Controls

The run uses 200 iterations per null control. Standard controls are:

- global token shuffle,
- row-internal shuffle,
- position-slot shuffle,
- edge-frame shuffle.

For matched overlap, the skeptic controls add block-conditioned variants:

- edge-length-position shuffle,
- edge-symbol-catalog-position shuffle,
- edge-symbol-catalog-interior shuffle.

These preserve more of the overlap rows' confounding structure: edge signs, row length, position, symbol/type/material block, and catalog block where available.

## Decision

Retract these support lanes:

- source-visible `861` terminal/tail directionality as evidence,
- matched Lipi/Mayig overlap as independent support for the directionality candidate.

Keep the broader harsh Indus directionality candidate live but unaccepted. It still needs source-normalized direction validation, stronger near-duplicate/source-family collapse, and crosswalk-blind heldout rebuilding before it can promote anything in the claim ledger.

## Artifacts

- `data/open_prototype/tools/effective_unicity_directionality_skeptic_controls.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_skeptic_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_skeptic_controls.csv`
- `data/open_prototype/reports/effective_unicity_directionality_skeptic_null_summary.csv`
- `data/open_prototype/reports/effective_unicity_directionality_skeptic_null_iterations.csv`
- `data/open_prototype/reports/effective_unicity_directionality_source_visible_861_rows.csv`
