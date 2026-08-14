# Directionality: stored order versus physical orientation

Date: 2026-07-12 America/Los_Angeles

## Question

Can the 365-row effective-unicity directionality result be promoted from coherent Lipi stored order to physical reading direction by building a larger homogeneous image denominator?

## Direct result

No. Close the physical-direction promotion and retain the stored-order result.

The decisive evidence is a matched-medium source case, not another crop-recognition denominator:

| Evidence | Direct observation |
| --- | --- |
| Meadow and Kenoyer 2000, Fig. 4.1 | The steatite seal is `H96-2796/6876-01`, locally `H-1682`. |
| Meadow and Kenoyer 2000, printed p. 16 / PDF p. 17 | The authors identify the seal's final two signs with one side of the 22 non-impressing tablets and explicitly describe the sequence as left-to-right on the seal versus tablets assumed to be read right-to-left. |
| Lipi row `810.1` | `H-1682`, `H96-2796Figure 20.02`, type `SEAL:S`, is recorded `R/L` with text `+154-003-617-033+`. |
| Lipi H-2218 through H-2239 | All 66 sides of the 22 matched tablets are also recorded `R/L`; `H-2237` side `794.3` is the exact local `+154-003+` match. |
| Harsh directionality scope | `H-1682` is one of the 365 scored rows and favors stored over reversed order by 10.091788 log-probability units, or 2.018358 per transition. |

This is an internal counterexample to treating Lipi `dir.` as a uniform label for physical as-pictured orientation across media. The same `R/L` value covers a source-described left-to-right intaglio seal and right-to-left non-impressing tablets.

The object bridge does not depend on accepting Lipi's segmentation: the source description implies five units on the seal, while Lipi records four. That mismatch is another reason to keep the conclusion at orientation-policy level rather than infer a sign crosswalk from this case.

The result is not driven by this row. Removing `H-1682` changes the 365-row stored-win share only from 0.841096 to 0.840659, a difference of 0.000437. The aggregate stored-order asymmetry therefore survives, but its physical-direction interpretation does not.

## Why the denominator is the wrong instrument

A homogeneous negative-image denominator can measure crop recognizability and false positive rates. It cannot identify whether an image is a seal, an impression, a normalized transcription, or a deliberately reversed copy unless those orientation states already have external labels.

The source literature warns about exactly this ambiguity. Meadow and Kenoyer note that seals are often published as impressions without the transformation being stated. The Mayig corpus makes a different convention explicit: graphemes are stored left-to-right on the artefact side, but seals are transcribed from the sealing rather than the seal. These conventions can each produce coherent stored sequences while disagreeing about physical orientation.

More anonymous signband crops would therefore add denominator precision around an unidentified target. They cannot repair the missing construct validity.

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

Reopen only with object-level records that jointly label the physical face, whether the published image is the object or its impression, the transcription transformation, and the proposed reading direction. Do not reopen by adding unlabeled crops or synthetic nulls.

## Sources used

- `evidence/tmp/h2148_h2100_h2152_110_route/kenoyer2000_tiny_steatite_seals_harappa.pdf`, Fig. 4 and printed pp. 15-19.
- `research/data/open_prototype/lipi/metadata_filtered.csv`, rows `693.1-693.3`, `794.1-794.3`, `810.1`, and the H-2218 through H-2239 series.
- `research/data/open_prototype/reports/effective_unicity_directionality_influence_rows.csv`, `H-1682` in `all_harsh`.
- `evidence/tmp/mayig_feature_namespace_probe/repo/indus-valley-script-corpus-ad2f1e218a34b8c33c57de0d6cb8d99272765bbb/README.md`.
