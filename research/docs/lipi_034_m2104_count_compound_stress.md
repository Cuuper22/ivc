# Lipi 034 M-2104 Count-Compound Stress

Date: 2026-05-25

Question:

```text
Does the local corpus support or kill the M-2104 hypothesis that 700-034 corresponds to Parpola's UIII cluster while 700-004 corresponds to UIIII?
```

Input:

- `data/open_prototype/lipi/metadata_filtered.csv`
- Prior M-2104 packets:
  - `docs/lipi_034_m2104_parpola_extraction.md`
  - `docs/lipi_034_m2104_visual_stroke_probe.md`
  - `docs/lipi_034_m2104_marshall_vol3_cxiv_source_adjudication.md`
  - `docs/lipi_034_m2104_cisi31_bridge_route_probe.md`

Output:

- `data/open_prototype/reports/lipi_034_m2104_count_compound_contexts.csv`
- `data/open_prototype/reports/lipi_034_m2104_count_compound_frames.csv`
- `data/open_prototype/reports/lipi_034_m2104_count_compound_tests.csv`
- `data/open_prototype/reports/lipi_034_m2104_count_compound_summary.json`

## Live Claim

Parpola 2019 treats `M-2104` as text no. 12, described as `UIII` plus signs 15 and 1. The named tablet parallels `M-478`, `M-480`, and `M-1425` are described as `UIIII` plus signs 15 and 107.

Local rows:

```text
M-2104: +151-097-700-034+
M-478:  +400-097-700-004+
M-480:  +400-097-700-004+
M-1425: +400-097-700-004+
```

The live extraction is:

```text
097                    = Parpola sign 15 candidate
151       vs 400       = Parpola sign 1 vs sign 107 candidate
700-034   vs 700-004   = UIII vs UIIII count/pot-cluster candidate
```

## Corpus Stress Result

```text
context rows: 139
frame rows: 17
test rows: 6
forward 700-034 rows: 116
reversed 034-700 rows: 14
forward 700-004 rows: 9
reversed 004-700 rows: 0
exact 097-700-034 rows: 1
exact 097-700-004 rows: 4
```

The narrow `097-700-X` frame is real:

```text
M-2104: +151-097-700-034+
M-478:  +400-097-700-004+
M-479:  +400-097-700-004+
M-480:  +400-097-700-004+
M-1425: +400-097-700-004+
```

`M-479` is not one of Parpola's named parallels in the current extraction, but the local corpus puts it in the same exact `+400-097-700-004+` family. That is useful, but it also means the `004` side is one repeated exact sequence family, not four independent substitutions.

The `097` left-context enrichment is strong in the local planning layer:

```text
prev097 among 700-004: 4/9
prev097 among 700-034: 1/116
right-tail Fisher p: 0.0000628573
```

This is a useful targeting signal, not a sign value. The counts are heavily structured by one Mohenjo-daro exact family and a large unrelated Harappa `+700-034+` short-mark population.

## Supports

- The exact suffix frame `097-700-X` contains the target `M-2104` on the `034` side and four Mohenjo-daro `004` rows on the other side.
- The result matches the prior-work pressure from Parpola 2019: `UIII` for M-2104 and `UIIII` for the named tablet parallels.
- Public CISI crops for `M-478` and `M-1425` already survived first-pass blind visual review as four-stroke/U-pot-like parallel witnesses.
- Public routing has moved from prose-only to source-testable: `M-478/M-480` are on CISI India leaf `n150`, `M-1425` is on CISI Pakistan leaf `n227`, and the target has a public Marshall Plate CXIV no. 532 route.

## Downgrades

