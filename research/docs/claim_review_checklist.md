# Claim Review Checklist

Date: 2026-05-24

This checklist is the last gate before any statement enters the translation system. Find the section that matches the type of claim, answer every question, and record one of the four decisions. The questions are deliberately boring: each one closes a hole that a past decipherment attempt has fallen through.

## Corpus Claim

- Is the artifact ID stable?
- Is the source corpus named?
- Is the source version, commit, page, or access date recorded?
- Is the trust tier recorded?
- Is primary image validation required?
- Are damaged, missing, or uncertain signs marked?
- Are claim-bearing columns excluded?

Decision:

```text
accept / revise / reject / blocked
```

## Sign Claim

- Which sign inventory is used?
- Is there a crosswalk to other inventories?
- Is the sign an allograph, split, merge, exact mapping, or unmapped?
- Does the mapping have at least two evidence types?
- Does the mapping depend on a desired meaning?
- Does the mapping survive held-out structural tests?

Decision:

```text
accept / revise / reject / blocked
```

## Direction Claim

- Is the artifact a seal, sealing, tablet, pottery mark, or other object?
- Is the direction inherited from a source or inferred locally?
- Is seal/sealing reversal handled?
- Is sign compression or edge crowding evidence available?
- Are mirrored signs involved?
- Does the direction rule work on held-out examples?

Decision:

```text
accept / revise / reject / blocked
```

## Structural Claim

- What structural role is being claimed?
- Which corpus build supports it?
- Which null model was beaten?
- Does it survive incomplete-record removal?
- Does it survive site-held-out or artifact-class-held-out testing?
- Are counterexamples listed?

Decision:

```text
accept / revise / reject / blocked
```

## Semantic Claim

- What bounded semantic field is being claimed?
- What non-semantic structural evidence supports it?
- What archaeological context supports it?
- Which competing explanations were tested?
- Does a generic administrative, emblem, name/title, or ritual model explain the same evidence?
- Are duplicates and boring examples explained?
- Are counterexamples listed?

Decision:

```text
accept / revise / reject / blocked
```

## Linguistic Claim

- Was the language prior declared before matching?
- Is the historical stage fixed?
- Is the lexicon fixed?
- Are sound-change liberties fixed?
- Was the same method tested against unrelated languages?
- Were shuffled-sign and shuffled-meaning controls run?
- Does it explain a class of inscriptions rather than one attractive example?

Decision:

```text
accept / revise / reject / blocked
```

## Translation Claim

- Does the plain English say more than the evidence permits?
- Is confidence reported by layer?
- Are competing explanations shown?
- Are counterexamples shown?
- Is the next falsification test shown?
- Would the output still be honest if the user only read the plain English?

Decision:

```text
accept / revise / reject / blocked
```

## Automatic Rejection Conditions

Some failures need no discussion. Reject immediately if:

- It uses quarantined translation labels as evidence.
- It assigns a language without declared priors and controls.
- It merges signs only to make a reading work.
- It cites a famous seal while ignoring the rest of the corpus.
- It calls synthetic data evidence for ancient meaning.
- It emits a confident English sentence without a layered evidence object.

## Minimum Public Claim Standard

A public claim must include:

```text
claim:
scope:
corpus build:
trust tier:
evidence:
null models:
counterexamples:
confidence:
next falsification:
```

Without that, it is not a research claim. It is a hunch.
