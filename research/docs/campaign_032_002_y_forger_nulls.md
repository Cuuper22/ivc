# `032-002-Y` Forger Nulls

Date: 2026-05-29

## Question

This note records an adversarial test. The forger is our hostile tool: it builds fake corpora that keep the real corpus's surface statistics, then runs our own method on them. If the method finds the same pattern in forged data, the pattern is worthless. Signs in this corpus are numeric IDs; `Y` names whichever sign follows `002`. A "closure" sign ends a row, a "branch" sign opens further material, and a "register" is the object class a row sits on — site, seal type, icon, shape. Each forger model is a null model: a randomized copy of the data used as a baseline.

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

FPR below is the false-positive rate: the share of forged runs that matched or beat the real result. Lower is better for the real pattern.

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

This forger pass strengthens the structural candidate but does not accept it. The live skeptic objection is overfitting: the fixed Y-class bins were chosen from observed terminal behavior. The next admissibility gate — the checkpoint this work must clear before any stronger claim — is a source-boxed, family-blocked, right-edge-matched holdout. A holdout is a test run once on evidence set aside in advance, so it cannot be tuned. It tests whether the Y class still predicts closure when repeated formula families and edge position are denied easy wins.

Accepted translations, phonetic values, sign meanings, language identification, and structural findings remain zero in `data/claim_ledger/claims.json`.
