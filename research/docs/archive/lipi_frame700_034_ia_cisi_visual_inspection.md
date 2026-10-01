# Lipi FRAME700 034 IA CISI Visual Inspection

Date: 2026-05-25

## Question

This note records what we saw when we actually opened the catalog pages. FRAME700 is the project's label for short inscription rows built on sign `700`, such as `+700-032+`; the `034` packet is the bundle of objects gathered to test whether the sign codes `032`, `033`, and `034` are separate choices in the same slot. An earlier note located those objects page by page in the Internet Archive (IA) scans of CISI, the Corpus of Indus Seals and Inscriptions — the standard photographic catalog of Indus objects. The question: what does the first manual visual pass over those located pages establish for the live `034` packet?

This pass only checks page/panel availability and reconciliation risk — whether the sides shown in the catalog can be squared with the sides our local records list. It does not validate `032`/`033`/`034` as accepted visual subtypes.

## Local Artifacts

```text
data/open_prototype/tools/lipi_frame700_034_ia_cisi_visual_inspection.mjs
data/open_prototype/reports/lipi_frame700_034_ia_cisi_visual_inspection.csv
data/open_prototype/reports/lipi_frame700_034_ia_cisi_visual_inspection_summary.json
```

The temporary inspected page images were kept under `tmp/ia_cisi_pages/` only. The stored research artifact keeps source pointers and observations, not copied plates.

## Result

```text
inspected objects: 9
core objects: 8
optional objects: 1
visual plate objects: 8
data-register-only objects: 1
source panel count matches local side count: 3
source panel count exceeds local side count: 5
high or variant risk objects: 7
accepted decipherment claims: 0
```

## Main Findings

The first IA pass did find real visual plate pages for most of the IA-hit queue.

Cleanest visual locators. In the packet role column, a target is an object the test is about, and a control is a comparison object used to check the target.

| Object | Packet role | Source observation | Consequence |
| --- | --- | --- | --- |
| `H-789` | `033` control | CISI Pakistan leaf `359` shows `H-789 A` and `H-789 B`. | Two labeled panels match the local two-side count; close sign inspection still needed. |
| `H-930` | `032` control | CISI Pakistan leaf `374` shows `H-930 A` and `H-930 B`. | Cleanest two-panel local-contrast control in this IA batch; subtype/direction not accepted. |
| `H-910` | optional `034` target | CISI Pakistan leaf `372` shows `H-910 A` and `H-910 B`. | Visually clean locator, but remains optional because the `+002-861-416+` branch is repetition pressured. |

Objects needing side-count or variant reconciliation:

| Object | Packet role | Source observation | Consequence |
| --- | --- | --- | --- |
| `H-771` | `034` target | CISI Pakistan leaf `358` shows `H-771 A`, `A bis`, `A ter`, `A quater`, and `B`. | Local two-side packet cannot be used until multiple `A` impressions/panels are mapped to the catalog rows. |
| `H-893` | `034` target | CISI Pakistan leaf `371` shows `H-893 A`, `B`, `H-893 (1) A`, and `(1) B`. | Variant `(1)` must be separated before this can upgrade the strict local contrast lane — a lane being one of the separate evidence tracks the project runs, kept apart so a result in one does not lean on the other. |
| `H-925` | `033` control | CISI Pakistan leaf `373` shows nine H-925 panels including numbered, `bis`, and `ter` variants. | Shared control is high-risk until copy/variant status and the intended panel are resolved. |
| `H-983` | `034` target | CISI Pakistan leaf `377` shows `A`, `A bis`, `B`, `B bis`, `B ter`, `C`, and `C bis`. | Local two-side coding suppresses visible source `C` and multiple variants; must be reconciled. |
| `H-353` | `033` control | CISI India leaves `265`/`696` show `H-353 A`, `B`, and `C`. | Source panel count exceeds local side count; the extra `C` side blocks clean use until reconciled. |

Register-only route:

| Object | Packet role | Source observation | Consequence |
| --- | --- | --- | --- |
| `H-212` | `032` control | CISI India leaves `406`/`837` are `DATA H-157 to H-321` register pages, not plate pages. | Useful as a routing/cross-reference locator only; fills no visual sign fields. |

## Consequence For The `034` Packet

The source situation got sharper and harsher.

The immediate local-contrast triad `H-893/H-925/H-930` is not clean yet:

```text
H-893 has a numbered variant.
H-925 has many variant panels.
H-930 is the only clean two-panel object in that triad.
```

The independent IA pair `H-771/H-789` is also asymmetric:

```text
H-789 is a clean two-panel source locator.
H-771 has multiple A photographs plus B, so the target needs panel/photo disambiguation.
```

This weakens the lazy version of the `034` story. The source images are not just confirming the local packet; they are exposing exactly the side/copy complexity that could kill it.

Follow-up:

[Lipi FRAME700 034 clean two-panel close-read](lipi_frame700_034_clean_two_panel_close_read.md) close-read `H-930` and `H-789`. Both survive as calibration controls for panel count and short-vs-long side split, but neither accepts subtype, direction, side function, or translation.

[Lipi FRAME700 034 CISI variant convention probe](lipi_frame700_034_cisi_variant_convention_probe.md) later corrected the blunt side-count language: `bis`, `ter`, and `quater` are same-side photographs under CISI convention, while `A/B/C` remain side categories.

## Boundary

No reading is accepted.

This pass does not decide:

- `034` versus `033` versus `032`,
- direction,
- physical side order,
- copy-family independence,
- sign meaning,
- numerical value,
- phonetic value,
- language identity,
- translation.

It decides only that some objects are now visually locatable and that several have immediate side-count, photo-label, or copy-variant hazards.
