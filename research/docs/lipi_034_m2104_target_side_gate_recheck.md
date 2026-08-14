# Lipi 034 M-2104 Target-Side Gate Recheck

Date: 2026-05-25

This note is a recheck. An earlier pass judged the target object, `M-2104`, under looser rules. Since then the project tightened how it counts evidence, so the same object gets rerun through the stricter test and the outcome is written down again from scratch.

A gate is a test a claim must pass before it can advance. The target side is the object carrying the sign we care about; the comparator side is the set of other objects we measure it against. This note is only about the target side.

Question:

```text
Can the current public raw-source layer validate M-2104 as the exact three-stroke target side for the 700-034 versus 700-004 count-compound hypothesis?
```

## Verdict

No. The target is now source-visible, but not source-validated.

Current public evidence supports:

```text
M-2104 / Marshall no. 532 / Plate CXIV target route is plausible and image-reachable.
The no. 532 region shows a U/V- or pot-like unit with an adjacent stroke group.
```

Current public evidence does not support:

```text
exact 034 = three strokes
accepted 700-034 = UIII
accepted M-2104 = Marshall no. 532 / VS 875 as an externally closed bridge
accepted local four-token segmentation +151-097-700-034+
accepted 700 role, sign value, function, phonetic value, language, or translation
```

The strict target-side gate fails because the best public crop remains:

```text
U/V-like unit + 3 secure adjacent strokes + possible fourth/boundary mark
```

That is not "exactly three." It is a live target, not a proof.

## Stored Outputs

- `data/open_prototype/reports/lipi_034_m2104_target_side_gate_sources.csv`
- `data/open_prototype/reports/lipi_034_m2104_target_side_gate_visual_adjudication.csv`
- `data/open_prototype/reports/lipi_034_m2104_target_side_gate_evidence_units.csv`
- `data/open_prototype/reports/lipi_034_m2104_target_side_gate_summary.json`

## Source Ladder

The rungs between our transcription and the physical object, weakest at the top. Each rung says what it gives and where it stops. A bridge is a chain of records tying identifiers to one another.

| Step | Status | Evidence | Limit |
| --- | --- | --- | --- |
| Local row `2527.1` | internal bridge | `M-2104`, `VS 875CXIV:532`, `+151-097-700-034+`, ivory rod, depth `-12.0 ft` | Local dataset bridge only. |
| Mahadevan/M77 text no. `2527` | standardized-text layer | IA page `0084` has text no. `2527`, code `100901`, and a printed sign row | Supports text lineage, not raw object identity or stroke count. |
| Parpola 2019 text no. `12` | prior-work hypothesis | Names `M-2104` and describes `UIII` plus signs 15 and 1 | Standardized extraction; Parpola points actual shapes back to CISI photos. |
| Local hook `VS 875CXIV:532` | alias route | Connects local row to Marshall Plate CXIV no. 532 | Still internal unless external source closes the `M-2104 = no. 532` bridge. |
| Harappa / Marshall no. `532` | public route | Harappa page and Marshall Plate CXIV reproduction make no. 532 reachable | Low resolution, not exact stroke-grade. |
| IA/IGNCA Marshall Vol. III Plate CXIV `48270_0205` | best public raw witness | 2601 x 3483 scan; no. 532 region visible | Count remains 3-to-4 ambiguous; five-character warning remains active. |
| CISI 3.1 | required acquisition target | Secondary range places `M-2104` inside `m1660-m2132`; hardbound purchase route exists | Not inspected yet, so identity/image/segmentation bridge is still open. |

Public source links already used by this packet — one self-contained bundle of evidence and rulings:

