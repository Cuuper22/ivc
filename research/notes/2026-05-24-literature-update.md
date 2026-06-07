# Literature Update

Date: 2026-05-24

## Newly Relevant Current Item

### Nair 2026: Synthetic-Baseline Scorecard

Source:

```text
arXiv:2604.17828
How Non-Linguistic Is the Indus Sign System? A Synthetic-Baseline Scorecard
Submitted: 2026-04-20
```

Why it matters:

- It directly attacks the weak-baseline problem.
- It compares Indus data against synthetic heraldic and administrative systems.
- It uses metrics central to the Farmer-Sproat-Witzel critique: brevity, repeated formulae, hapax rate, and positional rigidity.
- It reports an intermediate result rather than a clean "language" or "not language" outcome.

Important caution:

- The abstract says all code and data are publicly available.
- The arXiv comments say code is available from the corresponding author upon request.
- Treat this as a reproducibility flag until code/data are actually obtained.

Project impact:

- Add a nonlinguistic baseline scorecard to the first sprint.
- Do not treat the preprint as a result to cite uncritically.
- Use it as pressure to make our null models strong enough.

## Current Corpus Evidence From Open Sources

### `mayig/indus-valley-script-corpus`

Checked:

```text
GitHub commit: ad2f1e218a34b8c33c57de0d6cb8d99272765bbb
Commit date: 2025-04-16
Commit message: m184
```

Observed:

- 179 corpus JSON files.
- 397 feature files.
- Sample `m001.json` has one side, `M-1A`, description `unicorn I seal`.
- Grapheme IDs in the sample use Parpola-style notation such as `P121`, `P202`, `P385`, `P073`, and `P108`.

Research impact:

- Good enough for parser/crosswalk design.
- Not enough for authoritative statistics.

### Yajnadevam `lipi` CSV

Prior audit stands:

- 5,679 rows.
- `sanskrit`, `translation`, and `notes` must be quarantined.

Research impact:

- Use as metadata/sign probe after filtering only.
- Never train on the claimed readings.

## Comparator Evidence

### Coptic Scriptorium

The repository supplies machine-readable Coptic corpora in multiple formats and labels annotation quality as automatic, checked, or gold.

Research impact:

- Useful for testing what language continuity buys you.

### Linear B Series D

Zenodo record provides 2,565 Linear B sequences without missing symbols, CC BY 4.0.

Research impact:

- Good first known-deciphered comparator for masked sign prediction.

### SumTablets

The repository reports 91,606 tablets and 6,970,407 glyphs.

Research impact:

- Strong administrative corpus comparator.

## Research Decision

The next methodological addition should not be another broad literature list. It should be a first-sprint evidence package:

- Evidence ledger.
- Comparator benchmark design.
- First sprint plan.

Those files now exist in `docs/`.
