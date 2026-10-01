# Anchored Constraint-Collapse Stress

Date: 2026-05-30

This is the Priority C synthesis gate. An anchor here means an external fact that would fix the value of a specific sign. No external phonetic anchor and no Brahmi-derived phonetic anchor survived earlier gates, so no anchored partial reading is admissible. That leaves one honest question we can still ask: suppose we forced the rejected anchors anyway — how much would they reduce the unanchored label-symmetry floor? This note records that stress curve.

## Inputs

- `data/open_prototype/reports/effective_unicity_degeneracy_summary.json`
- `data/meluhha/external_phonetic_anchor_candidates.csv`
- `data/meluhha/object_level_onomastic_value_summary.json`
- `data/meluhha/object_level_onomastic_value_attempts.csv`
- `data/brahmi/brahmi_shape_descent_null_summary.json`
- `data/brahmi/source_token_brahmi_descent_v2_summary.json`
- `data/brahmi/source_token_family_descent_summary_v2.csv`
- `data/brahmi/brahmi_independent_source_token_gate_v3_summary.json`

Generated files:

- `data/open_prototype/tools/anchored_constraint_collapse_stress.mjs`
- `data/open_prototype/reports/anchored_constraint_collapse_stress.csv`
- `data/open_prototype/reports/anchored_constraint_collapse_stress_summary.json`

## Result

The strict exact-sequence-collapsed Lipi working corpus has 571 observed signs. With no accepted external value anchor, every way of assigning labels to those signs is equally allowed, so the lower-bound label-symmetry degeneracy is:

```text
log2(571!) = 4410.970864 bits
```

Accepted-anchor scenario:

| Scenario | Distinct fixed signs | Residual bits | Reduction |
| --- | ---: | ---: | ---: |
| Accepted anchors only | 0 | 4410.970864 | 0.000000 |

Weak rejected-anchor stress:

| Scenario | Forced assignments | Residual bits | Reduction | Decision |
| --- | ---: | ---: | ---: | --- |
| Kish `me-luh-ha` length/pattern candidate | 3 | 4383.506414 | 27.464450 | inadmissible |
| Failaka `ma2-me-luh-ha` length/pattern candidate | 4 | 4374.356667 | 36.614197 | inadmissible |
| Failaka `lu2-sun2-zi-da` length/pattern candidate | 4 | 4374.356667 | 36.614197 | inadmissible |
| Failaka `szu-i3-li2-su` length/pattern candidate | 4 | 4374.356667 | 36.614197 | inadmissible |
| One weak Brahmi `220` neighbor | 1 | 4401.813517 | 9.157347 | inadmissible |
| Failaka ship candidate plus one weak Brahmi `220` neighbor | 5 | 4365.209462 | 45.761402 | inadmissible |
| Brahmi v2 top near-miss set | 5 | 4365.209462 | 45.761402 | inadmissible |
| `U17649` object-level onomastic attempt | 6 | 4356.064804 | 54.906060 | inadmissible |
| `U17649` onomastic attempt plus Brahmi v2 near-miss set | 11 | 4310.379871 | 100.590993 | inadmissible |

The object-level onomastic harness adds the strongest explicit rejected external assignment so far: `002=ur;004=gun3;328=a;001=me;803=luh;415=ha` from forcing `ur gun3-a me-luh-ha` onto `3898.1/U17649`. It is inadmissible because `U17649` is Indus-only, the cuneiform phrase is a separate Ur text, and the target-site shuffle forger reproduces the observed strict mapped same-site pattern attempt with share `0.6857`.

The expanded Brahmi source-token gate adds no admissible anchor. Its strongest rejected stress set forces `817=dhya;527=ra;472=ra;060=ka;061=ra`, but those rows have already failed the v2 shape/label nulls, and v3 blocks every v2 family before visual review. The 2026-05-31 low-null autopsy closes the remaining real-token impostor loophole: all 21 rows with impostor share <= `0.01` still fail shape-null, 19 fail label-null, 11 fail minimum source-token independence, and zero pass both minimum independence and duplicate-collapse unanimity. The strongest combined rejected stress set fixes 11 signs and leaves `4310.379871` bits of label-symmetry degeneracy. That is not a collapse. It is not a partial reading.

## Idealized Lower Bound

Independent accepted anchors would reduce the label-symmetry floor slowly unless they also unlocked strong contextual propagation:

| Ideal accepted anchors | Residual bits | Reduction |
| ---: | ---: | ---: |
| 1 | 4401.813517 | 9.157347 |
| 5 | 4365.209462 | 45.761402 |
| 10 | 4319.511728 | 91.459136 |
| 20 | 4228.309541 | 182.661323 |
| 50 | 3956.292144 | 454.678720 |

## Decision

No anchored constraint collapse is accepted. A partial reading stays blocked because every available anchor is retracted, mutually fragile, or contradictory. What this note buys us is a guardrail: even if we forced the best current rejected object-level onomastic assignment together with the best rejected Brahmi near-misses, the effective-unicity problem would still not be solved.