- No Parpola-like multi-token full-sequence wildcard frame contains both variants. The exact full-frame contrast is `151-097-700-034` versus `400-097-700-004`, not a same-frame minimal pair — the two rows differ in two slots, not one.
- The only full-sequence wildcard frame with both variants is bare `+700-X+`, dominated by Harappa tablet short marks. That is a different problem from the M-2104 count-compound claim.
- `M-2104` remains source-gated. The public Marshall route is compatible, but CISI 3.1 or equivalent source metadata has not yet closed `M-2104 = Marshall no. 532 / VS 875`.
- Marshall's five-character description remains unreconciled against the local four-token row.
- The public target image keeps exact stroke count ambiguous; current reviewers allow three-plus-boundary and four-ish readings.
- `034` outside `700-034` exists in several contexts (`M-315`, `M-685`, `M-1206`, `M-1584`, `M-1963`), so no broad `034 = three` mapping is admissible.

## Adversarial Kill Gates

Hard kill if any of these fail:

1. Source bridge: CISI 3.1 or equivalent source must link `M-2104` to the target image/source route.
2. Standardization circularity: image-first reviewers must identify the U/pot-like unit and stroke group before using Parpola/local labels.
3. Stroke count: `M-2104` must force exactly three separable strokes in the relevant cluster.
4. Comparator symmetry: at least one `700-004` comparator must force exactly four separable strokes under the same image standard.
5. Direction/order: source conventions must show that `700-034` and `700-004` are not artifacts of normalized transcription order.
6. Tokenization: the `700` unit and following `034/004` component must be separable or consistently treated as a compound across target and comparators.
7. Duplicate-family: the `004` evidence cannot be counted as four independent witnesses if it is one repeated formula family.
8. Object-class: the result must not reduce to rod-versus-tablet, Mohenjo-daro versus Harappa, or short-mark versus line-text behavior.
9. Five-character warning: Marshall no. 532's five-character description must be reconciled with the local four-token segmentation.

## Adjudication

Accepted:

- M-2104 remains the strongest current `034` crosswalk target.
- The `097-700-X` frame gives a real local-corpus targeting signal.
- `M-479` should be added to the source-check set as an unmentioned local member of the `+400-097-700-004+` family.

Rejected or quarantined:

- No `034 = three` mapping is accepted.
- No `004 = four` mapping is accepted.
- No `700` value or classifier role is accepted.
- No sign meaning, phonetic value, language identity, or translation is accepted.
- The claim is not generalized to other `034` contexts.

Current status:

```text
M-2104 count-compound hypothesis = survives as count_hypothesis_unvalidated
```

Follow-up:

`M-479` has now been source-checked on CISI India leaf `n150`. It is visible as `M-479 A/B` on the same `MOHENJO-DARO 478-481` tablet plate as `M-478/M-480`, and the CISI introduction leaf `n19` explicitly discusses `M-478/M-479` as a four-plus-U case. This upgrades M-479 from a hidden local extra to a source-visible family-internal comparator, but it also sharpens the duplicate-family warning: it cannot be counted as an independent recurrence yet.

A separate family-dependence adjudication now collapses the four local `+400-097-700-004+` rows into two evidence units:

```text
EU_004_INDIA_478_479_480 = one same-plate tablet-family unit
EU_004_PAKISTAN_1425     = one provisional independent recurrence
```

It is not solved. It is also not dead. The next decisive move is raw/source-grade M-2104 evidence, then blind segmentation against `M-478`, `M-479`, and `M-1425`, with `M-480` retained as the weaker same-plate comparator.

Target-side gate recheck:

```text
EU_004_INDIA_478_479_480 = one same-plate tablet-family unit
EU_004_PAKISTAN_1425     = one provisional independent recurrence
EU_034_TARGET_2104       = one source-gated target unit
```

Applying that unit policy to the best public M-2104 source produces a negative exact-count result. IA/IGNCA Marshall Plate CXIV no. 532 is source-visible, but the target-side cluster remains `U/V-like unit + 3 secure adjacent strokes + possible fourth/boundary mark`. The public layer also still lacks an external bridge that explicitly says `M-2104 = Marshall no. 532 / VS 875`.

Updated status:

```text
M-2104 count-compound hypothesis = source_targeted_retrieval_and_segmentation_hypothesis
exact 034 = three = failed at current public-source resolution
accepted mappings/translations = 0
```
