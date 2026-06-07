# Experiment Backlog

Date: 2026-05-26

The experiments are ordered to prevent premature translation. Each experiment must publish inputs, corpus version, sign list, exclusions, code or manual protocol, outputs, and failure criteria.

## Phase 0: Corpus Integrity

Related protocols:

- [Corpus acquisition protocol](corpus_acquisition_protocol.md)
- [Falsification protocol](falsification_protocol.md)
- [Accuracy framework](accuracy_framework.md)
- [Evidence ledger](evidence_ledger.md)
- [First sprint plan](first_sprint_plan.md)
- [Comparator benchmark design](comparator_benchmark_design.md)
- [Known-script scarcity comparator acquisition audit](known_script_scarcity_comparator_acquisition_audit.md)

### E0.1 Corpus Inventory

Question: Which corpora can we legally and practically use?

Inputs:

- M77/IDF80 via indusscript.in if exportable.
- CISI data through open leads and library access.
- ICIT if access is granted.
- Open WIP datasets such as `mayig/indus-valley-script-corpus`.
- Public CSVs only after provenance audit.

Pass:

- Each inscription has source, ID, sign sequence, direction, artifact type, site, material, completeness, image availability, and uncertainty flags.

Fail:

- Any dataset mixes accepted corpus data with a claimed decipherment without separable columns.

### E0.2 Sign Inventory Crosswalk

Question: How do Mahadevan, Parpola, Wells/Fuls, and open datasets map signs to each other?

Pass:

- Crosswalk supports one-to-one, one-to-many, allograph, uncertain, and rejected mappings.

Fail:

- A sign merge is made only because it helps a reading.

Current prototype result:

- [Provisional crosswalk audit](provisional_crosswalk_audit.md) derived positional candidates from 136 strict rows and 739 aligned positions.
- The high-frequency review queue is `740 -> P324`, `002 -> P122`, `220 -> P050`, `390 -> P086`, and `032 -> P145`.
- A possible merge/allograph cluster was found where `817` and `861` both align to `P385`.
- [Lipi variant crosswalk pressure](lipi_variant_crosswalk_pressure.md) adds targeted pressure on the live H-series variants: `154/156` both align to `P004`, making collapse an active competitor, while `033` aligns to `P147` and `034` has no clean overlap candidate row.
- [Lipi 034 crosswalk darkness diagnostic](lipi_034_crosswalk_darkness_diagnostic.md) explains the `034` zero-row result: the current Mayig overlap has no exact lipi `034` token rows, so the gap is coverage darkness rather than clean-crosswalk filtering.
- [Lipi 034 Mayig acquisition targets](lipi_034_mayig_acquisition_targets.md) converts the `034` coverage gap into six P0 missing Mohenjo-daro target objects: `M-2104`, `M-315`, `M-1206`, `M-685`, `M-1584`, and `M-1963`.
- [Lipi 034 P0 public lead search](lipi_034_p0_public_lead_search.md) stores public leads for those six objects. `M-2104` is now the first P0 object with extractable prior-sign data: Parpola 2019 text no. 12 is described as `UIII` plus signs 15 and 1. `M-1206` has a CISI image lead, `M-315` and `M-685` have source-route/catalogue leads, and `M-1584`/`M-1963` are direct request targets.
- [Lipi 034 M-315 second-slot decision gate](lipi_034_m315_second_slot_decision_gate.md) turns M-315 into a narrow blind classification problem instead of a claimed reading. M-315 is source-visible and uniquely carries local `390-034-002`, but the second unit is not source-validated as numeric `034`. Public source-panel crops now exist for same-site non-034 controls `M-17`, `M-32`, `M-984`, `M-803`, and `M-918`; `M-984` is the clean new `004` comparator, `M-803` is weak, `M-918` is not token2-grade, and `M-1833` remains CISI 3.1/equivalent gated.
- [Lipi 034 M-315 preblind token-2 sort](lipi_034_m315_preblind_token2_sort.md) fixes the first M-315 target-crop error: old `second_034_region` crops followed page order, while the local `R/L` second-slot candidate is the stroke-bundle adjacent to edge `390`. Expanded first-three context crops now compare M-315 against `003`, `004`, `005`, `016`, and `869` public controls. The next gate is blind stroke-bundle/count/allograph sorting, with downgrade if M-315 collapses into a control class, damage, compound segmentation, or direction/metadata artifact.
- [Lipi 034 M-315 blind 390-X-002 sort](lipi_034_m315_blind_390x002_sort.md) executes that gate. The strict blind result is negative for upgrade: M-315 upper face clusters with M-984 `004`, while M-315 lower impression does not independently preserve a distinct `034` class. M-315 remains source-visible and locally unique, but it cannot be used as positive `034` evidence for translation work until higher-resolution source evidence or independent source transcription reverses this pressure.
- [Lipi 034 post-M315 reprioritization](lipi_034_post_m315_reprioritization.md) removes M-315 from the positive evidence pool and chooses `M-1206 +520-220-034+` as the next source-visible gate. The research question is now whether local `034/415` in the `520-220-X` frame are separate signs, allographs, source-side mapping artifacts, or transcription-policy splits. `M-685` and `M-1584` stay secondary pressure cases, `M-2104` stays CISI 3.1-gated, and `M-1963` stays public-dark.
- [Lipi 034 M-2104 Parpola extraction](lipi_034_m2104_parpola_extraction.md) attacks that lead directly. Local rows show `M-2104 +151-097-700-034+` against Parpola's named tablet parallels `M-478/M-480/M-1425 +400-097-700-004+`, giving candidate extraction `151 -> sign 1`, `097 -> sign 15`, `400 -> sign 107`, and `700-034` versus `700-004` as the `UIII` versus `UIIII` pot-count cluster.
- [Lipi 034 M-2104 source route probe](lipi_034_m2104_source_route_probe.md) makes the parallel side of that test public-image reachable. IA/CISI plate images are located for `M-478`, `M-480`, and `M-1425`, plus `H-543`, `H-544`, `M-915`, `M-715`, and `M-896`; exact IA OCR still does not locate `M-2104`.
- [Lipi 034 M-2104 visual stroke probe](lipi_034_m2104_visual_stroke_probe.md) stores the first five crop notes, 15 segmentation target boxes, and four overlay images. `M-478` and `M-1425` are strong first-pass four-stroke/U-pot-like parallels, `M-480` is weaker, and `M-2104` remains Parpola-standardized. The next step is blind sign-level segmentation, not another broad score.
- [Lipi 034 M-2104 blind visual adjudication](lipi_034_m2104_blind_visual_adjudication.md) runs that first independent visual check. `M-478 A` survives as the strong four-stroke adjacent-cluster witness; `M-1425 A` survives provisionally with blur/contamination caution. The next decisive evidence is raw or higher-resolution `M-2104`, not more public-parallel browsing.
- [Lipi 034 M-2104 raw source alias route](lipi_034_m2104_raw_source_alias_route.md) finds that raw target-side route: local source hook `VS 875CXIV:532 | -12.0 ft` matches Marshall no. `532`, Plate `CXIV`, `VS 875`, and Harappa's public Plate CXIV image shows no. 532 lower left. The next step is blind segmentation on that limited-resolution witness while waiting for a higher-resolution Harappa/CISI/Marshall image.
- [Lipi 034 M-2104 Marshall 532 visual adjudication](lipi_034_m2104_marshall532_visual_adjudication.md) runs that check. The no. 532 crop passes image reachability and cluster visibility, but fails exact count validation: the adjacent marks are `3-to-4 ambiguous`. A higher-resolution image is now the decisive next item for this branch.
- [Lipi 034 M-2104 Marshall Vol III CXIV source adjudication](lipi_034_m2104_marshall_vol3_cxiv_source_adjudication.md) finds the best public higher-resolution route: IA/IGNCA `in.gov.ignca.48270`, Plate CXIV leaf `48270_0205`, 2601 x 3483. It upgrades no. 532 from low-res public image to source-visible target, but still fails exact three-stroke `034`, fails local four-token segmentation validation, and records Marshall's five-character description as an active crosswalk/segmentation warning.
- [Lipi 034 M-2104 M77 identity and segmentation probe](lipi_034_m2104_m77_identity_and_segmentation_probe.md) locates Mahadevan M77 text no. `2527` on IA page `0084`, stores row crops and OCR geometry, and links the local id `2527.1` to the standardized text layer. Parpola 2019 supports the `M-2104` / `UIII` prior-work hypothesis, but explicitly downgrades raw shape evidence by pointing to CISI photos; the public layer still lacks an explicit `M-2104 = Marshall no. 532 / VS 875` bridge and the five-character/four-token mismatch remains unresolved. A follow-on CISI Pakistan Vol. 2 scope check is negative for `M-2104`: its Mohenjo-daro section covers `M-595` and `M-621` to `M-1659`, so the next source target is CISI 3.1/supplemental material or archive metadata.
- [Lipi 034 M-2104 CISI 3.1 bridge route probe](lipi_034_m2104_cisi31_bridge_route_probe.md) checks the exact public/acquisition bridge. It still finds no public proof that `M-2104 = Marshall no. 532 / VS 875`, but it confirms CISI 3.1 is the correct next source, adds secondary range support that CISI 3.1 includes `m1660` to `m2132`, and records a live purchase path: Tiedekirja says the hardbound volume is available for EUR 118.25 total shipped to the USA and has no digital form. An invoice/payment-link request was sent. The row remains quarantined until CISI 3.1 or equivalent archive metadata supplies identity, raw image, and segmentation bridges.
- [Lipi 034 M-2104 M-479 source probe](lipi_034_m2104_m479_source_probe.md) closes the local-extra comparator route. `M-479 +400-097-700-004+` is visible as `M-479 A/B` on CISI India leaf `n150`, and CISI introduction leaf `n19` discusses `M-478/M-479` as a four-plus-U tablet case. M-479 is now in the stored visual test set, but only as family-internal support with duplicate-family risk, not independent proof.
- [Lipi 034 M-2104 004 family dependence](lipi_034_m2104_004_family_dependence.md) fixes the comparator weighting. `M-478/M-479/M-480` are one India same-plate tablet-family evidence unit, not three independent witnesses. `M-1425` is one provisional Pakistan-volume recurrence. This gives the current safe count for the `700-004` side: two evidence units, one provisional.
- [Lipi 034 M-2104 target-side gate recheck](lipi_034_m2104_target_side_gate_recheck.md) applies the same unit policy to the target side and records the hard failure: IA/IGNCA Marshall Plate CXIV no. 532 is the best public witness and the target is source-visible, but the adjacent group after the U/V-like unit is still `3 secure strokes plus possible fourth/boundary mark`. Exact `034 = three` fails, and the public external `M-2104 = Marshall no. 532 / VS 875` bridge remains missing. The next action is CISI 3.1 or equivalent archive/museum source acquisition, not another broad statistical pass.
- [Lipi 034 M-1206 Bhaskar Fig. 3 source probe](lipi_034_m1206_bhaskar_fig3_source_probe.md) stores the first public image route for the next P0 object. It is now superseded by a stronger direct CISI route for source validation: CISI Pakistan IA leaf `n181` / printed p. 147 labels `M-1206` and shows multiple views, including the long `M-1206 e(1)` side, so the local companion row `3556.2 +740-690-435-255-002-861+` is no longer merely missing from Bhaskar Fig. 3. Bhaskar's `M-1206`/`M-2016` conflict remains a citation cleanup problem, not the main source gate.
- 2026-05-26 update: Bhaskar replied that the `M-2016` running-text mention is a typo and Fig. 3 caption `M-1206` is correct. This resolves the citation cleanup issue for the secondary Bhaskar route. The direct CISI source page remains the source-grade route; no side transcription, value, or translation follows from the reply.
- [Lipi 034 M-1206 terminal triad](lipi_034_m1206_terminal_triad.md) turns the 52-row `520-220-X` pool into a tighter source target: `M-1912 +520-220-003+`, `M-1206 +520-220-034+`, and `M-37 +520-220-415+` share site, object type, material, shape, class, sign count, direction, and prefix. The source recheck now adds CISI India IA leaf `n54` / printed p. 19 for `M-37 A/a` and CISI Pakistan IA leaf `n181` / printed p. 147 for `M-1206`. The decisive experiment is narrowed: blind-classify M-37 and M-1206 outer signs from source crops, resolve A/a and `R/L` orientation, then add M-1912 once CISI 3.1 or equivalent raw source is available.
- [Lipi 034 M-1206 / M-37 blind visual orientation](lipi_034_m1206_m37_blind_visual_orientation.md) completes that narrowed image-side experiment for the two public-source members. It finds the same broad three-class pattern on both objects, with A/a mirror order, but not fine-form identity. The next experiment is not another broad audit: collect source-visible `520-220-415` comparanda and any additional `520-220-034` comparanda, then blind-bin the outer forms before deciding whether `034/415` are allographs, subtypes, or separate signs.
- [Lipi 034 M-1206 / M-37 415 comparanda scout](lipi_034_m1206_m37_415_comparanda_scout.md) starts that collection step for `415`. It finds 17 exact `+520-220-415+` local rows and downloads public CISI source pages for `H-346`, `H-786`, and `H-938` through `H-941`.
- [Lipi 034 M-1206 / M-37 415 fine-form binning](lipi_034_m1206_m37_415_fine_form_binning.md) verifies 17 panel crops and integrates blind visual bins. Target-like panels are `H-786 A`, `H-938 A/A bis`, `H-940 A`, and `H-941 A/A bis`; `H-346 A` is weak and `H-939` does not upgrade. Follow-on [H-786 / H-941 415 side mapping adjudication](h786_h941_415_side_mapping_adjudication.md) weakens the old `.2 = B` conflict but does not close it: local row number and CISI side letter are not interchangeable. The data-register pass gives H-786 AV 775 with no side-sign mapping, and H-941 A: Plate 37:673 / B: Plate 36:3872 with no assignment to local `1821.1` or `1821.2`. H-786 A and H-941 A/A bis stay candidate visual reconciliations only; exact-side 415 evidence remains limited to H-938 A/A bis and H-940 A. No allograph/subtype/separate-sign claim yet.
- [Lipi 034 M-1206 cohesion gate](lipi_034_m1206_034_cohesion_gate.md) runs the post-M315 label-blind graphic-class packet. Two reviewers agree that the M-1206 target views are internally stable and that the closest external matches are `415`-family panels, especially M-37, with H-940/H-938 and side-gated H-786/H-941 as further pressure. M-1584 and M-685 are not classifiable in this packet. The branch moves toward `034/415` allograph, sign-splitting, side-mapping, or transcription-policy pressure, not value assignment.
- [Lipi 034 M-1206 terminal component gate](lipi_034_m1206_terminal_component_gate.md) removes the biggest confound in the previous whole-band test by isolating apparent terminal components. Two reviewers agree that T002/T003 form the M-1206 target-terminal core, T006/T007 from H-938 exact-side `415` are the closest clean controls, and T011-T016 prefix/nonterminal crops are rejected. The result strengthens terminal-level `034/415` family pressure while leaving allograph/sign-split/source-policy status unresolved.
- [H-786 / H-941 / H-938 / H-940 415 side-policy gate](h786_h941_h938_h940_415_side_policy_gate.md) closes the immediate admissibility gate after the terminal-component packet. CISI `A/B` labels and local `.1/.2` row numbers are not globally interchangeable. `H-938 A/A bis` and `H-940 A` remain clean exact-source-side `415` controls; `H-786 A` and `H-941 A/A bis` remain visual pressure only until object-specific side-label/transcription notes map them to local `1677.2` and `1821.2`.
- [H-786 / H-941 source-A pattern recheck](h786_h941_source_a_pattern_recheck.md) adds a tighter source-panel observation: the target-like broad three-class `415` pattern sits on source `A` for H-786, H-938, H-940, and H-941, not source `B`. H-939 is the damaged stress case. This strengthens the source-visible recurrence side of the `415` pool while keeping H-786/H-941 quarantined behind explicit A/B-to-row mapping.
- [H-938/H-939/H-1284/H-2145 Parpola reverse-side clue](h938_h939_h1284_h2145_parpola_reverse_clue.md) records a prior-work side clue: Parpola 2019 groups H-938/H-939/H-1284/H-2145 as `VIIII`-reverse tablets and H-940/H-2147/H-2148 as sign-no.-41 reverse tablets. This adds H-2145, H-2147, and H-2148 to the source/crosswalk queue, but it accepts no local row mapping, sign value, or translation.
- [H-2145/H-2147/H-2148 source route recheck](h2145_h2147_h2148_source_route_recheck.md) runs the next source gate. H-2147 improves to a public visual route through Meadow/Kenoyer 1997 Figure 10.17 -> H95-2514, with a stored crop packet in [H-2147 / H95-2514 public visual route](h2147_h95_2514_public_visual_route.md). The follow-up [H-2147 Figure 10 / Figure 27 accession concordance](h2147_fig10_fig27_accession_concordance.md) resolves the figure-number mismatch at accession/object level, but fragmentary local rows and lack of source-to-local side/sign assignment still block crosswalk use. H-2145 remains route-dark; H-2148 is upgraded by the Kenoyer 2005 route below.
- [H-940 / H-2147 / H-2148 `110` and Parpola sign-no.-41 gate](h940_h2147_h2148_110_sign41_gate.md) converts that clue into a bounded crosswalk test and records a correction: the checked local `110` population has six rows, not three. H-940, H-2147, and H-2148 remain the current three-object Parpola sign-no.-41 branch. H-940 B is source-visible as local `+110+`, and H-2148 is now source-visible at count-level through Kenoyer 2005 Figure 14.1. H-2100, H-2152, and Kanmer `4881.1` are outside `110` controls that must be route-checked before any broader crosswalk claim. Result: `local 110 <-> Parpola sign no. 41` remains a P0 hypothesis, not an accepted mapping.
- [H-2148 / H2001-5142 Kenoyer 2005 public visual route](h2148_kenoyer2005_public_visual_route.md) executes that acquisition target. Kenoyer 2005 Figure 14.1 publicly identifies `H2001-5142 / 11759-01`, and the item has a one-sign panel plus a three-sign panel matching local `481.2 +110+` and `481.1 +520-220-415+` by sign count. H-2148 is upgraded to `public_visual_route_count_mapped`, but this still does not prove Parpola sign no. 41, a value, or a translation. After the H-2147 recrop correction, H-2148 is the cleanest branch target.
- [H-2100 / H-2152 / Kanmer `110` outside controls route check](h2100_h2152_kanmer_110_outside_controls_route_check.md) executes the control check. H-2100 `H96-3179Figure 19.21` and H-2152 `H97-3327Figure 15.19` remain route-dark after local, exact web, Kenoyer/Meadow 2010, and Kenoyer 2000 checks; H-2152 stays high-priority because its companion row is `]220-415+`. Kanmer `4881.1` has only a refined RIHN 2012 *Excavation at Kanmer: 2005-06--2008-09* source-holder route, no exact object panel. These controls block a population shortcut but cannot yet enter the visual packet.
- [H-940 / H-2147 / H-2148 `110` branch visual precheck](h940_h2147_h2148_110_branch_visual_precheck.md) runs the first neutral visual pass after H-2148's upgrade. Result: H-2148 and H-2147 initially looked like a loose visual-family candidate, while H-940 B split out at current crop quality. The follow-up [H-2147 / H-940 `110` recrop recheck](h2147_h940_110_recrop_recheck.md) weakens H-2147 further: the public Figure 10.17 candidate is a multi-component panel, not a clean single-sign witness. H-940 IIIF max and IA JP2 routes give no real resolution upgrade. This blocks promoting the branch to an accepted `110` / Parpola sign-no.-41 crosswalk and moves the next gate to source-side notes/better panels, not more blind sorting from the same public crops.
- [H-2148 `110` / Parpola sign 41 crosswalk decision gate](h2148_110_parpola41_crosswalk_decision_gate.md) defines the next admissibility test after the source checks. The question is no longer generic similarity; H-2148's clean single-panel source image must be tied to both local `110` and Parpola sign no. 41 on the same physical side. Until that side/panel bridge exists, the branch stays P0.
- [Parpola reverse / local short-side consistency gate](parpola_reverse_local_short_side_consistency_gate.md) executes that role check over all seven objects in the clue. Result: Parpola's reverse clue consistently points to the local shorter companion row. For H-2148, the chain `reverse sign no. 41 -> 481.2 +110+ -> Kenoyer one-sign panel` is now strong_same_role_inference, not accepted crosswalk.
- [P041 / Parpola 41 crosswalk falsification gate](p041_mayig_parpola41_crosswalk_falsification_gate.md) rejects the tempting numeric shortcut. Mayig feature `P041` maps internally to Parpola `V141`, Wells `W112`, and Mahadevan `M034`; its only current Mayig overlap occurrence is M-33A, where it aligns positionally with local `112`, not local `110`. This preserves H-2148 as object-specific role pressure but blocks using Mayig `P041` as sign-no.-41 confirmation.
- [Parpola 41 / Mayig namespace probe](parpola41_mayig_namespace_probe.md) checks all 397 pinned Mayig feature files. Result: Mayig's `V041` maps to `P301`, not `P041`, and Mayig `P041` maps to `V141/W112/M034`. Therefore the next gate is the sign-list convention behind Parpola 2019's phrase "sign no. 41"; do not equate it with `P041`, `V041`, or local `110` until that convention is sourced.
- [Parpola 1994 sign 41 convention gate](parpola1994_sign41_convention_gate.md) sources that convention directly. Parpola 2019's sign no. 41 refers to Parpola 1994 Fig. 5.1 sign no. 41, visible on printed p. 70 / PDF page 88 with anthropomorphic/kneeling-pot variants. H-2148's one-sign panel is visually compatible with the family, but too low-res/fused for closed identification. The next gate is H-2148 same-side visual identity and source-note acquisition, not another namespace shortcut.
- [H-2148 same-side identity gate](h2148_same_side_identity_gate.md) runs that gate against the current public/acquisition layer. Result: no reply yet to the Harappa source-panel request, no public side-label/transcription route beyond Kenoyer 2005 Fig. 14.1, and no face label in the Kenoyer caption/table. A targeted Fuls request is now sent. H-2148 stays the cleanest live target but remains `same_side_identity_pending`.
- [H-2148 Parpola obverse recurrence stress gate](h2148_parpola_obverse_recurrence_stress_gate.md) checks Parpola's named obverse-text controls. H-2240 exactly supports local `+520-220-415+`, H-2241 is fragmentary `415` pressure, and H-942 is the live stress case at `+520-220-016+`. The next experiment is source-normalizing H-942/H-2240/H-2241, not accepting `415=016` or reading the text.
- [H-942 / H-2240 / H-2241 source normalization gate](h942_h2240_h2241_source_normalization_gate.md) executes that next experiment. H-942 is source-visible on CISI Pakistan `n374` but only as a full-signband `+520-220-016+` stress/control; H-2240 is exact local `+520-220-415+` but source-dark in the checked public layer; H-2241 is fragmentary `415` pressure and source-dark. Gmail `19e64843a928358d` now asks Andreas Fuls/Harappa for H-2240/H-2241 panels, side labels, and source transcription. Next useful work is awaiting/acquiring those sources, not collapsing `415/016`.
- [M-77 Parpola recurrence conflict gate](m77_parpola_recurrence_conflict_gate.md) checks the seal-control tail of the same Parpola recurrence sentence. M-77 is source-visible on CISI India `n68`, but local and Mayig both make it a five-sign seal string, not a `+520-220-X+` companion row. This quarantines the recurrence sentence as conflict-gated prior-work pressure. Next useful work is source transcription/sign-number bridging for M-77 and Parpola text no. 7, not expanding the branch or translating it.
- [Parpola text no. 7 scope / namespace gate](parpola_text7_scope_namespace_gate.md) checks whether text no. 7 itself solves the M-77 conflict. It does not. Parpola text no. 7 is source-located as standardized `M-2109/M-2111`, but local `M-2109/M-2111`, the H companion rows, `M-35`, and `M-77` do not align as exact strings. Next useful work is a Parpola/Mahadevan/Lipi/Mayig sign-list bridge for text no. 7, M-35, M-77, and the H controls.
- [Parpola text no. 7 feature namespace bridge gate](parpola_text7_feature_namespace_bridge_gate.md) executes that bridge check at the sign-list level. Parpola 1994 Fig. 5.1 visually anchors article sign `60` as fish-form, `107` as comb/rake-like, and `189` as spear/arrow-like. Mayig feature metadata blocks the numeric shortcuts: `V060`, `M060`, `V107`, `M107`, local M-35 `107`, `V189`, `M189`, M-77 `861`, local `415`, and local `016` all point to other catalog families or remain source-gated. Local `220 -> P050` is a bounded fish-form candidate for article sign `60`, not an accepted crosswalk.
- [Lipi 034 M-1206 H-938 same-object source panel audit](lipi_034_m1206_h938_same_object_source_panel_audit.md) tightens the strongest H-938 pressure case. Source panel `A/A bis` maps to local `1818.1 +520-220-415+`, with `A bis` only a duplicate photo, while panel `B` maps to companion `1818.2 +034-700+`. This is source-visible within-object proximity pressure, not identity: it strengthens the sign-inventory problem but accepts no `034=415`, value, or translation.
- [Lipi 034 M-1206 415 companion context inventory](lipi_034_m1206_415_companion_context_inventory.md) checks the cherry-pick risk around H-938. Exact local `+520-220-415+` has 17 rows across 16 objects; four rows/objects have same-object `+700-034+` or `+034-700+` companions: `H-319`, `H-938`, `H-939`, and `H-1284`. Only `H-938` is currently source-panel-audited clean. The pattern is repeated enough to prioritize source acquisition, but not enough to accept identity, allography, value, or translation.
- [Lipi 034 M-1206 H-319/H-1284 source-route recheck](lipi_034_m1206_h319_h1284_source_route_recheck.md) executes that acquisition triage. `H-319` is confirmed as a CISI India data/register route only, with byte-identical `n406/n837` pages and no inscription panel. `H-1284` remains source-route dark in the checked public CISI 1/2 layer, with Parpola 2019 only a secondary clue. Both remain acquisition targets, not evidence.
- [Lipi 034 M-1206 H-319/H-1284 source acquisition packet](lipi_034_m1206_h319_h1284_source_acquisition_packet.md) converts the route failure into action. Gmail `19e6376f912f32dc` was sent to Harappa requesting source-grade all-side material for `H-319 / 10060544` and `H-1284 / -458`. The packet defines object, side, visual-diagnostic, direction/order, and independence gates, and adds source-admissibility overrides so old local/model rows cannot silently become evidence.
- [Lipi 034 M-1206 H-938 B component probe](lipi_034_m1206_h938_b_component_probe.md) checks whether the source-visible H-938 companion side supports component-level `034/415` allography. It does not: the vertical B-side component resembles `415`, but candidate `034` under local `R/L` order is the right loop/cross component. H-938 stays same-object proximity pressure only.
- [Lipi 034 M-1206 allograph decision gate](lipi_034_m1206_allograph_decision_gate.md) records the post-side-policy hypothesis state. The exact `+520-220-X+` frame has `415` repeated 17 times and `034` as a singleton, so frequency cannot decide the branch. The admissible evidence creates real allograph/sign-split pressure but does not prove any explanation. The next source-normalized experiment must recut clean M-37 terminals, acquire/source-classify M-1912, keep H-786/H-941 side-gated, and add only classifiable independent `034` witnesses.
- [Lipi 034 M-1206 M-37 terminal recut gate](lipi_034_m1206_m37_terminal_recut_gate.md) executes the M-37 cleanup. `M37_A_terminal_strict_core_from_signband.png` promotes M-37 to clean isolated same-site `415` control, with the minimal signband crop as isolation check. The cleaned M-37 terminal is a comb/rake-with-stem subform, not the closest M-1206 vertical-bundle match, so this strengthens fine-form/subtype pressure rather than proving `034=415`.
- [Lipi 034 M-1206 M-1912 source gate](lipi_034_m1206_m1912_source_gate.md) executes the missing-control admissibility check. `M-1912 +520-220-003+` remains the correct same-site terminal control target, but current evidence is local metadata plus secondary RMRL/Bhaskar visual/catalogue leads and a CISI 3.1 route. It stays out of the clean component packet until CISI 3.1 or equivalent raw source is inspected.
- 2026-05-26 acquisition update: Omar Khan connected Cuper to Andreas Fuls, and Gmail `19e62f703c027ef0` asks specifically for M-1912 photo/plate/side/transcription records plus secondary M-1206 side confirmation. This improves the acquisition route, not the evidence grade.
- [Lipi 034 M-1206 K-150/H-942 singleton controls source gate](lipi_034_m1206_k150_h942_singleton_controls_source_gate.md) checks the other exact `+520-220-X+` singleton terminals. `H-942 +520-220-016+` upgrades to source-visible on CISI Pakistan `n374` with side-mapping caution; `K-150 +520-220-006+` remains secondary/catalogue-only. The next component sort should include H-942 as a negative singleton control, not K-150.
- [Lipi 034 M-1206 source-normalized component packet](lipi_034_m1206_source_normalized_component_packet.md) executes that sort. The blind packet confirms the stable M-1206 vertical terminal core and keeps H-938 A/A bis as the closest clean exact-side `415` pressure, while downgrading H-942 to full-signband control only and keeping M-37 as a distinct comb/rake subform. It preserves a bounded `034/415` terminal-frame question, but the later H-938/H-910 companion-side probes block direct component identity. No allograph, value, or translation is accepted.
- [Lipi 034 M-1206 H-910 component probe](lipi_034_m1206_h910_component_probe.md) runs the mirror-order source check after H-938 B. `H-910 B +700-034+` has left loop/leaf plus right vertical/rake; under local `R/L`, `034` again maps to loop/leaf and `700` to vertical/rake. This is negative pressure against direct `034/415` allography, not a reading.
- [Lipi 034 M-1206 H-938/H-910 direction sensitivity gate](lipi_034_m1206_h938_h910_direction_sensitivity_gate.md) clamps that result to its real evidence level. Under recorded local `R/L`, direct `034=415` is negative; under forced `L/R`, the assignment flips. The next gate is direction/order validation, not a translation claim.
- [Lipi 034 M-1206 direction policy provenance](lipi_034_m1206_direction_policy_provenance.md) traces recorded `R/L` to Lipi/Yajnadevam `dir.` metadata rather than source-image inference. Treat `R/L` as a working corpus policy until source notes or independent `034/032/033/700` controls validate it.
- [Lipi 034 M-1206 independent direction controls gate](lipi_034_m1206_independent_direction_controls_gate.md) checks source-visible `H-930 B`, `H-789 B`, and `H-942 B` controls. Recorded `R/L` is component-coherent across them because `700` lands on the vertical/bar component, but this is still not source-grade direction proof.
- This does not satisfy the full experiment because every mapping remains `uncertain` until image or authoritative sign-list validation.

