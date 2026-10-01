# Testing proposed structure in the Indus corpus: catalogue direction, tablet production batches, and null baselines for writing-operation and phonetic hypotheses

**Cúper (Yousef) Anas**
Independent researcher, San Francisco, California, USA
Version: author draft 0.2, 2026-10-01 (replaces draft 0.1 of 2026-09-07)

**Keywords:** Indus script; corpus data; null models; miniature tablets; reading direction; replication

## Abstract

This paper reports what survived testing in a computational study of Indus inscriptions carried out from May to September 2026. Five results hold up. (1) A frozen copy of Mahadevan's 1977 concordance reproduces all six of its published census figures. (2) The open Lipi catalogue stores inscriptions in the reverse of the conventional reading order, so results computed on its "final" position describe the reading-initial end. (3) On two-sided miniature tablets, the face opposite the cup-and-strokes face predicts the stroke count within a catalogue (permutation P 0.024 in Mahadevan, below 0.001 in Lipi) but not on later-excavated tablets, which fits production batches rather than a portable rule. (4) Tablets with cup plus four strokes are about 14% smaller in area than comparable cup plus two or three stroke tablets (ratio 0.861, 95% CI 0.79 to 0.93). (5) A known text-opening pattern after sign 002 replicates with a baseline-adjusted test. Two earlier leads fail their nulls: a two-operation spelling system for fish-sign variants ranks last of eight models in a joint test, and whole-inscription Sanskrit-dictionary fits do no better than Markov text. Known results are cited, not claimed.

## 1. Introduction

Draft 0.1 of this paper presented a connected system of "writing operations" in the Indus script as its main result. Later tests did not support that framing. This version keeps the results that survived, states each against the null that tests it, and credits prior work where it already reports the pattern. It makes no claim about sign values, word meanings or the language of the script, and none follows from anything below.

The study is computational and uses two public catalogues: the Mahadevan 1977 concordance [1] and the open Lipi inscription table [2]. Permutation tests use 20,000 shuffles with fixed seeds, and every script is deterministic (Section 10).

**Table 1. Summary of results.**

| # | Result | Status | Prior work |
|---|---|---|---|
| 1 | Frozen Mahadevan 1977 concordance; all six published census figures reproduce | Data contribution | Mahadevan 1977 [1] is the source; the snapshot is new |
| 2 | Lipi stores inscriptions in reverse of reading order; its "terminal" results are reading-initial | Verified correction | Directional asymmetry is known [3]; the catalogue reversal is not documented |
| 3 | On two-sided tablets the front predicts the cup + stroke count within a catalogue, not on later tablets | Supported; consistent with production batches | Variation noted [4, 5]; the association test is new |
| 4 | Cup + four-stroke (034) tablets are about 14% smaller in area (0.861; about 0.90 with area controls) | Supported as a size difference only | None found |
| 5 | After sign 002, three signs open the text more often than their baseline predicts; replicates in Mahadevan | Replication of a known pattern | Text openers listed in [3]; the baseline-adjusted test is new |
| 6 | Roof/87 and surrounding-marks/211 spelling operations; 15 to 149-342 contraction | Not supported: last of 8 in joint test; selection-sensitive | Fish-sign diacritics proposed in [6] |
| 7 | Sanskrit-dictionary key fits | No evidence of a language; original optimizer unavailable | None |

## 2. Data and conventions

**Mahadevan concordance.** The public concordance maintained by the Indus Research Centre (RMRL) at indusscript.in reproduces the corpus of Mahadevan 1977 [1]. I retrieved it on 2026-09-05 through its ordinary public interface, without authentication, as 14 response pages, and stored the exact records together with a decoded table of 14 sign slots per line. Slots are in reading order. A stored `0` marks a lost or illegible passage and a leading asterisk a doubtful reading; neither is converted into an ordinary sign. The snapshot holds 3,916 surface/line records, of which 343 describe surfaces without text. A "strict" subset keeps lines with a recorded direction code, only undoubted sign identifiers, no damage marker, no internal blank slot, and agreement between recorded and occupied slot counts: 2,575 lines, 1,659 distinct strings, 7,409 sign tokens and 390 sign types. "Strict" means unflagged under the catalogue's own rules.

