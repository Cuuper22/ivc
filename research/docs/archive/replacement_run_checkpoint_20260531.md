# Replacement Run Checkpoint

Date: 2026-05-31 America/Los_Angeles

Status: active goal, not complete.

A checkpoint is a trusted restart point. It states the accepted counts, the work that has been re-earned under the original scope, and the guardrails, so a new run does not inherit contaminated state. This checkpoint replaces the contaminated post-2026-05-31T01:04 successor state for current-run orientation. It does not mark the project complete.

## Accepted Claim Counts

| Claim class | Count |
| --- | ---: |
| translations | 0 |
| phonetic_values | 0 |
| sign_meanings | 0 |
| language_identification | 0 |
| structural_findings | 1 |
| external_anchors | 0 |

Only accepted claim: `accepted_struct_002_861_533_717_restricted_tail_2026_05_29`.

Boundary: fixed `002-861` branch only; `533-717` is a restricted terminal structural unit with witnesses `M-376` and `M-391`. No source-normalized token identity, sound, sign meaning, language family, external anchor, or translation is accepted.

## Replacement-Run Work Re-earned

### Quarantine

- Quarantine manifest: `data/quarantine/botched_successor_after_20260531T0104_manifest.csv`
- Guard: `data/quarantine/check_quarantine_references.mjs`
- Latest guard result: no accepted claim cites quarantined post-cutoff artifacts.

### V3 Brahmi

- Re-ran `data/brahmi/tools/build_brahmi_real_token_impostor_forger_v3.mjs`.
- Replacement low-null reaudit: `docs/brahmi_real_token_low_null_reaudit_20260531.md`
- Result: 21 low-null rows audited; 0 review-packet eligible; 0 accepted phonetic anchors.
- Normal-path index/ledger references now point to replacement-run low-null outputs, not `v3b`.

### V1 Meluhha / Failaka

- Object-level onomastic attempt re-run: `data/meluhha/object_level_onomastic_value_summary.json`
- Result: U17649 `ur gun3-a me-luh-ha` value attempt remains rejected; site-shuffle null >= observed share `0.6857`.
- Failaka acquisition guardrail: `docs/failaka_kjaerum_acquisition_20260531.md`
- Result: Laursen `12/13` Kjaerum `319/279` remain live acquisition targets. CDLI `1773730` is adjacent but not the target bridge; DAI route is anti-bot HTML; publisher/library routes are cached but expose no target pages.

### V4 Context

- Targeted fixed-pair null runner: `docs/vector4_targeted_context_nulls_20260531.md`
- Result: register-looking leads (`407`/Copper, `407`/`TAB:C`, `061-845`/Copper, `400`/`TAB:B`) are reproduced by site/type-preserved shuffles.
- Residue: `158-806 / Phyt` has low fixed-pair null shares, but text-only support is only `3`, below the support floor. It is a source-check queue item, not a sign meaning.

### V2 `002-390-X`

- Replacement branch forger: `docs/campaign_032_002_861_002390x_replacement_branch_forger.md`
- Branch ecology recheck: `docs/campaign_032_002_861_002390x_branch_sign_ecology_20260531.md`
- Result: `002-390-X` remains a live constructional ecology target. `125` is the largest in-frame branch and always continuing, while `095/692/705` are terminal in-frame. Promotion is blocked by source-binding gaps, continuing non-`125` exceptions, non-frame terminal `125`, and register/family concerns.

## Current Strongest State

The strongest accepted result is still the fixed `002-861` / terminal `533-717` structural finding.

The strongest live frontier is `002-390-X`, but it remains below ledger threshold. The next useful gates are:

1. Source-bind H-1993 to the actual `H96-2769 / Figure 17.07` image or remove it from strict `095` evidence.
2. Source-bind Dholavira `4237.1` through Acc. No. `8758` or `ZA-12:2`, not page-18 item 10.
3. Build a source-bound collapse of the `125-632-032` family.
4. Source-verify whether terminal `125` or continuing `095/692/705` occurs inside true `002-390-X` contexts.
5. For V4, source-check the three text-collapsed `158-806 / Phyt` witnesses before spending more null compute.

## Guardrail

Do not use:

- `tmp/quarantine_bad_successor_20260531T0104/**`
- `data/brahmi/brahmi_real_token_low_null_autopsy_v3b*`
- `docs/brahmi_real_token_low_null_autopsy_v3b.md`
- quarantined `campaign_032_002_861_002390x_source_normalized_family_collapse*`

Any broad post-cutoff dossier/state doc remains citation-risky until the specific claim is re-derived or line-audited.
