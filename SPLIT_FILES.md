# Split Files

GitHub rejects normal Git blobs larger than 100 MB, and the account LFS budget is currently exhausted. To keep the export pushable without dropping evidence bytes, one nested Git-history pack file was split into chunks below the GitHub hard limit.

Run this from the repository root to reconstruct it:

```powershell
.\tools\reconstruct_split_files.ps1
```

Split file:

| Original path | Bytes | SHA-256 |
| --- | ---: | --- |
| `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/_git_history/objects/pack/pack-f09fc4a9f75467afad858ed3a2ffed85bce03448.pack` | 276419355 | `bb754d1e5b346de79c43c061ce1a2809318aea30858767fa175ca75b6c091c06` |

Stored chunks:

- `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/_git_history/objects/pack/pack-f09fc4a9f75467afad858ed3a2ffed85bce03448.pack.split/part-001`
- `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/_git_history/objects/pack/pack-f09fc4a9f75467afad858ed3a2ffed85bce03448.pack.split/part-002`
- `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/_git_history/objects/pack/pack-f09fc4a9f75467afad858ed3a2ffed85bce03448.pack.split/part-003`
