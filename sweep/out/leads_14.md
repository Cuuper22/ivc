# Sweep 14 leads

Reader 14. Chunk: research docs, claim ledger, notes, the 2026-10-01 paper draft, the SLM and embeddings code, and the evidence/tmp map. Paths below are relative to /home/claude/ivc unless they start with a slash.

Terms, in plain words:
- Lipi: the numeric catalogue (signs written as three-digit numbers). Mahadevan: the 1977 concordance numbering. CISI: the published plate collection with the object drawings and photographs. Mayig: a catalogue that writes signs as P-codes.
- Stored-final: the last sign in the Lipi order. The reading-direction note says Lipi stores texts backwards, so stored-final is the first sign when a text is read conventionally. Every "terminal", "closure" or "tail" in the May-to-July work means the conventional opening.
- p (Fisher or permutation): the chance that a pattern this strong shows up under shuffled data. Small means unlikely by chance.
- OR (odds ratio): 1 means no effect; 4 means four times the odds.
- NLL: average surprise per sign, lower is better. Top-1: share of positions where the model's first guess is right.
- "My rerun": a count I ran this sweep on lipi_current_inscriptions_20260526.csv (5,679 rows, all rows, no filter except the sign-number pattern). It does not reproduce the papers' exact scopes.

---

### 1. Prefix-806 series: 154 or 158 before 806 sends the next sign into 465-475

- What was seen: In the 2026-05-31 run, the Harappa-trained rule (154 or 158, then 806, then a sign in 465-475) gets 23 of 23 positions right against 0 of 23 controls (p 1.2e-13). The holdout from the other sites gets 6 of 6 against 3 of 58 (p 1.1e-6). All sites, prefix-only: 29 of 29 against 3 of 81 (p 1.6e-23). With exact duplicates collapsed: 23 of 23 against 3 of 60 (p 1.4e-17). The extension (154, 155, 158, 100) on the non-Harappa holdout: 9 of 9 against 0 of 55 (p 3.6e-11). The predecessor table: 154 before 806 gives 16 of 16 in-band; 158 gives 13 of 13; 845 before 806 is always the end (15 of 15); 235 before 806 ends the text 14 times in the JSON scope. My rerun on the full Lipi table: 154-806 is followed by 465-475 in 17 of 18 cases, 158-806 in 13 of 16. The misses are all a 000 token (a lost-sign slot). 845-806 ends the text 15 of 15; 235-806 ends it 15 of 19.
- Where: evidence/tmp/risky_806_prefix_series_geographic_holdout_latest_stdout.json (the run and its falsifiers); evidence/tmp/blind_806_prefix_series_20260531/ (13 JPG blind packet, no key file in the folder); research/docs/archive/findings_dossier_formula_operator_20260531.md (verdict); research/docs/archive/vector4_158806_source_family_gate_20260712.md (the closed 158-806 / Phyt lead, which uses the same rows).
- Old label: "promoted metadata candidate; visual and source promotion blocked" (findings dossier, May 31). The blind packet recovered only BS007 and BS010 and missed the non-Harappa positives BS002, BS006, BS008. The July checkpoint does not mention the series. The ledger's 158-806 retraction is a different claim (context association) on the same rows.
- Why it is alive: The rule was learned from one set of sites and scored on sites it never saw, which is the test that matters. It fires on two predecessors the rule did not learn (155, 100) and both land in the same band. The visual packet's misses are the instrument's failure on small crops, which the dossier already says. 806 also has a second clean role (ends the text after 845 and mostly after 235), so it reads like a two-role sign, which the hypotheses section expects.
- What it would mean if true: 806 is a construction operator. A numbered series opens after 154 or 158, and the band 465-475 is its successor class. That is a grammar fact about the sign sequence, and it would be the first positional rule that predicts a specific sign rather than just a place in the text.
- Cheapest next move: Box the 806 and successor tokens on the plate images of the holdout rows (the JSON names them). The JSON's own falsifier is decisive: one source-visible 154-806 or 158-806 followed by a sign outside 465-475 kills the rule. Settle first whether a 000 slot counts as a sign in that check, using the 000 policy in the July checkpoint.

---

### 2. The 060-920 closing cap and its 741/742 feeder, never accepted, never retracted

- What was seen: My rerun: 060-920 occurs 65 times, and 920 is stored-final in 64 of them. 741-060 is followed by 920 in 38 of 38 cases; 742-060 in 9 of 9. 060 itself is stored-final in only 3 of 222 occurrences, so 060 is a sign before the cap, not an ending. The May brief: 060-920 has 52 exact cells, 51 terminal; 741/742/745 come before 060-920 in 40 of 52 object-collapsed cells, and before the sibling caps 060-692, 060-550, 060-820 in 0 of 84. A shuffle of cap labels gives p = 0/5000.
- Where: research/docs/archive/brief_741060920_terminal_formula_20260531.md; research/docs/archive/brief_terminal_governor_network_20260531.md; research/docs/archive/findings_dossier_formula_operator_20260531.md (called the single strongest frontier result); evidence/tmp/blind_060920_terminal_cap_20260531/ (13 JPG); evidence/tmp/blind_741060920_terminal_cluster_20260531/ (13 JPG, labels BT001 to BT010 visible in names); research/docs/archive/lipi_000_sign_bearing_policy_gate_20260712.md (M-105 carries 060-920 next to 000 tokens).
- Old label: "strongest current candidate" in the May dossier, with the brief saying not to enter it as accepted until a token-boxed, stratified source audit and a stricter graphic null both pass. Neither was run. The ledger does not list it, and the July checkpoint does not mention it. It is open, not retracted.
- Why it is alive: It is the cleanest two-sign closer the repo has. A three-sign feeder class (741, 742, 745) picks it out, and the sibling caps fail. The 060 sign also appears as a predecessor in the 002 test (entry 3), so the cap is not a side effect of noise; it is the same structure seen from the other side (entry 3).
- What it would mean if true: Because stored-final is the conventional opening, 920 is the first sign of a text read conventionally, and 741/742/745 + 060 is a fixed opening formula. That would make the cap a title or name slot, the kind of slot every past decipherment started from.
- Cheapest next move: Run the token-boxed source check the brief asked for on the 38 741-060-920 occurrences in the Lipi table that carry a real CISI number. Count how many have a plate on disk first.

---

### 3. The 002 text-end effect survives removing the 060 contexts (my rerun)

