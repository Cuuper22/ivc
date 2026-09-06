# IVC decipherment: integrated Codex execution plan

## Mission

Use `Cuuper22/ivc` as a research workspace to recover a connected decoding system: reusable writing operations, grounded meanings, numerical functions, and phonetic correspondences that explain additional inscriptions. Execute the research, not merely its infrastructure. Cover all four routes and combine their results wherever they constrain the same unknowns.

Use the evidence already acquired: repository data, archived sources, existing images, saved research outputs, and available comparative-language material. Recovering an already-acquired file is in scope; acquiring new archaeological or comparative datasets is not part of this campaign. Software dependencies are tools, not new evidence.

Do not turn dataset cleanup, reproduction of established observations, or better sign prediction into the main deliverable. Reuse existing work unless a specific defect changes an active inference. Treat earlier rejected approaches as rejected under their tested assumptions, not as universal impossibility results.

## Orchestration

The coordinator owns the shared representation, evaluation partitions, hypothesis dependencies, and integration. Assign separate route leads for **A: writing operations**, **B: semantic triangulation**, **C: numerical programs**, and **D: phonetic decipherment**. Use specialist subagents for source-image interpretation, constrained search, and decisive counterexample analysis as needed.

Give each agent a concrete scientific question, permitted evidence, input snapshot, owned output paths, and a return contract. Use isolated worktrees or nonoverlapping paths. Only the coordinator changes shared schemas, evaluation definitions, or the accepted-claim ledger. Merge useful work and remove completed temporary branches without overwriting unrelated user changes.

Start preparation for all four routes immediately. Start their substantive searches as soon as the shared foundation is usable. No route must wait for another to produce an accepted discovery. Exchange provisional hypotheses explicitly as provisional hypotheses.

## Execution order

**Shared evidence and interfaces → parallel route searches → integrated candidate systems → discriminating predictions → targeted adjudication → continued search and a reproducible handoff.**

Steps within each route are ordered. The four route sections run concurrently. Publish usable intermediate outputs instead of making other routes wait for an entire section to finish.

---

## Phase 1 — Establish the shared evidence foundation

**Owner: coordinator and evidence specialists. All route leads prepare their candidate models in parallel.**

- [ ] **01. Resume from the actual research state.** Read the current checkpoint and relevant portions of `MERGED_BRANCH_STATE.md`, `research/docs/mahadevan_crossface_constraints_20260905.md`, `research/docs/semantic_reading_search_20260906.md`, and the corresponding tools and outputs. Inspect `db/schema.sql` before adding another representation. Record the starting commit and existing uncommitted changes. Do not reread the entire research history or rerun completed campaigns by default.

- [ ] **02. Locate and classify the existing inputs.** Inventory the frozen Mahadevan corpus, other transcription systems, source photographs, glyph illustrations, copper-tablet material, source codebooks, contextual metadata, and comparative-language resources already held. Separate observations, published interpretations, derived tables, and model-generated proposals. Resolve existing filenames and paths rather than assuming that a README description proves an input exists. Record unavailable inputs without blocking work that does not need them.

- [ ] **03. Build a lossless object-centered observation layer.** Extend existing loaders and tables where practical. Represent physical objects, faces, lines, sign occurrences, catalogue-specific sign IDs, image regions, motifs, and source references separately. Preserve raw spellings, numeric formatting, direction codes, line boundaries, damage flags, and uncertainties. Normalize identifiers reversibly. Do not confuse a face with a line, concatenate unordered lines, or convert an unknown span into a sign meaning zero.

- [ ] **04. Resolve identity without inventing independence.** Distinguish the same object in different catalogues, multiple photographs of one surface, repeated impressions, exact textual copies, and merely similar formulas. Store secure identity links separately from proposed alignments and possible allographs. Allow unresolved and many-to-many mappings. Treat another transcription of the same object as another observation of that object, not another archaeological sample. Make family-based versus object-based weighting available.

