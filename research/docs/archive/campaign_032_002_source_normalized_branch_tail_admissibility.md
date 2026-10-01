# 032-002 Source-Normalized Branch-Tail Admissibility

Date: 2026-05-28

## Question

This note is an admissibility check: before running a decisive test, it asks which rows have evidence good enough to be used at all. Signs in this corpus are numeric IDs; `Y` names whichever sign follows `002`. "Terminality" is whether a row ends right after `Y`. A "register" is the object class a row sits on — site, seal type, icon, shape. A row is "source-boxed" when boxes have been drawn on its published photograph marking where each sign sits; a "source route" is the traceable chain from a transcribed row back to that published page. A "holdout" is a test kept back and run only once, on evidence set aside in advance, so it cannot be tuned.

The statistical result says Y class predicts terminality better than broad register metadata. The hostile objection is still correct: terminality is corpus-order terminality until source images prove physical order and continuation.

This packet asks a narrower question:

```text
Which decisive branch-tail rows are already source-admissible, and which rows are only route targets?
```

## Inputs

- Tail-family instances: `campaign_032_002_post_y_tail_family_instances.csv`
- Source route packet: `campaign_032_002_y_source_route_probe.csv`
- Current source-visible table: `campaign_032_002_y_source_function_current_table.csv`
- Token-box scaffold: `campaign_032_002_y_token_box_scaffold_v1.csv`
- Script: `tmp/run_032_002_source_normalized_branch_tail_packet.py`

Outputs:

- `data/open_prototype/reports/campaign_032_002_source_normalized_branch_tail_decisive_rows.csv`
- `data/open_prototype/reports/campaign_032_002_source_normalized_branch_tail_family_rows.csv`
- `data/open_prototype/reports/campaign_032_002_source_normalized_branch_tail_summary.json`

Mechanic validation: PASS.

## Decisive Adjacent Rows

The adjacent `032-002` continuation question now rests on six rows.

| row | text | role | admissibility |
|---|---|---|---|
| `M-49` | `+527-550-240-220-032-002-300-350-032-190+` | target branch-head `300` | source-boxed candidate |
| `M-240` | `+520-240-220-032-002-861-603+` | target leaky `861` extension | source route known, needs image |
| `M-91` | `+740-100-798-220-032-002-861-255-416+` | non-target leaky `861` extension | source route known, needs image |
| `M-1677` | `+520-382-032-002-820-001-440-012+` | outside leaky `820` extension | source route known, needs image |
| `M-70` | `+226-032-002-390-692+` | outside branch-head `390` | needs source route |
| unknown `3335.1` | `+740-205-032-002-390-590-032+` | outside branch-head `390` with later `032` | blocked until object ID is resolved |

Admissibility counts:

| status | count |
|---|---:|
| source-boxed candidate | 1 |
| source route known, needs image | 3 |
| needs source route | 1 |
| blocked until object ID is resolved | 1 |

## What Is Actually Source-Boxed

Only `M-49` is currently source-boxed among the decisive continuation rows.

`M-49` status:

- source-visible row-level witness from India page `n58` / `India_0058.djvu`
- token-box scaffold candidate pass
- physical source image: `tmp/032_002_y_source_function_batch/M49_target_300_fullpanel_a.png`
- token overlay: `tmp/032_002_y_token_box_scaffold_v1/M49_token_boxes.png`

Visual check:

```text
032/P145 - 002/P122 - 300/P205
```

form a visible adjacent central cluster. The downstream `350-032-190` material continues leftward in physical order under the current R/L policy. This is the first real source-backed positive for a branch-head continuation after `032-002`.

Accepted from `M-49`:

- source-visible same-line `032-002-300`
- source-visible continuation after branch-head `300`
- target `240-220-032` can enter an extended branch, not only a closure

Not accepted:

- exact sign identity beyond provisional scaffold labels
- meaning of `300`, `350`, `032`, or `190`
- phonetic value or translation

## What Is Not Yet Source-Normalized

