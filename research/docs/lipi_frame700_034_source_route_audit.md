# Lipi FRAME700 034 Source Route Audit

Date: 2026-05-25

## Question

For the actual 25-object FRAME700 `034` two-lane packet, what source-acquisition route exists right now?

This is not a decipherment claim. It is the acquisition map for the next evidence move.

## Local Artifacts

```text
data/open_prototype/tools/lipi_frame700_034_source_route_audit.mjs
data/open_prototype/reports/lipi_frame700_034_source_route_audit.csv
data/open_prototype/reports/lipi_frame700_034_source_route_audit_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_frame700_034_two_lane_source_packet.csv
```

## Sources Checked

- Internet Archive metadata for the Mahadevan/CISI scan bundle: https://archive.org/metadata/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan
- Internet Archive reader for the same bundle: https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan
- Harappa.com CISI 3.1 bibliographic page: https://www.harappa.com/content/corpus-indus-seals-and-inscriptions-vol-31
- University of Helsinki CISI 3.1 bibliographic record: https://researchportal.helsinki.fi/en/publications/corpus-of-indus-seals-and-inscriptions-volume-3-new-material-untr/
- CISI volumes 1 through 3.2 advertisement/order sheet: https://list.indology.info/pipermail/indology/attachments/20200116/6fb825d1/attachment.pdf
- HARP overview: https://www.harappa.com/content/harp
- Kenoyer and Meadow 2010 Harappa inscribed-objects source page: https://www.harappa.com/content/inscribed-objects-harappa-excavations-1987-2007
- Vats 1940 Harappa excavation text and plates route: https://www.harappa.com/content/Excavations-at-Harappa
- Harappa 1998-2000 public article with H95-2482 listing: https://www.harappa.com/indus4/e3.html
- Kenoyer 1997 Harappa 1994-1995 public PDF: https://www.harappa.com/sites/default/files/pdf/Kenoyer1997_Excavations%20at%20Harappa%201994-1995%20New%20Perspective.pdf
- ICIT access page: https://www.epigraphica.de/indus/menueindus.htm
- Parpola 2019 bone/ivory rods PDF: https://tuhat.helsinki.fi/ws/portalfiles/portal/129602857/Parpola_A_2019_Inscriptions_incised_on_the_Harappan_bone_rods_Proceedings_of_EASAA_22.pdf

Notes:

- Harappa.com identifies CISI 3.1 as the Mohenjo-daro/Harappa volume and gives its bibliographic route.
- The Helsinki record confirms the 2010 CISI 3.1 book metadata and ISBN.
- The CISI order sheet states the corpus purpose as providing research images of Indus seals and inscriptions, and lists volumes 1, 2, and 3.1 with image counts.
- ICIT is valuable but access-gated, so it is not a current image source.
- Vats 1940 is an online old-excavation text/plate route for legacy Harappa material, but H-number to plate/object reconciliation must be done through CISI/Kenoyer tables before using it.

## Result

```text
packet_objects: 25
core_objects: 22
optional_objects: 3
ia_ocr_hit_objects: 9
ia_ocr_hit_total: 27
direct_or_table_public_identity_leads: 3
secondary_textual_lead_objects: 2
source_request_only_objects: 3
accepted_decipherment_claims: 0
```

Route classes:

| Route class | Objects |
| --- | ---: |
| `cisi_3_1_library_or_purchase_request` | 11 |
| `internet_archive_cisi_vol1_2_ocr_lead` | 6 |
| `cisi_vol2_archive_request_no_public_ocr_hit` | 3 |
| `internet_archive_cisi_vol1_2_ocr_plus_secondary_text_lead` | 2 |
| `harappa_harp_public_object_lead_plus_cisi_3_1_reconcile` | 1 |
| `kenoyer_1997_table2_plus_cisi_scan_lead` | 1 |
| `kenoyer_1997_table2_public_lead` | 1 |

CISI volume targets:

| Target | Objects |
| --- | ---: |
| `CISI_3_1_Mohenjo-daro_and_Harappa` | 12 |
| `CISI_2_Collections_in_Pakistan` | 9 |
| `CISI_1_or_2_legacy_Harappa_entry` | 2 |
| `CISI_2_Collections_in_Pakistan_or_later_addenda` | 1 |
| `CISI_2_Collections_in_Pakistan_with_HARP_comparison` | 1 |

## Concrete Acquisition Consequence

The packet is not all equally dark.

The first practical source route is:

1. Use the Internet Archive CISI vol. 1/2 scans as plate locators for the nine OCR-hit objects: `H-212`, `H-353`, `H-771`, `H-789`, `H-893`, `H-925`, `H-930`, `H-983`, and optional `H-910`.
2. Use Kenoyer 1997 public Table 2 immediately for identity reconciliation on `H-212` and optional `H-916`.
3. Use Vats 1940 plates as a legacy route for older Harappa objects only after the CISI/Kenoyer crosswalk confirms which plate/object number belongs to the packet row.
4. Use the Harappa public H95-2482 lead to reconcile `H-2204`, but do not treat it as row validation because the public object identity and local `H-2204/Fig 27.06` still need alignment.
5. Acquire CISI 3.1 for the twelve HARP/H2000/H2001 targets: `H-1772`, `H-1824`, `H-1842`, `H-1850`, `H-1883`, `H-1940`, `H-1943`, `H-2137`, `H-2204`, `H-2209`, `H-2211`, and `H-2217`.
6. Keep `H-854`, `H-1123`, and optional `H-1294` as direct request-only objects because exact IA OCR did not surface them in this pass.

## What This Changes

Before this audit, the next step was vaguely "CISI/HARP/archive images."

Now the next step is smaller and nastier:

```text
Open the IA CISI scans and manually locate the nine OCR-hit packet objects first,
then use those pages to fill source citation, plate ID, side count, side order,
direction basis, and 032/033/034 visibility fields in the two-lane coding sheet.
```

That gives us a real chance to kill or preserve parts of the `034` contrast before waiting on the whole CISI 3.1 acquisition route.

## Follow-up Page Locator

The IA OCR-hit branch has now been page-located in [Lipi FRAME700 034 IA CISI page locator](lipi_frame700_034_ia_cisi_page_locator.md):

```text
IA route objects input: 9
located objects: 9
page locator rows: 11
total OCR hits: 27
```

First manual inspection pages:

```text
CISI Pakistan leaves 358, 359, 371, 373, 374, and 377
CISI India duplicate-locator pairs 265/696 and 406/837
optional CISI Pakistan leaf 372
```

## Boundary

No sign meaning, phonetic value, numerical value, administrative role, language identity, or translation is accepted here.

Every route row has:

```text
accepted_decipherment_claim = 0
```
