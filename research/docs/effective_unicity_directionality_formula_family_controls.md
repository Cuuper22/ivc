# Directionality Formula-Family Controls

Date: 2026-05-29

Status: hostile metadata-layer control. Accepted claim increment: 0.

This note records a deliberately hostile control run. It attacks the Vector 2 directionality candidate — the working result that Indus inscriptions score better in their stored order than reversed — at the place it looked softest: dependence on source, register, and formula family (groups of inscriptions that repeat the same formula). The test uses only fields already present in the Lipi working table, our main catalog-derived data table, so it does not solve source-image normalization. It asks whether the stored-order signal survives when the corpus is grouped by a stronger metadata proxy:

`source_convention_key = site|type|material|symbol|cult|direction`

The scoring rule is the same leave-out bigram instrument used in the directionality comparator: score each stored sequence against its reversed sequence after removing the tested row, family, or source-convention block from training. Nulls — shuffled versions of the data that destroy the order under test — are global-token shuffle, row-internal shuffle, position-slot shuffle, edge-frame shuffle, register-position shuffle, and register-edge/interior shuffle, 200 iterations per control.

## Result

Stored-win share is the fraction of rows where the stored order beats the reversed order. Max admissible null >= observed is the worst case across the valid null controls: the fraction of shuffled iterations that matched or beat the observed result, so small values mean the signal is hard to fake.

| Scope | Rows | Stored-win share | Max admissible null >= observed | Decision |
| --- | ---: | ---: | ---: | --- |
| Exact text, leave source convention out | 1,798 | 0.946607 | 0 | Survives |
| Top-10 edge removed, leave source convention out | 530 | 0.833962 | 0 | Survives |
| Top-10 edge removed plus one-edit-family collapse, leave source convention out | 365 | 0.832877 | 0.020000 | Survives |
| Exact text, source-convention collapsed | 502 | 0.930279 | 0.005000 | Survives |
| Top-10 edge removed, source-convention collapsed | 221 | 0.805430 | 0 | Survives with shrinkage |
| Harsh one-edit plus source-convention collapsed | 175 | 0.805714 | 0.005000 | Survives with shrinkage |
| Harsh R/L only, leave source convention out | 354 | 0.830508 | 0.015000 | Survives |
| Harsh L/R only, leave source convention out | 11 | 0.000000 | 1.000000 | Fails / too small |

The result survives the useful source-convention attacks in the dominant R/L layer. The harsh source-convention-collapsed scope has 175 rows, stored-win share 0.805714, mean stored-minus-reversed per transition 0.817965, median 0.761131, and max admissible null >= observed share 0.005000.

The L/R stratum — the rows whose recorded reading direction is left-to-right rather than the dominant right-to-left (`R/L`) — blocks any stronger claim. Exact L/R has 83 rows and a positive stored-win share, but it is null-compatible at max null >= observed share 0.520000. Harsh L/R has only 11 rows, stored-win share 0, negative mean difference, and max null >= observed share 1.000000. So the admissible wording is R/L-dominant metadata-layer stored-order asymmetry, not physical bidirectionality and not validated source direction.

## Degenerate Controls

After source-convention collapse, `register_position_shuffle` can become an identity-preserving control: every null iteration reproduces the observed score. The summary records this as `max_all_null_ge_observed_share = 1` and names the degenerate control, but excludes it from `max_admissible_null_ge_observed_share`. That exclusion is not a promotion trick; it prevents an identity control from pretending to be a hostile null. The all-null value remains in the output as a trap marker.

## Boundary

This narrows the formula-family objection but does not remove the source-normalization objection. The test still lives in the Lipi T3 metadata/sign layer. It does not validate physical source direction, source-side order, token identity, sign meaning, phonetic value, language family, or translation.

Main artifacts:

- `data/open_prototype/tools/effective_unicity_directionality_formula_family_controls.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_formula_family_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_formula_family_controls.csv`
- `data/open_prototype/reports/effective_unicity_directionality_formula_family_members.csv`
- `data/open_prototype/reports/effective_unicity_directionality_formula_family_null_summary.csv`
- `data/open_prototype/reports/effective_unicity_directionality_formula_family_null_iterations.csv`
