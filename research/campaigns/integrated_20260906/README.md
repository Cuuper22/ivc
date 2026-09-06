# Current campaign: reconstructed completion

Large artifacts are stored losslessly in `payload/` to support the publication transport. The completion runner restores them automatically. For direct access after cloning, run `python research/campaigns/integrated_20260906/restore_payload.py` once. The manifest retains every original file path and checksum.

[Reconstructed full execution, models, and task audit](completion/README.md). The lost completion pass has been rebuilt and rerun from the saved checkpoint and held sources. See completion/RECOVERY.md for the distinction between recorded lost results and newly executed reconstruction.

## Retained initial campaign report

# Integrated decipherment campaign — 6 September 2026

**Current result:** a connected, executable candidate for two graphical operations, tested against numerical, pictorial, contextual and phonetic alternatives. The campaign executed all four research routes and their interactions. **No translation, sound value, language identification or numerical meaning is accepted.** The decipherment objective remains open.

Start commit: `fcb6686c6439b1ad6fe33eafa63e99ed659a284b`; the worktree was clean. This campaign used existing evidence, including byte-identical recovery of previously acquired files. It did not acquire a new archaeological or comparative-language dataset. All corpus evaluations are retrospective: holding out an expression now does not erase earlier exposure to the corpus.

## Strongest connected candidate

Two operations can explain several different written forms while preserving the surrounding signs:

- Candidate **roof operation:** `65 → 87–59`; on the graphically marked fish, `66 → 87–60`.
- Candidate **surrounding-mark operation:** `60 → 59–211`, and corresponding transformations on other fish forms.

The operations compose in the following observed frame. Numbers below are Mahadevan 1977 sign identifiers in **stored catalogue order**, not sounds or a newly established physical reading direction. Every row is an actual inscription. The assertion that the rows are alternative spellings of the same expression is the hypothesis under test.

| Observed sequence | Source observations | Conditional analysis |
|---|---|---|
| `267–99–66` | 7249:20, 7251:20, 7255:0, 7267:20, 7269:0 | Both features incorporated in one fish form |
| `267–99–87–60` | 6211:0 | Roof represented separately; surrounding marks retained |
| `267–99–87–59–211` | 1551:0 | Both operations represented separately |
| `267–99–59–59–211` | 4232:0 | Candidate repeated-base realization of the 87 operation |

The original roof rule has two additional exact contexts, `65–348–342` / `87–59–348–342` and `65–48–342` / `87–59–48–342`. Combining the two operations also connects **1380:0 `65–70–211`** and **2452:0 `87–59–71`**, which both normalize conditionally to `87–59–70–211`. This reaches another fish base through the composition of the rules, without an exact single-rule substitution between the two source strings.

The graphical square and resulting recombination are new formalized candidates in this campaign. Some component matches were present in the earlier search; priority over the held scholarship is unresolved. The relevant target strings had already appeared in exploratory outputs, so this is not a claim of blind prediction.

The pair of rules ranks first among **290 combinations of previously observed individual roof/tick marker candidates**, of which 234 terminate without a rewrite cycle. It remains first after withholding the entire 70/71 family and its object/alias observations, before checking the 1380 / 2452 relation. Only this candidate pair unifies that relation. The search restriction and full competing programs are preserved in [composition adjudication](route_a/composition_adjudication.json). The result selects a useful spelling hypothesis within this restricted search; matching normal forms does not itself prove equal referents.

Source-linked derivations and competing marker searches: [Route A report](route_a/REPORT.md), [roof lattice](route_a/roof_lattice_predictions.json). Numerical scope analysis: [Route C report](route_c/REPORT.md), [executable scope results](route_c/roof_count_scope_programs.json).

## What the candidate does and does not force

Sign 87 depicts two long strokes under the existing graphical codebook. Assigning it the operation “duplicate the next glyph” creates a concrete problem. Starting from 66, different valid rewrite orders produce:

