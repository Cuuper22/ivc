# Vector 4 `158-806 / Phyt` source-family closure gate

Date: 2026-07-12 America/Los_Angeles

Status: fixed adjudication snapshot pending execution. Its current inputs deterministically close the queue item; genuinely new evidence requires a new dated gate.

## What this is and why it exists

This is a gate: a written pass/fail test a candidate must clear before the project builds on it. This one closes a candidate rather than promoting it.

The candidate is an association between the sign pair `158-806` and `Phyt`, an iconographic label inherited from catalogue metadata. It looked interesting because a null test — reshuffling the labels to see how often chance alone reproduces the pattern — rarely reproduced it. But a low null share only says the pattern is unlikely under shuffling. It says nothing about how many independent objects stand behind the pattern, and that is the question this gate asks.

Support is the count of distinct exact text families behind a candidate. Here it is `3`, against a floor of `5` fixed before any of this was looked at. That alone closes the item, and the source check below explains why the count cannot honestly be raised by grouping the objects differently.

The gate exists mainly to stop the recycling. Without a written closure, a weak correlation with a tempting label gets rediscovered every few months and re-enters the queue as though it were new.

## Why this gate exists

The May 31 targeted null run left one narrow queue item: `158-806 / Phyt`. Its harsh exact-text collapse had support `3` and a worst fixed-pair null tail share of `0.0075`, but the broad scanner's minimum support was `5`. It was never an accepted meaning. The remaining annotation was to source-check the three text families before either reopening or closing it.

## Fixed witnesses

A witness is one catalogue row that carries the candidate. They are grouped by exact text family, because rows with identical text are not independent evidence for each other.

| Exact text family | Catalogue rows | Conservative form/motif sensitivity stratum |
| --- | --- | --- |
| `400-158-806-475` | H-1980 | Kenoyer and Meadow list H-1979, H-1980, and H-1981 as examples of the almost-cylindrical form. |
| `740-158-806-467` | H-1979 | Same form stratum; this does not demonstrate copying or a common production source. |
| `158-806-465` | H-1104, H-1105, H-190, H-724, H-726 | Parpola groups these objects by recurring text and sacred-tree reverse motif. This does not demonstrate one mold or source. |

Kenoyer and Meadow also warn generally that Harappan tablets include copies of the same signs or motifs, and duplicate bas-reliefs made from molds. That warning is the whole problem in one sentence: objects made from the same mold are one piece of evidence wearing several faces. The snapshot therefore reports a two-stratum sensitivity analysis — one grouping by form and motif, one not — to show how much the answer depends on that choice. The closure itself does not depend on it. Exact-text support is `3`, below the floor of `5` fixed beforehand.

## Pre-registered decision rule

Pre-registered means these conditions were written before the outcome, so the bar cannot be lowered to fit what turned up. Reopening with genuinely new evidence requires all four:

1. at least five exact-text families;
2. at least five source-independent witnesses after an explicit independence audit;
3. a source-grade token-box panel for every text family;
4. a fixed matched-iconographic-negative packet.

If any condition fails, close the item as `closed_not_claim_eligible_support_below_floor_source_independence_unresolved`. Do not rerun the old targeted null. Its question is already answered, and resampling the same rows cannot create independent witnesses — the shortage is objects, not iterations.

## Artifacts

- runner: `research/data/open_prototype/tools/vector4_158806_source_family_gate_20260712.mjs`
- witness table: `research/data/open_prototype/reports/vector4_158806_source_family_gate_20260712_witnesses.csv`
- summary: `research/data/open_prototype/reports/vector4_158806_source_family_gate_20260712_summary.json`

The runner validates all seven catalogue rows against the clean Lipi planning layer, checks the pinned null result, checks that both published text extractions still contain the cited series statements, hashes every input, and then emits the decision.

## Evidence boundary

`Phyt` is inherited iconographic metadata — somebody else's description of a motif, carried along in the catalogue. It is not a decoded meaning, and pairing it with a sign string does not make it one.

Closing this queue item changes no accepted count. All it does is stop a weak, source-dependent correlation from being recycled as though it were live semantic evidence.
