# Research Manifest

Date: 2026-05-24

## Goal

Build a translation system for the Indus Valley Civilization script that is as honest and accurate as the evidence allows, with the moonshot target of approaching the practical reliability of Ancient Egyptian translation.

This is academic decipherment work, not an app build, OCR build, or software-delivery exercise. Scripts and code are tools for audit, statistics, visualization, and reproducibility. They exist to assist reasoning about a lost language and script. They are not the deliverable.

The system must not start by assigning words to signs. It starts by proving what can be known:

- Which sign inventory is being used.
- Which inscriptions are authentic, complete, damaged, or uncertain.
- Which direction each inscription is read.
- Which signs behave as positional operators, terminals, numerals, metrological marks, logograms, or possible phonetic elements.
- Which meanings are forced by archaeological context.
- Which candidate linguistic readings survive controls.

## Why Egyptian Is The Benchmark And The Warning

Ancient Egyptian became reliably readable because scholars had parallel texts such as the Rosetta Stone, a known language in Greek, script continuity through demotic and hieratic, and Coptic as a late Egyptian language bridge. The British Museum describes the Rosetta Stone as a decree written in hieroglyphs, demotic, and Greek, where Greek gave the key to decoding the Egyptian scripts. Britannica likewise notes Champollion used comparison across scripts plus Coptic.

IVC has the opposite profile:

- No known bilingual inscription.
- Very short inscriptions, usually around five signs in the standard literature.
- Disputed sign inventory size.
- Unknown underlying language or languages.
- Incomplete chronological and archaeological coverage.
- Multiple incompatible decipherment traditions, none broadly accepted.

So the benchmark cannot be "produce confident English sentences." The benchmark must be:

1. Reproducibility: independent researchers can rerun the corpus decisions and get the same structural outputs.
2. Calibration: confidence scores match observed uncertainty.
3. Predictive power: the system predicts hidden signs, sign positions, object classes, site distributions, iconographic correlations, and metrological patterns better than strong baselines.
4. Constraint satisfaction: proposed meanings explain multiple inscriptions and do not collapse under counterexamples.
5. Conservative translation: output is layered and bounded until a linguistic bridge exists.

## Claim Levels

Every claim must be tagged:

- `Known`: directly attested in corpus metadata, artifact context, or widely accepted epigraphic observation.
- `Strong`: supported by multiple independent analyses and survives obvious controls.
- `Working`: plausible and useful for experiment design, but not established.
- `Speculative`: interesting, not yet allowed to drive translation.
- `Rejected`: failed a stated test.

## Tooling Posture

Use code only where it sharpens the research:

- Parse and compare corpora.
- Freeze source versions and filtered fields.
- Detect contradictions between transcription layers.
- Run statistical baselines and null models.
- Simulate scarcity on deciphered comparator corpora.
- Preserve reproducible calculations behind published claims.

Do not let the work drift into software goals:

- No app as a default target.
- No OCR as a default target.
- No unit-test or CI/CD ceremony as a proxy for progress.
- No polishing tools while the underlying scholarly claim is weak.
- No treating a working script as evidence unless the result survives source criticism and falsification.

Verification here means scholarly verification first: source provenance, transcription integrity, corpus completeness, negative controls, comparator baselines, and claim calibration. Software checks are acceptable only when they protect those research claims.

## Core Hypothesis Space

We will test, not assume:

- H1: The script encodes spoken language in a logo-syllabic system.
- H2: The script is primarily logographic or semasiographic administrative notation.
- H3: The script is a mixed system with numerical/metrological notation, institutional formulae, and some linguistic elements.
- H4: The symbols are nonlinguistic emblems or status/ritual markers.
- H5: Different artifact classes use different encoding regimes.

The current recommended working hypothesis is H3, because it is compatible with the strongest constraints: short formulaic texts, administrative seal/tablet contexts, statistical structure, iconography, and possible linguistic residues. H3 can lose. That is why it is useful.

## Translation Output Standard

A future system should emit translations like this shape, not like a fake decoded sentence:

```text
Artifact: M-1088
Text: +740-540-002-820+
Reading direction: normalized right-to-left
Structural parse: [terminal/formula marker?] [core sign?] [modifier?] [metrological/object sign?]
Semantic field: administrative seal or commodity/control context, low-medium confidence
Candidate language reading: none accepted
Translation: "Administrative mark involving [unknown core entity/class], possibly connected to [bounded semantic field]."
Confidence: low until the parse predicts held-out metadata and survives controls
```

That looks unsatisfying. Good. It is the difference between scholarship and cosplay.

## Non-Negotiables

- Do not force Sanskrit, Dravidian, Munda, Elamite, or any other language onto the corpus.
- Do not treat a rebus match as evidence unless it beats cross-language false-positive controls.
- Do not use untrusted "decipherment" columns as labels.
- Do not collapse visually distinct signs without an explicit allograph test.
- Do not treat one famous seal as proof of a system.
- Do not report a translation without the inscription ID, corpus source, sign list, reading direction, and uncertainty.