- [ ] **05. Support both complete and partial observations.** Keep the existing strict view, but add a view that uses visible portions of incomplete inscriptions. Retain uncertain signs as alternatives and unknown spans as spans, including uncertain span length where necessary. Marginalize over compatible readings or use explicitly described search approximations. Never train on an imputed reconstruction as though it were observed. Preserve alternate direction and line-order hypotheses when unresolved; do not allow free reversals for every troublesome example.

- [ ] **06. Attach graphical and contextual features.** From already-acquired illustrations and photographs, record candidate bases, additions, enclosures, repeated elements, stroke arrangements, and spatial relationships. Annotate motifs and their attributes independently of proposed readings. Preserve picture, object, and publication references for each feature. Keep catalogue drawings distinct from individual artifact appearances. Use existing text extraction and direct image inspection; use OCR only where necessary. Missing or illegible imagery is not evidence that a motif is absent.

- [ ] **07. Prepare the linguistic interface and research priorities.** Normalize only the comparative material already available, preserving attested forms, reconstructions, phonetic conventions, and uncertain analyses. Keep published Indus readings separate from independent linguistic evidence. Identify frequent signs and recurring constructions connected to graphical variants, linked faces, or motifs, while retaining rare signs that connect otherwise separate candidate groups. Prioritize these connected targets rather than imposing an arbitrary vocabulary cutoff.

**Shared output:** a versioned observation snapshot, source manifest, identity/grouping map, partial-observation loader, graphical/contextual features, and an inventory of usable linguistic evidence.

## Phase 2 — Give all routes the same inference and evaluation interfaces

**Owner: coordinator. Route leads implement their search mechanisms against these interfaces as they become available.**

- [ ] **08. Define what each prediction may see.** Create task-specific input/output masks. Specify whether a prediction receives a prefix, another face, a motif, metadata, or a candidate language, and exactly what it must predict. Prevent scored evidence from reentering through another catalogue, companion face, generated annotation, or another agent's output. Record prior exposure: retrospective repartitioning of previously inspected material does not create a genuinely blind discovery test.

- [ ] **09. Separate two generalization questions.** Build a recombination evaluation that withholds complete combinations and their copies while allowing their components to be learned elsewhere. Separately build an unseen-family evaluation that withholds related expression families. Group confirmed same-object and copy links appropriately; do not join the entire corpus merely because strings form a transitive chain of small edits. Add site or medium transfer tests when a claim asserts that scope. Report these tasks separately.

- [ ] **10. Implement a shared candidate record.** Each hypothesis must carry an ID, rule or executable interpretation, sign namespace, applicable context, prerequisites, supporting observations, contradictions, alternative explanations, parameters, complexity, and predictions. Distinguish graphical equivalence, grammatical function, operational meaning, lexical meaning, sound assignment, and language identification. Record which evidence and upstream hypotheses produced it. Use machine-readable records alongside concise explanations.

- [ ] **11. Define comparable scoring without rewarding flexibility.** Compare candidates on the same observed targets using predictive fit and an explicit penalty for parameters, exceptions, and rule complexity. Keep graphical, textual, contextual, numerical, and phonetic performance visible separately. Account for dependent observations rather than multiplying repeated descriptions of one fact. Preserve unresolved alternatives when the evidence does not distinguish them. A clean interpretation must compete against simpler categorical and nonlinguistic explanations, not only against random signs.

- [ ] **12. Reuse controls and test the new mechanisms narrowly.** Reuse relevant frequency, neighboring-sign, positional, metadata-only, and memorization baselines where their inputs and evaluation tasks match. Add compact constructed examples and already-held deciphered-script controls to determine whether the new search can recover its intended rules or detect underdetermination. These are development diagnostics, not evidence about Indus. Fix mechanism-breaking errors, then proceed to the actual corpus; do not build an unrelated benchmark project.

**Shared output:** evaluation manifests, candidate contracts, scoring functions, necessary controls, and a minimal runner. Do not build a general-purpose platform before testing scientific candidates.

---

## Phase 3A — Recover graphical composition and grammatical operations

**Owner: Route A. Starts after the shared observations and candidate interface are usable. Runs alongside B, C, and D.**

