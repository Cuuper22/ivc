# Vector 4 `158-806 / Phyt` source-family closure gate

Date: 2026-07-12 America/Los_Angeles

Status: fixed adjudication snapshot pending execution. Its current inputs deterministically close the queue item; genuinely new evidence requires a new dated gate.

## Why this gate exists

The May 31 targeted null run left one narrow queue item: `158-806 / Phyt`. Its harsh exact-text collapse had support `3` and a worst fixed-pair null tail share of `0.0075`, but the broad scanner's minimum support was `5`. It was never an accepted meaning. The remaining annotation was to source-check the three text families before either reopening or closing it.

## Fixed witnesses

| Exact text family | Catalogue rows | Conservative form/motif sensitivity stratum |
| --- | --- | --- |
| `400-158-806-475` | H-1980 | Kenoyer and Meadow list H-1979, H-1980, and H-1981 as examples of the almost-cylindrical form. |
| `740-158-806-467` | H-1979 | Same form stratum; this does not demonstrate copying or a common production source. |
| `158-806-465` | H-1104, H-1105, H-190, H-724, H-726 | Parpola groups these objects by recurring text and sacred-tree reverse motif. This does not demonstrate one mold or source. |

Kenoyer and Meadow also warn generally that Harappan tablets include copies of the same signs or motifs and duplicate bas-reliefs made from molds. The snapshot therefore reports a two-stratum sensitivity analysis, but the decisive closure does not depend on that grouping: exact-text support is `3`, below the already fixed floor of `5`.

## Pre-registered decision rule

Reopening with genuinely new evidence requires all four conditions:

1. at least five exact-text families;
2. at least five source-independent witnesses after an explicit independence audit;
3. a source-grade token-box panel for every text family;
4. a fixed matched-iconographic-negative packet.

If any condition fails, close the item as `closed_not_claim_eligible_support_below_floor_source_independence_unresolved`. Do not rerun the old targeted null, because its question is already answered and repeated resampling cannot create independent witnesses.

## Artifacts

- runner: `research/data/open_prototype/tools/vector4_158806_source_family_gate_20260712.mjs`
- witness table: `research/data/open_prototype/reports/vector4_158806_source_family_gate_20260712_witnesses.csv`
- summary: `research/data/open_prototype/reports/vector4_158806_source_family_gate_20260712_summary.json`

The runner validates all seven catalogue rows against the clean Lipi planning layer, checks the pinned null result, checks that both published text extractions still contain the cited series statements, hashes every input, and then emits the decision.

## Evidence boundary

`Phyt` is inherited iconographic metadata, not a decoded meaning. A closed queue item changes no accepted count. It only prevents a weak, source-dependent correlation from being repeatedly recycled as if it were live semantic evidence.
