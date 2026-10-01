# Findings Dossier

Date: 2026-05-30

This dossier is the project's ledger: what has actually been established, what is still live, and what was tried and killed. The vocabulary is strict. "Accepted" means a claim survived every adversarial test built against it. A "candidate" is live but unproven. "Retracted" means a claim was made and then withdrawn when a test broke it. A "forger" is a null model — a procedure that tries to fake the observed pattern by chance — and FPR is its false-positive rate, how often the fake succeeds. When rows are "collapsed" or "deduped," duplicate copies of one inscription count once.

## Accepted Claims

Current ledger counts:

| Class | Accepted |
| --- | ---: |
| translations | 0 |
| phonetic_values | 0 |
| sign_meanings | 0 |
| language_identification | 0 |
| structural_findings | 1 |
| external_anchors | 0 |

### Accepted: `002-861-533-717` Restricted Terminal Tail

Claim ID: `accepted_struct_002_861_533_717_restricted_tail_2026_05_29`

Claim: within the fixed `002-861` branch question, `533-717` is the only tested unit of length 1 to 3 with support >= 2 whose every occurrence in strict local rows is a terminal tail — a unit that ends the inscription — after `002-861`. The two witnesses are `M-376` and `M-391`. Both are source-visible as same-line terminal-side material, and source-family review rejects exact copy-family collapse: they are not two prints of one object.

Core evidence:

- `data/open_prototype/reports/campaign_032_002_861_restricted_tail_forger_summary.json`: in 4,135 strict raw rows and 3,074 exact `text/site/type/symbol` dedup rows, `533-717` is the sole candidate. Worst recorded FPR is `0.006`; strict raw context-shuffle FPRs are `0.0002` global and `0.0010` within `site/type/symbol`.
- `data/open_prototype/reports/campaign_032_002_861_restricted_tail_forger_candidates.csv`: both scopes return only `unit_len=2`, `unit=533 717`, `total_occurrences=2`, `fixed_prefix_terminal_occurrences=2`.
- `data/open_prototype/reports/campaign_032_002_861_source_token_attachment_verdicts.csv`: `M-376` and `M-391` preserve source-visible same-line terminal-side candidate windows.
- `data/open_prototype/reports/campaign_032_002_861_533717_source_family_independence_summary.json`: exact copy-family collapse is rejected, while linguistic weighting remains one narrow source/register-family cell.
- `data/open_prototype/reports/campaign_032_002_861_533717_source_layout_discriminator_summary.json`: stronger layout wording is blocked because `M-1273` also has same-line terminal-side post-`861` material.

Skeptic boundary: the narrowness is the point. If any prefix is allowed, repeated terminal bigram cells are common: 96 in strict raw rows and 40 after exact dedup. So this is not a global formula-discovery claim. It is fixed to the prior `002-861` branch question, and it earns no exact source-normalized token boundary, sign value, sign meaning, phonetic value, language identification, external anchor, or translation.

## Live Candidate: `002-Y` Closure/Branch

Candidate ID: `candidate_struct_032_002_y_closure_branch_2026_05_29`

Claim: in the strict deduplicated all-`002` layer, the signs that follow `002` split into two poles: a high-terminal pole, where the inscription usually ends, and a continuation pole, where it usually goes on. The strict post-hoc partition support is `817/820` versus `390/368/031/220`. In the older fixed-bin description, `861` remains closure-heavy but leaky; it is not part of the strict best two-pole partition.

Scope: T3 Lipi metadata/sign layer, strict complete closed rows deduplicated by text, site, type, and `002` position. Not yet source-normalized corpus-wide.

Core evidence:

- `data/open_prototype/reports/campaign_032_002_post_y_summary.json`: 499 strict dedup all-`002` rows and 32 strict dedup adjacent `032-002` rows.
- `data/open_prototype/reports/campaign_032_002_y_matched_terminality_summary.json`: all-`002` `y_class` leave-one-out terminality accuracy/Brier/logloss = 0.885772 / 0.097554 / 0.331038; adjacent `032-002` = 0.906250 / 0.106698 / 0.381811.
- `data/open_prototype/reports/campaign_032_002_y_forger_null_summary.json`: 10,000 iterations per null model; all-`002` maximum recorded FPR across tested nulls and metrics = 0; adjacent `032-002` maximum recorded FPR = 0.0283.
- `data/open_prototype/reports/campaign_032_002_y_posthoc_partition_forger_summary.json`: 10,000 iterations per null model, with each null allowed to discover its own best high-terminal versus low-terminal partition. Broad all-`002` best split `817/820` versus `390/368/031/220` has z 13.211692, gap 0.954023, and worst FPR 0 for both z and gap. Adjacent `032-002` fails, with worst FPR 0.5205 for z and 0.7552 for gap.
- `data/open_prototype/reports/campaign_002_y_partition_source_queue_summary.json`: source-normalization acquisition queue for the same broad strict all-`002` partition. Closure signs `817/820` have four grade >= 2 source hooks; after corrected supplemental public CISI route acquisition, branch signs have 14 grade >= 2 route hooks: `390` has 2, `368` has 5, `031` has 4, and `220` has 3.
- `data/open_prototype/reports/campaign_002_y_branch_gap_public_source_summary.json`: supplemental public CISI route acquisition for branch-gap signs `368/031/220`; 29 target rows, 32 route rows, and 12 public CISI plate-route candidates. Accepted claim increment remains zero. The apparent `H-44` route was demoted as an OCR prefix/split-label trap from nearby `H-449`-style labels.
- `data/open_prototype/reports/campaign_002_y_branch_gap_blind_packet_summary.json`: first branch-gap blind source-box packet; 14 blind images, three primary targets, three backup targets, six scoring negatives, two quarantines, accepted claim increment zero.
- `data/open_prototype/reports/campaign_002_y_branch_gap_blind_review_summary.json`: three stage-1 blind reviews scored. The packet is not promotable because target and backup token counts are not stable; exact count matches are 2/14, 2/14, and 1/14 across reviewers. Hard branch notes on scoring negatives are 0/6 for all three reviewers, but this stage did not perform unblinded branch-relation scoring.
- `data/open_prototype/reports/campaign_m12_token_count_audit_summary.json`: follow-up audit for `BG001/M-12`. Lipi `2540.1` and Mayig `M-12A` both preserve 9-token witnesses; all three blind reviewers counted `BG001` as 10 uncertain visual units; same-packet scoring negative `BG009/M-654` gives a stable-overcount control at 1/6 scoring negatives. Accepted claim increment remains zero.
- `data/open_prototype/reports/campaign_032_002_y_skeptic_holdout_summary.json`: broad all-`002` result survives removal attacks and family-blocked prediction; exact right-edge matching is recorded as tautological, not counted as support.

Skeptic attacks survived:

- Exact duplicate collapse.
- Register-only baseline using `site/type/symbol`.
- Fixed-bin forger nulls preserving global and register-conditioned terminal/Y distributions.
- Post-hoc partition forger that searches the best split separately in every null corpus.
- Removal of Mohenjo-daro `SEAL:S`, Harappa, Mohenjo-daro, `SEAL:S`, and unnamed CISI rows in the broad all-`002` scope.
- Family-blocked `y_class` prediction in the broad all-`002` scope.

Unresolved attacks:

- The broad post-hoc partition now controls the main overfitting objection, but exact named-bin wording remains descriptive rather than independently discovered.
- Source-image/direction validation is incomplete.
- Adjacent `032-002` scope is too small after severe removals.
- Current source-normalized decisive rows mostly need source routes or better images.
- The new partition source queue no longer has a route-inventory gap for branch signs `368`, `031`, and `220`, but the first blind source-box packet failed stage-1 promotion because target and backup token counts are unstable. `BG001/M-12` is a useful diagnostic, but not a correction: Lipi and Mayig agree at 9 tokens, every `BG001` count was marked uncertain, and same-packet scoring negative `BG009/M-654` reproduces stable over-counting. A source-normalized proof still needs stable visual token boxing, physical side/direction checks, source-family/copy review, and matched-negative scoring.

Decision: live candidate, not accepted.

## Vector 2 Candidate: Effective Unicity / Internal Degeneracy

Candidate ID: `candidate_struct_effective_unicity_internal_degeneracy_2026_05_29`

Claim: the exact-sequence-collapsed strict Lipi working corpus has measurable local context constraint — nearby signs restrict which sign fits a slot. But unanchored phonetic assignments retain a very large label-symmetry lower bound: without an external anchor, any proposed set of sound values can be globally permuted into an equally good internal solution. This is structural evidence about solution-space degeneracy, not a reading.

Scope: T3 Lipi metadata/sign layer, `readiness_bucket = lipi_numeric_clean_candidate`, exact numeric token-sequence collapse. Not source-normalized; not near-duplicate/source-family collapsed.

Core evidence:

- `data/open_prototype/reports/effective_unicity_degeneracy_summary.json`: 2,883 strict rows; 1,798 exact-sequence families; 2,059 provenance-aware sequence families; 571 signs at full coverage.
- `data/open_prototype/reports/effective_unicity_degeneracy_curve.csv`: masked mean effective candidates fall from 44.286775 at 10% coverage to 12.891819 at full coverage.
- `data/open_prototype/reports/effective_unicity_degeneracy_null_summary.csv`: full-coverage masked top-1 observed value 0.279591; FPR 0 across global-token, row-internal, position-slot, edge-frame, register-blocked position, and template-admin controls at 100 iterations per control.
- `data/open_prototype/reports/effective_unicity_known_script_comparator_summary.json`: Linear B Series D known-script calibration; Indus masked top-1/top-5 = 0.279591 / 0.534096; Linear B IVC-length-capped clean bidirectional top-1/top-5 = 0.435897 / 0.698006; Linear B source-gapped sequence-leave-out top-1/top-5 = 0.294314 / 0.638796.
- `data/open_prototype/reports/effective_unicity_sumtablets_comparator_summary.json`: SumTablets glyph-only administrative-script calibration; 2,000 train rows fetched from Hugging Face dataset `colesimmons/SumTablets` at SHA `11638cd142afbed716df43c55d8810d47fb9b52c`; transliteration and glyph names hidden; selected 1,798 exact line sequences with 8,716 glyph tokens and 358 unique glyphs; masked top-1/top-5 = 0.171753 / 0.373681; max null >= observed share 0 across five matched controls.
- `data/open_prototype/reports/effective_unicity_nonlinguistic_comparator_summary.json`: structured nonlinguistic rerun; masked top-1 survives the effective-unicity forger gate with max FPR 0, but broad bidirectional top-1 is broken by administrative, emblem, and mixed admin/emblem nulls with null >= observed share 1.
- `data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_comparator_summary.json`: real-world nonlinguistic and ambiguous-system comparator from the Sproat 2014 XML corpus bundle; Pictish stones top-1/top-5 = 0.450292 / 0.614035 and barn stars / hex signs = 0.367123 / 0.673973, both above the Indus masked top-1 reference.
- `data/open_prototype/reports/effective_unicity_directionality_comparator_summary.json`: stored-order versus reversed-order comparator; harsh top-10-edge-removed plus one-edit-family-collapsed Indus stored-win share = 0.841096 with max null >= observed share 0, above current real-world nonlinguistic and ambiguous comparators and below known-script controls. Mayig P exact-collapsed pressure gives 0.943750 and harsh Mayig drops to 0.666667 over 24 rows.
- `data/open_prototype/reports/effective_unicity_directionality_skeptic_controls_summary.json`: hostile support-lane controls. The source-visible `861` terminal/tail probe scores 1.000000 but has max null >= observed share 1. Matched Lipi/Mayig overlap exact scores are 0.937500 and 0.929134, but after top-10 edge removal they collapse to Lipi 0.363636 and Mayig 0.473684, each with max null >= observed share 1.
- `data/open_prototype/reports/effective_unicity_directionality_block_controls_summary.json`: hostile block-holdout controls. In the harsh one-edit collapsed scope, `site|type|symbol` holdout gives stored-win share 0.827397 with max null >= observed share 0, while full leave-site-out gives 0.753425 with max null >= observed share 0.100000. In the register-edge-family collapsed scope, `site|type|symbol` holdout gives 0.835227 with max null >= observed share 0.005000, while full leave-site-out gives 0.774621 with max null >= observed share 0.265000.
- `data/open_prototype/reports/effective_unicity_directionality_site_balance_summary.json`: site-balanced resampling control. Mohenjo-daro plus Harappa balanced samples have observed median stored-win share 0.803571 and max paired null >= observed share 0.003 over 1,000 iterations; adding Lothal gives median 0.541667 and max paired null >= observed share 0.528; top-five-site balancing gives median 0.433333 and max paired null >= observed share 0.616.
- `data/open_prototype/reports/effective_unicity_directionality_site_profiles_summary.json`: within-site directionality profile. Mohenjo-daro has stored-win share 0.816038 with max null >= observed share 0.002, Harappa has 0.741071 with max null >= observed share 0.004, and Lothal has 0.312500 with max null >= observed share 0.988.
- `data/open_prototype/reports/effective_unicity_directionality_policy_controls_summary.json`: recorded-direction policy control. The harsh scope has 354 recorded `R/L` rows and 11 recorded `L/R` rows. `R/L`-only scoring gives stored-win share 0.838983; Mohenjo-daro `R/L` gives 0.813397; Harappa `R/L` gives 0.769231. Random row-orientation flips destroy the signal, with all-harsh null mean 0.471134 and null p95 0.526027.
- `data/open_prototype/reports/effective_unicity_directionality_influence_controls_summary.json`: influence/concentration control. No single supportive row carries the signal: largest supportive row delta is 0.005931, and the largest absolute row effect is adverse, L-115 at 0.010552. Coarse `site|type|symbol` families matter more, with `Mohenjo-daro|SEAL:R|None` the largest supportive family at 0.028975.
- `data/open_prototype/reports/effective_unicity_directionality_formula_family_controls_summary.json`: stronger metadata source/formula-family control using `site|type|material|symbol|cult|direction`. Harsh leave-source-convention-out scoring gives stored-win share 0.832877 with max admissible null >= observed share 0.020000; harsh source-convention collapse gives 175 rows, stored-win share 0.805714, and max admissible null >= observed share 0.005000. Harsh `L/R` fails with 11 rows, stored-win share 0, and max null >= observed share 1.
- `data/open_prototype/reports/effective_unicity_directionality_source_queue_summary.json`: source-validation acquisition queue. In the 324-row major-site harsh scope, pooled stored-win share is 0.845679; 223 rows need a public route or source request, 94 have only non-source-grade catalogue hints, and only five initially have public-route or crop-review hooks for immediate direction work.
- `data/open_prototype/reports/effective_unicity_directionality_public_route_probe_summary.json`: public CISI OCR route probe for 79 top high-pressure source-queue rows; 93 route rows, 38 public plate-route candidates, one data/register-only route, 40 not found, and accepted claim increment 0.
- `data/open_prototype/reports/effective_unicity_directionality_route_conditioned_control_summary.json`: route-conditioned support gate. In the frozen top-79 public-route probe universe, the 38 public CISI plate-route rows score stored-win share 0.684211; page collapse gives 0.625000, `site|type|symbol|direction` collapse gives 0.619048, `site|type|material|symbol|direction` collapse gives 0.652174, and matched route-label nulls reproduce or exceed the observed route share with null >= observed share 1. Accepted claim increment 0.
- `data/open_prototype/reports/effective_unicity_directionality_route_visual_triage_summary.json`: manual visual triage of nine top route hits; four attempted no-overlay target crops (`H-654`, `M-1310`, `M-1320`, `M-811`) and accepted claim increment 0.
- `data/open_prototype/reports/effective_unicity_directionality_m70_source_pilot.csv`: first queue-row source pilot. M-70 is visually checked as a row-level source-visible public CISI face/impression pair with a broad order-window continuation candidate; no token identity or direction claim is accepted.
- `data/open_prototype/reports/effective_unicity_m70_blind_token_box_packet_summary.json`: matched-negative blind packet for the M-70 source pilot. It has 15 blind items, nine scoring-negative images across seven unique CISI controls, and zero accepted-claim increment.
- `data/open_prototype/reports/effective_unicity_m70_blind_token_box_review_summary.json`: scorer output for the same packet. Two independent blind reviews scored the packet; max yes-only false-positive rate is 0.714286, max conservative false-positive-or-uncertain rate is 0.777778, and the promotion gate decision is `failed_packet_gate_no_promotion`.
- `docs/effective_unicity_methods_note.md`: standalone methods note.

Skeptic attacks survived:

- Exact sequence collapse before measuring the main curve.
- Leave-one-row-out masked scoring.
- Six forger controls for masked top-1 accuracy.
- Known-script scarcity calibration against Linear B Series D with verified source MD5.
- Known-script administrative calibration against SumTablets with Dataset Viewer provenance, pinned dataset SHA, hidden transliteration/name fields, exact line collapse, and matched controls.
- Structured administrative/emblem comparators rerun on the current corpus; broad bidirectional predictability was rejected as language or semantic evidence.
- Real-world nonlinguistic and ambiguous-system comparators added; masked top-1 predictability was rejected as language evidence because Pictish and barn-star corpora exceed the Indus reference.
- Directionality comparator added; harsh Indus stored-order wins exceed all current real-world nonlinguistic and ambiguous comparators, while remaining below known-script controls. Exact-collapsed Mayig P records show a similar order signal, but the harsh Mayig pressure test is too small.
- Directionality skeptic controls added; source-visible `861` and matched Lipi/Mayig overlap support lanes fail and are retracted as support.
- Directionality block controls added; harsh directionality survives `site|type|symbol` holdout but not full leave-site-out.
- Directionality site-balance control added; Mohenjo-daro plus Harappa balanced samples survive, while Lothal-inclusive and top-five-site balanced samples do not.
- Directionality site profiles added; Mohenjo-daro and Harappa each survive within-site controls, while Lothal is null-compatible in the current harsh scope.
- Directionality policy controls added; `R/L`-only rows preserve the major signal and random row-orientation flips destroy it.
- Directionality influence controls added; no single row carries the harsh signal, while coarse register-family concentration remains visible enough to require source-family review.
- Directionality formula-family controls added; the signal survives metadata source-convention holdout and collapse, but only as an R/L-dominant metadata-layer result.
- Directionality route-conditioned control added; public CISI route availability fails as support because route-visible rows weaken under page/source-convention collapse and matched route-label nulls reproduce the apparent route subset signal.

Unresolved attacks:

- Source-image/direction normalization is incomplete. The public route probe identified four attempted target crops, but the first no-overlay blind packet failed: seven packaged unique scoring negatives fell to six effective scorable controls after `D006/M-525` leaked a printed side annotation; yes-only denominators were only 3 and 4 by reviewer; hard scoring-negative false positives appeared; and target token counts were mostly overcounted or uncertain.
- Exact-sequence collapse does not remove physical near-duplicate source families, workshop/mold/impression families, or publication-lineage families. The metadata source-convention proxy narrows this attack but cannot replace source-image lineage.
- Known-script scarcity coverage is still narrow: Linear B Series D and SumTablets are integrated, but broader known-script comparator batteries remain incomplete.
- No accepted discriminator yet separates Indus local predictability from high-predictability real-world nonlinguistic or ambiguous systems.
- No source-normalized confirmation yet shows that the directionality signal survives outside the Lipi T3 metadata layer; the first M-70 source-box packet failed promotion under matched negatives.
- Matched Lipi/Mayig overlap failed under top-edge removal and block-conditioned controls; any future overlap claim needs crosswalk-blind heldout rebuilding.
- Full leave-site-out is not clean in harsh directionality scopes, so the current directionality candidate cannot be phrased as site-generalized.
- Minor-site balanced resampling is null-compatible, so the current directionality candidate cannot be phrased as pan-Indus.
- Lothal's current harsh subset is null-compatible and small; this does not prove Lothal lacks directionality in a source-normalized or broader corpus.
- Recorded direction is too imbalanced and inherited from metadata, so this still does not validate physical source-image direction.
- The L/R stratum does not support the directionality candidate under harsh controls; exact L/R is null-compatible and harsh L/R fails outright. Any current directionality wording must stay R/L-dominant.
- Current source queue and public route probe are acquisition instruments only. They identify high-pressure rows such as M-70 and four attempted visual target crops (`H-654`, `M-1310`, `M-1320`, `M-811`) but do not validate physical direction, sign order, or source-normalized transcription.
- Public-route visibility cannot be used to promote the directionality candidate: route-conditioned rows do not clear source-normalized collapse thresholds, and route-label shuffles reproduce or exceed the route subset score.
- Influence controls use coarse `site|type|symbol` families, not physical workshop, mold, seal/impression, or source-publication families.
- No external anchor exists in this Vector 2 run; language-family likelihood remains unearned.

