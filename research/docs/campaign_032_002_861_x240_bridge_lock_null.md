# 032-002-861 X-Before-240 Bridge-Lock Null

Date: 2026-05-29

## Question

Is the current `603` pattern rare enough to promote, or is it a small-count bridge-lock pattern that random X-label placement can reproduce?

## Method

The 95 X-before-`240` rows keep their after-`240` subframes fixed. The observed X-sign multiset is shuffled across those rows for 20,000 iterations, preserving sign counts and after-`240` subframe sizes but breaking sign-to-subframe association. Post-`002-861` tail-initial counts stay attached to sign labels.

This is a distributional adversary, not a source or value test.

## Observed

- `603` is locked to `060 692` inside X-before-`240`.
- `603` is a non-background post-`002-861` bridge sign.
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
