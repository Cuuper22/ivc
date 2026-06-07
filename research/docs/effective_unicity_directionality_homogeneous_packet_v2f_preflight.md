# Directionality Homogeneous Packet v2f Preflight

Date: 2026-05-29

Status: failed preflight. Accepted claim increment: 0.

## Question

Can the widened v2e signband-like pool be promoted into a homogeneous no-overlay blind packet for `H-654`, `M-1310`, `M-1320`, and `M-811`, with 12 fixed real-negative controls?

Answer: no.

## Mechanical Gate

Artifact: `data/open_prototype/reports/effective_unicity_directionality_homogeneous_packet_v2f_preflight_summary.json`.

Strict v2e reuse lane:

- Candidate rows: 82.
- Compact targets available: `H-654`, `M-1310`, `M-1320`.
- Compact target missing: `M-811`.
- Original fixed real-negative CISIs available: 7.
- Fixed real negatives available: `H-158`, `M-1315`, `M-171`, `M-365`, `M-386`, `M-525`, `M-527`.
- Target/control source-page collisions: `M-1310` with `M-1315` and `M-1314` on `n202`; `M-1320` with `M-1322` on `n203`.
- Exact duplicate hash groups across selected CISIs: none.

Derived top-strip lane:

- Candidate rows: 44.
- Targets available before visual review: `H-654`, `M-1310`.
- Targets missing before visual review: `M-1320`, `M-811`.
- Original fixed real-negative CISIs available: 6.
- Status: acquisition-only. These crops are not a blind packet and have no false-positive denominator.

## Human Visual Check

The target gate contact sheet confirms the mechanical result. `M-811` is absent from compact strict reuse because the available v2e candidates are bull/object-panel crops, not target-comparable signband strips. The strict contact sheet also shows why geometry alone is not enough: several non-target rows are page-context strips, object panels, or label-bearing views that would cue role or source context.

## Forger Requirement For Any Future Packet

A future v2f must be built as a fixed-denominator adversarial packet, not as a nicer contact sheet.

Minimum denominators:

- 12 unique real signband-negative CISIs, fixed before review.
- 12 unique source-real nonlinguistic null crops, matched for dimensions, contrast, and page quality.
- 32 fixed-seed synthetic nulls: 8 matched texture/noise, 8 asemic stroke bands, 8 mirror/reversal controls, and 8 shuffled-token/collage controls.
- Sentinels may be included only as auxiliary rows, never as denominator rescue.

False-positive rule:

- Compute yes-only and conservative false-positive rates per reviewer and max across reviewers.
- One hard or uncertain target-like/directional call on any denominator row fails the apparatus.
- Do not recalculate denominators downward after leaks. A leaked denominator row fails the packet.

Automatic pre-review failures include visible role/cisi/source metadata, target/control crop-world mismatch, duplicate blind image hashes, unregistered near-duplicate clusters, denominator below floor, reserve promotion after packet creation, visible label/page cues, target-only source-family style, post-review null generation, and fewer than three independent reviewers.

## Decision

`retracted_directionality_homogeneous_signband_v2f_packet_readiness_2026_05_29`.

The v2e pool remains useful acquisition infrastructure. It does not support a homogeneous no-overlay source-normalization packet, and no directionality/source-order claim follows from v2f.
