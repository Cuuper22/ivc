# 032-002 861 Source-Token Attachment Campaign

Date: 2026-05-28

## Question

This note records an image-level check on six inscriptions. We are asking a simple physical question: on the actual published photographs, does the candidate tail sit on the same line as the rest of the row? Numbers like `861` are sign IDs; a "tail" is the material after `861` at the end of a row.

The corpus scan narrowed the live post-`861` candidates to:

```text
861-533-717
861-255-416
861-603
```

This campaign checks six public-source rows selected from the current restricted-tail candidate set:

```text
M-376 / M-391: 861-533-717
M-91:          861-255-416
M-240 / M-714 / M-1273: 861-603
```

The test is source-level, not translational: do the public source panels preserve a same-line terminal-side continuation candidate, or is the candidate interrupted by side split, visible fusion, or catalog-order artifact — a case where the catalog's transcription order does not match the object?

## Stored Outputs

```text
tmp/run_032_002_861_source_token_attachment.py
data/open_prototype/reports/campaign_032_002_861_source_token_attachment_verdicts.csv
data/open_prototype/reports/campaign_032_002_861_source_token_attachment_boxes.csv
data/open_prototype/reports/campaign_032_002_861_source_token_attachment_summary.json
tmp/032_002_861_source_token_attachment/032_002_861_source_token_attachment_contact_sheet.png
```

The overlay windows drawn on the images are broad visual windows:

```text
purple = visible line
green  = pre-tail / 861-side candidate window
orange = terminal-side tail candidate window
```

They are not accepted exact token boxes — they do not claim to mark exact sign boundaries.

## Verdict Table

| row | tail | source verdict | confidence | reason |
|---|---|---|---|---|
| `M-376` | `533-717` | same-line candidate present | medium | A/a witnesses show one continuous row; terminal-side cluster is graphically separated from the preceding cluster |
| `M-391` | `533-717` | same-line candidate present, long row | medium-low | continuous long source row; terminal-side material remains on the same line, but blur/crowding blocks a stronger boundary claim |
| `M-91` | `255-416` | same-line singleton candidate present | medium-low | one continuous signband; singleton and low resolution keep it weak |
| `M-240` | `603` | same-line candidate present | medium | prior order window shows a seven-sign band with a separated terminal-side candidate |
| `M-714` | `603` | same-line candidate present, crowded | medium-low | top signband is continuous, but crowded and partly low-contrast |
| `M-1273` | `603` | same-line candidate present, strongest `603` witness | medium-high | short five-sign row with crisp separated graphic units |

## Result

In all six focus rows, the public panel preserves a same-line terminal-side candidate and shows no obvious side split or graphic fusion in the checked crop.

Output-backed grouping:

```text
533-717 = 2 same-line source-window rows: M-376, M-391
255-416 = 1 same-line source-window row: M-91
603     = 3 same-line source-window rows: M-240, M-714, M-1273
```

The public source layer still does **not** accept:

```text
exact source-normalized 861/tail token boundaries
source-derived direction policy
sign values
phonetic readings
language identity
translation
```

## Source Admissibility Notes

The source layer is clean for page/object routing — we can trace each row to its published page. But the icon/register layer (the animal icon and object-class labels attached to each seal) is not equally clean:

```text
M-376: CISI no-iconography III, local None. No immediate icon conflict.
M-391: CISI no-iconography III, local None. No immediate icon conflict.
M-91:  CISI unicorn IV, local Bull1:S. Icon label conflict.
M-240: CISI bison, local Gaur. Icon label conflict.
M-714: CISI unicorn III, local Bull1:W. Icon label conflict.
M-1273: CISI no-iconography II, local None. No immediate icon conflict.
```

So `533-717` can currently be discussed as a repeated no-icon `SEAL:R` candidate, but `603` cannot yet be given a stable icon/register interpretation from local labels alone.

## Interpretation Inputs, Not Decisions

These observations feed the next linguistic campaign. They decide nothing by themselves.

1. **Addendum input**

   The same-line windows are short and terminal-side in the six checked rows.

2. **Subclass input**

   `533-717` has two Mohenjo-daro `SEAL:R` no-icon rows. `603` crosses into rows with different icon/register metadata and also has a non-`861` corpus profile.

3. **Boundary / second-unit input**

   The packet does not show a phrase-scale visual break, but exact source-token boundaries are still catalog-mediated — they rest on the catalog transcription, not the image. A continuous second unit remains possible.

4. **Compound / segmentation-artifact input**

   The checked public crops do not show obvious fusion, but higher-resolution or blind token-boundary checks are still required before rejecting this explanation.

## Next Test

Do a matched terminal-control campaign — compare the tailed rows against rows that end bare at the same point:

```text
terminal 002-861
vs
002-861-603
vs
002-861-533-717
```

Use same-site/type/icon controls where possible, especially Mohenjo-daro `SEAL:R` no-icon rows around `M-376/M-391`. The immediate question is whether the tail rows differ distributionally from bare terminal `002-861` after those controls.
