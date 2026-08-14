# Lipi 034 M-1206 K-150/H-942 Singleton Controls Source Gate

Date: 2026-05-26

This note is a gate — a checkpoint the evidence must pass before it can be used. Two objects are up for admission. Each is a singleton: the only object in the corpus carrying its particular three-sign string. Singletons are useful here as contrast shapes, because they show what else can sit in the same slot. One of the two has a usable published photograph and is admitted; the other does not and stays out.

## Question

After `M-1912 +520-220-003+` failed source-grade admission, can the other exact `+520-220-X+` singleton terminals help constrain the `M-1206 +520-220-034+` branch — the open line of investigation into that object's final sign?

The two relevant singleton controls are:

```text
K-150 +520-220-006+
H-942 +520-220-016+
```

## Decision

`H-942` upgrades to a source-visible control target. `K-150` does not.

Current status:

```text
H-942 = source_visible_singleton_016_control_target_side_mapping_caution
K-150 = secondary_catalogue_lead_only_not_source_grade
accepted mapping/value/translation = 0
```

This improves the branch because `H-942` is not another `415` lookalike. It gives a source-visible exact-frame singleton terminal that can be used as a negative/control shape in future blind component sorting. It does not prove anything about `034`, `415`, `016`, or their values.

## H-942 Source Gate

Local rows:

| Local row | Object | Text | Side/context |
| --- | --- | --- | --- |
| `1822.1` | `H-942` | `+520-220-016+` | Harappa `TAB:I`, steatite, rectangular, two sides, `L/R`, class `MT`, three signs |
| `1822.2` | `H-942` | `+033-700+` | Companion side, `R/L`, class `NV`, two signs |

Source layer:

| Source | Locator | Result |
| --- | --- | --- |
| CISI Pakistan IA leaf `n374`, printed p. 340 | heading `HARAPPA 927-942 TABLETS incised`, `no iconography` | Source-visible `H-942 A` and `H-942 B` panels are present. |
| CISI Pakistan OCR text | local OCR lines `17115` and `17119` | OCR confirms labels `H-942 A` and `H 942 B`. |
| CISI Pakistan data page | `DATA H-838 to H-988`, p. 444 | Data row route exists but the currently stored crop is too blurry for secure side-transcription detail. |

Admissibility:

- `H-942 A` is the likely local `+520-220-016+` side because it visibly has the longer three-part signband.
- `H-942 B` is the likely companion `+033-700+` side because it visibly has the shorter side.
- The global rule `local .1 = source A` is still rejected. Here the side mapping is a local visual/sign-count inference, not a universal policy.
- Therefore `H-942` can enter the next packet as a source-visible singleton `016` control target, with side-mapping caution.

Stored crops:

```text
tmp/m1206_singleton_controls/derived/h942/H942_A_panel_labeled_from_cisi_pakistan_n374.png
tmp/m1206_singleton_controls/derived/h942/H942_A_signband_from_cisi_pakistan_n374.png
tmp/m1206_singleton_controls/derived/h942/H942_B_panel_labeled_from_cisi_pakistan_n374.png
tmp/m1206_singleton_controls/derived/h942/H942_B_signband_from_cisi_pakistan_n374.png
```

## K-150 Source Gate

Local row:

| Local row | Object | Text | Context |
| --- | --- | --- | --- |
| `5277.1` | `K-150` | `+520-220-006+` | Kalibangan `SEAL:S`, steatite, square, `Gaur`, one side, `R/L`, class `MT`, three signs |

Source layer:

| Evidence | Result |
| --- | --- |
| CISI India Vol. 1 OCR/page scan | The accessible Kalibangan section covers `K-1` to `K-122`, so `K-150` is outside the checked public CISI 1 range. |
| Bhaskar S1 zoomorphic catalogue | Lists `K-150` with text-present marker, `P8`, `F0`, and `Bison`. This is a catalogue lead, not a source plate. |
| Fresh exact public search, 2026-05-26 | No object-level source plate, museum/archive row, or raw CISI/HARP-style image surfaced in the checked public layer. |
| CISI 3.x route | K-series material beyond CISI India Vol. 1 likely belongs in a later supplement/acquisition lane, but no exact `K-150` source page has been inspected. |

Admissibility:

`K-150` remains a local exact-frame singleton and an acquisition target. It cannot enter a blind source-normalized component packet.

## Effect On The M-1206 Branch

Before this gate, the exact three-sign frame was:

```text
034: M-1206 source-visible target
415: source-visible controls, especially H-938/H-940 and clean M-37 recut
003: M-1912 secondary/CISI-gated
006: K-150 local only
016: H-942 local only
```

After this gate:

```text
034: M-1206 source-visible target
415: H-938/H-940/M-37 source-visible controls
016: H-942 source-visible singleton control target, side-mapping caution
003: M-1912 still secondary/CISI-gated
006: K-150 still secondary/acquisition-gated
```

This gives the next blind component sort a real non-`034`, non-`415`, non-Mohenjo-daro singleton control. It is a control for sign-inventory shape, not a semantic or phonetic clue.

## Next Experiment

Build the next source-normalized blind component packet with:

1. `M-1206` terminal target (`034`).
2. Clean `415` controls: `H-938 A/A bis`, `H-940 A`, and `M37_A_terminal_strict_core_from_signband.png`.
3. `H-942 A` as source-visible singleton `016` control target, marked side-mapping caution.
4. Prefix/nonterminal distractors — decoy crops from the non-final part of the same inscription, included to catch reviewers matching on context rather than form.

Do not include `M-1912` or `K-150` as clean witnesses — single source panels admitted as evidence — until raw source pages or equivalent archive records are acquired.

