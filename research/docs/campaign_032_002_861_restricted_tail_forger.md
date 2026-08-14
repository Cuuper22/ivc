# 032-002-861 Restricted-Tail Forger

Date: 2026-05-29

## Question

This note records one adversarial test on a tiny pattern in the Indus sign corpus. Numbers like `002` and `861` are sign IDs, and a "tail" is the run of signs that ends an inscription row.

The `861` suffix campaign found two repeated post-`861` tails:

```text
002-861-603      x3
002-861-533-717  x2
```

`603` occurs elsewhere in the corpus. The narrower live question is whether `533-717` is a real fixed-prefix terminal formula after `002-861` — a tail that genuinely belongs to this exact prefix — or just another tiny post-hoc tail cell, a coincidence we only noticed after looking.

## Method

The forger is our adversarial scanner. It hunts for every candidate pattern of the target shape, then measures how often shuffled data can fake the same thing. Here it scans strict local rows in two scopes:

| Scope | Rows |
| --- | ---: |
| strict raw rows | 4,135 |
| exact `text/site/type/symbol` dedup rows | 3,074 |

For each scope it scans all units of length 1, 2, and 3. A candidate must have support at least 2 — it must occur at least twice — and every occurrence must be a terminal tail after the fixed prefix:

```text
002 861
```

The null models are shuffled copies of the data. Each shuffle keeps some structure and destroys the rest; if a shuffle often reproduces the observed pattern, the pattern is cheap.

| Null | Iterations | Meaning |
| --- | ---: | --- |
| `context_shuffle_global_any_n_1_3` | 10,000 | Preserve unit repetition counts, shuffle fixed-prefix terminal context labels globally. |
| `context_shuffle_site_type_symbol_any_n_1_3` | 10,000 | Same, but shuffle only inside `site/type/symbol` blocks. |
| `token_shuffle_global_preserve_lengths_any_n_1_3` | 500 | Preserve row lengths and global sign counts, shuffle signs globally. |
| `token_shuffle_within_row_any_n_1_3` | 500 | Preserve each row's sign inventory, shuffle order within rows. |

The forger also runs a broad hostile check: if we let the method search any prefix, repeated terminal bigram cells are common. That attack is logged to keep the accepted wording fixed to the prior `002-861` branch question.

## Result

Observed candidates:

| Scope | Candidate | Total occurrences | Fixed-prefix terminal occurrences |
| --- | --- | ---: | ---: |
| strict raw rows | `533-717` | 2 | 2 |
| exact dedup rows | `533-717` | 2 | 2 |

The two witnesses — the actual inscription rows where the pattern occurs — are:

```text
M-376 +740-100-176-002-861-533-717+
M-391 +405-845-686-740-793-003-233-805-002-861-533-717+
```

False-positive rates for reproducing the observed max support — how often each shuffled null matched or beat the real result:

| Scope | Null | FPR |
| --- | --- | ---: |
| strict raw rows | context shuffle global | 0.0002 |
| strict raw rows | context shuffle site/type/symbol | 0.0010 |
| strict raw rows | token shuffle global | 0 |
| strict raw rows | token shuffle within row | 0.0060 |
| exact dedup rows | context shuffle global | 0.0004 |
| exact dedup rows | context shuffle site/type/symbol | 0.0006 |
| exact dedup rows | token shuffle global | 0 |
| exact dedup rows | token shuffle within row | 0 |

Worst recorded FPR: `0.006`.

## Source Layer

The source layer asks what the published photographs actually show, not what the transcribed sign lists say. Both target rows have source-visible same-line terminal-side material:

| Row | Source status |
| --- | --- |
| `M-376` | CISI India leaf `n129`, medium confidence, same-line candidate present. |
| `M-391` | CISI India leaf `n131`, medium-low confidence, same-line candidate present in a long row. |

Exact source-normalized `861/533/717` token boundaries are not accepted. The source packet — the bundle of image evidence attached to this claim — supports same-line terminal-side material only.

Source-family review rejects exact copy collapse, the worry that the two rows are really one object counted twice: the two rows differ in source leaf, printed page, full text, length, class, excavation identifiers, depth, boss, dimensions, and immediate pre-`002-861` context. But they remain one narrow Mohenjo-daro no-icon `SEAL:R` source/register-family cell for linguistic weighting.

Source-layout review blocks a stronger claim: `M-1273` also has same-line terminal-side post-`861` material for `603`, so same-line terminal placement is not unique to `533-717`.

## Skeptic Boundary

This section marks the honest edge of the claim. Broad post-hoc prefix searching is dangerous:

| Scope | Repeated terminal bigram cells if any prefix is allowed |
| --- | ---: |
| strict raw rows | 96 |
| exact dedup rows | 40 |

So the accepted result is not "the corpus has only one repeated terminal bigram formula." It is the narrower fixed-prefix result:

```text
given the prior 002-861 branch question, 533-717 is the only length-1-to-3 repeated terminal tail in the checked strict local layer.
```

## Ledger Decision

The ledger is the running record of what this workspace accepts and refuses. Accepted as one narrow structural finding:

```text
accepted_struct_002_861_533_717_restricted_tail_2026_05_29
```

Accepted count increment:

```text
structural_findings +1
```

Not accepted:

```text
sign value
sign meaning
phonetic value
language family
external anchor
translation
exact source-normalized 861/533/717 token boundaries
```

## Artifacts

- `data/open_prototype/tools/campaign_032_002_861_restricted_tail_forger.mjs`
- `data/open_prototype/reports/campaign_032_002_861_restricted_tail_forger_summary.json`
- `data/open_prototype/reports/campaign_032_002_861_restricted_tail_forger_candidates.csv`
- `data/open_prototype/reports/campaign_032_002_861_restricted_tail_forger_null_summary.csv`
- `data/open_prototype/reports/campaign_032_002_861_restricted_tail_forger_null_iterations.csv`
