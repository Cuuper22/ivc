# Leads from reader 12: the September four-route campaign and its completion pass

Scope: the chunk 12 reading list (campaign README, TASK_STATUS, the phase plan, route_b, completion README / RECOVERY / WORKED_EXAMPLES, completion route_a, route_b, route_c, route_d, sources, joint, audit, adjudication, evidence_inventory) plus the unlisted result files in route_a..d, integration and completion. All paths are relative to /home/claude/ivc. Counts marked "strict" come from research/data/mahadevan_20260905/concordance_rows.csv (2,575 fully legible texts, the same set the campaign calls strict lines). I ran those counts myself. "Sign N" means catalogue sign N in stored order. "Bits" are description-length or log-loss costs; lower is better. "Held-out" means withheld from fitting.

Glossary for the lead model: "roof" = sign 65 or 66 rewritten by the campaign as 87 plus a fish; "tick" = sign 211 (or 388 in the completion pass) read as a marker; "fish square" = signs 59/60/65/66; "stroke signs" = 86, 87, 89, 95, 96, which the route C labels read as 1 to 5 strokes.

---

### 1. The fish marker may be the wrong sign: 388 and 342 beat 211 on the campaign's own measures

- What was seen: The campaign's structured marker ranking for the broad four-stroke marker puts sign 342 first (score 60116; 6 base signs, 16 distinct pairs), then 211 (score 30111; 3 bases, 11 pairs), then 388 (score 10101; 1 base, 1 pair). The adjudication says 342 "remains the ranking winner after object/alias exclusions". In the completion pass's one-role latent grammar, tick388 costs 49,760.76 data bits and tick211 costs 49,874.77, with identical parameter (2,641.72) and rule (10.70) costs. With two roles, tick388 beats tick211 by 258 data bits (48,065.21 vs 48,323.14). In the frozen joint fit, tick388-after was selected on 6 of 7 tasks. The three-role analysis expands every marked fish as a plain fish plus 388: 66 176 becomes 65 388 176 (boundary probability 0.9925), 87 59 71 becomes 87 59 70 388, 87 60 176 becomes 87 59 388 176. In strict texts, sign 342 is last in 741 of 2,575 texts; sign 211 is last in 162 of the 193 texts that contain it.
- Where: research/campaigns/integrated_20260906/route_a/structured_marker_rankings.json; adjudication/scientific_review.md; route_a/REPORT.md; completion/route_a/summary.json; completion/route_a/latent_segmentation_alternatives.json; completion/joint/summary.json; integration/summary.json.
- Old label: 211 "selected" by the campaign; 388 dropped as "one base, one pair"; completion calls its tick388 model an "alternative multirole model; not global MDL winner" (MDL = description-length score).
- Why it is alive: The campaign's own adjudication keeps 342 as the broad winner, and 211 wins only the narrow fish-only search. The completion data fit prefers 388 over 211 by 114 bits (one role) and 258 bits (two roles). One marker (388) would explain all three marked fish (60, 66, 71) as plain fish plus one sign, which 211 never did for 60 or 71. On this reading 211 is an ending (last in 162 of 193 texts), not the fish marker. Contrary numbers, once: with one role, identity (no marker) beats tick388 on data by 21.7 bits and ties it after cost (52,412.89 vs 52,413.18). Two-role tick388 beats two-role identity by 18.5 bits in total, but only through 64.3 fewer parameter bits; its data are 35.0 bits worse than identity.
- What it would mean if true: Two markers with two jobs. 388 (or another tick) marks "fish with mark"; 211 or 342 closes the expression. The campaign's 87/211 composition would then be built on the wrong tick.
- Cheapest next move: Run the integration field-channel test with 388 and with 342 in place of 211, same held-out masks, and read the field bits next to fish211 (3084.08) and categorical (3087.20).

### 2. Roof 87 plus tick 211 spells both members of the 1380/2452 pair

