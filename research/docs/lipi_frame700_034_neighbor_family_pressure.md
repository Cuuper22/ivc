# Lipi FRAME700 034 Neighbor Family Pressure

Date: 2026-05-25

## Question

This note checks the company each blocked object keeps. FRAME700 is the project's label for short inscription rows built on sign `700`, such as `+700-034+`; the `034` work asks whether the sign codes `032`, `033`, and `034` are separate choices in the same slot. Several objects in that test are blocked on unresolved catalog labels. If a blocked object also sits among near-identical inscriptions, a mistake in mapping it to a catalog page would spread. A copy family is a set of objects carrying the same inscription that may be copies of one another; a neighborhood is the set of catalog-adjacent objects sharing tokens with it. The question: do the current `032/033/034` blocker objects look isolated in the local corpus layer, or are they sitting inside repeated/copy-family neighborhoods that make source contamination more likely?

This is a local-corpus pressure test, not source validation. It does not replace CISI 3.1 — the Corpus of Indus Seals and Inscriptions, volume 3.1 — or archive-object notes.

## Inputs

- Local filtered metadata: `data/open_prototype/lipi/metadata_filtered.csv`
- Prior source gate, a gate being a checkpoint the evidence must pass before the next step is allowed: `docs/lipi_frame700_034_source_note_panel_graph.md`
- Script: `data/open_prototype/tools/lipi_frame700_034_neighbor_family_pressure.mjs`
- CSV: `data/open_prototype/reports/lipi_frame700_034_neighbor_family_pressure.csv`
- Summary: `data/open_prototype/reports/lipi_frame700_034_neighbor_family_pressure_summary.json`

## Result

```text
target/control objects checked: 9
exact copy-family pressure objects: 1
high-repetition family pressure objects: 1
companion-context repetition pressure objects: 0
local-neighborhood pressure objects: 6
low-copy or isolated objects: 1
accepted readings: 0
```

## Object Pressure

A control here is a comparison object used to check a target, and a triad is a set of three objects, one per sign code.

| Object | Local pressure | Consequence |
| --- | --- | --- |
| `H-771` | Local-neighborhood pressure. | Nearby H-number objects share at least two tokens, so source note priority stays high and local adjacency cannot rescue the same-side photo-selection blocker. |
| `H-789` | Local-neighborhood pressure control. | Still only a clean calibration control; no subtype or direction reading follows. |
| `H-1123` | Low-copy/isolated in the local layer. | The object is not page-addressable in the checked IA OCR route, and local family evidence gives little rescue. |
| `H-893` | Local-neighborhood pressure. | The unresolved `H-893 (1)` source label cannot be explained away by local repetition or catalog adjacency. |
| `H-925` | Exact copy-family pressure. | Source request must include its local exact family, not only `H-925`; shared-control contamination risk increases. |
| `H-930` | Local-neighborhood pressure control. | Still only a calibration control because neighborhood recurrence is not source validation. |
| `H-983` | Local-neighborhood pressure. | The `C`-side hazard remains object-specific and cannot be dismissed by adjacent prism/`034` material. |
| `H-353` | High repetition-family pressure. | It belongs to a broad `+400-740-176+ / +700-033+` family, so its `C` side must be handled as a family/source-policy issue, not an isolated nuisance. |
| `H-2211` | Local-neighborhood pressure. | Needs source-normalized side labels before it can act as a `032` control; nearby token overlap is only a pressure flag. |

## Research Consequence

The local layer does not open a translation lane. It sharpens the source plan:

1. `H-925` is dangerous as a shared `033` control because local exact-family pressure means a wrong source mapping would contaminate several triads.
2. `H-353` is dangerous because it is embedded in a repeated `400-740-176 / 700-033` family while the source page exposes a `C` side.
3. `H-771`, `H-893`, `H-983`, and `H-2211` show local-neighborhood pressure, so catalog adjacency must be treated as a possible contamination/confound rather than evidence.
4. `H-1123` is the only low-copy/isolated target in this pass and remains a source-acquisition priority for the `032` control slot.

## Claim Status

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted side functions: 0
accepted FRAME700 subtype readings from this artifact: 0
```