**Lipi table.** The Lipi table is a public repository file [2] of 5,679 rows (retrieved 2026-05-24), one row per inscribed surface, with object identifiers (CISI-style numbers, for Harappa the H-numbers), site, excavation area and period fields, object dimensions, and a `text` field of signs in Lipi's own three-digit numbering. Its Sanskrit and translation columns were set aside and not used. Lipi sign numbers are a different namespace from Mahadevan's, and identical numbers must not be assumed to name the same sign. Where a result needs both, Section 7 gives an inferred mapping.

**Independence.** The two catalogues are independent transcriptions of overlapping archaeological objects, not independent samples.

## 3. A frozen Mahadevan 1977 concordance

**Question.** Does the retrieved snapshot match the corpus accounting in the 1977 book?

**Method.** I compared six figures from the snapshot with those the book publishes.

**Result.** All six agree exactly.

| Figure | Snapshot | Published |
|---|---:|---:|
| Catalogued objects | 2,906 | 2,906 |
| Non-empty inscription lines | 3,573 | 3,573 |
| Legible sign occurrences, including doubtful readings | 13,372 | 13,372 |
| Sign types, including doubtful readings | 417 | 417 |
| Occurrences of sign 342 (jar) | 1,395 | 1,395 |
| Occurrences of sign 99 | 649 | 649 |

**Interpretation.** The snapshot reproduces the base corpus and its published totals. Census agreement shows completeness of acquisition; it does not show that any single reading is correct. The snapshot and audit script are in the repository (Section 10), so the analyses below can be rerun without the live website. It covers the base corpus only, not the later addendum material the website announces.

## 4. The Lipi catalogue stores inscriptions in reverse reading order

**Question.** Does Lipi's stored sign order run in the same direction as the conventional (Mahadevan) reading order?

**Data and method.** I used the jar sign, which is Mahadevan 342 and Lipi 740. The identification rests on the object-level match H-306 = Mahadevan text 5474 (same excavation number), where Lipi records 740-032-840 and Mahadevan's slots read 403, 87, 342 (Lipi 032 = Mahadevan 87; Lipi 840 = Mahadevan 403), and on the alignment described in Section 7. I counted where the jar falls in lines of two or more signs, excluding Lipi rows with a bracket, slash or `000` and keeping the strict Mahadevan subset.

**Result.**

| Catalogue | Jar occurrences | Jar first | Jar last |
|---|---:|---:|---:|
| Mahadevan (strict, reading-order slots) | 1,051 | 0 | 739 |
| Lipi (stored `text`) | 1,319 | 919 | 4 |

The repository note on this reversal reports 937 and 4 under a slightly different row filter; the direction is the same under every filter I tried.

**Interpretation.** Under the standard convention the jar is text-final, a pattern already established for the script [3]. Lipi stores the same material in the opposite order. Anyone who uses the Lipi table for "terminal", "closure" or "line end" results is describing the reading-initial end of the inscription. The correction is mechanical: reverse Lipi strings before comparing with Mahadevan or with the literature. It also changes how I describe my own earlier results. The observation I had treated as the project's accepted structural finding, that seals M-376 and M-391 carry `861-533-717` after `002` at the "end", sits at the reading-initial end; in conventional order those seals begin `717-533-861-002`. That observation remains a description of two seals. Sign 533 occurs on only two seals in the 5,679-row table, and the 0.0002 false-positive rate I once attached to it was computed for a prefix (`002-861`) chosen after looking at the data; a scan over all prefixes finds many comparable repeated cells. I therefore do not treat `533-717` as a fixed unit.

## 5. Two-sided miniature tablets: the front predicts the stroke count within a catalogue

### 5.1 Question and prior work

Many miniature tablets from Harappa carry a short inscription on one face and a cup sign with two, three or four long strokes on the other. Priyanka [4] describes more than forty such tablets with an identical inscription on one side and two, three or four strokes followed by a pot on the other; Mukhopadhyay [5] shows the same obverse inscription with all three constructs and attributes the difference to separate licence slabs for one activity. Neither tests whether a given front tends to keep its stroke count. I tested that. In what follows "front" means the face other than the cup-and-strokes face; it carries no claim about ancient obverse and reverse.

