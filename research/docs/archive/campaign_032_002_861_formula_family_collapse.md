# 032-002-861 Formula-Family Collapse Attack

Date: 2026-05-29

This note is the hardest attack the campaign has run on its own model. The model says something interesting happens after `002-861`. The attack says: nothing does — what looks like variety is really a handful of stock inscriptions repeated, and once you refuse to count the same stock inscription twice, the variety disappears. This pass reruns every count with near-identical rows collapsed into single cells. Two claims survive that treatment in a bounded form; several are demoted outright.

## Question

Does the post-`861` secondary-zone model survive the strongest current adversary — the rival explanation that most threatens it: whole-left-formula templates and source/register family collapse? "Collapse" means refusing to count near-identical rows separately: rows that share a stock phrase, an object class, or a publication route are merged into one piece of evidence.

This is not a tail-value campaign. It asks whether the apparent post-`861` continuation field is productive enough to remain a language question, or whether it collapses into repeated formula pockets, object/register labels, and source-family artifacts.

## Inputs

- Canonical universe: `data/open_prototype/reports/campaign_032_002_861_source_normalized_tail_predictor_all_rows.csv`
- Rows: `144`
- Non-bare rows: `31`
- Source-ready rows: `14`
- Script: `tmp/run_032_002_861_formula_family_collapse.py`
- Reports:
  - `data/open_prototype/reports/campaign_032_002_861_formula_family_collapse_exact_prefix_groups.csv`
  - `data/open_prototype/reports/campaign_032_002_861_formula_family_collapse_tail_class_collapse.csv`
  - `data/open_prototype/reports/campaign_032_002_861_formula_family_collapse_tail_identity_collapse.csv`
  - `data/open_prototype/reports/campaign_032_002_861_formula_family_collapse_attack_verdicts.csv`
  - `data/open_prototype/reports/campaign_032_002_861_formula_family_collapse_summary.json`

Mechanic constraints used. A "family cell" is one group of rows treated as a single piece of evidence; the keys below define what counts as the same cell:

- Blank full prefix is normalized as `<START>`.
- Source-ready means `source_status` is not blank or `source_pending_or_not_checked`, or `display_image` is present.
- Strict identity family key is `(tail, prefix_norm, register_key, template_key)`.
- Strict class family key is `(tail_class, prefix_norm, register_key, template_key)`.

## Main Result

The post-`861` field survives as a structural object, but not as grammar yet.

The formula/template adversary is now the main blocker. Complete left formula carries the strongest signal, while true exact-prefix alternation is almost absent. In the current 144-row universe, only one exact-prefix group contains both closure and non-bare continuation:

| Exact prefix | Rows | Tail split | Source-ready non-bare | Status |
|---|---:|---|---:|---|
| `390 004` | 2 | `125:1;<END>:1` | 0 | source-pending exact-prefix split |

A "preframe" is the run of signs immediately before `002-861`, and "last-k" means only the final k of them are compared. This means most visible variation is being created by pooling different full formulas under looser last-k preframes. That can still be real grammar, but formula templates have not been beaten.

## Tail-Class Collapse

| Tail class | Rows | Strict class family cells | Tail identities | Exact prefixes | Registers | Source-ready | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| closure | 113 | 110 | 1 | 101 | 58 | 7 | background closure state |
| simple single | 22 | 16 | 14 | 14 | 13 | 3 | class alive, but empty-prefix/copy-family pressure active |
| fixed pair | 5 | 5 | 4 | 5 | 4 | 3 | heterogeneous fixed units, no shared value |
| long continuation | 4 | 4 | 4 | 4 | 3 | 1 | second-unit adversary, not productive class yet |

Class-level result:

- Closure is broad and real as a state.
- Simple-single tails remain alive as a class, but the class is polluted by empty-prefix source-pending rows.
- Fixed pairs exist as a structural class, but they are heterogeneous and do not imply one function.
- Long continuations are currently adversarial controls, not positive grammar evidence.

## Tail-Identity Collapse

