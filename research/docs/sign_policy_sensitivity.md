# Sign Policy Sensitivity

Date: 2026-05-24

## Purpose

This experiment tests whether the structural signal survives different provisional sign-inventory policies.

It is not a sign validation step. It asks a narrower question: if provisional crosswalk or allograph choices are applied, does the order/masked-sign signal collapse, stay stable, or change in suspicious ways?

## Local Artifacts

```text
data/open_prototype/reports/sign_policy_sensitivity_summary.json
data/open_prototype/reports/sign_policy_sensitivity_sequences.csv
data/open_prototype/reports/sign_policy_sensitivity_sequence_scores.csv
data/open_prototype/reports/sign_policy_sensitivity_sequence_summary.csv
data/open_prototype/reports/sign_policy_sensitivity_masked_predictions.csv
data/open_prototype/reports/sign_policy_sensitivity_masked_summary.csv
```

Source files:

```text
data/open_prototype/reports/mismatch_audit.csv
data/open_prototype/reports/crosswalk_lipi_to_mayig_candidates.csv
```

Eligibility rule:

```text
status == candidate_for_pre_crosswalk_structure_tests
lipi_dir == R/L
flags empty
```

Dataset:

```text
eligible_records: 136
tokens: 739
```

## Sign Policies

| Policy | Meaning |
| --- | --- |
| `raw_lipi_numeric` | Prefix numeric `lipi` signs as `L###`; no merges. |
| `p385_merge_only` | Collapse only `817` and `861` to `P385`; all other signs stay `L###`. |
| `provisional_high_map` | Map high-consistency positional candidates to `P###`; leave all others `L###`. |
| `provisional_high_medium_map` | Map high and medium positional candidates to `P###`; leave all others `L###`. |
| `mayig_observed_parpola` | Use observed `mayig` `P###` strings for the same rows. |

One-to-one renaming is not meaningful by itself. It should not change structural behavior. The important changes are merges and splits, especially `817`/`861 -> P385`.

## Sequence Order Result

| Policy | Vocab size | Distinct sequences | Rows >1 | Observed > reversed | Reversed > observed | Ties | Observed > shuffle mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `raw_lipi_numeric` | 189 | 136 | 136 | 129 | 4 | 3 | 127 |
| `p385_merge_only` | 188 | 136 | 136 | 129 | 4 | 3 | 127 |
| `provisional_high_map` | 188 | 136 | 136 | 129 | 4 | 3 | 127 |
| `provisional_high_medium_map` | 187 | 136 | 136 | 129 | 4 | 3 | 127 |
| `mayig_observed_parpola` | 160 | 135 | 136 | 129 | 5 | 2 | 127 |

Interpretation:

The order signal survives every tested sign policy. The `P385` merge and the broader provisional mappings do not create or destroy the basic direction/order result.

## Masked Sign Prediction

| Policy | Model | Top-1 accuracy | Top-5 accuracy | MRR |
| --- | --- | ---: | ---: | ---: |
| `raw_lipi_numeric` | Frequency | 0.098782 | 0.281461 | 0.195111 |
| `raw_lipi_numeric` | Position | 0.158322 | 0.335589 | 0.244833 |
| `raw_lipi_numeric` | Bidirectional bigram | 0.281461 | 0.487145 | 0.377468 |
| `p385_merge_only` | Bidirectional bigram | 0.307172 | 0.497970 | 0.393922 |
| `provisional_high_map` | Bidirectional bigram | 0.307172 | 0.497970 | 0.393922 |
| `provisional_high_medium_map` | Bidirectional bigram | 0.308525 | 0.499323 | 0.398087 |
| `mayig_observed_parpola` | Bidirectional bigram | 0.319350 | 0.515562 | 0.408703 |

The full masked summary is in:

```text
data/open_prototype/reports/sign_policy_sensitivity_masked_summary.csv
```

Interpretation:

Bidirectional context remains better than frequency and position baselines under every policy. The `P385` merge raises top-1 accuracy from 0.281461 to 0.307172. The full observed `mayig` Parpola policy reaches 0.319350, partly because the inventory is smaller and one pair of sequences collapses.

That is structurally interesting, but not a proof of the merge. Collapsed labels can make exact prediction easier even when the merge is not epigraphically correct.

## Result

The tested provisional sign policies pass a structural stability screen:

- Order signal remains stable.
- Bidirectional masked prediction remains above frequency and position baselines.
- The `P385` merge does not damage structural behavior.
- Observed `mayig` `P###` strings preserve the same order signal on the strict row set.

## Counterresult

The result does not validate the mappings:

- No image or publication-plate check was performed.
- No authoritative sign-list cross-reference was used.
- A lower vocabulary can inflate exact-sign prediction.
- The corpus slice is still Mohenjo-daro `SEAL:S` only.
- The sensitivity test cannot decide whether `817` and `861` are true allographs, catalog variants, transcription conventions, or different signs with similar distribution.

## Interpretation Boundary

This experiment supports only this claim:

```text
The provisional sign policies tested here preserve the prototype structural signal, and the `817`/`861 -> P385` candidate passes a first structural screen.
```

It does not support:

- Accepted allograph merge.
- Accepted sign crosswalk.
- Meaning.
- Phonetic value.
- Language identity.
- Translation.

## Next Falsification

The next step for `P385` is manual validation:

```text
817 -> P385
861 -> P385
```

Required evidence:

- Primary image or publication plate for paired examples.
- Feature comparison for the two numeric signs.
- Neighbor-distribution comparison outside the 136-row strict subset.
- Test whether keeping `817` and `861` split predicts any metadata or structural class better than merging them.

