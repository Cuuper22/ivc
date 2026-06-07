# Lipi 034 M-1206 H-319/H-1284 Source-Route Recheck

Date: 2026-05-26

## Question

The companion-context inventory found four local exact `+520-220-415+` objects with same-object `034/700` companions:

```text
H-319   1341.1 +520-220-415+   1341.2 +700-034+
H-938   1818.1 +520-220-415+   1818.2 +034-700+
H-939   1819.2 +520-220-415+   1819.1 +700-034+
H-1284  4069.1 +520-220-415+   4069.2 +700-034+
```

`H-938` is already source-panel-audited. This recheck asks whether `H-319` or `H-1284` can be upgraded from local pressure to source-grade same-object evidence.

## Result

No upgrade.

`H-319` now has a confirmed public route, but it is only a CISI India data/register page, not an inscription plate. The downloaded `n406` and `n837` pages are byte-identical duplicates. They show the `H-319` register row on printed page 371, but they do not show the inscribed sides, source side labels, direction basis, or segmentation. That means `H-319` is a better acquisition target, not evidence.

`H-1284` remains source-route dark in the checked public CISI 1/2 layer. The local OCR/XML layer has no exact `H-1284` object route. Bare `1284` and `4069` hits are noisy or refer to other catalog contexts. A secondary Parpola 2019 clue groups `H-1284` with `H-938`, `H-939`, and `H-2145` in a Harappa incised-tablet discussion, but that is not a substitute for a source image.

## Source Artifacts

| Object | Local rows | Recheck result | Stored artifacts |
| --- | --- | --- | --- |
| `H-319` | `1341.1 +520-220-415+`; `1341.2 +700-034+` | CISI India `n406/n837`, printed p. 371, data/register only; no source panel. | `tmp/h319_h1284_source_route_recheck/cisi_india_n406_h319_register_w2000.jpg`; `tmp/h319_h1284_source_route_recheck/cisi_india_n837_h319_register_w2000.jpg`; `tmp/h319_h1284_source_route_recheck/cisi_india_n406_h319_register_row_crop2.png` |
| `H-1284` | `4069.1 +520-220-415+`; `4069.2 +700-034+` | No exact public CISI 1/2 route in checked layer; secondary literature clue only. | `tmp/parpola_2019_bone_rods.txt` |
| `H-938` | `1818.1 +520-220-415+`; `1818.2 +034-700+` | Clean source-panel-audited control. | See `lipi_034_m1206_h938_same_object_source_panel_audit.md` |
| `H-939` | `1819.2 +520-220-415+`; `1819.1 +700-034+` | Source-visible on the H-938 page cluster, but not strict-upgraded. | `tmp/m1206_m37_blind_visual_comparanda/cisi_pakistan_n374_h939_h940_w2000.jpg` |

Report files:

```text
data/open_prototype/reports/lipi_034_m1206_h319_h1284_source_route_recheck_sources.csv
data/open_prototype/reports/lipi_034_m1206_h319_h1284_source_route_recheck_adjudication.csv
data/open_prototype/reports/lipi_034_m1206_h319_h1284_source_route_recheck_summary.json
```

## Admissible Interpretation

The repeated local pattern is real enough to prioritize source acquisition:

```text
1:+520-220-415+ | 2:+700-034+
```

appears locally for both `H-319` and `H-1284`, while `H-938` has the related clean source-panel pattern:

```text
1:+520-220-415+ | 2:+034-700+
```

But the language question does not move unless the source panels move. The current admissible claim is:

```text
H-319 and H-1284 are targeted source-acquisition objects for the M-1206 / 415 / 034 branch.
```

That is all.

## Blocked Claims

This recheck does not support:

- `034 = 415`.
- stable allography.
- a `415` value.
- a `034` value.
- a `700` role.
- same-object visual recurrence for `H-319` or `H-1284`.
- translation.

## Acquisition Packet

The next request should ask for plate-grade images or source panels for:

```text
H-319: all sides, with object bridge to source hook 10060544, side labels/order, inscription/impression direction, and segmentation.
H-1284: all sides, with object bridge to source hook -458, side labels/order, inscription/impression direction, and segmentation.
```

`H-2145` should be mentioned only as a related secondary-literature clue, not as a substitute target, because its local longer side is `+074-220-415+`, not exact `+520-220-415+`.