| Tail | Rows | Strict identity cells | Source-ready | Verdict |
|---|---:|---:|---:|---|
| `603` | 3 | 3 | 3 | post-`861` simple-tail class survives; no value |
| `533 717` | 2 | 2 | 2 | fixed final unit survives; narrow register; no function |
| `416` | 6 | 1 | 0 | demoted as copy/register template |
| `698` | 2 | 1 | 0 | demoted as copy/register template |
| `255 416` | 1 | 1 | 1 | singleton contrast only |
| `360 520 919 140` | 1 | 1 | 1 | singleton long-continuation adversary |

Everything else is singleton watch material.

The key demotion is hard: `416` has six rows but collapses to one strict identity family cell: empty prefix, Harappa `TAB:I|None|rectangular`, source-pending. `698` has two rows but collapses to one empty-prefix Mohenjo no-symbol square cell. These are not grammar evidence.

The key survivor is bounded: `603` has three source-ready post-`861` cells across three exact prefixes and three registers. It survives as post-`861` simple-tail behavior, not as a value and not as a Harappa bridge.

The fixed-tail survivor remains narrow: `533-717` has two source-ready identity cells and two exact prefixes, but one register: Mohenjo no-icon `SEAL:R|cuboid-convex`. It stays a fixed final-unit comparator, not a function.

## Exact-Prefix Attack

The exact-prefix test is hostile to easy grammar.

- Only `390 004` has closure/non-bare alternation, and it is source-pending.
- The source-ready non-bare rows are mostly exact-prefix singletons, so they cannot prove exact formula alternation.
- `<START>` is an all-non-bare special field: `416:6;698:2;096:1`, with no closure control and no source-ready rows.
- Repeated closure formulas exist as background, e.g. `740 482 240` has seven closure rows.

Decision:

- Exact-prefix evidence blocks promotion of optional post-`861` grammar.
- It does not kill the typed field, because simple/fixed/long classes still occupy multiple prefixes and family cells.
- The next exact-prefix acquisition target remains `390 004`, but only as part of the exact-prefix batch.

## Current Interpretation

The live interpretation is now:

`002-861` marks a closure-capable point with a possible typed secondary zone. The field contains closure, simple single tails, fixed pairs, and long continuations. However, grammar promotion is blocked by whole-formula templates, source/register family collapse, and terminal-space.

What survived:

- The post-`861` field as a structural research object.
- `603` as the strongest post-`861` simple-tail behavior.
- `533-717` as a fixed final-unit comparator inside one narrow register.
- Long continuations as hostile controls against suffix over-reading.

What was demoted:

- `416/698/096` as grammar evidence.
- Any claim that `220-032` proves a grammar slot.
- Any attempt to infer a sign value from `603`, `533-717`, `255-416`, or `125`.

## Decision Tree

1. Formula/template attack
   - Current result: strongest adversary.
   - If complete left formula keeps predicting tail outcome, do not promote grammar.
   - If exact or near-exact source-visible formulas show closure/simple/fixed/long alternation under matched layout, typed grammar upgrades.

2. Family-collapse attack
   - Current result: `416/698` demoted; `603` and `533-717` bounded.
   - If a tail class survives in at least two independent preframe lanes and two independent source/register families, promote class behavior.
   - If it collapses to one register/workshop/source pocket, park it.

3. Terminal-space attack
   - Current result: unresolved globally; already blocks `220-032`.
   - If tail class tracks terminal free space better than preframe, demote to layout-conditioned continuation.
   - If bare rows with tail-sized space still close, grammar gets stronger.

4. Exact-prefix acquisition
   - `390 004` is useful because it is the only closure/non-bare exact-prefix split in this universe.
   - It must be routed as part of a batch, not allowed to become another 12-hour one-sign campaign.

## Next Campaign

Run the terminal-space and source-first segmentation attack across all source-ready ranked lanes:

- `220-032`: already blocked, but needs a uniform blind recut including pending rows if obtainable.
- `603`: use the three source-ready post-`861` rows as simple-tail witnesses, not as values.
- `533-717`: score only as fixed-unit comparator against same-register controls.
- Long tails: source-route and segment `K-40`, `M-1661`, `M-20`, and `M-355`; count them only if they are continuous post-`861` signs.
- Empty-prefix rows: quarantine — set aside, uncitable as evidence — until source panels exist.

Accepted values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain `0`.
