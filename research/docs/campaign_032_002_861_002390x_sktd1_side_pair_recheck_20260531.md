# 002-390-X Sktd-1 side-pair recheck

Date: 2026-05-31 America/Los_Angeles

Status: active source gate, not goal completion.

## Question

Can Sktd-1 be upgraded inside the `004 -> 002-390` matched-predecessor split?

Local row:

- Object: `Sktd-1`
- Row id: `3875.1`
- Site: Surkotada
- Excavation id: `SKTD 1750`
- Type: `SEAL:S`
- Local text: `+390-004-002-390-125-820+`
- Relevant local frame: `004 -> 002-390 -> 125 -> 820`

No value, phonetics, language identity, function, sign meaning, or translation is accepted.

## Inputs

- Full source page: `tmp/002390x_source_normalization/cisi_india_n397_w2000.jpg`
- Face crop: `tmp/002390x_source_normalization/Sktd1_face_A_full_panel.jpg`
- Impression crop: `tmp/002390x_source_normalization/Sktd1_impression_a_full_panel.jpg`
- Face top-band crop: `tmp/002390x_source_normalization/Sktd1_face_A_signband.jpg`
- Impression top-band crop: `tmp/002390x_source_normalization/Sktd1_impression_a_signband.jpg`
- Report: `data/open_prototype/reports/campaign_032_002_861_002390x_sktd1_side_pair_recheck_20260531.csv`

## Observations

The source page is stronger than a generic public route. CISI India leaf `n397` / printed page `362` visibly labels the lower Surkotada row as `Sktd-1 A` and `Sktd-1 a`, under the page heading `Surkotada 1-2 seals`.

The object is therefore public panel-bound at the source-page side-pair level.

The remaining problem is token order, not object reachability. Both views show a wrapped layout:

- `Sktd-1 A` has a top inscription band plus a separate lower-field sign near the left side of the animal/body field.
- `Sktd-1 a` has the mirrored source view, with a top inscription band plus a separate lower-field sign near the right side.
- The top-band crops are visually compatible with the central `002-390-125` window under local `R/L` policy, but the full local six-token row is not a single clean top-line band.

That lower-field sign is exactly why this does not become strict token proof. The source panel supports object/side visibility and broad layout compatibility; it does not independently derive the local numeric order `390-004-002-390-125-820`.

## Decision

Status: `sktd1_side_pair_visible_wrapped_layout_not_strict`.

What changes:

- Sktd-1 is no longer merely a vague public route candidate.
- It is source-panel side-pair visible: `Sktd-1 A` and `Sktd-1 a` are labeled on the public page.
- The wrapped layout supports a real continuation layout after the top band, which keeps Sktd-1 useful as pressure in the `004 -> 002-390 -> 125 -> 820` lane.

What does not change:

- Sktd-1 remains below strict `M-119/M-735` source-visible `125` witnesses.
- The exact `002-390-125-820` path remains catalog-mediated.
- The `004` matched-predecessor split remains blocked because H-1993 is still route-only/no image.
- Sktd-1 cannot be counted as strict source-controlled branch evidence.

Accepted value, phonetics, language identity, function, sign meaning, and translation remain 0.

## Consequence For The Predecessor Gate

The predecessor-gate verdict does not change. The `004` group is still not a strict matched split:

- H-1993: `004 -> 002-390 -> 095 -> <END>`, route pressure only.
- Sktd-1: `004 -> 002-390 -> 125 -> 820`, public panel-bound side-pair visible, wrapped layout, not strict.

The positive model keeps one useful pressure point. It does not get a grammar promotion.
