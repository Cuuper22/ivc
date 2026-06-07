# Lipi 034 M-1206 H-938/H-910 Direction Sensitivity Gate

Date: 2026-05-26

## Question

Does the `H-938 B` / `H-910 B` mirror-order pair decide whether local `034` is the vertical/rake `415`-like component?

## Inputs

- `H-938 B`: local `+034-700+`, direction field `R/L`, visible left component vertical/rake, visible right component loop/leaf.
- `H-910 B`: local `+700-034+`, direction field `R/L`, visible left component loop/leaf, visible right component vertical/rake.
- Comparison sheet: `tmp/h910_component_probe/h938_h910_component_order_comparison.png`.
- CSV: `data/open_prototype/reports/lipi_034_m1206_h938_h910_direction_sensitivity_gate.csv`.
- Summary: `data/open_prototype/reports/lipi_034_m1206_h938_h910_direction_sensitivity_gate_summary.json`.
- Direction convention warning: CISI original/impression convention blocks silent reversal from scan orientation alone.

## Direction-Sensitive Result

| Object side | Local text | Recorded direction | Under recorded direction | If forced L/R instead |
| --- | --- | --- | --- | --- |
| `H-938 B` | `+034-700+` | `R/L` | `034` = right loop/leaf; `700` = left vertical/rake | `034` = left vertical/rake; `700` = right loop/leaf |
| `H-910 B` | `+700-034+` | `R/L` | `034` = left loop/leaf; `700` = right vertical/rake | `034` = right vertical/rake; `700` = left loop/leaf |

So the mirror-order pair is not an unconditional answer.

Under the recorded local `R/L` policy, the pair is negative for direct `034=415` component identity: `034` tracks loop/leaf in both sides, while `700` tracks vertical/rake.

Under a forced global `L/R` counter-policy, the pair flips: `034` would track vertical/rake in both sides. That is not accepted, because it requires invalidating the recorded direction fields without source-policy support.

## Claim Status

Accepted now:

- `H-938 B` and `H-910 B` are source-visible mirror-order component checks.
- Both relevant local rows carry recorded `R/L`.
- Under recorded `R/L`, direct component-level `034=415` is rejected.

Not accepted:

- A global proof that `034` is distinct from `415`.
- A global proof that `034=415`.
- Any allograph status, value, function, language identity, or translation.

## Next Gate

Validate the recorded `R/L` policy for these source panels.

Useful evidence would be one of:

1. Source/corpus notes that explain how the local direction field was assigned for `H-938 B` and `H-910 B`.
2. Independent source-visible `+700-032+`, `+700-033+`, and `+700-034+` controls where the component assigned to `032/033/034` can be checked without relying on this same pair.
3. A same-object or same-page case where `700` or `034` is anchored by a less ambiguous graphic counterpart.

Until then, the right state is:

```text
conditional negative under recorded R/L;
unresolved, not positive, if R/L policy fails.
```