- What was seen: Object 1380 carries 65 70 211 (raw field-symbol code 251, Mohenjo-daro seal). Object 2452 carries 87 59 71 (raw code 13, Mohenjo-daro seal). Under the campaign rules 65 goes to 87 59 and 71 goes to 70 211, so both expand to 87 59 70 211. Of 290 rule combinations (10 roof options by 29 tick options; 234 reach a stop), roof87-before with 211-after gives 10 expression classes (21 distinct expressions, 2 classes that join a cross-operation pair). Roof109 and roof102, each with 211, give 8 classes. Roof104 with 211 gives 7 classes with 2 cross-operation pairs. With all 70/71 expressions hidden, roof87 gives 9 classes against 8 for the next rival. With all 267–99 expressions hidden, 9 against 7. The 1380/2452 class is the only class with no single-operation edge at all.
- Where: research/campaigns/integrated_20260906/route_a/composition_adjudication.json (ranked list and the 1380/2452 record); route_a/REPORT.md; route_b/FISH_COMPOSITION_CONTEXT.md; completion/sources/1380_2452_adjudication.json; completion/WORKED_EXAMPLES.md.
- Old label: "conditional orthographic analysis; equal meaning not established." The integration joint test ranks the two-operation composite last of 8 (3192.96 bits against 3169.57 for the categorical baseline, 22 bits of rule charge). Field-channel fish211 beats categorical by 3.12 bits (3084.08 vs 3087.20), but the 11-bit rule charge removes that gain.
- Why it is alive: The ranking hid the 70/71 family and roof87 still came first. It predicted an equality (1380/2452) that the search did not build in. The two objects carry different pictures (composite animal, codebook field 25; unicorn, codebook field 01, per completion sources) with one spelled expression, so the spelled form names a role or category rather than a species.
- What it would mean if true: A two-sign grammar (roof = two-stroke sign plus fish; tick = suffix) generates the fish square and the 70/71 family. Sign 70 is then a fish root with its own sign, not an unread sign.
- Cheapest next move: Freeze roof87/211 and the two runners-up, hide 1380 and 2452 as a pair, and predict the spelled form of every strict text that contains 70 or 71. Score the predictions before looking at them.

### 3. A Tamil-conditioned roof87_tick211 beats identity on three held-out tasks

- What was seen: In completion/joint/linguistic_coupling, the Tamil fish/star prior selects roof87_tick211 on recombination_2, recombination_3 and the 70/71 family, where the graphical-only fit selected tick388. Held data totals across all three channels (file values): 70/71 family, identity 2686.12, tick388 2721.76, Tamil roof87_tick211 2678.49 (the Tamil figure is the sum of the text, motif and cup channels in its file). Derived by subtraction: roof87_tick211 is 7.63 bits better than identity on the 70/71 family, 29.03 bits better on recombination_2 (identity 11543.59, roof87_tick211 11514.57), and 9.31 bits better on recombination_3 (identity 10303.34, roof87_tick211 10294.03). The Sanskrit prior selects tick388 on all of these. In the training objective with the Tamil prior, roof87_tick211 beats tick388 by 41.3 bits (63148.91 vs 63190.24).
- Where: completion/joint/linguistic_coupling/unseen_family_70_71__tamil.json, recombination_2__tamil.json, recombination_3__tamil.json; completion/joint/linguistic_coupling/summary.json; completion/joint/recombination_*/summary.json.
- Old label: "lexical-prior energies reported separately; cannot identify a language; no sound or language accepted" (completion RECOVERY and linguistic_coupling summary).
- Why it is alive: The 70/71 family is where graphical-only fit was worst (tick388 at minus 35.64 bits against identity). The one prior that moves the choice to roof87/211, the campaign's own composition, also turns that family from a loss into a gain. Lead 2 and Tamil kal-mīṉ and kōḻi-mīṉ compounds (lead 17) point the same way.
- Caveat, once: the Tamil model maps 59, 67, 72 to the same fish word and sets 211 to a silent classifier. The gain may come from the fish-classifier role and not from the roof spelling.
- What it would mean if true: Roof 87 is a real modifier that a fish-compound grammar pays for, and 70/71 are fish compounds.
- Cheapest next move: Three ablations on the same held masks: (a) roof87 with no tick and the Tamil prior, (b) identity plus the mīṉ classifier only, (c) roof87_tick211 with no lexical prior. Whichever keeps the 7.6, 29.0 and 9.3 bit gains decides it.