Decision: live candidate, not accepted. It is useful as a degeneracy instrument and as a negative result against internal-only language identification.

## Failed Source-Gated Candidate: M-70 Source-Boxed Order Window

Retracted ID: `retracted_m70_source_boxed_order_window_promotion_2026_05_29`

Retracted claim: the first M-70 source pilot can be promoted from row-level source-visible broad order-window candidate to source-boxed order-window candidate using the current blind token-box packet — a set of images, targets mixed with matched negative controls, that reviewers score without seeing the answer key.

Scope: M-70 public CISI India face/impression pair plus matched-negative controls drawn from comparable source and metadata neighborhoods.

Evidence produced before retraction:

- `docs/effective_unicity_directionality_m70_source_pilot.md`: row-level source-visible source pilot.
- `docs/effective_unicity_m70_blind_token_box_packet.md`: promotion gate and blind-packet protocol.
- `data/open_prototype/reports/effective_unicity_m70_blind_token_box_answer_key.csv`: 15-item answer key.
- `data/open_prototype/reports/effective_unicity_m70_blind_reviews/avicenna_review.csv`: independent blind review A.
- `data/open_prototype/reports/effective_unicity_m70_blind_reviews/ohm_review.csv`: independent blind review B.
- `data/open_prototype/reports/effective_unicity_m70_blind_token_box_review_summary.json`: scored review summary.

Forger/null status:

- Reviewer `avicenna_review`: target yes 2/2; scoring-negative yes 5, no 2, uncertain 2; yes-only FPR 0.714286; conservative FPR 0.777778.
- Reviewer `ohm_review`: target yes 1/2 and uncertain 1/2; scoring-negative yes 5, no 4, uncertain 0; yes-only FPR 0.555556; conservative FPR 0.555556.
- Gate decision: `failed_packet_gate_no_promotion`.

Skeptic attacks that broke the claim:

- Not all M-70 target views were strictly recovered; reviewer `ohm_review` marked the face target uncertain.
- Both reviewers made hard target-like calls on scoring negatives.
- False-positive rates are far above the zero-hard-hit threshold set before review.

Decision: failed promotion after forger/skeptic scoring. M-70 remains row-level source-visible with a broad order-window continuation candidate; it does not support a source-boxed token order, physical direction, sign identity, meaning, phonetic value, language family, or translation.

## Failed Source-Gated Candidate: Directionality No-Overlay Source Packet

Retracted ID: `retracted_directionality_no_overlay_source_normalized_packet_2026_05_29`

Retracted claim: the no-overlay blind packet for `H-654`, `M-1310`, `M-1320`, and `M-811` promotes those route candidates from acquisition inventory to source-normalized crop/token-order candidates.

Scope: seven target images from four public CISI route-probe candidates, seven scoring-negative images across seven unique CISI controls, and one quarantine negative.

Evidence produced before retraction:

- `docs/effective_unicity_directionality_blind_packet.md`: packet protocol and failure analysis.
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_answer_key.csv`: 15-item answer key.
- `data/open_prototype/reports/effective_unicity_directionality_blind_reviews/blind_review_a.csv`: independent blind review A.
- `data/open_prototype/reports/effective_unicity_directionality_blind_reviews/blind_review_b.csv`: independent blind review B.
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_scored_rows.csv`: scored review rows.
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_review_summary.json`: scored review summary.

Forger/null status:

- Packet denominator: seven packaged unique real scoring negatives, below the forger floor of ten and below the planned target of twelve; after `D006/M-525` leaked a printed side annotation, only six unique real controls were effectively scorable.
- Reviewer `blind_review_a`: target pass 0, target fail 7, true negatives 2, hard false positives 1, uncertain negative hits 3, label-leak negatives excluded 1, yes-only FPR 0.333333, conservative FPR 0.666667.
- Reviewer `blind_review_b`: target pass 1, target fail 4, target uncertain 2, true negatives 3, hard false positives 1, uncertain negative hits 2, label-leak negatives excluded 1, yes-only FPR 0.250000, conservative FPR 0.500000.
- Gate decision: `failed_packet_gate_no_promotion`.

Skeptic attacks that broke the claim:

- `D006/M-525` leaked a printed side annotation and was excluded from the negative denominator.
- Scoring negatives produced hard count-boxable false positives: `D015/M-381` for reviewer A and `D009/H-665` for reviewer B.
- Target views were not cleanly recovered; `M-811`, `M-1320`, and `H-654` were overcounted by at least one reviewer, and `M-1310` was uncertain for reviewer B.
- The packet never tested physical source direction or source side; it only tested crop boxability and token-count recovery.

Decision: failed promotion after forger/skeptic scoring. The four objects remain acquisition and crop-QA targets only; they do not support source-normalized token order, physical direction, sign identity, meaning, phonetic value, language family, translation, or an accepted structural claim.

## Failed Source-Gated Candidate: Directionality No-Overlay Packet v2b

Retracted ID: `retracted_directionality_no_overlay_v2b_source_normalized_packet_2026_05_29`

Retracted claim: the v2b label-masked no-overlay packet for `H-654`, `M-1310`, `M-1320`, and `M-811` promotes those route-probe targets to source-normalized crop/token-order candidates.

Scope: four unique target images, 12 real routed scoring-negative images, three external stress controls, and four auxiliary synthetic controls. Synthetic controls never count toward the real-negative denominator.

Evidence produced before retraction:

- `docs/effective_unicity_directionality_blind_packet_v2b.md`: packet protocol and failure analysis.
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_summary.json`: 23-item packet summary.
- `data/open_prototype/reports/effective_unicity_directionality_blind_v2b_reviews/reviewer_a.csv`: independent blind review A.
- `data/open_prototype/reports/effective_unicity_directionality_blind_v2b_reviews/reviewer_b.csv`: independent blind review B.
- `data/open_prototype/reports/effective_unicity_directionality_blind_v2b_reviews/reviewer_c.csv`: independent blind review C.
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_scored_rows.csv`: scored review rows.
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_review_summary.json`: scored review summary.

Forger/null status:

- Reviewer `reviewer_a`: target pass 1, target fail 3, real true negatives 7, hard false positives 0, uncertain real-negative hits 0, real label leaks 5, yes-only FPR 0, conservative FPR 0.
- Reviewer `reviewer_b`: target pass 1, target fail 2, target uncertain 1, real true negatives 7, hard false positives 0, uncertain real-negative hits 0, real label leaks 5, yes-only FPR 0, conservative FPR 0.
- Reviewer `reviewer_c`: target pass 0, target fail 2, target uncertain 2, real true negatives 6, hard false positives 0, uncertain real-negative hits 2, real label leaks 4, yes-only FPR 0, conservative FPR 0.166667.
- Gate decision: `failed_packet_gate_no_promotion`.

Skeptic attacks that broke the claim:

- Real denominator label leakage broke the fixed-denominator policy: `H-665`, `H-158`, `M-527`, `M-1315`, and `M-171` were flagged by reviewers A and B; reviewer C flagged four of those five.
- Reviewer C produced conservative target-like uncertainty on `M-525` and `M-365`.
- Target counts varied for `M-1320` (`8/8/7`), `M-1310` (`7/7/6`), and `M-811` (`5/6/6`).
- The packet still did not test physical source direction or source side.

Decision: failed promotion after forger/skeptic scoring. v2b is useful as a stricter packet generator and as evidence that OCR word-box masking of route-context crops does not reliably remove neighboring catalogue labels. It does not support source-normalized token order, physical direction, sign identity, meaning, phonetic value, language family, translation, or an accepted structural claim.

## Failed Preflight Candidate: Directionality No-Overlay Packet v2c

Retracted ID: `retracted_directionality_no_overlay_v2c_preflight_packet_2026_05_29`

Retracted claim: the v2c OCR-coordinate-fix no-overlay packet repairs the v2b label-leak failure enough to proceed to blind source-normalization review for `H-654`, `M-1310`, `M-1320`, and `M-811`.

Scope: four unique target images, 12 real routed scoring-negative images, three external stress controls, and four auxiliary synthetic controls rebuilt from the corrected public-route probe.

Evidence produced before retraction:

- `data/open_prototype/reports/effective_unicity_directionality_public_route_probe_v2_summary.json`: corrected public-route probe preserving the 79-row / 38-plate-route acquisition counts while fixing the DjVu five-coordinate OCR parser.
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2c_summary.json`: 23-item v2c packet summary; zero duplicate blind image hash groups; status `v2c_packet_created_failed_visual_preflight_no_claim_promotion`.
- `docs/effective_unicity_directionality_visual_preflight_failures.md`: canonical visual-preflight failure note naming the v2c catalogue labels, v2d denominator failure, crop-world asymmetry, and page-layout cues.
- `data/open_prototype/reports/effective_unicity_directionality_visual_preflight_failures.csv`: row-level failure ledger for v2c/v2d/v2e visual preflight.
- `docs/effective_unicity_directionality_panel_crop_repair.md`: follow-up repair note and object-panel crop inventory.
- `data/open_prototype/tools/effective_unicity_directionality_panel_crop_shortlist_v2d.py`: reproducible cleaned-shortlist emitter.
- `data/open_prototype/reports/effective_unicity_directionality_panel_crop_repair_v2d_manual_shortlist_clean_draft.csv`: cleaned v2d visual shortlist draft; unreviewed and not a packet.
- `data/open_prototype/reports/effective_unicity_directionality_signband_pool_v2e_summary.json`: widened signband-like crop pool; unreviewed and not a packet.

Forger/null status:

- No reviewer FPR is reported because the packet failed before blind review.
- Fixed real-negative denominator intended: 12 rows.
- Gate decision: `failed_visual_preflight_no_review`.
- Failure modes: page-context label leakage, crop-world asymmetry, OCR masking as a class cue, and not reviewer-ready.

Skeptic attacks that broke the claim:

- Human visual preflight found remaining catalogue/page labels and neighboring object cues.
- Targets remained tight recuts while real negatives were broader OCR-masked route-context crops.
- The parser fix removed bogus tall OCR boxes but did not create true object-panel segmentation.
- Any v2d reserve replacement must be pre-registered before scoring; no after-review denominator repair is allowed.

Decision: failed before review. v2c is useful as a parser-fix and failure record only. The panel-crop repair inventory and cleaned v2d shortlist are acquisition infrastructure, not source-normalized evidence.

## Failed Preflight Candidate: Directionality Panel-Crop v2d Packet Readiness

Retracted ID: `retracted_directionality_panel_crop_v2d_packet_readiness_2026_05_29`

Retracted claim: the cleaned v2d panel-crop shortlist is ready to become a blind directionality source-normalization packet.

Evidence produced before retraction:

- `data/open_prototype/reports/effective_unicity_directionality_panel_crop_repair_v2d_manual_shortlist_clean_draft.csv`: cleaned 16-row visual shortlist draft.
- `tmp/effective_unicity_directionality_panel_crop_repair/visual_qc_manual_shortlist_v2d_clean_draft.jpg`: visual QC contact sheet.
- `docs/effective_unicity_directionality_visual_preflight_failures.md`: canonical visual-preflight failure note.
- `data/open_prototype/reports/effective_unicity_directionality_signband_pool_v2e_summary.json`: widened v2e candidate-pool summary.

Forger/null status:

- No reviewer FPR is reported because the shortlist failed before blind review.
- Fixed real-negative denominator in the cleaned shortlist: 9.
- Reserve rows not yet denominator rows: `H-421`, `M-127`, `M-1322`.
- Gate decision: `failed_preflight_no_review`.

Skeptic attacks that broke the claim:

- The denominator is not 12 until reserves are promoted in a new pre-registered manifest.
- Crop worlds are mixed: targets mostly signband strips; controls include tablet/object panels and animal/icon contexts.
- Page-layout slivers remain visible in rows such as `H-654`, `M-1310`, `M-386`, and `M-1322`.
- Shared source pages create layout leakage risk: `M-1310`/`M-1315` on `n202`, and `M-1320`/`M-1322` on `n203`.

Decision: failed before review. v2d is a crop-QA draft only. v2e widens the next candidate pool but does not produce a packet or FPR.

## Failed Preflight Candidate: Directionality Homogeneous Signband v2f Packet Readiness

Retracted ID: `retracted_directionality_homogeneous_signband_v2f_packet_readiness_2026_05_29`

Retracted claim: the v2e signband-like pool can be promoted into a homogeneous no-overlay v2f blind packet for `H-654`, `M-1310`, `M-1320`, and `M-811` with 12 fixed real-negative controls.

Evidence produced before retraction:

- `data/open_prototype/tools/effective_unicity_directionality_homogeneous_packet_v2f_preflight.py`: mechanical v2f gate script.
- `data/open_prototype/reports/effective_unicity_directionality_homogeneous_packet_v2f_preflight_summary.json`: failed gate summary.
- `data/open_prototype/reports/effective_unicity_directionality_homogeneous_packet_v2f_strict_reuse_candidates.csv`: strict compact signband-strip reuse candidates.
- `data/open_prototype/reports/effective_unicity_directionality_homogeneous_packet_v2f_derived_top_strip_candidates.csv`: derived top-strip acquisition candidates.
- `docs/effective_unicity_directionality_homogeneous_packet_v2f_preflight.md`: human-readable gate note and future forger requirements.

Forger/null status:

- No reviewer FPR is reported because no blind packet was promoted.
- Strict reuse lane: 82 candidate rows, compact targets `H-654`, `M-1310`, and `M-1320`, missing target `M-811`, seven original fixed real-negative CISIs, and three target/control source-page collisions.
- Derived top-strip lane: 44 candidate rows, targets `H-654` and `M-1310` only before visual review, missing `M-1320` and `M-811`, six original fixed real-negative CISIs, and one target/control source-page collision.
- Required future forger apparatus is now explicit: 12 fixed real signband-negative CISIs, 12 source-real nonlinguistic nulls, 32 fixed-seed synthetic nulls, auxiliary sentinels only, and zero hard or uncertain target-like/directional calls on denominator rows.

Skeptic attacks that broke the claim:

- `M-811` is not available as a compact target signband in v2e; its candidates are tall bull/object-panel crops.
- The original fixed real-negative denominator cannot reach 12 without duplicate rows, reserve rows, or newly introduced controls.
- `M-1310` shares page `n202` with `M-1315` and `M-1314`; `M-1320` shares `n203` with `M-1322`.
- Within-CISI duplicate rows are common in v2e, and near-duplicate grouping is not certified.
- The control pool mixes crop regimes and object contexts.

Decision: failed before review. v2f is crop acquisition and gate-failure evidence only; it does not support source-normalized token order, physical direction, sign identity, meaning, phonetic value, language family, translation, or an accepted structural claim.

## Failed Source-Gated Candidate: `032-002-Y` Source-Visible Packet

Retracted ID: `retracted_source_visible_032_002_y_packet_2026_05_29`

Retracted claim: current source-visible row-level evidence supports `032-002-Y` as a real same-signband packet across target `240-220-032`, non-240 `A-220-032`, and outside-`A-220` contexts, weakening the objection that the packet is only a catalog adjacency artifact.

Scope: source-visible subset of the 25-row `032-002-Y` route manifest. Row-level visibility and provisional token boxes only.

Evidence produced before retraction:

- `data/open_prototype/reports/source_visible_032_002_y_summary.json`: eight source-visible same-line rows; contexts cover target, non-240, and outside lanes; Y values cover `300`, `817`, `820`, and `861`; sites cover Chanhu-daro, Harappa, and Mohenjo-daro.
- `data/open_prototype/reports/source_visible_032_002_y_witness_matrix.csv`: consolidated 25-row route/source/token-box matrix.
- `docs/source_visible_032_002_y_witness_matrix.md`: source-gate note with allowed and forbidden wording.
- `data/open_prototype/reports/source_box_negative_control_summary.json`: 827 negative candidate positions found outside the 25-row route list; 23 local image-backed negative positions; blind packet v1 has 8 positives and 12 image-backed negatives.
- `docs/source_box_negative_control_manifest.md`: matched-negative control note.
- `data/open_prototype/reports/source_box_blind_adjudication_summary.json`: two blind reviews scored against the key.
- `docs/source_box_blind_adjudication_results.md`: retraction note and failure analysis.

Forger/null status:

- Exploratory coverage null only: 10,000 random 8-row subsets from the 25-row route manifest.
- Random-subset rates: all three categories = 0.8590; at least four Y values = 0.2724; at least three sites = 0.6342; target plus non-240 `817` = 0.2125; outside `861` at three sites = 0.0245.
- This is not accepted as a claim-specific false-positive rate because acquisition was target-driven.
- Matched-negative source-box adjudication failed. Reviewer 1: TP 0, FP 4, TN 6, FN 5, uncertain-positive 3, uncertain-negative 2, yes-only FPR 0.400000, conservative negative-failure rate 0.500000, yes-only sensitivity 0. Reviewer 2: TP 0, FP 3, TN 7, FN 6, uncertain-positive 2, uncertain-negative 2, yes-only FPR 0.300000, conservative negative-failure rate 0.416667, yes-only sensitivity 0.

Skeptic attacks that broke the claim:

- Blind reviewers recovered zero positives as confident positives.
- Blind reviewers called three to four negative controls positive.
- Both reviewers called `M-32` and `M-17` false positives.
- The packet also lacked local image-backed `negative_220_032_next_not_002` controls, so even the failed test did not fully stress the `A-220-032` lane.

Decision: retracted after forger failure. The source-route matrix remains useful infrastructure, but it no longer supports a live source-visible structural claim.

## Retractions

Each entry below is a claim that was made, tested, and withdrawn. The failure reasons are kept on record because they are the guardrails for the next attempt.

### `retracted_meluhha_site_overlap_as_external_anchor_2026_05_29`

Retracted claim: literal site overlap between Meluhha cuneiform attestations and external Indus-style objects can itself support a diffuse bilingual or external-anchor candidate.

Reason: the join-surface forger reproduced or exceeded the observed 25 join rows at high rates. Random site aliases from all external sites had null >= observed share 0.815100; Mesopotamia-only aliases had null >= observed share 0.933800; a provenance-preserving non-Meluhha control would reproduce the overlap exactly.

Evidence:

- `data/meluhha/meluhha_indus_join_surface_summary.json`
- `data/meluhha/meluhha_join_surface_null_summary.json`
- `docs/meluhha_indus_join_surface.md`

Decision: retracted as evidence. The join surface remains useful infrastructure for building stricter controls with sign sequence, object type, date, and non-Meluhha matched sources.

### `retracted_520_220_x_closure_slot_beyond_register_2026_05_29`

Retracted claim: inside the `520-220-X` frame, X predicts closure versus continuation beyond site/type register.

Reason: the focused context-slot forger shows site/type does better than X. In raw clean-behavior rows, third-slot leave-one-out accuracy is 0.687500 while `site|type` accuracy is 0.812500. After exact-text collapse, third-slot accuracy is 0.781250 while `site|type` accuracy is 0.906250. Exact collapse leaves 27 continuation families and only 5 terminal-closed families, so the raw short `415` closure impression is mostly repetition/register pressure.

Evidence:

- `data/open_prototype/reports/campaign_520_220_x_context_slot_null_summary.json`
- `data/open_prototype/reports/campaign_520_220_x_context_slot_null_iterations.csv`
- `docs/campaign_520_220_x_context_slot_nulls.md`

Decision: retracted as a context-slot meaning. The `520-220-X` frame remains useful as a source-validation target, especially same-stratum contrasts among `415`, `034`, `003`, and `016`.

### `retracted_vector4_158_806_phyt_context_association_2026_05_29`

Retracted claim: the bigram `158-806` carries a defensible iconographic association with `symbol=Phyt`.

Reason: the broad context-exact scan produced a tempting association, but exact-context collapse inflated support by splitting the same inscription text across material/context variants. In context-exact mode, support is 5 and z is 12.839621, but the family-wise null share is 1. Under exact-text collapse, support drops below the scan's own five-text minimum.

Evidence:

- `data/open_prototype/reports/vector4_context_association_summary.json`
- `data/open_prototype/reports/vector4_context_association_candidates.csv`
- `data/open_prototype/reports/vector4_context_association_text_only_summary.json`
- `docs/vector4_context_association_scan.md`

Decision: retracted as a context-sign association. Keep `158-806 / Phyt` only as a focused acquisition lead.

### `retracted_directionality_source_visible_and_overlap_support_2026_05_29`

Retracted claim: source-visible `861` terminal/tail directionality and matched Lipi/Mayig overlap support the broad Vector 2 directionality candidate.

Reason: the focused skeptic controls reproduce the `861` probe and break the overlap under top-edge removal. The source-visible `861` subset has 12 target-selected rows, stored-win share 1.000000, and max null >= observed share 1. The matched overlap exact headline is not enough: Lipi side is 0.937500 with max null >= observed share 0.035000, but Mayig side is 0.929134 with max null >= observed share 0.200000. After removing the ten most frequent edge signs, the overlap drops to Lipi 0.363636 and Mayig 0.473684, each with max null >= observed share 1.

Evidence:

- `data/open_prototype/reports/effective_unicity_directionality_skeptic_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_skeptic_null_summary.csv`
- `docs/effective_unicity_directionality_skeptic_controls.md`

Decision: retracted as support. The broad harsh Indus directionality candidate remains live and unaccepted; these support lanes cannot promote it.

### `retracted_m70_source_boxed_order_window_promotion_2026_05_29`

Retracted claim: the current M-70 blind token-box packet promotes M-70 from broad row-level source visibility to a source-boxed order-window candidate.

Reason: the packet failed its matched-negative gate. Two reviewers scored 15 blind items. The maximum yes-only false-positive rate on scoring negatives was 0.714286, the maximum conservative false-positive-or-uncertain rate was 0.777778, and one M-70 target view was only uncertain for one reviewer.

Evidence:

- `docs/effective_unicity_m70_blind_token_box_packet.md`
- `data/open_prototype/reports/effective_unicity_m70_blind_token_box_review_summary.json`
- `data/open_prototype/reports/effective_unicity_m70_blind_token_box_scored_rows.csv`
- `data/open_prototype/reports/effective_unicity_m70_blind_reviews/avicenna_review.csv`
- `data/open_prototype/reports/effective_unicity_m70_blind_reviews/ohm_review.csv`

Decision: retracted as a promotion. M-70 stays a row-level source-visible broad order-window candidate only.

### `retracted_directionality_no_overlay_source_normalized_packet_2026_05_29`

Retracted claim: the no-overlay blind packet for `H-654`, `M-1310`, `M-1320`, and `M-811` promotes those route candidates to source-normalized crop/token-order candidates.

Reason: the packet failed its promotion gate. The real scoring-negative denominator was seven unique CISI controls, below the forger floor of ten. Two independent blind reviews produced maximum yes-only FPR 0.333333 and maximum conservative FPR 0.666667. `D006/M-525` leaked a printed side annotation and was excluded, scoring negatives produced hard false positives, and targets were mostly overcounted or uncertain.

Evidence:

- `docs/effective_unicity_directionality_blind_packet.md`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_review_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_scored_rows.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_reviews/blind_review_a.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_reviews/blind_review_b.csv`