- [ ] **13. Generate competing explanations for graphical variation.** For candidate base/modified pairs and compounds, consider alternate spellings, grammatical operations, semantic distinctions, phonetic additions, and unrelated signs. Include the existing marked-fish/separate-211 candidate without privileging it. Search for shared operations across sign families, but also allow well-supported family-specific operations. Graphical resemblance alone must not force sign mergers.

- [ ] **14. Fit a compact spelling-and-grammar model.** Begin with an interpretable transducer or equivalent constrained rule system. Jointly infer expression boundaries, component roles, and permitted transformations. Allow a graphical change to correspond to an added or omitted written unit, a changed boundary, or a systematic change in surrounding signs. Charge for each additional operation and exception. Use restricted local context before introducing more elaborate dependencies.

- [ ] **15. Replace exact-string replacement with structured alignment.** Search beyond cases where everything around a substitution is identical. Align candidate constructions while preserving plausible shared components and allowing rule-governed changes. Incorporate partial observations without completing them opportunistically. Compare a shared transformation against separate memorized expressions and unrelated slot substitutions. Do not treat matching contexts as proof of synonymy.

- [ ] **16. Distinguish productive rules from local conventions.** Test shared operations against alternatives conditioned on artifact class, site, or other observed context. Require a proposed conditioning variable to explain more than an individual exception. Keep global and local models in competition. Do not force all inscriptions into one grammar, but do not create a separate grammar for each object either.

- [ ] **17. Predict unseen applications of candidate rules.** Freeze candidate operations and test the withheld combinations defined earlier. Check whether the operation predicts both the changed form and its permitted context, rather than merely ranking a common sign highly. Then evaluate extension to other families where the model claims it. Report unsupported applicability explicitly instead of silently narrowing the rule after seeing every failure.

- [ ] **18. Publish operations and unresolved equivalences.** Export candidate decompositions, grammatical features, segmentation alternatives, and counterexamples. Describe unanchored operations with neutral labels rather than naming them plural, genitive, or another grammatical category without evidence. Make the outputs directly usable by B's semantic aligner, C's field parser, and D's spelling model. Keep raw transcriptions unchanged.

**Route A output:** executable writing-operation models and expression analyses, with predictive consequences and stated limits.

## Phase 3B — Extract semantic constraints from text–picture–text relationships

**Owner: Route B. Uses the same objects and source-linked images; consumes A's analyses when available but begins without them.**

- [ ] **19. Construct the complete available correspondence network.** Link long texts, short texts, pictures, faces, and objects using existing evidence. Include both repeated-text/different-picture and repeated-picture/different-text cases. Preserve multiline structure and uncertainty. Treat same-object pairing, repeated inscription, pictorial similarity, and suspected abbreviation as different relationship types. Do not convert co-occurrence into equivalence by construction.

- [ ] **20. Fit competing referent models.** Test whether connected expressions encode the same referent, related categories, complementary documentary fields, or merely shared production context. Consider literal depiction, shared attributes, and role/category labels as alternatives. Keep anonymous latent categories anonymous unless the evidence identifies their meaning. A cluster that could be an institution, commodity, or person is not yet any of those things.

- [ ] **21. Isolate semantic contributions through contrasts.** Find networks where a component is retained or changes while paired evidence changes in a distinguishable way. Use A's candidate alignments to examine nonidentical expressions, but also retain analyses that do not depend on A. Seek constraints supported across connected relationships, rather than interpreting an entire inscription from one image. Preserve every alternative segmentation that changes the semantic conclusion.

- [ ] **22. Challenge the production-context explanation directly.** Compare semantic models against object-form, site, documented production-group, and other available contextual explanations. Distinguish documented relationships from inferred ones. Test matched contrasts where possible. Avoid treating success at predicting a motif from a whole inscription as sufficient: identify what the proposed semantic model explains that a workshop or provenance label does not.

- [ ] **23. Transfer candidate meanings beyond their defining examples.** Freeze a semantic hypothesis and predict allowed text–picture or text–text relationships elsewhere in the existing corpus under the designated evaluation masks. Test whether its component-level interpretation travels through another construction. Distinguish broad category identification from a specific lexical reading. Record when the candidate only reproduces the associations used to invent it.

