# Effective Unicity Without Decipherment

Date: 2026-05-29

## Abstract

Effective unicity asks how far a corpus's own internal structure narrows the space of possible readings. This note computes a structural effective-unicity curve for the local Lipi-derived Indus working corpus. It does not attempt a phonetic reading. The result is useful precisely because it separates two claims that are often blurred: the corpus does contain measurable internal constraint, but unanchored internal constraint does not identify phonetic values or a language family.

The measurement itself is straightforward. At full coverage, the exact-sequence-collapsed strict Lipi layer has 1,798 rows, 8,212 sign tokens, and 571 distinct numeric signs. A leave-one-row-out masked-sign model, which hides one sign and asks the rest of the corpus to guess it, ranks the true sign first in 0.279591 of token positions and in the top five in 0.534096. Against 100 iterations of each of six forger controls, full-coverage masked top-1 false-positive rate is 0 for every tested control. However, the corpus still has a global phonetic label-symmetry lower bound of log2(571!) = 4,410.970864 bits before any many-to-one, one-to-many, or null-sign freedoms are added. Label symmetry means that with no external anchor, every assignment of sound values to signs can be permuted wholesale and fit the internal evidence equally well. That lower bound is not broken by internal distributional evidence.

Conclusion: internal evidence narrows structural roles and local continuations; it does not earn translations, phonetic values, sign meanings, or language-family likelihood. Those require an external anchor.

## Input

Primary input:

- `data/open_prototype/reports/lipi_scope_rows.csv`

Filter:

- `readiness_bucket = lipi_numeric_clean_candidate`
- one or more parsed three-digit tokens

Current counts from the generated artifact:

| Quantity | Count |
| --- | ---: |
| strict numeric-clean rows | 2,883 |
| exact numeric sequence families | 1,798 |
| duplicate rows removed by exact-sequence collapse | 1,085 |
| provenance-aware sequence families | 2,059 |

The provenance-aware key is `token_sequence + site + type + material + symbol`. The main curve uses exact-sequence collapse because it is the more conservative duplicate policy for broad internal structure. This is still a T3 planning corpus, not a source-normalized accepted inscription corpus.

## Reconstructed Limit

The usual short-text ceiling says that individual Indus inscriptions are too short for decipherment. That is not the right unit for this test. The better unit is the coupled corpus: shared signs, repeated contexts, edge behavior, and formula families create constraints across inscriptions. Effective unicity is therefore computable as a solution-space question.

But a separate limit remains: without at least one external value anchor, every phonetic assignment can be globally permuted. If sign `A` is assigned value `x` and sign `B` value `y`, swapping all value labels gives an equally good internal solution unless an outside source names one value. For `V` distinct signs, that produces at least `V!` equivalent labelings. With 571 observed signs, the lower bound is log2(571!) = 4,410.970864 bits. Allowing nulls, allographs, homophony, polyvalence, or underspecified values only expands the space.

Attempted break: use internal context profiles and masked-sign prediction to collapse the space anyway. Result: the corpus does show context constraint, but the label-symmetry argument survives. Internal evidence can say “this sign fits this slot better than that slot.” It cannot name the sound or language family of the slot.

## Metrics

The script computes four families of metrics over increasing corpus coverage. Running them as a curve, from a small slice of the corpus up to all of it, shows whether adding more corpus actually adds constraint:

| Metric | Purpose |
| --- | --- |
| `label_symmetry_log2_bits` | lower bound on unanchored phonetic assignment degeneracy, log2(V!) |
| exact context-profile equivalence | signs with identical observed counts, edge positions, length-position slots, and left/right neighbors |
| leave-one-row-out masked-sign score | local sign predictability from length-position and left/right context |
| forger false-positive rates | whether controls reproduce or exceed observed metrics |

Forger controls:

| Control | Planted structure |
| --- | --- |
| `global_token_shuffle` | pure noise matched on token multiset and row lengths |
| `row_internal_shuffle` | row bag preserved, order destroyed |
| `position_slot_shuffle` | length-position slot frequencies preserved |
| `edge_frame_shuffle` | first/last signs preserved, interiors shuffled |
| `register_blocked_position_shuffle` | site/type/material position pools preserved where possible |
| `template_admin_code` | known nonlinguistic administrative template over observed sign pools |

## Coverage Curve

