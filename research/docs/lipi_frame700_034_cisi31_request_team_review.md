# Lipi FRAME700 034 CISI 3.1 Request Team Review

Date: 2026-05-25

## Purpose

This stores the non-code review of the 48-row CISI 3.1/end-matter request packet.

## Source-Research Requirements

For every requested object, ask for:

- CISI object ID, excavation number, accession/museum/owner ID, and photograph source.
- Figure/page/plate IDs for every source image.
- All side and panel labels exactly as printed: `A/B/C`, numbered labels, `bis/ter/quater`, and any enlargements.
- Side-order basis: physical order, photographic order, editorial order, or unknown.
- Direction basis: object inscription direction, seal impression direction, catalog-normalized direction, or unknown.
- Material, shape/cross-section, dimensions, condition, and preservation.
- Findspot, excavation unit, period/phase, stratum, and depth where available.
- Copy, mold, duplicate, and family-relation notes.
- Notes explaining omitted sides, blank/iconographic sides, separate inscriptions on one side, later photographs, or panel enlargements.

Object-specific pressure:

| Target | Required check |
| --- | --- |
| `H-893` | Resolve base `H-893 A/B` versus `H-893 (1) A/B`; classify `(1)` as separate object, copy/impression, catalog sub-entry, alternate photograph group, enlargement, or other convention. |
| `H-925` family | Request `H-925` plus `H-326` and `H-924`; map base, `(1)`, `(2)`, `A/B`, `A bis`, `B bis`, and `A ter` before using it as a shared `033` control. |
| `H-983` | Classify source `C` and B/C variants as inscriptional, iconographic, blank/edge, damaged, or excluded by catalog policy. |
| `H-353` family | Reconcile source `A/B/C` and the duplicate IA leaves, then check whether `C`-side inclusion/exclusion is consistent across the repeated `+400-740-176+ / +700-033+` family. |
| `H-2211` | Get source-grade side labels, figure-to-object mapping, side order, and direction basis before using it as a `032` control. |

## Linguistic Standard

The current path is not yet linguistic evidence. Before `032/033/034` can become evidence for contrast, it needs:

1. Stable CISI side identity for each object.
2. Resolved source blockers for numbered groups and `C` sides.
3. Explicit panel-to-local-row mapping with direction uncertainty carried.
4. Source-visible diagnostic separation of `032`, `033`, and `034`.
5. Copy-family and neighbor-family pressure controlled rather than counted as support.
6. CISI 3.1/end-matter or equivalent object-note acquisition for the live blockers.

Quarantine:

- semantic, phonetic, lexical, administrative, or translation values for `032/033/034`;
- claims that `032/033/034` form an ordered scale;
- long-side context claims before source-stable family control;
- public web, secondary parallels, and prior interpretive claims as evidence;
- local two-row metadata for unresolved `C`-side or numbered-panel objects;
- repeated photos/impressions as independent attestations.

The strongest admissible post-source claim would only be that `032/033/034` occupy a source-confirmed contrastive slot in a stable FRAME700 side environment. That would still not be a translation.

## Adversarial Failure Modes

The request packet can still fail if:

- copy-family notes do not say whether objects are copies, molds, shared exemplars, workshop parallels, or only catalog neighbors;
- `(1)/(2)` labels remain underdefined;
- side letters are editorial or photographic rather than physical;
- same-side photo labels are fixed but side-part/enlargement conventions remain mixed;
- local two-row metadata suppresses source-visible `C` sides;
- end-matter context fields correlate with publication/source route rather than inscriptional role;
- shared controls such as `H-925` contaminate multiple triads;
- direction and allography remain unresolved after image access;
- diagnostic strokes are too damaged or low-resolution to separate `032/033/034`;
- HARP accession, figure number, CISI H-number, and local row ID do not align cleanly;
- photograph source or museum-owner data is mistaken for sign validation.

Hard requirement:

```text
CISI 3.1/end matter is required to resolve object identity, subentry labels, side labels, photograph sources, and family pressure. It will not by itself validate a FRAME700 subtype contrast unless it also allows source-visible sign separation, row-to-side mapping, direction control, and copy-family independence.
```

## Claim Status

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted side functions: 0
accepted source mappings from this review: 0
```