### 5.2 Data

(a) Mahadevan: the 85 strict two-sided miniature tablets (object class 3, two single-line surfaces) in which exactly one face is cup sign 328 with a long-stroke group; 39 distinct fronts; 19, 35 and 31 tablets with two, three and four strokes. Eight fronts occur with more than one count and four with all three; four fronts (21, 6, 4 and 3 objects) account for the twelve occupied cells, 34 objects in all. Of the 85, 38 come from locus 42.

(b) Lipi: two-row tablet objects with exactly one face reading cup plus 032, 033 or 034 (two, three or four strokes), both faces complete, no `000` or bracket in the front, and preservation not fragmentary or partly damaged: 285 objects (80, 118, 87 for two, three, four strokes; 282 from Harappa), 190 distinct fronts. Lipi's older tablets overlap Mahadevan's objects, so (a) and (b) are not independent replications, and both are transcriptions of the same material.

(c) Held-out split, fixed before scoring: Harappa objects H-1 to H-1499 (earlier registers, existing before 1977) form the fit set (161 objects); objects from H-1500 on or with an excavation identifier of the 1986 to 2007 project form the test set (115 objects: 29, 35, 51 with two, three, four strokes). The realised gap runs from H-1347 to H-1768.

### 5.3 Method

Statistics: number of fronts with more than one count; lookup hits (sum over fronts of the most frequent count); leave-one-out lookup hits; mutual information between front and count; chi-square. Null: the counts are permuted across objects, 20,000 times, unrestricted and within strata (excavation locus for Mahadevan; site, era and area-section for Lipi). A cross-batch test predicts each object from same-front objects in a different locus or area-section. For the held-out test the lookup is fitted on the fit set only (ties resolved by fit-set frequency, unseen fronts given the fit-set mode, three strokes) and scored against the majority baseline and 20,000 shuffles.

### 5.4 Results

| Test | Observed | Null mean | P |
|---|---|---|---|
| Mahadevan (85), fronts with varying count | 8 | 11.0 | 0.024 |
| Mahadevan, within locus (12 strata) | 8 | 10.9 | 0.032 |
| Mahadevan, lookup hits (63 of 85) | 63 | 59.2 | 0.076 |
| Mahadevan, mutual information (bits) | 0.859 | 0.732 | 0.016 |
| Mahadevan, leave-one-out hits | 36 | 32.5 | 0.32 |
| Mahadevan, cross-locus prediction (55 eligible) | 27 | 21.1 | 0.13 |
| Mahadevan, locus 42 only (38 objects): varying fronts | 3 | 3.6 | 0.37 |
| Lipi (285), within era and area-section (33 strata): fronts varying | 23 | 32.8 | 0.0007 |
| Lipi, lookup hits | 250 | 231.8 | below 0.0001 |
| Lipi, leave-one-out hits | 141 | 112.5 | 0.0002 |
| Lipi, cross-area-section prediction (118 eligible) | 64 (global mode 52) | 43.5 | 0.004 |
| Lipi, without the 28-object family: lookup | 233 | 217.7 | 0.0001 |
| Held-out (115 objects), lookup fitted on older tablets | 37 | 36.3 | 0.47 |
| Held-out, always-three baseline | 35 | | |

In Mahadevan, same-front tablets differ in stroke count less often than chance (P 0.024; 0.032 within locus). The lookup advantage is only borderline (63 against 59.2 expected), the leave-one-out test is null, and inside locus 42 alone every statistic is null, with low power. Outside locus 42 the mutual information is still above chance (1.280 against 1.110 bits, P 0.031). In Lipi the association is strong within site, era and area-section strata, survives removal of the largest family, and holds across area-sections. It does not carry forward in time. Fitted on the older tablets, the lookup scores 37 of 115 on the later tablets, against 35 for always guessing three and 36.3 expected under shuffling (P 0.47; 0.78 within area-section). Only 27 of the 115 later tablets have a front that occurs in the fit set; on those 27 the lookup scores 13 against 11 for the majority rule, so a modest effect could be missed. The stroke-count mix also differs between the two periods: three strokes dominate the older set (48, 79, 34 for two, three, four) and four strokes the later one (29, 35, 51).