| Coverage | Rows | Signs | Label bits | Masked top-1 | Top-5 | Mean effective candidates |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.100 | 180 | 200 | 1,245.380507 | 0.223077 | 0.410256 | 44.286775 |
| 0.300 | 539 | 343 | 2,399.460947 | 0.257932 | 0.465183 | 28.378068 |
| 0.500 | 899 | 426 | 3,112.091596 | 0.259599 | 0.496408 | 20.437580 |
| 0.750 | 1,349 | 506 | 3,821.208541 | 0.282853 | 0.522228 | 15.183839 |
| 1.000 | 1,798 | 571 | 4,410.970864 | 0.279591 | 0.534096 | 12.891819 |

The effective-candidate curve falls as coverage grows, which means the coupled corpus is adding real local constraints. The top-1 curve improves more modestly. This is a structural result, not a reading.

At full coverage, exact context-profile equivalence leaves 13 non-singleton classes containing 38 signs; the largest class has 6 signs; 93.345009% of signs are profile singletons. Examples of exact profile-equivalent classes include `058 180 266 386 731 926`, `141 178 327 870 914 918`, and `098 131 678 852`.

## Forger Results

At full coverage, masked top-1 accuracy survives the six tested forgers:

| Control | Null mean | Observed | FPR |
| --- | ---: | ---: | ---: |
| global token shuffle | 0.106400 | 0.279591 | 0 |
| row internal shuffle | 0.120083 | 0.279591 | 0 |
| position slot shuffle | 0.165233 | 0.279591 | 0 |
| edge frame shuffle | 0.165025 | 0.279591 | 0 |
| register-blocked position shuffle | 0.169358 | 0.279591 | 0 |
| template administrative code | 0.087867 | 0.279591 | 0 |

Other metrics do not survive. Exact context-profile uniqueness is not strong evidence because noise-like controls can make signs look more profile-unique. Mean effective-candidate counts are also not clean evidence: edge-frame and position/register controls often match or improve the observed ambiguity score. This kills the tempting but wrong claim that “low ambiguity” alone proves language-like structure.

The structured nonlinguistic comparator was rerun on the current 2,883-row scope. It confirmed that administrative, emblem, and mixed admin/emblem generators can equal or exceed the older broad bidirectional predictability metric in every rerun iteration: broad bidirectional top-1 observed = 0.325865, administrative null mean = 0.472924, emblem null mean = 0.443351, mixed null mean = 0.415069, with `null >= observed` share 1 for all three.

A real-world nonlinguistic and ambiguous-system comparator battery was then added from the Sproat 2014 XML corpus bundle. Pictish stones and Pennsylvania German barn stars / hex signs exceed the Indus masked top-1 reference under the same masked-symbol instrument: Pictish top-1/top-5 = 0.450292 / 0.614035, barn-star top-1/top-5 = 0.367123 / 0.673973, versus Indus 0.279591 / 0.534096. Weather icons sit just below Indus at top-1 and above it at top-5. Therefore the surviving Vector 2 claim is narrower: the strict deduplicated corpus has masked-sign local context constraint beyond the specified effective-unicity controls, but masked local predictability itself is not a language diagnostic.

A directionality comparator was added as a stronger structural discriminator. It scores each stored sequence against its reversed sequence with the tested row removed from the bigram model. The strict exact-collapsed Indus scope has stored-win share 0.947720; after top-10 edge removal and one-edit-family collapse, the harsh Indus scope still has stored-win share 0.841096 with max null >= observed share 0. The strongest current real-world nonlinguistic or ambiguous comparator is Pictish at 0.802139; known scripts sit higher, with Linear B Series D at 0.996403 and SumTablets at 0.935484. A Mayig P-namespace pressure test gives exact-collapsed stored-win share 0.943750, but the harsh Mayig scope drops to 0.666667 over only 24 rows. A later skeptic-control run retracts two tempting support lanes: the source-visible `861` terminal/tail probe scores 1.000000 but has max null >= observed share 1, and matched Lipi/Mayig overlap collapses after top-10 edge removal to Lipi 0.363636 and Mayig 0.473684, each with max null >= observed share 1. The broad harsh Indus directionality result remains live, but the overlap and `861` subset no longer support it.

A block-holdout follow-up narrows the live directionality claim further. In the harsh top-10-edge-removed plus one-edit-family-collapsed scope, stored-order wins remain high under `site|type|symbol` holdout: 0.827397 with max null >= observed share 0 across 200 iterations per control. A register-edge-family collapsed scope gives 0.835227 under the same holdout, with max null >= observed share 0.005000. But full leave-site-out is not clean in the harsh scopes: 0.753425 with max null >= observed share 0.100000 for one-edit collapse, and 0.774621 with max null >= observed share 0.265000 for register-edge-family collapse. So the current result survives register-block controls but is not site-generalized.

