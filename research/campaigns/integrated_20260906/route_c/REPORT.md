# Route C — numerical and administrative programs

Executed C25–C30 against the frozen Mahadevan corpus. No numerical value, physical unit, pronunciation, or translated field name was accepted. The prior identical-front/different-reverse counterexamples remain constraints, not a new result of this campaign.

Run from the repository root:

```sh
python research/campaigns/integrated_20260906/route_c/run_numerical_programs.py
```

The runner preserves Mahadevan IDs, face and line boundaries, raw doubtful signs and unknown spans. It uses only the existing CSV and shared partial-observation loader. Source rows use the shared `M77:object:side/line` identifiers. Catalogue long-stroke counts 86/87/89/95/96 = 1/2/3/4/5 are graphical observations, not accepted numerical meanings. Sign 103's different stacked arrangement is not merged with them.

## Executed inference

**Local quantity-field hypothesis.** The search records 878 visible or doubtful long-stroke occurrences, 267 cup/other-face records, and 113 partial or multiface extensions. Among 330 strict full-line templates containing exactly one long-stroke group, only four permit more than one graphical count: bare N; 328–N; 328–N–341–192–197–177; and 328–N–149–402–267, in display order. The latter two vary between 2/3 and 3/4 respectively. This constrains where count substitution is observed; it does not turn unobserved combinations into prohibited ones or exclude broader grammatical contexts.

**Shared arithmetic does not outperform a field independent of the front.** Eleven distinct strict non-cup/cup records have exactly one count group on each relevant face. Recombination evaluation removes the target objects and exact paired-expression copies. The second task additionally withholds the complete normalized front descriptor family. Components and other count classes may remain. Target count symbols alone are not treated as whole-record aliases, because that would instead test an entirely unseen count class. All evaluations are retrospective.

| Program | Recombination mean NLL | Unseen descriptor mean NLL |
|---|---:|---:|
| Constant, fitted inside each training fold | 1.182 | 1.182 |
| Shared multiplier | 1.918 | 1.918 |
| Shared affine program | 1.274 | 1.274 |
| Unconditional categorical distribution | 1.313 | 1.298 |
| Class-and-front-count categorical distribution | 1.255 | 1.229 |

Lower NLL is better. The full-data affine optimum is `y = 0*x + 3`: it discards the front count. A separately reported fixed-3 comparator is explicitly post hoc; the fold-fitted constant supplies the relevant comparison. These small-sample results reject the tested shared arithmetic explanation, not arithmetic in every context. The approximate BIC sensitivity excludes matched rule/search costs and is not a complete MDL comparison or a promotion criterion.

**Addition, multiplication and grouping were also executed.** Adding the one eligible front with two count groups gives 12 distinct records. Exact sum predicts 3/12, product and maximum 4/12, and the post-hoc constant 3 predicts 6/12. Object 4718 contains visible groups 1 and 3 and a cup-side count 3. Its product, maximum, and last stored group all agree, so that example cannot distinguish multiplication from selection. No invented per-object multiplier repairs a failure.

**Relative units are conditional and underidentified.** The 29 strict single-count face pairs give 24 unique equations under the explicit hypothesis `n_A U_A = n_B U_B`. There are 31 descriptor-unit parameters and 12 free component scales. Objects 4444/4456 require the cup/119-frame unit ratio 2/3; 5498 requires 1. Object-class conditioning preserves this contradiction. Adding locus removes it by expanding to 47 unit parameters and 24 independent scales; adding level expands to 54 and 29. Such fragmentation mainly creates isolated assignments, not independently corroborated conversions. Absolute scale is never identified. Spanning-tree ratios in a conflicted component are not solutions.

**Repetition compression remains a one-frame candidate.** Across 98 repeated-sign runs, a count-based shorthand search allowing one paid context edit finds only the already-known `267–99–59–59–211` / `267–99–87–59–211` alignment, on M77:4232:0 and M77:1551:0. There is no additional base even after that relaxation. Of the 120 permutations of the five graphical count labels, 24 match at least as well. The alignment therefore does not identify a productive numerical operator.

