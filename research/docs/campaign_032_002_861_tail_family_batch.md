# 032-002 861 Tail-Family Batch

Date: 2026-05-29

## Question

The bare-edge packet made the contrast source-visible. The next question is not one row or one sign:

```text
Which post-861 tail families behave like restricted post-closure material,
and which are just broader formula material that sometimes follows 861?
```

This campaign batches the live post-`861` tails:

```text
603
533-717
255-416
096
416
698
000
```

## Stored Outputs

```text
tmp/run_032_002_861_tail_family_batch.py
data/open_prototype/reports/campaign_032_002_861_tail_family_batch_families.csv
data/open_prototype/reports/campaign_032_002_861_tail_family_batch_occurrences.csv
data/open_prototype/reports/campaign_032_002_861_tail_family_batch_summary.json
```

Input layers:

```text
data/open_prototype/reports/campaign_032_002_861_suffix_split_rows.csv
data/open_prototype/lipi/metadata_filtered.csv
strict complete source strings, text/site/type/symbol dedup: 4011 rows
```

## Family Table

| tail family | strict rows after `002-861` | occurrences anywhere | after `002-861` | non-`861` occurrences | current class |
|---|---:|---:|---:|---:|---|
| `603` | 3 | 7 | 3 | 4 | mixed post-`002-861` and independent |
| `533-717` | 2 | 2 | 2 | 0 | restricted to `002-861` in current strict layer |
| `255-416` | 1 | 1 | 1 | 0 | restricted singleton |
| `096` | 1 | 2 | 1 | 1 | mixed |
| `416` | 1 | 45 | 6 | 39 | broad formula material |
| `698` | 1 | 9 | 2 | 7 | broad formula material |
| `000` | 0 exact strict tail rows | 810 | 1 | 806 | background sign, not a target |

## Batch Read

1. `533-717`: strongest restricted post-`861` target in this batch because both current occurrences sit after `002-861`.
2. `603`: strongest repeated mixed target because it occurs after `002-861` three times and also has independent formula life.
3. `255-416`: restricted singleton; useful as a stress case, not as the carrier of the model.
4. `096`: low-count mixed tail.
5. `416` and `698`: broad formula/background controls, not good restricted-tail evidence in this pass.
6. `000`: background sign, not a post-`861` family target.

## Distribution Split

The batch separates three behaviors that should not be blended:

```text
restricted post-861 zone:
  533-717
  255-416, but singleton

mixed post-861 / independent formula zone:
  603
  096, weak

background formula material:
  416
  698
  000
```

The useful linguistic hypothesis to test next is narrower than "861 is sometimes followed by terminal material":

```text
002-861 can close bare,
and the rows that continue after it may split into
restricted addendum/subclass material and broader formula material.
```

## Next Decision

Run the restricted/mixed split against source and context:

| target | next test |
|---|---|
| `533-717` | Test whether the `M-376/M-391` no-icon rectangular context groups as a post-`861` addendum/subclass candidate without deciding the status in advance. |
| `603` | Compare the three post-`861` rows against the independent `740-603-240-060-692` lane. |
| `255-416` | Treat as singleton stress only; do not let it carry the model. |
| `416/698` | Use as negative controls for broad terminal material. |

No sign value, phonetic reading, language identity, or translation is accepted.
