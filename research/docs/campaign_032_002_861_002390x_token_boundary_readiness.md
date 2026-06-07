# 032-002-861 / 002-390-X Token-Boundary Readiness

Date: 2026-05-30

## Question

Which `002-390-X` witnesses are ready for source-token boundary judgment, and what would demote `125` if the visible source bands do not preserve the catalog window?

## Result

The next inference unit is a token-boundary packet, not a value assignment.

Strict target rows ready for blind token boxing: `M-119` and `M-735`.

Strict non-`125` controls ready for the same treatment: `M-70` and `M-71`.

Downweighted public-panel target: `Sktd-1`.

Excluded from strict source-token inference for now: `M-38`, `H-1993`, `M-1825`, and Dholavira `4237.1`.

Contact sheet: `C:\Users\Acer\OneDrive\Documents\ivc\tmp\002390x_token_boundary_readiness\campaign_032_002_861_002390x_token_boundary_readiness_contact_sheet.jpg`

## Readiness Rows

- `M-119`: token_box_ready_high; catalog positions 4-6 = 002-390-125; also tests 125->632-032. Risk: source-local side/order still catalog-mediated; face/impression must be boxed without assuming Mayig/local sequence is source-derived
- `M-735`: token_box_ready_high; catalog positions 4-6 = 002-390-125; tests 235->002-390->125. Risk: panel is readable but source/local side mapping is not independently proven in this packet
- `Sktd-1`: token_box_ready_medium; catalog positions 3-5 = 002-390-125; also tests 004->002-390 split. Risk: panel-bound, but exact side and token sequence remain weaker than M-119/M-735; site/register difference may be doing the work
- `M-71`: token_box_ready_high; catalog positions 4-6 = 002-390-095. Risk: it is one source-visible 095 control; H-1993 is still needed to make repeated 095 source-normalized
- `M-70`: token_box_ready_high; catalog positions 3-5 = 002-390-692. Risk: single 692 control, but already decisive against necessary-125 if token boxing holds
- `M-38`: not_ready; catalog positions 9-11 = 002-390-125; tests both 235-before and 125->632-032. Risk: public context exists, but the signband is too faint for token-level promotion
- `H-1993`: not_ready; catalog positions 5-7 = 002-390-095; would test 004->002-390 split. Risk: no public route in current packet
- `M-1825`: not_ready; catalog positions 3-5 = 002-390-705. Risk: direct public CISI route not found in this pass
- `Dholavira 4237.1`: not_ready; catalog positions 4-6 = 002-390-705. Risk: object route unresolved

## Demotion Triggers

- `M-119`: If neither public side preserves a separable 002-390-125 window followed by the expected post-125 cluster under any explicit direction policy, demote M-119 from strict 125 support to source-visible object only.
- `M-735`: If the visible band cannot support a separable 235->002-390->125 sequence under explicit side/order policy, demote the 235 subframe to one weak M-38-led clue.
- `Sktd-1`: If side/token boxing fails or the apparent window is not separable, keep Sktd-1 out of strict 125 counts and use only as acquisition pressure.
- `M-71`: If boxed source order does not preserve 002-390-095, repeated 095 drops back to source-dark H-1993 only.
- `M-70`: If source boxing fails to preserve 002-390-692, the strongest non-125 control weakens and M-71 must carry the control side.

## Linguistic Decision

If `M-119` and `M-735` both preserve separable `002-390-125` windows under explicit side/order policies, while `M-70` and `M-71` preserve separable non-`125` windows, then the live object upgrades to a source-tokenized `002-390-X` branch contrast. That still gives no phonetic value, meaning, language identity, or translation.

If either target fails source-token boxing, `125` drops back toward formula-family pressure. If both fail, `125` is demoted from live source-visible branch evidence to catalog/source-route pressure only.

The forbidden shortcut is to read `125`. The permitted question is whether source-visible inscriptions preserve a real branch slot after `002-390`.
