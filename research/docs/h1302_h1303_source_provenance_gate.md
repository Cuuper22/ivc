# H-1302/H-1303 Source Provenance Gate

Date: 2026-05-26

## Question

```text
Does the published Daggumati/Revesz 2021 direction/allograph note give H-1302/H-1303 usable source evidence, or only a source-acquisition lead?
```

## Artifacts

```text
data/open_prototype/reports/h1302_h1303_source_provenance_gate.csv
data/open_prototype/reports/h1302_h1303_source_provenance_gate_summary.json
```

Follow-up route check:

```text
docs/h1302_h1303_cisi_public_route_check.md
data/open_prototype/reports/h1302_h1303_cisi_public_route_check.csv
data/open_prototype/reports/h1302_h1303_cisi_public_route_check_summary.json
data/open_prototype/reports/h1302_h1303_source_request_log.csv
data/open_prototype/reports/h1302_h1303_source_request_log_summary.json
```

Source/context files:

```text
tmp/h1302_h1303_direction_prior_work/daggumati_revesz_2021_allographs_nature_article.pdf
tmp/h1302_h1303_direction_prior_work/daggumati_revesz_2021_allographs_nature_article.html
tmp/h1302_h1303_direction_prior_work/daggumati_revesz_2021_allographs_nature_article.pdftotext.txt
tmp/h1302_h1303_direction_prior_work/derived/pdf_pages/nature_page06_h1302_h1303_paragraph_crop.png
```

The first downloaded `daggumati_revesz_2021_allographs.pdf` is not usable source evidence. It is browser challenge HTML mislabeled as a PDF.

## Local Rows Under Review

```text
H-1302
4073.1 L/R +400-740-176+
4073.2 R/L +700-033+

H-1303
4077.1 L/R +400-740-176+
4077.2 R/L +700-033+
```

Both are `TAB:I` two-row packet objects in the short-mark source acquisition queue.

## Published Source Check

Source:

```text
https://www.nature.com/articles/s41599-021-00713-0
https://www.nature.com/articles/s41599-021-00713-0.pdf
```

The valid Nature PDF was acquired and confirmed as `%PDF-1.4`, 1,616,753 bytes, SHA256:

```text
1061899319d35477b8e4cf395993d837540f575222084b99587904a262752e0c
```

The PDF/HTML/page crop verify the prior-work claim: the article treats `H-1302`, `H-1303`, and `H-1822` as mirrored-writing / ICIT-correction cases after CISI comparison.

This is a real source-provenance upgrade over a vague citation. It says these exact objects are in a published correction-risk discussion.

## What It Does Not Prove

The article does not fill the local packet validation fields.

It does not prove:

- local `4073.2` or `4077.2` is physically the short side;
- local `R/L` direction is source-grade rather than corpus policy;
- `+700-033+` is visibly correct on either object;
- the inline article glyphs map to local lipi `700` or `033`;
- the Blogger candidate object panels are H-1302 or H-1303;
- a sign value, side function, language identity, or translation.

## Decision

`H-1302/H-1303` become higher-priority correction-risk acquisition targets, not accepted evidence.

The next gate is exact source reconciliation:

1. CISI/HARP source panels for all catalog sides of both objects.
2. Object-specific side labels and image-direction basis.
3. ICIT/Wells/Fuls row or note showing exactly what was corrected.
4. A controlled crosswalk between the article inline glyphs and local numeric lipi signs.
5. Caption/source binding for the public Blogger object-panel candidates before using them as object evidence.

This exact request has now been sent to Harappa:

```text
gmail:[redacted-msgid]
subject: Source image request: H-1302 and H-1303 Harappa tablets
```

## Boundary

This gate accepts no local sign correction, sign segmentation, side order, physical side function, numerical or metrological value, sign meaning, phonetic value, language identity, or translation.
