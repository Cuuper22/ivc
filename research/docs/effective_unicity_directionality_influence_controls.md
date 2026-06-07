# Effective Unicity Directionality Influence Controls

Date: 2026-05-29

This note documents an independent concentration diagnostic for the current harsh directionality result. It is not an accepted finding and does not increment any claim count. It only asks whether the stored-order signal depends on a tiny number of rows or conservative site/type/symbol families.

## Scope

Source input:

- `data/open_prototype/reports/lipi_scope_rows.csv`

Harsh scope reconstruction:

1. Keep `readiness_bucket == lipi_numeric_clean_candidate` rows with at least two parsed numeric tokens.
2. Collapse exact duplicate token sequences.
3. Remove rows whose first or last token is among the top 10 edge tokens.
4. Collapse one-edit token families and keep one representative per family.

This reproduces the current live harsh scope: 365 rows, 1,725 tokens, 358 unique tokens.

## Baseline Scores

Scores use the same add-alpha leave-one-row-out bigram directionality test as the directionality comparator. Stored-win share is the fraction of held-out rows where stored order scores higher than reversed order.

| Scope | Rows | Stored wins | Reversed wins | Ties | Stored-win share | Mean stored minus reversed per transition |
|---|---:|---:|---:|---:|---:|---:|
| All harsh rows | 365 | 307 | 47 | 11 | 0.841096 | 1.052098 |
| Mohenjo-daro only | 212 | 173 | 22 | 17 | 0.816038 | 0.986013 |
| Harappa only | 112 | 83 | 16 | 13 | 0.741071 | 0.653432 |
| Mohenjo-daro and Harappa only | 324 | 274 | 35 | 15 | 0.845679 | 1.046123 |

## Row Influence

For each row, the script removes that row from the scope and recomputes aggregate stored-win share and mean stored-minus-reversed score. Positive delta means removing the row weakens the signal. Negative delta means removing the row strengthens it.

All-harsh concentration:

- Tested row units: 365.
- Largest supportive row delta: +0.005931 stored-win share.
- Largest adverse row delta: -0.010552 stored-win share.
- Top five absolute row deltas sum to 0.034276.

Largest supportive row removals in the all-harsh scope:

| CISI | Site | Type | Symbol | Text | Delta stored-win share |
|---|---|---|---|---|---:|
| ?-3 | Unknown | SEAL:S | None | `+002-368-590-900+` | 0.005931 |
| H-1706 | Harappa | SEAL:R | None | `+405-003-002-293-360+` | 0.005931 |
| M-396 | Mohenjo-daro | SEAL:R | None | `+204-630-233-832-904-794-630-235-060-550+` | 0.005931 |
| M-1688 | Mohenjo-daro | SEAL:S | Bull1:S | `+125-435-255-002-286-220-031-012-031-455-033-590+` | 0.005931 |
| M-729 | Mohenjo-daro | SEAL:S | Bull1:I | `+234-415+` | 0.005931 |

The strongest single row effect is adverse, not supportive: removing L-115 increases the stored-win share from 0.841096 to 0.851648.

## Family Influence

Family influence uses the conservative key `site|type|symbol`. This is intentionally coarse enough to catch register/provenance concentration, but it is not a proof that all rows inside a family are one physical or formulaic object class.

All-harsh concentration:

- Tested family units: 110.
- Largest supportive family delta: +0.028975 stored-win share.
- Largest adverse family delta: -0.009320 stored-win share.
- Top five absolute family deltas sum to 0.069075.

Largest supportive family removals in the all-harsh scope:

| Family key | Rows removed | Delta stored-win share | Delta mean score |
|---|---:|---:|---:|
| Mohenjo-daro\|SEAL:R\|None | 35 | 0.028975 | 0.090625 |
| Harappa\|SEAL:R\|None | 23 | 0.013611 | 0.051551 |
| Mohenjo-daro\|SEAL:S\|Bull1:W | 40 | 0.010327 | 0.063608 |
| Mohenjo-daro\|SEAL:S\|Bull1:I | 3 | 0.006842 | 0.006391 |
| Mohenjo-daro\|SEAL:S\|Bull1:S | 15 | 0.006810 | 0.014733 |

The largest adverse family is `Lothal|SEAL:R|None`, with 4 rows. Removing it increases stored-win share from 0.841096 to 0.850416.

## Skeptic Read

The all-harsh directionality signal does not appear to be controlled by one row or one `site|type|symbol` family under this diagnostic. The largest single-family removal changes stored-win share by 0.028975, less than three percentage points, and no single row has a supportive delta above 0.005931.

That said, the strongest family effects are exactly the kind of register/provenance clusters a skeptic should care about: Mohenjo-daro seal rows without a symbol subtype, Harappa seal rows without a symbol subtype, and Mohenjo-daro bull-symbol seal rows. The result should remain structural-only until source-normalized acquisition checks those high-influence families against physical direction, transcription policy, and object/register duplication.

## Artifacts

- `data/open_prototype/tools/effective_unicity_directionality_influence_controls.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_influence_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_influence_rows.csv`
- `data/open_prototype/reports/effective_unicity_directionality_influence_families.csv`
