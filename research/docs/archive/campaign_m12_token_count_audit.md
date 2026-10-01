# M-12 / BG001 Token-Count Audit

Date: 2026-05-29

## Purpose

This note records an audit of one seal, `M-12`, known as `BG001` inside our blind review packets. It exists because `M-12` was the strongest residue — the strongest unexplained leftover — from the first branch-gap blind source-box packet. A source-box packet is a bundle of image crops scored by reviewers who cannot see the catalog answers; "blind" means exactly that. All three blind reviewers counted 10 visible units on the image, while the catalog string lists 9 tokens.

The audit asks one question. Is this a candidate for correcting the source catalog, or is it only a visual ambiguity stressor — a hard image that stresses the counting process without proving the catalog wrong?

## Source-Side Artifacts

Before looking at the seal itself, we had to fix a file-handling bug. The first ad hoc crop pass had a Windows-specific trap: filenames using `M12_A` and `M12_a` collided on the case-insensitive filesystem, so the second crop overwrote the first. The audit script fixes this with case-safe names and regenerates the M-12 face/impression crops from the original CISI India leaf `n45`.

Outputs:

- Builder: `data/open_prototype/tools/campaign_m12_token_count_audit.py`
- Summary: `data/open_prototype/reports/campaign_m12_token_count_audit_summary.json`
- Observations: `data/open_prototype/reports/campaign_m12_token_count_audit_observations.csv`
- Contact sheet: `tmp/m12_token_count_audit/m12_token_count_audit_contact_sheet.png`
- Crops: `tmp/m12_token_count_audit/`

## What The Audit Found

First, the catalog layer agrees with itself. Two independent witnesses — separate catalog records of the same inscription — both list 9 tokens:

| Witness | System | Sequence count |
| --- | --- | ---: |
| `lipi:2540.1` | Lipi numeric | 9 |
| `mayig:M-12A` | Mayig P namespace | 9 |

The blind packet did find a stable mismatch:

| Blind ID | CISI | Role | Catalog count | Blind counts |
| --- | --- | --- | ---: | --- |
| `BG001` | `M-12` | primary target | 9 | 10, 10, 10 |

But the same packet also contains an adversarial false-positive control — a seal planted specifically to measure how often reviewers over-count when nothing is actually wrong:

| Blind ID | CISI | Role | Catalog count | Blind counts |
| --- | --- | --- | ---: | --- |
| `BG009` | `M-654` | scoring negative | 4 | 6, 6, 6 |

All three `BG001` reviewers marked the count uncertain, and all three `BG009` reviewers did too. That control matters: on `BG009` the reviewers stably over-counted a seal whose catalog count is not in dispute. Under the packet's own scoring negatives, the stable over-count pattern has observed false-positive rate `1/6 = 0.166667`. In plain terms, reviewers agreeing on a higher count is not rare enough to prove the catalog wrong.

## Decision

`BG001/M-12` stays in the queue as a source/catalog tokenization audit target. It does not become a catalog-correction claim.

Allowed wording: three blind reviewers independently saw 10 visual units on the public `M-12 a` crop against a 9-token Lipi/Mayig catalog witness, but a same-packet scoring negative reproduces stable over-counting, so this is an ambiguity lead only.

Forbidden wording: "M-12 has 10 signs," "the catalog is wrong," "sign X is split," or any structural/semantic/phonetic inference from this crop.

Accepted claim increment: `0`.