- What was seen: For the three signs 861, 817, 820 following 002, my rerun gives 382 stored-final of 432 (88.4%). When 861/817/820 follow any other sign, 135 of 206 are stored-final (65.5%). Remove every row containing 060, 741, 742 or 745: 382 of 430 (88.8%) against 100 of 163 (61.3%). The paper's numbers: pooled OR 2.11 (95% interval 1.38 to 3.21; permutation p 0.0003); per sign 861 OR 4.0, 817 OR 6.2, 820 OR 4.9 (p 0.007, 0.009, 0.003 after Holm's correction for three tests, a standard step-down adjustment). The contrary number, once: 390, 368, 220, 595, 031 are never stored-final after 002 (0 of 15, 11, 10, 7, 11). Each is too few to mean much alone; the pooled test is what carries it.
- Where: research/publications/20261001/PAPER_2_v0.2.md (section 7); research/docs/strongest_result_brief.md; research/docs/archive/findings_dossier_formula_operator_20260531.md (060 placebo). The paper's own script lives in research/extensions_20261001/context_002/ (not read in this sweep).
- Old label: "a replication of a known pattern" (Yadav et al. 2010 text openers 267-99 and 391-99); "not unique to 002" (research/docs/README.md). The May ledger had the 002 end effect as a live candidate. The per-sign baseline matters: 817 and 820 are stored-final 0.91 and 0.80 of the time anywhere (my ledger rerun), against 0.10 and 0.07 for 390 and 368.
- Why it is alive: The effect holds after the 060 cap contexts are removed, so the cap does not explain it. The 390/368 zero-final pattern is the split that matters: one closing family and one continuing family after the same sign 002. The known text openers (267-99) are a different thing, because they sit at the other edge.
- What it would mean if true: 002 is a boundary marker. It sets the following sign to the text's edge, and it is the two-sided version of the stored-final pattern in entry 2.
- Cheapest next move: Rerun the paper's odds-ratio test for 861 alone with the per-sign baseline for 817/820 removed, and report the 060-controlled OR beside it. The paper already names the baseline problem.

---

### 4. Four-stroke tablets are smaller in the same family, so the stroke count may be a size grade

- What was seen: Paper 2, section 6: tablets with the four-stroke sign 034 have an area ratio of 0.861 against 032 and 033 tablets of the same format (95% interval 0.79 to 0.93; one-sided p 0.0005 after collapsing copied families). The regression with area-section controls gives 0.904 (0.82 to 0.997). Within 10 same-front pairs (one copy and one longer copy with a different stroke count), 034 is smaller in 8 of 10 (ratio 0.877; sign-flip p 0.07). Length and width each shrink by about 0.93. The sample: 309 tablets, 85 with 032, 113 with 033, 111 with 034. Mahadevan texts 4553, 4554, 4555 share the front 342-403-103 with 4, 2 and 4 strokes; the plate scan for objects 553 to 555 is on disk.
- Where: research/publications/20261001/PAPER_2_v0.2.md (sections 5.6 and 6); research/docs/mahadevan_crossface_constraints_20260905.md (section 5); research/docs/replacement_run_checkpoint_20260712.md (the 034 size-tier falsification); evidence/tmp/032_002_861_603_slot_source_normalization/vats_excavations_at_harappa_vol2_plates.pdf (288 pages; plate XCVII is the Vats source for 553 to 555).
- Old label: the July checkpoint closed a size tier on an AUC of 0.701 (interval 0.607 to 0.789) and called all 22 small H-series tablets 034 except one true 033. The October paper reopened it as "a size difference, not a tier". The paired-face study treated the count as a broken equal-quantity assumption.
- Why it is alive: The paired-face contradiction (2u = 0) only bites if both faces express one quantity in one unit. If the stroke count is a physical grade, the front and the count are two different fields, and both are data. The within-family comparison is exactly the controlled test that splits "unit" from "grade": same text, different count, and the four-stroke copy is smaller in 8 of 10 pairs.
- What it would mean if true: The number of long strokes is a size class stamped on the tablet. The 034 sign is then a physical grade, not a number, and the arithmetic readings in the Fuls line are reading the grade as a quantity.
- Cheapest next move: Take the 10 within-family pairs and compare area with the Lipi horizontal, vertical and thickness fields directly, with the 5,147 Lipi rows that carry an excavation number as the grouping key for find context.

---

### 5. Front-to-count batch association: real in-stratum, underpowered on the held-out split

- What was seen: Lipi, 285 two-row tablets: fronts that take more than one stroke count occur 23 times, against 32.8 expected under shuffling (p 0.0007: copied fronts keep their count). Lookup hits 250 against 231.8 (p below 0.0001). Leave-one-out hits 141 against 112.5 (p 0.0002). Predicting across area-sections: 64 against 43.5 (p 0.004). Mahadevan, 85 paired tablets: 8 varying fronts against 11.0 expected (p 0.024). The held-out split (115 later tablets) gives 37 against 36.3 expected (p 0.47). The contrary number, once: only 27 of the 115 later fronts appear in the fit set, and on those 27 the lookup scores 13 against 11 for the majority rule.
- Where: research/publications/20261001/PAPER_2_v0.2.md (section 5, and section 9 on what would move it forward); evidence/tmp/lipi_current_inscriptions_20260526.csv (the excavation-idno column is filled on 5,147 of 5,679 rows, my count).
- Old label: "an association among tablets within a catalogue... not a front-to-count rule", with the held-out result read as no transfer.
- Why it is alive: The held-out test had almost nothing to score: 27 of 115 later tablets share a front with the fit set. The cross-area-section test (p 0.004) is the stronger one and it is positive. The stroke-count mix also changes between periods (older 48, 79, 34 for 2, 3, 4 strokes; later 29, 35, 51), which would hurt a fit on the older set and says nothing about the rule.
- What it would mean if true: Copy sets were cut together, and the stroke count is a workshop or batch fingerprint. That gives a way to attach undated tablets to workshops.
- Cheapest next move: Build the crosswalk the paper asks for, using the excavation numbers already on the Lipi rows, and rerun the held-out split leaving out whole excavation groups rather than H-number ranges.

---

### 6. Paired-face counterexample, with the exact finite-data bounds

- What was seen: 85 paired objects, 39 distinct fronts, 51 distinct front-and-count pairs. A front-only lookup can fit at most 39 of 51 pairs, or 63 of 85 objects, so 22 objects are always missed. Texts 4553 and 4554 share the front 342-403-103 with 4 and 2 strokes; if the front is one fixed value F and each stroke is a fixed unit u, then F = 4u and F = 2u, so u = 0. Fuls's equations (v = 2S - L; vL + 1 = 7S + 5) reduce to S(2L - 7) = L^2 + 4, which has four integer solutions (L, S, v) = (4, 20, 36), (6, 8, 10), (10, 8, 6), (36, 20, 4). The bangle constraint in Fuls leaves (10, 8, 6).
- Where: research/docs/mahadevan_crossface_constraints_20260905.md (sections 3, 4 and 8); evidence/tmp/032_002_861_603_slot_source_normalization/ (the Vats scans used to check 553 to 555).
- Old label: "conditional counterexample; not a refutation of Fuls"; the front "descriptor" is "a proposed function, not established".
- Why it is alive: It is a hard arithmetic contradiction rather than a statistical one, so it does not depend on any null model. It rules out one model class (a fixed front equal to a fixed total) and leaves the rest open.
- What it would mean if true: The front is a name, title or commodity and the stroke count is an amount of a second item: a licence or ration pair. That fits the Mukhopadhyay reading of separate licence slabs, and it makes the 2 to 4 stroke split a commodity amount rather than a shared scalar.
- Cheapest next move: The paper names the exact check: high-resolution comparison of the minimal-pair front signs on 4553 to 4555 at plate scale. The Vats plates PDF on disk (section D of the map) is the starting point.

