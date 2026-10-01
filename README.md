# IVC: looking for checkable structure in the Indus script

By Cúper (Yousef) Anas · [Website](https://cuuper22.github.io/ivc/) · [Cite this](CITATION.cff)

## What this is

The Indus script (c. 2600-1900 BCE, about 4,000 short inscriptions) is undeciphered. This repository is an independent, heavily LLM-assisted attempt, May to September 2026, to find structure in it that can be checked, one claim at a time. It does not decipher anything: no sign value, no meaning, no language, no translation. What it offers instead is a clean, reproducible corpus, a few small tested results, and a documented record of what failed, including how the LLM agents inflated the work (more notes, more gates and more claims than the evidence supported). That story is [Paper 1](research/publications/20260907/README.md). A cleanup on 2026-10-01 cut the notes from 427 files to 5 and re-tested the open questions.

## What holds up

| Result | Evidence | Status |
| --- | --- | --- |
| Frozen Mahadevan 1977 concordance: 2,906 objects, 3,573 inscription lines, 417 signs | Six published census figures reproduce exactly ([data](research/data/mahadevan_20260905/README.md)) | Solid. A transcription system, not an independent archaeological sample |
| Reading direction: the Lipi catalogue stores inscriptions in reverse of the conventional (Mahadevan) order | The jar sign is first in 937 Lipi rows and last in 4; in Mahadevan it is last in 739 and first in 0 ([note](research/docs/reading_direction_note.md)) | Solid. Every Lipi "terminal" result means the reading-initial end |
| On two-sided tablets, the front predicts the cup + stroke count | Strong within the Lipi catalogue, weaker in Mahadevan, no gain on held-out newer tablets. The variation was noted by Priyanka (2003) and Mukhopadhyay (2023); the association test is new ([report](research/extensions_20261001/front_count/REPORT.md)) | Looks like production batches, not a portable rule |
| 034 tablets are about 14% smaller in area than 032/033 of the same format | One vote per copied family, P 0.0005; about 10% with excavation area controlled ([report](research/extensions_20261001/size_034/REPORT.md)) | A size difference. Not a tier, unit or meaning |
| After sign 002, signs 861, 817 and 820 sit at the stored (reading-initial) end more often than their own baseline predicts | Holm P < 0.01 each; replicates in Mahadevan, where these are the text-opening pairs 267-99 and 391-99 ([report](research/extensions_20261001/context_002/REPORT.md)) | Real, but already known (Yadav et al. 2010). Only the baseline-adjusted test is new |
| Seals M-376 and M-391 both carry `861-533-717` after `002`, at the stored end | Two source-visible witnesses ([ledger](research/docs/claim_ledger.md)) | The one accepted item. Descriptive; two seals, not a rule |

## What didn't hold up

- **Roof/87 and surrounding-marks/211 as "writing operations".** Ranks last of 8 models in the campaign's own joint test; the supporting alternations are selection-sensitive and about 94 other swap types recur as often. [report](research/extensions_20261001/alternation_null/REPORT.md)
- **Sanskrit dictionary fits.** Not reproducible (the optimizer is missing); a re-implementation does no better than Markov text with the same local repetition. [report](research/extensions_20261001/phonetic_null/REPORT.md)
- **`533-717` as a fixed unit, and its 0.0002 false-positive rate.** The prefix was chosen after the fact; sign 533 occurs on only two seals. [ledger](research/docs/claim_ledger.md)
- **Every external anchor:** Brahmi descent, Meluhha names, the Gadd/Ur seal bridge. All rejected, zero anchors. [ledger](research/docs/claim_ledger.md)
- **Small-language-model transfer.** Non-writing pretraining gives the same gain. [index](research/docs/README.md)

Eight further ledger entries were test instruments that failed (blind-review packets with label leaks, packets never scored). They are recorded as instrument failures, not as results either way.

## Already known: cited, not claimed

Directionality of sign order (Yadav et al. 2010), hidden-sign prediction and conditional entropy (Rao et al. 2009), fish-sign diacritics (Parpola 1994), arithmetic reading of the stroke tablets (Fuls 2020), same-front/different-reverse tablets (Priyanka 2003; Mukhopadhyay 2023), and the comparison with non-linguistic controls (Sproat 2014). Full references are in [CITATION.cff](CITATION.cff); where each was re-derived is in [research/docs/README.md](research/docs/README.md).

## Reproduce

Python 3.11 and Node 22 (the database build needs Node 22.5 or later).

```sh
python -m pip install -r requirements.txt
make check audit verify db     # a few minutes, no network
make campaign                  # full four-route rerun; long; rewrites files under research/campaigns/
python research/tools/check_headline_numbers.py
```

Each extension study runs on its own: `python3 research/extensions_20261001/<study>/<script>.py`. CI ([reproduce.yml](.github/workflows/reproduce.yml)) runs the checks, the campaign and the headline-number comparison on every change under `research/`, `db/` or `docs/`.

## Layout

| Path | Contents |
| --- | --- |
| [research/docs](research/docs/README.md) | The 5 notes worth reading, an index, and `archive/` (422 working notes, kept as a record) |
| [research/extensions_20261001](research/extensions_20261001/README.md) | Five October 2026 tests: one script, JSON output and one-page report each |
| [research/data](research/data/) | Frozen Mahadevan concordance, the Lipi catalogue, claim ledger JSON (`claim_ledger/claims.json`) |
| [research/campaigns](research/campaigns/integrated_20260906/README.md) | The September four-route search and its completion pass |
| [research/tools](research/tools/) | Audit and check scripts |
| [research/publications](research/publications/20260907/README.md) | Index of the two paper drafts |
| [db](db/README.md) | SQLite database of the evidence, with its build script and audit report |
| [docs](docs/) | The project website source (GitHub Pages) |
| [slm](slm/README.md), [embeddings](embeddings/README.md) | Small-language-model and embedding experiments |
| `evidence/tmp` | Raw source material and working files |
| `workspace/codex` | Hooks and logs from the earlier agent setup |

One source file over GitHub's 100 MB limit is stored in chunks with a checksum manifest; see [SPLIT_FILES.md](SPLIT_FILES.md). [MERGED_BRANCH_STATE.md](MERGED_BRANCH_STATE.md) records how the two original branches were merged.
