# Lipi FRAME700 `034` Clean Two-Panel Close-Read

Date: 2026-05-25

## Question

Do the two cleanest IA CISI page locators, `H-930` and `H-789`, survive a closer source-image read strongly enough to serve as calibration controls for the next `034` source attack?

## Inputs

- Prior locator table: `data/open_prototype/reports/lipi_frame700_034_ia_cisi_page_locator.csv`
- Prior visual inspection: `data/open_prototype/reports/lipi_frame700_034_ia_cisi_visual_inspection.csv`
- Close-read output: `data/open_prototype/reports/lipi_frame700_034_clean_two_panel_close_read.csv`
- Summary: `data/open_prototype/reports/lipi_frame700_034_clean_two_panel_close_read_summary.json`

Temporary page images were downloaded from the Internet Archive for inspection and are not source artifacts in this repository.

## Result

```text
objects close-read: 2
source panel count matches local side count: 2
short panel candidate on printed B: 2
companion panel candidate on printed A: 2
accepted decipherment claims: 0
```

| Object | Role | Source page | Close-read result |
| --- | --- | --- | --- |
| `H-930` | `032` control | CISI Pakistan leaf `374`, `HARAPPA 927-942 TABLETS incised no iconography` | Best current calibration control. `H-930 A` is compatible with the longer companion row `+740-900-004+`; `H-930 B` is compatible with the short row `+700-032+`. The scan supports object identity, two panels, and short-vs-long split, not independent subtype or direction. |
| `H-789` | `033` control | CISI Pakistan leaf `359`, `HARAPPA 778-793 TABLETS in bas-relief no iconography` | Independent-lane clean control. `H-789 A` is compatible with longer companion `+400-520-220-016+`; `H-789 B` is compatible with short row `+033-700+`. Stroke confidence is lower than `H-930`, so it stays a control, not subtype validation. |

## What This Actually Adds

This is not another acquisition scaffold. It is a source-image calibration result.

`H-930` and `H-789` can now be treated as clean two-panel controls for:

- object identity at the IA CISI plate level;
- source panel count matching local side count;
- printed `A`/`B` labels being catalog-compatible with longer companion side and shorter FRAME700 side;
- low copy-variant risk on their pages.

They cannot be used for:

- accepting `032` or `033` from visual stroke diagnostics;
- normalizing direction;
- equating printed `A`/`B` with physical side order;
- assigning any function, sign meaning, phonetic value, or translation.

## Research Consequence

`H-930` is now the calibration object for the strict local contrast lane. It should be used to set the visual standard before attempting `H-893` and `H-925`, where variants and copy panels are the actual danger.

`H-789` is now the calibration object for the independent lane. It can be paired against `H-771` only after `H-771`'s multiple `A` impressions are disambiguated.

The close-read changes the next source-gate from "find images" to "prove the messy targets can meet the standard set by these two controls."

That gate has now been run in [Lipi FRAME700 034 messy panel reconciliation](lipi_frame700_034_messy_panel_reconciliation.md). `H-771`, `H-893`, `H-925`, `H-983`, and `H-353` all fail clean upgrade until source-side variants and extra panels are reconciled.

## Source Discipline

The catalog rows remain catalog data:

```text
H-930: +700-032+
H-789: +033-700+
```

The source images currently support clean control status only. They do not establish those sign identities from scratch.
