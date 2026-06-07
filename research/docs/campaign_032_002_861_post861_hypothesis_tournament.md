# 032-002-861 Post-861 Hypothesis Tournament

Date: 2026-05-29

## Question

What is the post-`861` field doing as a language system?

The unit is no longer one sign. The unit is the whole strict `002-861` continuation field: closure, simple single-sign tails, fixed pairs, and longer continuations. The aim is to increase reading probability by ranking competing linguistic hypotheses and their kill gates, not by proving one catalog crosswalk.

## Inputs

- Canonical universe: `data/open_prototype/reports/campaign_032_002_861_source_normalized_tail_predictor_all_rows.csv`
- Rows: `144`
- Non-bare rows: `31`
- Source-ready rows: `14`
- Generated script: `tmp/run_032_002_861_post861_hypothesis_tournament.py`
- Generated reports:
  - `data/open_prototype/reports/campaign_032_002_861_post861_hypothesis_tournament_feature_information.csv`
  - `data/open_prototype/reports/campaign_032_002_861_post861_hypothesis_tournament_ranked_lanes.csv`
  - `data/open_prototype/reports/campaign_032_002_861_post861_hypothesis_tournament_tail_classes.csv`
  - `data/open_prototype/reports/campaign_032_002_861_post861_hypothesis_tournament_hypotheses.csv`
  - `data/open_prototype/reports/campaign_032_002_861_post861_hypothesis_tournament_summary.json`

## Tail-Class Field

The post-`861` zone is not one suffix candidate.

| Class | Rows | Family cells | Source-ready | Tail distribution |
|---|---:|---:|---:|---|
| closure | 113 | 110 | 7 | `<END>:113` |
| simple single | 22 | 17 | 3 | `416:6;603:3;698:2;000:1;125:1;216:1;626:1;392:1;683:1;096:1;832:1;901:1;031:1;803:1` |
| fixed pair | 5 | 5 | 3 | `533 717:2;244 165:1;831 165:1;255 416:1` |
| long continuation | 4 | 4 | 1 | `791 440 717:1;032 520 919 140:1;036 460 513:1;360 520 919 140:1` |

The live claim is a typed secondary-zone model: `002-861` is closure-capable, but a small field after it can carry several continuation types. This is a structural hypothesis only. No sign values, phonetics, language identity, or translation are accepted.

## Predictor Pressure

Feature information says preframe is carrying more signal than broad artifact metadata.

| Feature | Non-bare MI | Tail-class MI | Tail-identity MI |
|---|---:|---:|---:|
| `prefix` | 0.737562 | 0.986610 | 1.559061 |
| `prefix_last3` | 0.723673 | 0.972721 | 1.545172 |
| `prefix_last2` | 0.673069 | 0.908228 | 1.480679 |
| `prefix_last1` | 0.409266 | 0.616648 | 1.175210 |
| `register_key` | 0.424267 | 0.615921 | 1.195453 |
| `broad_register_key` | 0.398909 | 0.568028 | 1.147560 |

This does not prove grammar, because exact-prefix contrasts are still scarce and terminal-space is a live adversary. It does decide where to work: preframe lanes are the ranked research targets; register stays as an adversarial predictor and control layer, not as the target object.

## Ranked Research Lanes

1. `prefix_last1=032` and `prefix_last2=220 032`
   - `032`: `10` rows, tail split `<END>:8;255 416:1;603:1`.
   - `220 032`: `7` rows, tail split `<END>:5;255 416:1;603:1`.
   - Research value: best minimal-contrast-style field, already source-visible in five rows.
   - Current blocker: terminal-space recut favors the layout-capacity adversary, so this lane is blocked from grammar promotion.
   - Kill gate: if tail presence tracks available terminal space better than sign context, this lane remains positional/layout evidence only.

2. `prefix_last1=176`
   - `6` rows, tail split `<END>:4;392:1;533 717:1`.
   - Research value: lateral test for whether fixed-pair behavior belongs to a preframe family or only to the no-icon `SEAL:R` cell.
   - Kill gate: if `392` and `533-717` remain unrelated singleton outcomes after source routing, do not infer a selector.

3. Empty-prefix `002-861-X`
   - `9` rows, all non-bare: `416:6;698:2;096:1`.
   - Research value: possible special construction, not comparable to full-prefix post-`861` tails until source images exist.
   - Kill gate: if source routing collapses these into Harappa TAB:I and Mohenjo no-icon copy/template pockets, quarantine as object/register templates.