Decision: retracted as a promotion. The packet is a crop-QA and control-design failure report only.

### `retracted_directionality_no_overlay_v2c_preflight_packet_2026_05_29`

Retracted claim: the v2c OCR-coordinate-fix no-overlay packet repairs the v2b label-leak failure enough to proceed to blind source-normalization review.

Reason: v2c fixed the DjVu five-coordinate OCR parser and kept zero duplicate blind image hashes, but visual preflight still found page-context/catalogue leakage and crop-world asymmetry. It failed before blind review, so no reviewer false-positive rate is meaningful.

Evidence:

- `data/open_prototype/reports/effective_unicity_directionality_public_route_probe_v2_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2c_summary.json`
- `docs/effective_unicity_directionality_visual_preflight_failures.md`
- `data/open_prototype/reports/effective_unicity_directionality_visual_preflight_failures.csv`
- `data/open_prototype/reports/effective_unicity_directionality_panel_crop_repair_v2_summary.json`
- `data/open_prototype/tools/effective_unicity_directionality_panel_crop_shortlist_v2d.py`
- `data/open_prototype/reports/effective_unicity_directionality_panel_crop_repair_v2d_manual_shortlist_clean_draft.csv`
- `data/open_prototype/reports/effective_unicity_directionality_signband_pool_v2e_summary.json`
- `docs/effective_unicity_directionality_panel_crop_repair.md`

Decision: retracted before review. The cleaned v2d crop shortlist remains acquisition infrastructure only.

### `retracted_directionality_panel_crop_v2d_packet_readiness_2026_05_29`

Retracted claim: the cleaned v2d panel-crop shortlist is ready to become a blind directionality source-normalization packet.

Reason: the fixed real-negative denominator is 9, not 12, and crop worlds are mixed enough that a reviewer could classify target/control role by visual genre.

Evidence:

- `data/open_prototype/reports/effective_unicity_directionality_panel_crop_repair_v2d_manual_shortlist_clean_draft.csv`
- `tmp/effective_unicity_directionality_panel_crop_repair/visual_qc_manual_shortlist_v2d_clean_draft.jpg`
- `docs/effective_unicity_directionality_visual_preflight_failures.md`
- `data/open_prototype/reports/effective_unicity_directionality_signband_pool_v2e_summary.json`

Decision: retracted before review. v2e is a crop-QA pool, not a packet.

### `retracted_directionality_homogeneous_signband_v2f_packet_readiness_2026_05_29`

Retracted claim: the v2e signband-like pool can be promoted into a homogeneous no-overlay v2f blind packet.

Reason: strict reuse misses `M-811`, has only seven original fixed real-negative CISIs, and has target/control source-page collisions. The derived top-strip lane is acquisition-only and still misses `M-1320`/`M-811` before visual review.

Evidence:

- `data/open_prototype/reports/effective_unicity_directionality_homogeneous_packet_v2f_preflight_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_homogeneous_packet_v2f_strict_reuse_candidates.csv`
- `data/open_prototype/reports/effective_unicity_directionality_homogeneous_packet_v2f_derived_top_strip_candidates.csv`
- `docs/effective_unicity_directionality_homogeneous_packet_v2f_preflight.md`

Decision: retracted before review. A future packet needs fixed real signband negatives, real nonlinguistic nulls, fixed-seed synthetic nulls, and zero hard or uncertain null hits.

### `retracted_directionality_public_route_visibility_support_2026_05_29`

Retracted claim: public CISI route availability and the v2e signband-like subset promote the directionality candidate toward source-normalized evidence.

Reason: the route-conditioned support gate fails. The frozen top-79 public-route probe rows have only 0.670886 stored-win share; the 38 public-route rows have 0.684211; page collapse drops the route rows to 0.625000; `site|type|symbol|direction` collapse drops them to 0.619048; and all matched route-label nulls reproduce or exceed the observed route share.

Evidence:

- `data/open_prototype/reports/effective_unicity_directionality_route_conditioned_control_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_route_conditioned_control.csv`
- `data/open_prototype/reports/effective_unicity_directionality_route_conditioned_null_summary.csv`
- `docs/effective_unicity_directionality_route_conditioned_control.md`

Decision: retracted as support. Public routes remain acquisition hooks only, not evidence for physical direction, source-normalized order, sign identity, value, meaning, language, or translation.

### `retracted_external_anchor_lu_sunzida_meluhha_diagnostic_2026_05_29`

Retracted claim: the cuneiform string `lu2-sun2-zi-da` can be used as a Meluhha-diagnostic personal-name anchor for an Indus phonetic-value search.

Reason: current CDLI `atf_transliteration` exports find `lu2-sun2-zi-da` in 15 distinct artifacts, but only one artifact has any Meluhha line and only that one has adjacent Meluhha. The name-alone detector has 14 false-positive artifacts and a measured false-positive rate of `0.933333`.

Evidence:

- `data/meluhha/tools/build_cdli_current_meluhha_exports.mjs`
- `data/meluhha/cdli_current_anchor_failure_summary.json`
- `data/meluhha/cdli_current_lu_sunzida_test.csv`
- `docs/meluhha_lu_sunzida_anchor_failure.md`

Decision: retracted as an external phonetic anchor. `P212982` remains a real cuneiform-side adjacency lead (`lu2-sun2-zi-da` before `lu2 me-luh-ha-ke4`), but it does not license any Indus sign value, phonetic value, language-family claim, or translation.

### `retracted_external_phonetic_anchor_length_pattern_values_2026_05_29`

Retracted claim: strict length/pattern compatibility between cuneiform Meluhha-side strings and Mesopotamia/Gulf external Indus-style sign sequences yields candidate phonetic values.

Reason: the candidate generator produced plausible-looking assignments, but they were pure length and duplicate-pattern matches. The same four-sign external rows can be assigned to `ma2-me-luh-ha`, `lu2-sun2-zi-da`, and `szu-i3-li2-su` with equal formal success. Pattern-matched synthetic targets reproduce every positive target at null >= observed share `1.000000`; the only duplicate-pattern target, `e-me-bal-me-luh-ha`, has zero strict candidates.