- [ ] **24. Export semantic anchors at the precision actually supported.** Publish candidate meanings, semantic exclusions, same-referent relations, and unresolved category labels with their exact dependencies. Supply D with anchors that can constrain lexical candidates and A/C with constraints on field roles. Carry published interpretations as labeled priors or rival models, never as independently observed translations.

**Route B output:** grounded semantic hypotheses and referential relationships capable of constraining other inscriptions.

## Phase 3C — Infer executable numerical and administrative notations

**Owner: Route C. Starts from linked objects and graphical observations; incorporates A/B constraints without depending on their success.**

- [ ] **25. Represent candidate numerical observations neutrally.** Record visible stroke groups, their arrangements, repetitions, neighboring signs, and cross-face combinations. Keep distinct graphical counting systems separate. Model cardinal quantities, ordinal/category labels, and nonnumerical alternatives. Do not assume that similar-looking marks share a unit, or that opposite faces express equal quantities.

- [ ] **26. Define a compact language of record programs.** Allow explicit fields such as descriptor, quantity, denomination, authority, and allocation, initially as candidate roles. Permit constrained operations including addition, multiplication, grouping, and relative-unit conversion when they have observable consequences. Include categorical lookup and complementary-field models. Begin with the simplest programs; increase complexity only to address a specific unexplained pattern.

- [ ] **27. Infer fields, values, and operations jointly.** Search for programs that explain linked records and variant inscriptions with shared parameters. Use A's boundaries and B's possible referents as alternative constraints, not fixed truths. Evaluate equal-face models only in the contexts they actually claim. Include the existing identical-front/different-reverse counterexamples. Do not rescue a model with a freely invented unit, multiplier, or meaning for each object.

- [ ] **28. Determine what is identifiable.** Separate observable ratios and operational distinctions from arbitrary choices of scale, base representation, field names, or hidden labels. Report equivalent solutions together. Check whether the observed records genuinely distinguish arithmetic from an equally compact categorical program. Algebraic consistency of equations derived from guessed readings does not independently validate those readings.

- [ ] **29. Predict another representation or field.** Freeze the program and predict a withheld observed count, valid combination, or alternative notation from the permitted fields. Seek cases where competing arithmetic and categorical programs disagree. Exercise the program across different expressions and relevant object contexts. Retain open or absent combinations as unknown unless the corpus provides a reason they should have occurred.

- [ ] **30. Export operational meanings and constraints.** Publish executable parsers, operators, relative-value relationships, applicable contexts, and explicit failures. Feed quantity-field and unit-class constraints to A and B, and possible lexical roles to D. Do not assign absolute physical units or pronunciations without an independent basis already present in the evidence.

**Route C output:** executable record interpretations that make nontrivial observable predictions, including identified equivalences and unresolved alternatives.

## Phase 3D — Jointly infer phonetic correspondences, segmentation, and language

**Owner: Route D. Prepares its search from the shared linguistic inventory while A–C run; consumes their hypotheses as they arrive.**

- [ ] **31. Build the competing linguistic hypothesis space.** Use the comparative forms and analyses actually available. Include uncertainty in reconstructions, historical relationships, and morphology. Allow an unresolved-language alternative and analyses not tied to a named family. Where independent phonetic evidence is absent, distinguish anonymous sound-like classes from identified sounds; do not manufacture anchors from model memory or a favored published Indus reading.

- [ ] **32. Support mixed writing systems.** Allow signs to function as phonetic units, meaning-bearing signs, classifiers, or numerical signs, with context-dependent roles only where justified. Model multiple spellings and restricted polyphony without making every occurrence freely interpretable. Incorporate A's spelling operations and C's numerical distinctions as competing candidate configurations. Do not force an alphabetic substitution model onto every sign.

- [ ] **33. Search sounds, segmentation, and morphology together.** Alternate constrained search over sign-to-sound mappings, expression boundaries, candidate morphemes, and regular correspondences to the available linguistic material. Use interpretable constraints and retained alternative solutions. Penalize special sound changes and object-specific translations. A proposed correspondence must recur consistently; isolated dictionary resemblances cannot determine the solution.

