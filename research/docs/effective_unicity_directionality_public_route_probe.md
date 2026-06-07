# Effective-Unicity Directionality Public Route Probe

Date: 2026-05-29

## Purpose

This pass probes the public CISI India/Pakistan OCR layers for the top high-pressure directionality rows after the M-70 blind packet failed promotion. It is a source-acquisition/admissibility artifact, not a direction, token, sign, meaning, language, or translation claim.

Scope:

- input queue: `data/open_prototype/reports/effective_unicity_directionality_source_queue.csv`
- target rows: top 80 queue rows requiring public/source route work
- actual rows after filter: 79
- route method: exact OCR label search, rejecting starred partial labels and split numeric suffix traps
- demotion rule: late register/data-page hits are retained but not counted as source-panel routes

## Route Probe Result

| Measure | Count |
| --- | ---: |
| Target rows | 79 |
| OCR route rows | 93 |
| Targets with any route | 39 |
| Targets with public CISI plate-route candidate | 38 |
| Targets with data/register route only | 1 |
| Targets not found in public CISI OCR layer | 40 |
| Accepted claim increment | 0 |

The public route probe materially improves the directionality source queue, but the failed first packet changes the bottleneck to clean label-free crops, adequate real-negative denominators, stable target counts, and source-side/direction checks. It does not validate a physical reading direction.

Top route candidates by queue pressure included `H-665`, `M-1458`, `H-654`, `M-1310`, `M-1320`, `M-811`, `M-1523`, `H-152`, `M-365`, `M-527`, `M-534`, `M-525`, `M-1315`, `M-386`, and `H-158`.

## Visual Triage

Nine top route hits were manually inspected at image level. The review produced four attempted target crops for the first no-overlay blind token-box packet:

| Queue rank | CISI | Text | Visual status | Next gate |
| ---: | --- | --- | --- | --- |
| 9 | `H-654` | `+405-061-740-806+` | source panel visible | no-overlay crop, blind token-boxing |
| 10 | `M-1310` | `+407-004-001-740-407-590-235+` | source panel visible, route overlay must be removed | no-overlay crop, blind token-boxing |
| 11 | `M-1320` | `+527-555-231-240-798+` | source panel visible | no-overlay crop, blind token-boxing |
| 15 | `M-811` | `+226-032-803+` | source panel visible | no-overlay crop, blind token-boxing |

Lower-tier but useful route hits:

- `H-665`: source panel visible but weak/partial; needs a cleaner crop before review.
- `H-152`: source panel visible, but the route has a volume/provenance mismatch gate.
- `M-525`: source panels visible, but side geometry and legibility are not clean enough for the first packet.
- `M-1458` and `M-1523`: routed, but too low-legibility in the public crop to prioritize.

Visual triage counts:

| Measure | Count |
| --- | ---: |
| Public plate-route candidates | 38 |
| Manually visual-reviewed route hits | 9 |
| Attempted blind-packet target crops | 4 |
| Accepted claim increment | 0 |

## Adversarial Boundary

Forger boundary:

> The first follow-up no-overlay blind packet failed promotion: seven packaged unique real scoring negatives were below the forger denominator floor of ten, `D006/M-525` leaked a printed side annotation, scoring negatives produced hard count-boxable false positives, and the target views were mostly overcounted or uncertain. A stricter v2b packet reached 12 real negatives and zero duplicate blind image hashes, but it also failed because real denominator rows leaked labels, reviewer C had target-like uncertainty on two real negatives, and target counts were unstable. Accepted claims remain zero.

Skeptic boundary:

> Visual route triage cannot validate source-normalized token order, physical direction, sign identity, meaning, phonetic value, language family, or translation.

Known failure pressure:

- The previous M-70 source pilot looked plausible but failed a matched-negative blind packet with max yes-only FPR 0.714286 and max conservative FPR 0.777778.
- The branch-gap blind packet also failed token-count promotion and exposed stable over-counting in a scoring negative.
- Therefore, route visibility is not enough; the first such packet included a no-overlay/matched-negative gate and failed. Any future packet must include label-free source panels, a fixed adequate real-negative denominator, duplicate-hash checks, and matched negatives before any source-normalized directionality statement is admissible.

## Artifacts

- `data/open_prototype/tools/effective_unicity_directionality_public_route_probe.py`
- `data/open_prototype/tools/effective_unicity_directionality_route_visual_triage.py`
- `data/open_prototype/reports/effective_unicity_directionality_public_route_probe_routes.csv`
- `data/open_prototype/reports/effective_unicity_directionality_public_route_probe_status.csv`
- `data/open_prototype/reports/effective_unicity_directionality_public_route_probe_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_route_visual_triage.csv`
- `data/open_prototype/reports/effective_unicity_directionality_route_visual_triage_summary.json`
- `docs/effective_unicity_directionality_blind_packet.md`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_review_summary.json`
- `docs/effective_unicity_directionality_blind_packet_v2b.md`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_review_summary.json`
- `tmp/effective_unicity_directionality_public_route_probe/directionality_public_route_probe_contact_sheet.jpg`
- `tmp/effective_unicity_directionality_public_route_probe/directionality_route_visual_triage_reviewed_contact_sheet.jpg`

## Decision

The public route probe created a usable source-normalization worklist for the directionality candidate. Its first no-overlay, matched-negative blind packet using `H-654`, `M-1310`, `M-1320`, and `M-811` as attempted target crops failed the promotion gate. It does not promote the Vector 2 directionality result or add an accepted structural finding.

Follow-up artifact: `docs/effective_unicity_directionality_blind_packet.md`.
