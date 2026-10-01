# Extension studies, 2026-10-01

Honest tests of three open questions. Each folder has one script (fixed seeds, deterministic), its JSON output and a one-page REPORT.md.
Run from the repo root: `python3 research/extensions_20261001/<study>/<script>.py` (numpy; scipy for context_002).

| Study | Question | Headline result | Verdict | Folder |
|---|---|---|---|---|
| front_count | Does the front inscription predict the cup + N-stroke count on two-sided tablets? | Mahadevan (85): fronts vary less than chance, P 0.024 (0.032 within locus), lookup accuracy only borderline (P 0.08-0.10), null inside locus 42. Lipi (285): strong within-batch association (P<0.001, survives era/area strata and cross-area prediction). Held-out HARP-era: no gain over majority (37 vs 35 of 115). | Supported within a catalogue, not a portable rule | `front_count/` |
| size_034 | Are 034 tablets smaller than 032/033 of the same format? | Family-collapsed (216 families), format-stratified: area ratio 0.861 (95% CI 0.79-0.93), P 0.0005; 0.87 after era and material; 0.90 (0.82-0.997) with area-section fixed effects. | Supported as a size difference; says nothing about a tier | `size_034/` |
| context_002 | Is there a 002-specific end effect? | Stored-final after 002 (= reading-initial): 861, 817, 820 each Holm P<0.01 (OR 4.0, 6.2, 4.9); five other signs after 002 are never final (0/7 to 0/15). Pooled OR 2.1 (1.4-3.2). Mahadevan replication untestable (no exact 002 crosswalk). | Supported for 3 signs, heterogeneous, Lipi only | `context_002/` |
| alternation_null | Are the proposed rewrites 65→87-59, 66→87-60, 60→59-211, 15→149-342 more frequent than for matched-frequency/position decoys? | Each has 2 exact-context pairs. Fixed in advance: P≈1e-4. Allowing the selection the repo actually made: 1–9% of matched decoy searches do as well. 94 other swap types recur as often. | Modest, selection-sensitive; not significant after multiplicity | `alternation_null/` |
| phonetic_null | Do the Sanskrit-dictionary key fits beat chance? | The repo's optimizer is missing, so this uses a re-implementation. Real held-out rate 12% vs 7–8% for shuffled text, but 10% for Markov text that keeps local repetition. | No evidence of a language; the advantage is sign-sequence repetition | `phonetic_null/` |