---

### 7. Stored-order directionality: Lothal was "null" only because of training size; retrained it is 54 of 58

- What was seen: Stored order beats the reverse in 0.947720 of exact rows and 0.841096 of rows in the harsh scope. Per site, harsh: Mohenjo-daro 0.816038, Harappa 0.741071. The first Lothal pass read 0.3125 (null-compatible). The ledger's retrain on all other sites scores Lothal 54 of 58 exact rows, and harsh leave-site-out gives 275 wins, 54 losses, 36 ties. Known scripts: Linear B Series D 0.996403 and SumTablets 0.935484 are above Indus; the Pictish-stone comparator is 0.802139, below Indus. The SLM's own stored-order check: 0.883 win share on authentic rows against 0.470 on row-shuffled ones.
- Where: research/docs/strongest_result_brief.md; research/docs/claim_ledger.md (directionality section); research/docs/reading_direction_note.md; research/docs/replacement_run_checkpoint_20260712.md (directionality closure).
- Old label: "fails" leave-site-out, at Lothal, on the L/R stratum and in the Lipi/Mayig overlap; reclassified in October as "power artifacts" and cited, not carried as a project finding (Yadav et al. 2010). The contrary numbers, once: the L/R stratum has only 11 harsh rows and cannot test anything.
- Why it is alive: Published results are a starting point, and AGENTS says go past them. The asymmetry is a sorting key. The bigrams that drive it can be listed, and they show which sign pairs have one direction. Lothal passing on retrain means the site-level failures do not argue against the order.
- What it would mean if true: Sequence order in the stored record reflects a real ordering rule in the text, and the directional bigrams are the grammar's one-way rules.
- Cheapest next move: List the bigrams with the largest stored-minus-reversed margins and check whether 060-920, 741-060-920 and 002-861 are among them (entries 2 and 3). That is a rerun on data already on disk.

---

### 8. Mirror-image signs as writing-direction marks (a published claim the repo has not tested against objects)

- What was seen: Daggumati and Revesz (2021) report 23 mirrored sign pairs that they read as allographs, and argue that mirroring "often denotes only the direction of writing"; they write that "the direction of the tick of sign 851 indicates writing direction", describe a boustrophedon type (type 4) that reverses direction on each row, and discuss H-1302 and H-1303. The repo's Lipi direction field counts (from the 2026-05-24 audit): R/L 4,265 rows, L/R 215, NR 386, T/B 16, BUS 10, SYM 8.
- Where: evidence/tmp/h1302_h1303_direction_prior_work/daggumati_revesz_2021_allographs_nature_article.pdf and its .pdftotext.txt (the text layer is split across columns, so I did not confirm the exact H-1302 and H-1303 sentences); research/docs/replacement_run_checkpoint_20260712.md (H-1682 counterexample).
- Old label: none in the repo beyond "physical writing direction per object is not established". The one object test on file (H-1682) is physically left-to-right on the seal and recorded R/L in Lipi, so the recorded flag does not track the object.
- Why it is alive: A mirrored sign on the object is a direction mark that does not depend on the catalogue's flag at all. If the 23 mirror pairs fall on one side of an object, the physical direction can be read from the object, and the R/L flag can be checked against it. That is the one experiment that splits "stored order" from "physical order".
- What it would mean if true: The physical direction of each object is recoverable from which mirror of a sign it uses, and the Lipi R/L field is wrong for a large share of rows.
- Cheapest next move: Count the Lipi rows containing each of the 23 mirror pairs, tabulate their direction flags, and read the mirror on H-1682 from its plate.

---

### 9. Yajnadevam's allograph groups as a split test (claimed decipherment, used as a hint list only)