### E0.3 Artifact Authenticity And Completeness Filter

Question: Which inscriptions are safe for core analysis?

Pass:

- Core set excludes modern fakes, questionable private-collection items, damaged text without uncertainty encoding, and records lacking provenance.

Fail:

- Core statistics change materially when questionable artifacts are removed and this is not reported.

Current prototype result:

- [Mismatch collation queue](mismatch_collation_queue.md) classified the 29 count-mismatch rows into 10 `P1_source_image_required`, 12 `P2_standard_manual_review`, and 7 `P3_policy_check_candidate` rows.
- The queue does not clear any mismatch row. It defines the manual collation work needed before the core set can expand.

## Phase 1: Structural Replication

### E1.1 Directionality Replication

Question: Can reading direction be recovered from compression, sign crowding, edge damage, and known seal/sealing logic?

Pass:

- Model predicts accepted direction for high-confidence cases and flags ambiguous cases.

Fail:

- Direction is assumed globally without artifact-specific handling.

### E1.2 Entropy And Compression Baselines

Question: Does the script behave more like language, administrative notation, emblem systems, or mixed systems?

Baselines:

- Real written languages.
- Known nonlinguistic emblem corpora.
- Administrative accounting tokens or seal formulae where available.
- Synthetic systems with Zipfian frequency, positional rigidity, repeated formulae, and bigram dependencies.

Pass:

- Indus statistics are compared against strong nonlinguistic and mixed baselines, not strawmen.

Fail:

- Entropy alone is used to claim "language."

Current prototype result:

- [Lipi synthetic comparator baseline](lipi_synthetic_comparator_baseline.md) compared the duplicate-collapsed broad `lipi` numeric-clean planning layer against four strong synthetic nonlinguistic controls.
- Edge-position, edge-frame, and position-slot controls nearly reproduce stored-order asymmetry: observed stored win share is 0.948276, while the strongest slot/edge controls average 0.936235 to 0.939385.
- This weakens stored-order asymmetry as a diagnostic by itself.
- The same controls do not reproduce bidirectional masked-sign prediction. Observed bidirectional top-1 is 0.325865, while null means range from 0.098096 to 0.143747 across the four controls.
- [Lipi structured null comparator](lipi_structured_null_comparator.md) adds duplicate-calibrated administrative and emblem code generators. These explicit dependency systems exceed observed bidirectional masked-sign prediction: administrative register mean 0.472114, emblem formula mean 0.441719, and mixed admin-emblem mean 0.416074 versus observed 0.325865.
- This weakens bidirectional masked-sign top-1 as a standalone language-like diagnostic.
- This still does not satisfy the full experiment because the run uses a T3 planning source, five deterministic iterations per control, and artificial generators rather than real known-script or archaeology-grounded comparator corpora.

### E1.3 N-Gram And Markov Replication

Question: Can prior n-gram and Markov findings be reproduced on cleaned corpora?

Pass:

- Replicates sign order constraints and masked sign prediction better than frequency-only baselines.

Fail:

- Performance disappears under corpus cleanup or site-held-out splits.

Current prototype result:

