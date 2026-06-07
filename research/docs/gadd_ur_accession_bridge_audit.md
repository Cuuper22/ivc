# Gadd Ur Accession Bridge Audit

Date: 2026-05-30

This audit tests a narrower Priority A route than the earlier site-overlap joins: whether the Gadd Ur corpus contains an object-level micro-bilingual that can tie a local external Indus row to a readable cuneiform name, title, or Meluhha-tagged formula.

It does not. It does, however, improve the object identity layer for two local Ur rows.

## Inputs

- `data/meluhha/tools/audit_gadd_ur_accession_bridge.mjs`
- `data/meluhha/gadd_ur_accession_bridge_audit.csv`
- `data/meluhha/gadd_ur_accession_bridge_audit_summary.json`
- `data/meluhha/external_indus_objects.csv`
- `data/open_prototype/lipi/metadata_filtered.csv`
- Downloaded Gadd PDF: `tmp/gadd_ur/gadd_1932_33779.pdf`
- Rendered source contact sheets: `tmp/gadd_ur/pages_10_24_contact.jpg`, `tmp/gadd_ur/pages_22_34_contact.jpg`

External source routes:

- Gadd PDF: `https://ignca.gov.in/Asi_data/33779.pdf`
- British Museum Gadd bibliography page: `https://www.britishmuseum.org/collection/term/BIB2877`
- Penn Museum Journal, Woolley 1933: `https://www.penn.museum/sites/journal/9405/`

## Result

The modeled Gadd/BM/Penn surface has:

| Count | Value |
| --- | ---: |
| Local Ur rows checked | 5 |
| Local rows with verified excavation mapping | 2 |
| Candidate publication mappings | 2 |
| Modeled Gadd objects | 8 |
| Indus-sequence-only modeled objects | 7 |
| Cuneiform-only modeled objects | 1 |
| Objects with both Indus sequence and readable cuneiform | 0 |
| Accepted external phonetic anchors | 0 |

The two verified local row mappings are:

| Local row | Accession | Object route | Verdict |
| --- | --- | --- | --- |
| `3898.1` | `U17649` | Gadd no. 16 / Penn Museum Journal Plate XXX:2 | Mapped object, no cuneiform/name/title bridge |
| `3899.1` | `U8685` | Gadd no. 15 | Mapped object, no cuneiform/name/title bridge |

The best route is `3898.1 / U17649`. The local row is a circular Ur seal with text `+002-004-328-001-803-415+`. Woolley's Penn Museum Journal account says `U.17649` is a grey steatite circular stamp seal with a buffalo and a Mohenjo-daro-type inscription. Gadd no. 16 likewise treats it as an Indus-style seal. It is not cuneiform-inscribed, and nearby finds do not provide a readable owner/name/title bridge.

The second verified route is `3899.1 / U8685`, a circular Ur row with text `+000-000-004-090-350+`. Gadd no. 15 records `U.8685` as a circular object from Ur with a crowded, indistinct inscription. It gives object identity, not phonetic value.

## Candidate Mappings Not Accepted

`3897.1` is compatible with Gadd no. 2 / BM `122187` only by site, circular shape, bull/gaur icon, and five-sign length. That is not enough. No local accession field ties the row to BM `122187`, and BM/Gadd do not supply cuneiform on that object.

`5231.1` is a weak fragment candidate for Gadd no. 4 / BM `122188`, but the current local row has no accession or museum number. This remains a route to check in Mitchell 1986, not evidence.

`5225.1` remains unmapped.

## Micro-Bilingual Gate

The modeled Gadd objects split the wrong way:

- BM `120573 / U.7683` has a readable-writing route, but it is cuneiform-only in the current source surface and lacks a recorded Indus sign sequence.
- The mapped or candidate Indus-inscribed Ur objects lack readable cuneiform names, titles, or Meluhha formulas.

So the gate returns zero micro-bilinguals. No sign value, phonetic value, language identification, or translation is accepted.

## Skeptic Attacks

- Exact row-to-accession mapping exists for only `3898.1/U17649` and `3899.1/U8685`.
- The strongest mapped row, `3898.1/U17649`, is source-validated as Indus-style only, not cuneiform-bilingual.
- The cuneiform route BM `120573/U.7683` has no recorded Indus sequence.
- The remaining Ur rows rely on shape/site/length similarity or fragment plausibility.
- Site overlap with Ur Meluhha texts remains inadmissible because the previous forger already killed site overlap as evidence.

## Decision

Retracted as an external phonetic anchor. Retained as source-route infrastructure.

Next acquisition targets:

- Mitchell 1986 figures 106-117 for all Ur Indus/Gulf seals.
- Kjærum 1983 cat. `279` and `319` for the Failaka row-level mapping problem.
- Better images or catalogue records for local rows `3897.1`, `5225.1`, and `5231.1`.