- [ ] **34. Couple semantic anchors without circular confirmation.** Use B's candidate meanings to restrict lexical possibilities, tracking exactly which clues they depend on. Allow phonetic predictions to suggest new semantic distinctions, but mark these as downstream consequences, not independent confirmation of their own premises. Compare anchored, partially anchored, and unanchored runs where the distinction matters.

- [ ] **35. Compete against plausible rival systems.** Compare alternative languages, segmentations, mixed-script assignments, anonymous phonological models, and nonphonetic explanations under matched flexibility. Use already-held deciphered-script controls and constructed cases to diagnose whether the decoder prefers a supplied language regardless of the input. Do not substitute a larger masked-sign model for this phonetic search.

- [ ] **36. Predict recurring forms and partially read withheld inscriptions.** Freeze the mapping and grammatical rules before evaluating the designated targets. Require the same assignments to explain repeated forms, independently supplied semantic relationships, and new combinations. Preserve unread portions and ambiguous alternatives. Evaluate complete candidate analyses as well as individual sign predictions; shared easy signs must not conceal contradictory readings elsewhere.

- [ ] **37. Export sound assignments with explicit dependencies.** Publish each candidate sound correspondence, its orthographic conditions, linguistic assumptions, semantic prerequisites, and competing assignments. Separate genuine pronunciation claims from arbitrary renaming of latent classes. Return spelling and segmentation contradictions to A, semantic conflicts to B, and numerical/nonphonetic role conflicts to C.

**Route D output:** a competing set of explicit phonetic and lexical decipherment systems, not merely embeddings or next-sign scores.

---

## Phase 4 — Combine the routes into connected decoding systems

**Owner: coordinator. Begin with the first usable route outputs; do not wait for every local search to finish.**

- [ ] **38. Construct the dependency graph of candidate claims.** Join compatible operations, referents, fields, and sounds through shared observations and explicit prerequisites. Separate directly observed facts from inferred claims. Detect contradictions and circular justifications. Multiple routes explaining the same observation do not create multiple independent pieces of evidence. Keep alternative connected systems rather than accepting each route's local winner independently.

- [ ] **39. Execute cross-route prediction tasks.** Use A to predict where an operation should alter B's referential relationships or C's numerical fields. Use B to narrow D's lexical alternatives. Use C to identify expressions D should not treat as ordinary phonetic words. Use D to predict alternate spellings and morphological contrasts for A. Each exchange must produce a specific testable consequence, not merely a higher confidence label.

- [ ] **40. Fit compatible systems jointly.** Optimize the shared interpretation against the original observations, with shared parameters and explicit channel dependencies. Do not multiply route scores as though each came from independent data. Permit a weaker local model to win when it explains more of the combined evidence with fewer exceptions. Implement a larger joint solver only where actual candidate interactions require it.

- [ ] **41. Propagate assignments into additional constructions.** Follow recurring components, graphical variants, linked expressions, and candidate grammatical transformations outward from the connected core. Predict what the combined system implies before inspecting its designated evaluation outputs. Preserve original uncertain observations. Expand to less frequent signs when existing rules constrain them, rather than inventing standalone meanings for coverage.

- [ ] **42. Test competing causes of apparent agreement.** Remove or replace pivotal anchors, graphical assumptions, metadata associations, or language priors and determine which conclusions survive. Repeat only the comparisons needed to resolve an active claim. If the entire reading collapses when one uncertain premise changes, retain that dependency in the claim rather than presenting the cascade as independent confirmations.

- [ ] **43. Investigate contradictions by cause.** Distinguish source-reading uncertainty, mistaken object alignment, alternative sign identity, an incorrect grammar, a numerical-field error, and a false semantic or phonetic anchor. Check the exact existing source when that distinction can change the decision. Penalize any repair or exception in subsequent model comparison. Refit the affected portion; do not restart unrelated completed work.

- [ ] **44. Maintain a discriminating experiment queue.** For each unresolved competition, identify the observation or inference over existing evidence that best separates the rivals. Assign it to the appropriate route or specialist. Record why a rejected candidate failed and what changed assumption could legitimately reopen it. Continue alternative mechanisms when one fails; do not repeat the same search with cosmetic changes or leave a route dormant because another currently looks stronger.

