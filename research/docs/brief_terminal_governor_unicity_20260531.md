# One-Page Brief: Terminal-Governor Unicity Pressure

Date: 2026-05-31

Tier: promoted structural candidate, not accepted decipherment

## Result

The strongest current Indus-script result is structural. Signs `002` and `060` behave as terminal governors: when one of them sits in the next-to-last slot of an inscription, the set of signs that can follow it — its closure inventory — is small and constrained. That constraint is real enough to measure: knowing the governor lets you predict the final sign of held-out inscriptions far better than chance.

This is not a phonetic reading. It assigns no sound, no language family, no translation, no sign meaning. What it says is narrower: a specific part of the sign system is doing real grammatical/register work rather than behaving like free emblem noise.

## Core Evidence

Under exact-text collapse (each distinct inscription text counts once), the `002/060` terminal families predict held-out final signs by site:

- Target governors `002/060`: 456 evaluated leave-site rows, top-3 final prediction accuracy `0.787`, mean effective final candidates `6.39`.
- Non-target penultimate signs: 1,138 evaluated rows, top-3 accuracy `0.177`, mean effective candidates `15.71`.
- Final-label shuffle null over the same terminal families: `p=0/1000` for target top-3 accuracy, mean true probability, and effective-candidate compression; `p=0.001` for top-1 accuracy.

The signal is not just Mohenjo-daro square seals. Remove the big blocks and it stays:

- Remove Mohenjo-daro `SEAL:S`: 234 target rows, top-3 `0.761`, effective candidates `6.27`, 100-shuffle null `p=0`.
- Remove Harappa `SEAL:S`: 407 target rows, top-3 `0.806`, effective candidates `5.88`, null `p=0`.
- Remove both Mohenjo-daro and Harappa `SEAL:S`: 185 target rows, top-3 `0.778`, effective candidates `5.85`, null `p=0`.

Nor is it explained by raw penultimate-sign frequency. The nearest high-support non-target penults are far weaker: `740` has 133 evaluated rows with top-3 `0.090`; `220` has 56 with top-3 `0.286`; `390` has 55 with top-3 `0.127`. One small non-target mimic, `240`, reaches top-3 `0.652` — but only over 23 rows, so it should be tested as a separate future bet rather than used as a matched confound.

This strengthens the earlier terminal-governor model: `002->{817,820}` and `060->920` form the hardest-block core, with `060->{550,820}`, `060-692`, and leaky `002-861` as global extensions.

## What Was Killed

- `390` as an external Meluhha personnel/title bridge failed all-sign/all-pair max-stat enrichment: main `390` FPR `0.976`; `740-390` and `390-590` FPR `1`.
- `055 -> Brahmi ra` died on shape-null `0.097727` and thin support from only two object families.
- Damaged `002-000` rows did not yield a clean source-visible adjudication.
- `845` is not independent from `407`; its copper signal vanishes without `407`.
- `740-X-590` remains a repeated syntactic frame only. Its attempted semantic filler split failed.

## Live Companions

- `095` is a fragile candidate for an independent copper `TAB:C` subregister: non-`407` support has 4 object rows, 3 exact texts, and 2 prefix frames.
- `405/806` are candidates for a Bull1:W square-seal subtype/register. After removing the `740-X-590` frame and Harappa, `806` still survives max-stat stress; `405` weakens first and should be treated as the weaker partner.

## Next Test That Matters

The decisive next test is source-family/source-token collapse for the `002/060` terminal-governor unicity result — that is, count each physical source family once instead of each catalog row. If source-verified token families keep the top-3/effective-candidate advantage after excluding the major square-seal blocks, this becomes the cleanest structural finding in the project.