A site-balanced resampling control gives the cleanest current boundary. In 1,000 balanced Mohenjo-daro plus Harappa resamples, 112 rows per site, the observed median stored-win share is 0.803571 and max paired null >= observed share is 0.003. When Lothal is added, the cap drops to 16 rows per site and the result becomes null-compatible: observed median 0.541667 and max paired null >= observed share 0.528. In the top-five-site balanced design, cap 6 rows per site, observed median is 0.433333 and max paired null >= observed share is 0.616. This keeps the directionality candidate alive for the two major sites and blocks pan-Indus wording.

Per-site profiles explain the split. Within-site scoring in the same harsh scope gives Mohenjo-daro stored-win share 0.816038 with max null >= observed share 0.002, Harappa 0.741071 with max null >= observed share 0.004, and Lothal 0.312500 with max null >= observed share 0.988. Directionality is therefore visible inside both major sites independently, but not in the current Lothal subset. Smaller sites remain unresolved.

Recorded-direction policy controls add one more boundary. The harsh scope has 354 recorded `R/L` rows and 11 recorded `L/R` rows. Restricting to `R/L` rows leaves stored-win share almost unchanged at 0.838983, with Mohenjo-daro `R/L` at 0.813397 and Harappa `R/L` at 0.769231. Random row-level orientation flips destroy the signal: all-harsh random row flips have null mean 0.471134, p95 0.526027, and null >= stored-as-is share 0. This shows coherent stored-order orientation inside the metadata layer, but does not validate physical source direction because the recorded direction field is inherited and highly imbalanced.

An influence-control diagnostic checks whether the harsh directionality signal is concentrated in a tiny number of rows or coarse register families. Single-row dependence is not visible: the largest supportive row removal changes stored-win share by 0.005931, and the largest absolute row effect is adverse, L-115 at 0.010552. Coarse `site|type|symbol` families matter more: removing `Mohenjo-daro|SEAL:R|None` lowers stored-win share by 0.028975. That is below a single-family dependency threshold, but it is exactly the kind of register/provenance concentration that keeps the source-normalization attack alive.

A source/formula-family control now attacks that objection with a stronger metadata proxy, `site|type|material|symbol|cult|direction`. In the harsh top-10-edge-removed plus one-edit-family-collapsed scope, leave-source-convention-out scoring gives stored-win share 0.832877 with max admissible null >= observed share 0.020000. Collapsing to one deterministic row per source-convention key gives 175 rows and stored-win share 0.805714, with mean stored-minus-reversed per transition 0.817965 and max admissible null >= observed share 0.005000. The admissible result is narrower than "source-independent": it survives source-convention collapse in the dominant `R/L` metadata layer. It does not survive as a physical bidirectionality claim, because exact `L/R` is null-compatible at max null >= observed share 0.520000 and harsh `L/R` has only 11 rows, stored-win share 0, negative mean difference, and max null >= observed share 1.000000. Degenerate identity-preserving controls after source-convention collapse are recorded separately as `max_all_null_ge_observed_share = 1`, not counted as admissible nulls.

A source-validation queue now ranks the rows that matter most for breaking that boundary. In the harsh major-site scope, Mohenjo-daro plus Harappa have 324 rows and pooled stored-win share 0.845679. The queue scans 46 local source/provenance CSV files and finds route hints for 912 CISI identifiers, but the major-site directionality rows are still mostly source-dark: 223 of 324 need a public route or source request, 94 have only non-source-grade catalogue hints, two have public routes ready for boxing, two need request/location work, and three have existing crops that can be reviewed for direction and token order. This is an acquisition instrument only, not source-normalized directionality evidence. A first M-70 source pilot visually checks the queue's top row and upgrades it to row-level source-visible with a broad order-window continuation candidate, still with zero accepted claim increments. Its 15-item matched-negative blind token-box packet failed promotion: two reviewers produced hard target-like hits on scoring negatives, with maximum yes-only false-positive rate 0.714286 and maximum conservative false-positive-or-uncertain rate 0.777778. A follow-up no-overlay packet for `H-654`, `M-1310`, `M-1320`, and `M-811` also failed promotion: max yes-only FPR 0.333333, max conservative FPR 0.666667, one leaked negative label, hard scoring-negative false positives, and unstable target token counts. These rows remain useful source-validation targets, not source-boxed order-window evidence.