### 4. Count signs bind to noun classes: 87 (two strokes) to fish, 89 (three strokes) to the 336 stem

- What was seen: Route C labels 86, 87, 89, 95, 96 as 1, 2, 3, 4, 5 strokes. In strict texts: 87 is directly followed by 59 (41 times) and 60 (11), 52 fish adjacencies in all. Sign 86 precedes a fish sign 8 times, 89 once, 95 once, 96 never. Sign 87 is followed by 328 in 73 positions and begins 122 texts (70 of them with 328 second). Sign 89 sits between 336 and 211: 336 is directly followed by 89 in 96 texts, and 89 is directly followed by 211 in 38. 666 strict texts contain a stroke sign; 727 contain a fish base.
- Where: research/data/mahadevan_20260905/concordance_rows.csv (strict rows); research/campaigns/integrated_20260906/route_c/REPORT.md and summary.json.
- Old label: "catalogue long-stroke counts are graphical observations, not accepted numerical meanings" (route C); the repeat-compression match is "not established equivalence" (route C summary).
- Why it is alive: If sign 87 means two, then roof 65 (two fish) is a numeral fixed to a fish class, and the 52 adjacencies are that construction. The asymmetry is the signal: count 2 binds fish, count 3 binds the 336 stem, and each count takes its own class of noun. This fits the completion result that a categorical count distribution beats arithmetic programs (202.34 vs 275.03 bits on 128 held records, derived difference 72.69 bits).
- What it would mean if true: Stroke signs are classifiers tied to noun classes. Count is written as a class-bound marker, not multiplied.
- Cheapest next move: List the immediate neighbours of all 666 strict texts with a stroke sign, and check whether 87 keeps its fish partner, and 89 its 336 partner, in the partial and non-strict rows.

### 5. The 336–89 stem with 211 as ending: a recurring construction the campaign split two ways

- What was seen: 336 followed by 89 in 96 strict texts; 336–89–211 contiguous in 38 texts (38 objects); 89 followed by 211 in 38. Of 160 strict texts that end in 211 and have a predecessor, 96 have a fish sign just before it (59: 41, 67: 25, 72: 20, 70: 6, 65: 4) and 35 have 89. Text 1147 (387 66 336 89 211): route A proposes a split 387–66 | 336–89–211, and says the suffix occurs in 34 unique texts on 38 objects. Completion's three-role model gives boundary probability 0.001 between 66 and 336. The copper elephant/horned-tiger text 336–89–296–342–98 (objects 3328, 3336, 3368 with raw code 75; object 1704 with raw code 101) begins with the same stem. The retained suffix 67–336–89–211 recurs in the 2275/1008 pair.
- Where: concordance_rows.csv; research/campaigns/integrated_20260906/route_a/REPORT.md; completion/route_a/latent_segmentation_alternatives.json; completion/WORKED_EXAMPLES.md; route_b/REPORT.md; route_d/outputs/bound_marker_scope_test.json.
- Old label: "unresolved segmentation proposal" (route A); "a recurring suffix alone cannot fix the boundary" (completion).
- Why it is alive: The two readings contradict each other (split or no split at 66|336), so the lead keeps both and names the splitting observation. In strict texts, 66 is directly followed by 336 only twice, while 336 is directly preceded by fish bases 65 (17), 72 (14), 70 (8), 67 (7), 59 (7). A noun stem 336–89 with an ending 211 would explain the 1147 boundary, the 2275/1008 suffix and the copper text tail (296–342–98) as one stem with different endings.
- What it would mean if true: 336–89 is a noun stem; 211 is a case-like or number-like ending; the animal picture attaches to the stem and the ending varies.
- Cheapest next move: Compare the 58 strict texts with 336–89 not followed by 211 against the 38 that are, and check whether their remaining signs repeat the copper tail 296–342–98.

### 6. Fish compounds have a fixed order: modifier first, fish head last

