# Methods Note: Terminal-Governor Effective Unicity

Date: 2026-05-31

Status: structural candidate, not decipherment

## Question

Do the Indus signs `002` and `060` reduce final-slot uncertainty in a way that survives held-out prediction and adversarial nulls?

A terminal governor is a next-to-last sign that constrains which sign can close the inscription. This reframes effective unicity away from whole-inscription translation. Instead of asking "can we read the texts?", the test asks whether one local part of the corpus behaves like a constrained sign-role system: a penultimate governor predicts its terminal closure better than frequency, site, duplicate texts, or major excavation blocks can explain.

## Corpus Unit

Source file: `data/open_prototype/lipi/metadata_filtered.csv`

Rows are restricted to complete inscriptions for the main unicity delta test. Each exact inscription text contributes once, so duplicated catalogue rows cannot inflate prediction. Each text family keeps the set of sites where it is attested.

For every exact text with at least two signs:

- `penult` = next-to-last sign
- `final` = last sign
- target penults = `002`, `060`

## Held-Out Prediction

Held-out prediction means the model must predict rows it never trained on. For each site, the model holds out all terminal text families attested at that site. It trains on terminal families not attested at that site and excludes exact texts that also occur in the holdout. For each held-out row, it uses the training distribution `P(final | penult)` if that penult has at least 5 training examples.

Reported metrics:

- top-1 and top-3 accuracy for the held-out final sign
- mean probability assigned to the true final sign
- entropy-derived mean effective candidate count
- comparison to global final-sign probability

## Null

The null model is built to keep everything about the data except the one thing being claimed. It preserves:

- terminal text families
- penultimate signs
- sites
- the global final-sign inventory

It shuffles final labels across terminal families and reruns the same leave-site prediction. This destroys the specific `penult -> final` pairing while preserving how common each final sign is.

## Main Result

Target governors `002/060`:

- 456 evaluated leave-site rows
- top-1 accuracy `0.311`
- top-3 accuracy `0.787`
- mean effective final candidates `6.39`

Non-target penults:

- 1,138 evaluated rows
- top-1 accuracy `0.098`
- top-3 accuracy `0.177`
- mean effective final candidates `15.71`

Final-label shuffle null:

- `p=0.001` for target top-1 accuracy
- `p=0/1000` for target top-3 accuracy
- `p=0/1000` for mean true probability
- `p=0/1000` for effective-candidate compression

## Block Stress

A result carried by one big block of similar objects would not be a corpus property. So the same test was rerun after removing major square-seal blocks:

| Panel | Target rows | Top-3 | Effective candidates | Null p for top-3 |
|---|---:|---:|---:|---:|
| all complete exact texts | 456 | 0.787 | 6.39 | 0/100 |
| remove Mohenjo-daro `SEAL:S` | 234 | 0.761 | 6.27 | 0/100 |
| remove Harappa `SEAL:S` | 407 | 0.806 | 5.88 | 0/100 |
| remove both Mohenjo-daro and Harappa `SEAL:S` | 185 | 0.778 | 5.85 | 0/100 |

The 100-shuffle stress is a consolidation falsifier, not the final null. It is strong enough to reject the immediate “one major block carries it” explanation; it should be rerun heavier after source-token collapse.

## Frequency Confound Check

Maybe `002` and `060` look special only because they are common. They do not: high-frequency non-target penults fail to reproduce the target behavior:

| Penult | Rows | Top-3 | Effective candidates |
|---|---:|---:|---:|
| `002` | 313 | 0.856 | 6.22 |
| `060` | 143 | 0.636 | 6.75 |
| `740` | 133 | 0.090 | 54.07 |
| `220` | 56 | 0.286 | 13.74 |
| `390` | 55 | 0.127 | 18.69 |

The one nearest non-target mimic is `240`, with top-3 `0.652` and effective candidates `4.93`, but only over 23 evaluated rows. It should become a future risky bet, not a frequency confound for `002/060`.

## Interpretation

This result supports a local structural claim:

`002` and `060` behave as terminal governors whose closure inventories reduce final-slot uncertainty across held-out sites.

It does not support:

- phonetic values
- translations
- language-family identification
- a claim that the entire script is linguistic
- a claim that `002/060` are grammatical morphemes in a known language

The next decisive test is source-token collapse: source-box the target terminal rows, collapse by source family, rerun the held-out prediction, and require the top-3/effective-candidate advantage to survive.
