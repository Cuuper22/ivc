# Lipi FRAME700 034 Independent Triad Audit

Date: 2026-05-25

## Question

This note decides which objects to request from image archives first, and in what order. FRAME700 is the project's label for short inscription rows built on sign `700`, such as `+700-034+`; the `034` work asks whether the sign codes `032`, `033`, and `034` are separate choices in the same slot. Testing that needs triads — sets of three objects, one carrying each sign code, matched closely enough to compare. The previous triad packet, a bundled list of candidate triads, ranked the best local metadata matches for every non-H-series `034` row. This audit asks a harder source-acquisition question:

```text
Which 034 triads are most independent, least copy-family-heavy, and worth requesting first from image/plate sources?
```

## Inputs

```text
data/open_prototype/reports/lipi_frame700_034_source_triad_packet.csv
data/open_prototype/reports/lipi_frame700_034_source_acquisition_manifest.csv
```

## Outputs

```text
data/open_prototype/reports/lipi_frame700_034_independent_triad_audit.csv
data/open_prototype/reports/lipi_frame700_034_independent_triad_audit_summary.json
data/open_prototype/reports/lipi_frame700_034_archive_request_batch.csv
```

## Method

A copy family is a set of objects carrying the same inscription that may be copies of one another, so counting them as separate evidence would double-count one act of writing. Each of the 93 source triads is scored for:

- source-hook coverage for target, `033` control, and `032` control — a source hook is an identifier in our own records that can be searched for in an archive; the target is the object the test is about, and a control is a comparison object used to check it
- repeated target longer-side token set
- acquisition-manifest sequence-family count
- repeated use of the same `033` or `032` control
- material/shape/cross-section comparability
- exact `700` order and side-relation risk

This is an ordering audit, not a reading. It does not assign sign value, word value, sound value, language, or translation.

## Result

```text
audited_triads: 93
all_three_have_source_hooks: 91
source_hook_gap: 2
archive_request_triads: 10
archive_request_rows: 30
```

Evidence tiers:

| Tier | Count |
| --- | ---: |
| A independent source-ready | 4 |
| B source-ready, needs metadata review | 7 |
| B source-ready, direction/control-reuse pressure | 35 |
| C repeated target-family pressure | 45 |
| D source-hook gap | 2 |

Copy-family pressure:

| Pressure | Count |
| --- | ---: |
| None beyond current metadata | 47 |
| Repeated target long set, count 28 | 28 |
| Repeated target long set 9 plus acquisition family 7 | 7 |
| Repeated target long set 4 | 4 |
| Repeated target long set 5 plus acquisition family 3 | 3 |
| Repeated target long set 5 | 2 |
| Repeated target long set 9 | 2 |

## First Independent Source Batch

These are now the first four source requests if the goal is independent pressure on the `034` residue — the leftover signal that has survived the controls run so far — rather than confirming the `+002-861-416+` branch first:

| Independence rank | Target | `033` control | `032` control | Why first |
| ---: | --- | --- | --- | --- |
| 1 | `H-1850 +700-034+` / `382;400;740;760` | `H-1842 +033-700+` | `H-1772 +700-032+` | all source hooks present; target long set count 1; acquisition family count 1; same object format |
| 2 | `H-771 +700-034+` / `032;257;840` | `H-789 +033-700+` | `H-1123 +700-032+` | all source hooks present; target long set count 1; acquisition family count 1; same object format |
| 3 | `H-1943 +700-034+` / `031;384;740` | `H-1940 +700-033+` | `H-854 +700-032+` | all source hooks present; target long set count 1; acquisition family count 1; same object format |
| 4 | `H-2204 +700-034+` / `027;032;400;740` | `H-2209 +700-033+` | `H-2217 +700-032+` | all source hooks present; target long set count 2; acquisition family count 1; same object format |

Source handles for rank 1:

```text
H-1850 target: H2001-5141; Figure 48.07
H-1842 033 control: H95-2416; Figure 26.07
H-1772 032 control: H2000-4437; Figure 39.05
```

Source handles for rank 2:

```text
H-771 target: 657678
H-789 033 control: 12549604
H-1123 032 control: 9015360
```

Source handles for rank 3:

```text
H-1943 target: H2000-4482; Figure 42.10
H-1940 033 control: H2001-5072; Figure 44.05
H-854 032 control: 10010647
```

Source handles for rank 4:

```text
H-2204 target: H95-2482; Figure 27.06
H-2209 033 control: H95-2423
H-2217 032 control: H95-2521; Figure 27.09
```

## What Changed

The earlier top triad, `H-910` against `H-916` and `H-1294`, is still useful, but it is no longer the first independent source request.

The whole `+002-861-416+` target branch has repeated-family pressure:

| Target | Old triad rank | New independence rank | Tier | Target long-set count | Acquisition family count |
| --- | ---: | ---: | --- | ---: | ---: |
| `H-910` | 1 | 50 | C repeated target-family pressure | 5 | 1 |
| `H-2097` | 3 | 64 | C repeated target-family pressure | 5 | 1 |
| `H-2094` | 2 | 72 | C repeated target-family pressure | 5 | 3 |
| `H-2095` | 5 | 90 | C repeated target-family pressure | 5 | 3 |
| `H-2096` | 4 | 91 | C repeated target-family pressure | 5 | 3 |

That does not kill the branch. It means one representative can be requested to check the companion pattern, but it should not monopolize the first independent evidence batch.

## Public Lead Check

Exact public-web searches on 2026-05-25 for the new rank-1 handles (`H-1850`, `H2001-5141`, `Figure 48.07`; `H-1842`, `H95-2416`, `Figure 26.07`; `H-1772`, `H2000-4437`, `Figure 39.05`) returned no source-grade object-side image or plate hit in the checked public search layer. The next action remains archive/source request, not more broad web trawling.

## Source Request Shape

The generated archive request batch asks for:

```text
all source images or plates for every side;
source plate/page/image identifier;
side labels and side order;
inscription versus impression direction;
sign segmentation;
object material, shape, cross-section, dimensions, condition, and find context
```

The requested evidence must answer whether the target `034`, `033` control, and `032` control are visually distinct and comparable under the same source rules.

## Boundary

No accepted translation. No accepted phonetic value. No accepted sign meaning. No accepted numerical or metrological value.

The narrow gain is this: source acquisition is no longer aimed at the prettiest top triad. It is aimed at the first independent triads that can actually break the `034` residue out of copy-family suspicion.