- What was seen: 65 is directly followed by 67 in 36 strict texts; 67 is followed by 65 in 3. Other fish-to-fish bigrams: 67 then 72 (19), 65 then 72 (14), 65 then 59 (12), 59 then 67 (9). Roof 87 precedes 59 or 60 in 52 texts. The pair 267 then 99 occurs 222 times; 99 then 267 never occurs.
- Where: concordance_rows.csv; research/campaigns/integrated_20260906/route_a/REPORT.md ("roof before the fish"); route_d/REPORT.md (Tamil fish compounds kaṉ-mīṉ, kōḻi-mīṉ, kallu-k-kōḻi-mīṉ).
- Old label: "bound-morpheme claim refuted" (route D). That refutes only "211 is bound to a base": 211 follows a tested base in 101 strict occurrences and does not in 93. It says nothing about fish-to-fish order.
- Why it is alive: In the Tamil fish compounds the modifier comes before mīṉ (fish) in 88 of 89 exact forms. The Indus fish-to-fish order is lopsided, 36 to 3. Roof 65/87 and tick 211 both come before the fish, as route A set up. A compound grammar (modifier, then fish head) joins the roof, the stacked fish and the Tamil forms without an extra rule.
- What it would mean if true: Fish-fish pairs are compounds. Sign 65 is a modifier and 67 a head; the fish square is a set of compound heads.
- Cheapest next move: For the 36 texts with 65 then 67, record whether 211 follows the 67 (head) each time. Print the 3 reversed 67 then 65 pairs. Both printouts are one tabulation.

### 7. The final slot is a small inventory, and sign 342 leads it

- What was seen: Last sign in strict texts: 342 (741 of 2,575), 176 (257), 328 (250), 211 (162), 169 (102), 15 (80), 162 (77), 1 (65), 12 (55), 254 (51). All four roof exact contexts end in 342: 65 348 342, 65 48 342, 87 59 348 342, 87 59 48 342. The 358 construction ends in 342 in 26 of its 28 texts.
- Where: concordance_rows.csv; route_b/frozen_358_transfer.json; route_b/REPORT.md; route_d/outputs/coverage_not_accuracy.json (80 standalone 211 expression types).
- Old label: none for the final slot as a class. Route A calls 342 the "broad transfer marker" and 211 the narrow fish marker.
- Why it is alive: A short, closed set of final signs is what a case or number ending looks like. The roof rule's four exact contexts all end in 342, so the roof rule may be conditioned on that ending rather than on the fish. The 342 ending also gives the broad marker its 16 distinct pairs (lead 1).
- What it would mean if true: 342 closes the expression. Roof spelling depends on whether the text ends in 342.
- Cheapest next move: Count strict texts with 65 or 66 that do not end in 342, and check whether the roof rule's predicted spelling holds for them. The campaign has only tested roof 65 in 342-final texts.

### 8. Sign 12 is text-final, and the one counterexample to the 358 rule adds it

- What was seen: Sign 12 occurs in 62 strict texts, final in 55; raw picture code 13 appears in 34 of the 62 and on 33 of the 55 final texts. Sign 358 occurs in 28 strict texts. The only strict text with both 12 and 358 is 7244 (204 245 358 342 12, raw code 13, sealing, medium 2). The 18 defining copper objects carry 204 245 358 342 with raw codes 145 and 147. Six non-copper constructions carry 358 with raw code 13 and no 12.
- Where: concordance_rows.csv; research/campaigns/integrated_20260906/route_b/frozen_358_transfer.json; route_b/REPORT.md; adjudication/scientific_review.md.
- Old label: "B-358-LITERAL" rejected by 7244 under a direct-depiction reading. The adjudication says the rejection is narrow: it does not reject lexical, copper-only or compound-dependent uses of 358.
- Why it is alive: The counterexample differs from the defining cases by one final sign (12) and by picture code 13 instead of 145/147. The rule may hold for the core before a terminal. Sign 12 may be the switch that moves a text to picture class 13: 33 of 55 final-12 texts carry 13.
- What it would mean if true: Sign 358 names the copper category in its core, and terminal 12 changes the picture class.
- Cheapest next move: Among the 55 final-12 texts, find those with a copper-type core (a complete 342-final core with raw 145 or 147 on the other face) and see whether they carry 13 or 145/147.