- Internet Archive/IGNCA Marshall Vol. III item: `https://archive.org/details/in.gov.ignca.48270`
- Plate CXIV page: `https://archive.org/details/in.gov.ignca.48270/page/n205/mode/1up`
- Plate CXIV IIIF image: `https://iiif.archive.org/image/iiif/3/in.gov.ignca.48270%2F48270_jp2.zip%2F48270_jp2%2F48270_0205.jp2/full/max/0/default.jpg`
- Harappa no. 532 route: `https://www.harappa.com/node/3576`
- Parpola 2019 PDF: `https://tuhat.helsinki.fi/ws/portalfiles/portal/129602857/Parpola_A_2019_Inscriptions_incised_on_the_Harappan_bone_rods_Proceedings_of_EASAA_22.pdf`
- CISI 3.1 Harappa route: `https://www.harappa.com/content/corpus-indus-seals-and-inscriptions-vol-31`

## Visual Gate

The target-side public source was rechecked against the stricter comparator policy from the family-dependence packet.

The comparator side is no longer counted as four rows. Copies of one formula on one plate are one fact, so they collapse into a single evidence unit:

```text
EU_004_INDIA_478_479_480 = one same-plate tablet-family evidence unit
EU_004_PAKISTAN_1425     = one provisional independent recurrence
```

The target side is one source-gated unit:

```text
EU_034_TARGET_2104 = one target unit with visible source route, unresolved identity bridge, and failed exact-count gate
```

This changes the evidentiary posture:

```text
004 side: visually stronger, but only two evidence units and one is provisional
034 side: source-visible, but exact three-stroke count fails
```

## Kill Gates Applied

Seven tests written to be hostile to the claim. A kill gate is one whose failure ends the claim rather than weakening it.

1. Explicit source bridge: fails in the public layer. The local row links `M-2104` to `VS 875CXIV:532`; checked public sources split the legs.
2. CISI 3.1 bridge: open. The expected volume route exists, but the source has not been inspected.
3. Standardized-layer circularity: fail for acceptance. M77 and Parpola can motivate the test but cannot prove raw stroke shape.
4. Marshall five-character warning: unresolved. It blocks accepting the local four-token segmentation as settled.
5. Exact three-stroke gate: fails. Current public crop permits three-plus-boundary or four-ish readings.
6. Token boundary gate: unresolved. The image does not force a clean `700` plus `034` boundary independent of transcription labels.
7. Comparator symmetry: partial. `004` has stronger visual support, but its India witnesses collapse to one family unit.

## Research Consequence

The M-2104 count-compound hypothesis stays alive only as:

```text
source_targeted_retrieval_and_segmentation_hypothesis
```

It is downgraded from candidate extraction to source-gated retrieval until CISI 3.1, a museum/archive image, or an equivalent source-grade photograph closes:

```text
M-2104 = Marshall no. 532 / VS 875
the actual raw shape
the local token segmentation
the exact stroke count after the U/V-like unit
```

## Current Accepted Claims

Accepted:

- The local row records `M-2104 / VS 875CXIV:532 / +151-097-700-034+`.
- Parpola 2019 makes `M-2104` a serious prior-work target for a `UIII` extraction test.
- Marshall Plate CXIV no. 532 is the best public target-side route found so far.
- The no. 532 region is visually inspectable enough to show a U/V-like unit plus adjacent stroke group.
- The `004` comparator side is two evidence units after dependence correction, not four independent rows.

Rejected or quarantined — quarantine means held out of all downstream work until the blocking problem is fixed:

- No accepted `034 = three`.
- No accepted `004 = four`.
- No accepted `700 = pot`, classifier, or count carrier.
- No accepted source bridge from public evidence alone.
- No accepted local four-token segmentation from the raw image.
- No sign meaning, phonetic value, language identity, or translation.

## Next Move

Stop widening the frame here — the frame being the run of surrounding signs used for comparison. The next decisive action is source acquisition, not another broad audit:

```text
Acquire or inspect CISI 3.1 / archive / museum material for M-2104.
Demand the explicit identity bridge and raw image for M-2104 / VS 875 / no. 532.
Then rerun blinded segmentation against EU_004_INDIA_478_479_480 and EU_004_PAKISTAN_1425.
```

Until then, the honest state is:

```text
M-2104 is the strongest current 034 count-compound target.
The exact target-side three-stroke claim fails today.
The translation count remains zero.
```
