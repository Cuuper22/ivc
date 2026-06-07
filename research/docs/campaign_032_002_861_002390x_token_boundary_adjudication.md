# 032-002-861 / 002-390-X Token-Boundary Adjudication

Date: 2026-05-30

## Question

Are the visible source bands compatible with the immediate `002-390-X` windows for strict `125` targets and strict non-`125` controls under explicit side/order policy?

## Shape Reference

This pass compares visible bands against sign-shape descriptions, not only catalog numbers:

- `002`: two adjacent half-height simple vertical strokes
- `390`: simple tree with branches at the top
- `125`: person with bow and arrow
- `095`: person with short stick
- `692`: outlined X

## Result

The strict source-visible `125` targets `M-119` and `M-735` are compatible with separable boxed windows for `002-390-125` under explicit side/order policy. The strict non-`125` controls `M-70` and `M-71` are also compatible with boxed windows for `002-390-692` and `002-390-095`.

This upgrades the live object to a boxed-window-compatible `002-390-X` branch contrast. It is not yet a blind source-preserved branch proof. It still does not accept a numeric value, phonetic reading, language identity, sign meaning, or translation.

Boxed contact sheet: `C:\Users\Acer\OneDrive\Documents\ivc\tmp\002390x_token_boundary_adjudication\campaign_032_002_861_002390x_token_boundary_adjudication_boxed_contact_sheet.jpg`

## Witness Verdicts

- `M-119` (strict_125_target): boxed_window_compatible; shape_match_plausible_not_source_derived_numeric_proof; confidence `medium_high`. Consequence: keeps M-119 as strict target if M-735 also passes; no value accepted
- `M-735` (strict_125_target): boxed_window_compatible; shape_match_plausible_but_less_secure_than_M119; confidence `medium`. Consequence: keeps 235->002-390->125 as live only if family independence survives
- `M-70` (strict_non125_control): boxed_window_compatible; shape_match_plausible_control; confidence `medium_high`. Consequence: blocks necessary-125 if paired with M-71 and if target windows hold
- `M-71` (strict_non125_control): boxed_window_compatible; shape_match_plausible_control; confidence `medium`. Consequence: adds second strict non-125 control and strengthens branch plurality
- `Sktd-1` (downweighted_125_candidate): boxed_window_compatible_downweighted; shape_match_possible_not_strict; confidence `low_medium`. Consequence: cannot count equally with M-119/M-735 until side/token identity is explicit

## Active Adversaries

- `M-119`: side/order and local numeric identity remain catalog/Mayig mediated; source image itself supplies separability, not a standalone reading
- `M-735`: no Mayig independent row found; side/order and exact identity depend on local/corpus alignment
- `M-70`: single-branch control only; does not by itself establish repeated non-125 ecology
- `M-71`: H-1993 still source-dark, so repeated 095 is not fully source-normalized
- `Sktd-1`: site/register difference and side identity may be doing the work; H-1993 is absent on the 004->002-390->095 side

## Linguistic Decision

`125` survives the immediate boxed-window compatibility gate. It is not demoted by this visual pass alone.

The next danger is side/order blindness, independence, and formula-family collapse. If blind adjudication rejects the boundaries, if `M-119` and `M-735` reduce to one family/source habit, or if `125` occurs only inside closed longer formulas, then `125` demotes even though the current boxes are visually plausible.

Current status: `002-390-X` is a boxed-window-compatible branch contrast. `125` is a live branch member, not a reading.