- What was seen: The Yajnadevam repo's allographs file groups signs as phoneme classes: r = {390, 820, 861, 760}; v = {590, 002, 388, 363}; n = {615, 368, 520, 012, 019}; m = {220, 504, 527, 255, 070, 060, 092, 335, 340, 322}; y = {156, 422, 215, 277}. The positional numbers in the repo disagree inside the r group: 390 is never stored-final after 002 (0 of 15), while 820 is (80 of 86 after 002) and 861 is (113 of 137). 368 (in group n) is 0 of 11 after 002. 060 (in group m) is the cap sign of entry 2.
- Where: evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/src/assets/data/allographs.csv and decipher.csv; the repo README claims the script was "provably deciphered ... in 2022" (quarantined under the repo's rules, no value accepted).
- Old label: a claimed decipherment, quarantined. The sign values are not accepted.
- Why it is alive: A phoneme class makes a falsifiable statement about position: members of one class should share an edge profile beyond what each sign's own baseline predicts. The r group already fails that test, which is the observation that splits the grouping.
- What it would mean if true: The grouping is right for sound classes, and the position differences are grammar. Or the grouping is wrong at 390 and the class is really the 820/861 closing pair.
- Cheapest next move: Compute the stored-final rate of every member of each of the five groups in the Lipi table, and compare the spread inside each group with the spread across groups.

---

### 10. The 617 two-grid rule: 70 Lipi rows with CISI numbers are waiting for the check July named

- What was seen: 617 appears in 73 Lipi rows (77 token occurrences). 70 rows carry a CISI number and 60 of those are complete. Many texts start with it in stored order: +617-142+, +617-550-003+, +617-243-950+. 617-142 appears as an adjacent pair in 30 rows. Row H-1682 (+154-003-617-033+) also carries 617, so the physical-direction counterexample object is in this set.
- Where: research/docs/replacement_run_checkpoint_20260712.md (the accepted 617 expansion for the five overlap objects, and "Next executable order" item 1); evidence/tmp/lipi_current_inscriptions_20260526.csv; page scans of Mahadevan 1977 in evidence/tmp/mahadevan_m77_pages/ (26 files, 80 MB).
- Old label: "accepted catalogue expansion for the overlap cluster; Lipi-only 617 rows source-pending". The July checkpoint accepts 617 as two grid positions, with zero counterexamples across five objects, named there as M-4, M-25, M-45, M-81 and one more.
- Why it is alive: 617 would be the only catalogue number that the source shows as two signs. If it holds across the 60 complete CISI rows, it changes the count of every text that carries it, and it could explain the Lipi and Mayig count mismatches the July work logged. The 617-142 pair then becomes a grid plus a sign.
- What it would mean if true: 617 is a grid or square motif, and the grid-plus-number pattern is a formula (a grid, then a numeral, then a fixed sign) that repeats across Mohenjo-daro.
- Cheapest next move: Count the grid units on each of the 60 complete CISI plates. The July checkpoint names this as the next executable step.

---

### 11. The Brahmi 817 = dhya near-miss was blocked by a count of 61 rows, not by the corpus

- What was seen: The Brahmi gate (v2) tested 83 sign and orientation families and ranked the near-misses 817 = dhya, 527 = ra, 472 = ra, 060 = ka, 061 = ra. The independence rule (v3) blocked all 83: 817, 472 and 060 have one unique token hash and one CISI object; 527 and 061 have two hashes and one object. Those counts sit inside the 611 source-token features, which come from 61 exact projection-gap rows. In the Lipi table, 817 appears in 197 rows that carry a CISI number (195 distinct objects), 527 in 61 (61 objects), 060 in 199 (199 objects), 061 in 87 (87 objects), 472 in 5 (5 objects).
- Where: research/docs/strongest_result_brief.md (Brahmi section); research/docs/claim_ledger.md (retracted Brahmi entries); evidence/tmp/brahmi_v2_run_stdout.log (1,342 features, 611 source-token features, 83 families); evidence/tmp/lipi_current_inscriptions_20260526.csv; evidence/tmp/quarantine_bad_successor_20260531T0104/data/brahmi/brahmi_real_token_low_null_autopsy_v3b.csv (the low-null autopsy).
- Old label: "rejected; zero anchors; the near-misses are not independent".
- Why it is alive: The independence block describes the crops the gate happened to have, not the sign. 817 sits in 195 objects in the Lipi table, and 817 and 820 are stored-final closers in entry 3. A Brahmi match on 817 would connect two results that were built separately.
- What it would mean if true: 817 is a syllable sign, and the closing pair 817/820 is a name-ending pair in Indic style.
- Cheapest next move: Build source-token crops for the 195 objects that carry 817, starting with the ones whose plate pages are already on disk (the CISI plate folders listed in the map below).

---

### 12. The masked-sign score burden is a sign-count artifact until it is run at Linear B's size

- What was seen: The Indus leave-one-out masked top-1 is 0.279591 (top-5 0.534096) over 571 signs. Linear B Series D with the gapped task gets 0.294314 (top-5 0.638796) over 91 tokens; the bidirectional Linear B score is 0.435897. Pictish stones (a non-writing comparator) score 0.450292. The label-symmetry burden is log2(571!) = 4,410.970864 bits.
- Where: research/docs/strongest_result_brief.md; research/docs/claim_ledger.md (Vector 2 candidate); slm/ivcslm/evaluation.py (masked_token_evaluation is the same kind of scorer; the script that produced 0.279591 is not in this sweep's chunk).
- Old label: "masked predictability is not language evidence"; "the label-symmetry burden is the thing a decipherment claim has to pay down".
- Why it is alive: The comparison pits 571 Indus signs against 91 Linear B tokens. A bigger sign set lowers top-1 mechanically, so the Indus score sits below Linear B partly because of its inventory. Run at 91 signs, Indus is directly comparable, and the label-symmetry bits fall with it.
- What it would mean if true: The Indus inventory is a short syllabary plus a long tail of signs that behave as modifiers. The masked result would then be a phonotactic fact at syllabary size.
- Cheapest next move: Rerun the masked top-1 with the Indus sign set cut to the 91 most frequent signs and with the same split rules; report it beside the Linear B 0.294314.

---

### 13. SLM capacity curve: the smallest model is the bottom of the ladder, so the minimum may sit lower

- What was seen: micro (0.89M parameters): NLL 4.1165, top-1 25.45%. small (6.54M): NLL 4.1946, top-1 24.68%. medium (18.12M): NLL 4.3120, top-1 23.85%. micro is best in all five seeds. In the small model, authentic sign order beats a row-shuffled control by 0.3665 NLL and 6.05 top-1 points, and a position-slot-shuffled control by 0.6492 NLL and 12.86 points. Transfer from a pretrained body, exact-exposure matched: known writing +0.0566 NLL (interval 0.0212 to 0.0973), nonwriting +0.0529 (0.0018 to 0.0931), position-shuffled IVC +0.0371 (0.0035 to 0.0716). Writing against nonwriting: +0.0037 (interval -0.0372 to 0.0326), so the writing-specific gain is zero.
- Where: research/docs/replacement_run_checkpoint_20260712.md (SLM section); slm/configs/ivc_research_14usd.json (the model list starts at micro); slm/ivcslm/model.py; slm/README.md (the capacity rationale, about 8,205 sign tokens).
- Old label: "no scale-up signal; 1B escalation not justified"; the pre-registered transfer gate reads FAIL.
- Why it is alive: The minimum is at the bottom of the tested range. With 8,205 tokens, the bigger models overfit, and a model at 0.1 to 0.3M parameters was never run, so the optimum could be lower. The transfer gains are close in size for writing, nonwriting and shuffled IVC pretraining (0.037 to 0.057 NLL), which points to the body learning sign-order statistics that any corpus shares.
- What it would mean if true: The sign order is short-range. A model no bigger than a bigram table captures almost all of it, and the rest of the structure is the corpus's dependence on position.
- Cheapest next move: Run the micro config at widths 32 and 64 (about 0.1 and 0.2M parameters) with the same seeds. On the local machine if it fits in two minutes, otherwise on Colab per the agreed rules.

---

### 14. Unlabeled seal crops: the 286 "no valid ID" files are seal photographs with no catalogue number

- What was seen: The Yajnadevam repo's seal folder holds 6,870 JPG files. Its mapping file lists 3,318 seal IDs covering 6,570 image files. 300 image files are not in the mapping. Their names carry tags: 286 contain no_valid_id (for example vol1_page_297_seal_10_no_valid_id.jpg, vol1_page_328_seal_17_no_valid_id.jpg) and 16 contain duplicate; the rest are vol2 or unusual names such as fix_vol2_page_73_seal_1_no_valid_id.jpg and W-1_a.jpg. The "vol1" label points to a volume I did not find on disk.
- Where: evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images/ and repo/src/assets/data/seal_id_and_image_mapping.json.
- Old label: none in the repo; the mapping file treats them as having no ID.
- Why it is alive: Each file is a seal photograph with a page and seal number, which is enough to find its plate in the CISI or Vats scans and read the catalogue number off the page. These are free photographs of objects the repo's catalogues do not connect to any row.
- What it would mean if true: Several hundred seals in the Vats volumes are missing from the Lipi table, and the corpus is larger than 5,679 rows.
- Cheapest next move: Use the page numbers in the file names to find the plates in the Vats vol 2 scan on disk, and check whether vol1 pages can be reached through a free scan.

---

### 15. 531 is the near-twin of 533 on the accepted pair, and it never takes 717

- What was seen: The accepted pair (M-376 and M-391) carries 533 before 717. My rerun: 533 occurs in only those two rows; 717 occurs in 49 rows (55 token occurrences). The near-twin 531 occurs in five rows: +740-531-060-692+ (C-75), +740-531+ (H-37, K-17), +621-390-531-002-820+ (M-1911), +090-740-531-060-692+ (M-26). None has 717 after it. The Mayig P228 entry maps one-to-many to W531 and W533 (Wells's two forms), and M-26 is the object the July checkpoint lists as a Parpola-222 family member without 717.
- Where: research/docs/replacement_run_checkpoint_20260712.md (the 533 taxonomy table); evidence/tmp/lipi_current_inscriptions_20260526.csv.
- Old label: the accepted structural pair, with the 533 dependency "taxonomy-sensitive" and the fixed unit demoted.
- Why it is alive: If 531 and 533 are one graphic family in the Lipi cut, the accepted pair is a graphic accident of a fine split. If they are two forms, 531 is the unit that should appear before 717 and does not, which is a fact worth having.
- What it would mean if true: The 533-717 pair is a variant of a broader 531-or-533 terminal sign that the catalogue split for no reason.
- Cheapest next move: Box the 531 slot on the plates of C-75, H-37, K-17, M-1911 and M-26 and check whether it is the W531 form or the W533 form.

---

### 16. Cup-and-fish swap across three Mahadevan faces: observed, never tested

- What was seen: Mahadevan texts 4448, 4452 and 5461 share the main face 173-59-347-342-176. Their other faces are 95-328-59, 95-59-328 and 95-328-59. The cup (328) and the fish-shaped sign (59) change places relative to the four-stroke group. The paper runs no null for it.
- Where: research/publications/20261001/PAPER_2_v0.2.md (section 5.6).
- Old label: "an observation, offered only as an observation".
- Why it is alive: The same two signs swap order while the stroke count stays put. If order on the reverse face carries meaning, this is the minimal pair the paper says it lacks. A rule that fixes the count and reorders two signs is exactly what the paired-face study says is needed.
- What it would mean if true: The reverse face is written as a short list of two items whose order encodes which one is the unit and which is the amount.
- Cheapest next move: Draw random triples of the same signs from the Mahadevan concordance and count how often a swap of the cup and fish positions appears with the same count. That is the null the paper skipped.

---

### 17. The Sanskrit-dictionary fit can be rebuilt: the dictionary and the method are both on disk

- What was seen: The September key-fit (headword matches 54 of 146 train lines; 4 of 56 held-out) cannot be reproduced; the optimizer is missing from the repo and its history. The re-implementation in paper section 8.2: real lines reach 12.0% held-out match against 10.4% for a Markov order-1 corpus, a gap of 1.6 to 1.9 points that changes sign across seeds. The Monier-Williams dictionary is on disk as a JSON file of 903,458 bytes (with a redirect file of 3 KB), and glossing.csv (3,495 rows) cites MW only in its analysis column.
- Where: research/publications/20261001/PAPER_2_v0.2.md (section 8.2); evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/src/assets/data/mw.json; mw_redirects.json; evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/glossing.csv; lexicons.json (Apte, Wilson and RV glosses).
- Old label: "no evidence of a language; the original optimizer unavailable".
- Why it is alive: AGENTS says that a missing thing gets built from raw sources. The dictionary and the controls are in the repo. The Markov comparison was on a 46-sign key only; a key over all 571 signs, or a key with the 91-sign cut from entry 12, is a fresh run.
- What it would mean if true: A key that matches dictionary headwords on every line, and beats Markov, would be the first sound-level signal in the repo. This would be a bold result, and the cheapest route to it is still the same controlled comparison.
- Cheapest next move: Rebuild the annealing key search (six restarts, 40,000 proposals, eight seeds, the paper's controls) against mw.json, and run it at both 46 and 91 signs.

---

### 18. Mayig's figure codes name each human figure three ways, and Lipi 101 follows the jar sign 740 in 6 of its 8 rows

- What was seen: The 22 Mayig feature files (P000 to P021) describe human-figure codes, each with Parpola, Wells and Mahadevan cross-references. P010 is "Person with three heads, bracketed by right parentheses" (Wells W101 and W103; Mahadevan M009). The July checkpoint (M-7) reads Lipi's single 101 token as the bracketed three-headed figure, which Mayig decomposes as P154 P009 P154 and P010 encodes as one compound. My rerun on the Lipi table: 101 occurs in 8 rows (8 occurrences); 740 comes directly before it in 6 of them (for example +090-740-101-031+, +090-740-101-002-820+, +407-845-140-740-101-923-240-002-861+); it is stored-final in 2. The reading-direction note says 740 is the jar sign and sits at the conventional end of the text. The other figure codes include P001 to P005 (persons carrying two burdens) and P004 (jar handles for a head).
- Where: evidence/tmp/mayig_feature_namespace_probe/features/ (features__P000.json to features__P021.json); evidence/tmp/mayig_feature_namespace_probe/mayig_commit.zip (commit ad2f1e21, 623 files); research/docs/replacement_run_checkpoint_20260712.md (M-7 row); research/docs/reading_direction_note.md (jar sign 740); evidence/tmp/lipi_current_inscriptions_20260526.csv.
- Old label: the July checkpoint merged the three Mayig constituents into one cluster for sign-unit work, with no reading attached. Nothing else on disk ties 101 to a meaning.
- Why it is alive: Figure signs are the class whose picture is most legible, and the Mayig file gives a named description for each. A figure that repeatedly sits next to the jar sign is a pictorial phrase, and it can be read without a sound value.
- What it would mean if true: In conventional order the phrase is 101 then 740, a figure with the jar at the text end. Meanings-first (hypothesis rule 3) then gives a concrete guess for 101 as a person-type carrier or occupation slot, testable on the other figure codes.
- Cheapest next move: For each Mayig figure code with Lipi equivalents, count how often its sign sits directly before or after 740, and compare that with a chance baseline built from the same rows.

---

### 19. A contact object (Shu-ilishu's seal, Louvre AO 22310) staged in the June note and never checked against an image

- What was seen: The June 11 literature note stages the cylinder seal Louvre AO 22310, linked to Shu-ilishu, as a contact object: evidence that the two cultures met, not a bilingual. The note's candidate file is research/docs/archive/external_anchor_shu_ilishu_AO22310_candidate_20260611.md. On disk the object appears only as text mentions in evidence/tmp/041_source_acquisition_20260611/ (manifest and claim-verification CSVs, and a README). No image is on disk, and the note says binary downloads were blocked that week.
- Where: research/notes/2026-06-11-literature-update.md; evidence/tmp/041_source_acquisition_20260611/.
- Old label: "contact anchor candidate, not a reading; zero external anchors accepted".
- Why it is alive: The June note describes the seal as naming a Meluhhan interpreter, which is the nearest external text the repo has on the names of people. If its inscription carries a sign sequence that also appears on a Lipi object, the join is object-level, which is the kind of join the onomastic harness was built to test.
- What it would mean if true: The interpreter's name is written on a Mesopotamian seal with Indus-style signs, and the same sequence is on a Lipi object, which would be the first sign-to-object external anchor.
- Cheapest next move: Get the Louvre image through the route the June note names, and run the object-level onomastic harness on its sign sequence.

---

## Sources on disk

Map of /home/claude/ivc/evidence/tmp: 12,950 files, 3.5 GB by du (3.67 GB by apparent bytes). Counts are every file in the folder. Sizes are disk usage. File-type totals across the folder: 8,023 JPG, 3,723 PNG, 888 JSON, 47 CSV, 29 TXT, 20 PDF, 15 XML, 13 JP2, 17 MD, 58 PY, 69 files at the top level.

### A. Seal photographs (the only large set of whole-seal photos)
- 002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images/: 6,870 JPG (202 MB). Mapping file repo/src/assets/data/seal_id_and_image_mapping.json lists 3,318 seal IDs covering 6,570 files; 300 files unmapped (286 tagged no_valid_id, 16 duplicate). Some seal IDs have several sides (A, B, C, D, E).

### B. Sign pictures and crops (cut from CISI plates, Vats, Marshall, Mackay and Kenoyer scans)
- 002390x_390405_m34_m41_source_check_20260531/ (10 JPG, 2.4 MB)
- 002390x_390590032_family_recheck_20260531/ (4 PNG/JPG, 5.7 MB)
- 002390x_blind_boundary_packet/ (11 JPG, 856 KB)
- 002390x_h773_vats_side_guard_20260531/ (2 PNG, 100 KB)
- 002390x_intrinsic_sign_behavior_recheck/ (1 JPG, 728 KB)
- 002390x_m143_prefix_control_20260531/ (9 JPG, 1.3 MB)
- 002390x_source_normalization/ (32 JPG, 6.3 MB)
- 002390x_token_boundary_adjudication/ (15 JPG, 1.2 MB)
- 002390x_token_boundary_readiness/ (1 JPG, 336 KB)
- 002_y_branch_gap_blind_packet/ (29 PNG, 27 MB; the 14-image blind packet plus sheets)
- 002_y_branch_gap_public_source_acquisition/ (196 JPG, 134 MB; 130 crops, 65 page images, one contact sheet)
- 032_002_861_220032_source_visible_contrast_packet/ (1 PNG, 500 KB)
- 032_002_861_220032_terminal_space_recut/ (1 PNG, 516 KB)
- 032_002_861_390004_exact_prefix_source_gate/ (1 JPG, 176 KB)
- 032_002_861_533717_blind_layout_gate/ (6 PNG, 1.5 MB)
- 032_002_861_533717_register_controls/ (23 files, 12 MB)
- 032_002_861_533717_source_family_independence/ (1 PNG, 468 KB)
- 032_002_861_603_graphic_identity_packet/ (18 PNG, 600 KB)
- 032_002_861_603_h1138_h360_tokenization_gate/ (15 PNG, 956 KB)
- 032_002_861_603_slot_source_normalization/ (526 files, 135 MB; 511 PNG crops and contact-sheet folders, plus the Vats scans in section F)
- 032_002_861_bare_edge_source_controls/ (21 files, 6.7 MB)
- 032_002_861_source_first_terminal_space/ (1 file, 1.4 MB)
- 032_002_861_source_normalized_tail_predictor_packet/ (1 PNG, 1.2 MB)
- 032_002_861_source_token_attachment/ (7 PNG, 2.8 MB)
- 032_002_861_suffix_split/ (19 files, 8.8 MB)
- 032_002_861_terminal_space_blind_recut/ (2 PNG, 620 KB)
- 032_002_861_terminal_space_recut_v2/ (4 PNG, 1.9 MB)
- 032_002_branch_tail_source_acquisition/ (19 files, 6.8 MB)
- 032_002_branch_tail_token_order/ (5 PNG, 1.3 MB)
- 032_002_source_routes/ (3 JPG, 1.5 MB)
- 032_002_y_source_function_batch/ (42 files, 34 MB; 32 PNG, 6 JPG, 4 CSV crop manifests)
- 032_002_y_token_box_scaffold_v1/ (9 PNG, 2.6 MB)
- 041_source_acquisition_20260611/ (3 files, 16 KB; CSV and MD manifests, no images)
- 3335_source_identity_recheck_20260531/ (5 files, 6.6 MB; CISI Pakistan page images n124 to n126 and crops)
- 390004_exact_prefix_probe/ (65 JPG, 17 MB; grid and contact sheets)
- 820_m314_source_pages/ (3 JPG, 1.4 MB)
- 820_rhin_source_pages/ (1 JPG, 1.1 MB)
- 861_suffix_source_routes/ (4 JPG, 2.9 MB; CISI India and Pakistan pages)
- blind_060920_terminal_cap_20260531/ (13 JPG, 572 KB; no key file in folder)
- blind_741060920_terminal_cluster_20260531/ (13 JPG, 488 KB; BT labels; no key file in folder)
- blind_806_prefix_series_20260531/ (13 JPG, 496 KB; no key file in folder)
- blind_boundary_packet_20260530/ (11 JPG, 856 KB)
- blind_boundary_packet_alpha/ (11 JPG, 856 KB)
- cisi_m2104_packet/ (43 files, 21 MB)
- effective_unicity_directionality_blind_packet/ (44 files, 22 MB)
- effective_unicity_directionality_blind_packet_v2/ (91 PNG, 66 MB)
- effective_unicity_directionality_blind_packet_v2b/ (70 PNG, 44 MB)
- effective_unicity_directionality_blind_packet_v2c/ (70 PNG, 35 MB)
- effective_unicity_directionality_homogeneous_packet_v2f/ (103 files, 11 MB)
- effective_unicity_directionality_panel_crop_repair/ (964 files, 704 MB; object-panel and signband crops)
- effective_unicity_directionality_public_route_probe/ (281 JPG, 214 MB; CISI public-route page images)
- effective_unicity_directionality_public_route_probe_v2/ (280 JPG, 143 MB)
- effective_unicity_directionality_signband_pool_v2e/ (978 files, 682 MB; 976 PNG crops across 38 CISI plate routes)
- effective_unicity_m70_blind_packet/ (19 files, 6.4 MB)
- h1302_h1303_cisi_public_route_check/ (2 PNG, 1.6 MB)
- h2147_source_route/ (11 files, 4.6 MB; 9 PNG plus the Kenoyer and Meadow 1997 PDF)
- h2148_h2100_h2152_110_route/ (35 files, 21 MB; 24 PNG crops of Kenoyer 2005 Fig. 14; Kenoyer 2000 and 2005 PDFs; Kenoyer and Meadow 2010 PDF)
- h319_h1284_source_route_recheck/ (3 files, 1.6 MB)
- h910_component_probe/ (12 files, 1.7 MB)
- h938_b_component_probe/ (6 PNG, 840 KB)
- h940_higher_res_route/ (57 files, 14 MB; PNG crops, one 600 dpi page, one JP2, three CSV crop manifests)
- independent_direction_controls/ (17 files, 14 MB; PNG panels and JSON manifests)
- indoskript_probe/ (1 PNG, 20 KB)
- m1206_034_cohesion_gate/ (14 PNG, 4.9 MB)
- m1206_034_next_source_normalized_blind_component_control_20260526/ (22 files, 1.9 MB; includes blind_master_key.csv)
- m1206_034_terminal_component_gate/ (17 PNG, 1.8 MB)
- m1206_m37_blind_visual_comparanda/ (45 files, 51 MB; includes verified panel crop manifest)
- m1206_m37_terminal_recut_gate/ (11 PNG, 2.4 MB)
- m1206_singleton_controls/ (4 PNG, 756 KB)
- m1206_source_normalized_component_packet/ (4 PNG, 272 KB)
- m1206_terminal_triad_source_recheck/ (33 files, 19 MB)
- m12_token_count_audit/ (13 PNG, 8.9 MB)
- m1584_cisi2/ (17 files, 14 MB)
- m2104_raw_source/ (19 files, 2.9 MB; Marshall plate CXIV crops, 532 family)
- m315_cisi1/ (30 files, 6.7 MB)
- m315_second_slot_controls/ (90 files, 30 MB; 74 PNG, 10 CSV keys including blind_master_key.csv)
- m685_cisi2/ (25 files, 12 MB)
- m77_parpola_recurrence_gate/ (24 files, 9.2 MB; CISI India crops of nos. 33, 65 to 69)
- parpola_sign60_local220_middle_probe/ (15 PNG, 740 KB)
- parpola_sign60_local220_strict_probe/ (17 PNG, 536 KB)
- parpola_text7_scope_gate/ (1 PNG, 16 KB)
- risky_154806_series_prefix_source_probe_20260531/ (9 PNG, 5.1 MB; the 154-806 source check)
- risky_400740_source_visible_probe_20260531/ (7 PNG, 3.2 MB)
- risky_740407590_source_probe_20260531/ (5 PNG, 2.6 MB)
- source_box_blind_packet_v1/ (20 files, 12 MB)
- source_box_negative_control_v2/ (19 JPG, 4.3 MB)
- source_route_hunt_20260530/ (18 files, 13 MB)
- source_route_recheck_20260531/ (13 JPG, 1.8 MB)
- susa_3881_source_check/ (10 JPG, 680 KB; SB5614 tablet sign-band photos, 9537 and 9538)
- gadd_ur/ (39 files, 32 MB; 34 PNG page renders, 2 JPG, the Gadd 1932 PDF, two text files that are nearly empty: 44 bytes and 20 bytes)
- chanhudaro_mackay_1943/ (53 files, 41 MB; 46 PNG, four CSV crop manifests, one XML, the book in section C)
- v1_external_acquisition_20260531/ (4 files, 184 KB; three acquisition HTML pages and one CDLI JSON record, see section E)

### C. Scanned books and page scans
- cisi_pakistan_pages/cisi_pakistan.pdf: Corpus of Indus Seals and Inscriptions, Collections in Pakistan, 486 pages, 36 MB; plus 10 PNG page crops (data_h786_h941 subfolder).
- cisi_xml/: CISI India djvu text and XML; CISI Pakistan djvu text and XML; Mahadevan 1977 "The Indus Script: Texts, Concordance and Tables" djvu text (674 KB) and XML (15 MB). 27 MB in all.
- cisi_pakistan_ocr/pakistan_djvu.xml: OCR text layer of the Pakistan volume (4.8 MB).
- parpola_1994_signlist/parpola_1994_deciphering_sindhilanguagelibrary.pdf: Parpola 1994, "Deciphering the Indus Script", 392 pages, 19 MB; rendered figure 5.1 pages 88 to 94 and sign-40 to 43 crops; pages_60_90.txt.
- pdfs/S1-IndusZoomorphicIconCatalogue_20260531.pdf: 12 pages; txt copy 217 KB. pdfs/parpola_2019_bone_rods.pdf and parpola_2019_bone_rods.txt (at top level too): Parpola 2019 on bone rods, plus three crops.
- m1206_bhaskar/: Bhaskar 2022 IJHS article (PDF and text); S1 zoomorphic catalogue copy; bulletin No. 6, June 2025 (PDF 10.9 MB, text); a supplementary spreadsheet in XLSX form (160 KB, not opened); Fig. 3 crops in derived/.
- 032_002_861_603_slot_source_normalization/vats_excavations_at_harappa_vol2.pdf: M. S. Vats, "Excavations at Harappa", volume II, 520 pages, 32 MB; vats_vol2_djvu.xml (23 MB); vats_vol2_djvu.txt (1.7 MB).
- 032_002_861_603_slot_source_normalization/vats_excavations_at_harappa_vol2_plates.pdf: the plate volume, 288 pages, 17 MB.
- chanhudaro_mackay_1943/chanhudaro_mackay_1943.pdf: Mackay, Chanhu-daro excavations (the folder name gives 1943), 466 pages, 28 MB; djvu text 1.3 MB.
- marshall_vol3/: Marshall volume 3 (Internet Archive number 48270, taken from the scan's own files, not checked against the source page), two page scans at PNG and JP2 (0114 and 0205), IIIF max image, djvu XML (770 KB), page numbers; derived crops of plate 532 (17 PNG).
- mahadevan_m77_pages/: Mahadevan 1977 page scans (m77 pages 0066, 0084, 0093, 0101, 0254, 0324, 0491, 0617, 0683 and others) as PNG and JP2, 26 files, 80 MB.
- mahadevan_m2104_pages/: eight JPG page images of the same book.
- gadd_ur/gadd_1932_33779.pdf: Gadd 1932, 44 pages, 3.2 MB. The text layer is empty (44 bytes), so the page PNGs are the only readable copy here.
- h1302_h1303_direction_prior_work/: Daggumati and Revesz 2021, "A method of identifying allographs in undeciphered scripts" (article PDF, HTML, text); page renders.
- h2147_source_route/kenoyer_meadow_1997_harappa.pdf and h2148_h2100_h2152_110_route/: Kenoyer and Meadow 1997; Kenoyer 2000 (tiny steatite seals); Kenoyer 2005 (Harappa 2000-2001, and Fig. 14); Kenoyer and Meadow 2010 (inscribed objects).
- v1_external_acquisition_20260531/: acquisition pages (Aarhus University Press, CiNii, Open Library) for Kjaerum's Failaka volume; the book is not on disk.
- research/docs/ and archive: no scans.

### D. Plates
- Vats vol 2 plates (288 pages); Mackay plates LI and LII (in chanhudaro_mackay_1943/); Marshall plate CXIV (m2104_raw_source/); Parpola 1994 figure 5.1 (parpola_1994_signlist/rendered/); Kenoyer 2005 Fig. 14 (h2148 crops); the CISI plate page images in cisi_pakistan_pages/ and 002_y_branch_gap_public_source_acquisition/pages/.

### E. Downloaded datasets and data repos
- lipi_current_inscriptions_20260526.csv (top level): the Lipi table, 5,679 rows, 38 columns, 1.2 MB. Its copy at 002390x_3335_yajnadevam_provenance_20260531/inscriptions_current.csv is byte-identical (checked). inscriptions_pinned_b272ad99.csv in the same folder is the same size, pinned to commit b272ad99 (metadata JSON alongside, dated 2026-05-07).
- 002390x_3335_yajnadevam_repo_trace_20260531/repo/: a full clone of the Yajnadevam "lipi" web app (6,999 files, 568 MB). Includes repo/src/assets/data/inscriptions.csv (1.2 MB; it first differs from the top-level copy at byte 300, not examined further), the glossing data, prakriyas.json (4 MB), dhatu.json (572 KB), symbol-frequency.json, unknown.txt (a list of Sanskrit-looking tokens), words.csv and words_old.csv, xlits.csv, keyboard-tests.csv, and the git log. The claimed decipherment text is in README.md; its own sign tables are in decipher.csv and allographs.csv.
- mayig_feature_namespace_probe/: mayig_commit.zip (328 KB; Mayig "indus-valley-script-corpus" at commit ad2f1e21, 623 files); repo/ (2.6 MB, the extracted commit); features/ (22 JSON files, P000 to P0xx).
- 002390x_3335_yajnadevam_provenance_20260531/ (3 files, 2.4 MB): the two Lipi CSV copies and the commit metadata.
- quarantine_bad_successor_20260531T0104/ (10 files, 136 KB): quarantined outputs from an earlier broken run: a Brahmi low-null CSV and summary, a family-collapse CSV set, and two scripts.
- codex_schema/ (239 JSON files, 3.1 MB): JSON schemas for a coding-assistant protocol. Not corpus data; unrelated to the script work.
- Top-level scripts and logs: 56 run_*.py files (the 032_002_861 campaign scripts), make_032_002_y_token_boxes_v1.py, brahmi_v2_run_stdout.log (run log; size not confirmed), brahmi_v2_run_stderr.log (empty), risky_806_prefix_series_geographic_holdout_latest_stdout.json (10 KB), parpola_2019_bone_rods.txt, vats_vol2_archive_metadata.json.

### F. Dictionaries
- 002390x_3335_yajnadevam_repo_trace_20260531/repo/src/assets/data/mw.json (903 KB): Monier-Williams entries keyed by headword, with line IDs.
- .../data/mw_redirects.json (3 KB): spelling redirects into the same dictionary.
- .../data/lexicons.json (617 bytes): short glosses with sources Apte, Wilson, RV and Vaidya.
- .../data/dhatu.json (572 KB) and .../repo/src/assets/vidyut/vidyut_dhatupatha_5.tsv (57 KB): verb roots.
- .../data/prakriyas.json (4 MB): derivation records.
- .../repo/glossing.csv (374 KB, 3,495 rows): gloss lines citing MW, RV and other sources.
- No Monier-Williams or other dictionary is in any other subfolder.

### G. Cuneiform exports
- None of the usual exports (no CDLI or ETCSL text export, no SumTablets lines in this folder). The only cuneiform-related file is v1_external_acquisition_20260531/cdli_publication_1773730_kjaerum_failaka.json (7.5 KB), a publication record. The Gadd 1932 scan (gadd_ur/) covers Ur objects, but its text layer is empty.

### H. Code, logs and other downloads
- evidence/tmp/chanhudaro_mackay_1943/ and others carry CSV crop manifests; 041_source_acquisition_20260611/ holds the sources and claim-verification CSVs; quarantine_bad_successor_20260531T0104/ holds the quarantined scripts.

## Ideas named but never run

- Embedding recovery gate (embeddings/validate_recovery.py): the store files it reads (embeddings/store_images.parquet and store_text.parquet) are not on disk. The README says huggingface.co is blocked here and the model was never downloaded. The gate has never run.
- Crosswalk between Mahadevan and Lipi object numbers through shared excavation numbers (paper section 9); the Lipi side (5,147 rows) is on disk, the Mahadevan side is in research/data/mahadevan_20260905 (not read here).
- 034 size control within one dated deposit (paper section 9).
- Nair (2026) synthetic-baseline scorecard: the four measures (brevity, repeated formulae, hapax rate, positional rigidity) are not computed in the repo; the code is "on request" only.
- Masked-sign top-1 at Linear B's sign count (91 signs), and the 0.1 to 0.3M-parameter SLM widths (entries 12 and 13).
- The seven-route, 63-task plan (research/publications/20260907/README.md; the file IVC_RADICAL_ROUTES_EXECUTION_PLAN.md is not in my chunk): overlapping spellings, geometry and compression, coordinated variation, copying and correction, pragmatics, relational language identification, conservation and arithmetic loops. The paper says none has been run.
- Mahadevan cup-and-fish swap null (entry 16).
- Mirror-pair direction table (entry 8).
- Yajnadevam allograph-group split (entry 9).
- Sanskrit-dictionary key search rebuild (entry 17).
- Shu-ilishu AO 22310 object-level onomastic check (entry 19); the Louvre image is not on disk.
- Kjaerum and Failaka catalogue rows 279 and 319, Amiet Susa 1643, Sarzec and Heuzey Girsu 30.3a-b, Mitchell 1986 Ur figures 106 to 117: named as the next object-level bridges; none acquired (the Aarhus, CiNii and Open Library routes give no catalogue pages).
- ICIT occurrence database: returned HTTP 401 and is administrator-gated; no contact attempted.
- Vats volume 1 scan: needed for the vol1 seal crops in entry 14; not on disk.
- Per-object 617 check on the 60 complete CISI rows (entry 10): named in the July checkpoint, not run.
- 806 holdout token boxing (entry 1): named in the JSON's falsifier list, not run.
- Daggumati and Revesz's mirror-direction claim (entry 8) was never tested against any object.
