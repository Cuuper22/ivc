# IVC SLM exploration branch

This branch trains small Transformer encoders **from random initialization** on Indus Valley Civilization (IVC) sign sequences — the strings of numbered signs recorded on seals and tablets. It is a measuring instrument, not a translator.

The question it asks is narrow. If you hide a sign in a sequence the model has never seen, can the model guess it better than simple frequency counting? A model can only do that if the sequences carry structure that repeats across objects. So the harness is a test for repeatable order, nothing more.

Structure is easy to fake, though. A model can score well by memorizing near-copies of training rows, by riding one dominant site's habits, or by exploiting sign frequency alone. Every design choice below exists to remove one of those cheats: exact duplicates, one-edit formula families, site imbalance, and strong nonlinguistic controls.

## Why the largest model is about 20M parameters, not 1B

The evidence is small. The executed strict loader contains 1,796 exact-collapsed sequences and 8,205 sign tokens. (The older 1,798/8,212 prototype count is higher because it included one malformed row with a missing delimiter and one noncanonical direction case variant.)

Capacity has to be scaled to that. A 1B-parameter model would carry more than 100,000 parameters for every token it ever sees. It could store the corpus outright and still tell you nothing about whether the sequences share a constraint.

So the configured models — 0.89M, roughly 7M, and approximately 20M parameters — are used as a capacity curve, a deliberate ladder of model sizes run under identical conditions. The curve is itself a diagnostic: if the medium model's training loss keeps improving while its accuracy on held-out one-edit families falls, that gap is evidence of memorization rather than of shared structure.

This still satisfies the requested "up to 1B" ceiling. The ceiling is permission, not a target to chase away from the evidence.

## Questions answered by the run

1. Does masked-sign prediction — hide one sign, predict it from both sides — beat unigram and bidirectional-bigram baselines when one-edit sequence families cannot cross splits?
2. Does a model trained only on stored sequences assign higher pseudo-likelihood (the summed log probability of each sign given the rest) to held-out stored order than to reversed order?
3. Does the result survive site-stratified reporting and two order-destroying corpora, one that preserves each row's sign inventory and one that preserves position-slot frequencies?
4. Does a Transformer body pretrained on clean Linear B plus SumTablets transfer to IVC better than bodies pretrained on exposure-matched nonwriting systems or on a position-slot-shuffled IVC control? Every arm starts from the same vocabulary-invariant shared-body initialization, so the arms differ only in what they were pretrained on. Script vocabularies, embeddings, and task heads stay separate.
5. How does IVC compare with scarcity-preserving Linear B Series D and capped SumTablets samples under the identical architecture and split policy? Linear B contributes all 299 length-eligible audited rows; it is not padded or duplicated to look equally large.
6. In a `[BOS] prefix [MASK] [EOS]` cloze — one blank slot at the end of a fixed prefix — what sign does the model rank first after `002-861` and after the two narrower prefixes already in the research ledger? This is not a causal continuation model, not a termination model, and never a reading.

## Leakage controls

A leak here means any path by which a held-out sequence, or a near-copy of it, influences fitting. Each control below closes one path.

- Exact sequences are collapsed before splitting, so an identical string cannot sit on both sides.
- One-substitution and one-insertion/deletion neighbors are joined into connected components, and a whole component stays in one split. Formula variants therefore travel together.
- Every side or row tied to the same CISI object (or comparator source tablet) remains in one split.
- Entire one-edit components containing `002-861` or `002-390` are forced into the test partition before any continuation score is produced.
- The canonical IVC scope requires a real CISI identifier, complete numeric text, and a recorded `R/L` or `L/R` direction. The unverified source `class` field is not used as a supervised target.
- The test split never participates in early stopping or in vocabulary-frequency baselines.
- Metrics are reported by site and artifact type, not only as a global average.
- `row_internal_shuffle` applies a nonidentity permutation whenever a row has distinguishable signs, preserves each row's multiset of signs, and reports the rows that came out unchanged either mathematically or by accident.
- `position_slot_shuffle` preserves length and position-wise token frequencies while breaking the dependencies inside a row.
- Null transforms never move a held-out object's signs into a training object. Phase-2 controls transform the frozen train/validation partitions and score the unchanged authentic test partition; the shuffled pretraining source transforms only a nested split of canonical training objects. Exact and one-edit collisions that the transform creates across partitions are removed, and the resampling attempts and the resulting attrition are reported.
- Linear B uses its 299 audited, length-eligible Series D rows. SumTablets is capped deterministically rather than by duplicating the smaller comparator.
- The transfer tournament copies only positional and Transformer-body weights. It deliberately reinitializes token embeddings, tied output weights, replacement heads, and authenticity heads for IVC.
- The shuffled-IVC pretraining source is a nested group split of canonical IVC training objects only. Canonical IVC validation and test objects cannot reach its encoder or its early stopping. Known-writing and nonwriting source pools are capped by whole leakage groups toward the same unique-record and token exposure; all three get the same fixed optimizer-step budget, and the masked-token exposure actually reached is reported.

## Outputs

Each run writes one immutable directory containing:

- the resolved configuration and SHA-256 hashes of every input;
- hardware, package, Git, seed, parameter-count, runtime, and cost metadata;
- train/validation curves and the best checkpoint;
- exhaustive held-out masked-token predictions;
- stored-versus-reversed pseudo-likelihood rows;
- held-out performance of the explicitly trained authenticity-versus-corruption head, with any corruption that happens to match a published authentic sequence skipped and counted. This head was trained on that task, so its score is generalization of a trained task, not independent directionality evidence;
- one-more-sign cloze rankings for the fixed prefixes;
- embedding-neighbor and positional-profile tables;
- a matrix summary across seeds, scales, comparators, null controls, and transfer arms;
- paired-seed transfer deltas with an exploratory bootstrap interval and a pre-registered known-writing-specificity gate.

## Execution

From `slm/`, inside a CUDA-enabled PyTorch environment:

```bash
python -m pip install -e .
IVCSLM_HOURLY_RATE_USD=0.34 ivcslm run-matrix --config configs/ivc_research_14usd.json
```

Set `IVCSLM_HOURLY_RATE_USD` to the provider's actual all-in rate before allocating the GPU; 0.34 above is only an example. The runner accepts a supplied billed-start time, checks its deadline during fitting and evaluation, and refuses to fall back to CPU silently.

The provider workspace must also carry a hard `$14` spending cap or TTL. Accounting inside the application cannot terminate a host process that has already failed, so the ceiling has to exist outside the program too.

Set `IVCSLM_OUTPUT_DIR` to keep full checkpoints on attached storage outside the Git checkout. Curated summaries and tables can then be copied into `research/data/slm/`. Multi-run checkpoints are deliberately not repository artifacts.

## Evidence boundary

The IVC input is the T3 Lipi planning layer, not an authoritative image-normalized corpus. A positive model result can do two things: prioritize source validation, and reject weak nulls. It cannot establish a phonetic value, a sign meaning, a language family, an external anchor, or a translation.

Nothing this harness produces changes the workspace stance: zero accepted translations, phonetic values, sign meanings, language identifications, and external anchors, and exactly one accepted structural finding — the 002-861 / 533-717 terminal-tail result.