### 5.5 Interpretation

The pattern is an association among tablets within a catalogue, strongest where tablets share a find area, and absent in a forward test. That is what tablets made together in batches would produce: a front inscription copied across a set, with a count that stays constant or shifts within the set. Meadow and Kenoyer [7] describe moulded Harappa tablets made from sets of master moulds that could produce multiple duplicates, and incised steatite tablets with one inscription cut by at least three different engravers. This supports copy sets in general but does not link a front to a count. I do not read the result as a front-to-count rule, and it says nothing about what the signs mean. Area-section is a coarse stand-in for a production batch, and a direct test needs a crosswalk between the Mahadevan and Lipi object numbers (Section 9).

### 5.6 A remark on equal quantities

The variable stroke count has a simple consequence for numerical readings, and credit for the underlying observation belongs to the sources above. Suppose a front has a fixed value F, a reverse with n strokes expresses nu for a common positive unit u, and both faces express the same scalar quantity. Mahadevan texts 4554 and 4553, which share the front `342-403-103` and carry two and four strokes, then require F = 2u and F = 4u, so u = 0. At least one assumption fails: the front may be a descriptor and not a total, units may depend on context, or the strokes may not be cardinals in this use. It does not refute a numerical reading restricted to a justified subset of tablets, such as those Fuls [8] studies. Likewise a front-only lookup that memorises every front fits at most 63 of the 85 objects, which is only slightly above the 59.2 expected by chance.

One further observation is untested. Mahadevan records 4448, 4452 and 5461 share the main face `173-59-347-342-176`; their other faces are `95-328-59`, `95-59-328` and `95-328-59`, so the cup and fish-shaped signs exchange places relative to the four-stroke group. I ran no null for this and offer it only as an observation.

## 6. Cup plus four strokes tablets are smaller than their neighbours

### 6.1 Question

An earlier internal decision (July 2026) closed the question whether tablets carrying the four-stroke sign 034 form a distinct size class. It rested on discrimination within one series of 22 tablets (H-2218 to H-2239) and one 033 object. I re-tested the size difference itself.

### 6.2 Data

Lipi has 379 tablet objects with a short cup-plus-stroke face (`700` with `032`, `033` or `034`); 328 have positive recorded dimensions and 309 are in the frozen test file, all from Harappa: 85 with 032, 113 with 033, 111 with 034. Of the 309, 132 are from the later (H-1500 onward) period. Area-section is recorded for 255, material (steatite or faience) for 256, and phase for 217. The 22 tablets of the H-2218 to H-2239 series (a group of three-sided tablets with identical inscriptions described by Meadow and Kenoyer [7]) are counted as one family.

### 6.3 Method

The outcome is log(horizontal size multiplied by vertical size). Each near-duplicate family (an identical longer text on the other face) casts one vote: 216 families and 228 family-by-format-by-group cells, 69 of them 034. Format is tablet type crossed with the number of sides. The statistic is the format-weighted mean difference in cell log area between 034 and 032/033. I permuted the 034 label within strata 20,000 times and bootstrapped families 5,000 times for the confidence interval. As controls I permuted within format crossed with era, material or area-section, and fitted a cell-level regression with family-clustered errors and era, material, area-section and phase terms.

### 6.4 Results

| Analysis | Area ratio 034 / other | Evidence |
|---|---|---|
| One vote per object (not family-collapsed) | 0.857 | P below 0.0001 |
| Family-collapsed, format strata | 0.861 (0.79 to 0.93) | one-sided P 0.0005; two-sided 0.0012 |
| 034 against 033 only / against 032 only | 0.874 / 0.841 | P 0.002 / 0.001 |
| Permute within format by era | 0.861 | P 0.0025 |
| Regression with era and material | 0.872 (0.80 to 0.95) | z = -3.11 |
| Regression with area-section (33 parameters) | 0.904 (0.82 to 0.997) | z = -2.03 |
| Permute within format by area-section (50 strata) | 0.861 | P 0.086 |
| Later period only / earlier period only | 0.871 (P 0.017) / 0.903 (P 0.066) | same direction |
| Without the H-2218 to H-2239 series | 0.861 | P 0.0004 |
| Within-family pairs (10) | 0.877; 034 smaller in 8 of 10 | sign-flip P 0.07 |