4. `prefix_last1=235`
   - `8` rows, tail split `<END>:7;360 520 919 140:1`.
   - Research value: long-continuation adversary in a wider preframe lane.
   - Kill gate: if the long tail is explained by same-register/source-layout only, it remains a second-unit adversary and not a syntactic class.

5. `prefix_last1=031`
   - `7` rows, tail split `<END>:5;244 165:1;791 440 717:1`.
   - Research value: unproven fixed-pair and long-tail comparison lane.
   - Kill gate: source-pending status keeps it low priority until at least one non-bare witness is source-visible.

6. `exact_prefix=390 004`
   - Current split: `<END>:1;125:1`, both source-pending.
   - Research value: tiny but exact-prefix clean if source images hold.
   - Process rule: route it as part of the exact-prefix contrast batch, not as a 12-hour one-sign campaign.

## Adversarial Context Fields

Register fields are not ranked as target lanes, but they are required controls.

- `Mohenjo-daro|SEAL:S|Bull1:W|square`: `23` rows, tail split `<END>:17;032 520 919 140:1;832:1;036 460 513:1;031:1;603:1;803:1`.
- `Mohenjo-daro|SEAL:R|None`: `7` rows, `5` source-ready, tail split `<END>:3;533 717:2;360 520 919 140:1;603:1`.

If these register fields predict tail choice better than preframe after source-family and terminal-space controls, the grammar model is demoted to register/template behavior.

## Competing Hypotheses

1. `post_861_secondary_zone_is_typed_not_one_suffix`
   - Support: closure dominates, but non-bare rows split into simple singles, fixed pairs, and long continuations across multiple lanes.
   - Increase probability: class behavior survives source-family collapse, source-token continuity, and terminal-space controls.
   - Kill: every source-live non-bare row is explained by terminal margin, side-order, or one copied source/register family.

2. `terminal_space_or_line_capacity_selects_tail_presence`
   - Support: the `220-032` recut found tailed rows with `195px` and `120px` candidate windows, while bare controls had only `28-38px` marked post-terminal margins.
   - Increase probability: tails only appear when a tail-sized terminal zone exists.
   - Kill: bare rows with comparable terminal space still choose closure, or tailed rows are squeezed into ordinary sign flow.

3. `whole_formula_templates_not_optional_grammar`
   - Support: exact-prefix mixed groups are scarce; many tail contrasts are last-1/last-2 or register-level rather than exact formula-level.
   - Increase probability: complete left formula predicts tail better than tail class after `861`.
   - Kill: same formulas or near-formulas show source-visible closure/simple/fixed/long alternatives under comparable layout.

4. `register_or_object_label_system`
   - Support: `416` is concentrated in Harappa `TAB:I`, `533-717` in no-icon Mohenjo `SEAL:R`, and `698` in no-icon Mohenjo square rows.
   - Increase probability: site/type/icon/shape predicts tails after controlling preframe.
   - Kill: same tail class recurs across independent registers with stable placement and matched layouts.

5. `sign_list_segmentation_or_terminal_badge_artifact`
   - Support: the `861|tail` boundary is catalog-mediated; `255-416` especially depends on one large source window.
   - Increase probability: blind source-first segmentation fails to recover the `861` boundary or tails align with icon/edge geometry.
   - Kill: source-first annotators recover the same boundary and class behavior across different compositions.

## Decision Tree From Here

1. Run a same method, blind-first terminal-space recut across source-ready lanes, not only `220-032`.
   - If terminal-space predicts tail class better than preframe/register, stop grammar promotion and treat tails as layout-conditioned continuation zones.
   - If bare controls with tail-sized space still close, the typed secondary-zone hypothesis upgrades.

2. Batch formula clustering before the `861` split.
   - If whole formulas predict tails, interpret as template families.
   - If formulas leave real alternations, keep the grammar hypothesis alive.

3. Run source-family collapse on the ranked lanes.
   - If `603`, `533-717`, or long continuations collapse to one family pocket, park them.
   - If a class survives two or more independent family cells in at least two lanes, promote the class, not the value.

4. Only then route exact-prefix acquisition targets.
   - `390 004` is useful because exact-prefix contrast is cleaner than last-two contrast.
   - It is not allowed to become the whole campaign unless it changes the class model.

## Current Decision

The post-`861` field is alive as a typed secondary-zone research object. The strongest positive model is closure plus typed continuation after `002-861`. The strongest adversarial model is terminal-space/formula/register behavior sitting after a cataloged `002-861` boundary.

The next campaign should attack the model at class level:

- terminal-space across source-ready lanes,
- whole-formula clustering before `861`,
- source-family collapse of tail classes.

Do not spend another long run on a single tail unless it changes one of those class-level decisions.

Accepted values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain `0`.