### 9. The reverse cup count does not follow from the front, and the front-count pairs are a tally

- What was seen: Front 48 342 176 has reverse counts 2, 3 and 4, with 23, 10 and 2 witness rows (route C's own table). Front 119 87 342 176 has counts 2 and 3 on objects 4444/4456 and 5498; route C's prose and its JSON disagree about which object gives which count, and I have not resolved that. With the doubtful sign 119 read as given, objects 4581 and 4591 give 4. Object 4493 (66 176) has reverse count 4 and object 4556 (87 60 176) has 2. Completion route C reports 14 families with equal fronts and different reverse counts. An independent per-front count distribution beats arithmetic programs by 72.69 bits (202.34 vs 275.03, 128 held records). The campaign's fitted constant (3) beats the shared multiplier, 1.182 vs 1.918 nats.
- Where: research/campaigns/integrated_20260906/completion/route_c/equal_face_counterexamples.json; completion/route_c/REPORT.md; route_c/REPORT.md; route_a/REPORT.md (4493/4556).
- Old label: "identical-front, different-reverse counterexample; no arithmetic and no unit" (route C).
- Why it is alive: A counterexample only if you assume the front fixes the reverse face. Swapping sign 66 for 87 60 changes the count from 4 to 2 on the same 176. A tally that changes when one sign is swapped is a field with its own driver.
- What it would mean if true: The reverse face is a receipt-like count with its own driver (locus, level, medium or object form).
- Cheapest next move: Regress reverse count on locus, level, medium and object columns for the front 48 342 176 objects. The columns are in concordance_rows.csv.

### 10. Object form decides whether the second face is written or pictured

- What was seen: Shape classes alone predict the reverse-channel type on 37 of 44 legible reconstructed copper types, against 26 of 44 for the constant picture baseline. Seven exceptions are recorded, including mixed text-and-picture B12.
- Where: research/campaigns/integrated_20260906/route_b/REPORT.md; route_b/summary.json (shape_reverse_channel_types_correct 37, scored 44); route_b/published_copper_type_network.json.
- Old label: "supports object form as an explanatory variable; does not identify a workshop" (route B).
- Contrary number, once: the completion complementary-field model (shape plus context) scores 4932.81 bits on held families against 3961.71 for the independent model, 971 bits worse (derived).
- Why it is alive: One variable, object form, gains 11 of 44 types over a constant guess, with no text used. That is a document-type rule: a seal-like object carries a written face, a tablet-like object carries a picture.
- What it would mean if true: Object form tells the reader what kind of record a face is. No workshop label is needed.
- Cheapest next move: Score shape-only against shape plus site, on the same 44 types, held out by family. The 971-bit loss suggests site adds noise, so shape alone is the first arm to run.

### 11. Site and medium predict the held expression better than the text components do

- What was seen: On 1,081 held-out expression types: site and medium 740 correct, 2186.96 bits; text components 718 correct, 2498.46 bits; all three combined 747 correct, 2219.46 bits. Margin favouring site and medium over components: 311.50 bits (derived). In the completion nine-model run, components with context score 9426.20 bits against 3961.71 for the independent model.
- Where: research/campaigns/integrated_20260906/route_b/summary.json and REPORT.md; completion/route_b/REPORT.md; completion/route_b/competition.json.
- Old label: "no predictive win for a semantic component model" (route B).
- Why it is alive: The defender of a production-context reading argues that the carrier (site, medium, shape) chooses the formula, and meaning does not need to be invoked. The 1380/2452 pair is both Mohenjo-daro seals with direction 1 and the same spelling, but different pictures. That is the context signal the campaign flagged. This reading does not rule out a semantic one: it says the choice of spelling is contextual and the text carries the meaning.
- What it would mean if true: Expressions are formulas tied to production context, and the picture is chosen separately.
- Cheapest next move: Add site and medium conditioning to the roof87/211 composition and ask whether it predicts the 1380/2452 spelling on the held-out family without the 1380/2452 pair. One fit.

### 12. A one-sign swap in the first slot: 4581 against 4591

- What was seen: Objects 4581 and 4591 share faces 2 and 3 (face 2 is *119 87 342 176, with the doubtful sign 119 making it non-strict; face 3 is 95 328). Their first faces differ: 4581 carries 137 (one sign) and 4591 carries 59 (a fish). Both have reverse count 4 per route C.
- Where: research/data/mahadevan_20260905/concordance_rows.csv (rows 4581:10/20/30 and 4591:10/20/30); research/campaigns/integrated_20260906/route_b/decisive_object_contrasts.json; route_c/REPORT.md.
- Old label: "compatible with a further selector or complementary field; doubtful 119 stays doubtful" (route B).
- Why it is alive: A fish sign and a non-fish sign in the same first slot, with the rest fixed, is a clean slot test. Sign 137 occurs in 19 strict texts and begins 4; sign 59 begins 39. If the first slot is a selector for item class, the fish identity lives in the slot, not in the object name.
- What it would mean if true: The first slot picks the item class; sign 59 is the fish slot value and 137 another class value.
- Cheapest next move: Find every text whose last two faces match 4581's and list the first-slot signs. If 137 and 59 are the only two values, the slot is a two-value field.

### 13. Ka: the one suffix that survives across word categories

- What was seen: Route D's Sanskrit search, under the all-eight-fish prior, gives 360 systems, all with the suffix ka, six root pairs (cezwa→cezwaka, rAjIva→rAjIvaka, pallava→pallavaka, trikaRwa→trikaRwaka, daRqapAla→daRqapAlaka, siMhatuRqa→siMhatuRqaka). The same search over 451 bird headwords again gives only ka (7 root pairs). Over 542 tree headwords it gives ka (12 pairs) plus ja and pa (4 pairs each). On 16 fixed 259-word subsets per category, ka survives in 5 of 16 bird subsets and 5 of 16 tree subsets, and no other suffix survives any of those subsets. In the Indus data, sign 211 follows 15 different signs in strict texts: five fish signs and 89, 155, 176 and others.
- Where: research/campaigns/integrated_20260906/route_d/outputs/semantic_category_control.json; route_d/outputs/summary.json; route_d/REPORT.md; concordance_rows.csv.
- Old label: "not fish-only; general word-extension structure selects it" (route D). Route D keeps it as a conditional constraint, not an identification.
- Why it is alive: The fish-only prior is what narrows the field to ka. Remove that prior and the category sweep still gives ka. In the Indus data, 211 is not fish-only (89 then 211 in 38 texts), which is what a general suffix looks like.
- What it would mean if true: If sign 211 is any suffix, ka is the best-fit sound for it, conditional on the Sanskrit dictionary forms.
- Cheapest next move: Predict which signs can precede 211. "Any-root suffix" predicts the full 15-sign set. "Fish-only" predicts 5. Count held texts to decide.

### 14. The repeated-base null is a power failure: the pattern is rare

- What was seen: The bigram 59 59 occurs 5 times in 2,575 strict texts. Route D's null: zero exact counterparts for the composed spellings 65 to 59 59, 66 to 59 59 59 and 66 to 60 60, across 123 occurrences of 65 after 195 objects were removed. Route C found the repeated-base form once (object 4232, 267 99 59 59 211), with 24 of 120 label permutations matching it as well.
- Where: concordance_rows.csv; route_d/REPORT.md; route_d/outputs/counted_fish_composition.json; route_c/repeat_compression_candidates.json and summary.json.
- Old label: "no additional written-repetition transfer" (route D); "one-frame candidate" (route C).
- Why it is alive: With 5 occurrences of the pattern in the entire strict set, zero counterparts is what a rare spelling gives. The project's rule is that a null means the test was wrong, so the test should be redesigned at least once.
- What it would mean if true: A repeated fish is a rare spelling of "two fish"; the common spelling uses 87.
- Cheapest next move: Redesign the test around 65 followed by 59 (12 texts) and 65 followed by 67 (36 texts), and check whether the roof-65 spelling predicts each.

### 15. The 267–99 header: a fixed opening formula across four sites

- What was seen: Sign 267 begins 224 strict texts, the most common opening sign. The pair 267 then 99 occurs 222 times; 99 then 267 never occurs. Route B places the frame at four sites: Lothal, Chanhudaro, Mohenjo-daro and Harappa.
- Where: concordance_rows.csv; research/campaigns/integrated_20260906/route_b/FISH_COMPOSITION_CONTEXT.md; route_a/REPORT.md.
- Old label: "geographically confounded; no within-city contrast for this chain" (route B).
- Why it is alive: A heading used at four cities is a formula, not a local habit. The fish tails after 267 99 are the composition's variants, and the spread across cities is evidence for a shared heading.
- What it would mean if true: 267–99 is a name or title formula, and the fish tails inside it vary.
- Cheapest next move: Tabulate the sign that follows 267 99 in every strict text and check whether that set matches the roof and tick variants.

### 16. Sign 104: an uninterpreted roof candidate with two cross-operation pairs

- What was seen: Roof104 with 211 ranks fourth of 290 combinations, with 7 expression classes and 2 cross-operation pairs. Route C notes that 65 59 211 and 104 59 211 cannot both be declared equal: 104 has no assigned number, and 65 has two written items under that parser.
- Where: research/campaigns/integrated_20260906/route_a/composition_adjudication.json (ranked list); route_c/roof_count_scope_programs.json (the 65 and 104 warnings).
- Old label: "remains uninterpreted" (route A and route C).
- Why it is alive: If 104 is a second roof sign, it gives the frame a second roof value. The two roof signs would then be two counts or two classes, not one operation with variants.
- What it would mean if true: The roof is a small family of count or class signs, and 87 is one member.
- Cheapest next move: Count the strict texts where 104 precedes 59 or 67, and check whether the 87 and 65 contexts recur with 104 in the same place.

### 17. Tamil fish-name triangle: stone and cock as modifiers of mīṉ

- What was seen: The Tamil inventory has 93 category-marked entries, 89 exact-eligible, and 88 of those end in mīṉ (fish). The source-attested compounds are kaṉ-mīṉ (kal, stone, DEDR 1298), kōḻi-mīṉ (kōḻi, cock or fowl, DEDR 2248) and kallu-k-kōḻi-mīṉ (stone plus cock plus fish). Route D's joint parse D-TAMIL-JOINT-00 assigns 87 to kal, 211 to kōḻi and 59 to mīṉ. DEDR is cited by the source but not held.
- Where: research/campaigns/integrated_20260906/evidence_inventory/tamil_compounds.json (93 entries); evidence_inventory/tamil_compounds_relations.json; route_d/outputs/tamil_full_joint_search.json; route_d/outputs/tamil_joint_worked_readings.json; route_d/REPORT.md.
- Old label: "conditional lexical triangle; the sign assignment is an assumption; the sandhi rule is charged separately" (route D).
- Why it is alive: The Tamil compounds put the modifier before the fish head, which is the order the Indus fish pairs show (lead 6). Roof 87 comes before 59 in the Indus text, so 87 59 could spell a kal-mīṉ type compound with no extra rule.
- What it would mean if true: 87 59 211 spells a source-attested fish name. The roof and the tick are two modifiers on one fish head.
- Cheapest next move: Look up the Tamil compounds with kal or kōḻi as first member and check whether any matches the Indus order (modifier, fish, tick). That is one lookup in the held inventory.

---

## Sources on disk

- research/data/mahadevan_20260905/concordance_rows.csv: 3,916 rows, one per sign occurrence with textnum, object, face, locus, level, medium, raw codes and strict flag; 2,575 strict texts.
- research/data/mahadevan_20260905/ (concordance_documents.json.gz, paired_objects.json, front_families.json, scalar_counterexamples.json, four_by_three_grid.json, conditional_radix_algebra.json, source_witnesses/, summary.json): the derived layer and the earlier arithmetic tests. Not read in full by me.
- research/data/meluhha/cuneiform_attestations_expanded.csv (and cuneiform_seed_attestations.csv, cuneiform_source_routes.csv, cuneiform_fetch_log.csv): held cuneiform Meluhha attestations, 16 expanded rows per the inventory.
- research/campaigns/integrated_20260906/evidence_inventory/recovered/Parpola_2008_copper.pdf: the 2008 copper-tablet paper (552,079 bytes, sha256 1e68a8c2…f41cf1); 46 analytical classes.
- research/campaigns/integrated_20260906/evidence_inventory/recovered/glyph_059, 060, 065, 066, 067, 068, 069, 070, 071, 072, 073, 211 (.png): publisher drawings of 12 of the 417 signs.
- research/campaigns/integrated_20260906/evidence_inventory/parpola1994_compounds_pdfindex296.png and 300.png; parpola1994_pdfindex296.txt to 300.txt; parpola1994_table10_1_pdfindex199.png and .txt: Parpola 1994 Tamil appendix (pages 279 to 283) and Table 10.1 of Dravidian forms.
- research/campaigns/integrated_20260906/evidence_inventory/tamil_compounds.json, tamil_compounds_relations.json, tamil_compounds_report.md, dravidian_lexical_examples.json (8 entries).
- evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/dev-tools/ashtadhyayi/assets/mw.xml: Monier-Williams Sanskrit dictionary XML, 67,574,805 bytes, 286,539 entry keys (192,482 distinct headwords used by route D). Also assets/data.json (2,259 root rows).
- evidence/tmp/cisi_xml/The Indus Script. Text, Concordance and Tables - Iravathan Mahadevan_djvu.txt and .xml: the 1977 codebook (Appendix II). The mapping from the digital three-digit field codes (fs80) to it is not established.
- evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images/: third-party seal photo cache, 6,870 files (related surfaces, not independent objects).
- research/data/sign_crosswalk/source_panels/: 63 derived source crops, including m77_text7_concordance panels.
- research/campaigns/integrated_20260906/completion/sources/: 1380_2452_adjudication.json, original OCR extracts, page_60.png, page_801.png, page_802.png, page_82.png (the codebook pages for the composite animal and unicorn labels).
- research/campaigns/integrated_20260906/route_b/published_copper_type_network.json and copper_correspondences.json: 46 published copper types and 19 typed relations (from Parpola 2008), 98 copper text-picture edges.
- research/data/mahadevan_20260905/ and campaign outputs listed above; the campaign's own run commands are in each REPORT.md.

## Ideas named but never run

- Recover the other 405 publisher drawings of the 417 signs from the existing manifest (evidence_inventory/REPORT.md says they can be recovered; only 12 were).
- Transcribe the rendered Table 10.1 (Dravidian fish, star and glitter forms; parpola1994_table10_1_pdfindex199.png). The OCR loses distinctions; the table was never transcribed.
- Find a free route to the Dravidian Etymological Dictionary (DEDR). The campaign cites DEDR numbers but holds no copy. Free route first, per the rules.
- Join the cuneiform Meluhha attestations to Indus records by site and period. The inventory says no same-object join was found; a site-and-period join was never tried.
- Map the digital field codes (fs80 variants) to the 1977 codebook. The campaign says the bridge is not established and never built it.
- Sign 12 and sign 104 have no assigned meaning and were never run as standalone tests (lead 8 and lead 16 give the first steps).
- The 1380/2452 picture difference (raw code 251 vs 13): the route A report calls it the next experiment, and it was not run.
- The 1177/3103 tick pair (both Mohenjo-daro seals, direction 1, raw picture 13) as a same-locality contrast: named as the discriminating next evidence in route B, not run.
- Companion-field prediction where the spelling operation and a production convention disagree: named in route B, not run.
- Reverse cup count against physical volume or weight of the site's objects (the plan's "physical world" idea). Never run.
- Linear Elamite comparisons: named in the hypothesis list of the project rules and absent from the campaign runs.
- Route B's 362/363 short-sign distinction on the source images, and the 3315/3414 short-sign distinction: named as checks, not run.
- Route D's contextual allomorphy mechanism (source-attested, charged separately): named as next_mechanism in route_d/outputs/two_modifier_lattice.json, not run.
