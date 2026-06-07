# 002-390-X source-bound intrinsic sign behavior recheck

Date: 2026-05-31 America/Los_Angeles

Status: adversarial guardrail, not goal completion.

## Question

Can the `002-390-X` branch pattern be reduced to intrinsic behavior of the branch signs?

Lazy positive model:

```text
125 means/causes continuation.
095/692/705 mean/cause closure.
```

This gate tests that shortcut directly with source-visible non-frame behavior. It does not test values, phonetics, language identity, sign meanings, or translations.

## Result

The shortcut fails.

Source-visible or source-routed non-frame behavior exists in the opposite direction for each focus sign:

| Sign | Non-frame source check | Behavior outside `002-390-X` | Source tier | Consequence |
|---|---|---|---|---|
| `125` | `H-55 +390-004-002-861-125+` | terminal | same-line five-glyph source band | `125` is not intrinsically continuation-bearing |
| `095` | `H-660 +520-095-033-706-240-798+` | continuing | same-line six-glyph source band | `095` is not intrinsically closure-bearing |
| `692` | `M-21 +350-001-740-362-692-032-002-861+` | continuing | source-visible row plus medium token-box candidate | `692` is not intrinsically closure-bearing |
| `705` | `M-118 +740-772-033-705-233-803-002-861+` | continuing | source-visible signband / bare-edge control | `705` is not intrinsically closure-bearing |
| `705` | `M-714 +740-585-017-033-705-233-798-803-002-861-603+` | continuing | source-visible same-line candidate, crowded | second guardrail for `705` |

The source evidence is row/order pressure, not a new accepted sign-value layer. In every row above, numeric sign identity still rests on catalog transcription or previously boxed windows. That is enough to block intrinsic-value claims, but not enough to accept meanings.

## H-660 acquisition note

H-660 was the missing clean `095` guardrail in this pass.

- Local text: `+520-095-033-706-240-798+`
- Local role in this gate: non-frame continuing `095`
- Source route: CISI Pakistan leaf `n343`, printed p. 309, plate header `SEALS HARAPPA 658-665`
- Visual check: the page visibly carries `H-660 A` and `H-660 a` as same-line six-glyph bands
- Stored local page copy: `tmp/002390x_intrinsic_sign_behavior_recheck/H660_cisi_pakistan_n343_full_page.jpg`

This promotes the `095` non-frame continuation guard from metadata-only pressure to source-visible row pressure. It does not make `095` strict token evidence in this gate.

## Decision

`002-390-X` remains alive only as a branch-conditioned ecology:

```text
002-390-X may condition closure/continuation behavior.
The branch signs themselves do not carry accepted intrinsic closure/continuation values.
```

This helps both sides of the model fight:

- It protects the positive model from being dismissed as a trivial sign-position artifact.
- It blocks the positive model from inflating the frame pattern into sign meanings.

## Ledger effect

No accepted value, phonetics, language identity, function, sign meaning, or translation.

No strict `705` source witness inside `002-390-X`.

No strict H-1993 image witness.

No grammar promotion.

Current status: `source_bound_intrinsic_sign_behavior_shortcut_rejected_no_values`.

## Next gate

The next decisive gate is still inside the frame, not in global sign behavior:

1. Source-bind repeated `002-390-705` through Dholavira `4237.1`, M-1825, or a replacement witness.
2. Source-bind H-1993 / `002-390-095`.
3. Hunt a true source-bound in-frame exception: terminal `125` after `002-390`, or continuing `095/692/705` after `002-390`.
4. Collapse any positive exception by exact formula, broad register, source family, and terminal-space opportunity before treating it as grammar.
