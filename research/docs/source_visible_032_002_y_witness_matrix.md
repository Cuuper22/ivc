# Source-Visible `032-002-Y` Witness Matrix

Date: 2026-05-29

## Result

Status update: this candidate has been retracted after blind matched-negative source-box adjudication. Keep this file as a witness inventory, not as support for an accepted or live claim.

The source-visible layer initially suggested a narrow structural candidate:

> `032-002-Y` is visible as a same-signband packet across target `240-220-032`, non-240 `A-220-032`, and outside-`A-220` contexts. This weakens the objection that the packet is only a catalog adjacency artifact.

This is not an accepted claim. It does not establish final token segmentation, sign values, phonetics, language identity, translation, or even a final `Y` function. The later claim-specific forger failed: two blind reviewers recovered zero positives as confident positives and produced yes-only false-positive rates of 0.400000 and 0.300000 on negatives. See `docs/source_box_blind_adjudication_results.md`.

## Evidence

Generated artifacts:

- `data/open_prototype/tools/source_visible_032_002_y_matrix.mjs`
- `data/open_prototype/reports/source_visible_032_002_y_witness_matrix.csv`
- `data/open_prototype/reports/source_visible_032_002_y_coverage_null_iterations.csv`
- `data/open_prototype/reports/source_visible_032_002_y_summary.json`

Source-visible rows with same physical line:

| Row | Category | Y | Site | Token-box tier |
| --- | --- | ---: | --- | --- |
| `M-722` | target `240-220-032` | `817` | Mohenjo-daro | medium candidate |
| `M-49` | target `240-220-032` | `300` | Mohenjo-daro | medium candidate |
| `H-444` | non-240 `A-220-032` | `861` | Harappa | medium candidate |
| `M-375` | non-240 `A-220-032` | `820` | Mohenjo-daro | medium-low candidate |
| `C-10` | non-240 `A-220-032` | `817` | Chanhu-daro | low-res candidate |
| `M-21` | outside `A-220` | `861` | Mohenjo-daro | medium candidate |
| `H-597` | outside `A-220` | `861` | Harappa | medium-low candidate |
| `C-60` | outside `A-220` | `861` | Chanhu-daro | weak token box |

Coverage:

| Dimension | Covered values |
| --- | --- |
| contexts | target `240-220-032`; non-240 `A-220-032`; outside `A-220` |
| Y values | `300`, `817`, `820`, `861` |
| sites | Chanhu-daro, Harappa, Mohenjo-daro |

Token-box tiers among the eight source-visible rows:

| Tier | Count |
| --- | ---: |
| medium candidate | 4 |
| medium-low candidate | 2 |
| low-res candidate | 1 |
| weak | 1 |

## Coverage Null

The script sampled 10,000 random 8-row subsets from the 25-row route manifest. This is an exploratory coverage null only, because actual acquisition was target-driven rather than random.

| Criterion | Random-subset rate |
| --- | ---: |
| all three categories covered | 0.8590 |
| at least four Y values covered | 0.2724 |
| at least three sites covered | 0.6342 |
| target and non-240 `817` both present | 0.2125 |
| outside `861` present at three sites | 0.0245 |

Interpretation: broad context coverage is not surprising under random row visibility, so it cannot be used as a strong false-positive result. The later blind source-box test failed, so the coverage shape is only acquisition context, not candidate evidence.

## Skeptic Record

Broken:

- The blind source-box forger found positive-looking packets in negative controls.
- Two blind reviewers recovered zero true positives as confident positives.
- Yes-only false-positive rates were 0.400000 and 0.300000.
- Conservative negative-failure rates were 0.500000 and 0.416667.
- The packet lacked local image-backed `negative_220_032_next_not_002` controls, so the `A-220-032` lane was not even fully stressed.

Residual value:

- The route/source/token-box matrix still records useful acquisition state.
- The rows remain worth recutting or rechecking with a pre-registered sign-shape guide.
- The matrix cannot support a live structural claim until a rebuilt source-box method passes negative controls.

## Decision

Retracted after forger failure.

Allowed wording:

> The source-visible `032-002-Y` witness matrix is a useful source-route inventory, but its first blind matched-negative source-box test failed. It cannot currently support an accepted or live structural claim.

Forbidden wording:

- Current source-visible row-level evidence supports `032-002-Y` as a real same-signband packet.
- The live structural model is `A-220-032 -> 002 -> branch`.
- `032-002-Y` has an accepted phonetic value.
- `817`, `820`, and `861` are interchangeable endings.
- The packet identifies a language family.
- The source-visible claim survived the forger.
