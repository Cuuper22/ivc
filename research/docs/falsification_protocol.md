# Falsification Protocol

Date: 2026-05-24

## Purpose

Every proposed reading must be easy to attack. If a claim cannot fail, it cannot enter the translation system.

## Universal Claim Template

Every claim must be written as:

```text
Claim:
Scope:
Corpus build:
Evidence used:
Evidence withheld:
Prediction:
Competing explanations:
Null models:
Failure condition:
Status:
```

## Standard Null Models

Use at least one null model for structural claims and at least two for semantic or linguistic claims.

| Null | Description | Kills Claims That |
| --- | --- | --- |
| Frequency-only | Predicts signs by unigram frequency. | Mistake common signs for structure. |
| Position-only | Predicts signs by position distribution. | Mistake fixed slots for meaning. |
| Artifact-class-only | Predicts from object type or site, not signs. | Mistake archaeology metadata for text meaning. |
| Shuffled signs | Keeps lengths and frequencies, randomizes sequence order. | Mistake chance collocations for syntax. |
| Shuffled labels | Keeps signs, randomizes metadata labels. | Mistake noise for semantic association. |
| Synthetic emblem | Generates short formulaic identifiers with rare signs and rigid positions. | Overclaim language from brevity and repetition. |
| Synthetic administration | Generates procedural records with slots, numerals, commodities, and authorities. | Overclaim natural language from structured notation. |
| Cross-language rebus | Tests the same rebus flexibility against unrelated languages. | Overclaim a favorite language family. |

## Claim Types

### C1: Direction Claim

Example: "This inscription should be read right-to-left."

Required evidence:

- Artifact type and seal/sealing logic.
- Sign compression or edge crowding if available.
- Directional allographs if relevant.
- Corpus authority.

Failure:

- The same rule misclassifies high-confidence directions in held-out artifacts.

### C2: Allograph Claim

Example: "Signs X and Y are variants of one grapheme."

Required evidence:

- Visual similarity.
- Direction or mirroring basis.
- Positional distribution similarity.
- Neighbor distribution similarity.
- Effect on model performance.

Failure:

- Merge reduces held-out prediction, erases meaningful positional contrast, or depends on a desired reading.

### C3: Functional-Class Claim

Example: "Sign X is a terminal operator."

Required evidence:

- Positional concentration.
- Stable behavior across sites or artifact classes.
- Collocation constraints.
- Predictive value for held-out sequences.

Failure:

- The sign appears outside the proposed class often enough to require ad hoc exceptions.

### C4: Numerical Claim

Example: "This sign is a numeral or metrological marker."

Required evidence:

- Repetition or ordered variation.
- Co-occurrence with likely commodities, containers, measures, or reverse-side marks.
- Distribution consistent with quantity expression.
- Comparison with known Indus weight systems where relevant.

Failure:

- Proposed values do not predict context, ordering, or artifact measurement better than null models.

### C5: Semantic Field Claim

Example: "This formula marks access control."

Required evidence:

- Artifact context.
- Site or architectural association.
- Duplicate behavior.
- Formula structure.
- Competing semantic fields evaluated.

Failure:

- A generic ownership, name/title, emblem, or administrative-null model explains the same distribution as well or better.

### C6: Language-Family Claim

Example: "This sign uses a Proto-Dravidian rebus."

Required evidence:

- Language prior stated before matching.
- Historical language stage fixed.
- Sound-change flexibility fixed.
- Lexicon fixed.
- Structural slot already established.
- Cross-language and shuffled controls.

Failure:

- The same method produces equally attractive readings in unrelated languages.

### C7: Translation Claim

Example: "This inscription means X."

Required evidence:

- C1 through C6 where applicable.
- Plain English constrained to the lowest unresolved layer.
- Counterexamples listed.
- Confidence calibrated against held-out tests.

Failure:

- The translation contains information not licensed by corpus, structure, semantic class, or accepted linguistic evidence.

## Red-Team Questions

Ask these before accepting any claim:

- What would prove this false?
- Did the hypothesis exist before seeing the favorite example?
- Does it explain boring inscriptions, damaged inscriptions, and duplicates?
- Does it survive site-held-out testing?
- Does it survive artifact-class-held-out testing?
- Does it depend on merging signs that are only merged for this claim?
- Could the same method "decipher" the corpus as another language?
- Does a nonlinguistic administrative system explain it just as well?
- Would the claim still look convincing if the famous seal image were removed?

## Publication Rule

No claim may be written as "the sign means X" until it has a falsification record. Before that, it can only be written as:

```text
Current hypothesis: sign X participates in semantic field Y under conditions Z.
Status: working/speculative.
Known counterexamples: ...
Next falsification test: ...
```

Before publication, run the [claim review checklist](claim_review_checklist.md).
