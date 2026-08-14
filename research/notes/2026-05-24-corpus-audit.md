# Corpus Audit Notes

Date: 2026-05-24

## Why This Audit Exists

The corpus layer is the main failure point for any IVC translation attempt. Here is the trap: if a dataset imports somebody's claimed Sanskrit, Dravidian, or other decipherment as labels, a model can learn the claim and then appear to "confirm" it. The model is just echoing its own training labels back. That is circular, so every source gets audited before use.

## Open Source: `mayig/indus-valley-script-corpus`

Checked through GitHub tree API on 2026-05-24.

Observed:

- Total paths: 622.
- Corpus JSON files: 179.
- Feature files: 397.
- The repository README says it is a WIP digitization of CISI.
- The README says each corpus JSON file represents an artifact, with sides and graphemes.
- The README says graphemes are recorded from left to right on the artifact side while understanding that the script is read right-to-left.

Assessment:

- Useful for a first parser and feature audit.
- Not complete enough to serve as the main corpus.
- Must be pinned to a commit hash before use.

## Quarantined Source: Yajnadevam `lipi` CSV

Checked from:

```text
https://raw.githubusercontent.com/yajnadevam/lipi/refs/heads/main/src/assets/data/inscriptions.csv
```

Observed:

- Rows: 5,679.
- Columns: 38.
- Trusted-for-audit columns: 35 metadata/sign fields.
- Quarantined columns: `sanskrit`, `translation`, `notes`.

Completeness distribution:

```text
Y: 3673
N: 1338
?: 668
```

Direction distribution, top values:

```text
R/L: 4265
-: 776
NR: 386
L/R: 215
T/B: 16
BUS: 10
SYM: 8
```

Assessment:

- Useful as a broad metadata/sign probe only.
- The claimed decipherment columns must be removed before analysis.
- Any source field must be cross-checked against M77, CISI, ICIT, or publication images before entering the core corpus.

## Synthetic Source: `hellosindh/indus-script-synthetic`

Checked through the Hugging Face page on 2026-05-24. The API request failed due to a transport reset, but the web page rendered.

Observed from the dataset page:

- It describes 5,000 synthetic Indus Script sequences.
- It says the generation pipeline trained on 3,310 real archaeological inscriptions.
- It says exact seal matches were separated from novel generated sequences.

Assessment:

- This is not evidence for decipherment.
- It may be useful for stress tests that ask whether a model becomes overconfident when trained on generated sequences.

## Comparator Sources

These are corpora of other ancient scripts. We use them as yardsticks: they show what a real, deciphered writing system looks like under similar conditions.

### Coptic Scriptorium

The Coptic Scriptorium GitHub repository provides corpora in formats including CoNLL-U, relANNIS, PAULA XML, TEI XML, and TreeTagger SGML. It also reports annotation quality levels such as automatic, checked, and gold.

Use:

- Egyptian-language continuity benchmark.
- Scarcity simulation comparator.

### Linear B Series D Dataset

The Zenodo record for Mycenaean Linear B series D provides 2,565 sequences without missing symbols, derived from the Corpus of Mycenaean Inscriptions from Knossos, with a CC BY 4.0 license.

Use:

- Known deciphered logo-syllabic comparator under artificial scarcity.

### SumTablets

The SumTablets repository reports 91,606 tablets and 6,970,407 glyphs for Sumerian transliteration modeling.

Use:

- Large ancient administrative corpus comparator.

## Immediate Corpus Decision

The first local corpus should not be a single imported dataset. No single source is trustworthy enough. It should be a layered corpus:

1. `open_mayig_probe`: open WIP JSON, pinned by commit.
2. `lipi_metadata_filtered`: filtered metadata/sign table with decipherment columns removed.
3. `m77_reference`: acquired or manually exported M77/IDF80 reference.
4. `icit_reference`: access-gated reference if permission is granted.
5. `primary_image_check`: artifact image/publication validation for any claim-bearing subset.
