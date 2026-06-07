# Lipi FRAME700 034 Messy Panel Reconciliation

Date: 2026-05-25

## Question

Do the five messy IA CISI source objects survive the same clean close-read standard used for `H-930` and `H-789`?

## Inputs

- Prior gate: [Lipi FRAME700 034 IA CISI visual inspection](lipi_frame700_034_ia_cisi_visual_inspection.md)
- Calibration gate: [Lipi FRAME700 034 clean two-panel close-read](lipi_frame700_034_clean_two_panel_close_read.md)
- Script: `data/open_prototype/tools/lipi_frame700_034_messy_panel_reconciliation.mjs`
- CSV: `data/open_prototype/reports/lipi_frame700_034_messy_panel_reconciliation.csv`
- Summary: `data/open_prototype/reports/lipi_frame700_034_messy_panel_reconciliation_summary.json`

No IA page image is stored as a research artifact.

## Result

```text
objects checked: 5
objects meeting H-930/H-789 clean standard: 0
visible photo/side label count exceeds local side count: 5
variant, photo-selection, numbered-label, or extra-side failures: 5
single B short candidate visible: 2
multiple B short candidates visible: 3
accepted decipherment claims: 0
```

## Object-Level Decisions

| Object | Lane role | Source panels visible | Local sides | Decision |
| --- | --- | ---: | ---: | --- |
| `H-771` | independent `034` target | 5 | 2 | B short candidate visible, but four A-labeled photographs block companion mapping. |
| `H-893` | strict-local `034` target | 4 | 2 | Base A/B and numbered `(1)` A/B are both visible; the source panel for local `+700-034+` is unresolved. |
| `H-925` | strict-local `033` control | 9 | 2 | Shared control fails clean use because numbered, `bis`, and `ter` variants create high copy-variant pressure. |
| `H-983` | strict-local `034` target | 7 | 2 | A/B/C panels plus B/C variants expose a source C side suppressed by the local packet. |
| `H-353` | strict-local `033` control | 3 | 2 | B short candidate and A companion candidate are plausible, but source C is extra and blocks clean-control use. |

## What Is Established

Directly established from visible source pages:

- All five target/control objects have source labels visible on IA CISI plate pages.
- All five have more visible source photo or side labels than the local two-row packet records.
- `H-771` and `H-353` have plausible single B-side short candidates, but neither is a clean two-panel object at source level.
- `H-893`, `H-925`, and `H-983` have multiple B-labeled or variant short-panel candidates.

Inference, not accepted reading:

- The B panels are catalog-compatible short-side candidates in some cases.
- The local `+700-034+` and `+700-033+` rows may correspond to those B panels.
- This cannot be used as a subtype, direction, side-order, function, phonetic, semantic, or translation claim.

## Consequence

This is a real negative source result. `H-771`, `H-893`, `H-925`, `H-983`, and `H-353` cannot inherit the `H-930`/`H-789` calibration upgrade. The current `034` residue is still live as a distributional and source-targeting problem, but these five source objects remain unvalidated until panel identity and variant status are reconciled.

The next useful move is narrower than another broad audit:

1. Pull CISI notes or higher-resolution catalog metadata for the exact variant labels.
2. Resolve whether `bis`, `ter`, numbered, and C-side panels are copy variants, separate objects, alternate faces, or editorial duplicate impressions.
3. Only then re-open the strict comparisons `H-771/H-789/H-1123`, `H-893/H-925/H-930`, and `H-983/H-353/H-2211`.

The next linguistic experiment after that source work is a source-normalized panel graph. Each confirmed physical side, copy-equivalent panel, or separate catalog variant should become its own node before any `032`/`033`/`034` substitution test is allowed. The question then becomes whether those signs alternate in the same stable frame after source panel identity is fixed.

Update after CISI convention check:

[Lipi FRAME700 034 CISI variant convention probe](lipi_frame700_034_cisi_variant_convention_probe.md) refines this result. Under CISI convention, `bis`, `ter`, and `quater` are later photographs of the same side, not extra physical sides. The negative gate still stands, but the blockers split into same-side photo selection (`H-771`), true `C`-side hazards (`H-983`, `H-353`), and unresolved object-number labels (`H-893`, `H-925`).

## Claim Status

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted side functions: 0
accepted FRAME700 subtype readings from these source images: 0
```
