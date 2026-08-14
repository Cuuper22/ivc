# Lipi 034 M-2104 Parpola Extraction

Date: 2026-05-25

## Supersession Note

This is a hypothesis artifact, not an accepted mapping. It is superseded by the later target-side gate: the target is source-visible, but exact three-stroke `034`, the public `M-2104 = Marshall no. 532 / VS 875` identity bridge, and the local four-token segmentation all fail acceptance in the public evidence layer.

Question:

```text
Can Parpola 2019 text no. 12 and its named parallels explain the local lipi row M-2104 +151-097-700-034+?
```

Inputs:

- `data/open_prototype/lipi/metadata_filtered.csv`
- `data/open_prototype/reports/crosswalk_lipi_to_mayig_candidates.csv`
- Parpola 2019, Fig. 1 and prose around text no. 12

Outputs:

- `data/open_prototype/reports/lipi_034_m2104_parpola_context_rows.csv`
- `data/open_prototype/reports/lipi_034_m2104_parpola_mapping_hypotheses.csv`
- `data/open_prototype/reports/lipi_034_m2104_parpola_extraction_summary.json`

Rendered visual check:

- `tmp/pdfs/parpola_2019_page2-2.png`
- `tmp/pdfs/parpola_2019_fig1_text12_crop3.png`

## Result

```text
target: M-2104
target local row: +151-097-700-034+
named tablet parallels:
  M-478:  +400-097-700-004+
  M-480:  +400-097-700-004+
  M-1425: +400-097-700-004+
context rows stored: 9
mapping-hypothesis rows stored: 6
accepted mappings: 0
accepted decipherment claims: 0
```

Parpola's prose says text no. 12 (`M-2104`) begins with `UIII` ("three pots"), followed by signs 15 and 1. The three named tablet parallels begin with `UIIII` ("four pots"), followed by signs 15 and 107.

The local lipi rows line up as:

```text
M-2104: +151-097-700-034+
M-478:  +400-097-700-004+
M-480:  +400-097-700-004+
M-1425: +400-097-700-004+
```

That makes the live extraction:

```text
151       vs 400       = Parpola sign 1 vs sign 107 candidate
097                    = Parpola sign 15 candidate
700-034   vs 700-004   = UIII vs UIIII pot-count cluster candidate
```

This is the first useful internal explanation of the P0 (top-priority) `034` row. It explains why local lipi has four tokens while Parpola prose has three units: Parpola groups the pot-count cluster (`UIII` / `UIIII`) as a unit, while local lipi splits it into `700-034` / `700-004`.

## Hypotheses

| Local sign/group | Parpola candidate | Grade | Status |
| --- | --- | --- | --- |
| `151` | sign 1 | B | Supported by M-2104, H-543, H-544, M-915; source images still required. |
| `097` | sign 15 | B | Invariant between M-2104 and all three tablet parallels; also supported by H-543/H-544/M-915 under R/L reading. |
| `700` | U/pot component of `UIII`/`UIIII` | C | Shared compound component; do not map alone yet. |
| `034` | three-stroke count component in `UIII` | C | Single target, high value because it is the live `034` object. |
| `004` | four-stroke count component in `UIIII` | C | Three named tablet parallels, still source-image pending. |
| `400` | sign 107 | C | Tablet-parallel tail hypothesis, source-image pending. |

## Conflicts

Parpola also names M-715 and M-896 in the surrounding discussion of the signs 15 and 1 sequence. The current local rows do not cleanly expose the expected `151/097` pair:

```text
M-715: +520-220-016-741-556-000[
M-896: +151-031-090-032-001-505+
```

Those are not discarded. They become source-check conflicts. If source photos, variant notes, or catalog corrections explain them, they can support or kill the `151/097` extraction.

## Boundary

Accepted translations: 0

Accepted phonetic values: 0

Accepted sign meanings: 0

Accepted source mappings: 0

Accepted sign-list mappings: 0

The extraction is strong enough to prioritize source inspection, not strong enough to accept a sign value. The next test is visual and adversarial: compare the `700-034` cluster in M-2104 against the `700-004` cluster in M-478, M-480, and M-1425 from source images.

## Next Move

1. Get or inspect CISI images for M-2104, M-478, M-480, and M-1425.
2. Verify whether `034` and `004` are actually three-stroke and four-stroke count components in the same pot-count cluster.
3. Inspect H-543, H-544, and M-915 for the `097-151` R/L control.
4. Resolve M-715 and M-896 as conflicts, not exceptions to ignore.
