# 032-002-861 X-Before-240 Bridge-Lock Null

Date: 2026-05-29

## Question

This note records a null-model test: we shuffle the data at random many times and see how often chance alone reproduces the pattern we found. The subject is the sign `603` (signs in this corpus are numeric IDs).

Two facts about `603` are on trial. It sits in the X slot of rows shaped `...-X-240-...`, and the material after `240` in those rows — the "subframe" — is always the same. That is the "bridge-lock": `603` locked to one subframe, while also bridging into a second context as the first sign of a tail after `002-861`.

The question: is the current `603` pattern rare enough to promote, or is it a small-count bridge-lock pattern that random X-label placement can reproduce?

## Method

The 95 X-before-`240` rows keep their after-`240` subframes fixed. The observed X-sign multiset is shuffled across those rows for 20,000 iterations, preserving sign counts and after-`240` subframe sizes but breaking sign-to-subframe association. Post-`002-861` tail-initial counts stay attached to sign labels. If shuffled data often makes a lock like this, the observed lock is cheap.

This is a distributional adversary — a hostile check on the numbers alone — not a source or value test.

## Observed

- `603` is locked to `060 692` inside X-before-`240`.
- `603` is a non-background post-`002-861` bridge sign — that is, not one of the very common filler signs that turn up almost everywhere.
- `603` has 3 X-before-`240` rows and 3 post-`002-861` tail-initial rows.

## Null Results

- `P(shuffled 603 locked anywhere) = 0.040000`
- `P(shuffled 603 locked specifically to 060 692) = 0.000400`
- `P(any non-background bridge sign locked) = 0.040000`
- `P(any low-frequency non-background bridge sign locked) = 0.040000`

## Decision

Status: `bridge_lock_pattern_is_weak_to_moderate_distributional_support_not_a_promotion`.

- The exact `603 locked to 060 692` pattern is uncommon under row-label shuffle.
- The broader class of any low-frequency non-background bridge sign locked to one after-240 subframe appears at about the 4% level, so the pattern is real pressure but still small-count and model-sensitive.
- Therefore this null gives weak-to-moderate support to the bridge-lock pattern without promoting `603` to value evidence.
- The next promotion still depends on source graphic identity or an independent second X-before-240 context for `603`.

Accepted values, phonetics, language identity, translations, and graphic identity remain 0/unaccepted.