`M-240`, `M-91`, and `M-1677` are the high-value rows because they decide whether leaky closures are real:

```text
M-240   002-861-603
M-91    002-861-255-416
M-1677  002-820-001-440-012
```

They all have local source-reference routes but no source image in the current packet:

| row | route handle | needed |
|---|---|---|
| `M-240` | `HR 4098324` | plate/archive image for signband and direction |
| `M-91` | `DK6380429` | plate/archive image for signband and direction |
| `M-1677` | `DK11358130` | plate/archive image for signband and direction |

These rows cannot yet prove leaky closure. They define the acquisition queue.

`M-70` has local metadata:

```text
HR 4076048
+226-032-002-390-692+
```

but it was not routed in the current source-function packet. A local OCR hit for `RM-70` on Pakistan text-concordance page `Pakistan_0479.djvu` is register/table-like, not a source-panel route. Do not promote it.

The unknown `+740-205-032-002-390-590-032+` row has no CISI object ID. It is linguistically interesting because it is `390` plus later `032`, but it is source-blocked until the object can be identified.

## All-002 Tail Family Rows

The broader all-`002` tail families contain 18 rows:

| family | rows | current source state |
|---|---:|---|
| `002-220-065...` | 3 | all need source route |
| `002-220-455...` | 4 | all need source route |
| `002-390-125...` | 4 | all need source route |
| `002-390-705...` | 2 | one no object ID, one needs route |
| `002-861-533-717` | 2 | both need route |
| `002-861-603` | 3 | `M-240` route known; two need route |

This matters because branch-tail recurrence exists statistically, but the source-normalized holdout is not ready. The honest state is:

```text
branch-tail grammar: live
source-normalized branch-tail grammar: not yet proven
```

## Research Decision

Accepted:

- `M-49` is a real source-backed branch-head continuation candidate.
- The decisive branch-tail queue is now explicit and small.
- The hard holdout cannot be run honestly until at least `M-240`, `M-91`, and `M-1677` are source-imaged or replaced by source-visible analogues.

Rejected:

- treating the matched terminality result as source-normalized grammar
- treating leaky `861/820` continuations as proven physical continuations
- treating the all-`002` recurrent tail families as semantic codes before source-family checks

## Next Actions

1. Source-route `M-240`, `M-91`, and `M-1677` from their excavation/source handles.
2. Source-route `M-70` from `HR 4076048`.
3. Resolve object ID for unknown row `3335.1`.
4. Pull source routes for the 18 all-`002` family rows, starting with:
   - `M-1273`, `M-714`, and `M-240` for `002-861-603`
   - `M-376` and `M-391` for `002-861-533-717`
   - `M-38`, `M-119`, `M-735`, and `Sktd-1` for `002-390-125`
5. Only after source images exist, run the source-boxed/family-blocked/right-edge-matched holdout.

## 2026-05-28 Source Acquisition Addendum

Follow-up artifact: `campaign_032_002_branch_tail_source_acquisition.md`.

The acquisition state changed materially after checking public CISI India leaves by object range instead of only exact OCR hits.

New source-panel routes:

| row | branch-tail | public route |
|---|---|---|
| `M-240` | `002-861-603` | CISI India IA leaf `n95`, printed p.60, Mohenjo-daro 240-242 seals |
| `M-91` | `002-861-255-416` | CISI India IA leaf `n71`, printed p.36, Mohenjo-daro 89-94 seals |
| `M-70` | `002-390-692` | CISI India IA leaf `n66`, printed p.31, Mohenjo-daro 70-72 seals |

Source-visible decisive adjacent set now includes `M-49`, `M-240`, `M-91`, and `M-70`. `M-1677` remains the missing source route for leaky `820`, and unknown `3335.1` remains blocked until object-ID resolution.

Research consequence: source-normalized leaky `861` continuation is now a live image-backed hypothesis requiring token-box/direction adjudication; source-normalized leaky `820` continuation is still not proven.
