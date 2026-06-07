# 032-002-861 / 002-390-X Source-Normalized Contrast

Date: 2026-05-30

## Question

After the earlier `002-390-125` branch pass, does source normalization make `125` more alive, or does it dissolve into catalog/index noise once compared against source-visible non-`125` continuations?

## Result

`125` is upgraded, but not translated.

The prior state treated `M-119` as Mayig-only and `M-735` as an index-hint. This pass upgrades both: `M-119` is visible on CISI India `n076`, and `M-735` is visible on CISI Pakistan `n086`. `Sktd-1` is also panel-bound on CISI India `n397`, though it stays below strict token proof. `M-38` remains weak: the public context exists, but the signband is too faint for token-level promotion.

That changes the branch from "mostly source-dark" to "source-visible plurality candidate." It still does not give a sign value. The source-visible controls `M-70` (`002-390-692`) and `M-71` (`002-390-095`) show that `002-390` can continue without `125`, so `125` cannot be a necessary continuation marker.

Strict source-visible `125` candidates: 2 (`M-119 M-735`).

Permissive public-panel `125` candidates: 3 (`M-119 M-735 Sktd-1`).

Strict source-visible non-`125` controls: 2 (`M-70 M-71`).

Contact sheet: `C:\Users\Acer\OneDrive\Documents\ivc\tmp\002390x_source_normalization\campaign_032_002_861_002390x_source_normalized_contrast_contact_sheet.jpg`

## Branch Contrast

- `125`: 4 rows; strict source-visible 2 (M-119 M-735); decision: live_plurality_candidate_no_value; upgraded by M-119/M-735, still not necessary because source-visible non-125 controls exist
- `095`: 2 rows; strict source-visible 1 (M-71); decision: source_visible_non125_control_against_125_necessity
- `705`: 2 rows; strict source-visible 0 (none); decision: repeated_non125_branch_but_source_dark_in_this_pass
- `072`: 1 rows; strict source-visible 0 (none); decision: singletons_not_promoted
- `140`: 1 rows; strict source-visible 0 (none); decision: singletons_not_promoted
- `346`: 1 rows; strict source-visible 0 (none); decision: singletons_not_promoted
- `530`: 1 rows; strict source-visible 0 (none); decision: singletons_not_promoted
- `590`: 1 rows; strict source-visible 0 (none); decision: singletons_not_promoted
- `692`: 1 rows; strict source-visible 1 (M-70); decision: source_visible_non125_control_against_125_necessity
- `707`: 1 rows; strict source-visible 0 (none); decision: singletons_not_promoted

## Source Route Decisions

- `M-38`: weak_public_context_not_token_boxable via public_context_low_readability_cisi_india_n055. Panel/context exists, but the source image is too faint for token-level promotion.
- `M-70`: strict_source_visible_non125_control via public_source_visible_cisi_india_n066. Source-visible 002-390-692 control already cropped from CISI India n66.
- `M-71`: strict_source_visible_non125_comparator via public_source_visible_cisi_india_n066. M-71 A/a are visible on CISI India n66, upgrading repeated 095 from index hint.
- `M-119`: strict_source_visible_125_candidate via public_source_visible_cisi_india_n076. M-119 is visible on CISI India n76, printed p.41, panel M-119 A/a.
- `M-735`: strict_source_visible_125_candidate via public_source_visible_cisi_pakistan_n086. M-735 is visible on CISI Pakistan n86, printed p.52, panel M-735 A/a.
- `Sktd-1`: panel_bound_public_candidate via panel_bound_public_cisi_india_n397. Sktd-1 is panel-bound on CISI India n397, but exact side and token sequence still need token-boxing.
- `M-1825`: source_dark via still_unrouted_public_source_dark. Direct CISI XML search did not locate M-1825 in the local India/Pakistan scans.
- `H-1993`: source_dark via harappa_route_unresolved_not_public_cisi. Likely requires Harappa figure/acquisition route, not CISI India/Pakistan page route.
- `-`: source_dark via unresolved_non_cisi_object. No stable public label route yet.
- `-`: source_dark via dholavira_object_unresolved. No stable public label route yet.

