# Lipi 034 M-2104 M-479 Source Probe

Date: 2026-05-25

Question:

```text
Does M-479 materially improve the M-2104 700-034 versus 700-004 count-compound hypothesis, or only expose duplicate-family risk?
```

## Result

M-479 is no longer just a local-corpus surprise. It is source-visible on CISI India IA leaf `n150`, printed p. 115, under the plate header `MOHENJO-DARO 478-481`, `TABLETS in bas-relief`.

Stored crops:

- `tmp/cisi_m2104_packet/m479/m479_a_inscription_crop.png`
- `tmp/cisi_m2104_packet/m479/m479_b_scene_crop.png`
- `tmp/cisi_m2104_packet/m479/cisi_india_n19_m478_m479_pot_context_crop.png`
- `tmp/cisi_m2104_packet/overlays/m479_a_segmentation_overlay.png`
- `tmp/cisi_m2104_packet/closeups/m479_a_u_count_closeup_enhanced.png`

Stored reports:

- `data/open_prototype/reports/lipi_034_m2104_m479_source_notes.csv`
- `data/open_prototype/reports/lipi_034_m2104_m479_segmentation_targets.csv`
- `data/open_prototype/reports/lipi_034_m2104_m479_adjudication.csv`
- `data/open_prototype/reports/lipi_034_m2104_m479_summary.json`

## Local Row

```text
M-479: +400-097-700-004+
```

Metadata: Mohenjo-daro, `TAB:B`, clay, rectangular, complete, good condition, `R/L`, class `VX`, 4 signs, excavation/source hook `DK1007890.24`.

The exact comparator family now stands:

```text
M-478:  +400-097-700-004+
M-479:  +400-097-700-004+
M-480:  +400-097-700-004+
M-1425: +400-097-700-004+
```

M-479 is not a named Parpola 2019 parallel in the current extraction, but CISI itself discusses M-478/M-479 together as a four-plus-U case in the introduction. That gives prior-work pressure for the visual class while also warning that this is a tight tablet-family phenomenon.

## Visual Note

M-479 A shows the inscription side. The crop preserves the same broad family layout seen in M-478/M-480: a non-count sign region, a four-stroke group, a U/pot-like region, and a neighboring comb/ribbed sign region. The stored overlay marks these as visual boxes only; the boxes are not accepted local token boundaries.

M-479 B shows the companion scene side. It supports the source route for the pot/count interpretation, but it is not sign evidence.

## Prior-Work Pressure

CISI India introduction leaf `n19` describes a U-shaped tablet sign preceded by strokes and specifically discusses M-478/M-479 as a four-plus-U case beside a ritual scene. This is real prior-work support for testing the `700-004` cluster as a four-stroke U/pot compound.

It does not validate:

- `004 = four`
- `034 = three`
- `700 = pot`
- a phonetic value
- a language identity
- a translation

## Adversarial Adjudication

Accepted:

- M-479 is a source-visible local extra member of the exact `+400-097-700-004+` family.
- M-479 A is usable as a segmentation target for the four-stroke/U-pot visual test.
- M-479 B and CISI introduction leaf `n19` support the pot-count context route.

Quarantined:

- M-479 cannot currently be counted as an independent recurrence.
- The `004` side remains a repeated exact sequence family, not four independent substitutions.
- Same site, object class, material, plate cluster, and local text make duplicate-family inflation the main danger.

Current status:

```text
M-479 = source_visible_comparator_candidate_duplicate_family_risk
```

## Consequence

This is actual forward movement, but not a win condition. M-479 tightens the visual test set:

```text
M-2104: 700-034 target, source-gated
M-478:  700-004 strongest public tablet comparator
M-479:  700-004 source-visible family-internal comparator
M-480:  700-004 weaker same-plate comparator
M-1425: 700-004 independent Pakistan-volume comparator, lower visual confidence
```

The next hard test is not another broad corpus audit. It is blind segmentation on M-478/M-479/M-1425 and raw-source closure for M-2104.
