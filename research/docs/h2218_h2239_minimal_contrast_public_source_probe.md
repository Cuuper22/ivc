# H-2218 Through H-2239 Minimal Contrast Public Source Probe

Date: 2026-05-25

## Question

Can the public/source web layer validate the `H-2237/H-2238` minimal-contrast targets, or does it only sharpen the next archive/CISI/HARP request?

## Inputs

- Minimal contrast packet: `docs/h2218_h2239_minimal_contrast_packet.md`
- Prior public image-lead search: `docs/h2218_h2239_public_image_lead_search.md`
- CSV: `data/open_prototype/reports/h2218_h2239_minimal_contrast_public_source_probe.csv`
- Summary: `data/open_prototype/reports/h2218_h2239_minimal_contrast_public_source_probe_summary.json`

## Result

```text
probe rows: 10
source anchor hit rows: 4
method-control rows: 1
source-grade public image hits: 0
object-level public image hits for H-2230/H-2233/H-2237/H-2238: 0
accepted readings: 0
```

## What Was Found

The exact HARP IDs route back to the Meadow/Kenoyer 2000 Harappa PDF:

| Fig. 4 no. | Object | HARP/source ID | Public source result |
| ---: | --- | --- | --- |
| 17 | `H-2237` | `H96-3125/6937-16` | Source anchor hit in Fig. 4 legend. |
| 18 | `H-2238` | `H95-2613/6560-01` | Source anchor hit in Fig. 4 legend. |
| 19 | `H-2230` | `H97-3311/8040-10` | Source anchor hit in Fig. 4 legend. |
| 20 | `H-2233` | `H97-3341/8039-10` | Source anchor hit in Fig. 4 legend. |

The same source also matters methodologically. Its surrounding discussion treats the 22 tablets as manufacturing groups, reports microscopic mold observations relevant to engraving process, and explicitly raises workshop/group context. That is not a reading; it is a stronger confound model for the minimal-contrast packet.

## What Was Not Found

The public web search did not produce object-level, segmentation-grade image leads for `H-2230`, `H-2233`, `H-2237`, or `H-2238`.

The prior series-level RSS/blog search still stands:

```text
H-2219: public A/B/C thumbnail leads exist.
H-2230/H-2233/H-2237/H-2238: no object-level A/B/C image lead in checked RSS/blog pages.
```

A direct shell fetch of the Harappa PDF returned a small Cloudflare HTML page, not the PDF. The PDF was accessible through the web-open route for source-text anchoring, but no local PDF or image artifact was kept.

## Research Consequence

The minimal-contrast packet survives as a source target, not as source validation.

What improved:

1. The four target/control objects are publicly anchored to exact Fig. 4 numbers and HARP IDs.
2. The workshop/manufacturing confound is now source-backed, not merely invented as a caution.
3. The source request can ask for exact objects and controls instead of the whole series only.

What remains blocked:

1. Diagnostic `154/156` and `033/034` stroke visibility.
2. Physical side-role equivalence.
3. Direction and image/impression convention.
4. Damage and photo-quality status.
5. Copy/workshop independence.

## Claim Status

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted numerical values: 0
accepted side functions: 0
accepted source mappings from this probe: 0
```
