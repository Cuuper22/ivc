# context_002: is there a 002-specific end effect?

Question. For signs Y that follow 002 at least 5 times, is Y more often the last token (stored order) when 002 precedes it than its own baseline predicts? Lipi stored-final = reading-initial under the Mahadevan convention, so "002 before Y, Y final" in stored order reads "Y, then 002" with Y at the START of the text in reading order.

Data. Lipi metadata_filtered.csv, dir. R/L (4,266 rows), right end intact (text ends with '+'): 3,684 rows, 2,536 distinct texts after collapsing exact duplicates. 8,103 token occurrences with a legible predecessor; 592 follow 002.

Method. Per Y: 2x2 table (preceded by 002 vs not; final vs not), Haldane odds ratio with Woolf CI, Fisher exact P, Holm over the 10 qualifying Y (those with >=5 after 002 and some baseline occurrences). Pooled: logistic regression with a separate intercept per Y plus a 002 indicator; Mantel-Haenszel OR; permutation P (002 flag shuffled within Y, 20,000). Occurrences are conditioned on having a predecessor, which removes the text-initial confound; the sensitivity that includes text-initial tokens is in the JSON.

Result.
| Y | After 002: final / n | Baseline P(final) | OR (95% CI) | Holm P |
|---|---|---|---|---|
| 861 | 113 / 137 | 0.54 | 4.0 (1.8-8.6) | 0.007 |
| 817 | 114 / 121 | 0.72 | 6.2 (2.2-17.7) | 0.009 |
| 820 | 80 / 86 | 0.72 | 4.9 (2.0-12.5) | 0.003 |
| 031 | 0 / 11 | 0.38 | 0.07 (0.00-1.25) | 0.06 |
| 390, 368, 220, 595 | 0 / 15, 11, 10, 7 | 0.09, 0.09, 0.12, 0.17 | 0.3-0.4 (CI 0.01-8) | 1.0 |
| 824, 365 | 7 / 7, 0 / 5 | tiny baselines | uninformative | 1.0 |
Pooled over the 10 Y: OR 2.11 (1.38-3.21), MH 2.12, permutation P 0.0003; with row-length dummies 3.21 (2.04-5.07); text length >=3 only 2.38; leave-one-Y-out 1.56-2.82. Including text-initial tokens: 817 10.1, 820 7.8, 861 5.8 (all Holm P<0.001), pooled 3.6.
Placebo: the same pooled model for the 25 most frequent predecessors (each with its own Y set) gives 002 OR 2.1; 060 gives 30 (4 Y), and 233, 235, 705, 415 are nominally >1; most others are <1.

What it shows. After a terminal-prone baseline is accounted for, 861, 817 and 820 are still more often stored-final (reading-initial) right after 002. The effect is heterogeneous: five other signs after 002 are never final, so the pooled OR averages a strong effect on three signs with none or a negative one on the rest. Row length partly masks the pooled effect rather than creating it.
What it does not show. That the effect is specific to 002 as a kind of sign: other predecessors (060 most strongly) show comparable collocation-with-ending patterns, and these three Y are the signs the project already tracks as terminal-prone. Lipi only.
Mahadevan replication: not run. The sign crosswalk has no exact Lipi 002 -> Mahadevan edge: the only edge from Lipi 002 is edge_00002 -> Mayig P122, mapping_state conflict, accepted_for_analysis false; the only exact edge in the file is 740 -> P324. Mahadevan IDs exist only mediated through Mayig feature metadata.
Prior work. The repo holds no Yadav et al. 2010 or Wells 2015 text or pair list (docs cite Yadav 2010 only for directionality and n-gram method), so whether their frequent-pair lists already cover 002-Y: not checked, source not held.