Length and width shrink by about the same factor (0.93 each).

### 6.5 Interpretation

034 tablets are about 14% smaller in area than 032 and 033 tablets of the same format, with one vote per copied family, and the difference does not depend on the 22-tablet series. It holds after era and material. With area-section fixed effects it shrinks to about 10% and the interval nearly reaches 1, and permutation inside area-section strata loses power (P 0.07 to 0.09), so the excavation context may account for part of it. This reverses the July closure, which depended on a single object. The result is a shift in means with wide overlap, not a tier, a unit or a meaning. It also does not rule out a format or series confound that the metadata cannot show.

## 7. Sign 002 and text openers: a replication of a known pattern

### 7.1 Question and prior work

Yadav et al. [3] already report, in Mahadevan numbers, that signs 267, 391 and 293 are the most frequent text beginners and that 99 most often follows them; their bigram table ranks the pair (267, 99) first by both frequency (168) and log-likelihood ratio (792.4) and (391, 99) fifth by frequency (56). The question I asked is narrower: after allowing for how often each sign is final anyway, is a sign more often at the edge of the text when 002 (Lipi numbering) precedes it?

### 7.2 Data and method

I used Lipi rows with direction R/L and an intact end (3,684 rows; 2,536 distinct texts after removing exact duplicates). "Final" means last in stored order, which is the reading-initial position (Section 4). I counted 8,103 token occurrences with a legible predecessor, of which 592 follow 002; this conditioning removes the confound of text-initial tokens. For each of the 10 signs Y that follow 002 at least five times, I formed a two-by-two table (preceded by 002 or not; final or not) and computed a Haldane odds ratio with a Woolf interval and a Fisher exact P, with Holm correction over the 10 signs. A pooled logistic model gives each Y its own intercept and adds a 002 term; its P comes from shuffling the 002 flag within Y.

### 7.3 Results

| Y (Lipi) | After 002: final / n | Baseline P(final) | Odds ratio (95% CI) | Holm P |
|---|---|---|---|---|
| 861 | 113 / 137 | 0.54 | 4.0 (1.8 to 8.6) | 0.007 |
| 817 | 114 / 121 | 0.72 | 6.2 (2.2 to 17.7) | 0.009 |
| 820 | 80 / 86 | 0.72 | 4.9 (2.0 to 12.5) | 0.003 |
| 390, 368, 220, 595, 031 | 0 / 15, 11, 10, 7, 11 | 0.09, 0.09, 0.12, 0.17, 0.38 | 0.07 to 0.4 | 0.06 to 1 |

Pooled over the 10 signs the odds ratio is 2.11 (1.38 to 3.21; permutation P 0.0003), and 3.21 with row-length terms. The pooled figure averages a strong effect on three signs with none or a negative one on five others, which are never final after 002. As a placebo, the same pooled model for the 25 most frequent predecessors gives 002 an odds ratio of 2.1, while sign 060 gives 30 and most others fall below 1.

Mapping to Mahadevan numbers. I inferred a Lipi-to-Mahadevan sign mapping by aligning texts with exactly one length-matched, sign-consistent Mahadevan counterpart, starting from three seeds (700 = 328, 740 = 342, 032/033/034 = 87/89/95) and mapping 167 signs. With the target sign left out, 002 maps to 99 (202 of 206 rows), 861 and 817 both to 267 (62 of 65 and 59 of 62), and 820 to 391 (42 of 44). The mapping is partly circular and cannot separate 861 from 817. In Mahadevan's reading-order slots, 267 immediately before 99 is text-initial in 196 of 222 lines against 28 of 50 when 267 precedes another sign (odds ratio 5.9, P 8e-7); 391 before 99 gives 58 of 64 against 45 of 70 (odds ratio 5.0, P 4e-4). Direction and size match the Lipi odds ratios (4.0, 6.2, 4.9).

