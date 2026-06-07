# Effective-Unicity SumTablets Comparator

Date: 2026-05-29

## Result

SumTablets is now integrated as a pinned known-script administrative comparator for Vector 2. This is calibration, not Indus evidence. It asks whether the same glyph-only masked-sign instrument can recover local structure in a known readable cuneiform administrative corpus when transliteration and sign-name fields are hidden.

## Provenance

Dataset:

- Hugging Face dataset: `colesimmons/SumTablets`
- Dataset SHA: `11638cd142afbed716df43c55d8810d47fb9b52c`
- License: `cc-by-4.0`
- Train split rows reported by Dataset Viewer: 82,452
- Total rows reported by Dataset Viewer: 91,606
- Fields retained locally: `id`, `period`, `genre`, `glyphs`
- Fields intentionally excluded from cache and scoring: `transliteration`, `glyph_names`

Generated files:

- `data/open_prototype/tools/effective_unicity_sumtablets_comparator.mjs`
- `data/open_prototype/known_scripts/sumtablets/sumtablets_source_manifest.json`
- `data/open_prototype/known_scripts/sumtablets/sumtablets_sample_rows.jsonl`
- `data/open_prototype/known_scripts/sumtablets/sumtablets_line_sequences.csv`
- `data/open_prototype/reports/effective_unicity_sumtablets_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_sumtablets_comparator.csv`
- `data/open_prototype/reports/effective_unicity_sumtablets_null_iterations.csv`
- `data/open_prototype/reports/effective_unicity_sumtablets_null_summary.csv`

## Extraction

The script sampled 2,000 train rows by deterministic page offsets from Dataset Viewer. It tokenized only visible cuneiform Unicode code points, kept line lengths 2 through 8 to match the Indus-like length cap, collapsed exact line sequences, then selected 1,798 unique line sequences by stable hash order.

Extraction counts:

| Quantity | Count |
| --- | ---: |
| fetched tablets | 2,000 |
| line records after length filter | 26,242 |
| exact unique line sequences | 17,119 |
| selected line sequences | 1,798 |
| selected glyph tokens | 8,716 |
| unique glyphs | 358 |

## Primary Comparison

| System / test | Rows | Tokens or gaps | Signs/tokens | Label bits | Top-1 | Top-5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Indus strict exact-collapsed masked signs | 1,798 | 8,212 | 571 | 4,410.970864 | 0.279591 | 0.534096 |
| Linear B, IVC-length cap, clean bidirectional masking | 299 | 1,755 | 91 | 465.505030 | 0.435897 | 0.698006 |
| Linear B, IVC-length cap, source-gapped sequence leave-out | 299 | 299 | 91 | 465.505030 | 0.294314 | 0.638796 |
| SumTablets, glyph-only IVC-length-capped admin lines | 1,798 | 8,716 | 358 | 2,526.289215 | 0.171753 | 0.373681 |

## Forger Controls

SumTablets observed top-1 is lower than Indus in this line-level glyph-only setup, but it still cleanly beats its own matched controls. Forty iterations were run for each control, scoring 1,500 masked positions per null iteration.

| Control | Null mean top-1 | Null p95 | Null max | Null >= observed |
| --- | ---: | ---: | ---: | ---: |
| global token shuffle | 0.028933 | 0.036033 | 0.039333 | 0 |
| row internal shuffle | 0.044600 | 0.052667 | 0.054000 | 0 |
| position slot shuffle | 0.047133 | 0.056800 | 0.062667 | 0 |
| edge frame shuffle | 0.047050 | 0.058000 | 0.058667 | 0 |
| period/genre position shuffle | 0.049517 | 0.057400 | 0.059333 | 0 |

## Interpretation

The useful point is not that Indus is cuneiform or that SumTablets is a model for Indus. The useful point is calibration: a known readable administrative writing system, reduced to Indus-like line lengths and stripped to glyphs only, does not automatically look like Linear B under this masked-sign scorer. Comparator choice changes the scale.

This narrows one skeptic objection: Vector 2 is no longer calibrated only against Linear B. It does not close the real-world nonlinguistic gap, because SumTablets is a writing system. It also does not earn any Indus value, sign meaning, language family, or translation.

## Ledger Boundary

Accepted claim counts remain zero. The Vector 2 candidate stays live but unaccepted: source-image normalization, source-family collapse, and real-world nonlinguistic comparators remain open.
