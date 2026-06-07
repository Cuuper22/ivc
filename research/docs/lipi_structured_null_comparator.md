# Lipi Structured Null Comparator

Date: 2026-05-29

## Purpose

This experiment asks whether explicit nonlinguistic code systems can reproduce or exceed the duplicate-collapsed `lipi` structural signal.

It follows the [Lipi synthetic comparator baseline](lipi_synthetic_comparator_baseline.md). The earlier nulls preserved length, frequency, edge position, edge frames, and length-position slots. Those controls did not include explicit local dependencies. This run adds formula-like and administrative-code dependencies.

This is a hostile falsifier. If a nonlinguistic system can match a metric, that metric cannot stand alone as decipherment evidence.

It does not treat `lipi` as authoritative. It does not assume accepted reading order. It does not assign meanings, sign values, phonetics, language identity, or translations.

## Local Artifacts

```text
data/open_prototype/tools/lipi_structured_null_comparator.mjs
data/open_prototype/reports/lipi_structured_null_iterations.csv
data/open_prototype/reports/lipi_structured_null_summary.csv
data/open_prototype/reports/lipi_structured_null_summary.json
```

Source file:

```text
data/open_prototype/reports/lipi_scope_rows.csv
```

Scope:

```text
readiness_bucket = lipi_numeric_clean_candidate
source_rows = 2883
observed_exact_collapsed_families = 1798
iterations_per_control = 20
seed_base = 20260524
```

All structured nulls are duplicate calibrated:

```text
unique_sequences: 1798
exact_duplicate_row_share: 0.468609
top_sequence_count: 117
```

That prevents the nulls from winning merely by being much more duplicated than the observed layer.

## Controls

The four controls are:

- Duplicate-matched position slots: preserves the observed duplicate-weight and length distribution, but samples every slot independently from length-position pools.
- Administrative register code: duplicate-matched issuer, office, commodity, quantity, qualifier, and terminal dependencies.
- Emblem formula code: duplicate-matched clan, rank, device, variant, and terminal dependencies.
- Mixed admin-emblem code: tablet-like rows use administrative dependencies, seal-like rows use emblem dependencies, and short pottery rows use positional slots.

These are not claims about what IVC is. They are deliberately strong nonlinguistic systems designed to see which metrics can be faked.

## Main Result

Means below are over 20 deterministic iterations per control.

| Control | Stored Win Share | Bidirectional Top-1 | Bidirectional Top-5 |
| --- | ---: | ---: | ---: |
| observed `lipi` | 0.948276 | 0.325865 | 0.567828 |
| duplicate-matched position slots | 0.949638 | 0.145622 | 0.315136 |
| administrative register code | 0.990823 | 0.472924 | 0.689838 |
| emblem formula code | 0.987236 | 0.443351 | 0.692353 |
| mixed admin-emblem code | 0.982258 | 0.415069 | 0.662652 |

The duplicate-matched position-slot control reproduces stored-order asymmetry but not bidirectional context. This confirms that simple positional rigidity is not enough to reproduce the context signal.

The administrative, emblem, and mixed structured controls exceed observed bidirectional top-1 and top-5. That is a real falsification of bidirectional masked-sign prediction as a standalone language-like diagnostic.

## Simple Model Pattern

| Control | Frequency Top-1 | Position Top-1 | Length-Position Top-1 | Bidirectional Top-1 |
| --- | ---: | ---: | ---: | ---: |
| observed `lipi` | 0.107769 | 0.151120 | 0.154652 | 0.325865 |
| duplicate-matched position slots | 0.108433 | 0.150280 | 0.184200 | 0.145622 |
| administrative register code | 0.074269 | 0.172863 | 0.242407 | 0.472924 |
| emblem formula code | 0.100244 | 0.213316 | 0.253209 | 0.443351 |
| mixed admin-emblem code | 0.083475 | 0.184462 | 0.209888 | 0.415069 |

The structured controls are not subtle. They create stronger local dependencies and more rigid slot behavior than the observed layer. That does not make the observed layer nonlinguistic; it shows that local dependency metrics need tougher companion tests.

## Interpretation

This comparator changes the evidence boundary:

- Stored-order asymmetry is not diagnostic.
- Length-position and frequency baselines are not enough.
- Duplicate-collapsed bidirectional masked-sign prediction is not diagnostic by itself either, because explicit nonlinguistic administrative/emblem code can exceed it.
- The useful target is now narrower: find structural behavior that survives strong nonlinguistic code controls and also predicts independent metadata, artifact-class behavior, sign-class stability, or known-script comparators.

The result supports only this claim:

```text
In the filtered `lipi` numeric-clean planning layer, duplicate-collapsed bidirectional context is stronger than independent slot shuffles but can be exceeded by duplicate-calibrated nonlinguistic administrative and emblem formula generators. Therefore bidirectional masked-sign accuracy is not standalone evidence for language or translation.
```

It does not support:

- Accepted reading direction.
- Accepted sign segmentation.
- Sign meanings.
- Semantic slots.
- Phonetic values.
- Language identity.
- Translation.
- A conclusion that IVC is nonlinguistic.

## Limits

- `lipi` remains a T3 planning source.
- The controls are artificial and deliberately strong.
- The administrative and emblem generators are not archaeological models.
- The current rerun uses 20 deterministic iterations per control, enough for the Vector 2 boundary note but still not a final benchmark against real-world nonlinguistic corpora.
- A null beating a metric weakens that metric; it does not identify the real IVC system.

## Next Falsification

The next test should stop asking whether one metric is high and start asking whether a whole profile is hard to fake:

- Compare the observed layer and structured nulls on metadata prediction for artifact type, site, region, material, completeness, and direction.
- Run held-out artifact-class and site tests against the structured nulls.
- Add real known-script comparators under Indus-like scarcity, especially Linear B and Sumerian administrative records.
- Test whether learned sign classes remain stable under bootstrap, artifact-class splits, and image-validated corpora.
