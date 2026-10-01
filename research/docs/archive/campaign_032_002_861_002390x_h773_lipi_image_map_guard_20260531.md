# H-773 Lipi image-map guard

Date: 2026-05-31 America/Los_Angeles

Status: `h773_lipi_image_map_derivative_no_strict_upgrade`.

## Question

The cloned Yajnadevam/Lipi repository contains `public/seal_images/H-773_a.jpg` and `H-773_b.jpg`. H-773 is the best in-frame continuing non-`125` pressure row, so before we treat the public CISI crop as exhausted, these repo images needed a guard check: do they add anything?

## Findings

The repository image map has an explicit `H-773` entry:

- `H-773_a.jpg`
- `H-773_b.jpg`

Derivative image files:

| File | Size | SHA-256 | Role |
|---|---:|---|---|
| `tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images/H-773_a.jpg` | `269x170` | `A98945CB53542AAD8F0659A8FEB69F69C5F7A0578097B919E6100F4876968FDB` | Target side pressure, but low-resolution derivative. |
| `tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images/H-773_b.jpg` | `283x170` | `53B5A8760B225626A7BEEF4D0D1358C21C053FFFD8BF3D81B22CD9915EE48615` | Companion side guard, not target `002-390-X` side. |

The existing source-page-derived CISI crop for H-773 A is larger (`820x260`) and remains the stronger visual source:

- `tmp/source_route_recheck_20260531/cisi_pakistan_n358_h773_A_signband_tight_w2400.jpg`

## Decision

The answer is no. The Lipi image-map route confirms that H-773 has derivative A/B images in the repo, but it does not upgrade strictness. The images are lower resolution than the existing CISI crop and remain corpus-mediated; they do not independently prove `530`, `741`, or the `530 -> 741` continuation boundary.

Current status: `h773_lipi_image_map_derivative_no_strict_upgrade`.

Use H-773 as panel-bound and boxed-compatible pressure only. Do not count it as strict anti-`125` evidence, sign value, phonetics, function, language identity, meaning, or translation.
