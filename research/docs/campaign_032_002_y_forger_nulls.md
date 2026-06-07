# `032-002-Y` Forger Nulls

Date: 2026-05-29

## Question

Does the `002-Y` closure/branch signal survive synthetic corpora that preserve sign frequencies and register structure, or does the same method find a comparable pattern in forged data?

## Inputs

- `data/open_prototype/reports/campaign_032_002_post_y_all_002_rows.csv`
- `data/open_prototype/reports/campaign_032_002_post_y_branch_rows.csv`
- Y-class bins from `tmp/run_032_002_y_matched_terminality.py`

Rows are filtered to `strict_complete_closed=true` and deduplicated by `text_dedup_key`, `site`, `type`, and `idx_002`, matching the existing matched-terminality campaign.

## Forger Models

The tool `data/open_prototype/tools/campaign_032_002_y_forger_nulls.mjs` ran 2,000 iterations per model:

- `terminal_shuffle_global`: terminal labels shuffled globally.
- `terminal_shuffle_register`: terminal labels shuffled inside `site|type|symbol`.
- `y_shuffle_global`: Y signs shuffled globally.
- `y_shuffle_register`: Y signs shuffled inside `site|type|symbol`.
- `independent_register_admin`: Y signs and terminal outcomes sampled independently from register-conditioned distributions.

## Result

All-`002` strict dedup scope:

- Rows: 499.
- Observed y-class leave-one-out terminality accuracy: 0.885772.
- Observed Brier: 0.097554.
- Observed logloss: 0.331038.
- Observed closure-minus-branch terminality gap: 0.890785.
- Maximum recorded FPR across tested nulls and metrics: 0.

Adjacent `032-002` strict dedup scope:

- Rows: 32.
- Observed y-class leave-one-out terminality accuracy: 0.906250.
- Observed Brier: 0.106698.
- Observed logloss: 0.381811.
- Observed closure-minus-branch terminality gap: 0.850000.
- Maximum recorded FPR across tested nulls and metrics: 0.0265.

## Decision

This forger pass strengthens the structural candidate but does not accept it. The live skeptic objection is overfitting: the fixed Y-class bins were chosen from observed terminal behavior. The next admissibility gate is a source-boxed, family-blocked, right-edge-matched holdout that tests whether the Y class still predicts closure when repeated formula families and edge position are denied easy wins.

Accepted translations, phonetic values, sign meanings, language identification, and structural findings remain zero in `data/claim_ledger/claims.json`.