**Integrated output:** executable candidate decoding systems, their dependency graphs, explicit cross-route predictions, and a prioritized queue of unresolved scientific questions.

## Phase 5 — Adjudicate discoveries, not just model fit

**Owner: coordinator plus candidate-specific reviewers. Apply this work to substantive surviving claims, not indiscriminately to every exploratory pattern.**

- [ ] **45. Freeze the claim before its decisive test.** Write its precise meaning, scope, required assumptions, allowed inputs, predicted outputs, and strongest rival explanation. Freeze the relevant model and search settings. Identify which cases were already exposed during hypothesis development. Keep a prediction separate from an explanation constructed after seeing the target.

- [ ] **46. Run selection-aware comparisons.** Evaluate the frozen candidates on the agreed recombination, new-family, and applicable contextual-transfer tasks. Where discovery depended on searching many alternatives, reproduce the relevant selection procedure in a matched control rather than comparing only the winning candidate with unsearched noise. Match the control to the claim: preserve the plausible nuisance structure instead of destroying everything indiscriminately.

- [ ] **47. Check the load-bearing source observations.** Inspect the exact already-acquired images or source entries on which the claimed interpretation depends. Verify only distinctions capable of changing that interpretation: sign identity, stroke grouping, orientation, side assignment, or motif feature. Record unresolved details rather than treating image enlargement or a modern glyph drawing as new physical evidence. Do not expand this into a corpus-wide re-audit.

- [ ] **48. Establish what is new and what is inferred.** Compare surviving claims with the scholarship already held. Separate reproduction, new formalization, a new operational or lexical reading, and a newly identified sound correspondence. Clearly describe novelty as unresolved when the existing literature coverage cannot settle priority. Neither prior publication nor internal model agreement automatically validates a reading.

- [ ] **49. Promote only the supported claim.** Update the accepted-claim ledger only with the interpretation actually warranted, its scope, sources, and unresolved dependencies. Keep conditional, ambiguous, and rejected proposals accessible without conflating them with accepted readings. Report observed predictive reach separately from legible-text coverage or translation coverage. Do not count renamed latent states, recovered known patterns, or infrastructure as decipherment.

## Phase 6 — Preserve the research and keep the next action executable

- [ ] **50. Consolidate runnable artifacts.** Reuse the current research layout. Add a campaign area containing the source manifest, observations or references to them, evaluation masks, route outputs, joint models, prediction records, and claim dependencies. Provide executable entry points for each route and the integration runner. Preserve meaningful experiment settings and seeds; omit disposable checkpoints and redundant data copies unless necessary to reproduce a result.

- [ ] **51. Deliver worked decoding examples.** For each substantive supported interpretation, show the source observation, original sign sequence, proposed segmentation, applied operations, semantic or phonetic assignments, resulting reading, and unresolved portions. Include the strongest counterexample or competing analysis. For unsuccessful routes, document the exact tested mechanism and failure, not a claim that the whole route is impossible.

- [ ] **52. Close the orchestration state cleanly.** Merge useful research changes, resolve shared-contract mismatches, and remove finished temporary worktrees or branches. Preserve unrelated user work and the immutable source observations. Maintain one current campaign document linking to the evidence and code, with each task marked executed, unresolved, or blocked by a specific unavailable input. Do not claim a run occurred merely because its code exists.

- [ ] **53. Continue from the strongest unresolved scientific question.** Select the next discriminating experiment from Step 44 and keep all routes supplied with relevant findings. A failed candidate ends that candidate, not the campaign. Infrastructure completion is not scientific completion. If execution must pause, save the exact active models, remaining alternatives, and next executable task without describing the decipherment as complete or implying that work continues unattended.

## Required final research package

The campaign must leave runnable implementations and executed results for all four routes; an integrated interpretation of their interactions; source-linked candidate and accepted claims; explicit predictions and contradictions; worked examples where justified; and an exact continuation state.

The scientific objective remains a connected decoding system that forces further readings. Complete the listed research actions without replacing that objective with an inflated claim of success.
