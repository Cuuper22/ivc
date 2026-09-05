# Mahadevan 1977 concordance: frozen public snapshot, 2026-09-05

This directory contains the public Indus Research Centre / RMRL concordance snapshot used for the [paired-face constraint study](../../docs/mahadevan_crossface_constraints_20260905.md). It adds an independent transcription system, not an independent archaeological sample. It does not replace the canonical accepted-claim ledger.

## Reproduce

From the repository root, Python 3.10+; no third-party packages:

```sh
python research/tools/mahadevan_constraint_audit.py \
  --input research/data/mahadevan_20260905/concordance_documents.json.gz \
  --output /tmp/ivc-mahadevan-audit
```

The raw JSON SHA-256 after decompression is `6a0c597986783c5da8fbcb0afc3268a2c6a9f042a9b81746ebc4f89158efbd01`. The frozen input has 3,916 surface/line records: 3,573 nonempty lines and 343 no-text surfaces, across 2,906 catalogued objects. The six published-census checks must all pass before analysis continues.

## Files

- `concordance_documents.json.gz`: exact combined public records, losslessly compressed; original Firestore typed fields retained.
- `concordance_rows.csv`: decoded metadata, all fourteen sign slots, strict-inclusion flag, and explicit overlapping exclusion reasons.
- `summary.json`: corpus census and paired-face results.
- `paired_objects.json`: every eligible object, both faces, source metadata, and both stored/display sign order.
- `front_families.json`: complete reverse-count distributions grouped by unchanged front text.
- `four_by_three_grid.json`: the four front families each attested with two-, three-, and four-stroke reverses.
- `scalar_counterexamples.json`: minimal pairs and the assumptions required for the scalar-equality contradiction.
- `conditional_radix_algebra.json`: exhaustive arithmetic under the stated prior equations, not accepted numerical readings.
- `acquisition_manifest.json`: public URLs, original page hashes, and failures; the linked manual PDFs returned 404.
- `source_witnesses/`: limited original-plate and glyph witnesses, with a provenance manifest. No whole book or font package is redistributed here.
- `files.sha256.json`: generated analysis-file hashes; `snapshot.sha256.json` also covers supporting source and documentation files.

## Conventions that must not be flattened away

A stored `0` marks a lost or illegible passage, not a number. `*NNN` marks a doubtful reading. Blank trailing slots are padding. A doubtful sign contributes to the published full-corpus census but is excluded from the strict analysis. No possible allographs are merged.

Sign IDs use Mahadevan's 1–417 namespace. A number such as text 4554 is a Mahadevan text/object identifier, not CISI H-4554 or Wells sign 4554. Stored slot order is preserved. Reversing it for display is not a determination of phonetic reading direction.

Strict lines must be nonempty, have direction code 1/2/3, contain only undoubted IDs 1–417, have no internal blank slots, and agree with both recorded position and sign counts. Paired objects must have exactly two single-line surfaces, sideline codes 10 and 20, both strict, and object-class code 3. Exactly one face must be cup sign 328 plus one selected long-stroke group.

The counts one through five refer to the drawn strokes of signs 86, 87, 89, 95, and 96. They do not assert a language, a sound, an absolute measurement unit, or an accepted sign meaning. "Strict" refers to catalogue flags, not newly certified undamaged photographs.

## Attribution

Iravatham Mahadevan, *The Indus Script: Texts, Concordance and Tables* (Archaeological Survey of India, 1977); public concordance maintained through the Indus Research Centre / RMRL, https://indusscript.in/. Original-plate witness: M. S. Vats, *Excavations at Harappa*, volume II (1940), plate XCVII. Full citations and original repository source paths are in the research report and provenance manifests.

The project's code is separate from the third-party source materials. No new blanket license or scholarly priority claim is asserted over those materials. Reproducible catalogue-level constraints are not automatically promoted to accepted readings.
