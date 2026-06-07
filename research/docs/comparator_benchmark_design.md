# Comparator Benchmark Design

Date: 2026-05-24

## Purpose

The phrase "as accurate as Ancient Egyptian translations" cannot mean "pretend IVC has a Rosetta Stone." It means using known deciphered systems to estimate what can and cannot be recovered under Indus-like scarcity.

## Benchmark Principle

Use scripts/languages we can already read, then blindfold ourselves until the conditions resemble IVC:

- No bilingual key.
- Very short inscriptions.
- Small corpus slices.
- Damaged or missing signs.
- Unknown or hidden lexical readings.
- Metadata preserved only where IVC metadata is also available.

If a method cannot recover a known system under these artificial constraints, it cannot be trusted on IVC.

## Comparator 1: Egyptian/Coptic Continuity

Source lead:

- Coptic Scriptorium corpora.

Use:

- Test what linguistic continuity can recover when the late language is known.
- Compare full-continuity vs no-continuity settings.

Blindfold settings:

1. Full Coptic access: model can use lexical and morphological continuity.
2. Structure-only: model sees token sequences and metadata, but no meanings.
3. Indus-like: short segments only, no parallel text, no lexicon.

Expected lesson:

- Egyptian accuracy is not magic. It is infrastructure: bilingual text, continuity, corpora, grammar, dictionary, and correction loops.

Current acquisition note:

- [Known-script scarcity comparator acquisition audit](known_script_scarcity_comparator_acquisition_audit.md) keeps Coptic SCRIPTORIUM as the continuity upper bound. It should be used to measure how much known-language continuity helps, not as the first IVC-like scarcity baseline.

## Comparator 2: Linear B

Source lead:

- Zenodo Linear B series D dataset.

Use:

- Known logo-syllabic administrative script comparator.
- Test masked sign prediction and structural recovery.

Blindfold settings:

1. Preserve sign strings and document class.
2. Hide Mycenaean Greek readings.
3. Downsample to Indus-like lengths.
4. Remove obvious repeated duplicates in one condition and keep them in another.

Output tasks:

- Recover positional classes.
- Predict missing signs.
- Identify ideogram/numerical-like behavior.
- Estimate how much semantic structure survives without language.

Expected lesson:

- Even in a deciphered system, short administrative records may support structure before prose-like translation.

Current acquisition note:

- The known-script scarcity audit selects Linear B Series D as the first comparator to run.
- The clean first pass should use only the first 513 real Series D sequences from the Zenodo file. The 725 augmented rows and 1,327 duplicate rows should stay excluded unless the experiment explicitly tests augmentation or duplicate effects.
- The first baseline has now run in [Linear B Series D scarcity baseline](linear_b_series_d_scarcity_baseline.md): hidden-reading `sign_tokens` reach bidirectional top-1 `0.470200` on all clean rows and `0.435897` after the current IVC p95 length cap of 8 signs.
- The same file's source-provided gapped rows give a harder missing-sign ceiling. Under sequence-leave-one-out, bidirectional top-1 is `0.294347` all-lengths and `0.294314` after the IVC p95 length cap, with median rank `3`.

## Comparator 3: Sumerian Administrative Corpus

Source lead:

- SumTablets.

Use:

- Large ancient administrative corpus with glyph and transliteration fields.
- Create tiny Indus-like samples from a rich known system.

Blindfold settings:

1. Use glyphs only.
2. Hide transliterations.
3. Sample short administrative sequences.
4. Compare with and without metadata such as period and genre.

Output tasks:

- Text length distribution.
- Repeated formulae.
- Hapax rate.
- Positional rigidity.
- Metadata prediction.

Expected lesson:

- Administrative writing can look rigid and formulaic without being nonlinguistic.

Current acquisition note:

- The known-script scarcity audit keeps SumTablets as the large administrative comparator after Linear B. Before use, pin the Hugging Face dataset revision and hide `transliteration` labels in IVC-like conditions.

## Comparator 4: Synthetic Nonlinguistic Baselines

Source lead:

- Nair 2026 preprint concept, plus local generators.

Use:

- Test against emblem and administrative systems that are intentionally strong, not strawmen.

Baseline families:

- Heraldic/emblem generator.
- Administrative code generator.
- Mixed generator with numerical, commodity, issuer, and terminal slots.
- Shuffled-real corpus.

Output tasks:

- Compare IVC against systems designed to fool shallow language tests.

Expected lesson:

- If IVC only beats silly baselines, we have learned almost nothing.

Current first scout:

- [Lipi synthetic comparator baseline](lipi_synthetic_comparator_baseline.md) runs four local controls on the filtered `lipi` numeric-clean planning layer: length-frequency shuffle, edge-position shuffle, edge-frame template shuffle, and position-slot shuffle.
- The scout shows why weak baselines are dangerous. Edge/slot-preserving controls nearly reproduce stored-order asymmetry.
- The same controls do not reproduce duplicate-collapsed bidirectional masked-sign prediction in the first run. Observed top-1 is 0.325865; null means range from 0.098096 to 0.143747.
- [Lipi structured null comparator](lipi_structured_null_comparator.md) adds duplicate-calibrated administrative and emblem code generators. These controls exceed observed bidirectional top-1, showing that local context prediction is also not a standalone language diagnostic.
- [Lipi metadata prediction probe](lipi_metadata_prediction_probe.md) shows that type/site/region prediction can be matched or nearly matched by a mixed admin-emblem null, while inscription class prediction remains above the tested structured nulls in the first scout.
- [Lipi stratified class probe](lipi_stratified_class_probe.md) shows that class prediction remains above structured nulls within eligible site, type, and type-site strata.
- This is not yet a final comparator because the generators are artificial, not known-script or archaeology-grounded emblem or administrative systems.

## Metrics Shared Across Comparators

- Length distribution.
- Type-token ratio.
- Hapax rate.
- Duplicate sequence rate.
- Conditional entropy.
- Positional entropy by sign.
- Bigram and trigram predictability.
- Masked sign prediction.
- Metadata prediction.
- Robustness under downsampling.
- Robustness under artifact-class holdout.

## Translation Ceiling Estimate

The comparator benchmark should produce a ceiling table:

| Condition | Corpus Validity | Graphemic | Structural | Semantic | Linguistic | Translation |
| --- | --- | --- | --- | --- | --- | --- |
| Full Egyptian-style evidence | High | High | High | High | High | High |
| Known script, no bilingual | High | High | Medium-high | Medium | Low-medium | Low |
| Short administrative corpus, known language hidden | High | High | Medium | Low-medium | Low | Very low |
| IVC current evidence | Pending | Pending | Unknown until replicated | Not yet admissible | Not yet admissible | Not admissible |

## Pass Condition For IVC Research

An IVC method is worth keeping if it does at least one of these:

- Recovers structural facts in a known comparator under Indus-like scarcity.
- Predicts held-out IVC signs or metadata better than strong nulls.
- Reduces uncertainty without creating fake semantic certainty.
- Produces calibrated "unknown" outputs where evidence is insufficient.

That last one matters. A system that knows when not to translate is already ahead of most decipherment claims.

## Next Comparator Experiment

```text
E5.3a Linear B Series D Scarcity Baseline, second pass
```

Minimum output:

- Improve or replace the transliteration-derived `sign_tokens` split with a citable Linear B sign-ID tokenization.
- Keep the existing Zenodo source manifest, clean row-range inventory, Indus-like length cap, structural-only scorecard, source-provided gapped test, and ceiling statement as the first-pass baseline.
- Add SumTablets as the next administrative comparator after revision pinning and transliteration-label hiding.
