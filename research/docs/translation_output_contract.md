# Translation Output Contract

Date: 2026-05-24

## Purpose

This contract defines what a future IVC "translation" output is allowed to say. It prevents the system from turning weak evidence into fluent nonsense.

## Output Object

Every output must be a layered object:

```text
artifact_id:
source_corpus:
source_version:
trust_tier:
primary_image_checked:
raw_text:
normalized_text:
reading_direction:
direction_basis:
sign_list_authority:
allograph_policy:
damage_or_uncertainty:
structural_parse:
semantic_field:
linguistic_candidate:
plain_english:
confidence_by_layer:
competing_explanations:
counterexamples:
next_falsification_test:
release_status:
```

## Required Layer Behavior

### Corpus Layer

If corpus status is uncertain:

```text
plain_english: "No translation. Corpus validation pending."
release_status: "blocked_at_corpus_layer"
```

### Graphemic Layer

If sign mapping is uncertain:

```text
plain_english: "No translation. Sign crosswalk unresolved."
release_status: "blocked_at_graphemic_layer"
```

### Structural Layer

If only structure is supported:

```text
plain_english: "Formalized inscription with [known structural roles], but no accepted semantic reading."
release_status: "structural_only"
```

### Semantic Layer

If bounded semantics are supported:

```text
plain_english: "Likely [semantic field] record involving an unknown core class."
release_status: "semantic_bounded"
```

### Linguistic Layer

If a language candidate exists but is not accepted:

```text
plain_english: "Candidate [language family] reading exists, but remains unaccepted and fails/pending controls."
release_status: "linguistic_candidate_only"
```

### Translation Layer

Translation-grade output is only permitted if:

- Corpus source is validated.
- Sign segmentation and direction are validated.
- Structural parse survives nulls.
- Semantic field survives competing models.
- Linguistic reading survives false-positive controls.
- Confidence is calibrated against held-out tests.

Current status for IVC:

```text
Translation-grade output is not currently admissible.
```

## Example: Honest Output

```text
artifact_id: M-1088
source_corpus: ICIT example page
source_version: checked 2026-05-24
trust_tier: T1 literature/web reference, not local corpus
primary_image_checked: no
raw_text: +740-540-002-820+
normalized_text: unresolved
reading_direction: unresolved locally
direction_basis: source page gives sign sequence only
sign_list_authority: numeric ICIT-style signs
allograph_policy: none
damage_or_uncertainty: unknown
structural_parse: not attempted
semantic_field: not admissible
linguistic_candidate: none
plain_english: "No translation. Corpus and sign-list validation pending."
confidence_by_layer: corpus 1, graphemic 0, structural 0, semantic 0, linguistic 0, translation 0
competing_explanations: not evaluated
counterexamples: not evaluated
next_falsification_test: acquire source record and map signs across at least one other corpus
release_status: blocked_at_corpus_layer
```

## Example: Forbidden Output

```text
M-1088 means "merchant of the shining fish."
```

Why forbidden:

- No validated corpus layer.
- No allograph policy.
- No semantic field test.
- No language prior.
- No false-positive controls.
- No counterexamples.

## Human-Facing Rule

If the honest answer is "unknown," say unknown. The project is a moonshot because it refuses to win by cheating.