Evidence:

- `data/meluhha/tools/attempt_external_phonetic_anchors.mjs`
- `data/meluhha/external_phonetic_anchor_summary.json`
- `data/meluhha/external_phonetic_anchor_target_summary.csv`
- `data/meluhha/external_phonetic_anchor_candidates.csv`
- `docs/meluhha_external_phonetic_anchor_attempts.md`

Decision: retracted as phonetic values and external anchors. It remains useful as a negative-control harness for future object-level bridge evidence.

### `retracted_brahmi_shape_descent_nearest_neighbors_2026_05_29`

Retracted claim: nearest-neighbor shape matches between local Indus source probes and early Brahmi glyphs yield a Brahmi-descended phonetic anchor.

Reason: after repairing source-photo mask extraction, the actual local `220` probes do not converge on one Brahmi value: top-1 neighbors are `kaṃ`, `o`, and `ka`. The random shape-evolution null equals or beats the observed nearest distances too often: `0.576000`, `0.438000`, and `0.656000` for the three local `220` probes. The local `110` probe also fails, with top neighbor `a` and null <= observed share `0.666000`.

Evidence:

- `data/brahmi/tools/build_indoskript_brahmi_shape_gate.py`
- `data/brahmi/brahmi_shape_descent_null_summary.json`
- `data/brahmi/indus_brahmi_nearest_neighbors.csv`
- `data/brahmi/brahmi_shape_descent_null_iterations.csv`
- `docs/brahmi_shape_descent_gate.md`

Decision: retracted as morphological descent, phonetic value, language identification, or translation. The Brahmi route is now reusable infrastructure only.

### `retracted_brahmi_source_token_descent_v2_2026_05_30`

Retracted claim: exact projection-gap source-token crops compared against a larger early Brahmi glyph set yield a Brahmi-descended phonetic anchor.

Reason: the expanded v2 gate retained 1,342 early Brahmi glyph features from 36 Indoskript manuscripts and 611 Indus source-token features from 61 exact projection-gap source rows. It tested 83 sign/orientation families with >= 2 samples. All 83 failed the pre-registered gates; candidate-only rows = 0 and accepted phonetic anchors = 0. The strongest near-misses were `817=dhya`, `527=ra`, `472=ra`, `060=ka`, and `061=ra`, but their shape-null or label-null rates exceeded the required `0.01` thresholds. A duplicate-collapse audit then weakened those near-misses further: `817`, `472`, and `060` collapse below two unique token hashes, while `527` and `061` are single-CISI only.

Evidence:

- `data/brahmi/source_token_brahmi_descent_v2_summary.json`
- `data/brahmi/source_token_family_descent_summary_v2.csv`
- `data/brahmi/source_token_shape_null_iterations_v2.csv`
- `data/brahmi/source_token_label_null_iterations_v2.csv`
- `data/brahmi/source_token_duplicate_collapse_audit_v2_summary.json`
- `data/brahmi/source_token_duplicate_collapse_audit_v2.csv`
- `docs/brahmi_source_token_descent_gate_v2.md`

Forger/null status:

- Shape null: 200 random shape-evolution iterations per token-family sample.
- Label null: 1,000 Brahmi-label shuffle iterations per family.
- Survival rule: >= 2 samples, 100% modal Brahmi-label agreement, shape null <= 0.01, label null <= 0.01. A survivor would still be candidate-only pending manual visual descent review.
- Observed result: zero families survived.
- Duplicate-collapse result: 18 raw-unanimous families collapse below two unique token hashes, six raw-unanimous families are single-CISI only, and six raw-unanimous families survive duplicate collapse but still fail the original null gates.

Decision: retracted as morphological descent, phonetic value, language identification, or translation. The v2 source-token gate is reusable infrastructure and a stronger negative result.

### `retracted_anchored_constraint_collapse_from_rejected_anchors_2026_05_29`

Retracted claim: injecting the current weak external and Brahmi anchors into the effective-unicity instrument yields a partial reading or sharp constraint collapse.

Reason: there are no accepted anchors to inject. Forcing rejected anchors as a stress test still barely dents the label-symmetry floor. The current strongest rejected stress set combines the strict mapped `U17649` onomastic assignment (`002=ur;004=gun3;328=a;001=me;803=luh;415=ha`) with the Brahmi v2 near-miss set (`817=dhya;527=ra;472=ra;060=ka;061=ra`). It fixes 11 signs and leaves `4310.379871` bits from a `4410.970864`-bit baseline. The forced assignments remain inadmissible because the onomastic assignment failed the object/readable-script bridge and site-shuffle forger, while Brahmi v3 blocks all v2 families before visual review.

Evidence:

- `data/open_prototype/tools/anchored_constraint_collapse_stress.mjs`
- `data/open_prototype/reports/anchored_constraint_collapse_stress_summary.json`
- `data/open_prototype/reports/anchored_constraint_collapse_stress.csv`
- `docs/anchored_constraint_collapse_stress.md`

Decision: retracted as partial reading, phonetic value, and language identification. The stress curve is a guardrail only.

### `retracted_240_220_032_selects_single_y_2026_05_28`

Retracted claim: `240-220-032` controls one specific Y ending after `002`.

Reason: the adjacent `032-002` context campaign found strict target rows split across `300`, `817`, `820`, and `861`, with both terminal and continuing outcomes.

Evidence:

- `data/open_prototype/reports/campaign_032_002_context_summary.json`
- `docs/campaign_032_002_context_branch_campaign.md`

### `retracted_all_002_y_are_endings_2026_05_28`

Retracted claim: all signs after `002` are endings or terminal closures.

Reason: the post-Y continuation campaign split `002-Y` signs into closure-heavy and branch-head classes; `390`, `368`, `031`, `220`, `900`, and `300` are continuation-heavy.

Evidence:

- `data/open_prototype/reports/campaign_032_002_post_y_summary.json`
- `docs/campaign_032_002_post_y_continuation_campaign.md`

### `retracted_internal_only_effective_unicity_gives_language_family_2026_05_29`

Retracted claim: internal effective-unicity or masked-sign constraint can by itself choose among Dravidian, Indo-Aryan/Sanskritic, Elamite-adjacent, or unknown-language priors.

Reason: without an external sign-to-value anchor, any phonetic labeling remains invariant under global permutation of value labels. The full strict exact-collapsed corpus has 571 observed signs, giving a lower-bound unanchored label-symmetry degeneracy of log2(571!) = 4,410.970864 bits before nulls, allographs, homophony, or polyvalence are added.

Evidence:

- `data/open_prototype/reports/effective_unicity_degeneracy_summary.json`
- `docs/effective_unicity_methods_note.md`

### `retracted_source_visible_032_002_y_packet_2026_05_29`

Retracted claim: current source-visible row-level evidence supports `032-002-Y` as a real same-signband packet across target, non-240 `A-220-032`, and outside-`A-220` contexts.

Reason: the blind matched-negative source-box adjudication failed. Two independent blind reviewers produced yes-only false-positive rates of 0.400000 and 0.300000 on negatives, conservative negative-failure rates of 0.500000 and 0.416667, and zero yes-only sensitivity on positives.

Evidence:

- `data/open_prototype/reports/source_box_blind_adjudication_summary.json`
- `data/open_prototype/reports/source_box_blind_adjudication_scored_rows.csv`
- `data/open_prototype/reports/source_box_blind_reviews/heisenberg_review.csv`
- `data/open_prototype/reports/source_box_blind_reviews/jason_review.csv`
- `docs/source_box_blind_adjudication_results.md`

### `retracted_meluhha_context_leads_as_external_anchors_2026_05_29`

Retracted claim: CDLI Meluhha context leads such as `szu-i3-li2-su`, `a-li-a-hi`, `lu2-tukul`, `ur-{d}lamma`, `gug gi-rin-e`, or `ur gun3-a me-luh-ha` can be promoted into Indus external anchors by contextual specificity, same-site overlap, or strict sign-count/duplicate-pattern compatibility with external Indus-style rows.

Reason: paginated CDLI matched negatives break the standalone anchors, and the remaining source-side survivors do not connect to specific Indus objects. `szu-i3-li2-su` now returns 207 CDLI artifacts over three pages; 175 have query-line hits, and only one query-line artifact has any Meluhha line, giving false-positive rate `0.994286`. `lu2-tukul` has false-positive rate `0.976190`; `gurusz`, `nu-banda3`, `ur-{d}lamma`, and `ur-{d}ig-alim` fail at `0.995772` to `1.000000` in the paginated/capped searches. The external bridge retest has 23 query/site rows, 4 Ur/Susa/Failaka-focus rows, 8 same-site strict pattern matches, and zero object-level bridges. Same-site pattern matches have pattern-only forger share `1.000000` by construction.

Evidence:

- `data/meluhha/cdli_meluhha_context_leads.csv`
- `data/meluhha/cdli_meluhha_context_lead_query_plan.csv`
- `data/meluhha/cdli_context_lead_matched_negative_summary.csv`
- `data/meluhha/cdli_context_lead_matched_negative_artifacts.csv`
- `data/meluhha/cdli_context_lead_matched_negative_fetch_log.csv`
- `data/meluhha/context_lead_external_bridge_retest.csv`
- `data/meluhha/context_lead_external_bridge_retest_summary.json`
- `docs/meluhha_context_lead_matched_negatives.md`

Skeptic attacks that broke the claim:

- CDLI first-page search is capped; after pagination, `szu-i3-li2-su` becomes a much worse Meluhha detector than the initial current-export count implied.
- Phrases that literally contain `me-luh-ha` are useful source-side contexts but cannot serve as independent Meluhha diagnostics.
- The Irisagrig `a-li-a-hi dam-a-ni` cluster is 3/3 Meluhha-adjacent, but remains a small local cuneiform cluster with no external object bridge.
- The Ur `ur gun3-a me-luh-ha` to row `3898.1` overlap is only same-site `ABCDEF` pattern compatibility; no accession, publication, owner, title, or object-level link exists.
- Ur/Susa/Failaka catalogue routes remain acquisition targets, not anchors; BM `120573 / U.7683` is promising as a route because it is an Indus-style stamp seal with a Sumerian inscription, but it is outside the local external-object rows and has no verified Meluhha name/title bridge in the current workspace.

