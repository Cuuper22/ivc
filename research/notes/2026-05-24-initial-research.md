# Initial Research Notes

Date: 2026-05-24

## Workspace State

The workspace started empty except for `.git`. No local corpus, notes, scripts, images, or prior analyses were present.

## Current External Picture

The Indus script remains undeciphered at scholarly-consensus level. The core obstacles recur across sources:

- No known bilingual inscription comparable to the Rosetta Stone.
- Most inscriptions are very short, often summarized around five signs on average in the literature.
- The underlying language is unknown.
- Sign inventory is disputed, with Mahadevan's 417-sign list used often, while later work gives larger inventories depending on variants and allographs.
- There are credible statistical findings of structure, but structure is not translation.
- There are serious critiques of both linguistic and nonlinguistic claims.

## Egyptian Benchmark

Ancient Egyptian is not a fair comparator in resources. It is a fair comparator in epistemic discipline.

Egyptian decipherment benefited from:

- The Rosetta Stone, with the same decree in Greek, demotic, and hieroglyphs.
- Coptic as a late phase of Egyptian.
- Multiple scripts tied to the same language family.
- Large text corpora and later lexicographic infrastructure.

Therefore the IVC system must compete on calibration and reproducibility first, not on fluent translation.

## First Corpus Probe

I inspected the public Yajnadevam `lipi` CSV on 2026-05-24 only as a data-shape probe. It contains columns for inscription metadata, sign strings, and also columns named `sanskrit`, `translation`, and `notes`.

Important: those translation columns are not trusted labels. They are excluded from any serious research use unless the task is specifically to audit that decipherment claim.

Quick shape from that CSV:

- Rows: 5679
- Rows marked complete `Y`: 3673
- Mean text length field after rough numeric parsing: 3.51
- Maximum text length field: 17
- Most common type values include `SEAL:S`, `TAB:B`, `TAB:I`, `POT:T:g`, and `SEAL:R`

This does not replace corpus statistics from M77, CISI, or ICIT. It only confirms that public machine-readable metadata exists and must be aggressively audited.

## Initial Strategic Decision

The first target is not "decode the script." The first target is a calibrated structural translator:

```text
sign sequence -> direction/corpus normalization -> structural parse -> semantic field -> bounded gloss
```

Only after that layer proves predictive power do we allow candidate language readings.

## Working Hypothesis

The most productive starting hypothesis is a mixed administrative system:

- Some signs may be logographic.
- Some may be semasiographic.
- Some may be numerical or metrological.
- Some positions may function grammatically or procedurally.
- Some signs may eventually support rebus or phonetic readings, but this is downstream.

This is not a conclusion. It is a hypothesis designed to survive contact with the most evidence while remaining falsifiable.

## Immediate Next Moves

1. Get a clean corpus into the workspace with provenance and licenses.
2. Build a sign-list crosswalk before doing any analysis.
3. Reproduce published entropy, n-gram, Markov, and positional findings.
4. Build nonlinguistic and administrative baselines strong enough to embarrass weak claims.
5. Run artifact metadata prediction as the first semantic test.
6. Define the first translation output format with confidence and counterexamples.
