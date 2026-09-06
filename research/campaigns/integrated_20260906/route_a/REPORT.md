# Route A: writing-operation search, executed 6 September 2026

A two-operation candidate now connects expressions beyond the previous single-substitution fish examples. It remains a conditional orthographic analysis: no meaning, pronunciation, or equality of referents has been established.

## Strongest connected result

Use roof → separate87 before the fish, and four surrounding strokes → separate211 after the fish. The publisher drawings support the graphical square59/60/65/66; these are catalogue drawings, not independent artifact readings.

| Observation, stored order | Source objects | Conditional transformation |
|---|---|---|
|267–99–66|7249,7251,7255,7267,7269|roof removal gives267–99–87–60|
|267–99–87–60|6211|stroke removal gives267–99–87–59–211|
|267–99–87–59–211|1551|already expanded|
|65–70–211|1380|roof removal gives87–59–70–211|
|87–59–71|2452|stroke removal gives87–59–70–211|

The last pair extends the operation to fish70/71, which lacked an earlier exact single-rule counterpart. Both objects are Mohenjo-daro seals with direction code1, but their recorded picture codes differ251/13 (Route B). Site and medium alone cannot explain this particular contrast; it still may involve different referents in the same textual slot.

The roof premise came from two old contexts:65–348–342 ↔87–59–348–342 (1374/2913), and65–48–342 ↔87–59–48–342 (2821/2905/2906). Before the marked-fish transfer,87-before and102-before each had two long exact contexts. The new60/66 application has one exact context with two unchanged signs and another exact context with only176 unchanged (4493/4806 versus4556). The first two roof pairs confound medium; their repeated role across media is not itself a semantic control.

## Selected-rule rival comparison

`adjudicate_composition.py` compared every modifier/order candidate having a prior exact application:10 roof choices ×29 stroke choices =290 programs. All use the same fish features, recursive tick-then-roof grammar, and expression-collision metric.234 programs terminate;56 cyclic programs are explicitly retained as failures of this normalization mechanism.

Roof87-before plus211-after ranks first among the234 executable rivals:10 expression classes containing21 distinct raw expressions and12 pairwise relations. Roof109-before/211-after and roof102-before/211-after each give8 classes. After removing every70/71 expression, its whole objects and exact aliases,87/211 still ranks first with9 classes; the next rivals have8. Only87/211 produces the1380/2452 common form. Removing all267–99 prefix expressions leaves9 classes and preserves that pair.

Only two classes contain a pair requiring both operations. The267–99 triple is a transitive combination of single-operation edges.1380/2452 is the only class with no single-operation edge at all. These are counts of predicted equivalences, not independently observed synonymy. The comparison is restricted to prior exact modifier candidates, not the entire417² search space and not a statistical significance claim.

Both267–99 target strings had already appeared separately in the current211 alignment output before the dedicated roof test. The1380/2452 pair was noticed after the frozen composed transform produced it. All evaluations remain retrospective.

## Other executed mechanisms

The structured aligner preserves separate prefix and suffix anchors around a graphical base and permits one paid surrounding edit. It returns11 fish211 alignments, but these reduce to four compact expressions and three bases. Ten require a surrounding edit; one is the previously known exact context. Three compact expressions share267–99. A fourth,1235=150–123–65–67–73, aligns with7247=150–123–67–72–211 or4056=150–123–53–67–72–211. These edits remain explicit; they are not inferred synonyms.

Broad four-stroke →211 is not selected:342 yields16 structured pairs across six graphical bases, while211 yields11 across three fish bases. The21 literal-part hypotheses still give zero counterparts after allowing one context edit and requiring two observed anchors. Nine certain marked-fish occurrences in partial lines yield zero exact expanded visible-island counterparts; blanks, doubtful signs and unknown spans terminate an island and are never filled.

The existing graphical maps contain only one complete roof/stroke square,59/60/65/66. Every incomplete square is listed in `roof_lattice_predictions.json`; no extra base extensions were invented.

## Observable context prediction and simpler rivals

Each target graphical base is withheld with whole objects and exact-expression aliases. The task predicts the next observed sign or line boundary after a marked fish. There are50 target occurrences with44.333 total expression weight. All models use a fixed417-sign-plus-boundary alphabet and the same training-only background.

| Model | Predictive data cost, bits |
|---|---:|
|Base fish followed by211|135.17|
|One-parameter ending category|141.52|
|Other marked fish families|145.21|
|All211 continuations|146.11|
|Marked family + catalogue-number prefix|157.38|
|Marked family + object class|168.15|
|Bare fish|323.10|

The6.35-bit advantage of base+211 over a simple ending category is smaller than an explicit8.70-bit charge for selecting one marker among417, before any opcode or graphical-scope charge. This is an illustrative stated code, not a unique MDL prior. Continuation prediction therefore supports an ending-role relationship much more strongly than token equivalence. An unconstrained training-family continuation search actually chooses12 or388, predicts no observed complete alternate spellings, and demonstrates why next-sign success alone cannot recover the writing operation.

## Counterexamples and route interactions

1147=387–66–336–89–211 rejects unconditional whole-line exclusion of marked fish and separate211. A local split387–66 |336–89–211 remains possible: the suffix occurs in34 unique texts on38 objects and is standalone on2575,5089,7279,2015. The left fragment is not standalone. Marked66 also precedes336–89 on1425; no strict211–336 adjacency is observed. This is an unresolved segmentation proposal, not a license for a separate grammar per object.

Root integration found a concrete failure of an additional numerical interpretation:4493=[66,176] pairs with cup count4, while4556=[87,60,176] pairs with count2. If roof87 preserves the same fixed scalar value and opposite faces are equated, this is inconsistent. It does not refute a spelling operation when opposite faces are complementary fields. Route C's existing59–59 versus87–59 example uses1551 again, so that object is never counted twice as independent confirmation. Route D may propagate the anonymous root70 through the new equality; it cannot infer a sound for70 from this alone.

## Reproduction and continuation

From the repository root:

```sh
python research/campaigns/integrated_20260906/route_a/run_route_a.py
python research/campaigns/integrated_20260906/route_a/adjudicate_composition.py
python research/campaigns/integrated_20260906/route_a/build_report.py
```

A13–18 were executed: competing decompositions; constrained transducers; structured and partial alignments; context-conditioned alternatives; recombination/family exclusions; candidate operations and counterexamples. Phonetic and semantic identification remain unresolved. `candidates.json` follows the shared contract; no accepted ledger was changed.

The next discriminating experiment is to use the already-held object sources for1380 and2452 to determine what picture-code251 versus13 actually distinguishes, and to compare that feature across all independently held witnesses of the same two component constructions. Freeze roof87/211, roof102/211 and the categorical-field rival first; exclude the defining objects and their expression aliases. Predict one specified pictorial or companion-field contrast. If source images do not identify that contrast, retain the textual operation as conditional instead of manufacturing a semantic anchor. The executable starting point is `composition_adjudication.json.target_pair`, joined to Route B's source-linked object network.
