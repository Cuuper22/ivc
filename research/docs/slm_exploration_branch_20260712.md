# From-scratch IVC SLM exploration branch

Date: 2026-07-12 America/Los_Angeles

Branch: `codex/ivc-slm-exploration`

Status: implementation in progress; no model result is accepted by this note.

## What this is and why it exists

An SLM is a small language model: a neural network trained to predict signs that have been hidden from it. This note is the plan for building one on the Indus corpus and the rules it must obey. It is written before the runs, on purpose. Pre-registering the design is what stops the standard from sliding once results arrive, and a model is unusually good at producing something that looks like a result if you let it choose its own test afterwards.

The models here are trained from scratch, meaning they start from random weights and learn only from the corpus they are given. Nothing about any known language is built in.

A branch is one line of investigation, kept separate so it can be abandoned without disturbing anything else. This one exists because the source-only work has parked, and there are three questions left that a model can address and a person cannot easily.

The strong prior is that this will not decipher anything, and the note is built around that. Every question below is posed so that a null answer is informative, and every model comparison is run against a control that destroys the structure being claimed.

## Evidence boundary

This branch starts from the replacement-run checkpoint, not the quarantined global backlog, broad claim ledger, findings dossier, or post-cutoff strongest-result brief. The training input is `research/data/open_prototype/lipi/metadata_filtered.csv`, a T3 planning layer — third-tier data, good for generating candidates and never authoritative. It can support hypothesis generation and adversarial structural tests. It cannot support translation or values.

Accepted counts remain:

| Claim class | Count |
| --- | ---: |
| translations | 0 |
| phonetic values | 0 |
| sign meanings | 0 |
| language identification | 0 |
| external anchors | 0 |
| structural findings | 1 |

The only accepted structural result remains the fixed `002-861 / 533-717` restricted terminal-tail claim under its existing narrow wording.

## Why this branch exists

The replacement checkpoint leaves three questions a model can address, once the source-only gates are parked:

1. Does held-out local context remain learnable after exact duplicates and one-edit formula families are kept out of opposite splits?
2. Does stored order retain higher pseudo-likelihood than reversed order in a learned model, and does that survive order-destroying controls?
3. Does the post-`002-861` field support typed continuation predictions, or does a larger model merely memorize whole formulas?

## Pre-registered design

Fixed in advance, so that no choice below can be made after seeing which choice would flatter the result.

- Models are randomly initialized Transformer encoders trained by masked-sign prediction: hide one sign in a row, make the model name it.
- Capacity curve: approximately 0.89M, 7M, and 20M parameters. This is the scaling test — whether more parameters buy better predictions on this corpus. A 1B model is rejected as the primary instrument because the executed strict exact-collapsed layer has only 1,796 sequences and 8,205 sign tokens; a 1B model would be a memorization demonstration.
- Exact sequences are collapsed. Duplicate rows would otherwise let the model score well by recall.
- One-substitution and one-insertion/deletion connected components are split as indivisible groups. Rows that differ by a single sign are near-duplicates, so they must land on the same side of a split or the test leaks.
- Evaluation is exhaustive one-token masking on held-out sequences. Held out means kept out of training entirely, which is how learning is told apart from memorizing.
- Baselines: unigram and bidirectional bigram. A model that cannot beat sign frequency and neighboring-sign frequency has shown nothing.
- Learned controls: within-row shuffle and length/position-slot shuffle. Each destroys the structure the model is supposed to be finding, so the model should get worse on them.
- Real comparators: all 299 audited, length-eligible Linear B Series D rows plus capped SumTablets. The smaller Linear B inventory is reported honestly rather than duplicated to force equal sample size.
- Structural-transfer tournament: random-init IVC versus a shared Transformer body pretrained from scratch on clean known writing, a size-matched nonwriting/ambiguous-system bank, or position-slot-shuffled IVC. Transfer means training the body on one corpus and then moving it to another; the question is whether the head start helps, and whether it helps more when the first corpus is real writing. Token embeddings, output weights, and task heads are always fresh and script-specific.
- The shuffled pretraining source is built only from a nested group split of canonical IVC training objects; target validation/test objects never enter source training or early stopping. Source arms receive 1,000 optimizer steps each and report actual masked-position exposure — the amount of training material each arm actually saw, which must match or the comparison measures diet rather than source.
- Transfer uses the fixed-step endpoint checkpoint, not each source's independently timed best-validation checkpoint. Letting each source stop at its own best moment would hand one arm an advantage that has nothing to do with what it was trained on. A separate best checkpoint is retained only for source diagnostics.
- Learned null corpora are transformed separately inside frozen partitions. Their source/artifact membership is paired to the authentic split, and accidental null-world exact/one-edit collisions are reported explicitly.
- The full `002-861` and `002-390` one-edit components are forced into test before any continuation probe is emitted. Those are the sequences the project cares about most, so the model must never have trained on them.
- Primary probes: top-1/top-5, pseudo-perplexity, stored-versus-reversed pseudo-likelihood, site/type slices, embedding/positional neighborhoods, and a sign-only `[BOS] prefix [MASK] [EOS]` one-more-sign cloze after three fixed prefixes. Perplexity measures how surprised the model is by the true sign; lower is better. A cloze asks it to fill one blank. This cloze does not estimate termination or causal continuation.
- Five seeds are required for the online matrix. A seed is one random start, and a result that appears under only one of them is luck.
- No model output is a reading. Prefix predictions are queue-ranking evidence only: they say what to look at next, not what a sign means.

The pre-registered transfer gate passes only if known-writing pretraining improves paired held-out negative log-likelihood over random-init IVC, nonwriting pretraining, and shuffled-IVC pretraining, with all three exploratory paired-seed bootstrap lower bounds above zero. Note what that demands: not just that known writing helps, but that it helps more than a nonwriting corpus and more than the Indus corpus with its own order destroyed. With five seeds this interval is a stability screen, not a population-level inferential guarantee.

## Budget gate

Compute is capped in advance so that a disappointing result cannot be answered by buying more of it. The full configuration hard-limits measured runtime and estimated compute cost. With a planned GPU rate of USD 0.45/hour, the runner reserves USD 2 from the USD 14 ceiling and will not start another model after the smaller of six wall-clock hours or the cost-derived limit is reached. Provider deposits or unused credits are tracked separately from consumed compute.

## Required artifacts before interpretation

A run that cannot be audited cannot be believed. The run is not interpretable unless it emits input hashes, resolved configuration, Git state, package/hardware manifest, split groups, training curves, checkpoints, exhaustive predictions, directionality rows, continuation rankings, and a completed matrix summary. If controls are missing, the run is incomplete. It is not a positive result.