### 7.4 Interpretation

The stored-final pattern after 002 is the text-opening pair 267-99 and its relative 391-99, known from [3]. Because 99 is also the second most frequent sign, a frequent-pair list alone would contain these pairs without any end effect; the baseline-adjusted odds ratios, the split among signs, and the placebo are the only additions here. The Mahadevan result replicates a transcription and segmentation, not a new sample. Other predecessors, 060 most strongly, show comparable collocation with text edges, so the effect is not specific to 002.

## 8. Negative results

### 8.1 Roof/87 and surrounding-marks/211 as connected writing operations

**What was proposed.** Draft 0.1 proposed rewrite rules on fish-shaped signs: a roof operation (65 to 87-59; 66 to 87-60) and a surrounding-marks operation (60 to 59-211), with the claim that the operations compose through observed intermediate inscriptions. The idea that modifications of the fish sign carry separate writing operations is a variant of a proposal in [6]. A related candidate was a non-fish contraction, 15 to 149-342.

**Joint test.** The repository's integrated campaign scored eight models of how these fish variants are spelled. Each is a code-length comparison, in bits, of leave-one-expression-out prediction of the field symbol (1,175 objects or faces) and of the companion cup-and-stroke count (85 tablets), with a charge for the rule. The baseline that treats each variant as a separate category scored 3,169.57 bits. The two-operation model scored 3,192.96, the worst of eight; its data cost alone, before the 22-bit rule charge, is 3,170.96, which is also worse than the baseline. The other models fall between: 3,175.50 (unmarked fish category), 3,177.46, 3,178.46, 3,180.57, 3,181.74 and 3,190.29. The test predicts field symbol and stroke count, so a spelling rule could be true without improving those predictions; the status is no external support, not disproof. Draft 0.1 reported that the two-operation pair ranked first among 290 combinations of previously observed marker candidates; that ranking was within a pool derived from earlier observations and says nothing about matched decoys, which the null below supplies.

**Null test of the alternations.** For each rule, support is the number of exact-context pairs: a line with sign A at some slot such that replacing A with B C gives another observed line. I computed it over the 1,659 unique strict Mahadevan lines, reproducing the repository's own ranking exactly. Decoy rules A' to B' C' draw each sign from the 25 nearest neighbours of A, B and C in frequency and in share of initial and final positions, excluding every sign used in the proposed rules; all 14,063 to 15,400 decoys per rule were enumerated, plus 20,000 samples from wider pools. To reflect how the rules were chosen, I also fixed A and its base sign, scanned all 834 candidate extra signs, and compared the best result with the same scan on matched decoy pairs and reran the whole tick and roof family search on 2,000 relabelled decoy families.

| Rule | Exact-context pairs | Objects | Decoys at least as good, rule fixed in advance | Decoy scans at least as good, selection-aware |
|---|---:|---:|---|---:|
| 65 to 87-59 | 2 | 5 | 5 of 14,063 (P 0.0004) | 8.6% |
| 66 to 87-60 | 2 | 9 | 2 of 15,400 (P 0.0001) | 1.1% |
| 60 to 59-211 | 2 | 14 | 0 of 14,927 | 3.4% |
| 15 to 149-342 | 2 | 11 | 3 of 14,449 (P 0.0002) | 4.8% |

At the family level, the tick family (211 after the base, 6 pairs) is unusual by number of pairs (P 0.0035) and of contexts (P 0.0025) but not by number of bases (P 0.078) or by pairs with two shared context signs (P 0.44); the roof family gives P 0.026 and 0.020. Across the whole corpus, 1,612 swap types of one sign for two share at least two context signs, and 94 of them recur in two or more contexts; only 65 to 87-59 and 15 to 149-342 are among them, and the best-supported rewrite of 65 is 65 to 267-99 with six contexts, not 87-59.

