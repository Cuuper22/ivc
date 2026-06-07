# Meluhha Cuneiform Inventory

Date: 2026-05-29

This is Vector 1 infrastructure, not an external-anchor claim.

The inventory builder fetches primary digital CDLI and BDTNS source pages, extracts Meluhha-bearing cuneiform lines plus immediate context, records source metadata when exposed by the endpoint, and writes a hash log for every fetched source.

## Outputs

- `data/meluhha/tools/expand_meluhha_attestations.mjs`
- `data/meluhha/cuneiform_attestations_expanded.csv`
- `data/meluhha/cuneiform_fetch_log.csv`
- `data/meluhha/meluhha_token_inventory.json`

## Current Counts

| Item | Count |
| --- | ---: |
| requested source pages | 10 |
| attempted fetches | 18 |
| failed fetches | 0 |
| expanded cuneiform attestation rows | 16 |
| CDLI rows | 13 |
| BDTNS rows | 3 |
| accepted external anchors | 0 |

## Source Coverage

| Source | Rows |
| --- | ---: |
| BDTNS 000128 / BM 014594 | 2 |
| BDTNS 011069 / IM U. 03884 | 1 |
| P212982 / CT 50, 076 | 2 |
| P232277 / RIME 3/1.01.07, St D witness | 1 |
| P431881 / RIME 3/1.01.07, Cyl A composite | 3 |
| P431882 / RIME 3/1.01.07, Cyl B composite | 1 |
| P432309 / RIME 3/2.01.05.04 composite | 1 |
| P469516 / CDLI Literary 000334 (Enki and World Order) | 3 |
| P469679 / CDLI Literary 000375 (Curse of Agade) | 1 |
| P516138 / CUSAS 40, 1354 | 1 |

## What This Enables

The table gives Vector 1 a real cuneiform-side join surface: source ID, line reference, exact transliteration, exposed translation when present, metadata provenance, artifact type, period/date fields, co-route controls, and source hashes.

The important shift is that Meluhha no longer lives in a prose note or hand-picked examples. It is now a reproducible table that can be joined against external Indus-style objects by date, place, object context, and control toponyms before any phonetic pairing is attempted.

## Claim Status

No source row is treated as an Indus reading, translation, phonetic value, sign meaning, language identification, structural finding, or external anchor.

Promotion rule: any proposed Meluhha-Indus pairing must first define matched controls, run through the forger with a measured false-positive rate, and survive skeptic attacks. Until then this is inventory only.
