# 032-002 861 Bare-Edge Source Controls

Date: 2026-05-29

This note collects photographs of the seals that end plainly. Some inscriptions stop right after `002-861`; others add a tail. To argue that the tail is a choice, we need to see the plain ones on real published images and confirm they show a clean edge — not a broken corner or a worn patch where a tail might once have been. This pass acquired six such bare controls and records which lanes they cover and which are still missing.

## Question

The matched-controls campaign showed that tailed `002-861-*` rows have bare terminal `002-861` controls in comparable lanes. A "control" is a comparison row sharing the setting but not the feature under test; "bare" means the inscription stops right after `002-861`; a "lane" is a specific left-to-right pattern of the signs immediately before `002-861`.

This campaign asks the source-level version — the version answered by looking at images rather than trusting the catalogue:

```text
visible bare 002-861 edge
vs
visible 002-861-tail edge
```

The output is a source-layout input to the linguistic model: it records whether comparable bare rows have visible terminal-side windows — inspectable regions at the end of the line, where a tail would sit if there were one — that can be compared with the already checked tailed rows.

## Stored Outputs

```text
tmp/run_032_002_861_bare_edge_source_controls.py
data/open_prototype/reports/campaign_032_002_861_bare_edge_source_controls_rows.csv
data/open_prototype/reports/campaign_032_002_861_bare_edge_source_controls_crops.csv
data/open_prototype/reports/campaign_032_002_861_bare_edge_source_controls_summary.json
tmp/032_002_861_bare_edge_source_controls/032_002_861_bare_edge_source_controls_contact_sheet.png
```

## Source-Visible Bare Controls

| family | bare control | source route | comparison target | status |
|---|---|---|---|---|
| `220-032-002-861` | `H-444 +241-220-032-002-861+` | existing Pakistan source-function packet | `M-91 861-255-416`; `M-240 861-603` | source visible |
| `220-032-002-861` | `M-723 +740-460-510-235-220-032-002-861+` | CISI Pakistan IA leaf `n82`, printed p.48 | `M-91 861-255-416`; `M-240 861-603` | source visible this campaign |
| `220-032-002-861` | `M-1044 +520-220-032-002-861+` | CISI Pakistan IA leaf `n138`, printed p.104 | `M-91 861-255-416`; `M-240 861-603` | source visible this campaign |
| `803-002-861` | `M-77 +832-390-803-002-861+` | existing CISI India `n68` M-77 packet | `M-714 861-603` | source visible |
| `803-002-861` | `M-118 +740-772-033-705-233-803-002-861+` | CISI India IA leaf `n76`, printed p.41 | `M-714 861-603` | source visible this campaign |
| `176-002-861` | `M-15 +090-740-176-002-861+` | CISI India IA leaf `n46`, printed p.11 | `M-376 861-533-717` | source visible this campaign |

Pending controls:

```text
M-1763 220-032-002-861
M-1880 176-002-861
M-1755 176-002-861
M-2060 176-002-861
```

These are not discarded. They remain route targets, mostly because the local CISI OCR pass either did not locate a public panel or only hit data/register pages.

## Result

The three active matched lanes now have public source-visible bare edges:

```text
220-032 lane: H-444, M-723, M-1044
803 lane:     M-77, M-118
176 lane:     M-15
```

This adds source-visible controls to the `861` tail contrast.

The tailed rows already checked source-visible same-line material:

```text
M-91   002-861-255-416
M-240  002-861-603
M-714  002-861-603
M-376  002-861-533-717
M-391  002-861-533-717
M-1273 002-861-603
```

The bare controls now record visible terminal-side windows in comparable catalog-terminal rows. That makes the post-`861` zone a concrete comparison target instead of only a suffix-table residue — the leftover material at the end of a table, noticed but never examined.

## Hypotheses To Test

Current hypotheses from the wider `861` campaign:

```text
1. 861 closes a core phrase and some rows add a following tag/addendum
2. bare/expanded rows mark a subclass or register contrast
3. 861 is a boundary followed by an appended unit
4. catalog segmentation or compound handling creates part of the contrast
```

What this source packet adds:

| model | effect of this campaign |
|---|---|
| closure + addendum | the same broad lanes now have source-visible bare rows and source-visible tailed rows |
| subclass/register marker | still has to be tested against lane/context sorting, especially `176 -> 533-717` and `803 -> 603` |
| boundary + appended unit | needs spacing evidence or independent tail behavior before it can rise |
| compound/segmentation artifact | remains possible because exact token boundaries are still catalog-mediated |

## Limits

```text
Exact source-normalized 861/002 boundaries are not accepted for every control.
The M-15 source heading/icon layer differs from local symbol metadata, so it is used for line/edge behavior only.
M-77 and H-444 reuse earlier source packets; this campaign does not redo their full panel acquisition.
Addendum vs subclass vs apposition is not decided.
No sign value, phonetic reading, language identity, or translation is accepted.
```

## Next Research Move

Run the model as a batch over all repeated post-`861` tails, not only these six rows:

```text
861-603
861-533-717
861-416
861-698
861-096
861-000
```

For each tail family, ask:

```text
Does the tail have bare matched controls?
Does the tail recur outside 861?
Does it sort by prefix lane, object type, icon/register, or site?
Does it behave like a free mini-formula elsewhere?
```

This is the next campaign unit: tail families as the comparison set, not one-sign adjudications.