```
59–59–211
59–211–59–211
```

The writing rules alone have a common expanded form, `87–59–211`. The conflict appears when literal glyph duplication is added. A modifier applied once to the whole repeated-base field repairs the conflict. An abstract categorical operation with the same scope also repairs it. Thus the record supports a useful **scope question**, but does not establish multiplication, grammatical number, a unit or the meaning of 211.

The same frame also contains `65–59–211` and `104–59–211`. They cannot all be declared synonymous because their surroundings match. If roof 65 already represents two base items, `65–59–211` has three under that particular parser. Sign 104 remains unassigned.

A subsequent fixed-rule search tested `65 → 59–59`, `66 → 59–59–211` and literal marked-fish doubling throughout the strict corpus, outside the defining `267–99` frame, with a separate one-edit/two-anchor lane and partial-observation lane. It found no additional written-repetition transfer. The separate `65 → 87–59` spelling retains other witnesses. Unobserved duplicate spellings are unknown, not disproof; arithmetic productivity has not been established.

The new roof relation also connects miniature-tablet fronts 4493:10 `66–176` and 4556:10 `87–60–176`, whose cup faces carry four and two strokes. **If** the roof relation preserves value, **and** both faces express the same fixed-unit amount, this would require `4u = 2u` with `u > 0`. The combined assumptions fail. Complementary fields remain compatible, so this does not refute the writing operation itself.

## Context and picture tests

Coarse production context does not explain every alternation. The tick pair 1177 / 3103 consists of Mohenjo-daro seals with the same direction code and raw picture code. The new composed pair 1380 / 2452 also consists of Mohenjo-daro seals, although its picture codes differ. Workshop and phase remain uncontrolled. The original roof-only pairs are medium-confounded: the expanded examples are copper tablets. The four-row `267–99` chain spans Lothal, Chanhudaro, Mohenjo-daro and Harappa.

[Eight exact contextual contrasts](route_b/FISH_COMPOSITION_CONTEXT.md) distinguish these cases rather than claiming either universal spelling or universal production conditioning.

Route B built 3,788 faces, including 70 strict multiline faces, 170 distinct short/long correspondences and 429 matched component contrasts. Among 81 strict copper text/picture objects, 33 distinct text/raw-picture links connect 26 complete texts and 20 raw codes. A deterministic exact-text-to-code lookup needs at least seven exceptions. These are catalogue code distinctions, not seven established differences in word meaning.

The source-illustrated elephant/horned-tiger contrast on 3368 / 1704 is decisive against the particular universal model “this entire copper text names the pictured species.” It is explicitly discussed by Parpola and is not a new discovery. The short-sign 363 network likewise does not supply a uniquely identified depicted referent. None of these exclusions rules out text referring to a different entity from the picture.

On 1,081 held-out expression/target/context types, metadata alone costs 2,186.96 prediction bits, text components 2,498.46, and their combination 2,219.46. The component model does not beat that contextual rival. Details: [Route B](route_b/REPORT.md).

## Numerical and phonetic searches

Route C inspected 878 visible or doubtful long-stroke occurrences and 267 cup/other-face records. It tested fixed and conditional unit conversions, addition, multiplication, grouping, repeated-base compression, partial inscriptions and multiline/inline correspondences. On the 11 distinct single-count cross-notation pairs, a constant fitted separately in each training fold has mean log loss 1.182, versus 1.918 for a shared multiplier and 1.274 for an affine program. The affine full-data optimum has slope zero: it ignores the front count. Locus-specific units remove some contradictions by creating largely unconstrained separate scales. They do not earn arithmetic meanings.

The recovered linguistic evidence permits explicit phonetic searches rather than sign prediction alone: 192,482 distinct Sanskrit dictionary headwords, and the existing Tamil fish/star Appendix transcribed as 93 marked entries, 89 with exact-search-eligible forms. The source's category counts and uncertain forms are preserved separately.

