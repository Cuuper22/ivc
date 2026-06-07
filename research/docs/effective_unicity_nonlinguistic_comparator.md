# Effective-Unicity Nonlinguistic Comparator

Date: 2026-05-29

## Result

The Vector 2 comparator now separates three things that are easy to confuse:

1. Leave-one-row-out masked-sign top-1 accuracy survives the current effective-unicity forger gate.
2. Broad bidirectional predictability does not survive structured nonlinguistic adversaries.
3. Masked-sign top-1 predictability does not survive real-world nonlinguistic and ambiguous-system calibration as language evidence.

This is the useful boundary. The corpus has local context constraint, but generic predictability is not language evidence.

## Inputs

Generated files:

- `data/open_prototype/reports/effective_unicity_degeneracy_summary.json`
- `data/open_prototype/reports/lipi_synthetic_comparator_summary.json`
- `data/open_prototype/reports/lipi_structured_null_summary.json`
- `data/open_prototype/reports/effective_unicity_nonlinguistic_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_nonlinguistic_comparator.csv`
- `data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_comparator.csv`

The rerun uses the current strict Lipi scope: 2,883 source rows, 1,798 exact-collapsed rows, 8,212 tokens, and 571 observed signs.

## Surviving Narrow Metric

The effective-unicity masked-sign task tests each held-out token with its row excluded from training. At full coverage:

| Metric | Observed | Controls | Max FPR |
| --- | ---: | --- | ---: |
| masked top-1 | 0.279591 | 6 controls, 100 iterations each | 0 |

Control means:

| Control | Null mean | Null p95 | Null max | FPR |
| --- | ---: | ---: | ---: | ---: |
| global token shuffle | 0.106400 | 0.119167 | 0.127500 | 0 |
| row internal shuffle | 0.120083 | 0.135000 | 0.137500 | 0 |
| position slot shuffle | 0.165233 | 0.179208 | 0.198333 | 0 |
| edge frame shuffle | 0.165025 | 0.179167 | 0.190833 | 0 |
| register-blocked position shuffle | 0.169358 | 0.188375 | 0.200000 | 0 |
| template administrative code | 0.087867 | 0.106708 | 0.115000 | 0 |

Accepted interpretation: local context constrains signs beyond these tested controls.

Forbidden interpretation: this identifies a sound, word, language family, or translation.

## Failed Broad Metric

The older broad bidirectional predictor has observed top-1 accuracy 0.325865. Simple shuffles do not reproduce it, but structured nonlinguistic generators do:

| Structured control | Null mean | Null p05 | Null p95 | Null >= observed |
| --- | ---: | ---: | ---: | ---: |
| administrative register code | 0.472924 | 0.461842 | 0.482233 | 1 |
| emblem formula code | 0.443351 | 0.433902 | 0.453915 | 1 |
| mixed admin/emblem code | 0.415069 | 0.405170 | 0.425189 | 1 |

Decision: broad bidirectional predictability is retracted as language-identification or semantic evidence. It is too easy for administrative and emblematic systems to mimic or exceed.

## Real-World Comparator

The Sproat 2014 real-world corpus bundle adds nonlinguistic and ambiguous systems that are not synthetic forgers. The same masked-symbol instrument was run on exact-collapsed length-2-through-8 primary sequences.

| System | Class | Rows | Symbols | Top-1 | Top-5 | Max null >= observed |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Indus strict exact-collapsed | unread working corpus | 1,798 | 571 | 0.279591 | 0.534096 | 0 |
| Pictish stones | ambiguous symbol system | 187 | 78 | 0.450292 | 0.614035 | 0 |
| Barn stars / hex signs | known nonwriting decorative system | 97 | 29 | 0.367123 | 0.673973 | 1 |
| Weather icons | modern nonlinguistic icon sequences | 4,018 | 16 | 0.265555 | 0.790543 | 0 |
| Kudurru deity symbols | known nonwriting pictorial system | 24 | 39 | 0.177966 | 0.500000 | 0 |
| Vinca symbols | ambiguous archaeological symbol system | 91 | 82 | 0.088561 | 0.276753 | 0.75 |
| Totem poles | known nonwriting emblematic system | 246 | 359 | 0.085485 | 0.300980 | 0.05 |

Decision: masked top-1 predictability is retracted as language evidence. Pictish and barn-star systems exceed the Indus reference. This does not invalidate the narrower structural instrument; it blocks the interpretation that masked predictability itself is writing-specific.

## Boundary

Simple shuffles are weak adversaries. Passing them only says the corpus is not pure shuffled noise. The stronger result is narrower and more defensible: masked-sign local constraint survives the current forger suite, while unanchored label symmetry still blocks phonetic and language-family claims.

No accepted claim count changes follow from this comparator.