- [Direction and order baseline](direction_order_baseline.md) ran on the 138-row clean open subset.
- Observed order beat reversed order in 130 of 137 rows longer than one sign.
- The result survived removing the two most frequent signs, `740` and `002`, in 114 of 134 rows longer than one sign.
- Bidirectional masked-sign top-1 accuracy was 0.283422, above frequency at 0.098930 and position at 0.159091.
- This does not yet satisfy the full experiment because the subset is all Mohenjo-daro `SEAL:S` and has no authoritative image validation.
- [Lipi broad order baseline](lipi_broad_order_baseline.md) extends the same kind of structural scout to the filtered `lipi` planning layer. Stored order beats reversed order in 2,748 of 2,887 strict numeric-clean rows, and bidirectional masked-sign top-1 accuracy is 0.408323 versus 0.106221 for frequency. Held-out type/site tests remain above simpler baselines.
- [Lipi deduplicated order baseline](lipi_dedup_order_baseline.md) collapses exact duplicate sequences. Stored order still beats reversed order in 1,705 of 1,798 collapsed rows, while bidirectional masked-sign top-1 drops to 0.325865. This shows the order lead is not just exact duplicates, but exact-sign prediction remains duplicate/formula-sensitive.
- [Lipi leakage-controlled held-out baseline](lipi_leakage_control_baseline.md) removes exact train/test sequence overlap from the duplicate-collapsed held-out tests. Selected bidirectional scores remain above simple baselines, including `SEAL:S` 0.283740, `TAB:B` 0.305853, Harappa 0.271129, and Mohenjo-daro 0.297402, with `test_sequence_seen_share` equal to 0 in all reported rows.
- [Lipi high-frequency edge removal baseline](lipi_edge_removed_baseline.md) removes the top edge signs from every sequence before exact duplicate collapse. Removing the top 10 edge signs lowers bidirectional masked-sign top-1 to 0.222222, still above frequency at 0.072383, position at 0.088449, and length-position at 0.092508; stored order still beats reversed order in 1,383 of 1,530 rows longer than one sign.
- [Lipi formula-family downweighting baseline](lipi_family_downweight_baseline.md) downweights shared edge frames and one-edit neighborhoods. Top-10 edge removal plus one-edit-family collapse leaves bidirectional masked-sign top-1 at 0.224004 versus 0.070659 for frequency, but the one-edit families are large and require manual interpretation.
- [Lipi synthetic comparator baseline](lipi_synthetic_comparator_baseline.md) shows that simple stored-order asymmetry is largely reproducible by edge/slot synthetic controls, while duplicate-collapsed bidirectional masked-sign prediction remains above those controls.
- [Lipi structured null comparator](lipi_structured_null_comparator.md) shows that duplicate-calibrated nonlinguistic systems with explicit local dependencies can exceed observed duplicate-collapsed bidirectional masked-sign prediction.
- This still does not satisfy the full experiment because `lipi` is T3, stored order is not accepted reading order, family-collapse rules and null generators are artificial stress tests, and no image-level validation is present.

### E1.4 Network Syntax Replication

Question: Do sign co-occurrence networks reveal stable functional neighborhoods?

Pass:

- Communities are stable across bootstrap samples, corpus variants, and artifact classes.

Fail:

- Communities mainly reflect site, damage, or data-entry conventions.

### E1.5 Prior-Work Pressure Matrix

Question: Are prior claims actually shaping the experiments, or only being cited after the fact?

Pass:

- Every imported prior claim becomes a local support, downgrade, kill, or acquisition requirement.
- Prior work can weaken a live candidate rather than only decorate it.

Fail:

- A prior paper is treated as authority without a local falsification route.

Current prototype result:

- [Lipi FRAME700 034 prior research pressure probe](lipi_frame700_034_prior_research_pressure_probe.md) maps Rao/Yadav order dependency, Farmer/Sproat/Witzel repetition pressure, Sproat metric skepticism, Meadow/Kenoyer source-context demands, Daggumati/Revesz direction/allograph risk, Rao 2018 administrative-use framing, and Nair 2026 synthetic-baseline pressure onto the live `034` candidate.
- The result keeps `034` alive as a no-H-series distributional residue: under the harsh type+sides+order+context+relation block, observed `034` recall is `0.677419` versus null p95 `0.548387`.
- The same pressure matrix blocks overclaim: all `034` order is split (`700_first` 101, `700_last` 13), public source-grade row hits are still 0, and the candidate is Harappa tablet-bound in the current layer.
- [Lipi FRAME700 034 matched contrast stability](lipi_frame700_034_matched_contrast_stability.md) separates source independence from local minimal-contrast strength. It finds 13 strong local contrast triads, but 0 that are both strong local contrasts and low-repetition targets. This forces a two-lane source plan: one independent low-copy batch and one repetition-pressured local-contrast stress batch.
- [Lipi FRAME700 034 two-lane source packet](lipi_frame700_034_two_lane_source_packet.md) converts the split into 27 participant rows, 22 core source objects, 3 optional repeated-branch objects, and 51 row-level coding rows.
- [Lipi FRAME700 034 local contrast public lead audit](lipi_frame700_034_local_contrast_public_lead_audit.md) checks the local contrast lane against the public web layer. It finds 0 source-grade public row hits; H-353 and H-925 have only secondary textual leads in Parpola 2019.
- [Lipi FRAME700 034 long context substitution](lipi_frame700_034_long_context_substitution.md) tests longer-side token and exact-family association by shuffling contexts within matched `034/033/032` triads. It finds 0 corrected token tests and 0 corrected exact-family tests, demoting longer-context claims to source-check leads.
- [Lipi FRAME700 034 source route audit](lipi_frame700_034_source_route_audit.md) turns the source packet into acquisition routes. It finds nine IA CISI scan locator hits, three direct/public-table identity leads, twelve CISI 3.1 route objects, and three request-only objects after exact IA OCR checks. The next action is to fill source coding fields from those located plates, not to run another source-blind statistical pass.
- [Lipi FRAME700 034 IA CISI page locator](lipi_frame700_034_ia_cisi_page_locator.md) locates all nine IA OCR-hit objects at page level. It emits 11 page rows and 27 hits, making H-771/H-789, H-893/H-925/H-930, H-983/H-353, H-212, and optional H-910 page-addressable for manual source inspection.
- [Lipi FRAME700 034 IA CISI visual inspection](lipi_frame700_034_ia_cisi_visual_inspection.md) performs the first manual source-page pass. It finds eight visual plate objects, one register-only object, three clean two-panel locators, and five objects where source panel count or variants block a clean packet upgrade. This turns source inspection into an adversarial filter rather than a rubber stamp.
- [Lipi FRAME700 034 clean two-panel close-read](lipi_frame700_034_clean_two_panel_close_read.md) close-reads H-930 and H-789. Both survive as clean source-visible two-panel controls for object identity, panel count, and short-vs-long side calibration. Neither independently validates `032`/`033` subtype, direction, physical side order, function, phonetic value, or translation.
- [Lipi FRAME700 034 messy panel reconciliation](lipi_frame700_034_messy_panel_reconciliation.md) applies that same close-read standard to H-771, H-893, H-925, H-983, and H-353. All five fail clean upgrade because the source pages expose extra photo labels, extra side categories, unresolved numbered labels, or same-side `bis`/`ter`/`quater` photographs where the local packet has two rows. This is a concrete negative source result: the `034` residue remains live, but these lanes cannot be upgraded until variant/copy notes and extra sides are reconciled.
- [Lipi FRAME700 034 CISI variant convention probe](lipi_frame700_034_cisi_variant_convention_probe.md) tightens that negative result from CISI's own publication rules. `bis`, `ter`, and `quater` are same-side photograph labels, not extra physical sides; `A/B/C` are side categories. The next real source work is object-specific catalog-note reconciliation for `H-893 (1) A/B` and `H-925 (1)/(2) A/B`, plus C-side policy reconciliation for `H-983` and `H-353`.
- [Lipi FRAME700 034 source note and panel graph](lipi_frame700_034_source_note_panel_graph.md) performs that object-note route probe against the accessible IA CISI vol. 1/2 OCR. It finds plate-label hits but 0 object-specific notes for the current blockers, while the volumes themselves route detailed object data to the detailed catalogue/vol. 3 layer; external bibliographic checks point next to CISI 3.1 end matter. The resulting source-normalized panel graph has two useful calibration controls (`H-789`, `H-930`) and 0 substitution-ready `032/033/034` lanes.
- [Lipi FRAME700 034 source panel graph](lipi_frame700_034_source_panel_graph.md) expands the source-normalized check from the three current lanes to all 93 matched `034/033/032` triads. It emits 34 source panel nodes and 14 local-to-source edges from the IA/CISI inspection layer, then scores every triad for substitution admissibility. Result: 0 source-normalized substitution triads, with 75 missing source panel nodes, 12 blocked by panel/variant status, 5 blocked by register-only locators, and 1 blocked by visual-locator-only status.
- [Lipi FRAME700 034 neighbor family pressure](lipi_frame700_034_neighbor_family_pressure.md) uses the local filtered metadata to check whether the same blocked objects are isolated or embedded in repeated/copy-family contexts. `H-925` shows exact copy-family pressure, `H-353` shows high repetition-family pressure, and `H-771`, `H-789`, `H-893`, `H-930`, `H-983`, and `H-2211` show H-number local-neighborhood pressure; only `H-1123` remains low-copy/isolated in this pass. This sharpens source retrieval but does not validate any substitution.
- [Lipi FRAME700 034 CISI 3.1 route recheck](lipi_frame700_034_cisi31_route_recheck.md) stores a fresh eight-row public-source route table. It confirms that CISI 3.1 is the Mohenjo-daro/Harappa supplement and that its end matter is the concrete place to look for excavation, owner/museum, and photograph-source data, while also recording the negative access fact that the full image corpus is not freely downloadable from the public web. This turns `H-893`, `H-925`, `H-983`, `H-353`, and `H-2211` into specific CISI 3.1/end-matter requests.
- [CISI 3.1 access acquisition routes](cisi31_access_acquisition_routes.md) turns the CISI 3.1 route into an active acquisition lane: 14 route rows across bibliography/content, secondary range, library, bookseller, and distributor paths, plus sent Tiedekirja request `19e5f05e8752244a`, Tiedekirja reply `19e5f34b614ce407` confirming a hardbound EUR 118.25 shipped route and no digital form, and sent invoice/payment-link request `19e5fbf666770e04`. This is source access only.
- [Lipi FRAME700 034 CISI 3.1 end-matter request packet](lipi_frame700_034_cisi31_endmatter_request_packet.md) converts that route into a 48-row source-acquisition dataset: 9 core target rows, 17 exact-family comparator rows, and 22 local-neighborhood comparator rows across 47 unique objects. It makes `H-925` a family request with `H-326/H-924`, makes `H-353` a repeated-family request with 15 exact comparanda, and keeps neighborhood comparanda for `H-771`, `H-893`, `H-983`, and `H-2211` as contamination controls.
- [Lipi FRAME700 034 CISI 3.1 request team review](lipi_frame700_034_cisi31_request_team_review.md) stores the source-research, linguistic, and adversarial review of that packet. It requires exact subentry/side-label meanings, side-order and direction basis, source-visible `032/033/034` stroke separation, copy-family independence, and clean HARP/CISI/local-row alignment before any contrast can be treated as linguistic evidence.
- This does not satisfy the full experiment because source images, real nonlinguistic comparators, and external corpus access are still incomplete.

## Phase 2: Functional Classes

### E2.1 Positional Grammar Discovery

Question: Are there stable prefix, core, connector, pre-terminal, terminal, numeral, and metrological positions?

Methods:

- Hidden Markov models.
- Bayesian sequence segmentation.
- Minimum-description-length grammar induction.
- Manual epigraphic comparison for high-impact classes.

Pass:

- Learned classes predict held-out sign positions and match known structural observations.

Fail:

- Classes are unstable across corpora or only work after hand-picking examples.

Current prototype result:

- [Structural sign classes](structural_sign_classes.md) derived positional profiles under raw numeric, isolated `P385` merge, and observed Parpola policies.
- `740/P324` is a dominant initial-operator candidate.
- `002/P122`, `220/P050`, and `032/P145` are medial/core candidates.
- `817/861/P385` is a terminal-operator candidate cluster.
- `390/P086` is a distributed recurrent candidate rather than a simple initial or medial sign.
- [Formula pattern probe](formula_pattern_probe.md) found directional edge-class scaffolding: raw numeric signs have 22 observed `I...T` scaffolds versus 1.25 under within-row shuffling, while observed Parpola signs have 23 versus 1.25.
- Exact formula recurrence is still weak, which blocks semantic interpretation from these class patterns alone.
- [Formula variant probe](formula_variant_probe.md) found one exact duplicate under the Mayig policy, 75 near-pairs with edit distance <= 2, 14 edge-frame families, and 3 single-slot candidate groups.
- [Formula variant null model](formula_variant_null_model.md) found that the variant queue is strong under a loose length/frequency shuffle but mostly explained by first/last sign position under an edge-position preserving shuffle. These remain triage outputs until image/source validation and broader corpus replication.
- [Sensitivity formula probe](sensitivity_formula_probe.md) tested the 12 flagged count-matches and found no recurrent exact formula patterns, 0 raw `I...T` scaffolds, and only 1 Mayig `I...T` scaffold involving `P000`.
- This does not satisfy the full experiment because the classes have not yet survived larger corpora, image validation, artifact-class splits, or metadata prediction.

### E2.2 Allograph And Variant Testing

Question: Which visual variants are the same sign?

Pass:

- Merges improve predictive structure and are supported by visual, positional, and distributional evidence.

Fail:

- Merges are chosen because a desired phonetic reading needs them.

Current prototype result:

- [Sign policy sensitivity](sign_policy_sensitivity.md) compared raw numeric signs, an isolated `817`/`861 -> P385` merge, provisional high-consistency mappings, provisional high+medium mappings, and observed `mayig` Parpola strings.
- The order signal survived all tested policies.
- The isolated `P385` merge improved bidirectional masked top-1 accuracy from 0.281461 to 0.307172.
- This does not satisfy the full experiment because the merge is not image-validated and may benefit from label collapse.

### E2.3 Artifact-Class Split

Question: Do seals, tablets, pottery marks, tags, and long signboards use the same grammar?

Pass:

- The system identifies shared and class-specific structures.

Fail:

- A single grammar is forced across incompatible artifact types.

Current prototype result:

- [Metadata scope probe](metadata_scope_probe.md) found that the current open Mayig prototype contains only unicorn seal descriptions.
- Therefore no artifact-class split or cross-iconography test is possible yet from the Mayig subset.
- [Lipi broader scope probe](lipi_broader_scope_probe.md) found a broader T3 planning layer: 2,887 strict numeric-clean candidates and 3,308 direction-clean candidates after removing claim columns, with enough raw breadth for sealings, tablets, reverse seals, pottery marks, and site splits.
- [Lipi broad order baseline](lipi_broad_order_baseline.md) shows the filtered broad layer can support first scout baselines across artifact type and site, including held-out evaluations.
- [Lipi deduplicated order baseline](lipi_dedup_order_baseline.md) shows those scout baselines must be reported with exact-duplicate collapse and cross-split overlap controls.
- [Lipi leakage-controlled held-out baseline](lipi_leakage_control_baseline.md) applies the first cross-split overlap control and keeps selected artifact/site held-out scores above simple baselines, but it does not yet control near-duplicate formula families.
- [Lipi high-frequency edge removal baseline](lipi_edge_removed_baseline.md) shows edge signs are a major driver across these scout baselines, but selected type/site held-out scores remain above simple baselines after top-10 edge removal.
- [Lipi formula-family downweighting baseline](lipi_family_downweight_baseline.md) applies edge-frame and one-edit-family controls, including after top-10 edge removal. Selected artifact/site held-out scores remain above simple baselines, but the largest one-edit families are too broad to treat as real formula classes without manual review.
- This does not satisfy the full experiment because `lipi` is not authoritative. It can propose split designs; M77/CISI/ICIT or image validation must decide whether the splits are admissible.

## Phase 3: Semantic Anchoring

### E3.1 Metadata Prediction

Question: Can sign sequences predict site, region, material, artifact class, iconography, or completeness better than chance?

Pass:

- Predictions beat strong baselines on held-out sites and artifact classes.

Fail:

- Model memorizes high-frequency site-specific seals.

Current prototype result:

- [Lipi metadata prediction probe](lipi_metadata_prediction_probe.md) collapsed the broad `lipi` numeric-clean layer to 1,798 exact sign-sequence families and tested leave-one-out metadata prediction against family-level structured nulls.
- Observed token prediction scores include type 0.633492, site 0.654284, region 0.638717, and class 0.543312.
- Type/site/region are confounded by artifact-type mixtures. The mixed admin-emblem null reaches type 0.644458, site 0.649731, and region 0.642994.
- Material and direction are majority-dominated and do not provide useful evidence in this pass.
- The strongest surviving scout result is inscription `class`: observed token prediction is 0.543312 with macro-F1 0.474895, while structured null token accuracies range from 0.270359 to 0.289452.
- [Lipi stratified class probe](lipi_stratified_class_probe.md) tested `class` prediction within 11 eligible site, artifact-type, and type-site strata. Observed token prediction beats every structured-null control in every eligible stratum; the minimum observed-minus-null mean gap is 0.08.
- [Lipi class robustness probe](lipi_class_robustness_probe.md) attacked the `class` result with top-10 edge-sign removal and formula-family downweighting. Edge-sign removal alone does not erase class prediction, with top-10 edge-removed Token NB around 0.474 to 0.477. The harshest combined top-10 edge-removal plus one-edit-family policy drops Token NB to 0.372236 accuracy and 0.228813 macro-F1. This still beats majority, but raw accuracy is matched or exceeded by length/edge-frame controls.
- [Lipi class field audit](lipi_class_field_audit.md) found no upstream definition-like text for the `class` abbreviations in 67 scanned `yajnadevam/lipi` repository files. Several labels are near-proxies for length, site, type, or completeness: for example `TS` is 98.8095 percent length 1, `VN` is 98.5915 percent Harappa and 94.6479 percent length 2, and `UC` has zero numeric-clean rows.
- [Lipi class proxy-control probe](lipi_class_proxy_control_probe.md) removed proxy-heavy labels and shuffled labels within length/type/site blocks. Under the strict proxy >= 0.65 removal screen, Token NB is 0.643089 versus a length+type+site block-shuffle null mean of 0.322154. This shows the source field tracks sign structure beyond simple row metadata, but because the field is undefined it is best interpreted as source-internal coding or circularity.
- [Lipi semantic anchor target audit](lipi_semantic_anchor_target_audit.md) moves the next metadata work away from `class`. Candidate targets with enough exact-sequence-collapsed label coverage include `symbol`, `cult`, `material`, `shape`, `boss`, `type`, and coarse dimension bins. None are clean by default; they all require proxy-blocked controls because labels are tangled with object form, direction, material, site, type, cult fields, or edge-frame structure.
- [Lipi semantic anchor prediction probe](lipi_semantic_anchor_prediction_probe.md) prediction-tested those candidate fields under blocked label-shuffle nulls. No candidate target is clean enough for semantic interpretation. `symbol`, `cult`, `material`, `boss`, and `thickness_bin` are matched or exceeded by their hardest Token NB nulls, while `shape`, `type`, and dimension-bin residues are small and close to edge-frame-preserved nulls.
- This does not satisfy the full experiment because `lipi` is T3, `class` is now downgraded to an unverified source-code field, the new semantic-anchor candidates failed the first blocked-null pass, and nothing has been repeated on authoritative or image-validated data.

