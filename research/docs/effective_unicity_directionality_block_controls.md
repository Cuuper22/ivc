# Effective-Unicity Directionality Block Controls

Date: 2026-05-29

## Purpose

This is a hostile follow-up to the Vector 2 directionality candidate. The earlier directionality comparator removed each tested row from the model. This run removes whole provenance/register blocks before scoring each row, then asks whether stored order still beats reversed order.

The target failure mode is simple: the directionality signal might be only a site, object-type, iconography, or edge-family habit rather than a corpus-level ordering constraint.

## Result

The result is mixed in a useful way.

In the harsh scope already used by the main comparator, top-10 edge signs removed plus one-edit families collapsed, directionality survives `site|type|symbol` block holdout:

- rows: 365
- stored-win share: 0.827397
- holdout blocks: 110
- median held-out transitions: 67
- max null >= observed share: 0 across 200 iterations per control

The same harsh scope does not cleanly survive full leave-site-out:

- rows: 365
- stored-win share: 0.753425
- holdout blocks: 11
- median held-out transitions: 1258
- max null >= observed share: 0.100000

That full-site test is very severe because one site block can remove most of the harsh corpus from the training model. It is still an important skeptic result: the current directionality candidate should not be phrased as source-site-generalized.

The register-edge-family collapsed scope gives the same boundary. It survives `site|type|symbol` holdout with stored-win share 0.835227 and max null >= observed share 0.005000, but full leave-site-out weakens to stored-win share 0.774621 with max null >= observed share 0.265000.

## Primary Rows

| Scope | Holdout | Rows | Stored win share | Max null >= observed |
| --- | --- | ---: | ---: | ---: |
| exact-collapsed | leave one row out | 1,798 | 0.947720 | 0 |
| exact-collapsed | leave site out | 1,798 | 0.928810 | 0 |
| exact-collapsed | leave site-type-symbol out | 1,798 | 0.943826 | 0 |
| top10-edge removed + one-edit collapsed | leave one row out | 365 | 0.841096 | 0 |
| top10-edge removed + one-edit collapsed | leave site out | 365 | 0.753425 | 0.100000 |
| top10-edge removed + one-edit collapsed | leave site-type-symbol out | 365 | 0.827397 | 0 |
| top10-edge removed + one-edit collapsed | leave register-edge out | 365 | 0.841096 | 0 |
| top10-edge removed + register-edge-family collapsed | leave one row out | 528 | 0.837121 | 0.040000 |
| top10-edge removed + register-edge-family collapsed | leave site out | 528 | 0.774621 | 0.265000 |
| top10-edge removed + register-edge-family collapsed | leave site-type-symbol out | 528 | 0.835227 | 0.005000 |
| top10-edge removed + register-edge-family collapsed | leave register-edge out | 528 | 0.837121 | 0.015000 |

## Controls

The run uses 200 iterations for each null control:

- global token shuffle,
- row-internal shuffle,
- position-slot shuffle,
- edge-frame shuffle,
- register-position shuffle,
- register-edge-interior shuffle.

The last two controls preserve more provenance structure by keeping tokens inside `site|type|material|symbol` position pools or inside register plus edge-frame pools.

## Decision

Promote as a narrower live support fact, not an accepted claim:

> In the current Lipi T3 layer, harsh Indus stored-order directionality survives `site|type|symbol` block holdout and register-edge-family collapse, but it weakens under full leave-site-out.

Forbidden wording:

- Do not say the directionality result is source-normalized.
- Do not say it proves writing, language, sound, meaning, or translation.
- Do not say it is site-generalized under full leave-site-out.

## Artifacts

- `data/open_prototype/tools/effective_unicity_directionality_block_controls.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_block_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_block_controls.csv`
- `data/open_prototype/reports/effective_unicity_directionality_block_null_summary.csv`
- `data/open_prototype/reports/effective_unicity_directionality_block_null_iterations.csv`