Decision: retracted as an external anchor. Residual value: a cleaner source-side Meluhha query surface and a paginated matched-negative harness.

### `retracted_bm120573_as_external_phonetic_anchor_2026_05_30`

Retracted claim: BM `120573 / U.7683 / 1928,1009.56` can provide an object-level external phonetic anchor for local Ur Indus sign rows.

Reason: BM `120573` is verified as a rectangular Diqdiqqah/Ur cuneiform-inscribed Indus-style stamp seal, but current evidence does not give an Indus sign sequence on that object. Gadd no. 1 treats the cuneiform reading as doubtful, with best provisional reading `sak-ku-shi-?` in ASCII, and does not use it to read the Indus script. The five local Ur external rows (`3897.1`, `3898.1`, `3899.1`, `5225.1`, `5231.1`) do not map to BM `120573`; four are circular, and all five are local Indus numeric sign-sequence rows rather than the cuneiform-only BM object.

Evidence:

- `data/meluhha/bm120573_object_bridge_audit_summary.json`
- `data/meluhha/bm120573_object_bridge_audit.csv`
- `docs/bm120573_object_bridge_audit.md`
- British Museum collection page: `https://www.britishmuseum.org/collection/object/W_1928-1009-56`
- British Museum bibliography page for Gadd 1932a: `https://www.britishmuseum.org/collection/term/BIB2877`

Forger/null status:

- This is an object-identity gate, not a statistical association: mapped local rows = 0; accepted external anchors = 0.
- The earlier `3898.1` temptation remains rejected as same-site length/pattern evidence only.

Decision: retracted as an external anchor and phonetic-value source. Residual value: BM `120573` remains an acquisition target for Mitchell 1986 no. 7 / fig. 111 and Parpola 1994 p. 131, but cannot be used as a sign-value anchor unless a source records an Indus sign sequence or maps it to a local external row.

### `retracted_gadd_ur_accession_bridge_micro_bilingual_2026_05_30`

Retracted claim: the Gadd Ur object set provides a micro-bilingual external phonetic anchor for local Ur Indus rows.

Reason: Gadd/Penn routes now improve object identity for two local rows, but not enough to produce a reading. `3898.1` maps to `U17649`, and `3899.1` maps to `U8685`; both are Indus-inscribed Ur objects with no readable cuneiform name, title, owner, profession, or Meluhha formula attached. The modeled Gadd/BM/Penn surface has seven Indus-sequence-only objects and one cuneiform-only object, BM `120573 / U.7683`; zero modeled objects combine an Indus sequence with readable cuneiform.

Evidence:

- `data/meluhha/gadd_ur_accession_bridge_audit_summary.json`
- `data/meluhha/gadd_ur_accession_bridge_audit.csv`
- `docs/gadd_ur_accession_bridge_audit.md`
- Gadd PDF: `https://ignca.gov.in/Asi_data/33779.pdf`
- British Museum Gadd bibliography page: `https://www.britishmuseum.org/collection/term/BIB2877`
- Penn Museum Journal, Woolley 1933: `https://www.penn.museum/sites/journal/9405/`

Forger/null status:

- This is an object-identity micro-bilingual gate, not a statistical association: local Ur rows checked = 5; verified excavation mappings = 2; modeled Gadd objects = 8; modeled micro-bilingual objects = 0; accepted external anchors = 0.
- Candidate mappings for `3897.1` and `5231.1` remain below the accession-verified threshold and lack cuneiform in any case.

Skeptic attacks that broke the claim:

- `3898.1/U17649` and `3899.1/U8685` are object-mapped but Indus-only.
- BM `120573 / U.7683` is cuneiform-only in the current BM/Gadd source surface and lacks a recorded Indus sequence.
- No mapped Indus object carries a cuneiform owner, title, profession, Meluhha formula, or personal name.
- Ur site overlap with Meluhha texts has already failed the pattern/site forger and cannot be promoted through this object-route audit.

Decision: retracted as an external anchor and phonetic-value source. Residual value: source-route infrastructure for Ur is stronger, especially for `3898.1/U17649` and `3899.1/U8685`, and the next acquisition lane is Mitchell 1986 figures 106-117 plus unresolved fragment/catalogue rows.

### `retracted_object_level_onomastic_value_attempts_2026_05_30`

Retracted claim: object-routed Meluhha onomastic and lexical phrases yield candidate phonetic values for external Indus signs.

Reason: the harness tested 12 cuneiform-side strings against 30 external Mesopotamia/Gulf rows with parseable signs and wrote 47 pattern-compatible candidate rows. Only one attempt reached the strict mapped-object lane: `ur gun3-a me-luh-ha` against `3898.1/U17649`, proposing `002=ur;004=gun3;328=a;001=me;803=luh;415=ha`. That row is object-mapped, but the object is Indus-only in the current source surface. The cuneiform phrase is from a separate Ur text, not from `U17649`.

Evidence:

- `data/meluhha/object_level_onomastic_value_summary.json`
- `data/meluhha/object_level_onomastic_value_attempts.csv`
- `data/meluhha/object_level_onomastic_value_forger_iterations.csv`
- `docs/object_level_onomastic_value_attempts.md`

Forger/null status:

- Target phrases tested: 12.
- Focus external objects with parseable signs: 30.
- Candidate rows written: 47.
- Same-site or equivalent value attempts: 1.
- Strict mapped Indus-only value attempts: 1.
- Target-site shuffle iterations: 10,000.
- Null >= observed share: 0.6857.
- Accepted external anchors: 0.

Skeptic attacks that broke the claim:

- The only strict mapped attempt uses `U17649 / 3898.1`, an Indus-only object.
- The cuneiform phrase `ur gun3-a me-luh-ha` is from a separate Ur text and is not attached to `U17649` by owner, seal impression, title, profession, or exact find-context pairing.
- The proposed assignment depends on six-unit length and all-distinct pattern compatibility.
- The target-site shuffle forger reproduces the observed strict mapped same-site attempt count at high rate.

Decision: retracted as an external anchor and phonetic-value source. Residual value: this is the reusable value-attempt harness for any future exact Kjaerum, Amiet, Mitchell, or Sarzec/Heuzey bridge.

### `retracted_brahmi_independent_source_token_gate_v3_2026_05_30`

Retracted claim: the v2 Brahmi source-token near-misses survive duplicate collapse and object-independence preflight strongly enough to become visual-review candidates.

Reason: all 83 v2 sign/orientation families are blocked before review. The v3 gate requires at least three unique token hashes, three unique CISI objects, three unique source paths, unanimity after duplicate collapse, unchanged modal label after collapse, original shape-null <= 0.01, and original label-null <= 0.01. Review-packet eligible rows, candidate-only rows, and accepted phonetic anchors are all zero.

Evidence:

- `data/brahmi/brahmi_independent_source_token_gate_v3_summary.json`
- `data/brahmi/brahmi_independent_source_token_gate_v3.csv`
- `docs/brahmi_independent_source_token_gate_v3.md`

Forger/null status:

- Input families: 83.
- Blocked before review: 83.
- Review-packet eligible rows: 0.
- Candidate-only rows: 0.
- Accepted phonetic anchors: 0.
- Blocked reason counts: shape-null above 0.01 = 83; label-null above 0.01 = 72; fewer than 3 unique CISIs = 58; not unanimous after duplicate collapse = 53; fewer than 3 unique token hashes = 36; modal label changes after collapse = 23; fewer than 3 unique source paths = 22.

Skeptic attacks that broke the claim:

- The top v2 near-misses are not independent witness families: `817`, `472`, and `060` collapse to one unique token hash and one CISI; `527` and `061` have one CISI and two unique token hashes.
- Every family still fails the original shape-null threshold.
- Most families also fail the label-null threshold or lose unanimity after duplicate collapse.

Decision: retracted as a descendant-script phonetic anchor. Residual value: v3 is now the cheap pre-review filter for any future Brahmi swing.

## Reusable Infrastructure Produced

These artifacts survive the retractions: they are the datasets, harnesses, and audit notes the next campaigns build on.

