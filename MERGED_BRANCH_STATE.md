# Merged Branch State

Date: 2026-06-06 America/Los_Angeles

## What Was Merged

The local workspace sat on `codex/indus-frontier-replacement-20260531`, but Git had no commits and no remote. So the apparent "branches" were not Git branches at all — they were two research states encoded in the files.

This export merges both research states into one organized repository:

1. **Replacement branch, canonical live state.**
   - Main checkpoint: `research/docs/replacement_run_checkpoint_20260531.md`
   - Current 002-390-X state: `research/docs/campaign_032_002_861_002390x_current_decision_state_20260531.md`
   - Claim ledger: `research/docs/claim_ledger.md` and `research/data/claim_ledger/claims.json`

2. **Quarantined successor branch, preserved but not evidence.**
   - Quarantine policy: `research/data/quarantine/README.md`
   - Bad-successor quarantine note: `research/docs/quarantine_bad_successor_20260531.md`
   - Quarantined files: `evidence/tmp/quarantine_bad_successor_20260531T0104/`

## Current Decision

The replacement branch is the live source of truth. The quarantined branch stays in the repo, but only to explain the history and preserve local files. It is autopsy-only: nothing in it counts as evidence unless the result is independently re-earned under replacement-run naming.

Accepted claim counts in the live state:

| Claim class | Accepted count |
| --- | ---: |
| translations | 0 |
| phonetic values | 0 |
| sign meanings | 0 |
| language identification | 0 |
| external anchors | 0 |
| structural findings | 1 |

## Organization Map

| Original local path | Export path |
| --- | --- |
| `README.md` | `research/README.original.md` |
| `docs/` | `research/docs/` |
| `data/` | `research/data/` |
| `notes/` | `research/notes/` |
| `tmp/` | `evidence/tmp/` |
| `.codex/` | `workspace/codex/` |
| `tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/.git/` | `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/_git_history/` |

No local project evidence files were intentionally left out of the export. The original root `.git/` directory was not copied, but nothing was lost by that: it had no commits, and it is repository control metadata, not project evidence.

## Practical Next Work

The strongest honest statement of the project state is: one narrow structural tail formula earned, no reading earned.

The next useful work is getting sources and validating source images, especially:

- source-bind H-1993 / H96-2769 / Figure 17.07
- source-bind Dholavira 8758 / ZA-12:2 / 4237.1
- source-bind M-1825 / BJ25710
- resolve 3335.1 provenance or find a strict replacement witness
- source-normalize enough rows to test whether the broader role/backbone candidates survive outside the metadata layer
