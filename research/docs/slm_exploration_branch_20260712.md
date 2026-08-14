# From-scratch IVC SLM exploration branch

Date: 2026-07-12 America/Los_Angeles

Branch: `codex/ivc-slm-exploration`

Status: implementation in progress; no model result is accepted by this note.

## Evidence boundary

This branch starts from the replacement-run checkpoint, not the quarantined global backlog, broad claim ledger, findings dossier, or post-cutoff strongest-result brief. The training input is `research/data/open_prototype/lipi/metadata_filtered.csv`, a T3 planning layer. It can support hypothesis generation and adversarial structural tests, not translation or values.

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

The replacement checkpoint leaves three model-addressable questions after source-only gates are parked:

1. Does held-out local context remain learnable after exact duplicates and one-edit formula families are kept out of opposite splits?
2. Does stored order retain higher pseudo-likelihood than reversed order in a learned model, and does that survive order-destroying controls?
3. Does the post-`002-861` field support typed continuation predictions, or does a larger model merely memorize whole formulas?

## Pre-registered design

- Models are randomly initialized Transformer encoders trained by masked-sign prediction.
- Capacity curve: approximately 0.89M, 7M, and 20M parameters. A 1B model is rejected as the primary instrument because the executed strict exact-collapsed layer has only 1,796 sequences and 8,205 sign tokens; a 1B model would be a memorization demonstration.
- Exact sequences are collapsed.
- One-substitution and one-insertion/deletion connected components are split as indivisible groups.
- Evaluation is exhaustive one-token masking on held-out sequences.
- Baselines: unigram and bidirectional bigram.
- Learned controls: within-row shuffle and length/position-slot shuffle.
- Real comparators: all 299 audited, length-eligible Linear B Series D rows plus capped SumTablets. The smaller Linear B inventory is reported honestly rather than duplicated to force equal sample size.
- Structural-transfer tournament: random-init IVC versus a shared Transformer body pretrained from scratch on clean known writing, a size-matched nonwriting/ambiguous-system bank, or position-slot-shuffled IVC. Token embeddings, output weights, and task heads are always fresh and script-specific.
- The shuffled pretraining source is built only from a nested group split of canonical IVC training objects; target validation/test objects never enter source training or early stopping. Source arms receive 1,000 optimizer steps each and report actual masked-position exposure.
- Transfer uses the fixed-step endpoint checkpoint, not each source's independently timed best-validation checkpoint. A separate best checkpoint is retained only for source diagnostics.
- Learned null corpora are transformed separately inside frozen partitions. Their source/artifact membership is paired to the authentic split, and accidental null-world exact/one-edit collisions are reported explicitly.
- The full `002-861` and `002-390` one-edit components are forced into test before any continuation probe is emitted.
- Primary probes: top-1/top-5, pseudo-perplexity, stored-versus-reversed pseudo-likelihood, site/type slices, embedding/positional neighborhoods, and a sign-only `[BOS] prefix [MASK] [EOS]` one-more-sign cloze after three fixed prefixes. The cloze does not estimate termination or causal continuation.
- Five seeds are required for the online matrix.
- No model output is a reading. Prefix predictions are queue-ranking evidence only.

The pre-registered transfer gate passes only if known-writing pretraining improves paired held-out negative log-likelihood over random-init IVC, nonwriting pretraining, and shuffled-IVC pretraining, with all three exploratory paired-seed bootstrap lower bounds above zero. With five seeds this interval is a stability screen, not a population-level inferential guarantee.

## Budget gate

The full configuration hard-limits measured runtime and estimated compute cost. With a planned GPU rate of USD 0.45/hour, the runner reserves USD 2 from the USD 14 ceiling and will not start another model after the smaller of six wall-clock hours or the cost-derived limit is reached. Provider deposits or unused credits are tracked separately from consumed compute.

## Required artifacts before interpretation

The run is not interpretable unless it emits input hashes, resolved configuration, Git state, package/hardware manifest, split groups, training curves, checkpoints, exhaustive predictions, directionality rows, continuation rankings, and a completed matrix summary. Missing controls mean an incomplete run, not a positive result.
