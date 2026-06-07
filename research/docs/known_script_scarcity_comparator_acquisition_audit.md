# Known-Script Scarcity Comparator Acquisition Audit

Date: 2026-05-24

## Question

Which known-script comparator should be acquired first to estimate what an IVC translation system can honestly recover under Indus-like scarcity?

The target is not to compare current IVC work against full Ancient Egyptian translation. That would be nonsense dressed in a lab coat. The target is to blindfold known deciphered systems until they resemble the IVC evidence condition, then measure what survives.

## Sources Checked

| Comparator | Public source | Current availability | First-use decision |
| --- | --- | --- | --- |
| Egyptian/Coptic continuity | Coptic SCRIPTORIUM corpora and data site | Public corpora in CoNLL-U, relANNIS, PAULA XML, TEI XML, and TreeTagger SGML; current data site provides citable URNs and current versions; GitHub has previous/release versions. Annotation quality is marked as automatic, checked, or gold. | Use as the continuity upper bound, not as the first IVC-like comparator. Coptic preserves a kind of linguistic continuity IVC lacks. |
| Linear B Series D | Zenodo record `10.5281/zenodo.7404653` | Open Zenodo dataset, version 1.0, CC-BY 4.0, one `Samples.txt` file. The record reports 2,565 sequences without missing symbols: 513 real Series D tablet sequences, 725 augmented sequences, and 1,327 duplicates. | Run first. It is small, open, deciphered, short-sequence, administrative, and close to the kind of structural task IVC can currently support. Use only the first 513 real sequences for the clean blindfold unless explicitly testing augmentation/duplicate effects. |
| Sumerian administrative tablets | SumTablets GitHub, Hugging Face dataset, and arXiv paper | GitHub reports version 1, 91,606 tablets, 6,970,407 glyphs, CSV fields `id`, `glyphs`, `transliteration`, `glyph_names`, `period`, `genre`, and CC-BY 4.0. The arXiv abstract reports the same size and describes glyph/transliteration pairing plus retained structural tokens. | Acquire after Linear B. It is the large administrative comparator, but it must be pinned by Hugging Face revision and stripped of transliteration labels for IVC-like tests. |

## First Comparator Decision

Start with Linear B Series D.

Reason:

1. It is small enough to audit by hand and with simple scripts.
2. It has a clean source split: 513 real Series D sequences, then augmentation, then duplicates.
3. It is a known deciphered logo-syllabic administrative system, which is a better first comparator for short IVC marks than prose-heavy corpora.
4. Its own dataset task is masked symbol prediction, which aligns with the current IVC A2 structural layer.
5. It can produce an immediate ceiling: under short-sequence, no-translation conditions, how much structural recovery is possible before semantic or linguistic readings become cheating?

## Blindfold Protocol

For the first pass:

```text
source: Zenodo Linear B Series D
rows allowed: first 513 real Series D sequences only
rows excluded by default: 725 augmented rows; 1327 duplicate rows
labels hidden: Mycenaean Greek readings, lexical values, external translations
visible fields: sequence tokens, sequence length, row identity, optional document/series metadata if extractable
tasks allowed: length distribution, duplicate rate, positional entropy, masked sign prediction, edge-position classes, formula/slot variation
tasks not allowed: translation, lexical recovery, phonetic reading, known-language lookup
```

The duplicate and augmented rows can be added later as explicit stress conditions, never silently mixed into the clean comparator.

## Comparator Role Map

| Research layer | Coptic | Linear B | SumTablets |
| --- | --- | --- | --- |
| A0 corpus validity | Strong, with release/version and URN handling | Strong, with Zenodo DOI and file hash | Strong after Hugging Face revision pin |
| A1 graphemic accuracy | Strong but alphabetic/linguistic continuity is too generous for IVC | Good logo-syllabic sign sequence comparator | Strong glyph/transliteration pairing after label hiding |
| A2 structural accuracy | Useful upper bound | Best first run | Strong large-scale administrative run |
| A3 semantic accuracy | Too generous if lexicon is visible | Limited but useful for ideogram/numerical behavior if metadata exists | Useful after hiding transliteration and preserving period/genre |
| A4 linguistic accuracy | Continuity upper bound | Known language must be hidden | Transliteration must be hidden |
| A5 translation accuracy | Demonstrates why Egyptian-style success depends on infrastructure | Should not produce prose under blindfold | Should not produce prose under blindfold |

## Required Next Artifact

The next concrete experiment should be:

```text
E5.3a Linear B Series D Scarcity Baseline
```

Minimum outputs:

1. Source manifest with Zenodo DOI, version, file name, file size, license, and access date.
2. Parsed sequence inventory separating real, augmented, and duplicate ranges.
3. Indus-like downsample policy matched to current IVC length distribution.
4. A structural-only scorecard: length distribution, duplicate rate, hapax/token stats, positional entropy, masked sign prediction, and edge/frame controls.
5. A ceiling statement: what the method can recover from a known script when translation labels are hidden.

Status:

- First pass completed in [Linear B Series D scarcity baseline](linear_b_series_d_scarcity_baseline.md).
- The Zenodo `Samples.txt` source is MD5 verified.
- The clean 513-row real Series D block reaches hidden-reading `sign_tokens` bidirectional top-1 `0.470200`; the current IVC p95 length cap condition reaches `0.435897`.
- The source-provided gapped rows have also been evaluated. All 513 gapped rows contain exactly one aligned synthetic gap; under sequence-leave-one-out, bidirectional top-1 is `0.294347` all-lengths and `0.294314` under the current IVC p95 length cap.
- The next pass should improve tokenization with citable Linear B sign IDs and replicate the same blindfold on SumTablets.

## Interpretation Boundary

This audit does not validate any IVC sign, side relation, semantic field, language identity, or translation.

Its only job is to choose and constrain the first known-script scarcity comparator so the Egyptian-grade target becomes measurable instead of rhetorical.
