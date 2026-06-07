# `002-Y` Post-Hoc Partition Forger

Date: 2026-05-29

## Question

The earlier `002-Y` terminality result used named bins: `817` as hard closure, `820/861` as leaky closure, and `390/368/031/220/900/300` as branch heads. That is useful descriptively, but the skeptic objection is fair: if the bins were named after looking at terminal behavior, fixed-bin nulls do not measure the false-positive rate of discovering such a split.

This run asks the stricter question: if every null corpus is allowed to discover its own best high-terminal versus low-terminal partition among Y signs, does the real broad `002-Y` layer still stand out?

## Method

Script: `data/open_prototype/tools/campaign_032_002_y_posthoc_partition_forger.mjs`

Input: `data/open_prototype/reports/campaign_032_002_post_y_all_002_rows.csv`

Deduplication matches the prior forger: keep `strict_complete_closed=true`, then deduplicate by `text_dedup_key + site + type + idx_002`.

For each scope, the script:

1. Builds per-Y terminal rates.
2. Searches all terminal-rate threshold pairs among eligible Y signs.
3. Requires minimum sign counts and row counts on both poles.
4. Scores the best partition by two-proportion z and closure-minus-branch terminal-rate gap.
5. Gives every null corpus the same search privilege.

Null models:

- `terminal_shuffle_global`
- `terminal_shuffle_site_type_symbol`
- `terminal_shuffle_site_type_symbol_prev1`
- `y_shuffle_global`
- `y_shuffle_site_type_symbol`
- `register_bernoulli_terminals`

Iterations: 10,000 per null model.

## Result

Broad all-`002` strict dedup scope:

- Rows: 499
- Eligible Y signs at `n >= 8`: 7
- Best post-hoc closure pole: `817` at 100/103 terminal, `820` at 66/71 terminal
- Best post-hoc branch pole: `390` at 0/14 terminal, `368` at 0/11, `031` at 0/9, `220` at 0/9
- Best z: 13.211692
- Best terminal-rate gap: 0.954023
- Worst false-positive rate across all nulls: 0 for z and 0 for gap

The narrow adjacent `032-002` scope does not survive this harsher test:

- Rows: 32
- Best z: 1.526241
- Best gap: 0.272727
- Worst false-positive rate: 0.5205 for z, 0.7552 for gap

## Boundary

This strengthens only the broad all-`002` metadata-layer structural candidate. It does not promote the narrower adjacent `032-002` claim, and it does not by itself accept sign meaning, phonetic value, language family, or translation.

It also narrows the wording. The strict post-hoc partition supports `817/820` versus `390/368/031/220`. The older fixed-bin description can still call `861` closure-heavy but leaky, but `861` is not part of the strict best two-pole partition because its 95/119 terminal rate sits below the high threshold that maximizes the post-hoc z score.

## Files

- `data/open_prototype/reports/campaign_032_002_y_posthoc_partition_forger_summary.json`
- `data/open_prototype/reports/campaign_032_002_y_posthoc_partition_forger_observed.csv`
- `data/open_prototype/reports/campaign_032_002_y_posthoc_partition_forger_iterations.csv`
