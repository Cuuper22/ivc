# Effective-Unicity Known-Script Comparator

Date: 2026-05-29

## What This Note Is

This note calibrates our main structural instrument against writing systems that people can already read. A comparator is a control corpus scored with the exact same instrument as the Indus data, so we can see where the Indus number sits relative to a known quantity. Without one, a score has no scale.

The instrument is the Vector 2 effective-unicity masked-sign test: hide one sign at a time and ask a model to guess it from its neighbours. Effective unicity is the question of whether the surviving inscriptions constrain a solution enough to make one reading uniquely recoverable.

## Result

The Vector 2 effective-unicity instrument now has known-script scarcity calibration against Linear B Series D, plus a separate glyph-only administrative-script calibration against SumTablets. Scarcity calibration means cutting the known corpus down to Indus-like size and inscription length first, so the comparison is fair.

This is not a decipherment and not language-family evidence. It asks a simpler control question: when a readable script is reduced to Indus-like short rows and its readings are hidden, how much local context can a structural masked-sign model recover?

## Provenance

Linear B source file:

- `data/open_prototype/known_scripts/linear_b_series_d/Samples.txt`
- DOI: `10.5281/zenodo.7404653`
- MD5: `0c9b9190b86840c82cafdbf4f4b8c827`
- MD5 status: verified by `data/open_prototype/tools/linear_b_series_d_gapped_heldout.mjs`

Linear B generated files:

- `data/open_prototype/reports/linear_b_series_d_scarcity_summary.json`
- `data/open_prototype/reports/linear_b_series_d_gapped_heldout_summary.json`
- `data/open_prototype/reports/effective_unicity_known_script_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_known_script_comparator.csv`

SumTablets generated files:

- `data/open_prototype/known_scripts/sumtablets/sumtablets_source_manifest.json`
- `data/open_prototype/reports/effective_unicity_sumtablets_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_sumtablets_comparator.csv`
- `docs/effective_unicity_sumtablets_comparator.md`

## Primary Comparison

Top-1 is the share of hidden signs the model guesses exactly right; top-5 is the share where the right sign is in its first five guesses. Label bits measures how much information a full assignment of values to signs would take — the size of the unanchored solution space.

| System / test | Rows | Tokens or gaps | Signs/tokens | Label bits | Top-1 | Top-5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Indus strict exact-collapsed masked signs | 1,798 | 8,212 | 571 | 4,410.970864 | 0.279591 | 0.534096 |
| Linear B, IVC-length cap, clean bidirectional masking | 299 | 1,755 | 91 | 465.505030 | 0.435897 | 0.698006 |
| Linear B, IVC-length cap, source-gapped sequence leave-out | 299 | 299 | 91 | 465.505030 | 0.294314 | 0.638796 |
| SumTablets, glyph-only IVC-length-capped admin lines | 1,798 | 8,716 | 358 | 2,526.289215 | 0.171753 | 0.373681 |

## Interpretation

The Indus masked top-1 score is close to the Linear B source-gapped sequence-leave-out score under the same IVC p95 length cap. That matters because it shows the Indus constraint signal is not obviously vacuous.

The ceiling remains just as important. Clean Linear B bidirectional masking is much stronger, Linear B top-5 recovery is higher, and the Linear B capped comparator has 91 signs/tokens versus 571 Indus signs. The Indus label-symmetry burden is therefore much larger.

SumTablets adds a different known-script/admin calibration point. It is a known readable writing system, not a nonlinguistic null — a control corpus with no language behind it at all. In the glyph-only line-level setup, it scores below Indus while still beating its own matched controls, which means the comparator battery is no longer a single Linear B ruler.

Plainly: Vector 2 now has a useful known-script calibration, but no reading is earned. The result is structural: there is local constraint, and the unanchored solution space is still huge.

## Ledger Boundary

Accepted claim counts remain zero. These comparators strengthen the live Vector 2 candidate but do not accept it, because the Indus side still depends on the T3 Lipi metadata layer — our catalog-derived working table — on exact-only deduplication, which merges only byte-identical inscriptions and so leaves near-duplicates in, and on no external value anchor: no independent source that fixes what any sign stands for.
