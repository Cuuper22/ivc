# Directionality: stored order versus physical orientation

Date: 2026-07-12 America/Los_Angeles

## What this is and why it exists

There is a real structural result in this workspace: across 365 scored rows, inscriptions read in the order the Lipi catalogue stores them score better than the same inscriptions read backwards. That is a fact about the stored sequences.

The tempting next step is to say it is a fact about the objects: that the ancient writing was physically read in that direction. This note asks whether that step can be taken, and answers no. The reason matters more than the answer. Lipi's `dir.` field, which records values like `R/L` for right-to-left, does not mean the same physical thing on every kind of object, and one seal proves it.

## Question

Can the 365-row effective-unicity directionality result be promoted from coherent Lipi stored order to physical reading direction by building a larger homogeneous image denominator?

## Direct result

No. Close the physical-direction promotion and retain the stored-order result.

What settles it is a single case where the same object is described by both the catalogue and the published literature, not a bigger pile of image crops:

| Evidence | Direct observation |
| --- | --- |
| Meadow and Kenoyer 2000, Fig. 4.1 | The steatite seal is `H96-2796/6876-01`, locally `H-1682`. |
| Meadow and Kenoyer 2000, printed p. 16 / PDF p. 17 | The authors identify the seal's final two signs with one side of the 22 non-impressing tablets and explicitly describe the sequence as left-to-right on the seal versus tablets assumed to be read right-to-left. |
| Lipi row `810.1` | `H-1682`, `H96-2796Figure 20.02`, type `SEAL:S`, is recorded `R/L` with text `+154-003-617-033+`. |
| Lipi H-2218 through H-2239 | All 66 sides of the 22 matched tablets are also recorded `R/L`; `H-2237` side `794.3` is the exact local `+154-003+` match. |
| Harsh directionality scope | `H-1682` is one of the 365 scored rows and favors stored over reversed order by 10.091788 log-probability units, or 2.018358 per transition. |

Read the table together and the problem is plain. One `R/L` label covers two physically opposite situations: a seal the authors describe as left-to-right, and the tablets matched to it, which are assumed to be read right-to-left. So `dir.` is not a uniform label for as-pictured physical orientation across different media. That is a counterexample from inside the corpus itself, not an outside objection.

The bridge between the seal and the tablets does not require accepting Lipi's segmentation. The source description implies five units on the seal while Lipi records four. That mismatch is a second reason to hold the conclusion at the level of orientation policy instead of reading a sign crosswalk out of this case.

The 365-row result does not depend on this one row. Drop `H-1682` and the stored-win share moves from 0.841096 to 0.840659, a difference of 0.000437. So the aggregate stored-order asymmetry survives. Its physical-direction interpretation does not.

## Why the denominator is the wrong instrument

The proposal was to build a bigger, more uniform pool of image crops as a comparison baseline, a denominator. That instrument measures the wrong thing.

A denominator like that tells you how recognizable a crop is and how often the method fires on nothing. It cannot tell you whether the image in front of it is a seal, an impression taken from that seal, a cleaned-up transcription, or a copy someone reversed on purpose. Those four states are what the question turns on, and an image cannot report them unless something outside the image already labels it.

The published literature warns about this directly. Meadow and Kenoyer note that seals are often printed as impressions without anyone stating that the flip happened. The Mayig corpus follows a different convention and says so: graphemes are stored left-to-right as they sit on the artefact side, but seals are transcribed from the sealing rather than from the seal itself. Each convention yields a perfectly coherent stored sequence, and the two disagree about physical orientation.

So more anonymous signband crops would sharpen the baseline around a target nobody has identified. Precision is not the missing ingredient. The link between the measurement and the thing it is supposed to be about is missing, and crops cannot supply it.

## Decision

Status: `CLOSED_PHYSICAL_DIRECTION_PROMOTION_RETAIN_STORED_ORDER_STRUCTURE`.

Accepted:

- The harsh Lipi scope has reproducible stored-order asymmetry: stored-win share 0.841096.
- The result is structural evidence about the normalized metadata/transcription layer.
- H-1682 provides a source-bound example showing that `dir.` is not a uniform physical-orientation label across seal and tablet media.

Not accepted:

- Correct physical reading direction for the corpus or for all objects marked `R/L`.
- A pan-Indus directionality claim.
- Writing status, language family, sign values, meanings, or translation.

To reopen this, the records themselves have to carry the missing labels. Each object would need four things stated together: which physical face is described, whether the published image shows the object or its impression, what transformation the transcription applied, and what reading direction is being proposed. Adding unlabeled crops or synthetic nulls will not reopen it, because neither one supplies those labels.

## Sources used

- `evidence/tmp/h2148_h2100_h2152_110_route/kenoyer2000_tiny_steatite_seals_harappa.pdf`, Fig. 4 and printed pp. 15-19.
- `research/data/open_prototype/lipi/metadata_filtered.csv`, rows `693.1-693.3`, `794.1-794.3`, `810.1`, and the H-2218 through H-2239 series.
- `research/data/open_prototype/reports/effective_unicity_directionality_influence_rows.csv`, `H-1682` in `all_harsh`.
- `evidence/tmp/mayig_feature_namespace_probe/repo/indus-valley-script-corpus-ad2f1e218a34b8c33c57de0d6cb8d99272765bbb/README.md`.
