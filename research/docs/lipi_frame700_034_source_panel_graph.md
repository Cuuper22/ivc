# Lipi FRAME700 `034` Source Panel Graph

Date: 2026-05-25

## Question

This note asks whether any set of objects is yet clean enough to run the real linguistic test on. FRAME700 is the project's label for short inscription rows built on sign `700`, such as `+700-034+`. The test is a substitution test: whether the sign codes `032`, `033`, and `034` alternate in the same stable slot. Running it needs a triad — three objects, one per code — and a panel graph, meaning a map with one node per confirmed physical side of an object, built from the source catalog rather than from local metadata. The catalog is CISI, the Corpus of Indus Seals and Inscriptions, read here through Internet Archive (IA) scans. The question: after the IA/CISI source checks and CISI label-convention probe, can any current `032/033/034` triad be treated as a source-normalized substitution test?

This is the next linguistic gate — a checkpoint the evidence must pass before the next step is allowed — after the messy-panel reconciliation. It asks whether catalog rows can be promoted into source-panel nodes before claiming that `032`, `033`, and `034` alternate in a stable frame.

## Outputs

```text
data/open_prototype/tools/lipi_frame700_034_source_panel_graph.mjs
data/open_prototype/reports/lipi_frame700_034_source_panel_graph_nodes.csv
data/open_prototype/reports/lipi_frame700_034_source_panel_graph_edges.csv
data/open_prototype/reports/lipi_frame700_034_source_panel_graph_triad_admissibility.csv
data/open_prototype/reports/lipi_frame700_034_source_panel_graph_summary.json
```

Inputs:

```text
data/open_prototype/reports/lipi_frame700_034_clean_two_panel_close_read.csv
data/open_prototype/reports/lipi_frame700_034_messy_panel_reconciliation.csv
data/open_prototype/reports/lipi_frame700_034_ia_cisi_visual_inspection.csv
data/open_prototype/reports/lipi_frame700_034_source_triad_packet.csv
```

## Result

```text
source objects in graph or locator map: 9
panel node rows: 34
local-to-source edge rows: 14
triad rows scored: 93
clean two-panel calibration objects: H-930; H-789
blocked panel-mapping objects: H-771; H-893; H-925; H-983; H-353
visual locator not close-read: H-910
register/nonvisual locator: H-212
source-normalized substitution triads: 0
accepted decipherment claims: 0
```

Triad admissibility:

| Status | Triads |
| --- | ---: |
| Missing source panel nodes | 75 |
| Blocked panel mapping or variant status | 12 |
| Register-only/nonvisual locator | 5 |
| Visual locator not close-read | 1 |

## What The Graph Establishes

`H-930` and `H-789` are clean calibration controls at the panel level — known-clean examples that set the visual standard the harder objects must meet:

| Object | Source panel mapping supported | Still not accepted |
| --- | --- | --- |
| `H-930` | `A` maps to longer companion candidate; `B` maps to short `+700-032+` candidate. | Independent `032` stroke diagnostics and direction. |
| `H-789` | `A` maps to longer companion candidate; `B` maps to short `+033-700+` candidate. | Independent `033` stroke diagnostics and direction. |

The messy objects do not pass:

| Object | Why it fails source-normalized substitution |
| --- | --- |
| `H-771` | `A/A bis/A ter/A quater` are same-side photo variants, but the companion photo choice and direction/subtype status remain unresolved. |
| `H-893` | Base `A/B` and `H-893 (1) A/B` are not reconciled. |
| `H-925` | Numbered forms plus `bis/ter` photo variants make the shared `033` control unsafe. |
| `H-983` | `C` is a real CISI side category, so the local two-side packet is incomplete. |
| `H-353` | `C` is a real CISI side category, so the local two-side packet is incomplete. |

## Decipherment Consequence

This is not another vague source request. It is a direct substitution gate, and the current answer is no:

```text
No current FRAME700 `034/033/032` triad can be used as a source-normalized sign-function contrast.
```

That does not kill the `034` residue — the leftover pattern that has survived the controls run so far. It kills the upgrade from distributional residue to source-normalized sign-function evidence under the current source state.

Research/adversarial critique agrees on the dangerous confounds:

1. Series or copy-family repetition can masquerade as sign function.
2. Catalog side labels, same-side photographs, numbered object forms, and direction conventions can manufacture a fake substitution frame.

So the next decisive experiment is a source-resolved cross-family substitution test. Count evidence by independent source family, not by row. A pass requires the `032/033/034` contrast to recur across multiple independent families after physical side nodes, photo witnesses, numbered groups, A/B/C side coverage, direction, diagnostic strokes, and copy-family status are resolved.

The next source target is therefore precise:

1. Get or inspect source panels for one full triad, not isolated objects.
2. For the `H-771/H-789/H-1123` independent lane — a lane being one of the separate evidence tracks the project runs, kept apart so a result in one does not lean on the other — resolve `H-771` A-photo selection and acquire `H-1123`.
3. For the `H-893/H-925/H-930` strict local lane, resolve `H-893 (1)` and `H-925 (1)/(2)` before using `H-930`.
4. For the `H-910/H-916/H-1294` repeated-branch lane, close-read `H-910` and acquire `H-916/H-1294`, but keep repetition pressure marked.

## Claim Status

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted side functions: 0
accepted FRAME700 subtype readings from this graph: 0
```
