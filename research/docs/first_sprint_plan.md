# First Sprint Plan

Date: 2026-05-24

## Sprint Objective

Create the first evidence-bearing research package for IVC translation without making any translation claim.

The sprint succeeds only if it produces a frozen, auditable working corpus layer and reproduces at least one structural baseline against null models. It does not succeed by producing a fluent reading.

## Sprint Boundary

In scope:

- Corpus provenance.
- Sign-string normalization policy.
- Corpus overlap checks.
- First structural baselines.
- First null models.
- Comparator design against known deciphered scripts under artificial scarcity.
- Lightweight code or scripts when they directly support those research tasks.

Out of scope:

- Building an app.
- Building OCR.
- Creating a software product.
- Unit-test, CI/CD, packaging, or deployment work as an end in itself.
- Assigning sign meanings.
- Assigning phonetic values.
- Claiming Dravidian, Sanskrit, Munda, Elamite, or any other language.
- Training a translation model.
- Treating generated sequences as evidence.

## Deliverables

### D1: Source Evidence Ledger

File: [evidence_ledger.md](evidence_ledger.md)

Acceptance criteria:

- Every source has a trust tier.
- Every source has a current access status.
- Claim-bearing or synthetic sources are explicitly quarantined.
- Any contradiction between a source page and paper comment is flagged.

### D2: Frozen Open Prototype Corpus Definition

Corpus name:

```text
ivc-corpus-2026-05-24-open-prototype
```

Reference:

- [Corpus freeze manifest](corpus_freeze_manifest.md)

Inputs:

- `mayig/indus-valley-script-corpus` pinned to commit `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`.
- Yajnadevam `lipi` CSV metadata/sign fields only, with `sanskrit`, `translation`, and `notes` removed.

Acceptance criteria:

- The prototype corpus is marked as non-authoritative.
- It records source commit or source URL.
- It records excluded columns and why.
- It records that primary image validation is pending.

### D3: Corpus Crosswalk Questions

Questions to answer before analysis:

1. Which `mayig` artifact IDs overlap with `lipi`/CISI IDs?
2. Do sign strings agree where the same artifact appears?
3. Does `mayig` Parpola-style `P###` notation map cleanly to `lipi` numeric signs?
4. Which source preserves allograph features better?
5. Which source preserves archaeological metadata better?

Acceptance criteria:

- Each overlap is classified as exact, equivalent after normalization, conflict, missing, or impossible to compare.
- Sign mappings follow the [sign crosswalk protocol](sign_crosswalk_protocol.md).

Current result:

- [Open prototype results](open_prototype_results.md) materialized the first artifact-ID overlap probe.
- The probe found 179 `mayig` records matching 179 filtered `lipi` rows by CISI-style ID.
- 150 records matched by rough sign count; 29 need manual audit.
- [Mismatch audit](mismatch_audit.md) refines that into 138 clean pre-crosswalk candidates, 12 count-matching sensitivity-flag candidates, and 29 manual-review rows.
- [Structural readiness probe](structural_readiness_probe.md) found that the 138 clean rows contain an order signal strong enough to justify the next controlled direction/order baseline.
- [Direction and order baseline](direction_order_baseline.md) found that observed order beats reversed and shuffled controls, survives removing `740` and `002`, and that bidirectional context predicts masked signs better than frequency and position baselines.

### D4: First Structural Replication

Target:

- Direction and sign-order structure only.

Minimum tests:

- Unigram frequency baseline.
- Position-only baseline.
- Bigram or Markov baseline.
- Shuffled-sequence null.

Acceptance criteria:

- Report masked-sign prediction accuracy by text position and length bucket.
- Report whether results survive removing incomplete inscriptions.
- Report whether results survive site-held-out or artifact-class-held-out splits if metadata supports it.

Current prototype status:

- The clean subset reports masked-sign accuracy by position class and length bucket.
- The order signal survives removing `740` and `002`.
- Site-held-out and artifact-class-held-out splits are not possible inside the clean subset because all 138 rows are Mohenjo-daro `SEAL:S`.

### D5: Scarcity Comparator Design

Comparator candidates:

- Coptic Scriptorium: Egyptian-language continuity comparator.
- Linear B: deciphered logo-syllabic comparator.
- SumTablets: large ancient administrative corpus comparator.

Acceptance criteria:

- Each comparator is downsampled to Indus-like constraints before comparison.
- Parallel texts and known translations are hidden for the scarcity test.
- The output task is structural recovery first, not full translation.

## Sprint Experiments

### S1.1 Corpus Shape Audit

Question:

What does each usable source contain, and what must be excluded?

Evidence:

- Row/file counts.
- Field lists.
- Source version.
- Trust tier.

Failure condition:

- Any source enters the working corpus without a version or quarantine status.

### S1.2 Overlap Audit

Question:

Can the open WIP corpus and the broad metadata CSV agree on the same artifacts?

Evidence:

- Matched artifact IDs.
- Matched or conflicting sign sequences.
- Mismatched direction or completion flags.
- Sensitivity flags for unknown signs, boundary fragments, slash compounds, and source-level sign-count disagreements.

Failure condition:

- We cannot identify enough overlaps to use one source as a check on the other.
- The clean overlap subset collapses after manual collation or image-level validation.

### S1.3 Direction/Order Baseline

Question:

Can a sequence model recover known or assumed direction/order better than nulls?

Evidence:

- Log likelihood of original sequence vs reversed or shuffled sequence.
- Masked sign prediction over positions.
- Direction performance split by seals, tablets, and pottery if possible.
- Sensitivity check after removing very frequent edge signs.

Failure condition:

- Bigram/Markov model does not outperform frequency and position-only baselines.
- The observed order advantage disappears under length-bucket controls or edge-sign removal.

### S1.4 Allograph Sensitivity

Question:

How much do sign inventory choices change the structural signal?

Evidence:

- Compare raw signs, allograph-merged signs, and allograph-split signs.
- Measure effect on vocabulary size, hapax rate, entropy, and masked prediction.

Failure condition:

- A claimed structural result exists only under one unexplained allograph policy.

### S1.5 Nonlinguistic Baseline Scorecard

Question:

Does IVC look more like a linguistic, emblematic, administrative, or mixed system under strong baselines?

Evidence:

- Text length distribution.
- Repeated formula rate.
- Hapax rate.
- Positional rigidity.
- Conditional entropy.

Failure condition:

- The conclusion depends on weak toy baselines instead of strong emblem/admin controls.

## Output Format For Sprint Results

Every result should be reported as:

```text
Experiment:
Corpus build:
Source tiers:
Excluded data:
Method:
Null models:
Result:
Counterresult:
Interpretation:
Next falsification:
```

## Stop Conditions

Pause semantic work if:

- Corpus overlap is too poor.
- Primary corpus access is blocked.
- Sign inventory mappings are unstable.
- Translation-bearing columns leak into analysis.
- Structural baselines fail to beat nulls.

None of those stop the project. They stop overclaiming.
