# Meluhha-Indus Join Surface

Date: 2026-05-29

This note records the table that lets the cuneiform side and the Indus side of the project be compared at all. It exists so that any future external-anchor test has an explicit, auditable set of candidate pairings instead of ad-hoc examples.

Terms first. Meluhha is a place named in Mesopotamian cuneiform texts, widely identified with the Indus region. Vector 1 is this project's external-anchor line of work: constraining Indus signs using evidence from outside the Indus corpus. A "join surface" is simply the table produced by matching rows on one side against rows on the other. A "bilingual" would be the same text written in both a known script and Indus signs — the thing decipherment normally needs and this project does not have.

This is a controlled join surface for Vector 1. It is not a bilingual claim.

The join uses the expanded cuneiform Meluhha inventory and the local external Indus-style object table. A row is emitted only when an external object site exactly matches an explicit cuneiform provenance alias. For example, `Girsu (mod. Tello)` can join against external rows listed as Girsu or Tello; plain `Girsu` joins only Girsu.

## Outputs

- `data/meluhha/tools/build_meluhha_join_surface.mjs`
- `data/meluhha/tools/meluhha_join_surface_nulls.mjs`
- `data/meluhha/meluhha_indus_join_surface.csv`
- `data/meluhha/meluhha_indus_join_surface_summary.json`
- `data/meluhha/meluhha_join_surface_null_summary.json`
- `data/meluhha/meluhha_join_surface_null_iterations.csv`

## Current Counts

| Item | Count |
| --- | ---: |
| cuneiform attestation rows | 16 |
| external Indus-object rows | 41 |
| direct site-overlap join rows | 25 |
| accepted external anchors | 0 |

## Join Rows By External Site

| External site | Rows |
| --- | ---: |
| Ur | 10 |
| Girsu | 7 |
| Tello | 5 |
| Nippur | 3 |

## Forger Result

The forger is this project's standard adversary test: build fake versions of the thing being claimed and check whether they score as well as the real one. If they do, the claim is not evidence.

Site overlap alone is rejected as evidence.

Observed join-surface metrics:

| Metric | Observed |
| --- | ---: |
| join rows | 25 |
| administrative/name-like join rows | 7 |
| distinct join sites | 4 |

Forger controls. A "null model" is a scrambled version of the data that keeps some structure but destroys the relationship being claimed; the observed result has to beat it:

| Null model | Iterations | Mean join rows | Null >= observed |
| --- | ---: | ---: | ---: |
| random site aliases from all external sites | 10,000 | 28.351000 | 0.815100 |
| random site aliases from Mesopotamian external sites only | 10,000 | 32.847900 | 0.933800 |
| provenance-preserving non-Meluhha control | 1 | not applicable | 1.000000 |

Decision: the site-overlap table is infrastructure only. A non-Meluhha corpus with the same provenance distribution would reproduce the overlap count, and randomized site aliases usually do as well or better.

## Why This Matters

The old ceiling says there is no bilingual. This join surface attacks the assumption behind that ceiling without pretending the ceiling is already broken. The cuneiform side now has source-hashed Meluhha attestations; the Indus side has external object rows; this table gives the exact lanes — separate lines of inquiry, kept apart so one cannot contaminate another — where a future bilingual-like constraint could be tested.

The immediate next gate — the checkpoint a claim must clear before it can advance — is not "read the signs." It is build matched controls:

- same external site with non-Meluhha cuneiform route/toponym controls,
- same cuneiform source class with non-overlapping external sites,
- same external object type/iconography with shuffled site labels,
- same sign sequence family with non-Meluhha cuneiform controls.

Only after those controls exist can a row become a candidate external anchor. Current status: no external anchor earned.