A deliberately strong Sanskrit prior, requiring four distinct plain-fish readings and their four marked counterparts all to be dictionary fish terms, leaves `ka` as the shared extension with 360 assignments of roots. **Those eight Indus semantic attachments are assumptions.** Removing the marked-form semantic requirement restores 1,012,704 systems; allowing homophony restores additional markers. The same search also selects `ka` for bird terms, and it is a frequent surviving tree-term extension. The apparent unique sound is therefore not a fish-specific decipherment result.

The two-operation graphical square is more restrictive than one shared suffix. Exact concatenative fish-word squares fail in the held lexicons under the tested requirements. Source-supported Tamil compound-boundary and allomorph analyses produce conditional alternatives, but require an explicit ordering rule to reconcile the separate written 87-prefix and 211-suffix with the proposed lexical components. They are not direct sound substitutions. [Route D](route_d/REPORT.md) supplies exact assignments, alternative segmentations, source references, countermodels and worked partial parses. Printed candidate coverage is not phonetic correctness.

## Joint comparison and decision

The integration runner predicts original field-symbol codes and observed companion cup counts from fixed writing-operation models, including the competing roof-102/tick-211 system. It removes the target expression, all exact aliases and their whole objects from training. It uses a site/medium background and reports expression-type and object weighting separately. It does not multiply the four route reports as independent evidence.

| Candidate | Field-code data bits | Cup-count data bits | Declared rule cost | Composite total |
|---|---:|---:|---:|---:|
| Unmerged categorical expressions | 3,087.20 | 82.37 | 0 | 3,169.57 |
| Fish marks → 211 | 3,084.08 | 82.37 | 11 | 3,177.46 |
| Fish roof → 87 | 3,087.20 | 83.54 | 11 | 3,181.74 |
| Both fish operations | 3,087.42 | 83.54 | 22 | 3,192.96 |
| Competing roof 102 + marks 211 | 3,085.91 | 82.37 | 22 | 3,190.29 |

Lower is better. These are descriptive, model-relative code costs, not calibrated probabilities. The raw channel gains are shown because the declared rule costs are not uniquely determined. The joint test supplies no semantic or numerical confirmation of the composed rule. A separate next-context test gives the 211 model a 6.35-bit advantage over a simple terminal-role model, less than the cost of selecting one marker from 417 before paying for the rest of the rule.

The surviving object of research is the **conditional composition and scope system**. The proposed equal-value, literal-picture and direct-phonetic interpretations have specific failures or unresolved assumptions. No route-local observation has been silently promoted into the existing accepted-claim ledger.

## Reproduce and continue

Python 3.10+; primary research runners use the standard library. Existing recovered source files and extracted linguistic records are included or referenced in the source manifest. From the repository root:

```sh
python research/campaigns/integrated_20260906/run_campaign.py --route a
python research/campaigns/integrated_20260906/run_campaign.py --route b
python research/campaigns/integrated_20260906/run_campaign.py --route c
python research/campaigns/integrated_20260906/run_campaign.py --route d
python research/campaigns/integrated_20260906/run_campaign.py --route integration
```

`--route all` rebuilds the shared observation layer, executes the four routes concurrently, then runs integration and packaging. The individual research entry points were executed in this session; the wrapper is provided for reproduction rather than presented as another completed experiment.

- [Executed task status](TASK_STATUS.md) maps all 53 requested actions to results and specific limitations.
- [Continuation state](continuation.json) gives active models, remaining rivals and the next executable scientific tasks.
- [Candidate ledger](candidate_ledger.json), [dependency records](claim_dependencies.json), [results index](results_index.json) and [source manifest](evidence_inventory/source_manifest.json) retain the evidence chain.
- [Scientific adjudication](adjudication/scientific_review.md) records the few load-bearing implementation defects and their corrected results.

Research is paused at the preserved state described here; it is not running unattended, and the script has not been deciphered.