- `data/claim_ledger/claims.json`: global claim ledger.
- `data/sign_crosswalk/`: normalized provenance-tagged crosswalk scaffold with 1,085 unaccepted candidate edges; latest audit passes with caveats, zero accepted edges, zero dangling references, and zero evidence hash/path errors.
- `docs/sign_crosswalk_audit.md`: human-readable crosswalk audit with highest-pressure review targets and namespace caveats.
- `data/meluhha/`: Vector 1 scaffold with 16 fetch-backed Meluhha cuneiform attestation rows from 10 requested source pages, 18 successful source fetches, 41 external Indus-object rows, 25 literal site-overlap Meluhha-Indus join lanes, 5 control toponyms, a current CDLI Lu-Sunzida matched-negative gate, a strict external phonetic-anchor attempt over 29 Mesopotamia/Gulf focus rows, a paginated context-lead matched-negative harness over 52 unique CDLI queries, a BM `120573` object-identity audit, a Gadd Ur accession bridge audit that verifies `3898.1/U17649` and `3899.1/U8685` while finding zero micro-bilinguals, a Laursen Gulf Type external-object acquisition queue, and an object-level onomastic value-attempt harness; accepted external anchors remain zero.
- `docs/meluhha_cuneiform_inventory.md`: human-readable inventory note for the expanded cuneiform-side Meluhha table.
- `docs/meluhha_indus_join_surface.md`: controlled site-overlap join-surface note for Vector 1.
- `docs/meluhha_matched_control_schema.md`: next Vector 1 matched-control schema after the site-overlap forger failure.
- `docs/meluhha_external_phonetic_anchor_attempts.md`: direct value-attempt note showing that length/pattern-only assignments fail the forger and produce no accepted external anchor.
- `docs/meluhha_context_lead_matched_negatives.md`: paginated CDLI context-lead matched negatives and external bridge retest; no source-side survivor becomes an object-level external anchor.
- `docs/bm120573_object_bridge_audit.md`: object-level audit for BM `120573 / U.7683`; verified route, rejected as an external phonetic anchor.
- `docs/gadd_ur_accession_bridge_audit.md`: Ur/Gadd accession bridge audit; verifies two local row/object mappings and rejects the micro-bilingual route.
- `docs/gulf_type_indus_external_queue.md`: Laursen Table 1 external `Gulf INDUS` rows normalized into the next object-level bridge acquisition queue.
- `docs/object_level_onomastic_value_attempts.md`: direct value-attempt harness; tries and rejects the strongest current `3898.1/U17649` onomastic assignment.
- `data/brahmi/`: Brahmi back-door acquisition and shape-null surface. Gate 1 has 457 early Indoskript Brahmi glyph features, 14 Indus probes, nearest-neighbor retrieval, and 500 random shape-evolution nulls per actual source probe. Gate 2 has 1,342 early Brahmi glyph features, 611 source-token features, 83 sign/orientation families, 200 shape-null iterations per token-family sample, 1,000 label-null iterations per family, and a duplicate-collapse audit. Gate 3 blocks all 83 v2 families before visual review under stricter token-hash/CISI/source-path independence and duplicate-collapse unanimity rules. The real-token impostor forger directly reproduces 61 of 82 fully simulated families above the `0.01` threshold, and the 2026-05-31 low-null autopsy rejects the remaining 21 low-null rows: all fail shape-null, 19 fail label-null, 11 fail minimum source-token independence, and zero pass both minimum independence and duplicate-collapse unanimity. No candidate-only or accepted anchor survives.
- `docs/brahmi_shape_descent_gate.md`: human-readable failed Brahmi descent gate; no phonetic anchor accepted.
- `docs/brahmi_source_token_descent_gate_v2.md`: expanded source-token Brahmi gate and Priority C rejected-near-miss stress note.
- `docs/brahmi_independent_source_token_gate_v3.md`: duplicate/CISI/source-path independence preflight for v2 near-misses; zero review-eligible rows.
- `docs/brahmi_real_token_low_null_autopsy_v3b.md`: hostile audit of the low real-token impostor rows; zero review-eligible rows.
- `docs/anchored_constraint_collapse_stress.md`: synthesis stress curve showing that rejected anchors do not produce a collapse or partial reading.
- `docs/campaign_520_220_x_context_slot_nulls.md`: focused Vector 4 negative result for `520-220-X` closure/continuation beyond site/type.
- `docs/vector4_context_association_scan.md`: broad Vector 4 context-association scanner with context-exact and exact-text collapse modes; no association survived, and `158-806 / Phyt` was retracted as duplicate/context inflation.
- `docs/campaign_002_y_partition_source_queue.md`: source-normalization acquisition queue for the broad `002-Y` partition; after corrected supplemental public CISI acquisition, every branch-pole sign has a grade >= 2 route hook.
- `docs/campaign_002_y_branch_gap_public_source_acquisition.md`: supplemental public CISI route note for branch-gap signs `368`, `031`, and `220`; route candidates only, with the false `H-44` OCR route demoted, and no token-boxed or source-normalized claim.
- `docs/campaign_002_y_branch_gap_blind_packet.md`: first blind branch-gap source-box packet, with label-free visual QA, six target/backup rows, six scoring negatives, two quarantine controls, and a failed stage-1 blind token-count gate.
- `docs/source_box_negative_control_v2_targets.md`: five-row source acquisition queue for the missing `220-032` not followed by `002` negative-control lane.
- `data/open_prototype/reports/source_box_negative_control_v2_public_routes.csv`: public-route acquisition table for the v2 negative controls; M-381 now has a strong CISI India source-page crop, M-124 and M-38 have weaker public routes, and H-601/H-1678 remain secondary-catalogue-only.
- `data/open_prototype/reports/source_box_negative_control_v2_source_status.csv`: target-level adjudication status table; only M-381 is in `adjudication_queue_only`, with accepted-claim increments held at zero.
- `docs/source_box_negative_control_v2_m381_adjudication_packet.md`: one-item M-381 packet splitting blind tokenization from unblinded catalog alignment.
- `docs/source_box_negative_control_v2_m381_blind_adjudication.md`: blind adjudication result for M-381; three reviewers returned token counts of 9, 13, and 9 against the seven-token catalog key, all reporting fusion risk, so the panel failed clean-negative promotion.
- `docs/effective_unicity_methods_note.md`: Vector 2 structural degeneracy note and reproducible report pointers.
- `docs/effective_unicity_known_script_comparator.md`: Linear B Series D scarcity calibration for Vector 2.
- `docs/effective_unicity_sumtablets_comparator.md`: SumTablets glyph-only known-script administrative calibration for Vector 2.
- `docs/effective_unicity_nonlinguistic_comparator.md`: structured nonlinguistic comparator boundary for Vector 2.
- `docs/effective_unicity_realworld_nonlinguistic_comparator.md`: real-world nonlinguistic and ambiguous-system calibration for Vector 2.
- `docs/effective_unicity_directionality_comparator.md`: stored-order versus reversed-order directionality calibration for Vector 2.
- `docs/effective_unicity_directionality_skeptic_controls.md`: support-lane retraction for source-visible `861` and matched Lipi/Mayig overlap.
- `docs/effective_unicity_directionality_block_controls.md`: block-holdout boundary for the directionality candidate.
- `docs/effective_unicity_directionality_site_balance.md`: site-balance boundary for the directionality candidate.
- `docs/effective_unicity_directionality_site_profiles.md`: within-site profile boundary for the directionality candidate.
- `docs/effective_unicity_directionality_policy_controls.md`: recorded-direction policy boundary for the directionality candidate.
- `docs/effective_unicity_directionality_influence_controls.md`: influence and concentration boundary for the directionality candidate.
- `docs/effective_unicity_directionality_formula_family_controls.md`: metadata source-convention and formula-family boundary for the directionality candidate.
- `docs/effective_unicity_directionality_route_conditioned_control.md`: failed route-conditioned support gate for public CISI route visibility and v2e signband-like route subsets.
- `docs/effective_unicity_directionality_source_queue.md`: ranked source-validation queue for the major-site directionality candidate.
- `docs/effective_unicity_directionality_public_route_probe.md`: public CISI OCR route probe and manual visual-admissibility triage for top directionality rows; four attempted no-overlay target crops, zero accepted claim increment.
- `docs/effective_unicity_directionality_blind_packet.md`: failed no-overlay blind packet for `H-654`, `M-1310`, `M-1320`, and `M-811`, with two blind reviews and scored false-positive/target-recovery failure.
- `docs/effective_unicity_directionality_blind_packet_v2b.md`: stricter failed no-overlay packet for `H-654`, `M-1310`, `M-1320`, and `M-811`, with 12 real negatives, three blind reviews, real-negative label leakage, and unstable target counts.
- `docs/effective_unicity_directionality_panel_crop_repair.md`: corrected OCR-route and object-panel crop-repair note. v2c is demoted to a visual-preflight failure; the v2 repair inventory has 278 candidates across 22 CISIs, the cleaned v2d shortlist is rejected as a packet, the v2e pool has 488 wider signband-like candidate crops, and the v2f homogeneous gate rejects promotion. No blind review and no claim increment.
- `docs/effective_unicity_directionality_homogeneous_packet_v2f_preflight.md`: failed homogeneous signband-strip packet gate and future forger/null requirements.
- `docs/effective_unicity_directionality_m70_source_pilot.md`: first source-visible row-level pilot from the directionality queue.
- `docs/effective_unicity_m70_blind_token_box_packet.md`: failed M-70 blind token-box promotion gate, with two independent reviews and false-positive rates.
- `docs/strongest_result_brief.md`: one-page brief of the strongest current result, centered on Vector 2 structural degeneracy rather than a source-gated reading.
- `docs/completion_gap_matrix.md`: requirement-by-requirement status matrix for the active goal; records the one accepted structural finding and the remaining open gaps.
- `docs/source_visible_032_002_y_witness_matrix.md`: consolidated source-route witness matrix for the retracted `032-002-Y` packet candidate.

## Current Bottom Line

There is a real structural vortex around broad `002-Y`. Even a post-hoc partition forger — one allowed to hunt for its own best split in every null corpus — cannot reproduce the `817/820` versus `390/368/031/220` split in 10,000 iterations per null model.

The corrected source queue makes the bottleneck explicit: route hooks now exist for every branch-pole sign, including `368`, `031`, and `220`, and the false `H-44` route is demoted instead of laundered into evidence.

The directionality source queue now has a public-route triage surface too: 38 plate-route candidates from 79 high-pressure rows. But the source-image work keeps failing its own gates. Two reviewed no-overlay packets for `H-654`, `M-1310`, `M-1320`, and `M-811` have failed, and v2c failed visual preflight before review. v2b fixed the obvious denominator and duplicate-hash flaws but exposed a deeper crop-source problem: OCR word-box masking still leaves neighboring catalogue labels in real controls. The panel-crop repair inventory is now a crop-QA surface: 278 candidates across 22 CISIs, a cleaned v2d shortlist rejected as a packet because the fixed denominator is 9 and crop worlds are mixed, a widened v2e pool with 488 candidate crops across 38 public plate-route CISIs, and a v2f homogeneous gate rejected because strict reuse misses `M-811`, has seven original fixed real negatives, and collides on source pages.

The first branch-gap blind packet failed stage-1 token-count promotion, while surfacing a useful `M-12` catalog/source tokenization lead; the follow-up audit keeps it unpromoted because a scoring negative reproduces stable over-counting at 1/6.

Vector 2 gives a quantitative degeneracy frame for the broader corpus. The first source-box attempts at upgrading `032-002-Y`, M-70, the directionality no-overlay packets, and the branch-gap packet all failed under blind review gates, and the broad Vector 4 context scan killed its own `158-806 / Phyt` lead. None is strong enough to state as an accepted epigraphic finding yet. The honest current result is structure found, no reading earned.