### E3.2 Numerical And Metrological Binding

Question: Can numerical signs be connected to standardized weights, measures, quantities, or administrative tiers?

Pass:

- Proposed numerical/metrological classes predict artifact measurements, reverse-side tablet marks, or context.

Fail:

- Numerical readings explain only isolated examples.

Current prototype result:

- [Lipi dimension residue stress probe](lipi_dimension_residue_stress_probe.md) tested coarse dimension bins after the semantic-anchor probe left tiny size residues. The broad run derives fresh positional sign classes from 1,798 exact-sequence-collapsed families and compares Token NB against hard metadata shortcuts and edge/edge-class blocks.
- The result blocks broad metrological interpretation. For `vertical_bin`, Token NB is 0.465507 against an exact edge-frame null mean of 0.449037, but length+type+site reaches 0.627098 and material+shape reaches 0.597265. Metadata shortcuts beat sign-token prediction for every dimension-bin target.
- [Lipi multi-side mark scope probe](lipi_multiside_mark_scope_probe.md) isolates a better side-mark review queue. In 864 multi-side or multi-row CISI groups, there are 539 clean short-mark candidate rows and 558 clean longer-text rows. The short-mark queue is dominated by Harappa `TAB:I` and `TAB:B`; top tokens are `700`, `033`, `034`, `032`, `003`, `861`, and `156`.
- [Lipi multi-side mark stratified probe](lipi_multiside_mark_stratified_probe.md) splits the queue inside Harappa `TAB:B` and Harappa `TAB:I`. The queue survives both strata: `TAB:B` has 222 short-mark rows led by `700`, `034`, `033`, and `032`; `TAB:I` has 269 short-mark rows led by `700`, `034`, `033`, `003`, `861`, and `156`. The sharpest new validation target is the `TAB:I` row side index 3 concentration around `003` and `156`.
- [Lipi multi-side mark validation queue](lipi_multiside_mark_validation_queue.md) converts the stratified result into 397 artifact groups for source/image validation. It separates 22 Harappa `TAB:I` three-side all-short tablets from 205 mixed short-long artifacts. Kenoyer and Meadow 2010 externally anchors H-2218 through H-2239 as a 22-object rectangular steatite tablet group, triangular in section, from Period 3B secondary deposits, while leaving the tablet function unresolved.
- [Lipi short-mark orientation audit](lipi_short_mark_orientation_audit.md) checks two-token `700` companion marks in Harappa `TAB:B`/`TAB:I`. `700` appears first in 313 rows and last in 55. Corrected balance tests survive for `032`, `033`, and `034`; TAB:I versus TAB:B orientation differences survive FDR correction for `032` and `033`; side-index orientation checks do not survive correction. This makes exact short-mark order mandatory in validation.
- [Lipi short-mark context orientation audit](lipi_short_mark_context_orientation_audit.md) tests whether reversed core `700` companion marks also carry distinct longer-row contexts. It keeps 353 `032`/`033`/`034` rows, emits 57 Fisher exact context checks, and finds no corrected context flags. Reversal remains an orientation/source-validation variable, not a functional contrast.
- [Lipi short-mark companion context audit](lipi_short_mark_companion_context_audit.md) tests whether the companion tokens `032`, `033`, and `034` bind to distinct longer-row contexts after preserving `type|700_order` blocks. It emits 90 tests and finds two corrected catalog-side relation flags: `033` is overrepresented in `short_after_all_longer` rows and `034` is underrepresented there. This sharpens plate-validation priorities but accepts no side function or reading.
- [Lipi short-mark side-relation validation sheet](lipi_short_mark_side_relation_validation_sheet.md) converts that contrast into 251 row-level source-validation targets across 250 artifacts. The first plate request set is 17 unique artifacts where the corrected `033`/`034` side-relation contrast overlaps the raw `+400-740-176+` longer-context hint.
- [Lipi short-mark plate request packet](lipi_short_mark_plate_request_packet.md) converts those 17 artifacts into a manual validation packet with blank evidence fields and explicit outcome codes. This is the first artifact-level handoff from statistical planning to plate/source inspection.
- [Lipi short-mark plate public lead search](lipi_short_mark_plate_public_lead_search.md) checks 20 public endpoints for those 17 artifacts. It finds candidate image/post leads for H-233, H-1302, and H-1303; published direction/corpus-note leads for H-1302 and H-1303; text-only or bibliographic leads for ten artifacts; and no public lead in the checked sources for H-1304, H-1344, H-1345, H-1346, and H-1347. This sharpens source acquisition but does not validate any side relation.
- [Lipi short-mark source acquisition queue](lipi_short_mark_source_acquisition_queue.md) ranks those 17 source actions. The first pass should acquire or inspect H-1302/H-1303, H-355, H-933/H-960, and H-233 before spending effort on the source-dark and replicate `033` cases. This is still E3.2 source acquisition, not a numerical or metrological test.
- [H-233 public slide visual lead audit](h233_public_slide_visual_lead_audit.md) manually checks the H-233 public post image URLs. It keeps one H-233-relevant slide as a low-grade visual pointer and rejects one H-1997 slide as an H-233 image-lead false positive. This improves source targeting and gives a correction rule for page-level image sweeps.
- [H-1302/H-1303 direction-note recheck](h1302_h1303_direction_note_recheck.md) confirms that the Nature 2021 allograph article is a direction/corpus-correction lead for both objects, while the public Blogger images remain unlabeled or contextual. The next action is still CISI/HARP source acquisition, not interpretation.
- [H-1302/H-1303 source provenance gate](h1302_h1303_source_provenance_gate.md) verifies the actual Nature PDF/HTML and the visible page passage behind that lead. This turns the lead into a source-located published correction claim for `H-1302`, `H-1303`, and `H-1822`, while still rejecting any upgrade to local `+700-033+` validation, side order, sign correction, or reading before CISI/HARP/ICIT reconciliation.
- [H-1302/H-1303 CISI public route check](h1302_h1303_cisi_public_route_check.md) rules out public CISI Pakistan vol. 2 as the source-panel route: its Harappa photograph scope ends at `H-1019`, and exact OCR target hits for H-1302/H-1303 are absent. The next experiment is source-holder acquisition through CISI 3.1, HARP, or ICIT/Wells-Fuls notes.
- [H-355 double-short-side clarification audit](h355_double_short_side_clarification_audit.md) checks the only double-short-side packet case. Public evidence remains text-only through the `H-352-357 (incised)` range/list mention, with no H-355 object-level image found in the checked public searches. The next action is a three-side CISI/HARP source request that checks both `+700-033+` rows independently.
- [H-933/H-960 034 contrast source audit](h933_h960_034_contrast_source_audit.md) checks the two `034` contrast packet cases. Public evidence remains text-only through the `H-933, 936, 960, 964, 308, and 312-314 (incised)` range/list mention, with no object-level image found for either object in the checked public searches. The next action is a paired CISI/HARP source request that preserves `+034-700+` versus `+700-034+`.
- [H-1304/H-1344/H-1347 source-dark direct request audit](h1304_h1344_h1347_source_dark_direct_request_audit.md) checks the five source-dark `033` after-longer packet objects. Fresh public-web searches find no object-level image, plate, caption, or useful text-only lead for H-1304, H-1344, H-1345, H-1346, or H-1347. The next action is a direct two-side CISI/HARP/archive request, not more broad public searching.
- [Lipi TAB:I mixed 400-740-176 side-context audit](lipi_tab_i_mixed_400_740_176_side_context.md) isolates 26 mixed short-long `TAB:I` artifacts where `+400-740-176+` occurs with `+700-033+` or `+700-034+`. The queue contains 20 long-side-1/short-side-2 pairs, 4 reversed two-side pairs, one double-short-side case, and one three-side extra-long-text case. This means side order must be validated explicitly before any functional comparison.
- [Lipi TAB:I mixed 400-740-176 dimension probe](lipi_tab_i_mixed_400_740_176_dimension_probe.md) runs a pre-validation check on those 26 artifacts. `+700-033+` versus `+700-034+` shows weak raw all-target exact p values for horizontal measurement and aspect ratio, but no emitted test survives Bonferroni or Benjamini-Hochberg correction, and the canonical long-side-1/short-side-2 subset weakens the signal. The result only prioritizes plate/source validation; it does not support a numerical or metrological interpretation.
- [H-2218 through H-2239 series validation sheet](h2218_h2239_series_validation_sheet.md) isolates that 22-object series with HARP object IDs, figure references, local side texts, and pending plate checks. It identifies 13 main-signature objects, 7 local side-order variants, H-2237 as a `154`/`156` visual check, and H-2238 as a `033`/`034` visual check.
- [H-2218 through H-2239 Fig. 4 mapping](h2218_h2239_fig4_mapping.md) maps the 22 local rows to Meadow and Kenoyer 2000 Fig. 4 item numbers and manufacturing groups. The source manufacturing groups do not collapse to local side-order classes: every group contains mixed local signatures or variants.
- [H-2218 through H-2239 Fig. 4 visual availability audit](h2218_h2239_fig4_visual_availability_audit.md) records coarse public-PDF coverage for all 22 tablet items. Three side panels and a triangular/end-profile marker are visible for every mapped row, but the image is not adequate for segmentation, allography, stroke counts, or side orientation.
- [H-2218 through H-2239 dimension side-order probe](h2218_h2239_dimension_side_order_probe.md) compares available measurements against local side-order signatures and manufacturing groups. The canonical A versus side-swap split is not strongly separated by horizontal size, vertical size, area, or aspect, while the manufacturing groups do show measurement structure. This blocks a simple size-only explanation of A versus side-swap, but still requires image-level side validation before functional interpretation.
- [H-2218 through H-2239 side-order confound probe](h2218_h2239_side_order_confound_probe.md) tests whether the same local split is just manufacturing-group distribution or published Fig. 4 order. The canonical group-distribution check gives `p >= observed = 1.000000`, B-B adjacency across canonical Fig. 4 order gives 0.683243, group-count-conditioned B-B adjacency gives 0.438889, and coarse A/B/variant blockiness gives 0.173416. This weakens those two easy confounds without accepting physical side order.
- [H-2218 through H-2239 side-role template probe](h2218_h2239_side_role_template_probe.md) sharpens the local split into two catalog-side templates. All 22 rows have one `+861-003+` side, one `+700-03x+` side, and one `+15x-003+` side. The `+15x-003+` role is always local side 3, while the other two roles swap across local sides 1 and 2. This turns the next plate check into a precise falsification target: is local side 3 a real repeated physical side, a catalog convention, or an image-ordering artifact?
- [H-2218 through H-2239 slot grammar reconstruction](h2218_h2239_slot_grammar_reconstruction.md) hides each side once and asks whether the other two sides reconstruct the missing role and exact text. Role family is recovered in 66/66 cases; exact-text role-majority reconstruction is 64/66, with the only failures being H-2237 `+154-003+` and H-2238 `+700-033+`. This isolates the two singleton variants as source-validation targets, not readings.
- [H-2218 through H-2239 template recurrence audit](h2218_h2239_template_recurrence_audit.md) searches that three-role template across all 397 validation-queue rows. Strict and unordered policies both find 0 non-H complete matches, and 0 non-H near matches with even two of the three role families. This means the H-series template should be treated as series-specific until stronger source data expands it.
- [H-2218 through H-2239 minimal contrast packet](h2218_h2239_minimal_contrast_packet.md) isolates the two single-object variants inside group 3/template `700|861|15x`. It emits four same-group/same-template/single-slot contrast rows. The strongest local pair is `H-2237/H-2233`, which has exact dimensions `10 x 6.5` and differs only in side 3 `+154-003+` versus `+156-003+`. `H-2238` gives the matching `+700-033+` versus `+700-034+` side-role contrast against `H-2230/H-2233`. These are the best current minimal-contrast source targets, not readings.
- [H-2218 through H-2239 minimal contrast team review](h2218_h2239_minimal_contrast_team_review.md) keeps the claim boundary tight: `H-2237` and `H-2238` are two separate singleton slot-variant tests, not one paired contrast. It requires full group-3 controls, source-confirmed physical side positions, diagnostic stroke visibility, damage/photo-quality status, and HARP/CISI/Fig. 4/local-row alignment before either can be used for sign-function inference.
- [H-2218 through H-2239 minimal contrast public source probe](h2218_h2239_minimal_contrast_public_source_probe.md) checks the public source layer for `H-2230`, `H-2233`, `H-2237`, and `H-2238`. Exact HARP IDs anchor all four to Meadow and Kenoyer 2000 Fig. 4 nos. 17-20, but the checked public layer gives 0 source-grade image hits and 0 object-level public image hits for these minimal-contrast objects.
- [H-2218 through H-2239 group 3 source route recheck](h2218_h2239_group3_source_route_recheck.md) expands the source layer for the four group-3 target/control objects. It finds 0 public source-grade image hits, 0 object-level public image hits, and 0 direct archive target hits, but it records exact acquisition routes through Harappa image request, CISI 3.1 plates/end matter, Finna library holdings, and HARP object/photo database access.
- [H-2218 through H-2239 group 3 Harappa image request](h2218_h2239_group3_harappa_image_request.md) turns that acquisition route into a sent Gmail request to Harappa's published contact email. It requests exact all-side images, CISI plate references, source notes, direction and side-order basis, diagnostic visibility, copy/workshop notes, and permission terms. This is an acquisition action only.
- [H-2218 through H-2239 variant localization null](h2218_h2239_variant_localization_null.md) tests whether the two singleton variants are broad or local. `H-2237` and `H-2238` are both in group 3, both in `template_700_861_15x`, and adjacent in Fig. 4. Under unordered pair nulls over the 22 objects, both being in group 3 plus that template has probability 0.025974; also being adjacent there has probability 0.012987. This makes workshop/template-local confounding stronger, not weaker.
- [H-2218 through H-2239 variant external distribution](h2218_h2239_variant_external_distribution.md) checks the two singleton slot failures against the full filtered `lipi` planning layer. `700_033` is broadly supported with 151 adjacent rows, 150 outside the H-series, and 124 strict external exact rows; `154_003` is sparse but real, with four adjacent rows, three outside the H-series, and one strict external exact row at `H-366`. This keeps both variant questions alive while making the next test source-image adjudication, not more source-blind scoring.
- [Lipi 154/156 comparanda packet](lipi_154_156_comparanda_packet.md) ranks the sparse `154_003` rows against the `156_003` pool and checks overlap-crosswalk pressure. It keeps `H-2237/H-2233` as the strongest local source test, makes `H-366` the strict external exact support row, identifies `M-102/M-132` as the best longer-text external pressure pair, and records that both lipi `154` and `156` align to Mayig/Parpola `P004` in the current overlap layer. This turns allograph/crosswalk collapse into an explicit falsification branch.
- [Lipi variant crosswalk pressure](lipi_variant_crosswalk_pressure.md) separates the two singleton variant failures into different source tasks. `154/156` has `P004` collapse pressure and needs diagnostic-stroke image adjudication. `033/034` does not currently collapse in the clean overlap: `033 -> P147`, while `034` is crosswalk-dark and needs sign-list/source coverage before any merge or distinction can be claimed.
- [Lipi 034 crosswalk darkness diagnostic](lipi_034_crosswalk_darkness_diagnostic.md) verifies that the `034` darkness is upstream of the crosswalk: 182 broad filtered `lipi` rows contain exact `034`, but zero current Mayig-overlap rows do. Fuller Mayig/Parpola coverage or authoritative sign-list mapping should target both the Harappa tablet-heavy `034` branch and the Mohenjo-daro `034` rows outside the current overlap.
- [Lipi 034 Mayig acquisition targets](lipi_034_mayig_acquisition_targets.md) checks that the public Mayig head remains `m184` and ranks exact `034` acquisition targets. The first crosswalk acquisition lane is now `M-2104`, `M-315`, `M-1206`, `M-685`, `M-1584`, and `M-1963`; the 21 H-series `+700-034+` objects remain source-image controls for `H-2238`.
- [Lipi 034 P0 public lead search](lipi_034_p0_public_lead_search.md) turns that acquisition lane into concrete source actions. The immediate crosswalk extraction target is `M-2104`, where Parpola 2019 gives text no. 12 as `UIII` plus signs 15 and 1. `M-315` routes to CISI 1 p. 78, `M-1206` routes through a Bhaskar Fig. 3 CISI image, `M-685` is visible in Bhaskar S1, and `M-1584`/`M-1963` remain source-dark.
- [Lipi 034 M-1206 terminal triad source recheck](lipi_034_m1206_terminal_triad_source_recheck.md) is now the active non-M2104 P0 image route. It has already verified direct CISI pages for `M-37` and `M-1206`, including the `M-1206 e(1)` companion side. The required next action is no longer broad source scraping: perform a blind outer-sign classification on the stored source crops, align A/a with local `R/L`, and keep `M-1912` quarantined until raw CISI 3.1 or equivalent source is available.
- [Lipi 034 M-1206 M-1912 source gate](lipi_034_m1206_m1912_source_gate.md) is the current missing-control result. It confirms `M-1912` is a high-priority `003` acquisition target for the same-site `M-1912/M-1206/M-37` triad, but rejects using the RMRL/Bhaskar figure as source-grade evidence. The next action is exact CISI 3.1/equivalent object lookup, not more public scraping.
- 2026-05-26 update: Andreas Fuls source route is now active via Omar Khan's introduction; request `19e62f703c027ef0` is sent. Wait for source/photo response or CISI 3.1 access before admitting M-1912.
- [Lipi 034 M-1206 K-150/H-942 singleton controls source gate](lipi_034_m1206_k150_h942_singleton_controls_source_gate.md) is the current wider singleton-control result. It adds source-visible `H-942 A` as a cautious `016` control and keeps `K-150` out until a raw source page is acquired. This makes the next sort a real sign-inventory packet rather than a 034-vs-415-only echo chamber.
- [Lipi 034 M-1206 source-normalized component packet](lipi_034_m1206_source_normalized_component_packet.md) is the current M-1206 visual decision result. It runs the real source-normalized blind packet with H-942 included only as a full-signband singleton control and M-1912/K-150 excluded. Next useful work is source acquisition or an independent classifiable `034` witness, not broader packet growth.
- [Lipi 034 M-1206 H-938 same-object source panel audit](lipi_034_m1206_h938_same_object_source_panel_audit.md) is the next local control tightening: it records the exact source-panel relation between `H-938 A/A bis +520-220-415+` and companion `H-938 B +034-700+`, keeping the evidence as proximity pressure rather than a sign collapse.
- [Lipi 034 M-1206 415 companion context inventory](lipi_034_m1206_415_companion_context_inventory.md) adds the immediate anti-cherry-pick control: the `034/700` companion beside exact `+520-220-415+` repeats locally in `H-319`, `H-938`, `H-939`, and `H-1284`, but only H-938 is clean source-audited now.
- [Lipi 034 M-1206 H-319/H-1284 source-route recheck](lipi_034_m1206_h319_h1284_source_route_recheck.md) resolves the next two local repeats as acquisition targets only: `H-319` is a register-page route, `H-1284` is still route-dark, and neither can be used as source-grade recurrence before plate-grade all-side evidence is acquired.
- [Lipi 034 M-1206 H-319/H-1284 source acquisition packet](lipi_034_m1206_h319_h1284_source_acquisition_packet.md) is now the live external acquisition action for those repeats. Wait for Harappa/source reply before upgrading; otherwise continue with independent source-visible `034` witnesses.
- [Lipi 034 M-1206 H-938 B component probe](lipi_034_m1206_h938_b_component_probe.md) is a negative internal check on the best same-object pressure case. Next useful work should find an independent source-visible `034` component with unambiguous component assignment, not lean harder on H-938 B.
- [Lipi 034 M-1206 / M-37 blind visual orientation](lipi_034_m1206_m37_blind_visual_orientation.md) is now the active non-M2104 P0 visual result. It blocks a premature terminal-substitution claim and replaces it with a fine-form binning task: source-visible `034/415` outer signs must be sorted blind across more comparanda before any allograph, subtype, separate-sign, or function claim is allowed.
- [Lipi 034 M-1206 / M-37 415 comparanda scout](lipi_034_m1206_m37_415_comparanda_scout.md) provides the first source-visible `415` comparison pool.
- [Lipi 034 M-1206 / M-37 415 fine-form binning](lipi_034_m1206_m37_415_fine_form_binning.md) turns that pool into verified crop evidence plus blind review. Use `H-938 A/A bis` and `H-940 A` as the cleanest exact-side candidates for now; keep `H-786/H-941` quarantined behind unresolved side-to-local-row mapping and `H-939` behind visibility failure. The follow-on data-register pass shows why this is a language/source problem, not a filename problem: H-786 gives AV 775 without assigning sign strings to sides, and H-941 gives A/B plate references without assigning those sides to local `1821.1/.2`. Do not mix Harappa tablets with Mohenjo-daro seals as one evidence unit without explicit controls.
- [Lipi 034 M-2104 Parpola extraction](lipi_034_m2104_parpola_extraction.md) converts the `M-2104` lead into a falsifiable source-image test: verify whether `034` is the three-stroke count component in `700-034`, opposed to `004` as the four-stroke count component in `700-004`, while `097` carries Parpola sign 15. This is now the first P0 `034` image target, ahead of broader source-blind scoring.
- [Lipi 034 M-2104 source route probe](lipi_034_m2104_source_route_probe.md) stores the image routes needed for that falsification test: CISI India leaf 150 for `M-478/M-480`, CISI Pakistan leaf 227 for `M-1425`, and CISI Pakistan leaves 324/325/122/80/119 for `H-543/H-544/M-915/M-715/M-896`. The next E3.2 work is cropping and comparing the visible tablet clusters, not running another generic score.
- [Lipi 034 M-2104 visual stroke probe](lipi_034_m2104_visual_stroke_probe.md) performs that first crop pass and turns it into a 15-row segmentation target sheet. It keeps the `700-034`/`700-004` count hypothesis alive for segmentation because `M-478` and `M-1425` visibly carry the expected four-stroke/U-pot-like regions, but it accepts no mapping or meaning.
- [Lipi 034 M-2104 blind visual adjudication](lipi_034_m2104_blind_visual_adjudication.md) narrows the live gate: the public four-stroke parallel side survives provisionally, so the next E3.2 action is to acquire/check raw `M-2104` for the corresponding three-stroke target before any mapping can be accepted.
- [H-2219 public image lead audit](h2219_public_image_lead_audit.md) records three low-resolution public image leads labeled h2219A/B/C. They are useful for targeting higher-resolution plate requests and checking side-label conventions, but not for accepting segmentation, side orientation, or meaning.
- [H-2218 through H-2239 public image-lead search](h2218_h2239_public_image_lead_search.md) expands the public lead search across 66 possible A/B/C labels for the 22-object series. The checked RSS/blog pages expose object-level image URLs only for H-2219, so the other 21 tablets still require CISI plates, HARP images, or archive access.
- The next numerical/metrological test should validate these short side marks against images or stronger side metadata, then compare them against measurements, artifact type, row side index, longer text tokens, and known metrological comparators.

