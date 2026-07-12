# Local from-scratch SLM integrated result

Date: 2026-07-12 America/Los_Angeles

Status: complete negative calibration result. This validates the train-to-report instrument; it does not validate an IVC claim.

## What actually ran

One 886,850-parameter, four-layer Transformer encoder was initialized from scratch and trained for 120 epochs / 360 optimizer steps. The input was exact-sequence collapsed, grouped by one-edit family and catalogue object, and split with every component touching `002-861` or `002-390` forced into the hypothesis test partition.

The strict loader produced 1,796 sequences / 8,205 tokens rather than the older prototype's 1,798 / 8,212. This is deliberate, not silent loss:

- M-207 has `+892-831` without the required closing `+`, despite its older readiness label.
- H-23 has the malformed direction value `R/l`, not an allowed exact `R/L` or `L/R` value.

Both remain outside the model scope until source metadata is corrected by a dated corpus gate.

## Result

| Ordinary held-out metric | Micro SLM | Baseline | Delta |
| --- | ---: | ---: | ---: |
| top-1 restoration | 0.1989 | bidirectional bigram 0.2355 | -0.0365 |
| top-5 restoration | 0.3857 | bidirectional bigram 0.4560 | -0.0704 |
| mean negative log-likelihood | 4.3953 | not emitted for baseline | — |
| multiclass Brier | 0.9113 | not emitted for baseline | — |

The model loses to the bidirectional bigram on both restoration metrics. Its 80% prediction sets average 108 signs, so the probability distribution is not sharp enough to prioritize a small reading candidate set.

The directionality score is high (`0.8913` stored-order wins after excluding a palindrome and any authentic reverse pair), and the explicitly trained authenticity head beats reversals at `0.9130`. Neither is promotable: this is one seed, the authenticity head was trained on corruptions, and the learned shuffle/nonwriting controls have not run.

## Forced-family finding

The harsh family policy sends 855 of 1,796 exact sequences into the forced hypothesis partition, leaving 663 train, 139 validation, and 139 ordinary test sequences. This is important in its own right: `002-861`/`002-390` are embedded in a very large one-edit-connected formula region. A casual row split would leak that region badly.

The model scores 0.2219 top-1 and 0.4171 top-5 across the 3,047 forced-family sign positions, but that number is descriptive only. The local run has no matched forced-family baseline, no other seed, and no learned control.

## Decision

No claim count changes. The local model is a functioning research instrument with a negative first calibration. The online GPU run is justified only for the fixed transfer question: whether an exposure-matched known-writing body improves ordinary held-out IVC restoration more than random-init, nonwriting, and shuffled-IVC bodies. If that gate fails or exposures fall outside tolerance, the neural lane closes without semantic interpretation.

Machine-readable result: `research/data/open_prototype/reports/slm_local_integrated_20260712_summary.json`.
