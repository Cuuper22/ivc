# IVC Translation Research

This is an organized GitHub export, created on 2026-06-06, of the local workspace:

`C:\Users\Acer\OneDrive\Documents\ivc`

The workspace is a research project that tries to decipher the Indus Valley Civilization script, and every claim in it must be backed by evidence. It is not an app repo, and it does not currently claim fluent translations of anything.

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

The single accepted result is the narrow fixed-branch `002-861 / 533-717` terminal-tail finding. It is structural only. It says something about where signs sit in a sequence, not what they mean: no sound, sign meaning, language family, external anchor, or translation is accepted.

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
