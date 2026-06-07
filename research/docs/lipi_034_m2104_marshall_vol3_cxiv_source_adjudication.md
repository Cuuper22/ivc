# Lipi 034 M-2104 Marshall Vol III CXIV Source Adjudication

Date: 2026-05-25

## Question

Does the higher-resolution public Internet Archive/IGNCA scan of Marshall Vol. III, Plate CXIV, no. 532 validate the `M-2104` target-side `700-034` / `UIII` three-stroke hypothesis?

## Result

No decipherment upgrade.

It does make real progress: the best public source witness is now the Internet Archive/IGNCA Marshall Vol. III Plate CXIV page, not the lower-resolution Harappa gallery image. The target-side no. 532 crop is visibly better, and it clearly shows a U/V- or pot-like unit with an adjacent short-stroke cluster.

But the decisive claims still fail. The crop does not securely force exactly three strokes. Three secure strokes plus an ambiguous fourth boundary mark is possible; four-ish strokes are also plausible depending on segmentation. The image also does not by itself prove the crosswalk `Marshall no. 532 / VS 875 = CISI/local M-2104`, and Marshall's description of no. 532 as having five characters remains an active warning against silently treating the local four-token row as settled.

## Stored Outputs

- `data/open_prototype/reports/lipi_034_m2104_marshall_vol3_cxiv_source_routes.csv`
- `data/open_prototype/reports/lipi_034_m2104_marshall_vol3_cxiv_visual_inputs.csv`
- `data/open_prototype/reports/lipi_034_m2104_marshall_vol3_cxiv_visual_adjudication.csv`
- `data/open_prototype/reports/lipi_034_m2104_marshall_vol3_cxiv_summary.json`

Derived local visual files:

- `tmp/marshall_vol3/48270_0205.jp2`
- `tmp/marshall_vol3/48270_0205.png`
- `tmp/marshall_vol3/48270_0205_iiif_full_max.jpg`
- `tmp/marshall_vol3/derived/m2104_ia_48270_0205_no532_crop_overlay.png`
- `tmp/marshall_vol3/derived/m2104_ia_48270_0205_no532_pair_enhanced4x.png`
- `tmp/marshall_vol3/derived/m2104_ia_48270_0205_no532_impression_right_rot270_enhanced4x.png`
- `tmp/marshall_vol3/derived/m2104_ia_48270_0205_no532_inscription_zone_right_enhanced4x.png`

## Best Public Route

```text
Internet Archive item: in.gov.ignca.48270
Volume: John Marshall, Mohenjo-Daro and the Indus Civilization, Vol. III
Target leaf: 48270_0205
Plate: CXIV
Target object: no. 532
Image dimensions: 2601 x 3483
```

This is better than the Harappa `600 x 1000` plate image, but it is still a scan of the printed plate, not a fresh object photograph.

## Adjudication

| Reviewer | Count Read | Verdict | Risk |
| --- | --- | --- | --- |
| Local direct inspection | 3-vs-4 ambiguous; four plausible depending on boundary treatment | Source witness upgraded, no count validation | Print/scan blur, cylinder curvature, and absent CISI cross-reference. |
| Hypatia | 3 secure strokes plus at least one ambiguous neighboring or boundary mark | Source-visible and testable, exact `III` vs `IIII` unresolved | Contrast bloom, object/impression polarity, and edge contamination. |
| Kuhn | No secure downgrade to three; four-ish cluster plausible | Source lead upgraded, validation still fails | Visual resemblance cannot prove object identity or local four-token encoding. |
| Local synthesis | Exact three-stroke `034` fails; three-plus-boundary and four remain live | Best public witness found, no decipherment upgrade | CISI/local crosswalk and source segmentation remain required. |

## Pass / Fail

```text
best public Marshall Vol. III Plate CXIV route found: pass
Plate CXIV no. 532 visible: pass
U/V or pot-like unit visible: pass
adjacent stroke cluster visible: pass
Marshall five-character warning recorded: pass
explicit CISI/local M-2104 identity cross-reference found: fail
exact three-stroke 034 validated: fail
local four-token segmentation validated: fail
usable as standalone mapping evidence: fail
```

## Consequence

The `M-2104` branch is stronger as a source-acquisition target and weaker as an already-clean extraction. We now know exactly where the best public Marshall witness is, and the visual target is real. We also now have a sharper adversarial problem: if the object is five Marshall characters but four local tokens, then either later tokenization merged/excluded something, the crosswalk is incomplete, or the local row is over-normalized.

The next decisive evidence is not another broad web search. It is:

1. CISI 3.1 or later supplemental entry for `M-2104`, including old publication references. A later check found that CISI Pakistan Vol. 2 states its Mohenjo-daro section covers `M-595` and `M-621` to `M-1659`, so `M-2104` is outside that volume's stated scope.
2. Explicit confirmation whether `M-2104 = Marshall no. 532 / Plate CXIV / VS 875`.
3. Raw CISI, museum, or archive photograph of the object.
4. A segmentation note explaining Marshall's five characters versus the local four-token transcription.
5. Independent full-object segmentation covering broad face, narrow face, direction, and whether the narrow face belongs to the same text sequence.

## Claim Status

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted numerical values: 0
accepted source mappings: 0
accepted token boundaries from this image: 0
```

## Sources

- Internet Archive, Marshall Vol. III item: <https://archive.org/details/in.gov.ignca.48270>
- Internet Archive Plate CXIV page: <https://archive.org/details/in.gov.ignca.48270/page/n205/mode/1up>
- Internet Archive direct JP2: <https://archive.org/download/in.gov.ignca.48270/48270_jp2.zip/48270_jp2%2F48270_0205.jp2>
- Internet Archive IIIF full image: <https://iiif.archive.org/image/iiif/3/in.gov.ignca.48270%2F48270_jp2.zip%2F48270_jp2%2F48270_0205.jp2/full/max/0/default.jpg>
- Harappa, Indus Cylinder Seals: <https://www.harappa.com/node/3576>
- Harappa Plate CXIV image: <https://www.harappa.com/sites/default/files/cylinder-seals.jpg>