## Connected examples and partial observations

The shared partial loader finds eight cup-front rows compatible with at least one existing complete cup-front expression. Compatibility is existential and is never substituted for an observed transcription. M77:4581:20 and M77:4591:20, both `176–342–87–*119` in display order, each have only the complete 119-family as a compatible candidate in this restricted comparison. Their reverse count is 4, while complete witnesses 4444/4456 and 5498 supply 3 and 2. The additional faces are standalone 137 and 59. If the doubtful reading is correct, a third field can coexist with the same front and a different reverse parameter. The two different third-face signs prevent treating either one as a unique arithmetic multiplier without more evidence.

A Route D lead was executed across all 16 strict multiline faces containing long strokes. Two global line-order programs produce one inline correspondence: M77:2516 has catalogue-order lines `[86] / [211]`; M77:4474:20 and M77:4518:20 have inline stored `[86,211]`. Both latter objects pair this with display `89–267`. If both field equivalence and equal quantity were independently established, the equations would force `U_211/U_267 = 3`. At present it is a repeated conditional correspondence, equally compatible with categorical fields. Source line boundaries are retained; no complete inscription has been rewritten by concatenation.

## Interfaces and continuation

`candidates.json` contains eight records under the shared candidate contract. `fish_211_cup_records.json` supplies 68 paired records, 63 strict, to the integrated A/B experiment. `parse_face`, `record_fields`, `unit_graph`, and the fitted predictors are reusable Python entry points. Detailed source rows, masks, predictions, contradictions, and scalar-gauge information are in the accompanying JSON results.

## Roof/count/Q interaction executed after Route A's new bridge

The primary runner now also invokes `run_roof_count_program.py`. Four exact roof pairs are present: two plain65/87–59 contexts and two marked66/87–60 contexts. Besides the 267–99 frame, the latter include stored `[66,176]` (4493/4806) versus `[87,60,176]` (4556). The paired cup counts on 4493 and 4556 are 4 and 2. If the proposed spelling equivalence is correct, these independently variable reverse fields must remain in the model; a fixed-unit equal-face scalar interpretation fails.

The four proposed spelling rewrites are jointly confluent: both paths from66 yield87–59–211. Adding the literal instruction “87 duplicates the next glyph” makes the combined normalizer nonconfluent:

```text
66 → 65–211 → 87–59–211 → 59–59–211
66 → 87–60 → 60–60 → 59–211–59–211
```

These are distinct literal outputs, not independently established different meanings. A model in which Q=211 scopes over the counted field once can yield the observed59–59–211 form. An equally scoped categoricalR/Q writing grammar makes the same core spelling predictions; the data do not force numerical multiplication.

Six relevant spellings occur in the267–99 frame. Four admit the conditional representation “two written59 items plus one field Q”:66;87–60;87–59–211;59–59–211. The existing65–59–211 rival contains **three** written base items if roof65 means two and adjacent fish items share one counted field. Thus the previous65/87/104 same-slot matches cannot all be assumed equivalent. The104 alternative remains uninterpreted. This is an explicit scope and boundary constraint, not an accepted numerical reading.

The next discriminating source task is the 4581/4591 third-field contrast: adjudicate the already-held source entries at the doubtful 119 and face assignments, then compare the third-field relation with the complete 119-family. In parallel, the coordinator's fixed fish/211 normalization can test whether the same field parser transfers across marked and separated spellings. A successful transfer would support a writing/field operation; numerical magnitude would still require a representation on which arithmetic and categorical programs make different predictions.

Steps C25–C30 are executed as the bounded mechanisms above. Broader numerical decipherment remains unresolved. Missing publisher glyph files beyond the existing witness set limit additional graphical-series hypotheses; no new archaeological or linguistic source was acquired.