**Interpretation.** Each rule rests on two exact-context pairs. Fixed in advance, each beats matched decoys (P near 0.0001), but the rules were not fixed in advance: they were found by searching, and under that selection 1% to 9% of matched decoy searches do as well. None survives correction across four rules and 30 base pairs, and about 94 other swap types recur as often. The 15 to 149-342 contraction receives the same verdict. I did not rerun the 290-program joint selection on decoys; the family-level scan stands in for it and is the more generous of the two. The proposed operations are not disproved, but nothing here supports them over the many ordinary alternations in the corpus.

### 8.2 Whole-inscription Sanskrit-dictionary key fits

**What was tested.** Draft 0.1 included fits in which one injective sign-to-syllable key maps whole inscriptions onto Sanskrit dictionary headwords. The September report gave, for the unexpanded run, 54 of 146 training and 4 of 56 held-out matches, but no chance baseline.

**Data and method.** The optimizer that produced those numbers is not in the repository or its git history, so the original numbers cannot be reproduced. I wrote an independent re-implementation from the report's description. The dictionary is Monier-Williams (192,482 headwords, split into 7,231 syllable-like chunks). Lines are the 271 distinct strict lines of two to ten signs built from the 46 signs made up of the 40 most frequent signs plus the fish family. A line matches if its chunk sequence is exactly a headword. The key is chosen on training lines only by simulated annealing (6 restarts of 40,000 proposals, 8 seeds, an 80/20 split with identical indices in every condition). Every condition uses the same optimizer, budget and seeds. Controls: sign order shuffled within each line; all tokens shuffled across lines; independently drawn signs with the real lengths and frequencies; and order-1 and order-2 Markov corpora, which keep local sign repetition that the shuffles destroy.

**Result.** Mean over eight seeds.

| Condition | Train match rate | Held-out match rate | Held-out matches | Held-out bigram overlap with training |
|---|---|---|---|---|
| Real | 36.8% | 12.0% | 6.5 of 54 | 0.73 |
| Within-line shuffle | 30.5% | 7.2% | 3.9 | 0.58 |
| Across-corpus shuffle | 28.9% | 7.5% | 4.0 | 0.46 |
| Independent, matched | 29.0% | 8.4% | 4.5 | 0.49 |
| Markov order 1 | 35.6% | 10.4% | 4.5 of 43 | 0.86 |
| Markov order 2 | 35.9% | 10.1% | 3.3 of 32 | 0.75 |

Against the shuffled and independent controls the real corpus does better: its training rate is 6 to 8 points higher in all eight seeds, and it has about 2.5 more held-out matches. Against the Markov controls it is indistinguishable: the training rate is one point higher and the held-out gap is 1.6 to 1.9 points, with a spread of up to 7.6 and a sign that changes across seeds.

**Interpretation.** The advantage over shuffled text tracks repetition of sign sequences: held-out lines in the real corpus share far more sign pairs with training lines (0.73 to 0.86) than shuffled lines do (0.46 to 0.58). A flexible 46-sign key finds dictionary words about as often in synthetic text that keeps only local repetition. The report's held-out rates are what this search produces on a repetitive corpus, and the fits give no evidence of Sanskrit or of any language. The test is indicative only because the original optimizer could not be rerun against the same controls.

## 9. What would move this forward

A crosswalk between Mahadevan and Lipi object numbers, built from shared excavation numbers as for H-306 and text 5474, would let the batch hypothesis be tested directly: fit the front-to-count lookup on one catalogue and score it on tablets the other adds, and read excavation context for each batch. For the 034 size difference, the missing control is excavation phase and find context at object level; the difference should vanish within a single dated deposit if it is a batch effect. Newly published tablets, for example from later volumes of the Corpus of Indus Seals and Inscriptions or from Harappa excavation records, allow preregistered predictions: counts conditional on the front within find-area, a size ratio below one for 034, and the direction of the 002 pattern in reading order. For writing-operation hypotheses, the test that would count is a prediction made before looking at independent contexts, scored against matched decoys with the selection procedure included.

## 10. Data and code availability

Everything is at https://github.com/Cuuper22/ivc.

