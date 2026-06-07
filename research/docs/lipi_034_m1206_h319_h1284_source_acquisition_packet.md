# Lipi 034 M-1206 H-319/H-1284 Source Acquisition Packet

Date: 2026-05-26

## Question

What exact source evidence is needed before `H-319` and `H-1284` can upgrade the M-1206 `034/415` branch?

## Current State

`H-319` and `H-1284` are not evidence yet.

They matter because both carry the same local side family:

```text
1:+520-220-415+ | 2:+700-034+
```

That is the forward companion pattern that would make `H-938` less isolated if source-validated. But the source-route recheck failed to upgrade either target:

- `H-319` is visible only on CISI India `n406/n837`, printed p. 371, as a data/register row. The two downloaded pages are byte-identical. There is no inscription panel.
- `H-1284` has no exact public CISI 1/2 source route in the checked layer. Parpola 2019 is only a secondary clue, not a source image.

## Primary Targets

| Priority | Object | Local exact `415` side | Local `034/700` side | Current status | Request |
| ---: | --- | --- | --- | --- | --- |
| 1 | `H-319` | `1341.1 +520-220-415+` | `1341.2 +700-034+` | register/data-only route | all-side source panels, source data row, side labels/order, direction basis, segmentation |
| 2 | `H-1284` | `4069.1 +520-220-415+` | `4069.2 +700-034+` | route-dark in checked public CISI 1/2 | all-side source panels, source data row, side labels/order, direction basis, segmentation |

Secondary context:

- `H-938` is the clean source-panel-audited control: `A/A bis +520-220-415+`, `B +034-700+`.
- `H-939` is source-visible but not strict-upgraded.
- `H-2145` is only a related secondary-literature clue because its local longer side is `+074-220-415+`, not exact `+520-220-415+`.

## Required Evidence

The packet requires five bridges before any source upgrade:

1. Object bridge: source label, source hook, or catalogue row must identify the object as `H-319 / 10060544` or `H-1284 / -458`.
2. Side bridge: source side labels must be object-specific. Do not infer local `.1/.2` from source `A/B`.
3. Visual diagnostics: image quality must distinguish `034` from `032/033` and must show the terminal `415` form clearly.
4. Direction/order basis: inscription, impression, or catalog-normalized order must be documented well enough to preserve `+700-034+` versus `+034-700+`.
5. Independence check: copy, template, mold, duplicate-photo, or workshop/family dependence must be recorded rather than hidden.

Report files:

```text
data/open_prototype/reports/lipi_034_m1206_h319_h1284_source_acquisition_targets.csv
data/open_prototype/reports/lipi_034_m1206_h319_h1284_source_acquisition_gates.csv
data/open_prototype/reports/lipi_034_m1206_h319_h1284_source_acquisition_summary.json
data/open_prototype/reports/lipi_034_m1206_h319_h1284_source_admissibility_overrides.csv
data/open_prototype/reports/lipi_034_m1206_h319_h1284_source_admissibility_overrides_summary.json
```

The override table is a guardrail for old local/model reports. It marks `H-319` and `H-1284` as acquisition-only even when older rows call them `clean_side_row`, `lipi_numeric_clean_candidate`, `FRAME700_SUBTYPE034`, or model top-1 predictions. Those labels are local parse/model labels, not source-grade evidence.

## Upgrade Condition

`H-319` or `H-1284` can upgrade only if the source shows:

```text
one physical side carrying exact +520-220-415+
one companion physical side carrying exact +700-034+
object-specific side mapping
documented direction/order basis
visible diagnostic distinction between 034 and 032/033
visible terminal 415 form
copy/template/family status recorded
```

If both upgrade, the claim becomes:

```text
H-938 is not the only source-grade same-object 034/415 pressure case.
```

That would strengthen the sign-inventory problem. It would still not be a reading.

## Downgrade Conditions

Any of these blocks the upgrade:

- Only register or prose evidence is available.
- Side labels cannot be bridged to local sign rows.
- The source order can flip or normalize `+700-034+` without documentation.
- `034` is damaged, ambiguous, or collapses visually into `032/033`.
- Terminal `415` is not visible enough to compare.
- The objects collapse to one copy/template family.

## Claim Status

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted numerical values: 0
accepted allograph decisions: 0
accepted source upgrades for H-319/H-1284: 0
```

## Outbound Action

Created and sent a Gmail request from `cuuper225@gmail.com` to `[harappa-project-email]`.

```text
sent_message_id: [redacted-msgid]
thread_id: [redacted-msgid]
status: sent
```

## Email Body

```text
Subject: Source image request: H-319 and H-1284 Harappa tablets

Dear Harappa team,

I am working on a non-commercial scholarly project on Indus script source validation. I am trying to verify two very specific Harappa tablet records before using them in any argument:

- H-319 / source hook 10060544
- H-1284 / source hook -458

The local corpus rows I am trying to source-check are:

- H-319: 1341.1 +520-220-415+ and 1341.2 +700-034+
- H-1284: 4069.1 +520-220-415+ and 4069.2 +700-034+

For H-319, I found the CISI India data/register page only: n406/n837, printed p. 371. It confirms a register route but does not show the inscription sides. For H-1284, I have not found a public CISI 1/2 image route; Parpola 2019 mentions H-1284 in a related Harappa incised-tablet discussion, but that is only a secondary clue.

Could you help me access source-grade images, plate references, or catalogue notes for these objects?

The specific evidence I need is:

1. all available sides/panels for H-319 and H-1284;
2. source side labels and whether side order is physical, photographic, editorial, or arbitrary;
3. inscription/impression/catalog-normalized direction basis;
4. source transcription or segmentation notes for the two sides above;
5. enough image quality to distinguish the +700-034+ side from nearby 032/033 forms and to inspect the terminal 415 form;
6. any notes on duplicate photography, copy/template/workshop family, condition, damage, dimensions, findspot, period/phase/stratum, or uncertainty.

I am not asking for an interpretation. The goal is to keep the evidence clean: if the source images or notes do not support the local row pairing, I will record that as a negative result.

If this request is better routed to HARP, CISI 3.1, Andreas Fuls, or another archive/source holder, I would be grateful for the right route.

Best,
Cuper Y. Ashraf
cuuper225@gmail.com
```
