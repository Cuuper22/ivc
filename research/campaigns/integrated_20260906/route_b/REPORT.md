# Route B: semantic triangulation, executed 6 September 2026

The available text–picture–text network supports distinctions between fields and representations, but the tested mechanisms do not identify a word meaning. Literal pictured-species models fail explicit transfers. Anonymous semantic categories and anonymous production categories remain observationally equivalent under the fitted categorical models.

## Executed evidence and search

`run_route_b.py` reads the shared lossless M77 observations, preserving objects, faces, line boundaries, doubtful signs and source references. The network contains 3,788 faces, including 2,461 strict complete textual faces and 70 strict multiline faces. There are 1,023 same-object face-pair edges and 170 distinct short/long correspondences across 251 object-pair instances. The three additions to the earlier 167-candidate set are complete multiline relations on objects 1471 and 4386; no lines were joined into fictitious adjacency.

The search executed 429 one-component insertion/replacement contrasts matched on site and object medium. Multiple copies of a contrast are witnesses to one expression-pair relation. A separate 989-candidate scan tested within-line components of one to three signs, including initial and terminal position, across distinct expression families.

Parpola's already-acquired 2008 copper paper was recovered by the evidence agent with its original SHA-256 `1e68a8c2cf64bece75855987572c73133d215315e8432ad3f6f61db278f41cf1`. I inspected Figures 1a–b and their defining discussion, and encoded all 46 reconstructed types and 19 typed relationships. The author's 217 copies are not independent new observations, and these types are not automatically joined to M77 objects. Broken-line reconstructions remain tentative.

## Worked contrasts

All sequences here are in **stored M77 order**, not an asserted reading direction.

1. **A complete text need not identify the depicted animal species.** `336–89–296–342–98` occurs with raw picture code 75 on copper objects 3328, 3336 and 3368. The exact text occurs on face 20 of object 1704 with raw picture code 101, on the same face as the picture. Parpola's B6/B12 discussion independently identifies the corresponding contrast as elephant versus horned tiger and explicitly notes the shared text. A literal species-name reading of the whole text fails. A deity represented by different animals, a broad category, complementary fields and production context remain possible. This relationship was already discussed by Parpola; it is not a new discovery.

2. **A promising component fails transfer.** `204–245–358–342` occurs on 18 strict copper objects with raw codes 145/147. Removing 358 gives `204–245–342`, associated with raw 113 on copper 1707 and paired with short 184 on 3334/3398. This motivates, but does not establish, a component-specific pictorial distinction. Freeze the stronger rule that 358 names the copper picture category wherever it occurs, or that this four-sign core retains that category when extended. Six picture-bearing non-copper constructions containing 358 carry raw code 13. Most directly, sealing **7244** contains the entire core plus 12: `204–245–358–342–12`, with raw 13. That disproves the unconditional component/unchanged-core-to-picture rule under a direct depiction interpretation. It does not disprove every context-dependent meaning of 358 or establish what 12 does.

3. **Short/long pairing does not establish synonymy.** Short 363 is paired with `59–112–194–18–211–87–169` on 2901/3360, and with `389–407–124–169–373–287–342` on 3414. The first long family connects to raw 139; the second to raw 520. Short 362 also pairs with the second long text on 3315. Parpola explicitly discusses the related C5/C6 markhor/archer bridge. A shared broad referent or category survives; a single literal animal label does not follow. Checking the exact 362/363 distinction on the load-bearing sources remains relevant to a stronger spelling claim.

4. **Three fields can vary separately at catalogue resolution.** Objects 4581 and 4591 carry the same four-stroke cup face and the same middle text `*119–87–342–176`, while their short first faces differ, 137 versus 59. The doubtful 119 stays doubtful. This is compatible with a further selector or complementary field; no category name or arithmetic interpretation is assigned.

## Competing models and limits

The strict copper subset contains 81 picture-bearing objects, collapsing to 33 complete-text/raw-picture edge types across 26 texts and 20 raw picture codes. A one-to-one text/picture mapping fits at most 18/33 edges; a deterministic text-to-picture lookup fits at most 26/33. These are finite fit bounds at **raw-code resolution**. Some raw codes may describe variants of one referent; the seven lookup exceptions are not seven proven semantic contradictions.

For recombination prediction, exact complete-text families and their copies are withheld together. Each object contributes only its single longest unambiguous complete face; the target picture and all companion faces are hidden. Copies collapse by expression, raw picture code, site and medium. On 1,081 retained target types:

| Model | Correct | Predictive data cost, bits |
|---|---:|---:|
| Site and medium | 740 | 2,186.958 |
| Text components | 718 | 2,498.462 |
| Site, medium and components | 747 | 2,219.462 |

The combined model gains seven top-ranked matches but worsens the proper log score. It also uses far more nominal parameters. This executed mechanism provides no predictive win for a semantic component model. Nominal BIC-style parameter counts are recorded separately; they are not asserted to be effective degrees of freedom under regularization. Rare raw categories and candidate damaged/shape codes were excluded before fitting; the exact filter is in the executable. These are retrospective results, not blind discovery tests, and they do not prove that no better semantic model exists.

The published A/B/C **shape classes alone** predict reverse-channel type on 37/44 legible reconstructed types, versus 26/44 for the constant picture baseline. Seven exceptions are recorded, including mixed text-and-picture B12. Full type IDs would leak text and motif information, so they are never predictors. This supports treating object form as a serious explanatory variable for whether a complementary field is written or pictured. It does not identify a workshop.

A latent semantic-category model and a latent production-group model can have identical likelihood and parameter count: rename their unobserved state labels. Without an independently documented production variable or a discriminating component transfer, the available category fit cannot choose between them. Same-site or same-medium matches do not eliminate that ambiguity.

The digital `fs80` values remain exact raw codes. The 1977 Appendix II labels conventional two-digit field symbols; the complete bridge from the digital three-digit variants to that codebook was not independently established. No final-digit meaning was invented. Semantic names used for the B6/B12 and C5/C6 contrasts come from the separately inspected Parpola figures and discussion, not from silently decoding `fs80`.

## Output contract and continuation

`candidates.json` exports six candidates at their actual scope. `semantic_anchors.json` exports **no lexical or sound anchors**. It exports the failed literal-category transfer and references to unresolved relations. A phonetic search must not filter a lexicon to animal words using these observations.

The next discriminating campaign action is to combine the surviving writing-operation candidate with these fixed picture/short-field targets while withholding entire expression families and target objects. The coordinator is executing that interaction. Source adjudication should focus on the 3315/3414 short-sign distinction only if a candidate spelling model actually depends on it. The route does not require another corpus-wide re-audit.

Executed from the repository root:

```sh
python research/campaigns/integrated_20260906/route_b/run_route_b.py
```

The final source-network addition and its affected candidates were executed through the same module's `published_typology()` and `decisive_tests()` functions without repeating the already completed predictor fits. The full entry point includes them for reproduction. Required libraries: NumPy, SciPy and scikit-learn, all present in the campaign environment. BLAS threads are capped to one.

Primary evidence is linked by row IDs in `correspondence_network.json`, `decisive_object_contrasts.json`, `copper_referent_competition.json` and `frozen_358_transfer.json`. The publication graph records source page indices and the recovered PDF hash. Figures are publication reconstructions, not newly inspected physical artifacts. No accepted-claim ledger was modified.