- Mahadevan snapshot, decoded table, paired-tablet outputs and census summary: `research/data/mahadevan_20260905/` (`concordance_documents.json.gz`, `concordance_rows.csv`, `summary.json`, `paired_objects.json`, `front_families.json`). `make audit` reruns the six census checks and the paired-face census with the standard library only.
- Lipi table (as retrieved): `research/data/open_prototype/lipi/metadata_filtered.csv`. Reading-direction note: `research/docs/reading_direction_note.md`.
- Extension studies, one script, one JSON output and one-page report each, under `research/extensions_20261001/`: `front_count/` (Section 5), `size_034/` (Section 6), `context_002/` (Section 7, with `mahadevan_check.py` for the mapping), `alternation_null/` and `phonetic_null/` (Section 8). Run any one as `python3 research/extensions_20261001/<study>/<script>.py` (numpy; scipy for `context_002`). Seeds are fixed.
- Joint test of the eight spelling models: `research/campaigns/integrated_20260906/integration/summary.json`, regenerated by `make campaign` (long). `make verify` runs the verification stage of the completion pass; `make check` syntax-checks the scripts; `python research/tools/check_headline_numbers.py` compares headline numbers.
- Claim ledger and the earlier accepted observation: `research/docs/claim_ledger.md`.

The phonetic re-implementation does not reproduce the September run. The Mahadevan concordance and the Lipi table are third-party material and remain subject to their own terms; the repository's code and analysis outputs are separate from them.

## AI assistance and responsibility

Large language models gave substantial assistance with the analysis (search design, coding, statistical tests) and with drafting this paper. I designed the study questions, reviewed the outputs, and am responsible for the content, the corrections and any remaining errors. Models are not authors.

## Changes from 0.1

- Cut the "connected system" framing, the scope-incompatibility algebra, the counter-field section (now one untested sentence) and the research program; the roof/87, tick/211 and 15 to 149-342 proposals are now a negative result against matched-decoy nulls, and the equal-quantity argument is a remark.
- Added the frozen concordance, the Lipi reversal correction, the front-and-count association with its held-out test, the 034 size result, the 002 replication and the Sanskrit-fit null; known results are cited to the sources that reported them.
- Replaced the pinned-snapshot citation and appendices with path-level availability notes, and corrected the joint-test comparison to 3,169.57 against 3,192.96 bits.

## References

1. Mahadevan, I. (1977). *The Indus Script: Texts, Concordance and Tables*. Memoirs of the Archaeological Survey of India 77. New Delhi: Archaeological Survey of India. Public concordance: https://indusscript.in/.
2. Lipi inscription table (5,679 rows). Public repository file `src/assets/data/inscriptions.csv`, https://github.com/yajnadevam/lipi, retrieved 2026-05-24.
3. Yadav, N., Joglekar, H., Rao, R. P. N., Vahia, M. N., Adhikari, R., and Mahadevan, I. (2010). Statistical analysis of the Indus script using n-grams. *PLoS ONE* 5(3): e9506. https://doi.org/10.1371/journal.pone.0009506.
4. Priyanka, B. (2003). New Iconographic Evidence for the Religious Nature of Indus Seals and Inscriptions. *East and West* 53: 31-66. https://www.jstor.org/stable/29757572.
5. Mukhopadhyay, B. A. (2023). Semantic scope of Indus inscriptions comprising taxation, trade and craft licensing, commodity control and access control: archaeological and script-internal evidence. *Humanities and Social Sciences Communications* 10. https://doi.org/10.1057/s41599-023-02320-7.
6. Parpola, A. (1994). *Deciphering the Indus Script*. Cambridge: Cambridge University Press.
7. Meadow, R. H., and Kenoyer, J. M. (2000). The 'Tiny Steatite Seals' (Incised Steatite Tablets) of Harappa: Some Observations on Their Context and Dating. In M. Taddei and G. De Marco (eds), *South Asian Archaeology 1997*, vol. 1, pp. 321-340. Rome: Istituto Italiano per l'Africa e l'Oriente.
8. Fuls, A. (2020). Ancient Writing and Modern Technologies: Structural Analysis of Numerical Indus Inscriptions. Author's copy: https://www.researchgate.net/publication/361812318.
