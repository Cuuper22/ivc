# Strongest Current Result: A Carrier-Conditioned Role Backbone

Date: 2026-05-31, America/Los_Angeles

## Plain Claim

The current strongest result is not a translation and not a phonetic reading. It is a structural claim: a subset of Indus signs behaves like a carrier-conditioned role grammar across object classes.

The minimal model is split after length/carrier stress:

- Hard core: `740 -> 002`, `002 -> {861,820}`, and `806 -> 002`
- Scoped edge: tablet/account `400 -> 740`
- Soft periphery: `817` terminal-partner edges and thin-slice `740 -> 820`
- Rectangular/copper strings: `407` feeds the `806` boundary zone

## Why This Is Hard To Dismiss

The role backbone is not one cherry-picked pair. It is a convergent set of independently tested constraints:

- Initial sign carries carrier information: `I(first sign; carrier class)=0.6023` bits; row-internal shuffle FPR `0`, carrier-label shuffle FPR `0`.
- `400` is the tablet/account frame: `187/765` TAB:B/I rows vs `100/2738` background; Bonferroni `3.63e-59`; maxstat FPR `0`.
- `400` precedes `740` in co-occurrence rows: `127/140`; row-shuffle maxstat FPR `0`. This edge is carrier-scoped: tablet/account rows are `104/105`, while square-seal rows are split and should not be treated as a universal `400 -> 740` rule.
- `740` is the strongest precedence hub: rank `1/13`, with 26 qualified outgoing edges; row-internal maxstat FPR `0`.
- `002` is the strongest preterminal bridge: rank `1/48`; outgoing terminal partners `861/820/817`; bridge maxstat FPR `0`.
- `407/806` split in rectangular/copper rows: `407` is initial-heavy, `806` is boundary-heavy; direct Fisher tests `3.74e-10` and `1.75e-12`; row-shuffle maxstat FPR `0`.
- Combined partial-order grammar: 9 usable constraints, 9 pass, `1090/1126` rows satisfied; row-internal shuffle FPR `0`.

Quality and site stress did not collapse the backbone:

- Complete rows: 9/9 constraints pass, `897/921` rows satisfied.
- Non-poor rows: 9/9 pass, `691/710` satisfied.
- Without Mohenjo-daro: 9/9 pass, `479/497` satisfied.
- Without Harappa: 8/9 pass, `795/823` satisfied; the weak edge is `400_before_740`.
- Without both Harappa and Mohenjo-daro: 9/9 pass, `184/194` satisfied.

A destructive cross-site prediction check also survived. Constraints learned from Harappa, Mohenjo-daro, non-major sites, and quality slices were tested on held-out slices. All 8/8 train/test experiments survived the strict gate, no learned constraint conflicted with the current core, and row-shuffle null FPR was `0` in every experiment. Reversed constraints performed at about `0.03-0.06` share while observed shares were about `0.94-0.97`.

A family-collapse check also survived the "repeated object family" objection. When rows were collapsed by `site/type/symbol/cult/material/shape`, all 9/9 backbone constraints survived by family-majority vote, with null FPR `0` for every core constraint. Broader collapses weakened only `400_before_740`, which is exactly why that edge is now scoped to tablet/account contexts rather than claimed as universal.

Length and carrier stratification forced a sharper model. The hard-core edges have zero bad length/carrier slices. The weak slices are concentrated in peripheral/scoped edges: `400_before_740` fails as a universal edge in long rows and square/other carriers, `740_before_817` weakens in long square rows, `002_before_817` weakens in medium tablet/account rows, and `740_before_820` weakens in a small tablet/account slice. That does not kill the backbone; it prevents overclaiming the 817/400 periphery.

## What Got Compressed Or Killed

`806` is not being split into two values. Its rectangular/copper role and its Bull1:W square-seal enrichment are compatible under one boundary/pivot model: occurrence-aware boundary share is `27/51` in rectangular/copper contexts and `11/20` in Bull1:W square contexts. That supports "same role, context-selected use" rather than two readings.

`405/806` as a Bull1:W marker remains a candidate, but not part of the core backbone. It is Harappa-weighted: primary SEAL:S/square gates are strong, but leave-Harappa FPR is about `0.025`.

`741` was demoted. It has J/L pressure, but it is not a clean Bull1:J/L subtype marker: within Bull1 square seals, `741` appears in `25/374` W rows, `40/229` J/L rows, and `52/517` other Bull1 rows.

`520` as an elephant header was killed as a candidate and kept only as a wild-shot prediction. Same-type and square all-sign maxstats are bad, and without Mohenjo-daro the target FPR is `0.214`.

The `861/820/817` terminal partners are not semantic allomorphs under current evidence. The context split failed maxstat tests.

## Best Next Destructive Tests

1. Blindly predict sign order in held-out rows containing two or more of `{400,740,407,806,002,861,820,817}` before checking metadata.
2. Test whether new `806` rows remain boundary-like across both rectangular/copper and Bull1:W contexts.
3. Test non-Harappa Bull1:W square seals for `405/806`; that decides whether the icon candidate is regional or pan-corpus.
4. Keep the external Meluhha vector pointed at commodity/register bridges, not personal-name readings, unless a new source-bound name bridge beats the existing forger.

## Bottom Line

The defensible frontier result right now is a role backbone: carrier-conditioned administrative structure with statistically hard left-edge, bridge, and terminal slots. It earns structural content without claiming sound.