A route-conditioned control now closes another shortcut. In the frozen public-route probe universe, the top-79 route-probe rows have stored-win share 0.670886. The 38 public CISI plate-route candidates alone score 0.684211, while the 41 no-public-route rows score 0.658537. Collapsing public-route rows by source page drops the share to 0.625000; collapsing by `site|type|symbol|direction` gives 0.619048; collapsing by `site|type|material|symbol|direction` gives 0.652174. The v2e possible/strong signband-like subset reaches 0.741935 before collapse, but drops to 0.692308 by page and 0.647059 by `site|type|symbol|direction`. Matched route-label nulls blocked by priority, site, type, symbol, direction, and length bin reproduce or exceed the observed route share with null >= observed share 1. Public route visibility is therefore not source-normalized directionality evidence.

## Known-Script Scarcity Comparator

A scarcity comparator takes a script we can already read, hides its readings, and cuts it down to Indus-like conditions. That gives a fair ceiling: it shows what the same instrument scores on a corpus we know is real writing. The known-script comparator battery now has two controls: Linear B Series D and SumTablets. Linear B uses the local Zenodo sample file, `data/open_prototype/known_scripts/linear_b_series_d/Samples.txt`, MD5 `0c9b9190b86840c82cafdbf4f4b8c827`, verified by the gapped-heldout script. SumTablets uses Hugging Face dataset `colesimmons/SumTablets`, dataset SHA `11638cd142afbed716df43c55d8810d47fb9b52c`, with `transliteration` and `glyph_names` intentionally excluded from local cache and scoring. These comparators hide known readings from the model; they do not use known-script philology to infer anything about Indus signs.

Generated artifacts:

- `data/open_prototype/reports/linear_b_series_d_scarcity_summary.json`
- `data/open_prototype/reports/linear_b_series_d_gapped_heldout_summary.json`
- `data/open_prototype/reports/effective_unicity_known_script_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_known_script_comparator.csv`
- `data/open_prototype/reports/effective_unicity_nonlinguistic_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_nonlinguistic_comparator.csv`
- `data/open_prototype/reports/effective_unicity_sumtablets_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_sumtablets_comparator.csv`
- `data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_comparator.csv`
- `data/open_prototype/reports/effective_unicity_directionality_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_comparator.csv`
- `data/open_prototype/tools/effective_unicity_directionality_skeptic_controls.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_skeptic_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_skeptic_controls.csv`
- `data/open_prototype/tools/effective_unicity_directionality_block_controls.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_block_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_block_controls.csv`
- `data/open_prototype/tools/effective_unicity_directionality_site_balance.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_site_balance_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_site_balance.csv`
- `data/open_prototype/tools/effective_unicity_directionality_site_profiles.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_site_profiles_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_site_profiles.csv`
- `data/open_prototype/tools/effective_unicity_directionality_policy_controls.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_policy_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_policy_controls.csv`
- `data/open_prototype/tools/effective_unicity_directionality_influence_controls.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_influence_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_influence_rows.csv`
- `data/open_prototype/reports/effective_unicity_directionality_influence_families.csv`
- `data/open_prototype/tools/effective_unicity_directionality_formula_family_controls.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_formula_family_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_formula_family_controls.csv`
- `docs/effective_unicity_directionality_formula_family_controls.md`
- `data/open_prototype/tools/effective_unicity_directionality_route_conditioned_control.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_route_conditioned_control_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_route_conditioned_control.csv`
- `docs/effective_unicity_directionality_route_conditioned_control.md`
- `data/open_prototype/tools/effective_unicity_directionality_source_queue.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_source_queue_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_source_queue.csv`
- `data/open_prototype/reports/effective_unicity_directionality_source_queue_source_index.csv`
- `data/open_prototype/reports/effective_unicity_directionality_m70_source_pilot.csv`
- `data/open_prototype/reports/effective_unicity_m70_blind_token_box_packet_summary.json`
- `data/open_prototype/reports/effective_unicity_m70_blind_token_box_review_summary.json`
- `data/open_prototype/tools/effective_unicity_directionality_blind_packet.py`
- `data/open_prototype/tools/score_effective_unicity_directionality_blind_reviews.py`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_review_summary.json`
- `docs/effective_unicity_directionality_blind_packet.md`

Primary calibration:

| System / test | Rows | Tokens or gaps | Signs/tokens | Label bits | Top-1 | Top-5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Indus strict exact-collapsed masked signs | 1,798 | 8,212 | 571 | 4,410.970864 | 0.279591 | 0.534096 |
| Linear B Series D, IVC-length cap, clean bidirectional masking | 299 | 1,755 | 91 | 465.505030 | 0.435897 | 0.698006 |
| Linear B Series D, IVC-length cap, source-gapped sequence leave-out | 299 | 299 | 91 | 465.505030 | 0.294314 | 0.638796 |
| SumTablets, glyph-only IVC-length-capped admin lines | 1,798 | 8,716 | 358 | 2,526.289215 | 0.171753 | 0.373681 |

The useful comparison is not “Indus is Linear B” or “Indus is cuneiform.” It is narrower: the Indus masked top-1 score is in the same neighborhood as a known readable script under a source-provided gapped heldout task at Indus-like row lengths, but it remains below clean Linear B bidirectional masking and carries almost ten times the unanchored label-symmetry burden. Linear B has 91 signs/tokens in the IVC-length-capped view; the Indus run has 571 observed signs. SumTablets adds a second known-script calibration point: a known readable administrative corpus, stripped to glyphs and line-capped, scores below Indus in this exact instrument while still beating its own shuffled controls. Comparator choice therefore matters, and internal predictability still is not a reading.

## Language Priors

Dravidian, Indo-Aryan/Sanskritic, Elamite-adjacent, and unknown-language priors were not run as accepted phonetic priors because no frozen primary lexicon and no external sign-to-value anchor were available in the local artifact set. Running lexical priors without an anchor would only relabel internally equivalent assignments.

The mechanism that can break this limit is external:

- a Meluhha cuneiform name/title/toponym matched to an Indus sign sequence,
- a source-normalized morphological descent line to a known-valued script,
- a controlled semantic association strong enough to pin a sign or class externally,
- or another independently dated bilingual or quasi-bilingual anchor.

## Skeptic Record

This section is the honest scorecard: every attack the result has survived, and every attack it has failed or not yet faced.

Survived:

- Exact-sequence dedup before the main curve.
- Leave-one-row-out masking, so the tested row does not train on itself.
- Six forger controls, including edge-frame and register-blocked controls, for masked top-1 accuracy at 100 iterations per control.
- Structured administrative, emblem, and mixed admin/emblem controls rerun on the current corpus; these break broad bidirectional predictability as language evidence.
- Real-world nonlinguistic and ambiguous-system comparators added; this breaks masked top-1 predictability as language evidence because Pictish stones and barn stars exceed the Indus reference.
- Directionality comparator added; harsh top-edge-removed plus one-edit-family-collapsed Indus stored-order wins exceed all current real-world nonlinguistic and ambiguous comparators, while remaining below known-script controls.
- Directionality skeptic controls added; source-visible `861` terminal/tail and matched Lipi/Mayig overlap support lanes fail, so they are retracted as support for the broad directionality candidate.
- Directionality block controls added; harsh directionality survives `site|type|symbol` holdout but not full leave-site-out.
- Directionality site-balance control added; Mohenjo-daro plus Harappa balancing survives, while Lothal-plus and top-five-site balancing do not.
- Directionality site profiles added; Mohenjo-daro and Harappa each survive within-site nulls, while Lothal is null-compatible.
- Directionality policy controls added; `R/L`-only rows preserve the signal and random row orientation flips destroy it, but physical source direction remains unvalidated.
- Directionality influence controls added; no single row carries the signal, while the largest coarse `site|type|symbol` family effect is `Mohenjo-daro|SEAL:R|None` at 0.028975 stored-win share.
- Directionality formula-family controls added; harsh leave-source-convention-out scoring using `site|type|material|symbol|cult|direction` survives at stored-win share 0.832877 with max admissible null >= observed share 0.020000, and harsh source-convention collapse survives at 0.805714 with max admissible null >= observed share 0.005000.
- Route-conditioned directionality control added; public-route visibility fails as a source-normalized support lane because the 38 routed rows score 0.684211, page/source-register collapses fall below 0.70, and matched route-label nulls reproduce the route share with null >= observed share 1.
- Source-validation queue added; it ranks the 324 major-site harsh rows by directionality pressure and found that M-70, the first immediate route target, failed matched-negative blind token-box promotion with maximum yes-only FPR 0.714286 and maximum conservative FPR 0.777778. A later public-route probe over the 79 high-pressure source-validation targets found 38 plate-route candidates; manual visual triage moved H-654, M-1310, M-1320, and M-811 into no-overlay blind packets. v1 failed with maximum yes-only FPR 0.333333, maximum conservative FPR 0.666667, a leaked negative label, hard scoring-negative false positives, and unstable target counts. v2b fixed the 12-real-negative and duplicate-hash design defects but failed because real denominator rows leaked labels, reviewer C had conservative target-like uncertainty on 2/12 real negatives, and target counts were unstable. This is acquisition and failure-discovery progress only, not an accepted source-normalized reading.

Not survived or not yet tested:

- Source-family and near-duplicate collapse beyond exact token strings.
- Source-image direction validation. The queue identifies where to start, but it does not perform the source-image read.
- M-70 source-box promotion. The first blind packet has been reviewed and fails: one target view was only uncertain for one reviewer, and both reviewers called multiple scoring negatives target-like.
- H-654/M-1310/M-1320/M-811 source-box promotion. The v1 no-overlay packet has been reviewed and fails: real scoring negatives are below the forger denominator floor, `D006/M-525` leaks a printed side annotation, hard scoring-negative false positives appear, and most target views are overcounted or uncertain. The stricter v2b packet also fails despite 12 real negatives and zero duplicate hashes, because real denominator rows leak labels and target counts remain unstable.
- Physical source-family, workshop-copy, mold/impression, and publication-lineage collapse. The metadata-only source-convention proxy survives, but it is not the same as physical source normalization.
- A bidirectional or physical-direction version of the directionality claim. Exact `L/R` is null-compatible and harsh `L/R` fails under current controls.
- Known-script scarcity controls beyond the current Linear B Series D plus SumTablets sample.
- A discriminator that separates Indus masked predictability from high-predictability nonlinguistic/ambiguous symbol systems.
- Source-normalized confirmation that the directionality signal is not a Lipi metadata artifact.
- Crosswalk-blind heldout rebuilding of any Lipi/Mayig overlap result.
- Site-balanced or source-image-normalized directionality rerun, because full leave-site-out is not clean in harsh scopes.
- Stronger multisite directionality evidence, because current minor-site balanced samples collapse to null-compatible scores.
- Source-normalized site profiles, because current per-site results are still Lipi T3 metadata-layer evidence.
- Source-image direction validation, because recorded `R/L` is an inherited corpus field and too imbalanced to prove physical direction.
- Any language-family likelihood claim.

## Claim Status

No accepted claim count changes. The result enters the ledger as a live structural candidate:

> Internal constraints measurably reduce local continuation ambiguity in the exact-sequence-collapsed strict Lipi working corpus, but the corpus remains far from phonetic unicity because unanchored value assignments retain at least 4,410.970864 bits of global label symmetry.

This is useful because it gives future anchors a quantitative place to attach. It is also useful because it rejects a bad shortcut: context predictability is not decipherment.

## Artifacts

- `data/open_prototype/tools/effective_unicity_degeneracy.mjs`
- `data/open_prototype/reports/effective_unicity_degeneracy_curve.csv`
- `data/open_prototype/reports/effective_unicity_degeneracy_null_iterations.csv`
- `data/open_prototype/reports/effective_unicity_degeneracy_null_summary.csv`
- `data/open_prototype/reports/effective_unicity_degeneracy_summary.json`
- `data/open_prototype/tools/effective_unicity_known_script_comparator.mjs`
- `data/open_prototype/reports/effective_unicity_known_script_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_known_script_comparator.csv`
- `data/open_prototype/tools/effective_unicity_sumtablets_comparator.mjs`
- `data/open_prototype/reports/effective_unicity_sumtablets_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_sumtablets_comparator.csv`
- `data/open_prototype/tools/effective_unicity_nonlinguistic_comparator.mjs`
- `data/open_prototype/reports/effective_unicity_nonlinguistic_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_nonlinguistic_comparator.csv`
- `data/open_prototype/tools/effective_unicity_realworld_nonlinguistic_comparator.mjs`
- `data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_comparator.csv`
- `data/open_prototype/tools/effective_unicity_directionality_comparator.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_comparator.csv`
- `data/open_prototype/reports/linear_b_series_d_scarcity_summary.json`
- `data/open_prototype/reports/linear_b_series_d_gapped_heldout_summary.json`
