# IVC Translation Research

This is an organized GitHub export, created on 2026-06-06, of the local workspace:

`C:\Users\Acer\OneDrive\Documents\ivc`

The workspace is a research project that tries to decipher the Indus Valley Civilization script, and every claim in it must be backed by evidence. It is not an app repo, and it does not currently claim fluent translations of anything.

## Latest Research — 2026-09-06

[Reconstructed completion pass](research/campaigns/integrated_20260906/completion/README.md) now contains the rebuilt four-route execution, frozen joint systems, source adjudication, and full recovery provenance. No new reading is accepted.


[Integrated four-route campaign](research/campaigns/integrated_20260906/README.md) executes writing-operation, semantic, numerical and phonetic searches over the existing evidence. Its strongest new candidate composes a roof/87 operation with a surrounding-marks/211 operation and connects another fish family under an explicit held-family comparison. Numerical scope, contextual and linguistic alternatives remain unresolved; no reading is accepted. The campaign includes runnable searches, source-linked candidates, executed cross-route predictions and a precise continuation state.

## Paired-face Research — 2026-09-05

[Paired-face constraints on numerical readings](research/docs/mahadevan_crossface_constraints_20260905.md) adds a frozen public Mahadevan 1977 concordance: 2,906 catalogued objects, 3,573 nonempty inscription lines, and 417 signs. Six published-census checks match exactly. This is an independent transcription system, not an independent archaeological sample.

The strict paired-tablet set contains 85 objects. Four unchanged front inscriptions each occur with cup-plus-two, cup-plus-three, and cup-plus-four long-stroke reverses, covering 34 objects. The resulting conditional counterexamples constrain any interpretation that treats both faces as equivalent scalar amounts under fixed units. An original Vats plate was inspected; exact fine allograph identity remains catalogue-dependent. No lexical or phonetic reading is promoted.

The [frozen evidence packet](research/data/mahadevan_20260905/README.md) includes raw records, normalized rows, exclusion reasons, complete paired-object witnesses, explicit counterexample assumptions, source figures, and hashes. Reproduce the research with Python 3.10+ and no third-party packages:

```sh
python research/tools/mahadevan_constraint_audit.py \
  --input research/data/mahadevan_20260905/concordance_documents.json.gz \
  --output /tmp/ivc-mahadevan-audit
```

This new catalogue-level study is separate from the accepted-claim ledger below. Scholarly priority has not been established.

## Current Evidence State

The live replacement run — the current, canonical line of work — has exactly one accepted structural finding and no accepted readings:

| Claim class | Accepted count |
| --- | ---: |
| translations | 0 |
| phonetic values | 0 |
| sign meanings | 0 |
| language identification | 0 |
| external anchors | 0 |
| structural findings | 1 |

Following the [2026-07-12 replacement checkpoint](research/docs/replacement_run_checkpoint_20260712.md), the accepted observation is strictly descriptive: M-376 and M-391 are source-visible attestations of the same three-position terminal `861 | 533 | 717` string after `002`. The stronger source-independent fixed two-sign `533-717` unit claim was demoted. No sound, sign meaning, language family, external anchor, or translation is accepted.

## Directory Layout

| Path | Contents |
| --- | --- |
| `research/docs/` | Main research notes, claim ledgers, campaign reports, and decision records. |
| `research/data/` | Source datasets, generated reports, claim ledger JSON, scripts, and reproducible artifacts. |
| `research/notes/` | Initial working notes and literature/corpus updates. |
| `research/README.original.md` | Original local workspace README before this organized export. |
| `evidence/tmp/` | Temporary source artifacts, OCR/image/PDF working files, blind packets, route probes, and cached source checks. |
| `workspace/codex/` | Local Codex hooks, state, assets, and logs that were present in the workspace. |
| `MERGED_BRANCH_STATE.md` | How the replacement branch and quarantined successor branch were merged in this export. |

## Branch Merge Policy

The original local Git state had no commits and no real branch history. The meaningful branch split lived in the research files themselves:

- live replacement branch: canonical current evidence
- quarantined post-2026-05-31T01:04 successor branch: preserved for autopsy/history only

This export keeps both, but the replacement branch is canonical. Quarantined artifacts must not be cited as support unless a result is independently re-earned in replacement-named outputs.

## Large Files

This repo does not depend on Git LFS. Only one file exceeded GitHub's normal 100 MB blob limit. It was split into chunks with a SHA-256 manifest so nothing was lost; see `SPLIT_FILES.md`.

One more quirk: a nested temporary repository had its own history, and Git would have ignored its internal `.git` directory during upload. To preserve that history, the directory was renamed to `_git_history`.
