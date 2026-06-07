# Lipi 034 M-1206 H-938 Same-Object Source Panel Audit

Date: 2026-05-26

## Question

What does `H-938` actually support for the M-1206 `034/415` branch once the source panels are kept separate from local row numbers?

This is a source-language audit. The target is not a new app, OCR pipeline, or broad scrape. The question is whether one source-visible Harappa tablet can sharpen the sign-inventory problem around local `034` and `415`.

## Source Inputs

`H-938` is visible on CISI Pakistan leaf `n374`, printed page `340`, in the Harappa 927-942 tablets plate. The checked source page is:

```text
tmp/m1206_m37_blind_visual_comparanda/cisi_pakistan_n374_h939_h940_w2000.jpg
sha256: 121ccdd225452daa000a3ab058ad44259fed39d82b62b012a1e98035e6f465eb
```

The verified panel crops are:

| Panel | Local row | Local text | Crop | Status |
| --- | --- | --- | --- | --- |
| `H-938 A` | `1818.1` | `+520-220-415+` | `tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H938_A_panel.png` | clean exact-source-side `415` control |
| `H-938 A bis` | `1818.1` | `+520-220-415+` | `tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H938_A_bis_panel.png` | duplicate photo of the same A side |
| `H-938 B` | `1818.2` | `+034-700+` | `tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H938_B_panel.png` | companion-side pressure only |

The machine-readable panel audit is:

```text
data/open_prototype/reports/lipi_034_m1206_h938_same_object_source_panel_audit.csv
data/open_prototype/reports/lipi_034_m1206_h938_same_object_source_panel_audit_summary.json
```

## Adjudication

`H-938 A/A bis` remains the strongest clean external `415` terminal pressure for the M-1206 branch. The `bis` label is another photograph of side `A`, so it improves visibility but does not create an independent witness.

`H-938 B` matters for a different reason: it is the same object's companion side and carries local `+034-700+`. That creates source-visible within-object `034/415` proximity pressure:

```text
H-938 A/A bis: +520-220-415+
H-938 B:       +034-700+
```

The pressure is real, but it is not identity. The two rows have different local roles: `1818.1` is a longer `MT` row in the `520-220-X` frame; `1818.2` is a short `NV` `FRAME700` companion. This blocks a direct `034 = 415` move.

## What It Supports

- `H-938 A/A bis` as clean exact-source-side `415` visual control.
- `H-938 B` as same-object `+034-700+` companion evidence.
- A sharper sign-inventory question: are local `034` and `415` separate signs, allographs, graphic-family variants, source-side artifacts, or transcription-policy splits?

## What It Does Not Support

- `034 = 415`.
- Proven allography.
- A stable `415` fine form.
- Any semantic value, phonetic value, object-class value, animal/species value, or translation.
- Counting `H-938 A bis` as a second object-level recurrence.
- Treating local `.1/.2` side ordinals as globally equivalent to CISI `A/B`.
- Treating `+034-700+` versus `+700-034+` order as meaningful before direction and side-policy closure.

## Comparanda Weighting

`H-940` is the key negative companion check: it has clean exact-side `+520-220-415+`, but its companion is `+110+`, not `+034-700+`. So `415` does not automatically imply a `034/700` partner.

`H-939` and `H-1284` have local pairings involving `+520-220-415+` and `+700-034+`, but they do not upgrade the claim here. `H-939` failed to become a secure source-panel recurrence in the strict visual packet, and `H-1284` is still source-route dark in the checked public layer.

`M-1206` remains the source-visible `+520-220-034+` target. `M-37` remains a source-visible same-site `+520-220-415+` control, but its cleaned terminal is a comb/rake-with-stem subform rather than the closest M-1206 vertical-bundle match.

## Decision

`H-938` is now explicitly recorded as source-visible same-object proximity pressure:

```text
clean exact-side 415 control + companion 034-700 side
```

That strengthens the unresolved `034/415` sign-inventory problem. It does not settle it.

Accepted mappings: `0`

Accepted values: `0`

Accepted translations: `0`
