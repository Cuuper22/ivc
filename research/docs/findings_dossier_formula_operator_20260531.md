# Findings Dossier: Formula/Operator Consolidation

Date: 2026-05-31  
Phase: consolidation window 15:30-16:00 America/Los_Angeles  
Status: candidate-level frontier output. No accepted phonetics, translation, language ID, or sign meaning.

## Promoted Candidate: `060-920` Terminal Cap

**Tier:** promoted candidate, metadata plus blind visual packet. Not accepted.

**Claim:** `060-920` is a portable terminal cap. `741-060` is the dominant feeder into this cap, not the whole phenomenon.

**Evidence:**

- `060-920`: `53` raw rows, `52` exact-collapsed cells.
- Terminal after `920`: `52/53` raw, `51/52` exact-collapsed.
- Exact-collapsed all-bigram tournament: `060-920 -> END` ranks `4/3270` by best successor support.
- `741-060 -> 920`: `31/31` raw and `30/30` exact-collapsed, across `7` sites.
- Successor-shuffle null over bigrams with at least `30` exact cells: `0/5000` reached a `30/30` exact-successor formula.
- Blind packet 1, narrow `741-060-920`: reader recovered `5/6` target panels as same-cluster at medium-low or better.
- Blind packet 2, broad non-`741` `060-920`: reader called all `6/6` positives cap-like, rejected `5/6` `060`-non`920` controls, with one low-confidence possible false positive.

**Survived attacks:**

- Exact duplicate collapse.
- All-bigram max-stat ranking.
- Broad-form correction from narrow `741-060-920` to `060-920`.
- Blind visual packet against `060`-non`920` controls.

**Still vulnerable:**

- Exact token boundaries are not independently boxed sign-by-sign.
- Blind read is one sidecar reader, not a multi-reader adjudication.
- Source images are public trace-cache images, not a fully source-normalized plate edition.
- One exact-collapsed `060-920` row continues after `920`: `Unknown +740-100-415-927-060-920-031+`.

**Falsifiers:**

- A clean source-visible `060-920` row where `920` is not visually terminal or belongs to a different local cluster.
- Multiple `060`-non`920` controls that blind readers call the same cap at comparable rates.
- Source-normalized token boxes showing that the recurring visual cap is not actually `060-920`.

## Promoted Metadata Candidate: Prefix-`806` Series Operator

**Tier:** promoted metadata candidate; visual/source promotion blocked.

**Claim:** `806` has a prefix-conditioned nonterminal role. With prefix `154` or `158`, it selects a `465..475` successor band. `155` and `100` are possible extension members but remain lower-confidence.

**Evidence:**

- Harappa-trained `154/158 + 806 -> 465..475`: `23/23` hits versus `0/23` controls.
- Non-Harappa holdout: `6/6` hits versus `3/58` controls, Fisher `p = 0.0000011203829020606104`.
- Exact-collapse holdout: `6/6` versus `3/44`, Fisher `p = 0.000005286110744019978`.
- Expanded `154/155/158/100`: `32/32` raw and `26/26` exact-collapsed hits; non-Harappa exact-collapse `9/9` versus `0/41`, Fisher `p = 3.9913249350800554e-10`.
- Prev-before-`806` window tournament: `154` ranks first with `14/14` exact cells in window `464..474`; `158` ranks second with `9/9` in `465..475`.

**Survived attacks:**

- Exact duplicate collapse.
- Harappa-to-non-Harappa holdout.
- Predecessor-specific contrast against nonprefix `806`.

**Demotion from visual packet:**

- Blind packet recovered clean visual construction only for `BS007` and `BS010`; `BS011` possible.
- It missed non-Harappa/source-holdout positives `BS002`, `BS006`, and `BS008`.
- Therefore this remains a promoted metadata candidate, not a visual/source-promoted candidate.

## Candidate: `740-H-590` Register Family

**Tier:** candidate, probabilistic.

**Claim:** `740` forms a register family where middle heads such as `390`, `407`, and `405` often select `590`.

**Evidence:**

- `740-390 -> 590`: `40/41` raw, `36/37` exact-collapsed, `7` sites.
- `740-407 -> 590`: `16/16` raw, `6/6` exact-collapsed, `4` sites.
- `740-405 -> 590`: `21/22` raw, `15/16` exact-collapsed, `4` sites.

**Demoters:**

- `M-1669 +740-390+` is metadata-complete/fair and blocks an obligatory `740-390-590` claim.
- `C-87 +740-405+` is metadata-complete/fair and blocks an obligatory `740-405-590` claim.
- `740-407` is exact but copy-pressured.

## Candidate Context Lead: `{090,091}` / `091` External Circular Route Cap

**Tier:** candidate context lead, below formula/operator results.

**Evidence:**

- `091` is enriched in external/circular contexts under broad tests.
- Sidecar max-pair stress says `{090,091}` ranks `#1` for broad external-circular tests after multiple-comparison correction.

**Demoters:**

- Broad external/circular and corridor/circular tests use effectively the same foreground rows.
- Same-type `SEAL:C` controls do not survive pairwise Bonferroni.
- Support is sparse, fragmentary, and source validation remains unresolved.

## Retracted Or Demoted Candidates

- `752-615 -> 503` broad formula: killed as general structural candidate. Raw `29/29`, but exact-collapse leaves `2` cells at one Mohenjo-daro `TAB:C` context.
- `465` terminal/plant suffix inside the `806` series: killed as promoted candidate. Raw `5/5`, but exact-collapse leaves one family cell; broader plant/no-symbol semantics fail hostile sidecar checks.
- `400` primary-face heading: demoted/killed by side-shuffle null at `p_ge = 0.175`.
- `400` companion `700/032` predictor: demoted/killed; companion tests did not survive.

## Single Strongest Result

The strongest current frontier result is the `060-920` terminal cap with dominant `741-060` feeder. It is specific, falsifiable, cross-site, survives exact collapse and broad formula competition, and has direct blind visual support against `060`-non`920` controls.