## Subframe Tests

- `235_before_002390_then_125`: The subframe survives as a live branch pattern through M-735, but not as a two-source proof because M-38 is unreadable at token level. Source state: M-735 is now public-source-visible; M-38 remains weak context only
- `125_followed_by_632_032`: This is a real internal 125 subfamily candidate, but it may be one formula family rather than a general 125 function. Source state: M-119 is now public-source-visible; M-38 remains weak context only
- `004_before_002390_split`: Potentially useful minimal split, but not interpretable until H-1993 is routed. Source state: Sktd-1 is panel-bound public candidate; H-1993 remains source-dark
- `source_visible_non125_controls`: This kills any necessary-125 reading for 002-390. 125 is a branch member, not a mandatory suffix. Source state: Both are source-visible on CISI India n66 after this pass
- `repeated_705_branch`: Potentially important because repeated non-125 continuations would sharpen the branch ecology, but currently unusable for source-normalized inference. Source state: Both are source-dark/unresolved in this pass

## Crop Packet

- `M71_face_A`: inspectable_comparator -> `C:\Users\Acer\OneDrive\Documents\ivc\tmp\002390x_source_normalization\M71_face_A_signband.jpg`
- `M71_impression_a`: inspectable_comparator -> `C:\Users\Acer\OneDrive\Documents\ivc\tmp\002390x_source_normalization\M71_impression_a_signband.jpg`
- `M119_face_A`: inspectable_target -> `C:\Users\Acer\OneDrive\Documents\ivc\tmp\002390x_source_normalization\M119_face_A_signband.jpg`
- `M119_impression_a`: inspectable_target -> `C:\Users\Acer\OneDrive\Documents\ivc\tmp\002390x_source_normalization\M119_impression_a_signband.jpg`
- `M735_face_A`: inspectable_target -> `C:\Users\Acer\OneDrive\Documents\ivc\tmp\002390x_source_normalization\M735_face_A_signband.jpg`
- `M735_impression_a`: inspectable_target -> `C:\Users\Acer\OneDrive\Documents\ivc\tmp\002390x_source_normalization\M735_impression_a_signband.jpg`
- `Sktd1_face_A`: panel_bound_candidate -> `C:\Users\Acer\OneDrive\Documents\ivc\tmp\002390x_source_normalization\Sktd1_face_A_signband.jpg`
- `Sktd1_impression_a`: panel_bound_candidate -> `C:\Users\Acer\OneDrive\Documents\ivc\tmp\002390x_source_normalization\Sktd1_impression_a_signband.jpg`
- `M70_a_existing`: inspectable_comparator -> `C:\Users\Acer\OneDrive\Documents\ivc\tmp\032_002_branch_tail_source_acquisition\M70_impression_a_signband_from_cisi_india_n066.png`
- `M38_context_existing`: weak_not_token_boxable -> `C:\Users\Acer\OneDrive\Documents\ivc\tmp\source_box_negative_control_v2\panel_crops\M-38_cisi_india_n55_plate_label_free_panel_enhanced_x2.jpg`

## Linguistic Decision

Keep `125` alive as a source-visible branch member inside `002-390-X`. Do not assign a value, phonetic reading, language identity, or translation.

What changed: `125` is no longer just a catalog plurality. It now has strict public visual support through `M-119` and `M-735`, plus weaker panel-bound support through `Sktd-1`.

What did not change: `125` is not necessary after `002-390`; `M-70` and `M-71` are source-visible non-`125` controls. The live linguistic object is therefore a branching continuation system after `002-390`, not a single suffix.

## Next Acquisition Targets

1. Token-box `M-119`, `M-735`, `M-71`, `M-70`, and `Sktd-1` from the public plates.
2. Route `H-1993` to test the `004->002-390` split against `Sktd-1`.
3. Route `M-1825` and Dholavira `4237.1` to decide whether repeated `705` is a real non-`125` branch.
4. Acquire a sharper `M-38` image before using it as anything stronger than weak formula-family support.

Accepted values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain `0`.
