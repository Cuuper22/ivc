# alternation_null: are the proposed sign alternations more frequent than chance?

**Question.** Do the four proposed rewrites have more exact-context support than rewrites of signs with the same frequency and positional profile?

- roof `65 -> 87-59`
- marked fish `66 -> 87-60`
- surrounding marks `60 -> 59-211`
- non-fish `15 -> 149-342`

**Data.** 1,659 unique strict Mahadevan lines (`research/data/mahadevan_20260905/concordance_rows.csv`, reading order).

**Method.** `alternation_null.py` is deterministic and runs in about 30 s.

- **Support** uses the repo's own definition from `research/tools/semantic_transducer_search.py`. Take a line with A at slot i; if replacing A with B C gives another observed line, that counts as support. The script reproduces `modifier_ranking.json` exactly.
- **Decoy rules** `A' -> B' C'` draw each sign from the 25 nearest neighbours of A, B and C. "Nearest" combines |log2 frequency difference| with twice the difference in initial and final share.
  - The pools exclude every sign the repo used as a tick, roof or part.
  - All decoys are enumerated: 14,063 to 15,400 per rule, plus 20,000 samples from 50-sign pools.
- **Selection-aware tests** reflect how the repo actually found its rules.
  - Per rule: fix A and its base, scan all 834 candidate extra signs, and compare with equal-sized scans on matched decoy pairs.
  - Per family: rerun the whole tick and roof family search on 2,000 relabelled decoy families.

**Result.** Each rule has 2 exact-context pairs. The 15 rule has one more pair, but that pair shares no sign.

| Rule | Pairs (≥1 / ≥2 shared signs) | Objects | Pre-specified decoys ≥ observed | Selection-aware: decoy scans ≥ observed | Matched signs with some rewrite as good |
|---|---|---|---|---|---|
| 65 → 87-59 | 2 / 2 | 5 | 5 of 14,063 (P 0.0004) | 8.6% | 14 of 25 |
| 66 → 87-60 | 2 / 1 | 9 | 2 of 15,400 (P 0.0001) | 1.1% | 6 of 25 |
| 60 → 59-211 | 2 / 1 | 14 | 0 of 14,927 | 3.4% | 10 of 25 |
| 15 → 149-342 | 2 / 2 | 11 | 3 of 14,449 (P 0.0002) | 4.8% | 11 of 25 |

**Family level:**

- **Tick family** (best candidate: 211 after the base, 6 pairs). It is unusual by pairs (P 0.0035) and by contexts (P 0.0025). It is not unusual by number of bases (P 0.078) or by pairs with ≥2 shared signs (P 0.44).
- **Roof family.** P 0.026 for pairs; P 0.020 for pairs with ≥2 shared signs.

**Corpus census** (confirms the audit):

- 1,612 one-sign ↔ two-sign swap types share ≥2 context signs.
- 94 of those recur in ≥2 contexts, or 29 if the contexts must share no sign.
- Only `65 → 87-59` and `15 → 149-342` are among the 94.
- The best-supported rewrite of 65 is `65 → 267-99` (6 contexts), not `87-59`.

**Verdict.** The rules are modestly supported, and that support depends on how they were picked; nothing here says what any sign means.

- **Rule fixed in advance:** each beats chance (P about 1e-4).
- **After the selection the repo actually made:** 1–9% of matched decoy scans do as well.
- **Multiplicity:** none survives correction across 4 rules and 30 base pairs.
- **Comparison with the rest of the corpus:** each rests on 2 pairs, and about 94 other swap types recur just as often.

**Not done.** The repo's 290-program joint selection was not rerun on decoys. The family-level scan stands in for it and is the more generous of the two searches.