### E3.3 Iconography Link Test

Question: Do animal and cult symbols constrain adjacent signs?

Pass:

- Associations survive site controls and artifact-type controls.

Fail:

- The same sign is assigned incompatible meanings depending on famous iconography.

Current prototype result:

- [Lipi semantic anchor target audit](lipi_semantic_anchor_target_audit.md) found that iconography-like targets are available in the filtered `lipi` planning layer: `symbol` has 952 eligible exact-sequence families across 10 labels, and `cult` has 783 eligible families across 5 labels.
- [Lipi semantic anchor prediction probe](lipi_semantic_anchor_prediction_probe.md) blocks naive iconography. `symbol` Token NB is 0.276261, below majority at 0.310924 and below the hard-proxy null mean at 0.283613. `cult` Token NB is 0.605364, below majority at 0.633461 and below the type-block null mean at 0.610047.
- This is a negative iconography-link result for the current T3 planning layer. It does not rule out real iconographic structure; it says the current broad metadata route is dominated by object-form and catalog proxies.

### E3.4 Administrative-Semantic Scope Test

Question: Are seals/tablets best modeled as tax, licensing, trade/craft, commodity, access-control, ownership, ritual, or mixed records?

Pass:

- A semantic-scope model predicts object distribution, duplicate inscriptions, sign classes, and archaeological context.

Fail:

- It cannot outperform generic "name/title" or "clan emblem" baselines.

## Phase 4: Linguistic Hypothesis Testing

### E4.1 Candidate Language Prior

Question: Which language families are even plausible under archaeology, chronology, and substrate evidence?

Candidates:

- Proto-Dravidian or lost Dravidian branch.
- Para-Munda or lost substrate.
- Elamite or areal contact language.
- Unknown isolate or multilingual administrative system.

Pass:

- Candidate priors are documented before lexical matching.

Fail:

- Language choice is reverse-engineered from attractive sign readings.

### E4.2 Rebus False-Positive Control

Question: Do rebus readings beat random language dictionaries and phonological flexibility controls?

Pass:

- A reading must explain a class of inscriptions and beat shuffled signs, shuffled meanings, and unrelated language lexicons.

Fail:

- A single pun is treated as decipherment.

### E4.3 Proper-Name And Title Test

Question: Are inscriptions names, titles, institutions, commodities, ritual formulae, or mixed administrative records?

Pass:

- Proposed category predicts distribution and duplicate behavior.

Fail:

- Every inscription is made into a name/title because ancient scripts often contain names.

## Phase 5: Translation System

### E5.1 Layered Translation Prototype

Question: Can the system produce useful translations without overclaiming?

Output layers:

- Corpus text.
- Normalized sign string.
- Structural parse.
- Semantic field.
- Candidate readings.
- Competing explanations.
- Confidence.
- Counterexamples.

Pass:

- Users can see exactly why the system says what it says.

Fail:

- It emits polished English sentences without evidence.

### E5.2 Calibration Benchmark

Question: Does confidence mean anything?

Pass:

- High-confidence structural predictions are correct more often than low-confidence predictions on held-out tests.

Fail:

- Confidence reflects narrative appeal.

### E5.3 Ancient Egyptian Comparator

Question: What would the same system do on a known ancient script under artificial scarcity?

Design:

- Take Egyptian, Sumerian, or Linear B corpora.
- Downsample to Indus-like inscription lengths and corpus sizes.
- Remove bilingual labels.
- Test how much structure and semantics can be recovered.

Pass:

- Gives a realistic ceiling for what IVC can achieve with current evidence.

Fail:

- We compare IVC to full Egyptian translation without controlling for corpus advantage.

Current acquisition result:

- [Known-script scarcity comparator acquisition audit](known_script_scarcity_comparator_acquisition_audit.md) chooses Linear B Series D as the first known-script scarcity comparator, Coptic SCRIPTORIUM as the continuity upper bound, and SumTablets as the later large administrative comparator.
- [Linear B Series D scarcity baseline](linear_b_series_d_scarcity_baseline.md) executes the first structural-only known-script comparator and gives an initial hidden-reading ceiling.

### E5.3a Linear B Series D Scarcity Baseline

Question: Under IVC-like blindness, how much structure can be recovered from a known deciphered logo-syllabic administrative script?

Inputs:

- Zenodo Linear B Series D dataset, DOI `10.5281/zenodo.7404653`.
- Default clean rows: first 513 real Series D sequences.
- Excluded by default: 725 augmented rows and 1,327 duplicate rows.

Pass:

- Emits a source manifest, parsed row-range inventory, Indus-like length/downsample policy, structural-only scorecard, and ceiling statement.

Fail:

- Uses known Mycenaean Greek readings, lexical values, translations, augmented rows, or duplicate rows without declaring that condition.

Current prototype result:

- [Linear B Series D scarcity baseline](linear_b_series_d_scarcity_baseline.md) acquired and verified the Zenodo `Samples.txt` source, with MD5 `0c9b9190b86840c82cafdbf4f4b8c827`.
- The clean default uses 513 real Series D rows; 725 augmented rows and 1,327 duplicate rows remain excluded by default. A separate 513-row gapped test section was detected but not used.
- Under primary hidden-reading `sign_tokens`, bidirectional masked-sign top-1 is 0.470200 on all clean rows and 0.435897 after the current IVC p95 length cap of 8 signs.
- The matching position-slot null means are 0.136725 and 0.141961, so the bidirectional structural signal survives simple null controls.
- The source-provided gapped test has now been run. All 513 gapped rows contain exactly one aligned synthetic gap. Under sequence-leave-one-out, bidirectional top-1 is 0.294347 all-lengths and 0.294314 under the IVC p95 length cap, with median rank 3.
- This satisfies the first source-manifest, scout scorecard, and gapped held-out version of E5.3a, but not the final comparator program. Remaining work: stronger sign-ID tokenization, SumTablets replication, and comparison only after IVC source validation.

### P0 Source Bridge: Parpola Sign 60 / Local 220

Question: Can local Lipi `220` be promoted from fish-form candidate to Parpola article sign no. `60`?

Current result:

- [Parpola sign 60 / local 220 fish bridge probe](parpola_sign60_local220_fish_bridge_probe.md) strengthens the candidate but keeps the crosswalk unaccepted.
- [Parpola sign 60 / local 220 middle-crop probe](parpola_sign60_local220_middle_crop_probe.md) runs the first neutral visual packet. M-37, H-938 A, and H-940 A survive broad fish/leaf-family compatibility; H-942 A does not upgrade; article sign `60` specifically is still unaccepted.
- [Strict Parpola sign 60 / local 220 fish-family gate](parpola_sign60_local220_strict_fish_family_gate.md) adds nearby fish-family controls. Result: two of three reviewers block a sign-specific threshold; S009/M-37 is strongest pressure, but the safe accepted result remains broad fish/leaf-family compatibility only.
- Next admissible experiment: acquire clean source-visible Mayig `P050` visual examples and higher-quality local `220` crops where internal decoration can be judged.
- Pass condition: local `220` crops remain closest to plain sign `60` controls after nearby fish-family and source-visible `P050` controls are included.
- Fail condition: local `220` remains only broad-family compatible, or specific fit depends on damaged/low-contrast crops.

### P0 Formula Campaign: `520-220`

Question: Is `520-220` a fixed formula stem with a productive terminal slot, and what linguistic function does that stem have?

Current result:

- [520-220 formula stem campaign](campaign_520_220_formula_stem.md) moves the object from one-sign `220` adjudication to a whole formula family.
- The campaign stores 67 total `520-220` bigram occurrences, 59 opening occurrences, 4 clean exact `+520-220+` rows, 21 exact `+520-220-X+` rows, and 52 broad `^+520-220-X` rows.
- Exact `+520-220-415+` has 17 rows and currently ranks second among exact three-sign formulas.
- Harappa is standardized around terminal `415`; Mohenjo-daro carries most terminal diversity.

Next campaigns:

- `520-*` opener campaign: decide whether `520` is a broad opener/classifier or whether `520-220` is the true compound.
- `*-220-*` neighbor campaign: decide whether `220-415` is the real unit or whether `520` is required.
- Exact triplet source packet: compare all 17 `415` exact rows against singleton `003`, `006`, `016`, and `034`.
- Companion branch campaign: test whether terminal `X` predicts `700-034`, `700-032`, `700-033`, or `110` companion classes.

Pass condition:

- `520-220` predicts its terminal distribution better than either `520` alone or `220` alone, singleton terminals survive source-grade visual checks, and terminal `X` predicts companion-side behavior after site/type control.

Fail condition:

- `415` tracks `220` without needing `520`, singleton terminals collapse into source/catalog noise, or all apparent structure disappears after Harappa/Mohenjo-daro and tablet/seal stratification.

Current campaign result:

- [Unit boundary campaign: `520`, `220-415`, or `520-220`](campaign_unit_boundary_520_vs_220.md) executes the first two controls.
- Best current parse: `520-H-C`, where `520` opens a frame, slot 2 is a head, and slot 3 is a head-conditioned closure/complement.
- `520-220-415` is the strongest branch, but `220-415` remains portable outside `520`.
- The enrichment of `415` after `520-220` is Harappa/TAB:I-heavy, so site/type controls are mandatory.

Next immediate campaign:

- `A-220-X` frame campaign: compare `520-220-X`, `318-220-X`, `740-220-X`, `845-220-X`, row-start `220-X`, `000-220-X`, and `176-220-X`.
- Pass condition: different previous signs before `220` select different terminal distributions after site/type controls.
- Fail condition: `220-415` remains stable across previous signs, sites, and object types, making `A` mostly peripheral.

Current result:

- [A-220-X frame selection campaign](campaign_a_220_x_frame_selection.md) confirms frame-conditioned terminal selection.
- Productive candidates: `520-220-X`, `740-220-X`, and especially compact `240-220-032`.
- Local/family-confounded candidates: `318-220-415`, `740-220-055`, `176-220-235`, and small `845-220-415`.
- Artifact-heavy zones: row-start `220-X` and `000-220-X`.
- [A-220-X strict dedupe and companion campaign](campaign_a_220_x_strict_dedup_companion.md) completes the immediate strict pass. The post-dedupe ranking is now `240-220-032` first, productive `520-220-X` second, and `740-220-003` third. Raw `740-220-055`, `318-220-415`, `176-220-235`, and `845-220-415` are quarantined as local formula/source-family cases.
- [A-220-X 240 selector contrast](campaign_a_220_x_240_selector_contrast.md) executes the statistical first cut. In strict frame-text dedup units, `240 -> 032` is 9/12 versus non-`240` 46/239; in matched site/type/frame/text blocks it is 9/12 versus 35/150. The signal survives no-companion filtering but is strongly carried by Mohenjo-daro `SEAL:S`. Tail profiling shows 7/9 target rows continue after `032`, so `032` cannot yet be called an ending.
- [032 after 220 function campaign](campaign_032_after_220_function.md) executes the slot-function follow-up. It rejects `032` as an ending after `240-220` because only 2/9 targets are terminal. It shows `A-220-032` has a strong `002` continuation lane, while outside `A-220-X` `032` is a mixed start/700/740-heavy population with much lower next-`002` pressure. The next live object is `A-220-032-002-Y`.
- [032-002 tail campaign](campaign_032_002_tail.md) executes that next layer. It shows that combined `A-220-032` enters next `002` in 24/55 dedup units versus outside `032` at 16/257, and core `002-861/820/817` in 16/55 versus 8/257. The working function model is now `A-220-032 -> 002 -> Y`: `002` as tail-lane marker candidate and `861/820/817` as a compact ending family. `240` remains an entry selector into the `032` construction, not yet a proven controller of the Y slot.
- [032-002-Y leave-one-block campaign](campaign_032_002_y_leave_one_block.md) tests the load-bearing Mohenjo-daro `SEAL:S` block. Removing that block weakens absolute rates but does not collapse the contrast: strict `A-220` next `002` remains 6/28 versus outside 12/387, and core terminal tails remain 5/28 versus 6/387. The accepted next object is `A-220-032-002-{861,820,817}` as a short continuation/closure formula; the broad script-level Y closure-class claim is demoted until source-clean row behavior decides it.
- [032-002-Y source route probe](campaign_032_002_y_source_route_probe.md) converts the 25-row source-function manifest into acquisition lanes. Source-volume OCR rows first: `H-444`, `M-375`, `M-174`, `M-221`, `H-597`, `M-21`, `M-1385`, `M-49`, and `M-722`. Chanhu-daro plate rows next: `C-10`, `C-60`, `C-65`. Eleven rows have local source-reference routes, and only `K-145` / `H-140` are direct-route-needed at this stage.
- [032-002-Y source-function batch 1](campaign_032_002_y_source_function_batch1.md) starts the source-volume lane. `M-722` target `002-817` and `H-444` non-240 control `002-861` are now row-level source-visible from Pakistan source pages. `M-1385` outside control is object-visible but side/local-row gated because the source page has multiple faces.
- [032-002-Y source-function batch 2](campaign_032_002_y_source_function_batch2.md) adds `M-49` target non-core `002-300`, `M-21` outside `002-861`, `M-375` non-240 `002-820`, and `H-597` outside `002-861` as row-level source-visible witnesses. It explicitly rejects `M-174` and `M-221` as source-function evidence for now because their current OCR hits are data/prose pages, not inscription panels.
- [032-002-Y source-function batch 3](campaign_032_002_y_source_function_batch3_chanhudaro.md) executes the Chanhu-daro lane. `C-10` upgrades non-240 `002-817`; `C-60` upgrades outside `002-861`; `C-65` remains target `002-861` acquisition-needed because Mackay's public Plate LII scan is too dark for row evidence.
- [032-002-Y branch model](campaign_032_002_y_branch_model.md) replaces the loose "core ending family" wording with `A-220-032 -> 002 -> branch`. Current source-clean rows make `002-861` the strongest portable branch, put `002-820` only in non-240 A-220 so far, put `002-817` in target and non-240 A-220, and make `002-300...` a target extended branch.
- [032-002-Y token-box scaffold v1](campaign_032_002_y_token_box_scaffold_v1.md) boxes provisional `032/P145`, `002/P122`, and Y in the eight current source-visible anchor rows. The scaffold does not die as catalog adjacency, but `M-375`, `H-597`, and `C-60` need stronger crop/image work before token-level evidence is high-confidence.
- [032-002 context branch campaign](campaign_032_002_context_branch_campaign.md) widens the unit to every adjacent `032-002` context. It finds 50 adjacent rows, 34 strict complete rows, and 32 strict dedup units. The key change: strict `target_240_220_032` has four rows and four different Y values (`300`, `817`, `820`, `861`), so `240-220-032` selects entry into the `032-002` lane but does not determine the branch. `861/820/817` remain the best compact branches, but the construction is broader than that family.

Next immediate campaign:

- `032-002-Y` branch campaign: first fill the source-clean target `820/861` cells and outside `817/820` cells, then test the other-Y A-220 singleton branch values.
- Immediate scaffold fixes: wider right-edge recut for `M-375`; improved dark-background crop for `H-597`; better image for `C-60`.
- Highest value target rows after scaffold boxing: better `C-65` target terminal `002-861`, `M-1728` target `002-820`, and `M-240` target extended `002-861-603`.
- Highest value outside rows: `H-140` or resolved `M-1385` for outside `002-817`, plus `M-1677` or `M-1045` for outside extended `002-820`.
- Cross-site non-240 A-220 row: `K-145` tests `002-820` outside Mohenjo-daro.
- Other-Y A-220 controls: `M-636`, `M-1686`, `M-130`, `M-1159`, `M-36`, `H-1657`, and `M-1667` test whether `{861,820,817}` is special or just a sampled part of broader `002-Y`.
- [032-002 post-Y continuation campaign](campaign_032_002_post_y_continuation_campaign.md) is now complete as the first branch-behavior pass. It finds that all-`002` strict dedup behavior splits `817/820/861` from continuation-heavy `390/368/031/220/900/300`; inside adjacent `032-002`, `817` is hard closure, `820/861` are leaky closures, and `390/300` continue.
- [032-002-Y matched terminality campaign](campaign_032_002_y_matched_terminality.md) is now complete locally. `y_class` beats `site/type/symbol` in both the 499-row all-`002` strict dedup layer and the 32-row adjacent `032-002` layer, and produces 47 all-`002` matched blocks plus 17 adjacent matched blocks.
- Mechanic validation: PASS. Hostile constraint: because `y_class` is terminality-informed, the result must survive a source-boxed, family-blocked, right-edge-matched holdout before it can be treated as strong branch grammar.
- Next immediate linguistic campaign: post-Y tail-family test. Cluster the continuation material after `861`, `820`, `390`, `300`, and singleton branches to see whether the tails are licensed chunks, administrative code, or row residue.
- [032-002 post-Y tail family campaign](campaign_032_002_post_y_tail_family_campaign.md) is now complete locally with mechanic validation PASS. The all-`002` field shows recurrent tail pressure after `390` (`125`, `705`), `220` (`455`, `065`), and `861` (`603`, `533-717`), while adjacent `032-002` tails are mostly singletons.
- Next immediate source-normalization campaign: inspect `M-240`, `M-91`, `M-1677`, `M-49`, and `M-70`/unknown `390` continuations so the terminal/continuation classes are not just catalog-order artifacts.
- [032-002 source-normalized branch-tail admissibility](campaign_032_002_source_normalized_branch_tail_admissibility.md) is now complete locally with mechanic validation PASS. The decisive adjacent queue is six rows; only `M-49` is currently source-boxed. `M-240`, `M-91`, and `M-1677` have local source-reference routes but need images; `M-70` needs source routing; the unknown `390-590-032` row needs object-ID resolution.
- [032-002 branch-tail source acquisition](campaign_032_002_branch_tail_source_acquisition.md) upgrades the decisive queue: `M-240`, `M-91`, and `M-70` now have public CISI India source-panel routes and stored A/a crops. The source-visible decisive continuation set is now `M-49`, `M-240`, `M-91`, and `M-70`, which makes leaky `861` continuation and branch-head `390` continuation image-backed hypotheses. `M-1677` remains the missing `820` continuation route, and unknown `3335.1` remains object-ID blocked.
- [032-002 branch-tail linguistic model](campaign_032_002_branch_tail_linguistic_model.md) is now the controlling research model for this cluster. Current parse: `[left frame]-032-002-Y(-tail)`, with `002` as a post-`032` branch introducer candidate and Y as the closure/branch selector. Highest-value next campaigns: source-token branch cluster (`M-49`, `M-240`, `M-91`, `M-70`), `861` suffix split, `390` branch-head family, `820` missing-cell acquisition, and recursive later-`032` tails.
- [032-002 branch-tail token/order adjudication](campaign_032_002_branch_tail_token_order.md) completes the first source-token cluster pass. `M-49`, `M-240`, `M-91`, and `M-70` all preserve source-visible same-line continuation at order level. The next campaign should be the `861` suffix split, not another source-route audit: compare `M-240/M-91` against all-`002` `861->603` rows (`M-1273`, `M-714`) and `861->533-717` rows (`M-376`, `M-391`).
- [032-002 861 suffix-split campaign](campaign_032_002_861_suffix_split.md) is now complete as a grammar campaign. Strict dedup `002-861` gives 119 rows, 95 terminal and 24 continuing; adjacent `032-002-861` gives 9 rows, 7 terminal and 2 continuing. The strict repeated tails are `603` x3 and `533-717` x2; raw duplicate-family pressure preserves `416` x6 and `698` x2. Four new public CISI source routes were added for `M-376`, `M-391`, `M-714`, and `M-1273`, joining prior `M-240`/`M-91`. Working promotion: `861` is no longer just a compact ending candidate; it is a closure-capable branch sign with testable restricted-tail behavior.

Next immediate campaign:

- `861` suffix-attachment test: extract every occurrence of `603`, `533-717`, `255-416`, `416`, and `698`; decide whether these tails occur independently, after other closure signs, or preferentially after `861`.
- Source-token check only where it matters: isolate spacing around `861` in `M-240`, `M-91`, `M-376`, `M-391`, `M-714`, and `M-1273`; kill the suffix model if source panels show fusion, side mismatch, or catalog-order artifact.
- Compare the `861` tails against `390` branch-head tails (`390-125`, `390-705`, `390-692`) so closure-addenda and branch-head complements do not get blurred.
- [032-002 861 tail-attachment campaign](campaign_032_002_861_tail_attachment.md) completes the suffix-attachment scan over 4,135 strict closed rows. `533-717` and `255-416` are restricted to terminal post-`002-861` in this scan; `603` has a real post-`861` terminal use but also an independent `740-603-240...` lane; `416` and `698` are downgraded as restricted post-`861` tails because they are broader terminal/formula chunks. Next action is source-token attachment on only the six rows that can change the parse: `M-376/M-391/M-91/M-240/M-714/M-1273`.
- [032-002 861 source-token attachment campaign](campaign_032_002_861_source_token_attachment.md) executes that six-row source pass. All six rows preserve same-line terminal-side candidates in the public source crops, with no obvious fusion or side split. Strength ranking: `M-1273` strongest for `603`, `M-376/M-391` repeated for `533-717`, `M-91` weak singleton, and `M-714` crowded. The restricted-tail model survives as a candidate, but exact source-normalized `861`/tail boundaries remain unaccepted.
- [032-002 861 matched terminal-controls campaign](campaign_032_002_861_matched_terminal_controls.md) completes the corpus-level contrast against bare terminal `002-861`. Every focus family has bare terminal controls in a relevant block. Strong controls: `220-032-002-861` has 4 bare controls versus `M-91 255-416` and `M-240 603`; `803-002-861` has 2 bare controls versus `M-714 603`; `176-002-861` has 4 bare controls versus `M-376 533-717` and `L-46 392`; Mohenjo-daro `SEAL:S Bull1:S` has 9 bare controls versus `M-91 255-416`. The tailed rows are now countable against a bare background in matched blocks.
- [032-002 861 bare-edge source-controls campaign](campaign_032_002_861_bare_edge_source_controls.md) completes the first source-visible bare-edge packet. Source-visible controls now exist for the three live lanes: `H-444/M-723/M-1044` for `220-032-002-861`, `M-77/M-118` for `803-002-861`, and `M-15` for `176-002-861`. The next unit is no longer one row or one sign. It is a batch model over post-`861` tail families.
- [032-002 861 tail-family batch](campaign_032_002_861_tail_family_batch.md) runs that batch. It promotes `533-717` as the best restricted post-`861` target, keeps `603` as the best mixed post-`861`/independent formula target, treats `255-416` as singleton stress, and downgrades `416/698/000` as restricted-tail evidence.
- [032-002 861 context-split campaign](campaign_032_002_861_context_split.md) turns that batch into the next linguistic decision. `533-717` becomes the P1 restricted post-`861` target because it is terminal, source-visible, no-icon Mohenjo-daro `SEAL:R`, and has no independent strict occurrence. `603` becomes the P1 mixed bridge target because the post-`861` Mohenjo-daro seal uses coexist with the independent Harappa `TAB:B` formula `740-603-240-060-692`. `255-416` remains P2 singleton stress.
- [032-002 861 533-717 register test](campaign_032_002_861_533717_register_test.md) promotes `533-717` to a conditional register/subclass marker candidate. It is rare globally (`2/144` strict `002-861` rows) but concentrated inside no-icon Mohenjo-daro `SEAL:R` with `002-861` (`2/7`) and especially cuboid-convex no-icon `SEAL:R` with `002-861` (`2/3`), while Mohenjo-daro `SEAL:S` with `002-861` has `0/71`.
- [032-002 861 533-717 source controls](campaign_032_002_861_533717_source_controls.md) and [032-002 861 tail rarity register scan](campaign_032_002_861_tail_rarity_register_scan.md) demote the broad register-marker reading. Same-register public controls now include `M-355` with a long alternate tail, `M-1267` bare, and `M-1273` with `603`; the whole strict scan finds 23 post-`002-861` tail families and 20 small perfect-looking register cells. Current live reading: `533-717` is a narrow subclass/apposition candidate, not the marker of no-icon `SEAL:R + 002-861` as a whole.
- [032-002 861 533-717 focus contrast](campaign_032_002_861_533717_focus_contrast.md) runs the seven-row same-register contrast. Shape, text length, and source visibility do not separate `M-376/M-391` from controls; only singleton pre-`002-861` contexts are target-specific. Current live reading: `533-717` is a source-layout/source-family question, not yet a metadata-defined subclass.
- [032-002 861 533-717 source-family independence](campaign_032_002_861_533717_source_family_independence.md) rejects exact duplicate/copy collapse for `M-376/M-391` in the current evidence layer. They differ in source leaf/page, full text, length, local class, excavation identifiers, depth/boss metadata, dimensions, and immediate pre-`002-861` context. Current live reading: two real artifact attestations, one narrow source/register-family cell for linguistic weighting.
- [032-002 861 533-717 source-layout discriminator](campaign_032_002_861_533717_source_layout_discriminator.md) fails the promotion gate. `M-376/M-391` both have same-line terminal-side tail windows, but `M-1273` also has same-line terminal-side post-`861` material, `M-355` is a same-register cuboid-convex long-tail control, and `M-1267` is a same-register bare-edge control. Current live reading: repeated terminal-tail pressure inside one narrow cell, not a unique layout marker.
- [032-002 861 preframe tail comparison](campaign_032_002_861_preframe_tail_comparison.md) tests the immediate pre-`002-861` frames. Target last-2 frames `100-176` and `233-805` are singletons; broader last-1 frames do not isolate `533-717`. Current live reading: preframes are context clues, not values or selectors.
- [032-002 861 post-tail ecology](campaign_032_002_861_post861_tail_ecology.md) widens the unit to all post-`002-861` tails. The field has 144 strict `002-861` rows and 23 tail families: bare `<END>` is dominant, `603` is the mixed post-`861` plus independent bridge, `533-717` is real but one narrow source/register-family cell, `416/698/000` are broad controls, and the rest are source-target singletons. Current live reading: `002-861` is a closure edge with an optional secondary zone; the next translation-relevant object is `603` mobility, not another single-tail audit.
- [032-002 861 603 mobility](campaign_032_002_861_603_mobility.md) executes the first bridge test. `603` occurs seven times in the strict layer: three terminal post-`002-861` Mohenjo-daro seal rows, three Harappa TAB:B rows in exact formula `+740-603-240-060-692+`, and one weak independent scene/control row. Current live reading: `603` is mobile enough to prioritize but too formula-bound on the independent side to read.
- [032-002 861 603 source route](campaign_032_002_861_603_source_route.md) separates source-ready and source-routed evidence. The post-`861` Mohenjo side is source-visible with local crops/overlays for `M-240`, `M-714`, and `M-1273`. The independent Harappa side is only routed through Kenoyer and Meadow 1997 / Vats 1940 references and must be cropped/normalized before it can decide graphic or layout identity.
- [032-002 861 603 slot substitution](campaign_032_002_861_603_slot_substitution.md) runs the immediate `740-X-240-060-692` falsifier. The Harappa X slot has `603` x3, `636` x2, and `642` x2. Only `603` also appears as a post-`002-861` tail initial. Current live reading: `603` survives as a uniquely cross-slot bridge among observed X-slot signs, but remains under copied-template attack.
- [032-002 861 603 source-normalized slot family](campaign_032_002_861_603_source_normalized_slot_family.md) attacks the copied-template objection directly. `603` now has two source-visible Harappa objects (`H-1138` Vats Plate XCIV no. 346 and `H-1846` Kenoyer/Meadow H95-2672) plus one low-weight route-only echo (`H-1137` no. 7537 similar to no. 346). `636` has one source-visible Vats control (`H-360` Plate XCVIII no. 584) and one route-only row; `642` has one public-page route (`H-1845` H2000-4484 Figure 42.05) and one metadata-only row. Current live reading: `603` survives duplicate-row collapse better than before, but formula-family independence and value are still unaccepted.
- [032-002 861 slot-control source routes](campaign_032_002_861_slot_control_source_routes.md) executes the control-side source route check. `H-823/H88-1196` remains exact-route-dark after public CISI IA OCR, local route, and web checks; `H-1845/H2000-4484/2227-15` remains public Harappa.com route-only because shell image download is Cloudflare-blocked and no public CISI OCR route was found; `H-237` is demoted to near-zero independent `642` control weight because it has no excavation route and the current local export marks the SP text as `ref:424.2`. Current live reading: the `603` bridge survives, but the `636/642` controls are source-imbalanced and cannot be treated as fully negative source-balanced controls.

Next immediate campaign:

- Treat `H-237` as non-independent until a source image or excavation route is found; do not use it as a real `642` negative control.
- Acquire/store source-grade control images for `H-823/H88-1196` and `H-1845/H2000-4484 Figure 42.05`; if no public route appears, mark those cells as route-dark/public-page-only and move the linguistic test forward with explicit downweighting.
- Re-tokenize the five-sign source bands for the visible witnesses (`H-1138`, `H-1846`, `H-360`) and the public-page `H-1845` view if a usable crop can be captured, instead of accepting the local numeric sequence blindly.
- [032-002 861 603/636/642 external ecology](campaign_032_002_861_603_636_642_external_ecology.md) is complete. `603` splits between exact Harappa `740-603-240-060-692` and terminal post-`002-861-603`; `636` and `642` stay inside X-before-240 frames and never occur as post-`861` tail initials.
- [032-002 861 X-before-240 bridge ecology](campaign_032_002_861_x240_bridge_ecology.md) is complete. Across 95 X-before-240 rows and 28 X signs, only raw `603` and background/control `000` also appear as immediate post-`002-861` tail initials. Current live question: source-normalize why low-frequency `603` bridges while `636/642` do not.
- [032-002 861 X-before-240 internal subframes](campaign_032_002_861_x240_internal_subframes.md) is complete. The `240-060-692` continuation is a compact subframe: 7 strict rows, all prefix `740`, with X limited to `603/636/642`. This validates the slot-family contrast as a count-supported subframe object and stops treating it as a one-sign hunt.
- [032-002 861 X-before-240 internal subframe interpretation](campaign_032_002_861_x240_internal_subframe_interpretation.md) is complete as the first interpretation pass for that object. It ranks five live explanations: X-slot subconstruction, mobile `603` classifier/addendum, `060-692` subtype frame, homograph/catalog split, and Harappa copied-template artifact.
- [032-002 861 603 graphic identity packet](campaign_032_002_861_603_graphic_identity_packet.md) is complete as the first visual bridge gate. It promotes post-`861` `603` to source-visible terminal-region candidate status, anchored by `M-1273`, but keeps the Harappa bridge unresolved because `H-1138` and `H-360` are still source-visible bands rather than source-tokenized X-slot crops. `M-714` is demoted for fine-form use because the previous tail window split the terminal graphic.
- [032-002 861 603 H-1138/H-360 tokenization gate](campaign_032_002_861_603_h1138_h360_tokenization_gate.md) attempts that visual source test. The positive upgrade fails: under both explicit orientation policies, the candidate `H-1138` X slot does not cleanly match the clean `M-1273` terminal anchor. Current live status: `603` is still distributionally alive but graphically weakened; split-homograph/catalog-conflation and Harappa tablet-template explanations move up.
- [032-002 861 X-before-240 subframe migration](campaign_032_002_861_x240_subframe_migration.md) completes the next distributional campaign. `603` is the only low-frequency non-background X-before-`240` sign that also appears as a post-`002-861` tail initial, but inside X-before-`240` it is locked to `240-060-692` with 3 rows, 1 register cell, and 1 formula family. `636` and `642` are stronger internal-mobility controls: each spans 5 after-`240` continuations. Current live status: the bridge survives distributionally, but Harappa `603` looks narrower than the controls; copied-template and split-homograph/catalog-conflation explanations move up.
- [032-002 861 X-before-240 bridge-lock null](campaign_032_002_861_x240_bridge_lock_null.md) completes the immediate adversarial null. Shuffling X labels across the 95 X-before-`240` rows while preserving X counts and after-`240` subframe sizes gives `P(603 locked anywhere)=0.040000`, `P(603 locked specifically to 060 692)=0.000400`, and `P(any low-frequency non-background bridge sign locked)=0.040000`. Current live status: the bridge-lock pattern is real pressure but not decisive; it does not promote `603` past the failed graphic-identity gate.
- [032-002 861 X-before-240 family-cell bridge audit](campaign_032_002_861_x240_family_cell_bridge_audit.md) completes that stricter register/family-cell null. The 95 raw X-before-`240` rows collapse to 81 family cells; `603` collapses to one Harappa `+740-603-240-060-692+` family cell. The broad single-cell bridge event is not rare (`P(any nonbackground bridge single family cell)=1.000000`), so the row-level 0.04 pressure is demoted to acquisition priority, not decipherment evidence.
- [032-002 861 X-before-240/post-861 bridge cluster scan](campaign_032_002_861_x240_post861_bridge_cluster_scan.md) runs the full family-cell intersection scan. Result: no promoted bridge cluster. The only observed nonbackground intersection is `603`, and it has one X-before-`240` family cell, so it fails the two-cell recurrence gate. Within-side and identity-remap max scans both give `P(max >= observed)=1.000000`; identity-remap produces some fake multi-cell shape-gate candidates (`0.071350`) while the observed packet produces none.
- Immediate decision: stop 603-only active work. Keep `603` only as a source-acquisition watchlist item requiring either clear cross-context graphic identity (`M-1273` terminal equals `H-1138/H-1846` X-slot while `636/642` controls differ) or a second independent non-Mohenjo/non-family `603` context.
- [032-002 861 533-717 component ecology](campaign_032_002_861_533717_component_ecology.md) executes the first post-603 pivot. `533-717` remains a fixed-prefix restricted-tail unit, not a decomposed phrase: independent `533` occurs 0 times outside the pair, while `717` is broad with 37 independent occurrences. Broad no-icon `SEAL:R + 002-861` still contains bare closure, `603`, and long-tail controls, so `533-717` is not the marker of the whole branch.
- [032-002 861 post-861 fixed-tail contrast](campaign_032_002_861_post861_fixed_tail_contrast.md) completes that fixed-tail comparison. Bare `<END>` is the background closure (`113` rows / `110` family cells); `533-717` is the fixed restricted-tail unit (`2` rows / `2` cells); `603` is recurrent as post-`861` tail material but parked from bridge evidence (`3` rows / `3` cells); `255-416` and `360-520-919-140` are source-visible singleton contrasts. The goal remains syntactic class contrast, not value.
- [032-002 861 source-normalized tail predictor packet](campaign_032_002_861_source_normalized_tail_predictor_packet.md) completes the next competing-predictor pass with a 25-row source/contact-sheet packet. Load-bearing results: `220 032` splits into bare, `603`, and `255-416`, so last-two preframe alone is insufficient; Mohenjo no-icon `SEAL:R` splits into bare, `533-717`, `603`, and long-tail behavior, so register alone is insufficient. Current live status: `533-717` is a conditional final-unit candidate, `603` is a recurrent post-`861` class with no value, and the long tail is the strongest same-register adversary.
- [032-002 861 contact-packet visual scoring](campaign_032_002_861_contact_packet_visual_scoring.md) completes the first human/epigraphic score pass. Visual status: `603` is a recurrent Mohenjo post-`861` tail class anchored by `M-1273`; `533-717` survives as a fixed restricted final-unit candidate; `255-416` stays singleton; `M-355` is the key long-tail adversary in the same no-icon cuboid-convex lane; bare controls preserve closure behavior; Harappa controls are visible but not tokenized.
- [032-002 861 533-717 blind layout gate](campaign_032_002_861_533717_blind_layout_gate.md) completes that same-register visual/copy-family gate. `M-376/M-391` preserve comparable terminal-pair layout, so `533-717` survives as a repeated final-unit candidate. It does not promote to function/morphology/value because the target remains one no-icon cuboid-convex cell and `M-355/M-1273` show the same broader lane can take other continuations.
- Next immediate linguistic campaign: leave `533-717` parked as a conditional final-unit comparator and run the post-`861` secondary-zone minimal-contrast search across all 144 `002-861` rows. Target: find any tail class with either a third independent source-visible row, a same-prefix minimal contrast, or tail choice predicted by full preframe after register/source controls. If no such class appears, move up one level from tail identities to typed continuation behavior after `861`.
- Bridge promotion criteria for future packets remain: at least two independent X-before-`240` family cells, at least two independent post-`002-861` tail-initial family cells, at least two signless formula templates, same after-`240` subframe in at least 80 percent of X-before-`240` cells, candidate-specific family-cell null `<= 0.01`, global any-sign null `<= 0.05`, and no single site/register carrying the whole effect.
- Use `533-717` only as a secondary restricted-cell comparator unless it gains a third independent row, a same-prefix minimal contrast, or an independent `533/717` phrase ecology.
- Source-route `M-1954` and `M-1973` only if the contrast still depends on the bare rectangular controls after using `M-1267`.
- Finish pending bare-control routes only where they change that decision: `M-1763`, `M-1880`, `M-1755`, and `M-2060`.
- Negative controls: source-check A-220-032 rows without `002` and outside `032` rows without `002`, matched by site/type when possible.
- Next source-volume/source-function rows: add token-level boxes for `M-722`, `M-49`, `H-444`, `M-375`, `M-21`, and `H-597`; keep `M-174`, `M-221`, and `M-1385` out of source-function counts until panel/side mapping is solved.
- Check whether terminal `A-220-032`, core terminal `A-220-032-002-{861,820,817}`, and extended tails such as `002-861-603` split by source-visible layout or neighbor context.
- Test whether `520-220-016` companion `700_033` pressure survives all-side source labels and object-family controls.

Current post-`861` campaign state:

- [032-002 861 post-861 minimal-contrast search](campaign_032_002_861_post861_minimal_contrast_search.md) is complete with mechanic validation PASS. It ranks the whole 144-row field: `603` is the top source-ready simple-tail cluster, `533-717` is a parked conditional fixed-final comparator, `255-416` is a singleton third arm in the `220-032` cluster, and `416/698` are source-pending acquisition clusters.
- [032-002 861 220-032 source-visible contrast packet](campaign_032_002_861_220032_source_visible_contrast_packet.md) is complete with mechanic validation PASS. It scores the source-visible same-last2 split: `H-444/M-723/M-1044` preserve bare closure, `M-240` preserves a simple `603` tail, and `M-91` preserves a longer `255-416` tail. The sheet is semi-blind because overlay labels leak, so use it for layout behavior only.
- [032-002 861 220-032 register/length kill test](campaign_032_002_861_220032_register_length_kill_test.md) is complete with mechanic validation PASS. Broad register, site, and total length do not cleanly explain the split; fine icon remains singleton-confounded; terminal-space is the live unresolved adversary because bare controls lack the same quantified line metrics as the tailed rows.
- [032-002 861 220-032 terminal-space recut](campaign_032_002_861_220032_terminal_space_recut.md) is complete with mechanic validation PASS. It makes the terminal-space adversary positive: `M-91/M-240` have 195px/120px terminal candidate windows, while `H-444/M-723/M-1044` have only 28-38px marked post-terminal margins. The `220-032` split is preserved as source-visible positional contrast but blocked from grammar-slot promotion.

Next immediate linguistic campaign:

- Do not promote `220-032` to grammar-slot evidence unless a stricter fresh source recut overturns the terminal-space adversary. For forward movement, shift from this narrow split back to the 144-row post-`861` field and hunt a stronger object: same-prefix contrasts, third independent source-ready rows, or typed continuation behavior not explained by terminal margin.
- Keep `533-717` parked unless it gains a third independent source-visible row, an exact/same-prefix contrast, or a stronger independent phrase ecology.
- Keep `603` separated into two questions: post-`861` simple-tail behavior is alive; Harappa X-before-`240` bridge remains parked until cross-context graphic identity or a second independent family cell appears.

Current post-`861` campaign state:

- [032-002 861 post-861 hypothesis tournament](campaign_032_002_861_post861_hypothesis_tournament.md) is complete with mechanic validation PASS. The campaign explicitly demotes one-sign work and ranks the 144-row post-`002-861` field as a typed secondary-zone question. Tail classes are closure `113`, simple single `22`, fixed pair `5`, and long continuation `4`. Preframe features carry more tail-class information than broad register fields, so ranked target lanes are preframe/exact-context lanes: `prefix_last1=032`, `prefix_last2=220 032`, `prefix_last1=176`, empty-prefix `002-861-X`, `prefix_last1=235`, `prefix_last1=031`, and exact-prefix `390 004`. Register fields remain adversarial controls, not targets.

Next immediate linguistic campaign:

- Run a source-visible terminal-space recut across ranked preframe lanes, not only `220-032`; blind the tail class before measuring terminal free slot and sign windows.
- Run whole-formula clustering before the `861` split; kill optional-grammar readings if full left formulas predict the tail.
- Run source-family collapse by tail class; promote only class behavior that survives multiple independent family cells, not individual sign values.
- Route `390 004` only inside an exact-prefix batch, not as a standalone one-sign campaign.

Current post-`861` formula/template state:

- [032-002 861 formula-family collapse attack](campaign_032_002_861_formula_family_collapse.md) is complete with mechanic validation PASS. It confirms that whole-left-formula templates are now the main blocker to grammar promotion. Only `390 004` has exact-prefix closure/non-bare alternation (`<END>:1;125:1`), and it is source-pending. `416` collapses from 6 rows to one strict identity cell; `698` collapses from 2 rows to one. `603` survives as post-`861` simple-tail behavior with 3 source-ready strict identity cells, while `533-717` survives as a fixed-unit comparator in one narrow Mohenjo no-icon cuboid-convex register.

- [032-002 861 source-first terminal-space campaign](campaign_032_002_861_source_first_terminal_space.md) is complete with mechanic validation PASS. It generalizes the terminal-space attack across the source-ready post-`861` packet: 14 rows source-ready, 12 quantified, with `M-355` and `M-1267` still visual-only. Tailed terminal-content windows are `120-265px` / `0.177-0.433`; bare post-terminal margins are `28-45px` / `0.040-0.063`. Same-line tail attachment survives as source-visible positional evidence, but grammar promotion is blocked because no quantified bare row currently shows tail-sized available terminal space while choosing closure.
- [032-002 861 terminal-space recut v2](campaign_032_002_861_terminal_space_recut_v2.md) is complete with mechanic validation PASS. It closes the immediate visual-only gap: all 14 source-ready rows are now quantified. `M-355` is now a measured long-continuation adversary (`525px` / `0.395`), and `M-1267` is now a measured bare closure (`35px` / `0.043`) under quality/orientation limits. The adversary strengthens rather than weakens: tailed windows now span `120-525px` / `0.177-0.433`; bare margins remain `28-45px` / `0.040-0.063`. No bare row with tail-sized same-line terminal opportunity has been observed.

Completed campaign:

- [032-002 861 / 390-004 exact-prefix source gate](campaign_032_002_861_390004_exact_prefix_source_gate.md) is complete with mechanic validation PASS. `H-55` is source-visible as same-line five-glyph terminal-material evidence; `M-1750` is public-source-dark, so the split stays acquisition-gated. Counts are `390-004` starts `21`, `390-004-002-Y` rows `10`, local `125` occurrences `59`, immediate `002-861-125` occurrences `1`, and exact-prefix mixed candidates `1`.
- [032-002 861 / 390-004 branch and 125 ecology](campaign_032_002_861_390004_branch_125_ecology.md) is complete with mechanic validation PASS. It widens the unit to `390-004-002-Y` plus all local `125` adjacency. Result: `125` is not a general post-`861` suffix (`59` local occurrences, `17` terminal, `2` immediate after `861`, `1` immediate after `002-861`), but four `002-390-125` rows make it live inside `002-390-X`.
- [032-002 861 / 002-390-125 branch source route](campaign_032_002_861_002390125_branch_source_route.md) is complete with mechanic validation PASS. `002-390-X` has `15` rows and `10` next signs; `125` is the largest raw group at `4`, but source-visible `M-70 +226-032-002-390-692+` proves `002-390` can continue without `125`. `125` stays alive as a source-weak plurality branch member, not as a suffix/value/translation.
- [032-002 861 / 002-390-X subframe hypotheses](campaign_032_002_861_002390x_subframe_hypotheses.md) is complete with mechanic validation PASS. The next live positives are `235->002-390->125` (`2/2` local rows) and the `125->632 032` prefix (`2` rows), but both are source-weak and must be attacked as possible formula/copy-family artifacts.

- [032-002 861 / 002-390-X source-normalized contrast](campaign_032_002_861_002390x_source_normalized_contrast.md) is complete. `M-119` and `M-735` are now strict public source-visible `125` candidates, `Sktd-1` is a panel-bound public candidate, and `M-71` is a source-visible repeated `095` non-`125` comparator. The decision is not `125` solved; it is `125` upgraded to a source-visible plurality candidate while `M-70/M-71` block any necessary-marker/value reading.
- [032-002 861 / 002-390-X token-boundary readiness](campaign_032_002_861_002390x_token_boundary_readiness.md) and [linguistic decision gate](campaign_032_002_861_002390x_linguistic_decision_gate.md) are complete. The next experiment is boxed-source adjudication of `M-119/M-735` against `M-70/M-71`, with `Sktd-1` downweighted and `M-38/H-1993/M-1825/Dholavira 4237.1` excluded until stronger routes exist.
- [032-002 861 / 002-390-X boxed-window adjudication](campaign_032_002_861_002390x_token_boundary_adjudication.md) is complete with adversarial label correction. The result is boxed-window-compatible, not blind source-window-preserved proof. `M-119/M-735` are compatible with `002-390-125`; `M-70/M-71` are compatible non-`125` controls; `Sktd-1` remains downweighted.
- [032-002 861 / 002-390-X family-independence stress](campaign_032_002_861_002390x_family_independence_stress.md) is complete. Strict `M-119/M-735` do not collapse by exact text, previous sign, tail, symbol/cult, or source route, but they share broad Mohenjo-daro square steatite `SEAL:S` register.
- [032-002 861 / 002-390-X family-collapsed branch ecology](campaign_032_002_861_002390x_family_collapsed_branch_ecology.md) is complete. `125` remains live as a continuation-bearing branch candidate after `002-390`: four raw rows/four family cells, strict visible `M-119/M-735`, all local `125` rows nonterminal. Strict visible non-`125` controls `M-70(692)` and `M-71(095)` are terminal, but not matched previous-frame controls. `705` is the missing repeated source-visible non-`125` branch.
- [032-002 861 / 002-390-X source-normalized family collapse](campaign_032_002_861_002390x_source_normalized_family_collapse.md) is quarantined, not complete. The post-cutoff artifact is physically moved and must not be cited as a settled result. Use the replacement branch-sign ecology recheck and later source-gate artifacts for live status.

