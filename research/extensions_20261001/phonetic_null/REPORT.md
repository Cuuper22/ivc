# phonetic_null: do the Sanskrit-dictionary key fits beat chance?

**Question.** Do the whole-inscription dictionary fits in `research/docs/archive/decoding_followup_20260907.md` §1 beat chance? Those fits report, for example, 54/146 training and 4/56 held-out matches for the unexpanded run.

**Blocker.** The optimizer that produced those numbers is not in the repo, in the working tree or anywhere in git history. The report says it lives in a "downloadable research packet" that was never committed. Only the report and `research/data/decoding_followup_20260907/summary.json` exist. **The September 7 phonetic results therefore cannot be reproduced from this repository.** The dictionary itself is present: Monier-Williams, 192,482 headwords, matching the report.

**Method.** This is an independent re-implementation of the method as described. It does not reproduce the repo's numbers. Every condition uses the same optimizer, budget and seeds.

- **Dictionary.** Headwords use the same extraction as `run_completion_d.py`. That gives 7,231 syllable-like chunks; each word is split after each vowel, and any final consonants stay on the last chunk.
- **Lines.** Distinct strict lines of 2–10 signs drawn from the 40 most frequent signs plus the fish family: 271 lines and 46 signs. The report had 202, because I could not reproduce its seal-only filter.
- **Key.** An injective sign → chunk map. A line matches if its chunk sequence is exactly a headword. The key is selected on training score only.
- **Search.** Simulated annealing: 6 restarts × 40,000 proposals, with 8 seeds and an 80/20 split whose indices are the same in every condition. This budget is smaller than the repo's, and the reduction applies equally to real and control data.
- **Controls.**
  - Sign order permuted within each line.
  - All sign tokens shuffled across lines, keeping line lengths.
  - Independently drawn signs with the real lengths and frequencies.
  - Order-1 and order-2 Markov corpora. These keep the real sign-sequence repetition; the shuffles destroy it.

**Result.** Mean ± sd over 8 seeds. "Bigram overlap" is the share of sign pairs in held-out lines that also appear in training lines.

| Condition | Train match rate | Held match rate | Held matches | Bigram overlap |
|---|---|---|---|---|
| real | 36.8 ± 1.5% | 12.0 ± 2.4% | 6.5 ± 1.3 of 54 | 0.73 |
| within-line shuffle | 30.5 ± 1.1% | 7.2 ± 4.2% | 3.9 ± 2.3 | 0.58 |
| across-corpus shuffle | 28.9 ± 1.2% | 7.5 ± 3.4% | 4.0 ± 1.9 | 0.46 |
| iid matched | 29.0 ± 1.0% | 8.4 ± 2.4% | 4.5 ± 1.3 | 0.49 |
| Markov order 1 | 35.6 ± 2.4% | 10.4 ± 3.6% | 4.5 ± 1.5 of 43 | 0.86 |
| Markov order 2 | 35.9 ± 2.0% | 10.1 ± 6.7% | 3.3 ± 2.1 of 32 | 0.75 |

**Comparisons with the real corpus:**

- **Against the shuffled and iid controls,** real data wins.
  - Training rate: 6–8 points higher in 8 of 8 seeds.
  - Held-out matches: about 2.5 more.
- **Against the Markov controls,** real data is indistinguishable.
  - Training rate: +1 point.
  - Held-out gap: +1.6 to +1.9 points, ± up to 7.6, and its sign flips across seeds.
- **What drives the advantage.** It tracks repetition: held-out lines in the real corpus share far more sign pairs with training lines (0.73–0.86) than shuffled lines do (0.46–0.58).

**Verdict.** The fit gives no evidence of Sanskrit or of any language. Its advantage over shuffled text comes from repeated sign sequences: a flexible 46-sign key finds dictionary words about as often in synthetic text that keeps only local repetition. The report's held-out rates (4/56, 7/49) are what this search produces on a repetitive corpus. The result is indicative only, because the original optimizer is missing and could not be rerun against the same controls.
