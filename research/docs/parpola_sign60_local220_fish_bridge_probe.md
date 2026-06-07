# Parpola Sign 60 / Local 220 Fish Bridge Probe

Date: 2026-05-26

## Question

Can local Lipi `220` be promoted from a bounded fish-form candidate to Parpola 2019 article sign no. `60`, the "plain fish" sign used in the text no. 7 recurrence discussion?

This is a sign-list/source bridge question. It is not a translation attempt.

## Evidence Checked

Primary sources and local evidence:

```text
tmp/parpola_2019_bone_rods.txt
tmp/parpola_1994_signlist/rendered/fig5_1-089.png
tmp/m1206_terminal_triad_source_recheck/derived/m37_A_signband_v2.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H938_A_panel.png
tmp/h940_higher_res_route/derived/h940_a_panel_from_iiif_max_gray_autocontrast.png
tmp/m1206_singleton_controls/derived/h942/H942_A_signband_from_cisi_pakistan_n374.png
tmp/mayig_feature_namespace_probe/repo/indus-valley-script-corpus-ad2f1e218a34b8c33c57de0d6cb8d99272765bbb/features/P050.json
data/open_prototype/reports/crosswalk_alignment_pairs.csv
data/open_prototype/lipi/metadata_filtered.csv
```

## Observations

Parpola 2019 explicitly describes sign no. `60` as the plain fish sign. In the text no. 7 discussion, the spear-like sign no. `189` follows this plain fish sign; in the text no. 8 comparison, the related sign no. `61` is the plain fish surrounded by four dots. A later passage also discusses sign no. `60` in horizontal and vertical positions. That establishes the article-side target: sign no. `60` is a plain fish-form sign in Parpola's convention.

Parpola 1994 Fig. 5.1 gives the source sign-list convention used by the article. The rendered Fig. 5.1 page stores sign no. `60` as a fish-form visual anchor:

```text
tmp/parpola_1994_signlist/rendered/fig5_1-089.png
width 1805
height 2357
sha256 8AFCF0D1D4662FC47014FDBF6CD6CED0F85E0FF07C2799169758E2AC2FF6996B
```

Mayig feature `P050` is described as `Fish with no other decoration` and maps to Parpola `V177/V517`, Wells `W220`, and Mahadevan `M059`. This is not the same as the rejected shortcut `V060`, but it is the relevant fish-form namespace witness.

The current overlap layer has 27 rows where local Lipi `220` aligns positionally to Mayig `P050`. The clean object-level row for the live branch is:

```text
M-37 2565.1 M-37A R/L +520-220-415+
local: 520 220 415
Mayig: P217 P050 P092
status: provisional_position_alignment_only
```

The source signband for M-37 shows the same three-part row already used in the M-1206 branch: a triangular/standard-like first sign, a fish-like middle sign, and a comb/rake terminal sign. This makes local `220` a stronger candidate bridge to article sign no. `60` than it was before the source visual check.

The broader local frame is distributionally real but not decisive. In `metadata_filtered.csv`, rows starting with `+520-220-X` number 52 and cover 16 third-slot types. The exact three-sign `+520-220-X+` subset has 21 rows: `415` appears 17 times, while `003`, `006`, `016`, and `034` appear once each. This supports the usefulness of the `520-220-X` frame, but it does not make `220` a solved article sign no. `60` bridge by itself.

## Decision

Status:

```text
local220_sign60_candidate_strengthened_not_accepted
```

Accepted:

```text
Parpola article sign no. 60 is a plain fish-form target in the checked article/sign-list convention.
Mayig P050 is a plain undecorated fish-form namespace witness.
Local Lipi 220 has repeated positional overlap pressure to Mayig P050.
M-37 gives the strongest current object-level source-visible candidate row for local 220 in the exact +520-220-415+ frame.
```

Not accepted:

```text
local 220 = Parpola article sign no. 60
Mayig P050 = Parpola article sign no. 60
Wells W220 = local Lipi 220
sign no. 60 semantic value
fish as a lexical reading
phonetic value
translation
```

## Next Gate

The next useful test is not another broad corpus scrape. It is a source-normalized middle-sign crop packet:

1. Crop the middle `220` component from source-visible `+520-220-X` rows where the side mapping is already usable: M-37 first, then H-938/H-940/H-942 if their middle component can be isolated without label or neighbor contamination.
2. Compare those middle components blind against Parpola 1994 sign no. `60` variants and Mayig `P050` source examples.
3. Accept a bridge only if the same object-side source, local token position, and sign-list convention all align.

Until that happens, local `220` is a P0 candidate bridge for article sign no. `60`, not a crosswalk.