Next immediate linguistic campaign:

- Alpha blind adjudication packet is complete and produced a downgrade, not promotion. Readers marked all panels partial; `Sktd-1` is demoted from strict visual counts; `M-119/M-735` remain partial blind witnesses only. Next blind work must compare reader boundary proposals against the neutral overlay key and decide which local windows survive without catalog forcing.
- Blind-over-key alignment is complete. Decision: no alpha witness reaches source-window-preserved proof. Ranking: `M-70/692` strongest partial control, `M-119/125` strongest partial target, `M-71/095` partial control, `M-735/125` weak partial target, `Sktd-1/125` demoted. Stop defending `125` visually; force the next step onto source-bound matched alternatives and branch/tail predictions.
- Route `H-1993` from the concrete public lead `H96-2769 Figure 17.07`; it can test the `004->002-390` split against panel-bound `Sktd-1`, but it still lacks an artifact image.
- Bind Dholavira page 18 item 10 to Lipi row `4237.1` or reject it. It visually matches the reverse of `+151-032-388-002-390-705+`, making `705` an acquisition-hot branch candidate, but it is not strict until the item-to-row link is proven.
- Dholavira route got stronger but remains unbound: public OCR exposes the matching `ZA-12:2` and `27.62 x 21.31 x 7.11-11.17` metadata cluster, while page 18 item 10 remains only visually plausible. Next target is a plate/list/table bridge explicitly tying item 10 to `ZA-12:2`, dimensions, or row `4237.1`.
- Route `M-1825` / `BJ25710`; Bhaskar S1 confirms M-1825 as an F2 unicorn object, but not the sign band. Until M-1825 or Dholavira item 10 is bound, `705` must not be counted in source-normalized inference.
- Keep `ICIT 4348 (Dholavira)` out of the `4237.1` route. The Singh et al. supplement mentions it near the H-1993 lead, but local `4348.1` is a different clay `TAG` fragment and does not bind the Bisht item 10 candidate.
- Branch-tail prediction object is now active: in the 15-row `002-390-X` matrix, `125` is 4/4 continuation, repeated `095` is 2/2 closure, repeated `705` is 2/2 closure but source-gated, and strict-visible `692` is closure. Next work must test the prediction at batch scale: source-bind `705`, source-bind H-1993, then hunt matched source-bound exceptions (`125` terminal or non-`125` continuation) before any grammar/value claim.
- Competing linguist hypotheses are recorded. Positive model: branch-conditioned construction. Adversarial model: copied visual-register/template plus source-window, tail-space, and catalog artifacts. The next campaign should be a direct model fight, not a one-sign audit.
- Source-normalized family collapse is quarantined. Do not use its post-cutoff result as evidence. Keep the next decisive work on re-earned gates: `705`, H-1993, `3335.1`, or a source-bound matched exception.
- Replacement branch-sign ecology recheck is complete and supersedes the quarantined post-cutoff `source_normalized_family_collapse` artifact for live status. `002-390-X` remains the object; `125` is a frame-conditioned continuation-heavy branch, not a value; `705` remains zero strict after both Dholavira and M-1825 route checks; H-1993 remains supplement-only; H-773 remains boxed-compatible but not strict.
- Source-bound intrinsic sign-behavior recheck is complete as a guardrail, not a promotion. H-55 terminal `125`, H-660 continuing `095`, M-21 continuing `692`, and M-118/M-714 continuing `705` reject the intrinsic-value shortcut. The next live `002-390-X` work must stay inside the frame: source-bind repeated `705`, source-bind H-1993, or find source-bound in-frame exceptions.
- `3335.1` source-identity recheck is complete as a negative gate, not a promotion. The row is not rescued by the nearby `M-940` gap: `M-940` is present as local row `2243.1` and source-visible on CISI Pakistan page 91 / IA leaf `n125`. Keep `3335.1` as raw local continuing non-`125` pressure only; do not count it as a source-normalized exception until a real object/source bridge appears.
- `390-590-032` family recheck is complete and increases adversarial pressure on `3335.1`. The chunk occurs in seven local rows across Lothal tags, Mohenjo-daro seals, and unbound `3335.1`; `M-746` and `M-965` are source-visible non-frame controls. Future `3335.1` use must survive both object/source binding and formula-family collapse.
- H-1993 image-binding recheck is complete as a route-tightening negative gate. Full CISI 3.1 is now the acquisition target: HARP `H-1521` to `H-2583` photos on pages `207-360`, plus Harappa basic data on pages `423-441`. The public Harappa PDF is only a 17-page essay/front-matter excerpt; fresh public/local searches found no H-1993 artifact image/caption. Keep H-1993 out of strict `095` source counts until the full plate/data source or an equivalent archive/museum image binds `H-1993`, `H96-2769`, or `ICIT 744`.
- H-773 side-guard recheck is complete as a false-upgrade block. Kenoyer/Meadow 1997 plus Vats Plate XCIV item `351` route local pointer `12377351` to `H-773B`, not the target `H-773A`. Keep the Vats route as object/provenance pressure and side-label guard only. The target `002-390-530-741` side A still needs either a cleaner H-773 A image or an independent sign list fixing `530` and `741`.
- Source-tiered predecessor gate is complete as a promotion block, not as a negative against the branch-tail object. Strict rows preserve polarity (`M-70/M-71` non-`125` terminal; `M-119/M-735` `125` continuing), but no strict source-visible predecessor group has two branch alternatives. Current status: `strict_core_polarity_unmatched_prev_gate_blocks_grammar_no_values`. Next `002-390-X` work should prioritize a true matched predecessor branch split: bind H-1993 for the `004` split, bind or replace `3335.1` for the `032` split, or find a new strict same-predecessor exception.
- Sktd-1 side-pair recheck is complete as a route upgrade with a token-order block. CISI India `n397` labels `Sktd-1 A/a`, so Sktd-1 is source-panel side-pair visible; the layout is wrapped, with a top band plus a separate lower-field sign. Current status: `sktd1_side_pair_visible_wrapped_layout_not_strict`. The next `004` split work is therefore H-1993 acquisition, not more Sktd-1 promotion from the same public plate.
- Near-frame scout is complete and found no hidden damaged/open or gapped rescue. Adjacent `002-390` remains exactly 15 rows, with 0 damaged/open adjacent cases; gapped `002-X-390` rows are K-89 and Dholavira `4348.1` only. Current status: `near_frame_scout_no_hidden_matched_prev_rescue_no_values`. Keep ICIT 4348 guarded out of the `4237.1 / 002-390-705` lane.
- H-1993 acquisition packet is ready but not sent. Current status: `h1993_acquisition_packet_ready_no_image_binding`. Use one compact source request or full CISI 3.1 inspection for `H-1993 / H96-2769 / ICIT 744`; do not send more scattered micro-asks into the existing Andreas/Fuls thread.
- Dholavira `8758 / ZA-12:2` acquisition packet is ready but unbound. Current status: `dholavira_8758_acquisition_packet_ready_unbound_no_strict_705`. Next useful move is source image/caption/data row for Acc. No. `8758`, not more page-18 item-10 visual matching.
- 2026-05-31 update: Dholavira `8758 / ZA-12:2` source contact has been sent to `harappa@gmail.com` as Gmail message/thread `19e7dc93574535f6`. Current status: `dholavira_8758_source_contact_sent_awaiting_reply_no_values`. Wait for a reply/source bridge; do not upgrade page-18 item 10 or strict `705` from the sent request itself.
- 2026-05-31 update: M-1825 / `BJ25710` source contact has been sent to `harappa@gmail.com` as Gmail message/thread `19e7dce8a7220bff`. Current status: `m1825_source_contact_sent_awaiting_reply_no_values`. Wait for a reply/source bridge; do not upgrade strict `705` from the sent request itself.
- M-1825 acquisition packet is now sent but still sign-band dark. Current status: `m1825_source_contact_sent_awaiting_reply_no_values`. Next useful move is a source reply or independent source volume/archive/catalogue bridge for `M-1825 / BJ25710`, not another icon-class list.
- `390-X` context adversary is complete. Current status: `390_context_adversary_keeps_002_conditioning_live_no_values`. The next non-acquisition experiment should compare `002`-conditioned `390-X` behavior against matched left-context/full-formula controls, because generic `390-X` alone does not explain `125` or `095` behavior.
- Full-left formula controls are complete. Current status: `full_left_formula_controls_break_head_determinism_but_no_branch_promotion_no_values`. The gate weakens deterministic-template collapse because `7/15` target frames have exact full-left controls with alternate post-`002` heads, but it finds `0` exact full-left `002-390-X` branch splits. Continue with acquisition, exact-left singleton controls, or a new matched branch split, not value claims.
- Left-context radius scan is complete. Current status: `left_context_radius_scan_immediate_splits_source_blocked_no_values`. Branch alternatives exist only at immediate predecessor radius: `004` and `032`. Radius `>=2` has no branch splits, and no strict source-visible branch split exists at any radius.
- Matched-lane replacement scout is complete. Current status: `matched_lane_replacement_scout_no_local_replacement_witness_no_values`. The only local adjacent `002-390-X` rows for the `004`/`032` lanes are H-1993/Sktd-1 and M-70/`3335.1`; there is no local backup witness. Continue with external acquisition or a genuinely new public/source row, not local row re-ranking.
- Source-upgrade impact audit is complete. Current status: `source_upgrade_impact_audit_3335_single_unlock_004_dual_upgrade_705_ecology_no_values`. Acquisition priority now separates matched-gate proof from ecology: `3335.1` is the highest single-object matched-gate unlock; `004` needs dual strict sides, not H-1993 alone; M-1825 plus Dholavira improves repeated `705` ecology but not matched-lane proof.
- `3335.1` identity-neighborhood audit is complete. Current status: `3335_identity_neighborhood_no_local_bridge_external_source_required_no_values`. Local triangulation does not bind the target: one exact-text row only, seven `390-590-032` family rows, no row-order bridge, and no source-bound metadata-neighborhood replacement. Continue with external source acquisition or a genuinely new strict `032` replacement row.
- Sktd-1 strictness audit is complete. Current status: `sktd1_strictness_audit_wrapped_layout_blocks_dual004_no_values`. The current public Sktd-1 plate is panel-bound and top-band compatible, but wrapped layout, lower-field sign order, and boxed-only adjudication block strict token/order. Do not spend more local effort re-promoting this plate; the `004` lane needs H-1993 plus a cleaner Sktd source, or an equivalent dual strict pair.
- `3335.1` acquisition packet is complete. Current status: `3335_acquisition_packet_ready_external_source_or_replacement_required_no_values`. The target is now a precise external source request: `3335.1 / +740-205-032-002-390-590-032+ / 29 x 29 / SEAL:S / Bull1:J / RAF`; it remains `T3_quarantined_metadata` with no object/image bridge. M-143 is only a `740-205-032-002` prefix-family control, not an identity bridge.
- M-143 prefix-control source recheck is complete. Current status: `m143_prefix_control_source_panel_found_not_3335_bridge_no_values`. CISI India `n80` visibly labels `M-143 A` and `M-143 a`, so the shared `740-205-032-002` prefix control is now source-panel visible. It still branches to `252-840`, does not bind `3335.1`, and is not a blind numeric token-box proof.
- `3335.1` Yajnadevam provenance recheck is complete. Current status: `3335_yajnadevam_pinned_provenance_recheck_no_source_bridge_no_values`. The upstream raw Lipi CSV is pinned to commit `b272ad99c253ba7fa1e4cd91f48cce31f6d02bf4` and confirms the same unbound row; it adds no object/source/image bridge, only quarantined `sanskrit`, `translation`, and `notes` fields. Do not keep looping on local Lipi provenance.
- `3335.1` Yajnadevam repo trace is complete. Current status: `3335_yajnadevam_repo_history_private_collection_no_image_bridge_no_values`. The unshallowed upstream repo adds only an old-history clue: 2024 old row `3335` had `museum = Private collection`. Current repo/app/image mapping has no `3335.1` key, no `-` fallback key, no object id, and no source-generation trail. Use this as acquisition wording only.
- `3335.1` private-collection web scout is complete. Current status: `3335_private_collection_web_scout_no_public_bridge_no_values`. Exact public web searches found no target bridge; auction/private-collection/zebu candidates are false leads or comparanda unless they gain matching dimensions, sign sequence, and object/caption evidence.
- `3335.1` private-collection cluster probe is complete. Current status: `3335_private_collection_cluster_two_rows_no_bridge_no_values`. The old `Private collection` field covers exactly two rows, old `3335` and old `3118`; current `3118.1` is also Unknown/dash-CISI/no-image-map and does not identify a source holder or bridge the target. Do not keep looping on sibling `3118`.
- H-1993 source contact is sent. Current status: `h1993_source_contact_sent_awaiting_reply_no_values`. Message `19e7dc4f6f34e60c` in Gmail thread `19e6211289c772f3` asks Andreas Fuls/Omar Khan for source binding of `H-1993 / H96-2769 / ICIT 744`. This is acquisition only; H-1993 remains route-only until a reply/source arrives.
- CISI 3.1 acquisition route is complete as a scope/acquisition gate. Current status: `cisi31_acquisition_route_confirms_h1993_m1825_scope_no_object_pages`. Public bibliographic routes confirm full CISI 3.1 as the Mohenjo-daro/Harappa supplement and the shared acquisition target for H-1993 and M-1825; no object pages have been inspected. Continue with full-volume acquisition or source-holder reply, not evidence-tier promotion.
- CISI 3.1 invoice-address reply is sent. Current status: `cisi31_invoice_address_sent_awaiting_payment_link_no_object_pages`. Message `19e7de2eaceb9d99` in Gmail thread `19e5f05e8752244a` answered Tiedekirja's address/zip request; now wait for the payment link/password. This is purchase logistics only, not evidence-tier promotion.
- CISI 3.1 public access guard is complete. Current status: `cisi31_public_excerpt_finna_holdings_no_object_pages`. The Harappa public PDF is still only a 17-page excerpt with no `H-1993` or `M-1825` text hits, and Finna holdings metadata is access routing only. Do not use public excerpt/holdings metadata as object-page evidence.
- Current `002-390-X` decision state is synthesized in `docs/campaign_032_002_861_002390x_current_decision_state_20260531.md`. Current status: `390405_collision_adversary_blocks_p086_collapse_no_values`. Continue with H-1993/Dholavira/M-1825/Yajnadevam reply tracking, Tiedekirja payment-link tracking, full-CISI acquisition, external `3335.1` private-collection source acquisition/replacement, dual-side `004` acquisition, or repeated `705` source control, not Mayig crosswalk inflation, 390/405 collapse, or value claims.
- Re-earned family collapse is complete as a clean replacement gate, not as goal completion. Current status: `reearned_family_collapse_demotes_subframes_no_values`. It used replacement frames and metadata only, not the quarantined artifact. `235-002-390-125`, `125-632-032`, and repeated `705` all demote under strict/source-family pressure. Continue with reply tracking, source acquisition, or matched strict exceptions.
- H-773 Lipi image-map guard is complete as a strictness downgrade. Current status: `h773_lipi_image_map_derivative_no_strict_upgrade`. The repo has derivative A/B images, but they are lower-resolution than the existing CISI crop and do not independently prove `530`, `741`, or `530 -> 741`. Keep H-773 panel-bound/boxed-compatible only.
- Mayig shadow-lane check is complete as a crosswalk-inflation guard. Current status: `mayig_shadow_exact_032_lane_no_replacement_pair_collision_guard_no_values`. Exact `P145 P122 P086` adds no replacement for `3335.1` because it returns only known `M-70`; broader `P122 P086` collides with local `002-405` on `M-34` and `M-41`. Do not use Mayig `P122 P086` as source-normalized `002-390` evidence or as a shortcut around the blocked `032` matched lane.
- `3335.1` Yajnadevam source contact is sent. Current status: `3335_yajnadevam_source_contact_sent_awaiting_reply_no_values`. Message/thread `19e7dee9b40595b7` asks `yajnadevam@proton.me` for source image, object id, catalogue/plate/figure reference, provenance note, source table, or no-source confirmation for row `3335.1`. Wait for a reply/source bridge; the sent request itself does not bind the row.
- 390/405 collision adversary is complete. Current status: `390405_collision_adversary_blocks_p086_collapse_no_values`. `002-405-X` has 32 frames but 29 are exact repeated Harappa cylindrical `TAB:B` `+520-240-002-405-501+`, so Mayig `P086` cannot be used to merge `390` and `405` or inflate `002-390-X`. Future crosswalk-normalized work must carry the `390/405/406/407 -> P086` collision guard.
- Acquire `M-1750` or an equivalent exact-prefix bare `390-004-002-861+` control from CISI 3.1, HARP, archive, museum, or direct contact. This remains important, but it is no longer the only lane.
- Source-route the whole `390-004-002-Y` branch batch, especially `M-103`, `M-984`, `M-1844`, `Sktd-1`, and `M-1823`, so the branch behavior is not judged from one positive H-55 witness.
- Keep `125` ecology as a sign-system question only inside branch/tail contexts: terminal `125`, post-`861-125`, `002-390-125-X`, and `390-004-*125*`, with `416/698/096`, `692`, `095`, `705`, and long continuations as controls.
- Positive-space hunt still remains active: find a bare `002-861+` closure with at least `120px` same-line terminal opportunity under matched formula/register conditions. Without that, post-`861` grammar promotion stays blocked.
- Recut all `220-032` rows tail-hidden and add `C-65` / `M-1763` only if they can be measured under the same rule.
- Do not promote optional grammar until at least one bare row with tail-sized terminal space still chooses closure, and until complete-formula alternatives are source-visible and still alternate under comparable terminal-space and source-family controls.
