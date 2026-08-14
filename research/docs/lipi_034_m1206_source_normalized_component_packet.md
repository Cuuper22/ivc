# Lipi 034 M-1206 Source-Normalized Component Packet

Date: 2026-05-26

## Question

This note records one blind-review experiment and the decisions it earned. The numbers in strings like `+520-220-034+` are local numeric sign labels — transcription codes, not readings. "Source-visible" means readable directly in a published source photograph; a control is a known comparison crop we measure the target against; a singleton is a sequence attested only once.

The question: after adding `H-942 +520-220-016+` as a source-visible singleton control and excluding `M-1912` / `K-150` as non-source-grade, does the `M-1206 +520-220-034+` terminal — its final sign — still behave like the same source-visible graphic family as the clean `415` controls?

This is a sign-inventory experiment: it probes how many distinct signs there are, not what any sign means. It does not test meaning, phonetic value, grammar, or translation.

## Packet

A packet is the bundle handed to blind reviewers: anonymized ("neutral") crops with neutral IDs, a blank review sheet, and a master key that stays hidden until adjudication. Distractors are filler crops that should not match the target; they check that reviewers are not simply matching everything.

Primary neutral packet:

```text
tmp/m1206_034_next_source_normalized_blind_component_control_20260526/m1206_source_normalized_component_neutral_contact_sheet.png
tmp/m1206_034_next_source_normalized_blind_component_control_20260526/blind_review_sheet_blank.csv
tmp/m1206_034_next_source_normalized_blind_component_control_20260526/blind_master_key.csv
data/open_prototype/reports/lipi_034_m1206_source_normalized_component_packet_inputs.csv
```

Outcome reports:

```text
data/open_prototype/reports/lipi_034_m1206_source_normalized_component_packet_blind_reviews.csv
data/open_prototype/reports/lipi_034_m1206_source_normalized_component_packet_adjudication.csv
data/open_prototype/reports/lipi_034_m1206_source_normalized_component_packet_summary.json
```

Primary packet contents:

| Blind item | Unblinded role |
| --- | --- |
| `N002`, `N008` | `M-1206 A/a` target `034` terminal core |
| `N003`, `N011` | `H-938 A/A bis` clean exact-side `415` terminal control and same-side duplicate |
| `N006` | `H-940 A` secondary clean exact-side `415` terminal control |
| `N005` | `M-37 A` clean same-site `415` comb/rake recut |
| `N009` | `H-942 A` full source-visible `+520-220-016+` signband control, side-mapping caution |
| `N001`, `N004`, `N007`, `N010`, `N012` | Prefix/nonterminal distractors |

Appendix/quarantine contents:

| Appendix item | Status |
| --- | --- |
| `A001` | `M-1206 A+E` weaker composite target view |
| `A002` | `M-37 A` minimal isolation check, too context-poor for primary |
| `A003`, `A004` | `H-786 A`, `H-941 A` side-gated visual pressure only |
| `A005`-`A007` | Exploratory H-942 component crops, rejected as terminal evidence |

Hard exclusions:

```text
M-1912 = secondary visual/catalogue lead only, CISI 3.1/equivalent source still needed
K-150  = local metadata plus Bhaskar catalogue lead only, raw source still needed
```

## Blind Review Result

Two independent blind visual reviews — each reviewer classified the anonymized crops without knowing which object any crop came from — agreed on the key structure. "Unblinds to" means what the neutral ID turned out to be once the master key was opened:

| Blind result | Items | Adjudication |
| --- | --- | --- |
| Parallel vertical terminal family core | `N002`, `N008` | Unblinds to `M-1206 A/a`; the target terminal core survives. |
| Near vertical/top-band family | `N003`, `N011` | Unblinds to `H-938 A/A bis`; closest clean exact-side `415` pressure survives, but `A bis` is not independent. |
| Related but context-heavy / weaker vertical controls | `N005`, `N006` | Unblinds to `M-37 A` and `H-940 A`; M-37 is clean but distinct comb/rake-with-stem, H-940 is secondary/blurred. |
| Oblique/fork/triangular distractor families | `N001`, `N004`, `N007`, `N010`, `N012` | Distractor gate passes. The target/control relation is not generic prefix/nonterminal similarity. |
| Different evidence kind | `N009` | Unblinds to `H-942 A` full signband; both reviews reject treating it as a terminal-component crop. |

## Decision

Accepted:

```text
M-1206 A/a has a stable source-visible target terminal component.
H-938 A/A bis remains the closest clean exact-side 415 vertical-family pressure.
H-940 A remains weaker secondary exact-side 415 pressure.
M-37 A is now a clean same-site 415 control, but it is a distinct comb/rake-with-stem subform.
H-942 A can be used as a source-visible non-034/non-415 singleton signband control with side-mapping caution.
The prefix/nonterminal distractor gate passes.
```

Not accepted:

```text
034 = 415
034/415 allograph status
034 value
415 value
016 value
H-942 terminal-isolated evidence
M-1912 or K-150 as clean witnesses
translation
```

## Effect On The Branch

This packet preserves a bounded `034/415` visual-family question, but it does not cross the allograph threshold — the point at which we would treat `034` and `415` as two written forms of one sign. After the later `H-938 B` component probe, its positive scope is limited to M-1206 versus exact-side `415` controls such as `H-938 A/A bis` and `H-940 A`; it must not use the `H-938 B` companion side as component-level `034` evidence.

The active sign-inventory state is now sharper:

```text
M-1206 target terminal = stable vertical-bundle core
H-938 exact-side 415 = closest clean vertical-family control
H-940 exact-side 415 = weaker vertical-family control
M-37 exact-side same-site 415 = clean but comb/rake subtype
H-942 singleton 016 = source-visible signband negative control, not terminal-comparable
```

The best current interpretation is still a constrained open set:

```text
allograph / broad graphemic family
separate visual-family signs
source-side mapping artifact
transcription-policy split
```

No value or translation can be accepted from this branch yet.

## Next Gate

Stop expanding broad packets unless they add new source evidence. The next useful moves are:

1. Acquire source-grade `M-1912` from CISI 3.1 or an equivalent archive route.
2. Find an independent source-visible `034` witness that can be component-cropped without damage, medium, or side-policy failure.
3. Locate object-specific side-label tables for `H-786` and `H-941`.
4. If H-942 is to be used at terminal level, first create a defensible source-normalized recut and have reviewers classify it blind; the current accepted H-942 role is full-signband control only.

Accepted mappings, values, and translations remain:

```text
0
```
