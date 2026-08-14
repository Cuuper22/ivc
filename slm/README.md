# IVC SLM exploration branch

This branch trains compact Transformer encoders **from random initialization** on sign sequences. It is a research instrument, not a translator. Its purpose is to test whether a learned sequence model discovers held-out structure that survives exact duplicates, one-edit formula families, site imbalance, and strong nonlinguistic controls.

## Why the largest model is about 20M parameters, not 1B

The executed strict loader contains 1,796 exact-collapsed sequences and 8,205 sign tokens. The older 1,798/8,212 prototype count includes one malformed missing delimiter and one noncanonical direction case variant. A 1B-parameter model would have more than 100,000 parameters per observed token and could memorize the corpus without learning a transferable constraint. The configured 0.89M, roughly 7M, and approximately 20M models form a capacity curve: if the medium model loses family-held-out accuracy while training loss improves, that is evidence of memorization rather than language structure.

This still satisfies the requested "up to 1B" ceiling. The ceiling is treated as permission, not as a target detached from the available evidence.

## Questions answered by the run

1. Does masked-sign prediction beat unigram and bidirectional-bigram baselines when one-edit sequence families cannot cross splits?
2. Does a model trained only on stored sequences assign higher pseudo-likelihood to held-out stored order than reversed order?
3. Does the result survive site-stratified reporting and two order-destroying corpora that preserve row inventories or position-slot frequencies?
4. Does a Transformer body pretrained on clean Linear B plus SumTablets transfer to IVC better than bodies pretrained on exposure-matched nonwriting systems or a position-slot-shuffled IVC control? Every arm begins from a vocabulary-invariant shared-body initialization, and script vocabularies, embeddings, and task heads remain separate.
5. How does IVC compare with scarcity-preserving Linear B Series D and capped SumTablets samples under the identical architecture and split policy? Linear B contributes all 299 length-eligible audited rows; it is not padded or duplicated to look equally large.
6. In a `[BOS] prefix [MASK] [EOS]` cloze, what sign does the model rank in the one-more-sign slot after `002-861` and the two narrower prefixes already in the research ledger? This is not a causal continuation or termination model and never a reading.

## Leakage controls

- Exact sequences are collapsed before splitting.
- One-substitution and one-insertion/deletion neighbors are joined into connected components and kept in one split.
- Every side or row tied to the same CISI object (or comparator source tablet) remains in one split.
- Entire one-edit components containing `002-861` or `002-390` are forced into the test partition before any continuation score is produced.
- The canonical IVC scope requires a real CISI identifier, complete numeric text, and recorded `R/L` or `L/R` direction. The unverified source `class` field is not a supervised target.
- The test split never participates in early stopping or vocabulary-frequency baselines.
- Metrics are reported by site and artifact type, not only as a global average.
- `row_internal_shuffle` applies a nonidentity permutation whenever a row has distinguishable signs, preserves each row's multiset, and reports rows that are mathematically or accidentally unchanged.
- `position_slot_shuffle` preserves length and position-wise token frequencies while breaking within-row dependencies.
- Null transforms never redistribute a held-out object's signs into a training object. Phase-2 controls transform frozen train/validation partitions and score the unchanged authentic test partition; the shuffled pretraining source transforms only a nested split of canonical training objects. Cross-partition null-world exact/one-edit collisions are removed, with resampling attempts and attrition reported.
- Linear B uses its 299 audited, length-eligible Series D rows. SumTablets is deterministically capped without duplicating the smaller comparator.
- The transfer tournament copies only positional and Transformer-body weights. It deliberately reinitializes token embeddings, tied output weights, replacement heads, and authenticity heads for IVC.
- The shuffled-IVC pretraining source is a nested group split of canonical IVC training objects only. Canonical IVC validation/test objects cannot influence its encoder or early stopping. Known-writing and nonwriting source pools are capped by whole leakage groups toward the same unique-record/token exposure; all three receive the same fixed optimizer-step budget, with actual masked-token exposure reported.

## Outputs

Each run writes an immutable directory containing:

- resolved configuration and SHA-256 hashes of every input;
- hardware, package, Git, seed, parameter-count, runtime, and cost metadata;
- train/validation curves and the best checkpoint;
- exhaustive held-out masked-token predictions;
- stored-versus-reversed pseudo-likelihood rows;
- held-out performance of the explicitly trained authenticity-versus-corruption head, with any corruption that matches a published authentic sequence skipped and counted (this is generalization of a trained task, not independent directionality evidence);
- one-more-sign cloze rankings for the fixed prefixes;
- embedding-neighbor and positional-profile tables;
- a matrix summary across seeds, scales, comparators, null controls, and transfer arms;
- paired-seed transfer deltas with an exploratory bootstrap interval and a pre-registered known-writing-specificity gate.

## Execution

From `slm/` inside a CUDA-enabled PyTorch environment:

```bash
python -m pip install -e .
IVCSLM_HOURLY_RATE_USD=0.34 ivcslm run-matrix --config configs/ivc_research_14usd.json
```

Set `IVCSLM_HOURLY_RATE_USD` to the provider's actual all-in rate, not the example, before allocating the GPU. The runner accounts for a supplied billed-start time, checks its deadline during fitting and evaluation, and refuses silent CPU fallback. The provider workspace must also have a hard `$14` spending cap or TTL because application-level accounting cannot terminate a failed host process.

Set `IVCSLM_OUTPUT_DIR` to keep full checkpoints on attached storage outside the Git checkout. Curated summaries and tables can then be copied into `research/data/slm/`; multi-run checkpoints are intentionally not repository artifacts.

## Evidence boundary

The IVC input is the T3 Lipi planning layer, not an authoritative image-normalized corpus. A positive model result can prioritize source validation and reject weak nulls. It cannot establish a phonetic value, sign meaning, language family, external anchor, or translation.
