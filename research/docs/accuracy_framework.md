# Accuracy Framework

Date: 2026-05-24

## Purpose

The goal is a translation system whose reliability can eventually stand beside mature Ancient Egyptian translation. Because the evidence conditions are radically worse for IVC, "accuracy" must be split into layers. A system can be highly accurate at sign normalization and still have no right to emit a sentence in English.

This framework measures decipherment progress, not software maturity. Code may assist the work, but an app, OCR pipeline, test suite, deployment setup, or clean engineering pipeline is not evidence that the script has been understood.

## Accuracy Layers

### A0: Corpus Accuracy

Question: Is the system reading the right object, from the right source, with the right uncertainty flags?

Required evidence:

- Stable corpus ID.
- Source corpus and version.
- Artifact type, site, material, and preservation status.
- Image or publication reference when available.
- Damage, missing signs, direction uncertainty, and suspected modern/fake status.

Acceptable output:

```text
M-1088, source: CISI/ICIT crosswalk pending, complete: unknown, text: +740-540-002-820+
```

Not acceptable:

```text
This seal says...
```

### A1: Graphemic Accuracy

Question: Are signs segmented, normalized, and crosswalked correctly?

Metrics:

- Agreement with sign-list authority.
- Crosswalk consistency between Mahadevan, Parpola, Wells/Fuls, and any open dataset.
- Explicit allograph status: distinct, merged, possible allograph, rejected merge.
- Direction-specific rendering.

Pass gate:

- Any proposed sign merge must improve or preserve held-out structural prediction and be visually/distributionally justified.

### A2: Structural Accuracy

Question: Does the system identify how a sequence works internally?

Targets:

- Direction.
- Position class.
- Terminal and pre-terminal behavior.
- Core sign behavior.
- Numeral and metrological behavior.
- Connector behavior.
- Artifact-class grammar.

Metrics:

- Masked sign prediction against frequency-only baseline.
- Position prediction on held-out inscriptions.
- Artifact-class split performance.
- Bootstrap stability of sign classes.

Pass gate:

- A structural parse must predict something not used to create it: held-out sign, position, artifact class, site, iconographic class, or metrological context.

Current prototype status:

- The open prototype has A2-only structural evidence on a narrow Mohenjo-daro seal subset.
- It has preliminary positional classes for signs such as `740/P324`, `002/P122`, `220/P050`, `032/P145`, `817/861/P385`, and `390/P086`.
- It has a first formula-pattern probe showing directional `I...T` edge scaffolds, but exact formula recurrence is weak.
- It has a formula-variant probe producing near-duplicate and single-slot review queues, with a first null model showing that most of the queue is explained by edge-position structure.
- It has a sensitivity-row stress test showing that flagged count-matches do not cleanly extend the strict formula scaffold.
- It has a metadata-scope audit showing the current open prototype is limited to unicorn seal descriptions.
- It has a broader filtered `lipi` scope survey that can propose artifact-class and site split baselines, but this remains a T3 planning layer rather than authoritative corpus evidence.
- It has a broad filtered `lipi` order baseline showing stored-order and masked-sign structure across artifact/site splits, including held-out tests, with duplicate-heavy rows flagged as a major inflation risk.
- It has an exact-duplicate-collapsed broad `lipi` baseline showing stored-order structure survives collapse, while exact-sign prediction weakens and remains formula-sensitive.
- It has a leakage-controlled held-out `lipi` baseline showing selected held-out exact-sign scores remain above simple baselines after exact train/test sequence overlap is removed, but this still does not control near-duplicate formula families.
- It has a high-frequency edge-removal `lipi` baseline showing edge signs carry a large part of the signal, but top-10 edge removal still leaves duplicate-collapsed stored-order and masked-sign prediction above simple baselines.
- It has a formula-family downweighting `lipi` baseline showing shared edge frames and one-edit neighborhoods do not erase the residual structural signal, including after top-10 edge removal; this is a blunt anti-template stress test, not a natural formula inventory.
- These classes are not semantic categories and do not permit translation.

### A3: Semantic Accuracy

Question: Can signs or formulae be assigned bounded semantic fields?

Allowed semantic fields:

- Number.
- Measure or metrological tier.
- Commodity or material class.
- Craft or institutional process.
- Access, license, tax, ownership, ritual, or administrative role.
- Proper name or title, but only after competing administrative and emblem models fail.

Metrics:

- Metadata prediction.
- Duplicate-inscription behavior.
- Site and artifact-type generalization.
- Iconography association surviving controls.
- Ability to explain counterexamples without ad hoc exceptions.

Pass gate:

- A semantic claim must beat at least two competing explanations and one strong null model.

### A4: Linguistic Accuracy

Question: Is there evidence that a sign or sequence maps to a language?

Candidate language readings are downstream. They require:

- Pre-declared language prior.
- Phonological constraints fixed before matching.
- Dictionary and historical stage fixed before matching.
- Cross-language false-positive controls.
- Shuffled-sign and shuffled-meaning controls.
- Explanation of multiple inscriptions, not one emblematic seal.

Pass gate:

- A reading must explain a class of structurally similar inscriptions and fail to appear just as easily in unrelated languages.

### A5: Translation Accuracy

Question: Can a human use the output as a translation?

For IVC, this is not currently achievable at Ancient Egyptian levels. The system may still emit a bounded translation object:

```text
Translation status: structural-semantic only.
Plain English: "Formalized administrative mark involving an unknown core class and a probable terminal/operator sign."
Rejected: no accepted linguistic reading.
Confidence: low semantic, medium structural, pending corpus validation.
```

Pass gate:

- The plain English must not contain more semantic information than the evidence layer permits.

## Egyptian Comparator

Ancient Egyptian translation accuracy rests on evidence IVC does not have:

- Parallel text support, especially the Rosetta Stone.
- Readable Greek in the same decree.
- Coptic continuity.
- Large corpora.
- Dictionaries, grammars, and two centuries of correction.

So the fair test is not "can IVC produce Egypt-style prose now?" The fair test is:

1. If Egyptian, Sumerian, or Linear B data are artificially reduced to Indus-like conditions, what accuracy remains?
2. Which tasks remain possible under short inscriptions and no bilingual key?
3. Does the IVC system reach that scarcity-adjusted ceiling?

Current comparator acquisition status:

- [Known-script scarcity comparator acquisition audit](known_script_scarcity_comparator_acquisition_audit.md) chooses Linear B Series D as the first known-script scarcity baseline.
- Coptic SCRIPTORIUM is kept as an Egyptian/Coptic continuity upper bound because it has machine-readable corpora, citable current data, and annotation-quality metadata, but it gives continuity evidence IVC does not have.
- SumTablets is kept as the large administrative comparator after dataset revision pinning and transliteration-label hiding.
- [Linear B Series D scarcity baseline](linear_b_series_d_scarcity_baseline.md) has run as the first known-script scarcity baseline. Using hidden-reading `sign_tokens`, bidirectional masked-sign top-1 is `0.470200` on the 513 clean real rows and `0.435897` after the current IVC p95 length cap of 8 signs. The stricter source-provided gapped test drops the sequence-leave-one-out ceiling to `0.294347` all-lengths and `0.294314` under the IVC p95 length cap, with median rank `3`. This is an A2 structural ceiling, not semantic or translation evidence.

## Confidence Scale

| Level | Meaning | Output Permission |
| --- | --- | --- |
| 0 | Unchecked | Store only, no interpretation. |
| 1 | Corpus-valid | Corpus metadata and sign string may be shown. |
| 2 | Graphemic-valid | Normalized sign sequence may be shown. |
| 3 | Structural-valid | Structural parse may be shown. |
| 4 | Semantic-bounded | Semantic field may be shown with alternatives. |
| 5 | Linguistic-candidate | Candidate reading may be shown as unaccepted. |
| 6 | Translation-grade | Human translation may be shown. Not currently expected for IVC. |

## Release Rule

Any public-facing output must show the lowest confidence layer that remains unresolved. If corpus validity is uncertain, the system cannot hide that under a polished semantic reading.

Operational checks:

- [Translation output contract](translation_output_contract.md)
- [Claim review checklist](claim_review_checklist.md)
