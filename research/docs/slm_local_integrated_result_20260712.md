# Local from-scratch SLM integrated result

Date: 2026-07-12 America/Los_Angeles

Status: complete negative calibration result. This validates the train-to-report instrument; it does not validate an IVC claim.

## What this is and why it exists

An SLM is a small language model: a neural network trained to predict signs hidden from it. This note records the first end-to-end run of one on the Indus corpus, on a local machine, before any money was spent on GPUs.

The purpose of a first run is not to learn something about the script. It is to find out whether the machinery works — whether data loads, splits hold, training converges, and numbers come out the far end in a form that can be checked. That is calibration. The result here is a negative calibration: the pipeline works and the model loses to a simple baseline. Both halves of that sentence matter, and neither is a claim about the Indus script.

The run also decides one practical question. A GPU run costs money, so it needs a reason. This note says what that reason is and what would close the lane instead.

## What actually ran

One 886,850-parameter, four-layer Transformer encoder was initialized from scratch — random weights, nothing learned from any other corpus — and trained for 120 epochs / 360 optimizer steps. The input was exact-sequence collapsed, grouped by one-edit family and catalogue object, and split with every component touching `002-861` or `002-390` forced into the hypothesis test partition. Grouping that way keeps near-identical rows from landing on both sides of the split, where they would let the model score by recall instead of by learning.

The strict loader produced 1,796 sequences / 8,205 tokens rather than the older prototype's 1,798 / 8,212. Two rows dropped out, and they dropped out for stated reasons rather than silently:

- M-207 has `+892-831` without the required closing `+`, despite its older readiness label.
- H-23 has the malformed direction value `R/l`, not an allowed exact `R/L` or `L/R` value.

Both remain outside the model scope until source metadata is corrected by a dated corpus gate.

## Result

Held out means kept out of training entirely, so these numbers measure prediction rather than recall. Restoration is the task itself: one sign is hidden, and the model names it. Top-1 counts how often its best single guess is right; top-5 how often the right answer is anywhere in its top five. The bidirectional bigram is the honest floor — a baseline that only knows which signs tend to sit next to which.

| Ordinary held-out metric | Micro SLM | Baseline | Delta |
| --- | ---: | ---: | ---: |
| top-1 restoration | 0.1989 | bidirectional bigram 0.2355 | -0.0365 |
| top-5 restoration | 0.3857 | bidirectional bigram 0.4560 | -0.0704 |
| mean negative log-likelihood | 4.3953 | not emitted for baseline | — |
| multiclass Brier | 0.9113 | not emitted for baseline | — |

The model loses to the bidirectional bigram on both restoration metrics. It is also vague where it needs to be sharp: to be 80% sure of covering the right answer, its prediction sets have to average 108 signs. A distribution that wide cannot narrow a reading down to a short candidate list.

The directionality score is high — `0.8913` stored-order wins, after excluding a palindrome and any authentic reverse pair — and the explicitly trained authenticity head beats reversals at `0.9130`. Neither number is promotable, for three separate reasons: this is one seed, the authenticity head was trained on exactly the corruptions it then scored, and the learned shuffle and nonwriting controls have not run yet.

## Forced-family finding

The harsh family policy sends 855 of 1,796 exact sequences into the forced hypothesis partition, leaving 663 train, 139 validation, and 139 ordinary test sequences. That split is lopsided, and the reason it is lopsided is itself worth knowing: `002-861` and `002-390` sit inside a very large region of rows connected to each other by single-sign edits. A casual row split would put close relatives of the test rows into training and leak the region badly.

The model scores 0.2219 top-1 and 0.4171 top-5 across the 3,047 forced-family sign positions. That number is descriptive only. The local run has no matched forced-family baseline, no second seed, and no learned control, so there is nothing to compare it against.

## Decision

No claim count changes. The local model is a functioning research instrument with a negative first calibration. That is enough to justify a GPU run for one fixed question and no other: whether an exposure-matched known-writing body improves ordinary held-out IVC restoration more than random-init, nonwriting, and shuffled-IVC bodies. Exposure-matched means every arm sees the same amount of training material, so the comparison is about the source and not the diet. If that gate fails, or if the exposures fall outside tolerance, the neural lane closes without semantic interpretation.

Machine-readable result: `research/data/open_prototype/reports/slm_local_integrated_20260712_summary.json`.
